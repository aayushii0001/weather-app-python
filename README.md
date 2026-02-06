# 🌦️ Smart Weather App (Python + PyQt5)

A desktop weather application built using **Python** and **PyQt5** that delivers real-time weather updates with intelligent city search.
The app is designed with a strong focus on **usability, performance, and error handling**, making it both lightweight and practical.

---

## 🚀 Features

✅ Real-time weather data using the OpenWeather API
✅ Intelligent city search with **fuzzy matching** (handles typos like *"delhi"* → *New Delhi*)
✅ Alias support for alternate city names (Bombay → Mumbai, Bangalore → Bengaluru)
✅ Regex-based input cleanup for better search accuracy
✅ Optimized dataset focused on Indian cities for faster lookup
✅ Clean and responsive GUI
✅ Weather emojis for quick visual understanding
✅ Robust exception handling for network/API errors

---

## 🛠️ Tech Stack

* **Python**
* **PyQt5** — Desktop GUI development
* **Requests** — API communication
* **JSON** — Structured city dataset
* **Difflib & Regex** — Intelligent search logic

---

## 📂 Project Structure

```
weather-app
│
├── weather_app.py
├── data/
│   └── indian_cities.json
├── requirements.txt
└── .gitignore
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```
git clone https://github.com/YOUR_USERNAME/weather-app.git
cd weather-app
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Add your OpenWeather API key

Open `weather_app.py` and replace:

```python
api_key = "YOUR_API_KEY"
```

with your actual API key.

👉 Get a free key from: [https://openweathermap.org/](https://openweathermap.org/)

### 4️⃣ Run the application

```
python weather_app.py
```

---

## 🎯 Key Learning Outcomes

This project strengthened my understanding of:

* GUI development with PyQt5
* API integration and data parsing
* Intelligent search algorithms
* Exception handling
* Writing maintainable, user-focused code
* Structuring production-like repositories

---

## 🔮 Future Improvements

* Auto-detect user location
* 5-day / hourly forecast
* Recent search history
* Dark mode
* Convert into a web-based version

---

## 💡 Why This Project Stands Out

Instead of building a basic weather app, this project focuses on **real user behavior**.

Users often:

* misspell city names
* use old city names
* type partial inputs

The intelligent matching system ensures the app still returns accurate results — improving overall user experience.

---

⭐ If you found this project interesting, consider giving it a star!
