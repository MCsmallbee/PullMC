@echo off
setlocal EnableExtensions
chcp 65001 >nul
pushd "%~dp0" || exit /b 1

set "PYTHON=py -3.13"
set "OUTPUT=dist\PullMC.dist"

echo [1/3] Checking Python 3.13...
%PYTHON% --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python 3.13 was not found. Install it or adjust PYTHON in build.bat.
    goto :fail
)

echo [2/3] Installing runtime and build dependencies...
%PYTHON% -m pip install --disable-pip-version-check --no-input -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies from requirements.txt.
    goto :fail
)

echo [3/3] Building PullMC with Nuitka...
if exist "dist\PullMC.dist" rmdir /s /q "dist\PullMC.dist"
if exist "dist\PullMC.build" rmdir /s /q "dist\PullMC.build"

rem Nuitka 4.3.5 strips binaries by default and has no --strip option.
%PYTHON% -m nuitka ^
    --standalone ^
    --lto=yes ^
    --jobs=8 ^
    --remove-output ^
    --assume-yes-for-downloads ^
    --enable-plugin=pyside6 ^
    --include-package=RinUI ^
    --include-package-data=RinUI ^
    --include-data-dir=pullmc/qml=pullmc/qml ^
    --include-data-dir=pullmc/i18n_data=pullmc/i18n_data ^
    --include-data-dir=pullmc/res=pullmc/res ^
    --nofollow-import-to=pytest ^
    --nofollow-import-to=pyinstaller ^
    --nofollow-import-to=setuptools ^
    --nofollow-import-to=pip ^
    --nofollow-import-to=wheel ^
    --nofollow-import-to=tests ^
    --nofollow-import-to=build ^
    --output-dir=dist ^
    --output-filename=PullMC.exe ^
    --windows-console-mode=disable ^
    --windows-icon-from-ico=pullmc/res/favicon.ico ^
    tools/PullMC.py

if errorlevel 1 (
    echo ERROR: Nuitka build failed.
    goto :fail
)

if not exist "%OUTPUT%\PullMC.exe" (
    echo ERROR: Build output was not found at %OUTPUT%\PullMC.exe.
    goto :fail
)

echo.
echo Build complete: %OUTPUT%\PullMC.exe
popd
exit /b 0

:fail
popd
exit /b 1
