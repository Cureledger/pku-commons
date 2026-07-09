# Benchmark report: `estimators.stub_estimator`

- **Run:** 2026-07-09T11:45:59.447013Z
- **Test set:** `testset/seed_v0.jsonl` (18 cases)
- **Tolerance band:** ±max(15.0 mg, 15% of truth)

## Metrics

| metric | value |
|---|---|
| MAE (mg) | 6.61 |
| Median AE (mg) | 0.0 |
| RMSE (mg) | 18.51 |
| Bias (mg, +over) | 6.56 |
| Within band | 88.9% |
| Crashed cases | 0 |

## Per-case

| id | case | truth mg | est mg | err mg | pass |
|---|---|--:|--:|--:|:--:|
| c01 | Raw banana, 1 medium (118 g) | 57.8 | 57.8 | 0.0 | pass |
| c02 | Raw apple, 1 medium w/o skin (180 g) | 12.6 | 12.6 | 0.0 | pass |
| c03 | Baby carrots, 85 g serving | 51.9 | 51.9 | 0.0 | pass |
| c04 | Cucumber slices, 100 g | 31.0 | 31.0 | 0.0 | pass |
| c05 | Strawberries, 144 g (1 cup) | 27.4 | 27.4 | 0.0 | pass |
| c06 | Broccoli florets, 91 g (1 cup) | 106.5 | 106.5 | 0.0 | pass |
| c07 | Cornstarch, 8 g (1 tbsp) | 1.0 | 1.0 | 0.0 | pass |
| c08 | Tapioca pearls dry, 30 g | 1.2 | 1.2 | 0.0 | pass |
| c09 | Diced tomato, 120 g | 32.4 | 32.4 | 0.0 | pass |
| c10 | Cooked white rice equiv, 45 g dry | 158.8 | 158.8 | 0.0 | pass |
| c11 | Fruit salad cup (apple+banana+strawberry | 46.4 | 50.0 | 3.6 | pass |
| c12 | Veggie sticks tray (carrot+cucumber), 15 | 69.0 | 69.0 | 0.0 | pass |
| c13 | Low-pro thickened fruit sauce (apple + c | 9.7 | 16.0 | 6.3 | pass |
| c14 | Tomato-broccoli medley, 180 g | 102.6 | 129.6 | 27.0 | FAIL |
| c15 | Banana-strawberry smoothie base (no dair | 77.8 | 85.0 | 7.2 | pass |
| c16 | Rice + carrot bowl (small), 130 g | 196.1 | 269.1 | 73.0 | FAIL |
| c17 | Tapioca-fruit pudding (tapioca + strawbe | 18.1 | 19.5 | 1.4 | pass |
| c18 | Cucumber-tomato side salad, 200 g | 58.4 | 58.0 | 0.4 | pass |
