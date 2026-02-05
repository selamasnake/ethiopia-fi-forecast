# Forecasting Financial Inclusion in Ethiopia

## Project Overview

This project builds a forecasting system to track Ethiopia's digital financial transformation using time series methods. The focus is on two core dimensions of financial inclusion, defined by the World Bank's Global Findex:

1. **Access** — Account ownership rate
2. **Usage** — Digital payment adoption rate

### Business Context

Ethiopia is rapidly digitizing financial services: Telebirr has over 54M users (since 2021), M-Pesa entered in 2023, and P2P digital transfers now surpass ATM withdrawals. Yet only 49% of adults have a financial account (2024 Findex). Selam Analytics is tasked with:

* Understanding drivers of financial inclusion
* Assessing impacts of events like product launches, policies, and infrastructure investments
* Forecasting Access and Usage trends for 2025–2027

## Project Structure

### Notebooks

* **`schema_exploration.ipynb`** — Explores dataset schema, pillars, record types, confidence, and sources
* **`data_enrichment.ipynb`** — Adds new observations, events, and impact links; saves enriched datasets and documents changes in `logs/data_enrichment_log.md`
* **`eda.ipynb`** — Performs exploratory data analysis, visualizes trends, correlations, and events; documents key insights, data gaps, and hypotheses
* **`event_impact_modeling.ipynb`** — Models how events (policies, product launches, infrastructure) affect financial inclusion indicators
* **`forecasting.ipynb`** — Builds trend and event-augmented forecasts for Access and Usage; generates scenario-based projections (Baseline, Optimistic, Pessimistic)


### Source Code (`src/`)

* **`eda.py`** — EDA class for loading, preprocessing, summarizing, and filtering data; provides helper methods for Task 2 analyses
* **`forecasting.py`** — `Forecaster` class: fits trend models, merges events and impacts, computes cumulative effects, generates scenario-based forecasts
* **`impact_model.py`** — `ImpactModel` class: maps impact magnitude, applies ramp/decay effects, calculates event-driven adjustments
* **`utils.py`** — Utility functions for data handling, date conversions, and plotting helpers
* **`dashboard/`** — Streamlit dashboard app: interactive visualizations for trends, forecasts, scenario analysis, and inclusion projections


### Tasks Overview

**Task 1: Data Acquisition & Schema Exploration**

* Load raw datasets, understand structure, identify pillars, record types, and confidence levels

**Task 2: Exploratory Data Analysis (EDA)**

* Summarize Access, Usage, Infrastructure, and Events
* Visualize correlations, gaps, and trends

**Task 3: Event & Impact Modeling**

* Build `ImpactModel`
* Merge events and impacts
* Compute cumulative event effects by year

**Task 4: Forecasting & Scenario Analysis**

* Fit linear trend models (`Forecaster`)
* Apply event-augmented adjustments
* Generate Baseline, Optimistic, and Pessimistic scenario forecasts

**Task 5: Dashboard Development**

* Create interactive Streamlit dashboard (`dashboard/app.py`)
* Sections: Overview, Trends, Forecasts, Inclusion Projections
* Visualizations: key metrics, interactive time series, scenario-based forecasts, confidence intervals, milestones
* Data download functionality for stakeholders

---

### Requirements

* Python 3.10+
* `pandas`, `numpy`, `scikit-learn`, `matplotlib`, `seaborn`, `plotly`, `streamlit`

---

### How to Run

**Environments**

```bash
# Create environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install requirements
pip install -r requirements.txt
```

**Jupyter Notebooks**

```bash
jupyter lab
# Open notebooks in order: schema_exploration → data_enrichment → eda → event_impact_modeling → forecasting 
```

**Streamlit Dashboard**

```bash
streamlit run dashboard/app.py
```