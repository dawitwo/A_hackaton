
## File — `reports/A_cleaning_and_integration.md`

```markdown
# Deliverable A — Cleaning & Integration

See `notebooks/01_cleaning_and_integration.ipynb` for full code.
Supporting CSVs: `A1_cleaning_log.csv`, `A2_label_proof.csv`,
`A5_join_proof.csv`, `A6_feature_table.csv`.

## A1 Cleaning log
See table `reports/A1_cleaning_log.csv`.

## A2 Label standardization
All three tables now use the identical set:
`Amhara, Oromia, SNNPR, Somali, Tigray`.
Plot + price tables use: `barley, maize, sorghum, teff, wheat`.

## A3 Join map
- plot (left) → weather (right) on `region` + `year` + `month` inside
  4-month growing window (planting month + 3).
  Cardinality: plot 1 → many weather rows (aggregated to 1 row per plot).
- plot (left) → prices (right) on `region` + `crop_type` + `year`.
  Cardinality: many-to-one.

## A4 Join audit
- Weather: dedup 232 → 226 rows (duplicates removed).
- Plot → weather: no rows dropped, no unmatched plots in train or test.
- Weather join produced one row per plot; season_months_count reports
  how many months were actually matched.
- Plot → price: match rate reported in Notebook 02.

## A5 Join proof
See `reports/A5_join_proof.csv` — raw monthly weather rows for 3 sample
plots and the resulting aggregated season numbers.

## A6 Feature engineering
See `reports/A6_feature_table.csv`.

## A7 Integrity checks
See the printed PASS/FAIL output at the end of Notebook 01.