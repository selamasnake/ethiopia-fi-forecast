import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from impact_model import ImpactModel

class Forecaster:
    """Handles trend fitting, event augmentation, and scenario-based forecasting."""

    def __init__(self, target_obs, impacts, main):
        """Initialize with target observations, impact links, and main dataset."""
        self.target_obs = target_obs
        self.impacts = impacts
        self.main = main
        self.trend_models = {}
        self.trend_predictions = {}
        self.impact_model = ImpactModel(ramp=12, decay=False)
        self.impact_full = None

    def fit_trend_models(self, targets, forecast_years, min_points=2):
        # Fit linear trends
        self.forecast_years = forecast_years
        for code in targets:
            df = self.target_obs[self.target_obs['indicator_code'] == code]
            df = df.dropna(subset=['value_numeric'])  # make sure NaNs are removed

            print(f"DEBUG: {code} has {len(df)} rows before dropping NaNs")  

            if len(df) < min_points:
                print(f"⚠️ Not enough points for {code}, using last observation with simple growth")
                if len(df) == 2:
                    last_value, prev_value = df['value_numeric'].iloc[-1], df['value_numeric'].iloc[-2]
                    growth = last_value - prev_value
                else:
                    growth = 0
                self.trend_predictions[code] = np.array([
                    df['value_numeric'].iloc[-1] + growth*(i) for i in range(len(forecast_years))
                ])
                continue

            # Standard linear regression trend if enough points
            X = df['year'].values.reshape(-1, 1)
            y = df['value_numeric'].values
            model = LinearRegression()
            model.fit(X, y)

            self.trend_models[code] = model
            self.trend_predictions[code] = model.predict(np.array(forecast_years).reshape(-1,1))
            print(f"✅ Fitted trend for {code}")

    # def fit_trend_models(self, targets, forecast_years, min_points=2):
    #     self.forecast_years = forecast_years
    #     for code in targets:
    #         df = self.target_obs[self.target_obs['indicator_code']==code]
    #         print(f"DEBUG: {code} has {len(df)} rows before dropping NaNs")
    #         df = df.dropna(subset=['value_numeric'])
    #         print(f"DEBUG: {code} has {len(df)} rows after dropping NaNs")
    #         if len(df) < min_points:
    #             print(f"⚠️ Skipping {code}: only {len(df)} data point(s)")
    #             continue
    #         X = df['year'].values.reshape(-1,1)
    #         y = df['value_numeric'].values
    #         print(f"DEBUG: X = {X.ravel()}, y = {y}")
    #         model = LinearRegression()
    #         model.fit(X, y)
    #         self.trend_models[code] = model
    #         self.trend_predictions[code] = model.predict(np.array(forecast_years).reshape(-1,1))
    #         print(f"✅ Fitted trend for {code}")


    def merge_events(self):
        """Merge event records with impacts and compute event years."""
        events = self.main[self.main['record_type']=='event'][['record_id','observation_date']]
        events = events.rename(columns={'observation_date':'event_date'})
        self.impact_full = self.impacts.merge(
            events, left_on='parent_id', right_on='record_id', how='left'
        )
        self.impact_full['event_date'] = pd.to_datetime(self.impact_full['event_date'])
        self.impact_full['event_year'] = self.impact_full['event_date'].dt.year

    def cumulative_event_effect(self, year, indicator_code, scale=1.0):
        """Compute total event impact for a given year, indicator, and scale."""
        if self.impact_full is None:
            self.merge_events()
        effects = self.impact_full[self.impact_full['related_indicator']==indicator_code]
        total = 0
        for _, row in effects.iterrows():
            t = (year - row['event_year']) * 12
            if t < 0: continue
            mag = self.impact_model.map_magnitude(row['impact_magnitude'])
            signed = mag * (1 if row['impact_direction']=="increase" else -1)
            total += scale * self.impact_model.event_effect(
                t=t, t_event=0, lag=row['lag_months'], magnitude=signed
            )
        return total

    def generate_forecasts(self, targets, forecast_years, scenarios):
        """Generate scenario-based forecasts combining trends and event effects."""
        self.merge_events()
        rows = []
        for code, preds in self.trend_predictions.items():
            for i, year in enumerate(forecast_years):
                trend = preds[i]
                for scenario, scale in scenarios.items():
                    event_effect = self.cumulative_event_effect(year, code, scale)
                    forecast = trend + event_effect
                    forecast = min(max(forecast,0),100)  # clamp to 0–100%
                    rows.append({
                        "indicator": code,
                        "year": year,
                        "scenario": scenario,
                        "forecast_value": forecast
                    })
        return pd.DataFrame(rows)
