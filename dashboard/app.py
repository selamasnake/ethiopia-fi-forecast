# dashboards/app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from forecaster import Forecaster  # your module from earlier
from datetime import datetime

# ---------------------------
# Load Data
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/enriched_data.csv", parse_dates=['observation_date'])
    return df

data = load_data()

# ---------------------------
# Sidebar Navigation
# ---------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Trends", "Forecasts", "Projections"])

# Scenario selector
SCENARIOS = {"Pessimistic": 0.5, "Baseline": 1.0, "Optimistic": 1.5}

# ---------------------------
# Helper Functions
# ---------------------------
def plot_time_series(df, indicators, year_range=None):
    filtered = df[df['indicator_code'].isin(indicators)]
    if year_range:
        filtered = filtered[(filtered['year'] >= year_range[0]) & (filtered['year'] <= year_range[1])]
    fig = px.line(filtered, x='year', y='value_numeric', color='indicator_code', markers=True,
                  labels={'year':'Year','value_numeric':'Value','indicator_code':'Indicator'})
    fig.update_layout(legend_title_text='Indicator', hovermode='x unified')
    return fig

def download_button(df, filename="data.csv"):
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Data", csv, file_name=filename, mime='text/csv')

# ---------------------------
# Overview Page
# ---------------------------
if page == "Overview":
    st.title("Financial Inclusion Dashboard - Overview")

    latest_year = data['year'].max()
    latest_data = data[data['year'] == latest_year]

    # Key metrics
    col1, col2, col3 = st.columns(3)
    acc_own = latest_data.loc[latest_data['indicator_code']=='ACC_OWNERSHIP','value_numeric'].values[0]
    crossover = latest_data.loc[latest_data['indicator_code']=='USG_CROSSOVER','value_numeric'].values[0]
    p2p_count = latest_data.loc[latest_data['indicator_code']=='USG_P2P_COUNT','value_numeric'].values[0]
    
    col1.metric("Account Ownership (%)", f"{acc_own:.1f}")
    col2.metric("P2P/ATM Crossover Ratio", f"{crossover:.2f}")
    col3.metric("Digital Payment Users (count)", f"{int(p2p_count):,}")

    st.subheader("Largest Event Drivers")
    st.markdown("- Mobile money interoperability\n- Telecom competition\n- Digital ID rollout")

    st.subheader("Key Uncertainties")
    st.markdown("- Survey vs administrative data mismatch\n- Regional heterogeneity\n- Behavioral adoption vs access")

# ---------------------------
# Trends Page
# ---------------------------
elif page == "Trends":
    st.title("Trends")

    indicators = st.multiselect("Select indicators to visualize", 
                                options=data['indicator_code'].unique(),
                                default=["ACC_OWNERSHIP","USG_P2P_COUNT","USG_CROSSOVER"])

    min_year, max_year = int(data['year'].min()), int(data['year'].max())
    year_range = st.slider("Select year range", min_year, max_year, (min_year, max_year))

    if indicators:
        fig = plot_time_series(data, indicators, year_range)
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Forecasts Page
# ---------------------------
elif page == "Forecasts":
    st.title("Forecasts")
    
    forecast_years = list(range(datetime.now().year, datetime.now().year + 5))
    scenario = st.selectbox("Select scenario", options=list(SCENARIOS.keys()))
    scale = SCENARIOS[scenario]

    # Initialize forecaster
    target_codes = ["ACC_OWNERSHIP","USG_P2P_COUNT"]
    forecaster = Forecaster(data, impacts=pd.DataFrame(), main=pd.DataFrame())  # update impacts/main if available
    forecaster.fit_trend_models(target_codes, forecast_years)

    # Generate forecasts
    df_forecast = forecaster.generate_forecasts(target_codes, forecast_years, {scenario: scale})

    st.subheader(f"Forecasts ({scenario} Scenario)")
    st.dataframe(df_forecast[['indicator','year','forecast_value']])

    # Plot
    fig = px.line(df_forecast, x='year', y='forecast_value', color='indicator', markers=True,
                  labels={'year':'Year','forecast_value':'Forecast Value','indicator':'Indicator'})
    st.plotly_chart(fig, use_container_width=True)

    download_button(df_forecast, filename=f"forecasts_{scenario}.csv")

# ---------------------------
# Projections Page
# ---------------------------
elif page == "Projections":
    st.title("Financial Inclusion Projections")

    scenario = st.selectbox("Select scenario", options=list(SCENARIOS.keys()))
    scale = SCENARIOS[scenario]

    target_codes = ["ACC_OWNERSHIP"]
    forecast_years = list(range(datetime.now().year, datetime.now().year + 10))

    forecaster = Forecaster(data, impacts=pd.DataFrame(), main=pd.DataFrame())
    forecaster.fit_trend_models(target_codes, forecast_years)
    df_proj = forecaster.generate_forecasts(target_codes, forecast_years, {scenario: scale})

    st.subheader(f"Account Ownership Projections ({scenario} Scenario)")
    fig = px.line(df_proj, x='year', y='forecast_value', markers=True, 
                  labels={'year':'Year','forecast_value':'Account Ownership (%)'})
    fig.add_hline(y=60, line_dash="dash", line_color="red", annotation_text="60% Target")
    st.plotly_chart(fig, use_container_width=True)

    download_button(df_proj, filename=f"projections_{scenario}.csv")
