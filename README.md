# Auto Patcher for ReVanced

Automated system to patch YouTube ReVanced using GitHub Actions or manually on your local machine.

---

## 1. Automated Patching via GitHub Actions (Recommended)

The workflow automatically checks for the latest ReVanced Patches daily. If a new update is available, it will automatically build and create a GitHub Release containing the patched APK.

### Initial Setup (One-time):
1. **Fork** this repository to your GitHub account.
2. **Configure Keystore for APK Signing (Optional):**
   * If you want to use your own keystore to overwrite previous installations, convert your `revanced.keystore` file to a Base64 string:
     * **Windows (PowerShell):**
       ```powershell
       [Convert]::ToBase64String([System.IO.File]::ReadAllBytes("path/to/revanced.keystore"))
       ```
   * Go to your GitHub repository: **Settings** -> **Secrets and variables** -> **Actions** -> **New repository secret**.
   * Create a new secret named `KEYSTORE_BASE64` and paste the Base64 string.
   *(If this secret is not configured, ReVanced CLI will automatically generate a random keystore to sign the APK).*
3. **Configure Discord Notifications (Optional):**
   * If you want to receive notifications on Discord when a new build is released, create a Discord Webhook in your server.
   * Add a new GitHub Secret named `DISCORD_WEBHOOK` and paste the Webhook URL.

### How to Run:
* **Automated:** The workflow runs automatically at **00:00 UTC daily** (only builds when new Patches are released).
* **Manual (Force Build):** Go to the **Actions** tab -> Select **Auto Patch YouTube** -> Click **Run workflow**. This will force a rebuild and overwrite the APK in the current Release even if there are no new updates (useful when you modify the patch configuration).

### Customizing Patches:
Edit the `scripts/config.json` file in your repository to enable/disable specific patches:
* `include_patches`: Patches you want to enable (equivalent to `-e`).
* `exclude_patches`: Patches you want to disable (equivalent to `-d`).

---

## 2. Manual Patching (Local Machine)

### Requirements:
* OS: Windows / Linux / macOS.
* Java JDK 17 or later and Python 3 installed.

### Steps:
1. Place the following files in the `resources/` directory:
   * `re-cli.jar` (Download the latest `-all.jar` from GitHub ReVanced CLI).
   * `patches.rvp` (Download from ReVanced Patches).
   * `yt.apk` (Download the original YouTube APK with the compatible version from APKMirror).
   * `revanced.keystore` (Your keystore file).
2. Run `build.bat` (on Windows) or execute the patch command directly:
   ```bash
   java -jar resources/re-cli.jar patch \
     -b --purge \
     -p resources/patches.rvp \
     --keystore=resources/revanced.keystore \
     -e "Remove screen capture restriction" -e "Remove screenshot restriction" \
     -d "Disable player popup panels" -d "Spoof app version" -d "Enable debugging" \
     -o output/youtube_revanced_patched.apk \
     resources/yt.apk
   ```
3. The patched APK will be saved in the `output/` directory.