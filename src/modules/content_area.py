from kivy.uix.boxlayout import BoxLayout

class ContentArea(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def swap_content(self, new_content):
        self.clear_widgets()
        self.add_widget(new_content)