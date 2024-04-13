@echo off
setlocal

REM Read settings from .env file
for /f "tokens=1* delims==" %%a in (.env) do (
    if "%%a"=="SOURCE_PATH" set "SOURCE_PATH=%%b"
    if "%%a"=="DESTINATION_PATH" set "DESTINATION_PATH=%%b"
)

REM Check if source and destination paths are set
if not defined SOURCE_PATH (
    echo SOURCE_PATH is not set in .env file.
    exit /b 1
)
if not defined DESTINATION_PATH (
    echo DESTINATION_PATH is not set in .env file.
    exit /b 1
)

REM Copy the file
echo Copying %SOURCE_PATH% to %DESTINATION_PATH%
copy /y "%SOURCE_PATH%" "%DESTINATION_PATH%"

REM Check if the file was copied successfully
if errorlevel 1 (
    echo Error occurred while copying the file.
    exit /b 1
) else (
    echo File copied successfully.
)

REM Open the copied file
echo Opening the copied file...
start "" "%DESTINATION_PATH%\Plugin.as"

endlocal
