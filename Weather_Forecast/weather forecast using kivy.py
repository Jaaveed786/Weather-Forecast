import requests
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics.texture import Texture
import plyer

# API key from OpenWeatherMap
API_KEY = "your_openweathermap_api_key"


class WeatherApp(App):
    def build(self):
        self.icon = 'weather_icon.png'
        self.title = 'Live Weather Forecast'

        # Main layout
        layout = BoxLayout(orientation='vertical')

        # TextInput for entering location
        self.location_input = TextInput(hint_text='Enter location (City, State, Country)', size_hint=(1, 0.1))
        layout.add_widget(self.location_input)

        # Weather details
        self.weather_label = Label(text='Weather Information', size_hint=(1, 0.7))
        layout.add_widget(self.weather_label)

        # Update weather button
        update_btn = Button(text='Update Weather', size_hint=(1, 0.1))
        update_btn.bind(on_press=self.update_weather)
        layout.add_widget(update_btn)

        # Save data button
        save_btn = Button(text='Save Data', size_hint=(1, 0.1))
        save_btn.bind(on_press=self.save_data)
        layout.add_widget(save_btn)

        # Set background image or video
        self.set_background()

        return layout

    def set_background(self):
        # Placeholder for setting live wallpaper
        pass

    def update_weather(self, instance):
        location = self.location_input.text
        if location:
            weather_data = self.get_weather_data(location)
            if weather_data:
                self.display_weather(weather_data)

    def get_weather_data(self, location):
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            return response.json()
        except Exception as e:
            self.weather_label.text = f"Error: {e}"
            return None

    def display_weather(self, data):
        try:
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            visibility = data['visibility']
            feels_like = data['main']['feels_like']
            uv_index = self.get_uv_index(data['coord']['lat'], data['coord']['lon'])

            weather_info = (
                f"Weather: {weather}\n"
                f"Temperature: {temperature}°C\n"
                f"Feels Like: {feels_like}°C\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} m/s\n"
                f"Visibility: {visibility} m\n"
                f"UV Index: {uv_index}"
            )
            self.weather_label.text = weather_info
        except KeyError:
            self.weather_label.text = "Error retrieving weather data."

    def get_uv_index(self, lat, lon):
        try:
            url = f"http://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid=34ce23a572a01e8e1bc0f9617565cd31"
            response = requests.get(url)
            return response.json()['value']
        except Exception as e:
            return "N/A"

    def save_data(self, instance):
        try:
            with open('weather_data.txt', 'w') as file:
                file.write(self.weather_label.text)
            self.weather_label.text = "Weather data saved successfully!"
        except Exception as e:
            self.weather_label.text = f"Error saving data: {e}"


if __name__ == '__main__':
    WeatherApp().run()
