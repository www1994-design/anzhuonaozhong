[app]
title = 我的提醒
package.name = reminderapp
package.domain = org.kivy

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 1.0.0

# ⚠️ 关键：依赖列表，一定要包含 plyer 和 ctparse
requirements = python3,kivy,kivymd,plyer,ctparse,sqlite3

# 权限（Android 13+ 需要 POST_NOTIFICATIONS）
android.permissions = POST_NOTIFICATIONS,INTERNET,VIBRATE,WAKE_LOCK,ACCESS_NETWORK_STATE

# API 级别
android.api = 31
android.minapi = 21

android.enable_androidx = True
android.gradle_dependencies = androidx.core:core:1.6.0

# 注册后台服务（服务类名需与代码匹配）
services = ReminderService:service.py

log_level = 2
android.debug = True

[buildozer]
log_level = 2
warn_on_root = 1