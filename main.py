from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock

from database import ReminderDB
from nlp_parser import NLPParser
from notification_helper import send_reminder_notification

KV = '''
MDScreenManager:
    id: screen_manager
    MainScreen:
        name: "main"
    AddReminderScreen:
        name: "add_reminder"

<MainScreen>:
    name: "main"
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(10)
        spacing: dp(10)

        MDTopAppBar:
            title: "📅 我的提醒"
            elevation: 4
            right_action_items: [["plus", lambda x: root.go_to_add()]]

        ScrollView:
            MDList:
                id: reminder_list
                spacing: dp(8)
                padding: dp(8)

        MDRaisedButton:
            text: "检查待提醒事件"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            on_release: app.check_reminders()

<AddReminderScreen>:
    name: "add_reminder"
    MDBoxLayout:
        orientation: "vertical"
        padding: dp(16)
        spacing: dp(16)

        MDTopAppBar:
            title: "添加提醒"
            elevation: 4
            left_action_items: [["arrow-left", lambda x: root.go_back()]]

        MDTextField:
            id: input_text
            hint_text: "输入提醒内容，如：明天下午3点在公司会议室开会"
            multiline: True
            size_hint_y: None
            height: dp(120)

        MDRaisedButton:
            text: "智能解析并添加"
            pos_hint: {"center_x": 0.5}
            size_hint_x: 0.8
            on_release: app.parse_and_add()

        MDCard:
            orientation: "vertical"
            padding: dp(12)
            size_hint_y: None
            height: dp(200)
            spacing: dp(4)

            MDLabel:
                text: "解析预览"
                font_style: "H6"

            MDLabel:
                id: preview_time
                text: "时间: 未解析"
                theme_text_color: "Secondary"

            MDLabel:
                id: preview_location
                text: "地点: 未解析"
                theme_text_color: "Secondary"

            MDLabel:
                id: preview_title
                text: "标题: 未解析"
                theme_text_color: "Secondary"
'''


class MainScreen(MDScreen):
    def go_to_add(self):
        self.manager.current = "add_reminder"

    def refresh_list(self, reminders):
        list_widget = self.ids.reminder_list
        list_widget.clear_widgets()
        if not reminders:
            list_widget.add_widget(
                MDLabel(text="暂无提醒，点击右上角➕添加",
                        halign="center", theme_text_color="Secondary")
            )
            return
        for r in reminders:
            card = MDCard(
                orientation="vertical",
                padding=dp(10),
                size_hint_y=None,
                height=dp(80),
                md_bg_color=(0.95, 0.95, 0.95, 1)
            )
            title_label = MDLabel(text=f"📌 {r[1]}", font_style="H6", size_hint_y=None, height=dp(30))
            info = f"⏰ {r[4]}"
            if r[3]:
                info += f"  📍 {r[3]}"
            info_label = MDLabel(text=info, theme_text_color="Secondary", size_hint_y=None, height=dp(25))
            card.add_widget(title_label)
            card.add_widget(info_label)
            list_widget.add_widget(card)


class AddReminderScreen(MDScreen):
    def go_back(self):
        self.manager.current = "main"
        self.ids.input_text.text = ""
        self.ids.preview_time.text = "时间: 未解析"
        self.ids.preview_location.text = "地点: 未解析"
        self.ids.preview_title.text = "标题: 未解析"


class ReminderApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = ReminderDB()
        self.parser = NLPParser()
        self.dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Indigo"
        return Builder.load_string(KV)

    def on_start(self):
        self.load_reminders()
        Clock.schedule_interval(self.check_reminders, 60)

    def load_reminders(self):
        reminders = self.db.get_all_reminders()
        main_screen = self.root.get_screen("main")
        main_screen.refresh_list(reminders)

    def parse_and_add(self):
        add_screen = self.root.get_screen("add_reminder")
        text = add_screen.ids.input_text.text.strip()
        if not text:
            self.show_dialog("提示", "请输入提醒内容")
            return
        parsed = self.parser.parse(text)
        add_screen.ids.preview_time.text = f"时间: {parsed['time'] or '未识别'}"
        add_screen.ids.preview_location.text = f"地点: {parsed['location'] or '未识别'}"
        add_screen.ids.preview_title.text = f"标题: {parsed['title']}"
        if parsed['time']:
            self.db.add_reminder(parsed['title'], text, parsed['location'], parsed['time'])
            self.show_dialog("成功", f"✅ 提醒已添加！\n时间: {parsed['time']}")
            self.load_reminders()
            add_screen.go_back()
        else:
            self.show_dialog("提示", "⚠️ 未能识别出有效时间，请包含具体时间信息")

    def check_reminders(self, *args):
        pending = self.db.get_pending_reminders()
        for r in pending:
            send_reminder_notification(r)

    def show_dialog(self, title, text):
        if self.dialog:
            self.dialog.dismiss()
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDFlatButton(text="确定", on_release=lambda x: self.dialog.dismiss())]
        )
        self.dialog.open()


if __name__ == "__main__":
    ReminderApp().run()