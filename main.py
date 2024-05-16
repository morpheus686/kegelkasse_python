from kivymd.app import MDApp
from kivymd.uix.button import MDButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.textfield import MDTextField


class TestApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"

        screen = MDScreen()

        label = MDLabel(text="Huhu")
        screen.add_widget(label)
        btn_flat = MDButton()
        screen.add_widget(btn_flat)
        icon_label = MDIcon(icon="language-python")
        icon_label.icon_color = "red"
        screen.add_widget(icon_label)
        textfield = MDTextField("Enter user")
        screen.add_widget(textfield)

        return screen


if __name__ == '__main__':
    TestApp().run()
