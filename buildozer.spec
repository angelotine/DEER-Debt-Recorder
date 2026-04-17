[app]
# (str) Title of your application
title = DEER Debt Recorder

# (str) Package name
package.name = deer

# (str) Package domain (needed for android packaging)
package.domain = org.deloria

# (str) Source code where the main.py live
source.dir = .

# (list) List of inclusions using pattern matching
source.include_exts = py,png,jpg,kv,json

# (str) Application version
version = 0.1

# (list) Application requirements
# Note: sqlite3 is usually built-in, but including it here for safety.
requirements = python3,kivy==2.3.0,hostpython3,setuptools

# (str) Custom source folders for requirements
# (list) Garden requirements
# (list) Internal substitutions

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/logo.png

# (str) Presplash of the application
presplash.filename = %(source.dir)s/assets/logo.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# --- Android specific ---

[android]
# (list) Permissions (COMBINED INTO ONE LINE)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 34

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK version to use
android.ndk = 26b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded)
#android.ndk_path =

# (str) Android SDK directory (if empty, it will be automatically downloaded)
#android.sdk_path =

# (str) ANT directory (if empty, it will be automatically downloaded)
#android.ant_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid any automated update while building apk
android.skip_update = False

# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only.
android.accept_sdk_license = True

# (str) Android entry point, default is main.py
android.entrypoint = main.py

# (list) Android architectures to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a

# (bool) Allow backup of app data
android.allow_backup = True

# --- Buildozer specific ---

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 0

# (str) Path to build artifacts (default is ./.buildozer)
#build_dir = ./.buildozer

# (str) Path to bin directory (default is ./bin)
#bin_dir = ./bin