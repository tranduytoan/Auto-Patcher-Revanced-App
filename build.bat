@echo off

echo Try to delete old 'temp' folder if exist...
rd /s /q temp
md temp
cd ./temp

REM select app to patch
echo Select app to patch (1: Youtube, 2: YT Music, 3: Google Photos):
set /p app=Input app number: 

REM check Revanced's resources files
call :checkFileIsExist re-cli.jar
call :checkFileIsExist patches.jar
call :checkFileIsExist inte.apk

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
    set app_name=youtube_revanced_
    set out=%app_name%%version%.apk

    java -jar ../resources/re-cli.jar patch ^
    -b ../resources/patches.jar ^
    -m ../resources/inte.apk ^
    -i remove-screen-capture-restriction -i remove-screenshot-restriction ^
    -e always-autorepeat -e comments -e disable-fullscreen-panels -e disable-player-popup-panels -e spoof-app-version -e enable-debugging ^
    -o %out% ^
    ../resources/yt.apk
goto:eof

:patchYoutubeMusic
    REM input version
    set /p version=Input youtube music version (E.g: v.3.39.50):

    REM if input is null
    if "%version%"=="" (
        set "version=unknow_version"
        echo Use default value: %version%
    )
    set app_name=youtube_music_revanced_
    set out=%app_name%%version%.apk

    java -jar ../resources/re-cli.jar patch ^
    -b ../resources/patches.jar ^
    -m ../resources/inte.apk ^
    -o %out% ^
    ../resources/yt-music.apk
goto:eof

:patchGooglePhotos
    REM input version
    set /p version=Input google photos version (E.g: v.6.93.0):

    REM if input is null
    if "%version%"=="" (
        set "version=unknow_version"
        echo Use default value: %version%
    )
    set app_name=google_photos_revanced_
    set out=%app_name%%version%.apk

    java -jar ../resources/re-cli.jar patch ^
    -b ../resources/patches.jar ^
    -m ../resources/inte.apk ^
    -o %out% ^
    ../resources/photos.apk
goto:eof

:checkFileIsExist
    set file_name=%1
    echo Checking resources file: %file_name%
    if exist ../resources/%file_name% (
        echo %file_name% found
    ) else (
        echo ERROR: %file_name% not found
        pause
        exit
    )
goto:eof