import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file('whatever.kv')
class MyGrid(Widget):


    name = ObjectProperty(None)
    pizza = ObjectProperty(None)
    '''def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)

        self.cols = 1

        self.top_grid = GridLayout()
        
        self.top_grid.cols = 2

        self.add_widget(Image(source = "Slug.png"))
        
        self.top_grid.add_widget(Label(text = "Student Name"))
        self.s_name = TextInput(multiline = False)
        self.top_grid.add_widget(self.s_name)


        self.top_grid.add_widget(Label(text = "Student Gender"))
        self.s_gender = TextInput()
        self.top_grid.add_widget(self.s_gender)

        self.add_widget(self.top_grid)

        self.press = Button(text = "CLICK ME", font_size = 40, size_hint_y = None, height = 100)
        self.press.bind(on_press = self.click_me)
        self.add_widget(self.press)'''

    def press(self):
        name = self.name.text
        pizza = self.pizza.text
        print(f'{name} and {pizza}')

        self.name.text = ""
        self.pizza.text = ""
        
        '''if self.name.text != '':
            print(f"name of student is {self.name.text}")
            self.add_widget(Label(text = "thank you for your input"))

            self.s_name.text = '''''


class Awe(App):
    def build(self):
        return MyGrid()
if __name__ == "__main__":
    Awe().run()

