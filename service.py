import time
from datetime import datetime
from jnius import autoclass
import sqlite3

PythonActivity = autoclass('org.kivy.android.PythonActivity')
Context = autoclass('android.content.Context')


def get_db():
    # 注意：包名请修改为你的实际包名（buildozer.spec中定义的）
    return sqlite3.connect('/data/data/org.kivy.reminderapp/files/reminders.db')


def send_notification(title, message):
    try:
        context = PythonActivity.mActivity
        NotificationManager = autoclass('android.app.NotificationManager')
        NotificationCompat = autoclass('androidx.core.app.NotificationCompat')
        NotificationChannel = autoclass('android.app.NotificationChannel')
        BuildVersion = autoclass('android.os.Build$VERSION')

        notification_manager = context.getSystemService(Context.NOTIFICATION_SERVICE)

        channel_id = "reminder_channel"
        if BuildVersion.SDK_INT >= 26:
            channel = NotificationChannel(
                channel_id,
                "提醒通知",
                NotificationManager.IMPORTANCE_HIGH
            )
            notification_manager.createNotificationChannel(channel)

        builder = NotificationCompat.Builder(context, channel_id)
        builder.setContentTitle(title)
        builder.setContentText(message)
        builder.setSmallIcon(autoclass("android.R$drawable").ic_dialog_info)
        builder.setDefaults(NotificationCompat.DEFAULT_ALL)
        builder.setPriority(NotificationCompat.PRIORITY_HIGH)

        notification_manager.notify(int(time.time()), builder.build())
        return True
    except Exception as e:
        print(f"Service notification error: {e}")
        return False


def check_and_notify():
    try:
        conn = get_db()
        cursor = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        cursor.execute('''
                       SELECT id, title, description, location, reminder_time
                       FROM reminders
                       WHERE reminder_time <= ?
                         AND is_completed = 0
                       ''', (now,))
        reminders = cursor.fetchall()
        for r in reminders:
            title = f"⏰ {r[1]}"
            msg = r[2] or "待办提醒"
            if r[3]:
                msg += f" @ {r[3]}"
            send_notification(title, msg)
            cursor.execute('UPDATE reminders SET is_completed = 1 WHERE id = ?', (r[0],))
            conn.commit()
        conn.close()
    except Exception as e:
        print(f"Check error: {e}")


if __name__ == "__main__":
    while True:
        check_and_notify()
        time.sleep(60)