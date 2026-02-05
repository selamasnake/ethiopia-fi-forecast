## Source Modules Overview

This folder contains Python modules used for preprocessing and EDA.

### Modules

* `eda.py`: Load, clean, and perform exploratory analysis on datasets.
* `impact_model.py` — Encapsulates event–indicator impact logic, including:
    - Mapping qualitative impact magnitudes to numeric weights
    - Computing lagged ramped effects of events
    - Reusable class-based interface for modeling and forecasting event impacts
