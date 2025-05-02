🌍 NASA Earth Object Tracking

This project fetches Near-Earth Object (NEO) data from NASA's public API and stores asteroid and close-approach information in a MySQL database for further analysis.

🚀 Features

- Fetches NEO data for a specific date range from NASA's API.

- Extracts detailed information about each asteroid including size, magnitude, and hazard status.

- Tracks close-approach metrics like velocity, distance from Earth, and orbiting body.

- Stores the data into two MySQL tables: asteroids and close_approach.

🧰 Technologies Used

- Python 3.x

- requests – for API interaction

- mysql-connector-python – to connect Python with MySQL

- MySQL – for structured data storage

- NASA NEO API – source of real-time asteroid data

# 🚀 NASA Asteroid Tracker 🌠

A Streamlit-based interactive dashboard that connects to a MySQL database to display and analyze asteroid approach data provided by NASA. The application allows users to filter asteroid approaches and execute predefined queries for data insights.

## 🔧 Features

- 🔍 **Filter Criteria**:
  - Absolute Magnitude range
  - Estimated Diameter (min/max)
  - Relative Velocity (km/h)
  - Astronomical Unit
  - Date Range
  - Hazardous Status (Yes/No)

- 📊 **Predefined Queries** (15 options), including:
  - Count asteroid approaches
  - Average velocity per asteroid
  - Fastest asteroids
  - Monthly approach statistics
  - Closest approaches
  - Brightest and largest asteroids
  - Hazardous vs. non-hazardous breakdown

- 📁 **Data Source**:
  - MySQL database with tables: `asteroids`, `close_approach`

## 🖥️ Tech Stack

- Python 🐍
- [Streamlit](https://streamlit.io/)
- MySQL
- Pandas
- `streamlit-option-menu`

📦 Installation

1. Clone this repository:
   git clone https://github.com/SenthilTimu/nasa-neo-tracker.git
   cd nasa-neo-tracker
   
2. Install dependencies:
   pip install requests mysql-connector-python
   
3. Make sure you have a MySQL server running and a database named nasa created:
   CREATE DATABASE nasa;
   
4. pip install streamlit pandas mysql-connector-python streamlit-option-menu

5. python -m venv env

6. C:\Nasa_Project\env\Scripts\Activate.ps1

7. streamlit run C:\Nasa_Project\env\Scripts\nasa.py
