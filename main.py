import kivy
from kivy.app import App
from kivy.uix.label import Label

kivy.require('1.10.1')


class NeuralRandom(App):
    def build(self):
        return Label(text='Hello World')


NeuralRandom().run()