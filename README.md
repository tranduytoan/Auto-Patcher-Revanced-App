# Auto Patcher for Revanced

A small Windows helper to run Revanced CLI and produce patched APKs.

Supported apps:
- YouTube
- YouTube Music
- Google Photos

Requirements:
- Windows
- Java Runtime (JRE) 11

Setup:
1. Put these files into the `resources/` folder:
	- `re-cli.jar` (Revanced CLI)
	- `patches.jar` (Revanced patches)
	- `inte.apk` (Revanced Integrations)
	- `yt.apk`, `yt-music.apk`, or `photos.apk` (original APKs)

Usage:
1. Open PowerShell or cmd in the project folder.
2. Run:

```
build.bat
```

Output:
- The patched APK will be saved to `output/`

Update resources:
- Replace files in `resources/` and run `build.bat` again.

Contribute:
- Pull requests welcome.