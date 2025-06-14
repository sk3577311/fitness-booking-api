# 🧘‍♀️ Fitness Studio Booking API

A simple FastAPI application to view, book, and manage fitness class bookings with a Bootstrap HTML frontend.

## 🚀 Features

- View upcoming fitness classes
- Book a class (with name, email, and class selection)
- Check bookings by email
- Bootstrap-powered frontend
- SQLite local database with `seed.sql` data

## 📦 Requirements

- Python 3.8+
- pip

## 🔧 Setup

```bash
git clone https://github.com/yourusername/fitness-booking-api.git or download the zip folder
cd fitness-booking-api # go into directory
python -m venv venv # Initailize virtual enviroment
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt # Install all required dependencies
uvicorn main:app --reload # start the server
```
