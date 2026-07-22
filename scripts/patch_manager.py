import os
import sys
import json
import re
import subprocess
import requests
from bs4 import BeautifulSoup

# Configuration
CONFIG_FILE = "scripts/config.json"
RESOURCES_DIR = "resources"
OUTPUT_DIR = "output"
PATCHES_API = "https://api.revanced.app/v5/patches"
CLI_RELEASES_API = "https://api.github.com/repos/ReVanced/revanced-cli/releases/latest"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

os.makedirs(RESOURCES_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_latest_patches_info():
    print("Fetching latest patches info...")
    r = requests.get(PATCHES_API, headers={"User-Agent": USER_AGENT})
    r.raise_for_status()
    return r.json()

def get_latest_release_tag():
    repo = os.environ.get("GITHUB_REPOSITORY")
    if not repo:
        return None
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {"User-Agent": USER_AGENT}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json().get("tag_name")
    return None

def download_file(url, dest_path):
    print(f"Downloading {url} -> {dest_path}...")
    headers = {"User-Agent": USER_AGENT}
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(dest_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def download_cli():
    print("Fetching latest revanced-cli release...")
    r = requests.get(CLI_RELEASES_API, headers={"User-Agent": USER_AGENT})
    r.raise_for_status()
    release_data = r.json()
    for asset in release_data.get("assets", []):
        if re.match(r"revanced-cli-.*-all\.jar", asset["name"]):
            download_file(asset["browser_download_url"], os.path.join(RESOURCES_DIR, "re-cli.jar"))
            return
    raise Exception("Could not find revanced-cli-*-all.jar in the latest release")

def get_latest_compatible_version(patches_file):
    print("Determining latest compatible YouTube version...")
    cmd = [
        "java", "-jar", os.path.join(RESOURCES_DIR, "re-cli.jar"),
        "list-versions", "-p", patches_file, "-b", "-f", "com.google.android.youtube"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        print(result.stderr)
        raise Exception("Failed to list compatible versions")
    
    versions = []
    for line in result.stdout.splitlines():
        match = re.match(r"^\s+([\d\.]+)", line)
        if match:
            versions.append(match.group(1))
    
    if not versions:
        raise Exception("No compatible YouTube versions found in patches")
    
    # Sort versions semantically
    def version_key(v):
        return [int(x) for x in v.split(".")]
    
    versions.sort(key=version_key)
    latest = versions[-1]
    print(f"Latest compatible YouTube version: {latest}")
    return latest

def download_youtube_apk(version):
    # We use a reliable APKMirror scraper logic or alternative APK source.
    # For stability, we scrape APKMirror for the specific version (nodpi, arm64-v8a/universal).
    print(f"Searching YouTube v{version} on APKMirror...")
    base_url = "https://www.apkmirror.com"
    search_url = f"{base_url}/apk/google-inc/youtube/youtube-{version.replace('.', '-')}-release/"
    headers = {"User-Agent": USER_AGENT}
    
    r = requests.get(search_url, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Find the variant that is nodpi and either arm64-v8a or universal
    variant_url = None
    for row in soup.find_all("div", class_="table-row"):
        cells = row.find_all("div", class_="table-cell")
        if len(cells) >= 4:
            variant_text = cells[0].text.strip()
            arch = cells[1].text.strip()
            dpi = cells[3].text.strip()
            if "nodpi" in dpi.lower() and ("arm64-v8a" in arch.lower() or "universal" in arch.lower() or "noarch" in arch.lower()):
                a_tag = cells[0].find("a", class_="accent_color")
                if a_tag:
                    variant_url = base_url + a_tag["href"]
                    break
                    
    if not variant_url:
        # Fallback to first variant if specific arch not found
        a_tags = soup.find_all("a", class_="accent_color")
        for a in a_tags:
            if "youtube" in a["href"] and "download" in a["href"]:
                variant_url = base_url + a["href"]
                break
                
    if not variant_url:
        raise Exception(f"Could not find download variant for YouTube version {version}")
        
    print(f"Found variant page: {variant_url}")
    r = requests.get(variant_url, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    
    download_btn = soup.find("a", class_="downloadButton")
    if not download_btn:
        raise Exception("Could not find download button on variant page")
        
    final_page_url = base_url + download_btn["href"]
    print(f"Found final download page: {final_page_url}")
    
    r = requests.get(final_page_url, headers=headers)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    
    # Find the actual direct download link
    direct_link_tag = soup.find("a", id="download-link")
    if not direct_link_tag:
        # Try to find any link with "key=" or "force=true"
        for a in soup.find_all("a"):
            if a.get("href") and ("key=" in a["href"] or "force=true" in a["href"]):
                direct_link_tag = a
                break
                
    if not direct_link_tag:
        raise Exception("Could not find direct download link")
        
    direct_url = base_url + direct_link_tag["href"]
    download_file(direct_url, os.path.join(RESOURCES_DIR, "yt.apk"))

def patch_apk(config_file, patches_file):
    print("Patching APK...")
    with open(config_file, "r") as f:
        config = json.load(f)
        
    cmd = [
        "java", "-jar", os.path.join(RESOURCES_DIR, "re-cli.jar"),
        "patch",
        "-b", "--purge",
        "-p", patches_file,
    ]
    
    # Add keystore if exists
    keystore_path = os.path.join(RESOURCES_DIR, "revanced.keystore")
    if os.path.exists(keystore_path):
        cmd.append(f"--keystore={keystore_path}")
        
    for p in config.get("include_patches", []):
        cmd.extend(["-e", p])
    for p in config.get("exclude_patches", []):
        cmd.extend(["-d", p])
        
    cmd.extend([
        "-o", os.path.join(OUTPUT_DIR, "youtube_revanced_patched.apk"),
        os.path.join(RESOURCES_DIR, "yt.apk")
    ])
    
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise Exception("Patching failed")
    print("Patching completed successfully!")

def main():
    patches_info = get_latest_patches_info()
    latest_patches_ver = patches_info["version"]
    print(f"Latest ReVanced Patches version: {latest_patches_ver}")
    
    # Check if we already built this version
    latest_release = get_latest_release_tag()
    print(f"Latest release tag in repo: {latest_release}")
    
    # Download CLI and Patches first to determine YouTube version
    patches_file = os.path.join(RESOURCES_DIR, "patches.rvp")
    download_file(patches_info["download_url"], patches_file)
    download_cli()
    
    yt_version = get_latest_compatible_version(patches_file)
    expected_tag = f"youtube-v{yt_version}-patches-{latest_patches_ver}"
    
    if latest_release == expected_tag:
        print(f"Version {expected_tag} is already patched and released. Skipping.")
        # Write output variables for GitHub Actions to skip
        if "GITHUB_OUTPUT" in os.environ:
            with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                f.write("skip=true\n")
        sys.exit(0)
        
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            f.write("skip=false\n")
            f.write(f"yt_version={yt_version}\n")
            f.write(f"patches_version={latest_patches_ver}\n")
            f.write(f"release_tag={expected_tag}\n")
            
    download_youtube_apk(yt_version)
    patch_apk(CONFIG_FILE, patches_file)

if __name__ == "__main__":
    main()
