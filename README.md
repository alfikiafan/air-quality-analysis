# Air Quality Data Analysis Project

This repository contains a comprehensive data analysis project on **Air Quality Dataset**, covering the complete data analysis process from data gathering, cleaning, exploratory data analysis (EDA), to building a fully interactive dashboard using Streamlit.

## Project Overview

Air quality is an essential factor that affects public health and the environment. This project aims to analyze air pollution data from various monitoring stations to explore patterns, relationships, and key insights related to air quality in China.

We used a dataset that contains air quality data measured in several locations in China, including the concentrations of various pollutants like PM2.5, PM10, NO2, CO, SO2, O3, along with weather conditions like temperature (TEMP), dew point (DEWP), wind speed (WSPM), and precipitation (RAIN).

The key objectives of the project are:

- **Understand the effect of wind speed on PM2.5 concentrations during the summer months (June to August).**
- **Explore how NO2 and CO concentrations influence the overall air quality index (AQI) over the past three years in urban areas.**
- **Investigate the relationship between temperature, humidity, and pollutant concentrations (PM10, SO2) over the last five years.**
- **Provide a user-friendly dashboard to visualize the findings interactively.**

## Key Features

- **Data Wrangling:** The project includes data collection, cleaning, and preprocessing to prepare the dataset for analysis. The dataset used in this project consists of multiple CSV files representing different monitoring stations.
- **Exploratory Data Analysis (EDA):** Various plots and visualizations were created to explore the relationships between variables. Correlation heatmaps, scatter plots, and distribution analysis were used to uncover key insights.
- **Interactive Dashboard:** A fully functional dashboard created using Streamlit to visualize key findings interactively. The dashboard provides options for users to explore the data across different stations and timeframes.

## Dataset

The dataset used for this project is the **Air Quality Dataset** available from multiple monitoring stations. It contains the following information:

- **PM2.5**: Particulate matter smaller than 2.5 microns in diameter (µg/m³).
- **PM10**: Particulate matter smaller than 10 microns in diameter (µg/m³).
- **NO2**: Nitrogen dioxide (µg/m³).
- **CO**: Carbon monoxide (µg/m³).
- **SO2**: Sulfur dioxide (µg/m³).
- **O3**: Ozone (µg/m³).
- **TEMP**: Temperature (°C).
- **PRES**: Atmospheric pressure (hPa).
- **DEWP**: Dew point temperature (°C).
- **WSPM**: Wind speed (m/s).
- **RAIN**: Precipitation (mm).
- **Station**: Location of the monitoring station.
- **DateTime**: Date and time of the recording.

## Folder Structure

```plaintext
📂 Air-Quality-Data-Analysis
├── 📂 dashboard               # Streamlit dashboard scripts
├─────📄 dashboard.py          # Main dashboard script for Streamlit
├── 📂 data                    # Directory containing CSV files of air quality data from various stations
├── 📄 notebook.ipynb          # Jupyter notebooks for data analysis and visualization
├── 📄 README.md               # Overview of the project (this file)
├── 📄 requirements.txt        # List of Python packages required for the project
├── 📄 url.txt                 # URL to the dashboard deployment
```

## Running the Project

### Prerequisites

Make sure you have **Python 3.12** installed along with the following libraries:
- pandas
- numpy
- matplotlib
- seaborn
- plotly
- streamlit
- geopandas
- folium
- streamlit-folium
- scikit-learn
- tqdm

You can install all dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Running the Dashboard

1. Clone the repository:

```bash
git clone https://github.com/alfikiafan/air-quality-analysis.git
cd air-quality-analysis
```

2. Run the Streamlit dashboard:

```bash
cd dashboard
streamlit run dashboard.py
```

This will launch a local server where you can explore the air quality data interactively.

## Key Insights from the Analysis

1. **Wind Speed (WSPM) vs. PM2.5:**
   - Low wind speeds (< 1 m/s) are associated with higher concentrations of PM2.5, indicating that weak winds allow the particulate matter to accumulate in the atmosphere.
   - Higher wind speeds (> 3 m/s) slightly reduce PM2.5 concentrations, but the effect is limited.

2. **NO2 and CO Impact on AQI:**
   - Both NO2 and CO have a positive correlation with AQI. Higher concentrations of these pollutants lead to a significant deterioration in air quality.
   - Stations like Wanshouxigong report the highest levels of NO2 and CO, indicating higher pollution in these areas.

3. **Temperature and Humidity vs. PM10 and SO2:**
   - Higher temperatures are associated with an increase in PM10 concentrations, likely due to increased human activity or other environmental factors.
   - Higher humidity helps reduce SO2 concentrations, potentially due to the formation of acid rain that removes SO2 from the air.
