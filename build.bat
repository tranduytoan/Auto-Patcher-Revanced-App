@echo off

REM select app to patch
echo Select app to patch (1: Youtube, 2: YT Music, 3: Google Photos, 4: Spotify):
set /p app=Input app number: 

REM check Revanced's resources files
call :checkFileIsExist re-cli.jar
call :checkFileIsExist patches.rvp

if %app%==1 (
    call :checkFileIsExist yt.apk
    call :patchYoutube
    pause
    exit
) else if %app%==2 (
    call :checkFileIsExist yt-music.apk
    call :patchYoutubeMusic
    pause
    exit
) else if %app%==3 (
    call :checkFileIsExist photos.apk
    call :patchGooglePhotos
    pause
    exit
) else if %app%==4 (
    call :checkFileIsExist spotify.apk
    call :patchSpotify
    pause
    exit
) else (
    echo ERROR: Invalid app number
    pause
    exit
)


:patchYoutube
    REM input version
    set /p version=Input youtube version (E.g: v.19.09.37):

    REM if input is null
    if "%version%"=="" (
        set "version=unknow_version"
        echo Use default value: %version%
    )
    set out=output\youtube\youtube_revanced_%version%.apk

    java -jar resources/re-cli.jar patch ^
	-b --purge ^
    -p resources/patches.rvp ^
	--keystore=resources/revanced.keystore ^
    -e "Remove screen capture restriction" -e "Remove screenshot restriction" ^
    -d "Disable player popup panels" -d "Spoof app version" -d "Enable debugging" ^
    -o %out% ^
    resources/yt.apk
goto:eof

:patchYoutubeMusic
    REM input version
    set /p version=Input youtube music version (E.g: v.3.39.50):

    REM if input is null
    if "%version%"=="" (
        set "version=unknow_version"
        echo Use default value: %version%
    )
    set out=output\youtube_music\youtube_music_revanced_%version%.apk

    java -jar resources/re-cli.jar patch ^
	-b --purge ^
    -p resources/patches.rvp ^
	--keystore=resources/revanced.keystore ^
    -o %out% ^
    resources/yt-music.apk
goto:eof

:patchGooglePhotos
    REM input version
    set /p version=Input google photos version (E.g: v.6.93.0):

    REM if input is null
    if "%version%"=="" (
        set "version=unknow_version"
        echo Use default value: %version%
    )
    set out=output\google_photos\google_photos_revanced_%version%.apk

    java -jar resources/re-cli.jar patch ^
	-b --purge ^
    -p resources/patches.rvp ^
	--keystore=resources/revanced.keystore ^
    -o %out% ^
    resources/photos.apk
goto:eof

:patchSpotify
    REM input version
    set /p version=Input spotify version (E.g: v.9.0.26):

    REM if input is null
    if "%version%"=="" (
        set "version=unknow_version"
        echo Use default value: %version%
    )
    set out=output\spotify\spotify_revanced_%version%.apk

    java -jar resources/re-cli.jar patch ^
	-b --purge ^
    -p resources/patches.rvp ^
	--keystore=resources/revanced.keystore ^
    -o %out% ^
    resources/spotify.apk
goto:eof

:checkFileIsExist
    set file_name=%1
    echo Checking resources file: %file_name%
    if exist resources/%file_name% (
        echo %file_name% found
    ) else (
        echo ERROR: %file_name% not found
        pause
        exit
    )
goto:eof