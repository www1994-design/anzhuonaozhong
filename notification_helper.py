from plyer import notification

def send_notification(title, message, reminder_id=None):
    try:
        notification.notify(
            title=title,
            message=message,
            app_name="我的提醒",
            timeout=10
        )
        return True
    except Exception as e:
        print(f"通知发送失败: {e}")
        return False

def send_reminder_notification(reminder):
    title = f"⏰ {reminder[1]}"
    message = reminder[2] or "您有一条待办提醒"
    if reminder[3]:
        message += f" 📍 {reminder[3]}"
    return send_notification(title, message, reminder[0])