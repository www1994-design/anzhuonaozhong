[app]
title = 我的提醒
package.name = reminderapp
package.domain = org.kivy

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 1.0.0

# 精简依赖，先验证基础构建
requirements = python3,kivy,kivymd,plyer

android.permissions = POST_NOTIFICATIONS,INTERNET,VIBRATE,WAKE_LOCK,ACCESS_NETWORK_STATE
android.api = 31
android.minapi = 21

android.enable_androidx = True
android.gradle_dependencies = androidx.core:core:1.6.0

services = ReminderService:service.py

android.accept_sdk_license = True   # 关键，自动接受许可

log_level = 2
android.debug = True

[buildozer]
log_level = 2
warn_on_root = 1
