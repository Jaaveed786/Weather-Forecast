import json
import requests
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDRaisedButton
from kivy.lang import Builder
from kivymd.uix.dropdownitem import MDDropDownItem
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivymd.uix.spinner import MDSpinner
from kivymd.toast.kivytoast import toast


# image="""
# Image:
#     source:" Filename.ico "
#     pos_hint:{'center_x':.3,'center_y':.8}
#     size_hint:.1,.1"""

class CustomList(DropDown):
    pass
class WeatherApp(MDApp):
    def build(self):
        self.screen=Screen()
        self.l1=MDLabel(text='WEATHER FORECAST',halign='center',font_style='H4',theme_text_color='Custom',
                        text_color=(0,0,1,1),pos_hint={'center_x':0.5,'center_y':0.9})
        self.l2 = MDLabel(text='Select City : ', theme_text_color='Custom',
                          text_color=(0, 0, 1, 1), pos_hint={'center_x': 0.85, 'center_y':0.8})
        self.spr=Spinner(text='Click to select',values=('hyderabad','bangalore','chennai','mumbai'))
        self.spr.pos_hint={'center_x':0.57,'center_y':0.8}
        self.spr.size_hint=(0.2,0.06)
        self.spr.bind(text=self.on_spinner_select)
        self.a=self.on_spinner_select

        def get_data(x):
            city=self.spr.text
            if city=="Click to select":
                toast("Please select the city...",duration=4)
            else:
                data=requests.get(
                    "https://api.openweathermap.org/data/2.5/weather?q=" +city+ "&appid=5f95eca4e5fa6317ffc96cb40b021628").json()

                self.ll1.text=data["weather"][0]["main"]
                self.ll2.text = data["weather"][0]["description"]
                self.ll3.text = str((round(data["main"]["temp"]-273.15),0))
                self.ll4.text = str((round(data["main"]["temp_max"] - 273.15), 0))
                self.ll5.text = str((round(data["main"]["temp_min"] - 273.15), 0))
                self.ll6.text = str(data["main"]["pressure"])

        #self.img=Builder.load_string(image)
        self.l3=MDLabel(text="Climate : ",theme_text_color="Custom",text_color=(0,0,1,1),
                        size_hint=(.2,.05),pos_hint={'center_x':0.35,'center_y':0.7})
        self.l4 = MDLabel(text="Description : ", theme_text_color="Custom", text_color=(0, 0, 1, 1),
                          size_hint=(.2, .05), pos_hint={'center_x': 0.35, 'center_y': 0.63})
        self.l5 = MDLabel(text="Temperature : ", theme_text_color="Custom", text_color=(0, 0, 1, 1),
                          size_hint=(.2, .05), pos_hint={'center_x': 0.35, 'center_y': 0.56})
        self.l6 = MDLabel(text="Minimun Temp : ", theme_text_color="Custom", text_color=(0, 0, 1, 1),
                          size_hint=(.2, .05), pos_hint={'center_x': 0.35, 'center_y': 0.49})
        self.l7 = MDLabel(text="Maximum Temp: ", theme_text_color="Custom", text_color=(0, 0, 1, 1),
                          size_hint=(.2, .05), pos_hint={'center_x': 0.35, 'center_y': 0.41})
        self.l8 = MDLabel(text="Air Pressure : ", theme_text_color="Custom", text_color=(0, 0, 1, 1),
                          size_hint=(.2, .05), pos_hint={'center_x': 0.35, 'center_y': 0.33})

        self.ll1 = MDLabel(text="0", theme_text_color="Custom", text_color=(0, 0, 1, 1),
                          size_hint=(.2, .05), pos_hint={'center_x': 0.55, 'center_y': 0.7})
        self.ll2 = MDLabel(text="0", theme_text_color="Custom", text_color=(0, 0, 1, 1),
                          size_hint=(.2, .05), pos_hint={'center_x': 0.55, 'center_y': 0.63})
        self.ll3 = MDLabel(text="0", theme_text_color="Custom", text_color=(0, 0, 1, 1),
                          size_hint=(.2, .05), pos_hint={'center_x': 0.55, 'center_y': 0.56})
        self.ll4 = MDLabel(text="0", theme_text_color="Custom", text_color=(0, 0, 1, 1),
                          size_hint=(.2, .05), pos_hint={'center_x': 0.55, 'center_y': 0.49})
        self.ll5 = MDLabel(text="0", theme_text_color="Custom", text_color=(0, 0, 1, 1),
                          size_hint=(.2, .05), pos_hint={'center_x': 0.55, 'center_y': 0.41})
        self.ll6 = MDLabel(text="0", theme_text_color="Custom", text_color=(0, 0, 1, 1),
                          size_hint=(.2, .05), pos_hint={'center_x': 0.55, 'center_y': 0.33})
        self.bt2=MDRaisedButton(text="DONE",size_hint=(.1,.05),pos_hint={'center_x':0.80,'center_y':0.8})
        self.bt2.bind(on_press=get_data)
        self.spinnerSelection=MDLabel(text="%s"%self.spr.text)

        self.screen.add_widget(self.l1)
        self.screen.add_widget(self.spr)
        #self.screen.add_widget(self.img)
        self.screen.add_widget(self.l2)
        self.screen.add_widget(self.l3)
        self.screen.add_widget(self.l4)
        self.screen.add_widget(self.l5)
        self.screen.add_widget(self.l6)
        self.screen.add_widget(self.l7)
        self.screen.add_widget(self.l8)
        self.screen.add_widget(self.ll1)
        self.screen.add_widget(self.ll2)
        self.screen.add_widget(self.ll3)
        self.screen.add_widget(self.ll4)
        self.screen.add_widget(self.ll5)
        self.screen.add_widget(self.ll6)
        self.screen.add_widget(self.bt2)
        return self.screen
    def on_spinner_select(self,spinner,text):
        self.spinnerSelection.text=self.spr.text

WeatherApp().run()



