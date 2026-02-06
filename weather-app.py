import sys
import difflib
import re
import requests
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from requests import HTTPError, RequestException


class WeatherApp(QWidget):
    aliases = {
        "delhi": "new delhi",
        "bombay": "mumbai",
        "bangalore": "bengaluru",
        "madras": "chennai",
        "calcutta": "kolkata",
    }

    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        with open("data/indian_cities.json", "r", encoding="utf-8") as f:
            self.indian_cities = json.load(f)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;

            }
            QLineEdit#city_input{
                font-size: 40px;
            }

            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }

            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }

            QLabel#description_label{
                font-size: 50px;
            }
        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def find_city_id(self, name: str):
        """Find a city ID by name with alias, substring, and fuzzy matching."""
        if not name:
            return None, None

        q = name.strip().lower()

        # Alias substitution
        q = self.aliases.get(q, q)

        # Remove common suffixes like 'city', 'district'
        q = re.sub(r"\b(city|district)\b", "", q).strip()

        # Exact match
        for c in self.indian_cities:
            if c.get("name", "").lower() == q:
                return c["id"], c["name"]

        # Substring match (Meerut City -> Meerut)
        for c in self.indian_cities:
            if q in c.get("name", "").lower():
                return c["id"], c["name"]

        # Fuzzy match (handles typos like 'merut' → 'Meerut')
        city_names = [c.get("name", "") for c in self.indian_cities]
        matches = difflib.get_close_matches(q, [n.lower() for n in city_names], n=1, cutoff=0.8)
        if matches:
            match_name = matches[0]
            for c in self.indian_cities:
                if c.get("name", "").lower() == match_name:
                    return c["id"], c["name"]

        # Not found
        return None, None

    def get_weather(self):
        api_key = "YOUR_API_KEY"  # your key
        user_input = self.city_input.text()

        city_id, pretty_name = self.find_city_id(user_input)

        if not city_id:
            # Try OpenWeather text search as fallback
            url = f"https://api.openweathermap.org/data/2.5/weather?q={user_input},IN&appid={api_key}&units=metric"
        else:
            # Use city ID if found
            url = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&units=metric"

        url = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&units=metric"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Some responses return "cod" as string, some as int
            cod = int(data.get("cod", 0))
            if cod == 200:
                # Attach resolved display name to data so UI shows the canonical name
                data["_pretty_name"] = pretty_name
                self.display_weather(data)
            else:
                self.display_error(data.get("message", "Unknown error"))
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied")
                case 404:
                    self.display_error("Not found:\nCity not found")
                case 500:
                    self.display_error("Internal Server Error:\nPlease try again later")
                case 502:
                    self.display_error("Bad Gateway:\nInvalid response from the server")
                case 503:
                    self.display_error("Service Unavailable:\nServer is down")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred:\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects:\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)

    def display_weather(self, data):
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        city_name = data.get("_pretty_name") or data.get("name", "")

        # Pick an emoji
        d = desc.lower()
        if "cloud" in d:
            emoji = "☁️"
        elif "rain" in d or "drizzle" in d or "thunder" in d:
            emoji = "🌧️"
        elif "clear" in d:
            emoji = "☀️"
        elif "mist" in d or "fog" in d or "haze" in d or "smoke" in d:
            emoji = "🌫️"
        elif "snow" in d:
            emoji = "❄️"
        else:
            emoji = "🌍"

        self.temperature_label.setStyleSheet("font-size: 75px;")
        self.temperature_label.setText(f"{city_name}\n{temp:.1f}°C")
        self.emoji_label.setText(emoji)
        self.description_label.setText(desc.capitalize())



if __name__ == '__main__':
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())