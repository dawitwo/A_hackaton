import os, json
from pathlib import Path
import numpy as np
import pandas as pd
import joblib
import gradio as gr
import matplotlib.pyplot as plt

HERE = Path(__file__).parent
ASSETS = HERE / "assets"
MODEL = joblib.load(ASSETS / "final_model.joblib")
WEATHER = pd.read_csv(ASSETS / "season_weather.csv")
PRICES  = pd.read_csv(ASSETS / "price_table.csv")
AVG = pd.read_csv(ASSETS / "region_crop_avg.csv")

REGIONS = ["Amhara","Oromia","SNNPR","Somali","Tigray"]
CROPS   = ["barley","maize","sorghum","teff","wheat"]
MONTHS  = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTH_NUM = {m:i+1 for i,m in enumerate(MONTHS)}

FEATURES = ["altitude_m","rainfall_mm_season","farm_size_ha","fertilizer_kg_per_ha",
            "soil_quality_index","labor_days_per_ha","distance_to_market_km",
            "season_mean_temp","season_total_rain","season_extreme_heat",
            "season_months_count","temp_dev","rain_dev","fert_x_seed","planting_month_num",
            "region","crop_type"]

def weather_for(region, year, month):
    mnum = MONTH_NUM[month]
    rows = []
    for off in range(4):
        m = mnum + off
        y = year + (m - 1) // 12
        mm = (m - 1) % 12 + 1
        rows.append({"region":region,"year":y,"month":mm})
    df = pd.DataFrame(rows).merge(WEATHER, on=["region","year","month"], how="left")
    season_mean_temp    = df["avg_temp_c"].mean()
    season_total_rain   = df["monthly_rainfall_mm"].sum()
    season_extreme_heat = df["extreme_heat_days"].sum()
    season_months_count = df["avg_temp_c"].count()
    reg = WEATHER[(WEATHER["region"]==region)]
    region_year_temp = reg["avg_temp_c"].mean()
    region_year_rain = reg.groupby("year")["monthly_rainfall_mm"].sum().mean()
    return dict(season_mean_temp=season_mean_temp,
                season_total_rain=season_total_rain,
                season_extreme_heat=season_extreme_heat,
                season_months_count=season_months_count,
                temp_dev=season_mean_temp - region_year_temp,
                rain_dev=season_total_rain - region_year_rain)

def predict(region, crop, year, month, altitude, farm_size, fertilizer,
            improved_seed, pest_flag, soil_quality, labor_days, distance):
    try:
        w = weather_for(region, int(year), month)
    except Exception as e:
        return f"Could not look up weather: {e}", None

    row = {
        "altitude_m": altitude, "rainfall_mm_season": np.nan,
        "farm_size_ha": farm_size, "fertilizer_kg_per_ha": fertilizer,
        "soil_quality_index": soil_quality, "labor_days_per_ha": labor_days,
        "distance_to_market_km": distance,
        "planting_month_num": MONTH_NUM[month],
        "region": region, "crop_type": crop, "improved_seed_used": int(improved_seed),
        "pest_disease_flag": int(pest_flag),
        **{k: w[k] for k in ["season_mean_temp","season_total_rain","season_extreme_heat",
                             "season_months_count","temp_dev","rain_dev"]},
        "fert_x_seed": fertilizer * int(improved_seed),
    }
    X = pd.DataFrame([row])[FEATURES]
    pred = float(MODEL.predict(X)[0])

    pr = PRICES[(PRICES["region"]==region) & (PRICES["crop_type"]==crop) &
                (PRICES["year"]==int(year))]
    price = float(pr["price_birr_per_quintal"].iloc[0]) if len(pr) else float(
        PRICES[(PRICES["region"]==region) & (PRICES["crop_type"]==crop)]["price_birr_per_quintal"].mean())
    revenue = pred * farm_size * 10 * price

    lookup = (f"Season avg {w['season_mean_temp']:.1f} °C · "
              f"season rain {w['season_total_rain']:.0f} mm · "
              f"heat days {int(w['season_extreme_heat'])} · "
              f"price {price:,.0f} birr/quintal")

    avg = AVG[(AVG["region"]==region) & (AVG["crop_type"]==crop)]
    region_avg = float(avg["mean_yield"].iloc[0]) if len(avg) else float(AVG["mean_yield"].mean())

    fig, ax = plt.subplots(figsize=(5,3))
    ax.bar(["This plot", "Region-crop avg"], [pred, region_avg],
           color=["steelblue","lightgray"])
    ax.set_ylabel("yield (t/ha)"); ax.set_title("Prediction vs average")
    for i, v in enumerate([pred, region_avg]):
        ax.text(i, v, f"{v:.2f}", ha="center", va="bottom")
    plt.tight_layout()

    text = (f"Predicted yield: **{pred:.2f} t/ha**\n\n"
            f"Estimated revenue: **{revenue:,.0f} birr**  "
            f"({pred:.2f} t/ha × {farm_size} ha × 10 × {price:,.0f} birr/quintal)\n\n"
            f"Looked up: {lookup}")
    return text, fig

demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Dropdown(REGIONS, value="Oromia", label="Region"),
        gr.Dropdown(CROPS, value="maize", label="Crop"),
        gr.Dropdown([2021,2022,2023,2024], value=2024, label="Survey year"),
        gr.Dropdown(MONTHS, value="Jun", label="Planting month"),
        gr.Number(value=1800, label="Altitude (m)"),
        gr.Number(value=1.2, label="Farm size (ha)"),
        gr.Number(value=40, label="Fertilizer (kg/ha)"),
        gr.Checkbox(label="Improved seed used"),
        gr.Checkbox(label="Pest/disease flag"),
        gr.Slider(0, 1, value=0.6, label="Soil quality index"),
        gr.Number(value=45, label="Labor days/ha"),
        gr.Number(value=8, label="Distance to market (km)"),
    ],
    outputs=[gr.Markdown(label="Result"), gr.Plot(label="Comparison")],
    title="Crop-yield & revenue estimator (team dawit)",
    description="Enter plot details; weather and price are looked up automatically.",
)
if __name__ == "__main__":
    demo.launch()