# main.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDButton, MDButtonText

import hashlib
import base64
import random
from datetime import datetime, timedelta


class SerialGeneratorApp(MDApp):
    def build(self):
        self.title = "Serial Generator"
        Window.size = (400, 600)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.txt_prefix = TextInput(hint_text="Ship", multiline=False)
        self.txt_months = TextInput(hint_text="Use Months", multiline=False, input_filter='int')
        self.txt_computer_serial = TextInput(hint_text="Computer Serial", multiline=False)

        layout.add_widget(Label(text="Ship:", size_hint_y=None, height=20, color=(0.2,0.2,0.2,1)))
        layout.add_widget(self.txt_prefix)
        layout.add_widget(Label(text="Months:", size_hint_y=None, height=20, color=(0.2,0.2,0.2,1)))
        layout.add_widget(self.txt_months)
        layout.add_widget(Label(text="Comp Serial:", size_hint_y=None, height=20, color=(0.2,0.2,0.2,1)))
        layout.add_widget(self.txt_computer_serial)

        btn = MDButton(MDButtonText(text="Generate Serial"), style="elevated")
        btn.bind(on_release=self.generate)
        layout.add_widget(btn)

        self.output = TextInput(text='', readonly=True, multiline=True, hint_text="Generated serial will appear here")
        scroll = ScrollView(size_hint=(1, 0.5))
        scroll.add_widget(self.output)
        layout.add_widget(scroll)

        return layout

    def decode_b64(self, s):
        return base64.b64decode(s).decode("utf-8")

    def f4g5h6(self, s):
        h = hashlib.sha256(s.encode()).digest()
        b = base64.b64encode(h).decode()[:8].replace("/", "X").replace("+", "Y").upper()
        return b

    def scramble_date(self, date):
        return str(random.randint(10, 99)) + date[::-1]

    def generate(self, *args):
        try:
            p = self.txt_prefix.text.strip()
            m = self.txt_months.text.strip()
            c = self.txt_computer_serial.text.strip()

            if not p: raise Exception(self.decode_b64("UGxlYXNlIGVudGVyIGEgcHJlZml4Lg=="))
            if not m.isdigit() or int(m) <= 0: raise Exception(self.decode_b64("UGxlYXNlIGVudGVyIGEgdmFsaWQgbnVtYmVyIG9mIG1vbnRocy4="))
            if not c: raise Exception(self.decode_b64("UGxlYXNlIGVudGVyIHRoZSB1c2VyJ3MgY29tcHV0ZXIgc2VyaWFsIG51bWJlci4="))

            m = int(m)
            now = datetime.now()
            exp = now + timedelta(days=30*m)
            w = self.scramble_date(now.strftime("%Y%m%d")) + f"{random.randint(0,999999):06d}"
            x = self.f4g5h6(c)
            key = f"{p}-{w}-{x}"
            sha = hashlib.sha256(key.encode()).hexdigest().upper()[:16]
            serial = f"{p}-{w}-{x}-{sha}"

            self.output.text = serial
            self.show_popup("Success", self.decode_b64("U2VyaWFsIG51bWJlciBzdWNjZXNzZnVsbHkgY3JlYXRlZDo=") + "\n" + serial)
        except Exception as e:
            self.show_popup("Error", self.decode_b64("U2VyaWFsIGdlbmVyYXRpb24gZXJyb3I6") + " " + str(e))

    def show_popup(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[MDButton(MDButtonText(text="OK"), on_release=lambda x: dialog.dismiss())]
        )
        dialog.open()


SerialGeneratorApp().run()
