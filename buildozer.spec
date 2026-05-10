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
# Added 'txt' to include your requirements.txt just in case
source.include_exts = py,png,jpg,kv,json,txt

# (list) List of directory to include
# Added 'kv_files' so your UI logic isn't missing!
source.include_dirs = assets, kv_files

# (str) Application version
version = 0.1

# (list) Application requirements
# Added 'android' for system integration
requirements = python3,kivy==2.3.0,hostpython3,setuptools,android

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
# (list) Permissions (Included CALL_PHONE for your Call button)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, CALL_PHONE

# (int) Target Android API
android.api = 34

# (int) Minimum API your APK will support
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 34

# (str) Android NDK version to use
android.ndk = 26b

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (bool) If True, then automatically accept SDK license
android.accept_sdk_license = True

# (str) Android entry point, default is main.py
android.entrypoint = main.py

# (list) Android architectures to build for (Added armeabi-v7a for wider compatibility)
android.archs = arm64-v8a, armeabi-v7a

# (bool) Allow backup of app data
android.allow_backup = True

# --- Buildozer specific ---

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = off, 1 = on)
warn_on_root = 0
