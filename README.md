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


### Notebooks
* **`schema_exploration.ipynb`** — Explored dataset schema, pillars, record types, confidence, and sources  
* **`data_enrichment.ipynb`** — Addd new observations, events, impact links; save enriched datasets and document changes
* **`eda.ipynb`** — Performd exploratory data analysis, visualized trends, correlations, and events, and documentd key insights and data gaps

### Source Code (src/)
* **`eda.py`** — EDA class for loading, preprocessing, summarizing, and filtering data; provides helper methods for Task 2 analyses