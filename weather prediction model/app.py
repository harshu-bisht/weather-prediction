# app.py
# Author: Harshit Bisht
# Project: Weather Data Visualization (CSV Version)

from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

DATA_FILE = 'weather_data.csv'

@app.route('/', methods=['GET', 'POST'])
def index():
    df = pd.read_csv(DATA_FILE)
    cities = sorted(df['city'].unique())

    if request.method == 'POST':
        city = request.form['city']
        chart_path = create_chart(df, city)
        return render_template('result.html', city=city, chart_path=chart_path)
    
    return render_template('index.html', cities=cities)

def create_chart(df, city):
    city_data = df[df['city'].str.lower() == city.lower()]

    if city_data.empty:
        return None

    plt.figure(figsize=(10, 5))
    plt.plot(city_data['date'], city_data['temperature'], marker='o', color='tomato', label='Temperature (°C)')
    plt.plot(city_data['date'], city_data['humidity'], marker='s', color='dodgerblue', label='Humidity (%)')

    plt.title(f"Temperature & Humidity Trends in {city}")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    chart_path = os.path.join('static', 'weather_chart.png')
    plt.savefig(chart_path)
    plt.close()
    return chart_path

if __name__ == "__main__":
    app.run(debug=True)
