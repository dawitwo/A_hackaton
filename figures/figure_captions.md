# Figure captions

- **fig01_missingness.png** — Share of missing values per column across train, test, and weather. Shows that fertilizer, soil quality, and labor days are the main missing columns.
- **fig02_before_after_cleaning.png** — Distribution of farm_size_ha before and after capping the 99th percentile. Cleaning removes the long impossible tail without discarding rows.
- **fig03_yield_distribution.png** — Yield (t/ha) overall and by crop. Maize dominates the mean; teff and barley are lower-yield and tighter.
- **fig04_region_crop_heatmap.png** — Mean yield by region × crop with plot counts. Some cells are thin and shouldn't be over-interpreted.
- **fig05_correlation_heatmap.png** — Correlations between numeric plot features, weather-derived features, and yield. Season temperature and altitude stand out.
- **fig06_climate_by_region.png** — Monthly average temperature by region, with the typical kiremt growing window shaded. Regions separate cleanly in temperature.
- **fig07_yield_vs_season_temp.png** — Yield vs season mean temperature per crop. Several crops show a sweet spot rather than a monotonic trend.
- **fig08_price_trends.png** — Average price per quintal by year and crop. Prices rose across the board, but unevenly.
- **fig09_revenue_by_crop_region.png** — Estimated revenue per hectare by region and crop. The ranking differs from yield alone because prices differ.
- **fig10_model_comparison.png** — Validation RMSE for each model family, with the mean baseline marked and CV error bars on the winner.
- **fig11_predicted_vs_actual_residuals.png** — Predicted vs actual and residuals. Residuals fan out at higher yield, which the error analysis discusses.
- **fig12_feature_importance.png** — Permutation importances for top features, with weather-derived features highlighted in orange.
