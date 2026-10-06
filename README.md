# team_dawit — Qiyas Crop-Yield Hackathon

Solo submission by Dawit for the Qiyas / IADE Crop-Yield Challenge.

## Summary
Predict `yield_tons_per_ha` for 3,750 smallholder plots using plot
features, regional weather aggregated over a 4-month growing window,
and engineered features (temperature/rainfall deviations, fertilizer ×
seed interaction). Final model: tuned HistGradientBoosting inside a
scikit-learn pipeline. Revenue estimates in the demo use a separate
market price table (not used as a model feature).

**Final validation RMSE: see `reports/D_model_evaluation.md`.**

## Setup
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows
pip install -r requirements.txt
