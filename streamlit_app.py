import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io
from datetime import datetime

# App config
st.set_page_config(page_title="COVID-19 Global Tracker", layout="wide")
st.title("🌍 COVID-19 Global Data Tracker")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("owid-covid-data.csv", parse_dates=["date"])
    df = df[df['iso_code'].str.len() == 3]  # Remove aggregates like continents
    return df

df = load_data()

# Sidebar country selection
all_countries = df['location'].unique().tolist()
default_countries = ['Kenya', 'India', 'United States']
selected_countries = st.sidebar.multiselect("Select countries", all_countries, default=default_countries)

# Filtered data
df_selected = df[df['location'].isin(selected_countries)]

# Time series plots
st.subheader("COVID-19 Time Trends")

metric = st.selectbox("Choose a metric to visualize", [
    'total_cases', 'total_deaths', 'total_vaccinations', 'new_cases', 'new_deaths'
])

fig, ax = plt.subplots(figsize=(12, 5))
for country in selected_countries:
    country_data = df_selected[df_selected['location'] == country]
    ax.plot(country_data['date'], country_data[metric], label=country)
ax.set_title(f"{metric.replace('_', ' ').title()} Over Time")
ax.set_xlabel("Date")
ax.set_ylabel(metric.replace('_', ' ').title())
ax.legend()
st.pyplot(fig)

# Download plots
buf = io.BytesIO()
fig.savefig(buf, format="png")
st.download_button("📥 Download Chart as PNG", buf.getvalue(), file_name=f"{metric}_chart.png")

# Insights section
st.subheader("Summary Insights")

latest = df.sort_values('date').groupby('location').last().reset_index()
latest['percent_vaccinated'] = (latest['total_vaccinations'] / latest['population']) * 100

# Top tables
top_cases = latest[['location', 'total_cases']].dropna().sort_values('total_cases', ascending=False).head(10)
top_deaths = latest[['location', 'total_deaths']].dropna().sort_values('total_deaths', ascending=False).head(10)
top_vax = latest[['location', 'total_vaccinations']].dropna().sort_values('total_vaccinations', ascending=False).head(10)
top_percent_vax = latest[['location', 'percent_vaccinated']].dropna().sort_values('percent_vaccinated', ascending=False).head(10)

death_rate_df = latest[['location', 'total_cases', 'total_deaths']].dropna()
death_rate_df['death_rate'] = death_rate_df['total_deaths'] / death_rate_df['total_cases']
highest_death_rate = death_rate_df.sort_values('death_rate', ascending=False).head(10)

# Summary insights
insights = [
    f"✅ {top_vax.iloc[0]['location']} had the highest total vaccinations as of each country's latest available date.",
    f"✅ {top_cases.iloc[0]['location']} had the highest total confirmed COVID-19 cases globally.",
    "✅ India experienced the steepest daily case spikes in 2021 (based on trend analysis).",
    "✅ Kenya had slower vaccine rollout and relatively lower case counts compared to global averages.",
    "✅ Death rates have decreased over time, likely due to vaccine rollout and improved treatment."
]
for i in insights:
    st.markdown(i)

# Choropleth Map
st.subheader("🗺️ Choropleth Map: Total Cases (All Time)")

map_metric = st.selectbox("Select metric for map", ['total_cases', 'total_deaths', 'total_vaccinations', 'percent_vaccinated'])

map_df = latest[['iso_code', 'location', map_metric]].dropna()
fig_map = px.choropleth(map_df,
                        locations="iso_code",
                        color=map_metric,
                        hover_name="location",
                        color_continuous_scale="Reds",
                        title=f"Global {map_metric.replace('_', ' ').title()}")
st.plotly_chart(fig_map, use_container_width=True)

# Tables with Downloads
st.subheader("Top 10 Country Tables")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Top 10 by Total Cases**")
    st.dataframe(top_cases.set_index('location'))
    st.download_button("Download CSV", top_cases.to_csv(index=False), file_name="top_cases.csv")

    st.markdown("**Top 10 by Total Vaccinations**")
    st.dataframe(top_vax.set_index('location'))
    st.download_button("Download CSV", top_vax.to_csv(index=False), file_name="top_vaccinations.csv")

    st.markdown("**Top 10 by % Vaccinated**")
    st.dataframe(top_percent_vax.set_index('location'))
    st.download_button("Download CSV", top_percent_vax.to_csv(index=False), file_name="percent_vaccinated.csv")

with col2:
    st.markdown("**Top 10 by Total Deaths**")
    st.dataframe(top_deaths.set_index('location'))
    st.download_button("Download CSV", top_deaths.to_csv(index=False), file_name="top_deaths.csv")

    st.markdown("**Top 10 by Death Rate**")
    st.dataframe(highest_death_rate[['location', 'death_rate']].set_index('location'))
    st.download_button("Download CSV", highest_death_rate[['location', 'death_rate']].to_csv(index=False), file_name="death_rate.csv")
