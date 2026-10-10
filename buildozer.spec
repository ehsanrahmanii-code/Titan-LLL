[app]
title = Titan LLL
package.name = titanlll
package.domain = org.titanlll
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,txt,html,js,css,woff,ttf,md,gif,webp
version = 1.0.0
requirements = python3,flask,requests,urllib3,websocket-client,jinja2,werkzeug,markupsafe,itsdangerous,click,blinker,certifi,charset-normalizer,idna,six,setuptools
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,ACCESS_NETWORK_STATE,FOREGROUND_SERVICE
android.api = 33
android.minapi = 26
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a
android.allow_backup = True
android.presplash_color = #050816
android.bootstrap = webview
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 0
