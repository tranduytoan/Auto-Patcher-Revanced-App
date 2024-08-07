<h3 align="center">AUTO PATCHER FOR REVANCED'S APPLICATION</h3>

### This is a simple script that will automatically patch some Revanced applications for you (If you are interested in this script, you probably already know about Revanced. If not, you can find out more information [here](https://github.com/ReVanced))
The Revanced team only provides patches for users to create their own modified APK files. While pre-patched APKs can be found online, these sources may be unsafe and could contain malicious code. To help users patch their applications securely, the Revanced team offers two methods: the Command Line Interface (CLI) and the Revanced Manager.

I prefer using Revanced CLI due to its faster patching speed and customizable options. However, using the CLI can be cumbersome for those unfamiliar with command line operations or who find writing commands each time inconvenient. To simplify the process, I developed this program to automate patching Revanced applications.

### Supported Applications
- Youtube
- Youtube Music
- Google Photos

Currently, this program supports patching only these three Revanced applications, as they are the ones I use. I may add support for more applications in the future. If you understand code, feel free to check the [documentation](https://github.com/ReVanced/revanced-cli/tree/main/docs) and add additional functions yourself. Contributions are welcome, so don't hesitate to create a pull request (PR)!

### Requirements
- Windows
- Java Runtime Environment 11 ([Azul Zulu JRE](https://www.azul.com/downloads/?version=java-11-lts&package=jdk#zulu) or [OpenJDK](https://jdk.java.net/archive/))

More information about the requirements can be found [here](https://github.com/ReVanced/revanced-cli/blob/main/docs/0_prerequisites.md).

Here's a revised version of your "How to use" section with improved clarity and conciseness:

---

### How to Use

1. **Clone the Repository or Download the ZIP File:**
   - Clone this repository or download and extract the ZIP file.

2. **Gather Required Resources:**
   - **Original APK File:** Obtain the APK file of the application you want to patch.
   - **Revanced CLI JAR File:** Download the latest version from [here](https://github.com/revanced/revanced-cli/releases/latest).
   - **Revanced Patches JAR File:** Download the latest version from [here](https://github.com/revanced/revanced-cli/releases/latest).
   - **Integrations APK File:** Download the latest version from [here](https://github.com/revanced/revanced-integrations/releases/latest).

   **This step is crucial. Please read additional instructions [below](#more-about-step-2).**

3. **Run the `build.bat` File:**
   - Execute the `build.bat` file and follow the on-screen instructions.

4. **Retrieve the Patched APK:**
   - Find the patched APK file in the `temp` folder.

5. **Updating Resource Files:**
   - To update resources, simply replace the old files with the new ones.

### More About Step 2

- **Original APK File:** Download from a trusted source, such as [APKMirror](https://www.apkmirror.com), or another reliable source.
- **Supported Versions:** Ensure the APK files match supported versions. Refer to [CHANGELOG.md](https://github.com/ReVanced/revanced-patches/blob/v4.12.0/CHANGELOG.md) or [Revanced Patches](https://revanced.app/patches) for compatibility. YouTube may require specific versions, while other apps usually support all versions.
- **Renaming Resource Files:** After downloading, rename the files as follows:
  - Revanced CLI JAR: `re-cli.jar`
  - Revanced Patches JAR: `patches.jar`
  - Integrations APK: `inte.apk`
  - YouTube APK: `yt.apk`
  - YouTube Music APK: `yt-music.apk`
  - Google Photos APK: `photos.apk`
- **Organizing Files:** Place all renamed files in the `resources` folder. You can store multiple APK files for different applications simultaneously. Then, run the `build.bat` file.
- **Regular Updates:** Regularly check for new releases of Revanced CLI, Patches, and Integrations APKs to access the latest features.