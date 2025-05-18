# COVID-19_Global_Data_Tracker

## Description
This is a comprehensive **COVID-19 data analytics project** that tracks global cases, deaths, and vaccinations over time. The project includes:
- A **Jupyter Notebook** for exploratory data analysis (EDA), insights, and visualizations.
- An **interactive Streamlit dashboard** for real-time exploration and download of visual and tabular data.

The project leverages real-world data from [Our World in Data](https://ourworldindata.org/coronavirus-source-data) and includes tools like pandas, matplotlib, seaborn, and plotly.

## Features
- Import and clean global COVID-19 data
- Time series analysis of:
  - Total cases
  - Total deaths
  - Vaccination rollout
- Visualize:
  - Country comparisons
  - Daily new cases
  - Choropleth maps
- Download charts and tables (Streamlit)
- Summary insights with automated top-10 rankings
- Percent of population vaccinated included

## How to Use

### Jupyter Notebook
- Open `covid_tracker.ipynb` in Jupyter Lab or VS Code.
- Execute cells sequentially to view analysis and visualizations.

### Streamlit App
- Run the app:
```bash
streamlit run app.py
```
- Use sidebar to select countries and metrics.
- View dynamic charts, choropleth maps, insights, and download data.

### Dependencies
Install all required packages using:
```bash
pip install pandas matplotlib seaborn plotly streamlit
```
### Data Source
Our World in Data – COVID-19 Dataset