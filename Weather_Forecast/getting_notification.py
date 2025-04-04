import sys
import requests
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QProgressBar
from PyQt5.QtCore import QTimer, Qt

# Replace with your own API key and city
API_KEY = "your_openweathermap_api_key"
CITY = "your_city"

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.fetchWeatherData()

    def initUI(self):
        self.setWindowTitle('Weather Forecast')

        self.layout = QVBoxLayout()

        self.currentWeatherLabel = QLabel('Current Weather:', self)
        self.layout.addWidget(self.currentWeatherLabel)

        self.forecastLabel = QLabel('7-Day Forecast:', self)
        self.layout.addWidget(self.forecastLabel)

        self.progressBar = QProgressBar(self)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.progressBar)

        self.saveButton = QPushButton('Save Weather Data', self)
        self.saveButton.clicked.connect(self.saveWeatherData)
        self.layout.addWidget(self.saveButton)

        self.setLayout(self.layout)

        # Set up a timer to update the weather every 10 minutes (600000 milliseconds)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.fetchWeatherData)
        self.timer.start(600000)

    def fetchWeatherData(self):
        try:
            self.progressBar.setValue(0)
            self.progressBar.setMaximum(0)  # Indeterminate state
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast/daily?q={CITY}&cnt=7&appid={API_KEY}&units=metric"

            current_response = requests.get(current_url)
            forecast_response = requests.get(forecast_url)

            current_weather = current_response.json()
            forecast_weather = forecast_response.json()

            self.displayWeatherData(current_weather, forecast_weather)
            self.progressBar.setMaximum(100)  # Back to determinate state
            self.progressBar.setValue(100)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not fetch weather data: {e}")
            self.progressBar.setMaximum(100)  # Back to determinate state
            self.progressBar.setValue(0)

    def displayWeatherData(self, current_weather, forecast_weather):
        current_text = f"Current Weather:\n{current_weather['weather'][0]['description'].capitalize()}\n" \
                       f"Temperature: {current_weather['main']['temp']}°C\n" \
                       f"Humidity: {current_weather['main']['humidity']}%\n" \
                       f"Wind: {current_weather['wind']['speed']} m/s\n"

        forecast_text = "7-Day Forecast:\n"
        for day in forecast_weather['list']:
            forecast_text += f"Date: {day['dt']}\n" \
                             f"Weather: {day['weather'][0]['description'].capitalize()}\n" \
                             f"Temperature: {day['temp']['day']}°C\n" \
                             f"Humidity: {day['humidity']}%\n\n"

        self.currentWeatherLabel.setText(current_text)
        self.forecastLabel.setText(forecast_text)

    def saveWeatherData(self):
        weather_data = self.currentWeatherLabel.text() + "\n" + self.forecastLabel.text()
        with open("weather_forecast.txt", "w") as file:
            file.write(weather_data)
        QMessageBox.information(self, "Saved", "Weather forecast saved to weather_forecast.txt")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WeatherApp()
    ex.show()
    sys.exit(app.exec_())
