[app]

title = DEER Debt Recorder


package.name = deer


package.domain = org.deloria


source.dir = .


source.include_exts = py,png,jpg,kv,json,txt


source.include_dirs = assets, kv_files


version = 0.1


requirements = python3,kivy==2.3.0,hostpython3,setuptools,android


icon.filename = %(source.dir)s/assets/logo.png


presplash.filename = %(source.dir)s/assets/logo.png


orientation = portrait


fullscreen = 0



[android]

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, CALL_PHONE


android.api = 34


android.minapi = 21


android.sdk = 34


android.ndk = 26b


android.private_storage = True


android.accept_sdk_license = True


android.entrypoint = main.py


android.archs = arm64-v8a, armeabi-v7a


android.allow_backup = True



[buildozer]

log_level = 2


warn_on_root = 0
