# Benchmark report: `estimators.rubric_estimator`

- **Run:** 2026-07-11T17:10:55.894219Z
- **Test set:** `low_protein_usda.jsonl` (729 cases)
- **Tolerance band:** ±max(15.0 mg, 15% of truth)

## Metrics

| metric | value |
|---|---|
| MAE (mg) | 11.61 |
| Median AE (mg) | 9.3 |
| RMSE (mg) | 16.1 |
| Bias (mg, +over) | 7.29 |
| Within band | 69.5% |
| Crashed cases | 0 |

## Per-case

| id | case | truth mg | est mg | err mg | pass |
|---|---|--:|--:|--:|:--:|
| usda-169814 | Agave, raw | 19.0 | 23.5 | 4.5 | pass |
| usda-168749 | Alcoholic beverage, beer, light | 0.0 | 9.4 | 9.4 | pass |
| usda-168746 | Alcoholic beverage, beer, regular, all | 0.0 | 23.5 | 23.5 | FAIL |
| usda-173168 | Alcoholic beverage, creme de menthe, 72  | 0.0 | 0.0 | 0.0 | pass |
| usda-173664 | Alcoholic beverage, distilled, all (gin, | 0.0 | 0.0 | 0.0 | pass |
| usda-174815 | Alcoholic beverage, distilled, all (gin, | 0.0 | 0.0 | 0.0 | pass |
| usda-171919 | Alcoholic beverage, distilled, all (gin, | 0.0 | 0.0 | 0.0 | pass |
| usda-171920 | Alcoholic beverage, distilled, all (gin, | 0.0 | 0.0 | 0.0 | pass |
| usda-173663 | Alcoholic beverage, distilled, all (gin, | 0.0 | 0.0 | 0.0 | pass |
| usda-174817 | Alcoholic beverage, distilled, rum, 80 p | 0.0 | 0.0 | 0.0 | pass |
| usda-174818 | Alcoholic beverage, distilled, vodka, 80 | 0.0 | 0.0 | 0.0 | pass |
| usda-169020 | APPLEBEE'S, coleslaw | 17.0 | 26.4 | 9.4 | pass |
| usda-173930 | Apples, canned, sweetened, sliced, drain | 5.0 | 6.6 | 1.6 | pass |
| usda-171690 | Apples, dehydrated (low moisture), sulfu | 8.0 | 9.9 | 1.9 | pass |
| usda-173931 | Apples, dehydrated (low moisture), sulfu | 37.0 | 42.9 | 5.9 | pass |
| usda-171693 | Apples, dried, sulfured, stewed, with ad | 6.0 | 6.6 | 0.6 | pass |
| usda-171692 | Apples, dried, sulfured, stewed, without | 6.0 | 6.6 | 0.6 | pass |
| usda-171691 | Apples, dried, sulfured, uncooked | 26.0 | 29.7 | 3.7 | pass |
| usda-173932 | Apples, frozen, unsweetened, heated | 8.0 | 9.9 | 1.9 | pass |
| usda-171694 | Apples, frozen, unsweetened, unheated | 8.0 | 9.9 | 1.9 | pass |
| usda-168202 | Apples, raw, golden delicious, with skin | 7.0 | 9.9 | 2.9 | pass |
| usda-168201 | Apples, raw, red delicious, with skin | 7.0 | 9.9 | 2.9 | pass |
| usda-171688 | Apples, raw, with skin | 6.0 | 9.9 | 3.9 | pass |
| usda-171689 | Apples, raw, without skin | 7.0 | 9.9 | 2.9 | pass |
| usda-173929 | Apples, raw, without skin, cooked, micro | 8.0 | 9.9 | 1.9 | pass |
| usda-167773 | Applesauce, canned, sweetened, with salt | 5.0 | 6.6 | 1.6 | pass |
| usda-171696 | Applesauce, canned, sweetened, without s | 5.0 | 6.6 | 1.6 | pass |
| usda-167772 | Applesauce, canned, unsweetened, with ad | 5.0 | 6.6 | 1.6 | pass |
| usda-171695 | Applesauce, canned, unsweetened, without | 5.0 | 6.6 | 1.6 | pass |
| usda-171701 | Apricots, canned, extra heavy syrup pack | 23.0 | 28.2 | 5.2 | pass |
| usda-173938 | Apricots, canned, extra light syrup pack | 25.0 | 28.2 | 3.2 | pass |
| usda-171699 | Apricots, canned, heavy syrup pack, with | 22.0 | 23.5 | 1.5 | pass |
| usda-171700 | Apricots, canned, heavy syrup pack, with | 21.0 | 23.5 | 2.5 | pass |
| usda-173937 | Apricots, canned, juice pack, with skin, | 26.0 | 28.2 | 2.2 | pass |
| usda-173939 | Apricots, canned, light syrup pack, with | 22.0 | 23.5 | 1.5 | pass |
| usda-171698 | Apricots, canned, water pack, with skin, | 30.0 | 32.9 | 2.9 | pass |
| usda-173936 | Apricots, canned, water pack, without sk | 28.0 | 32.9 | 4.9 | pass |
| usda-173940 | Apricots, dehydrated (low-moisture), sul | 80.0 | 89.3 | 9.3 | pass |
| usda-173943 | Apricots, dried, sulfured, stewed, with  | 49.0 | 56.4 | 7.4 | pass |
| usda-173942 | Apricots, dried, sulfured, stewed, witho | 22.0 | 56.4 | 34.4 | FAIL |
| usda-171703 | Apricots, frozen, sweetened | 26.0 | 32.9 | 6.9 | pass |
| usda-171697 | Apricots, raw | 52.0 | 65.8 | 13.8 | pass |
| usda-170684 | Arrowroot flour | 12.0 | 15.6 | 3.6 | pass |
| usda-169314 | Asparagus, canned, no salt added, solids | 43.0 | 84.6 | 41.6 | FAIL |
| usda-169206 | Asparagus, canned, regular pack, solids  | 43.0 | 84.6 | 41.6 | FAIL |
| usda-171705 | Avocados, raw, all commercial varieties | 97.0 | 94.0 | 3.0 | pass |
| usda-171706 | Avocados, raw, California | 95.0 | 94.0 | 1.0 | pass |
| usda-170999 | Babyfood, banana with mixed berries, str | 35.0 | 47.0 | 12.0 | pass |
| usda-173519 | Babyfood, beverage, GERBER, GRADUATES, F | 2.0 | 0.0 | 2.0 | pass |
| usda-170967 | Babyfood, cereal, mixed, with applesauce | 62.0 | 32.9 | 29.1 | FAIL |
| usda-170966 | Babyfood, cereal, mixed, with applesauce | 63.0 | 32.9 | 30.1 | FAIL |
| usda-171363 | Babyfood, cereal, oatmeal, with applesau | 67.0 | 42.3 | 24.7 | FAIL |
| usda-171362 | Babyfood, cereal, oatmeal, with applesau | 66.0 | 42.3 | 23.7 | FAIL |
| usda-170970 | Babyfood, cereal, rice, with applesauce  | 58.0 | 56.4 | 1.6 | pass |
| usda-171364 | Babyfood, cereal, with egg yolks, junior | 92.0 | 89.3 | 2.7 | pass |
| usda-170971 | Babyfood, cereal, with egg yolks, strain | 92.0 | 89.3 | 2.7 | pass |
| usda-172317 | Babyfood, corn and sweet potatoes, strai | 53.0 | 61.1 | 8.1 | pass |
| usda-171379 | Babyfood, dessert, custard pudding, vani | 73.0 | 75.2 | 2.2 | pass |
| usda-170977 | Babyfood, dessert, dutch apple, junior | 6.0 | 9.4 | 3.4 | pass |
| usda-171374 | Babyfood, dessert, fruit pudding, orange | 42.0 | 51.7 | 9.7 | pass |
| usda-170998 | Babyfood, fruit, banana and strawberry,  | 53.0 | 32.9 | 20.1 | FAIL |
| usda-173487 | Babyfood, GERBER, 2nd Foods, apple, carr | 42.0 | 51.7 | 9.7 | pass |
| usda-168144 | Babyfood, grape juice, no sugar, canned | 17.0 | 0.0 | 17.0 | FAIL |
| usda-173478 | Babyfood, juice treats, fruit medley, to | 0.0 | 0.0 | 0.0 | pass |
| usda-170989 | Babyfood, mashed cheddar potatoes and br | 51.0 | 51.7 | 0.7 | pass |
| usda-173485 | Babyfood, snack, GERBER GRADUATE FRUIT S | 0.0 | 37.6 | 37.6 | FAIL |
| usda-172255 | Babyfood, tropical fruit medley | 8.0 | 14.1 | 6.1 | pass |
| usda-173505 | Babyfood, vegetables, beets, strained | 18.0 | 61.1 | 43.1 | FAIL |
| usda-173507 | Babyfood, vegetables, carrots, junior | 25.0 | 37.6 | 12.6 | pass |
| usda-173506 | Babyfood, vegetables, carrots, strained | 24.0 | 37.6 | 13.6 | pass |
| usda-171334 | Babyfood, vegetables, corn, creamed, jun | 49.0 | 65.8 | 16.8 | FAIL |
| usda-172280 | Babyfood, vegetables, corn, creamed, str | 49.0 | 65.8 | 16.8 | FAIL |
| usda-172272 | Babyfood, vegetables, green beans, junio | 49.0 | 56.4 | 7.4 | pass |
| usda-172271 | Babyfood, vegetables, green beans, strai | 53.0 | 56.4 | 3.4 | pass |
| usda-172283 | Babyfood, vegetables, mix vegetables jun | 55.0 | 65.8 | 10.8 | pass |
| usda-173515 | Babyfood, vegetables, mix vegetables str | 47.0 | 47.0 | 0.0 | pass |
| usda-172276 | Babyfood, vegetables, sweet potatoes str | 62.0 | 51.7 | 10.3 | pass |
| usda-172277 | Babyfood, vegetables, sweet potatoes, ju | 61.0 | 51.7 | 9.3 | pass |
| usda-172664 | Bagels, cinnamon-raisin | 43.0 | 32.9 | 10.1 | pass |
| usda-169212 | Bamboo shoots, canned, drained solids | 60.0 | 79.9 | 19.9 | FAIL |
| usda-168497 | Bamboo shoots, cooked, boiled, drained,  | 53.0 | 70.5 | 17.5 | FAIL |
| usda-169211 | Bamboo shoots, cooked, boiled, drained,  | 53.0 | 70.5 | 17.5 | FAIL |
| usda-173944 | Bananas, raw | 49.0 | 36.3 | 12.7 | pass |
| usda-170079 | Beans, mung, mature seeds, sprouted, can | 60.0 | 71.4 | 11.4 | pass |
| usda-169319 | Beans, pinto, mature seeds, sprouted, co | 94.0 | 96.9 | 2.9 | pass |
| usda-170087 | Beans, pinto, mature seeds, sprouted, co | 94.0 | 96.9 | 2.9 | pass |
| usda-169144 | Beans, snap, canned, all styles, seasone | 30.0 | 40.8 | 10.8 | pass |
| usda-168505 | Beans, snap, green, canned, no salt adde | 41.0 | 56.1 | 15.1 | FAIL |
| usda-168502 | Beans, snap, green, canned, no salt adde | 29.0 | 40.8 | 11.8 | pass |
| usda-169143 | Beans, snap, green, canned, regular pack | 38.0 | 56.1 | 18.1 | FAIL |
| usda-169142 | Beans, snap, green, canned, regular pack | 29.0 | 35.7 | 6.7 | pass |
| usda-169321 | Beans, snap, green, cooked, boiled, drai | 69.0 | 96.9 | 27.9 | FAIL |
| usda-169141 | Beans, snap, green, cooked, boiled, drai | 69.0 | 96.9 | 27.9 | FAIL |
| usda-169964 | Beans, snap, green, frozen, all styles,  | 66.0 | 102.0 | 36.0 | FAIL |
| usda-169962 | Beans, snap, green, frozen, all styles,  | 66.0 | 91.8 | 25.8 | FAIL |
| usda-169963 | Beans, snap, green, frozen, cooked, boil | 54.0 | 76.5 | 22.5 | FAIL |
| usda-169325 | Beans, snap, green, frozen, cooked, boil | 54.0 | 76.5 | 22.5 | FAIL |
| usda-169961 | Beans, snap, green, raw | 67.0 | 91.8 | 24.8 | FAIL |
| usda-169375 | Beans, snap, yellow, canned, no salt add | 42.0 | 61.2 | 19.2 | FAIL |
| usda-168504 | Beans, snap, yellow, canned, no salt add | 29.0 | 40.8 | 11.8 | pass |
| usda-169374 | Beans, snap, yellow, canned, regular pac | 42.0 | 61.2 | 19.2 | FAIL |
| usda-168503 | Beans, snap, yellow, canned, regular pac | 29.0 | 40.8 | 11.8 | pass |
| usda-169323 | Beans, snap, yellow, cooked, boiled, dra | 69.0 | 96.9 | 27.9 | FAIL |
| usda-169322 | Beans, snap, yellow, cooked, boiled, dra | 69.0 | 96.9 | 27.9 | FAIL |
| usda-169324 | Beans, snap, yellow, frozen, all styles, | 66.0 | 91.8 | 25.8 | FAIL |
| usda-169327 | Beans, snap, yellow, frozen, cooked, boi | 54.0 | 76.5 | 22.5 | FAIL |
| usda-169326 | Beans, snap, yellow, frozen, cooked, boi | 54.0 | 76.5 | 22.5 | FAIL |
| usda-169320 | Beans, snap, yellow, raw | 67.0 | 91.8 | 24.8 | FAIL |
| usda-170193 | Beef, variety meats and by-products, sue | 59.0 | 70.5 | 11.5 | pass |
| usda-169966 | Beets, canned, drained solids | 26.0 | 42.3 | 16.3 | FAIL |
| usda-168507 | Beets, canned, no salt added, solids and | 23.0 | 37.6 | 14.6 | pass |
| usda-169147 | Beets, canned, regular pack, solids and  | 23.0 | 32.9 | 9.9 | pass |
| usda-169146 | Beets, cooked, boiled, drained | 48.0 | 79.9 | 31.9 | FAIL |
| usda-168506 | Beets, cooked, boiled. drained, with sal | 48.0 | 79.9 | 31.9 | FAIL |
| usda-170479 | Beets, harvard, canned, solids and liqui | 24.0 | 37.6 | 13.6 | pass |
| usda-170480 | Beets, pickled, canned, solids and liqui | 23.0 | 37.6 | 14.6 | pass |
| usda-169145 | Beets, raw | 46.0 | 75.2 | 29.2 | FAIL |
| usda-174820 | Beverages, almond milk, chocolate, ready | 28.0 | 28.2 | 0.2 | pass |
| usda-174842 | Beverages, carbonated, club soda | 0.0 | 0.0 | 0.0 | pass |
| usda-173203 | Beverages, carbonated, grape soda | 0.0 | 0.0 | 0.0 | pass |
| usda-174854 | Beverages, carbonated, orange | 0.0 | 0.0 | 0.0 | pass |
| usda-173209 | Beverages, carbonated, pepper-type, cont | 0.0 | 0.0 | 0.0 | pass |
| usda-171869 | Beverages, carbonated, tonic water | 0.0 | 0.0 | 0.0 | pass |
| usda-171882 | Beverages, Clam and tomato juice, canned | 10.0 | 28.2 | 18.2 | FAIL |
| usda-171890 | Beverages, coffee, brewed, prepared with | 3.0 | 4.7 | 1.7 | pass |
| usda-171889 | Beverages, coffee, brewed, prepared with | 3.0 | 4.7 | 1.7 | pass |
| usda-175100 | Beverages, Orange drink, breakfast type, | 5.0 | 18.8 | 13.8 | pass |
| usda-174155 | Beverages, tea, black, brewed, prepared  | 0.0 | 0.0 | 0.0 | pass |
| usda-173227 | Beverages, tea, black, brewed, prepared  | 0.0 | 0.0 | 0.0 | pass |
| usda-174871 | Beverages, tea, black, brewed, prepared  | 0.0 | 0.0 | 0.0 | pass |
| usda-171918 | Beverages, tea, instant, lemon, with add | 1.0 | 28.2 | 27.2 | FAIL |
| usda-173233 | Beverages, water, bottled, PERRIER | 0.0 | 0.0 | 0.0 | pass |
| usda-173234 | Beverages, water, bottled, POLAND SPRING | 0.0 | 0.0 | 0.0 | pass |
| usda-173948 | Blueberries, canned, heavy syrup, solids | 23.0 | 32.9 | 9.9 | pass |
| usda-173951 | Blueberries, frozen, sweetened | 14.0 | 18.8 | 4.8 | pass |
| usda-173950 | Blueberries, frozen, unsweetened | 15.0 | 18.8 | 3.8 | pass |
| usda-171711 | Blueberries, raw | 26.0 | 32.9 | 6.9 | pass |
| usda-171714 | Breadfruit, raw | 26.0 | 57.2 | 31.2 | FAIL |
| usda-169974 | Burdock root, raw | 33.0 | 70.5 | 37.5 | FAIL |
| usda-173412 | Butter oil, anhydrous | 14.0 | 14.1 | 0.1 | pass |
| usda-173410 | Butter, salted | 41.0 | 42.3 | 1.3 | pass |
| usda-173411 | Butter, whipped, with salt | 41.0 | 23.5 | 17.5 | FAIL |
| usda-173430 | Butter, without salt | 41.0 | 42.3 | 1.3 | pass |
| usda-168517 | Cabbage, chinese (pak-choi), cooked, boi | 46.0 | 75.2 | 29.2 | FAIL |
| usda-170391 | Cabbage, chinese (pak-choi), cooked, boi | 46.0 | 75.2 | 29.2 | FAIL |
| usda-170390 | Cabbage, chinese (pak-choi), raw | 44.0 | 70.5 | 26.5 | FAIL |
| usda-169337 | Cabbage, chinese (pe-tsai), cooked, boil | 44.0 | 70.5 | 26.5 | FAIL |
| usda-169980 | Cabbage, chinese (pe-tsai), cooked, boil | 44.0 | 70.5 | 26.5 | FAIL |
| usda-169979 | Cabbage, chinese (pe-tsai), raw | 35.0 | 56.4 | 21.4 | FAIL |
| usda-169335 | Cabbage, common (danish, domestic, and p | 39.0 | 56.4 | 17.4 | FAIL |
| usda-169336 | Cabbage, common (danish, domestic, and p | 39.0 | 56.4 | 17.4 | FAIL |
| usda-168514 | Cabbage, common, cooked, boiled, drained | 32.0 | 61.1 | 29.1 | FAIL |
| usda-169976 | Cabbage, cooked, boiled, drained, withou | 32.0 | 61.1 | 29.1 | FAIL |
| usda-169975 | Cabbage, raw | 32.0 | 61.1 | 29.1 | FAIL |
| usda-168515 | Cabbage, red, cooked, boiled, drained, w | 38.0 | 70.5 | 32.5 | FAIL |
| usda-169978 | Cabbage, red, cooked, boiled, drained, w | 38.0 | 70.5 | 32.5 | FAIL |
| usda-169977 | Cabbage, red, raw | 36.0 | 65.8 | 29.8 | FAIL |
| usda-168516 | Cabbage, savoy, cooked, boiled, drained, | 58.0 | 84.6 | 26.6 | FAIL |
| usda-170389 | Cabbage, savoy, cooked, boiled, drained, | 58.0 | 84.6 | 26.6 | FAIL |
| usda-170388 | Cabbage, savoy, raw | 64.0 | 94.0 | 30.0 | FAIL |
| usda-172901 | CAMPBELL'S, Cream of Mushroom Soup, cond | 37.0 | 61.1 | 24.1 | FAIL |
| usda-167995 | Candies, marshmallows | 42.0 | 84.6 | 42.6 | FAIL |
| usda-167971 | Candies, TOOTSIE ROLL, chocolate-flavor  | 50.0 | 75.2 | 25.2 | FAIL |
| usda-171715 | Carambola, (starfruit), raw | 37.0 | 47.0 | 10.0 | pass |
| usda-173199 | Carbonated beverage, cream soda | 0.0 | 0.0 | 0.0 | pass |
| usda-168568 | Carrots, baby, raw | 26.0 | 28.8 | 2.8 | pass |
| usda-168518 | Carrots, canned, no salt added, drained  | 20.0 | 28.8 | 8.8 | pass |
| usda-169340 | Carrots, canned, no salt added, solids a | 39.0 | 28.8 | 10.2 | pass |
| usda-170396 | Carrots, canned, regular pack, drained s | 42.0 | 28.8 | 13.2 | pass |
| usda-170395 | Carrots, canned, regular pack, solids an | 18.0 | 28.8 | 10.8 | pass |
| usda-169339 | Carrots, cooked, boiled, drained, with s | 50.0 | 38.4 | 11.6 | pass |
| usda-170394 | Carrots, cooked, boiled, drained, withou | 50.0 | 38.4 | 11.6 | pass |
| usda-168519 | Carrots, frozen, cooked, boiled, drained | 38.0 | 28.8 | 9.2 | pass |
| usda-169984 | Carrots, frozen, cooked, boiled, drained | 38.0 | 28.8 | 9.2 | pass |
| usda-169983 | Carrots, frozen, unprepared | 34.0 | 38.4 | 4.4 | pass |
| usda-170393 | Carrots, raw | 61.0 | 43.2 | 17.8 | FAIL |
| usda-169985 | Cassava, raw | 26.0 | 64.4 | 38.4 | FAIL |
| usda-168556 | Catsup | 21.0 | 47.0 | 26.0 | FAIL |
| usda-169381 | Catsup, low sodium | 21.0 | 47.0 | 26.0 | FAIL |
| usda-168520 | Cauliflower, cooked, boiled, drained, wi | 66.0 | 86.4 | 20.4 | FAIL |
| usda-170397 | Cauliflower, cooked, boiled, drained, wi | 66.0 | 86.4 | 20.4 | FAIL |
| usda-168521 | Cauliflower, frozen, cooked, boiled, dra | 58.0 | 76.8 | 18.8 | FAIL |
| usda-170399 | Cauliflower, frozen, cooked, boiled, dra | 58.0 | 76.8 | 18.8 | FAIL |
| usda-170398 | Cauliflower, frozen, unprepared | 72.0 | 96.0 | 24.0 | FAIL |
| usda-169986 | Cauliflower, raw | 65.0 | 91.2 | 26.2 | FAIL |
| usda-169342 | Celery, cooked, boiled, drained, with sa | 24.0 | 38.4 | 14.4 | pass |
| usda-169989 | Celery, cooked, boiled, drained, without | 24.0 | 38.4 | 14.4 | pass |
| usda-169988 | Celery, raw | 20.0 | 33.6 | 13.6 | pass |
| usda-169990 | Celtuce, raw | 36.0 | 42.3 | 6.3 | pass |
| usda-171671 | Cereals, corn grits, white, regular and  | 90.0 | 88.4 | 1.6 | pass |
| usda-171655 | Cereals, corn grits, white, regular and  | 90.0 | 88.4 | 1.6 | pass |
| usda-171672 | Cereals, corn grits, yellow, regular and | 70.0 | 62.4 | 7.6 | pass |
| usda-171673 | Cereals, corn grits, yellow, regular, qu | 70.0 | 62.4 | 7.6 | pass |
| usda-173914 | Cereals, CREAM OF RICE, cooked with wate | 37.0 | 46.8 | 9.8 | pass |
| usda-173012 | Cereals, CREAM OF WHEAT, 1 minute cook t | 182.0 | 104.0 | 78.0 | FAIL |
| usda-173011 | Cereals, CREAM OF WHEAT, 1 minute cook t | 88.0 | 88.4 | 0.4 | pass |
| usda-173009 | Cereals, CREAM OF WHEAT, 2 1/2 minute co | 94.0 | 98.8 | 4.8 | pass |
| usda-173008 | Cereals, CREAM OF WHEAT, 2 1/2 minute co | 72.0 | 72.8 | 0.8 | pass |
| usda-173902 | Cereals, CREAM OF WHEAT, instant, prepar | 99.0 | 93.6 | 5.4 | pass |
| usda-173915 | Cereals, CREAM OF WHEAT, regular (10 min | 79.0 | 78.0 | 1.0 | pass |
| usda-171657 | Cereals, CREAM OF WHEAT, regular (10 min | 78.0 | 72.8 | 5.2 | pass |
| usda-171659 | Cereals, farina, enriched, assorted bran | 107.0 | 93.6 | 13.4 | pass |
| usda-173917 | Cereals, farina, enriched, cooked with w | 106.0 | 93.6 | 12.4 | pass |
| usda-173897 | Cereals, QUAKER, corn grits, instant, pl | 87.0 | 83.2 | 3.8 | pass |
| usda-169343 | Chard, swiss, cooked, boiled, drained, w | 114.0 | 89.3 | 24.7 | FAIL |
| usda-170401 | Chard, swiss, cooked, boiled, drained, w | 114.0 | 89.3 | 24.7 | FAIL |
| usda-169991 | Chard, swiss, raw | 110.0 | 84.6 | 25.4 | FAIL |
| usda-169344 | Chayote, fruit, cooked, boiled, drained, | 36.0 | 28.2 | 7.8 | pass |
| usda-170403 | Chayote, fruit, cooked, boiled, drained, | 36.0 | 28.2 | 7.8 | pass |
| usda-170402 | Chayote, fruit, raw | 47.0 | 37.6 | 9.4 | pass |
| usda-173953 | Cherimoya, raw | 42.0 | 75.2 | 33.2 | FAIL |
| usda-171719 | Cherries, sweet, raw | 24.0 | 51.7 | 27.7 | FAIL |
| usda-169992 | Chicory greens, raw | 41.0 | 79.9 | 38.9 | FAIL |
| usda-170404 | Chicory, witloof, raw | 22.0 | 42.3 | 20.3 | FAIL |
| usda-169363 | Corn, sweet, white, canned, cream style, | 81.0 | 88.4 | 7.4 | pass |
| usda-169362 | Corn, sweet, white, canned, cream style, | 81.0 | 88.4 | 7.4 | pass |
| usda-169360 | Corn, sweet, white, canned, whole kernel | 90.0 | 104.0 | 14.0 | pass |
| usda-168541 | Corn, sweet, white, canned, whole kernel | 90.0 | 104.0 | 14.0 | pass |
| usda-170409 | Corn, sweet, yellow, canned, brine pack, | 90.0 | 104.0 | 14.0 | pass |
| usda-169346 | Corn, sweet, yellow, canned, cream style | 81.0 | 88.4 | 7.4 | pass |
| usda-169215 | Corn, sweet, yellow, canned, cream style | 81.0 | 88.4 | 7.4 | pass |
| usda-169345 | Corn, sweet, yellow, canned, no salt add | 74.0 | 104.0 | 30.0 | FAIL |
| usda-169219 | Cornsalad, raw | 91.0 | 104.0 | 13.0 | pass |
| usda-169698 | Cornstarch | 13.0 | 14.1 | 1.1 | pass |
| usda-171721 | Crabapples, raw | 11.0 | 18.8 | 7.8 | pass |
| usda-169843 | CRACKER BARREL, coleslaw | 30.0 | 46.8 | 16.8 | FAIL |
| usda-171722 | Cranberries, raw | 36.0 | 23.5 | 12.5 | pass |
| usda-171904 | Cranberry juice cocktail, bottled, low c | 0.0 | 0.0 | 0.0 | pass |
| usda-173453 | Cream substitute, flavored, liquid | 33.0 | 33.6 | 0.6 | pass |
| usda-172214 | Cream substitute, flavored, powdered | 33.0 | 33.6 | 0.6 | pass |
| usda-171261 | Cream substitute, liquid, with hydrogena | 55.0 | 48.0 | 7.0 | pass |
| usda-171262 | Cream substitute, liquid, with lauric ac | 54.0 | 48.0 | 6.0 | pass |
| usda-169225 | Cucumber, peeled, raw | 31.0 | 28.8 | 2.2 | pass |
| usda-168409 | Cucumber, with peel, raw | 19.0 | 33.6 | 14.6 | pass |
| usda-168191 | Dates, medjool | 48.0 | 84.6 | 36.6 | FAIL |
| usda-169023 | DENNY'S, coleslaw | 30.0 | 47.0 | 17.0 | FAIL |
| usda-170867 | Dessert topping, pressurized | 53.0 | 47.0 | 6.0 | pass |
| usda-170868 | Dessert topping, semi solid, frozen | 67.0 | 61.1 | 5.9 | pass |
| usda-169371 | Dock, cooked, boiled, drained, with salt | 104.0 | 84.6 | 19.4 | FAIL |
| usda-170077 | Dock, cooked, boiled, drained, without s | 104.0 | 84.6 | 19.4 | FAIL |
| usda-170076 | Dock, raw | 114.0 | 94.0 | 20.0 | FAIL |
| usda-169352 | Eggplant, cooked, boiled, drained, with  | 35.0 | 44.0 | 9.0 | pass |
| usda-169229 | Eggplant, cooked, boiled, drained, witho | 35.0 | 44.0 | 9.0 | pass |
| usda-169228 | Eggplant, raw | 43.0 | 55.0 | 12.0 | pass |
| usda-171727 | Elderberries, raw | 40.0 | 32.9 | 7.1 | pass |
| usda-168412 | Endive, raw | 53.0 | 61.1 | 8.1 | pass |
| usda-168413 | Escarole, cooked, boiled, drained, no sa | 49.0 | 56.4 | 7.4 | pass |
| usda-171400 | Fat, beef tallow | 0.0 | 0.0 | 0.0 | pass |
| usda-173564 | Fat, chicken | 0.0 | 0.0 | 0.0 | pass |
| usda-173572 | Fat, goose | 0.0 | 0.0 | 0.0 | pass |
| usda-173571 | Fat, turkey | 0.0 | 0.0 | 0.0 | pass |
| usda-168176 | Feijoa, raw | 19.0 | 32.9 | 13.9 | pass |
| usda-173025 | Figs, canned, extra heavy syrup pack, so | 9.0 | 18.8 | 9.8 | pass |
| usda-173024 | Figs, canned, heavy syrup pack, solids a | 9.0 | 18.8 | 9.8 | pass |
| usda-173023 | Figs, canned, light syrup pack, solids a | 10.0 | 18.8 | 8.8 | pass |
| usda-173022 | Figs, canned, water pack, solids and liq | 10.0 | 18.8 | 8.8 | pass |
| usda-174666 | Figs, dried, stewed | 33.0 | 65.8 | 32.8 | FAIL |
| usda-173021 | Figs, raw | 18.0 | 37.6 | 19.6 | FAIL |
| usda-169625 | Frostings, chocolate, creamy, dry mix | 64.0 | 61.1 | 2.9 | pass |
| usda-168800 | Frostings, chocolate, creamy, dry mix, p | 54.0 | 51.7 | 2.3 | pass |
| usda-168845 | Frostings, chocolate, creamy, dry mix, p | 54.0 | 51.7 | 2.3 | pass |
| usda-168795 | Frostings, chocolate, creamy, ready-to-e | 52.0 | 51.7 | 0.3 | pass |
| usda-169619 | Frostings, cream cheese-flavor, ready-to | 0.0 | 4.7 | 4.7 | pass |
| usda-168802 | Frostings, vanilla, creamy, dry mix | 13.0 | 14.1 | 1.1 | pass |
| usda-168844 | Frostings, vanilla, creamy, dry mix, pre | 15.0 | 14.1 | 0.9 | pass |
| usda-169626 | Frostings, white, fluffy, dry mix, prepa | 83.0 | 70.5 | 12.5 | pass |
| usda-167953 | Fruit syrup | 0.0 | 0.0 | 0.0 | pass |
| usda-169596 | Gelatin desserts, dry mix, prepared with | 28.0 | 28.8 | 0.8 | pass |
| usda-169231 | Ginger root, raw | 45.0 | 84.6 | 39.6 | FAIL |
| usda-169353 | Gourd, white-flowered (calabash), cooked | 14.0 | 28.2 | 14.2 | pass |
| usda-169233 | Gourd, white-flowered (calabash), cooked | 14.0 | 28.2 | 14.2 | pass |
| usda-169232 | Gourd, white-flowered (calabash), raw | 15.0 | 28.2 | 13.2 | pass |
| usda-168207 | Grape juice, canned or bottled, unsweete | 12.0 | 13.2 | 1.2 | pass |
| usda-173042 | Grape juice, canned or bottled, unsweete | 12.0 | 13.2 | 1.2 | pass |
| usda-173033 | Grapefruit, raw, pink and red and white, | 38.0 | 19.8 | 18.2 | FAIL |
| usda-174673 | Grapefruit, raw, pink and red, all areas | 13.0 | 26.4 | 13.4 | pass |
| usda-174674 | Grapefruit, raw, pink and red, Californi | 30.0 | 16.5 | 13.5 | pass |
| usda-174675 | Grapefruit, raw, pink and red, Florida | 33.0 | 19.8 | 13.2 | pass |
| usda-174676 | Grapefruit, raw, white, all areas | 41.0 | 23.1 | 17.9 | FAIL |
| usda-174677 | Grapefruit, raw, white, California | 53.0 | 29.7 | 23.3 | FAIL |
| usda-173034 | Grapefruit, raw, white, Florida | 38.0 | 19.8 | 18.2 | FAIL |
| usda-173036 | Grapefruit, sections, canned, juice pack | 42.0 | 23.1 | 18.9 | FAIL |
| usda-173037 | Grapefruit, sections, canned, light syru | 34.0 | 19.8 | 14.2 | pass |
| usda-173035 | Grapefruit, sections, canned, water pack | 35.0 | 19.8 | 15.2 | FAIL |
| usda-174682 | Grapes, american type (slip skin), raw | 13.0 | 19.8 | 6.8 | pass |
| usda-174685 | Grapes, canned, thompson seedless, heavy | 10.0 | 16.5 | 6.5 | pass |
| usda-174684 | Grapes, canned, thompson seedless, water | 10.0 | 16.5 | 6.5 | pass |
| usda-174683 | Grapes, red or green (European type, suc | 19.0 | 23.1 | 4.1 | pass |
| usda-171599 | Gravy, HEINZ Home Style, savory beef | 34.0 | 51.7 | 17.7 | FAIL |
| usda-174686 | Guava sauce, cooked | 1.0 | 14.1 | 13.1 | pass |
| usda-173045 | Guavas, strawberry, raw | 1.0 | 28.2 | 27.2 | FAIL |
| usda-169701 | Hominy, canned, white | 76.0 | 70.5 | 5.5 | pass |
| usda-169752 | Hominy, canned, yellow | 76.0 | 70.5 | 5.5 | pass |
| usda-169640 | Honey | 11.0 | 14.1 | 3.1 | pass |
| usda-174687 | Jackfruit, raw | 52.0 | 79.9 | 27.9 | FAIL |
| usda-169641 | Jams and preserves | 21.0 | 18.8 | 2.2 | pass |
| usda-170340 | KFC, Coleslaw | 25.0 | 42.3 | 17.3 | FAIL |
| usda-168153 | Kiwifruit, green, raw | 44.0 | 51.7 | 7.7 | pass |
| usda-169357 | Kohlrabi, cooked, boiled, drained, with  | 41.0 | 84.6 | 43.6 | FAIL |
| usda-168425 | Kohlrabi, cooked, boiled, drained, witho | 41.0 | 84.6 | 43.6 | FAIL |
| usda-168424 | Kohlrabi, raw | 39.0 | 79.9 | 40.9 | FAIL |
| usda-171401 | Lard | 0.0 | 0.0 | 0.0 | pass |
| usda-168535 | Leeks, (bulb and lower leaf-portion), co | 30.0 | 37.6 | 7.6 | pass |
| usda-168426 | Leeks, (bulb and lower leaf-portion), co | 30.0 | 37.6 | 7.6 | pass |
| usda-169246 | Leeks, (bulb and lower leaf-portion), ra | 55.0 | 70.5 | 15.5 | FAIL |
| usda-168429 | Lettuce, butterhead (includes boston and | 53.0 | 67.2 | 14.2 | pass |
| usda-169247 | Lettuce, cos or romaine, raw | 65.0 | 57.6 | 7.4 | pass |
| usda-169249 | Lettuce, green leaf, raw | 55.0 | 67.2 | 12.2 | pass |
| usda-169248 | Lettuce, iceberg (includes crisphead typ | 23.0 | 43.2 | 20.2 | FAIL |
| usda-168431 | Lettuce, red leaf, raw | 67.0 | 62.4 | 4.6 | pass |
| usda-168156 | Lime juice, raw | 11.0 | 18.8 | 7.8 | pass |
| usda-169089 | Longans, raw | 30.0 | 61.1 | 31.1 | FAIL |
| usda-169908 | Loquats, raw | 14.0 | 18.8 | 4.8 | pass |
| usda-168536 | Lotus root, cooked, boiled, drained, wit | 28.0 | 75.2 | 47.2 | FAIL |
| usda-168430 | Lotus root, cooked, boiled, drained, wit | 28.0 | 75.2 | 47.2 | FAIL |
| usda-169910 | Mangos, raw | 27.0 | 26.4 | 0.6 | pass |
| usda-171018 | Margarine, regular, hard, soybean | 41.0 | 42.3 | 1.3 | pass |
| usda-168819 | Marmalade, orange | 10.0 | 14.1 | 4.1 | pass |
| usda-169092 | Melons, cantaloupe, raw | 23.0 | 37.6 | 14.6 | pass |
| usda-169911 | Melons, honeydew, raw | 15.0 | 23.5 | 8.5 | pass |
| usda-171264 | Milk substitutes, fluid, with lauric aci | 94.0 | 86.4 | 7.6 | pass |
| usda-171279 | Milk, human, mature, fluid | 46.0 | 48.0 | 2.0 | pass |
| usda-171977 | Mollusks, clam, mixed species, canned, l | 0.0 | 18.8 | 18.8 | FAIL |
| usda-168552 | Mountain yam, hawaii, cooked, steamed, w | 80.0 | 79.9 | 0.1 | pass |
| usda-168433 | Mountain yam, hawaii, cooked, steamed, w | 80.0 | 79.9 | 0.1 | pass |
| usda-168432 | Mountain yam, hawaii, raw | 62.0 | 61.1 | 0.9 | pass |
| usda-168499 | Mung beans, mature seeds, sprouted, cook | 86.0 | 102.0 | 16.0 | FAIL |
| usda-169137 | Mung beans, mature seeds, sprouted, cook | 86.0 | 102.0 | 16.0 | FAIL |
| usda-169254 | Mushrooms, canned, drained solids | 52.0 | 91.2 | 39.2 | FAIL |
| usda-169403 | Mushrooms, maitake, raw | 60.0 | 91.2 | 31.2 | FAIL |
| usda-170097 | Mushrooms, shiitake, cooked, with salt | 67.0 | 76.8 | 9.8 | pass |
| usda-168437 | Mushrooms, shiitake, cooked, without sal | 67.0 | 76.8 | 9.8 | pass |
| usda-169914 | Nectarines, raw | 21.0 | 51.7 | 30.7 | FAIL |
| usda-174258 | Noodles, chinese, cellophane or long ric | 10.0 | 10.4 | 0.4 | pass |
| usda-169388 | Nopales, cooked, without salt | 52.0 | 65.8 | 13.8 | pass |
| usda-168571 | Nopales, raw | 49.0 | 61.1 | 12.1 | pass |
| usda-170168 | Nuts, chestnuts, european, boiled and st | 84.0 | 94.0 | 10.0 | pass |
| usda-170575 | Nuts, chestnuts, european, raw, peeled | 69.0 | 75.2 | 6.2 | pass |
| usda-168589 | Nuts, chestnuts, japanese, boiled and st | 32.0 | 37.6 | 5.6 | pass |
| usda-170171 | Nuts, coconut cream, canned, sweetened | 60.0 | 56.4 | 3.6 | pass |
| usda-170173 | Nuts, coconut milk, canned | 102.0 | 94.0 | 8.0 | pass |
| usda-169409 | Nuts, coconut milk, frozen | 82.0 | 75.2 | 6.8 | pass |
| usda-170174 | Nuts, coconut water | 37.0 | 32.9 | 4.1 | pass |
| usda-171031 | Oil, almond | 0.0 | 0.0 | 0.0 | pass |
| usda-171032 | Oil, apricot kernel | 0.0 | 0.0 | 0.0 | pass |
| usda-171428 | Oil, babassu | 0.0 | 0.0 | 0.0 | pass |
| usda-171421 | Oil, cocoa butter | 0.0 | 0.0 | 0.0 | pass |
| usda-171412 | Oil, coconut | 0.0 | 0.0 | 0.0 | pass |
| usda-171029 | Oil, corn, industrial and retail, all pu | 0.0 | 0.0 | 0.0 | pass |
| usda-171024 | Oil, cottonseed, salad or cooking | 0.0 | 0.0 | 0.0 | pass |
| usda-173563 | Oil, cupu assu | 0.0 | 0.0 | 0.0 | pass |
| usda-171028 | Oil, grapeseed | 0.0 | 0.0 | 0.0 | pass |
| usda-171427 | Oil, hazelnut | 0.0 | 0.0 | 0.0 | pass |
| usda-172367 | Oil, industrial, coconut (hydrogenated), | 0.0 | 0.0 | 0.0 | pass |
| usda-172365 | Oil, industrial, coconut, confection fat | 0.0 | 0.0 | 0.0 | pass |
| usda-173595 | Oil, industrial, coconut, principal uses | 0.0 | 0.0 | 0.0 | pass |
| usda-172368 | Oil, industrial, palm and palm kernel, f | 0.0 | 0.0 | 0.0 | pass |
| usda-172366 | Oil, industrial, palm kernel (hydrogenat | 0.0 | 0.0 | 0.0 | pass |
| usda-173602 | Oil, industrial, palm kernel (hydrogenat | 0.0 | 0.0 | 0.0 | pass |
| usda-173601 | Oil, industrial, palm kernel (hydrogenat | 0.0 | 0.0 | 0.0 | pass |
| usda-173603 | Oil, industrial, palm kernel (hydrogenat | 0.0 | 0.0 | 0.0 | pass |
| usda-173600 | Oil, industrial, palm kernel, confection | 0.0 | 0.0 | 0.0 | pass |
| usda-172362 | Oil, industrial, soy ( partially hydroge | 0.0 | 0.0 | 0.0 | pass |
| usda-172363 | Oil, industrial, soy (partially hydrogen | 0.0 | 0.0 | 0.0 | pass |
| usda-173604 | Oil, industrial, soy (partially hydrogen | 0.0 | 0.0 | 0.0 | pass |
| usda-172364 | Oil, industrial, soy (partially hydrogen | 0.0 | 0.0 | 0.0 | pass |
| usda-172361 | Oil, industrial, soy (partially hydrogen | 0.0 | 0.0 | 0.0 | pass |
| usda-173596 | Oil, industrial, soy (partially hydrogen | 0.0 | 0.0 | 0.0 | pass |
| usda-173598 | Oil, industrial, soy, refined, for woks  | 0.0 | 0.0 | 0.0 | pass |
| usda-172335 | Oil, nutmeg butter | 0.0 | 0.0 | 0.0 | pass |
| usda-171413 | Oil, olive, salad or cooking | 0.0 | 0.0 | 0.0 | pass |
| usda-171015 | Oil, palm | 0.0 | 0.0 | 0.0 | pass |
| usda-171410 | Oil, peanut, salad or cooking | 0.0 | 0.0 | 0.0 | pass |
| usda-171423 | Oil, poppyseed | 0.0 | 0.0 | 0.0 | pass |
| usda-171013 | Oil, rice bran | 0.0 | 0.0 | 0.0 | pass |
| usda-171027 | Oil, safflower, salad or cooking, high o | 0.0 | 0.0 | 0.0 | pass |
| usda-171026 | Oil, safflower, salad or cooking, linole | 0.0 | 0.0 | 0.0 | pass |
| usda-171016 | Oil, sesame, salad or cooking | 0.0 | 0.0 | 0.0 | pass |
| usda-171429 | Oil, sheanut | 0.0 | 0.0 | 0.0 | pass |
| usda-171012 | Oil, soybean, salad or cooking | 0.0 | 0.0 | 0.0 | pass |
| usda-171411 | Oil, soybean, salad or cooking | 0.0 | 0.0 | 0.0 | pass |
| usda-173565 | Oil, soybean, salad or cooking, (partial | 0.0 | 0.0 | 0.0 | pass |
| usda-171017 | Oil, sunflower, linoleic | 0.0 | 0.0 | 0.0 | pass |
| usda-171025 | Oil, sunflower, linoleic | 0.0 | 0.0 | 0.0 | pass |
| usda-172328 | Oil, sunflower, linoleic | 0.0 | 0.0 | 0.0 | pass |
| usda-171425 | Oil, teaseed | 0.0 | 0.0 | 0.0 | pass |
| usda-171424 | Oil, tomatoseed | 0.0 | 0.0 | 0.0 | pass |
| usda-173570 | Oil, ucuhuba butter | 0.0 | 0.0 | 0.0 | pass |
| usda-172370 | Oil, vegetable, soybean, refined | 0.0 | 0.0 | 0.0 | pass |
| usda-171030 | Oil, walnut | 0.0 | 0.0 | 0.0 | pass |
| usda-171014 | Oil, wheat germ | 0.0 | 0.0 | 0.0 | pass |
| usda-170098 | Okra, cooked, boiled, drained, with salt | 61.0 | 89.3 | 28.3 | FAIL |
| usda-169261 | Okra, cooked, boiled, drained, without s | 61.0 | 89.3 | 28.3 | FAIL |
| usda-170099 | Okra, frozen, cooked, boiled, drained, w | 55.0 | 75.2 | 20.2 | FAIL |
| usda-169263 | Okra, frozen, cooked, boiled, drained, w | 53.0 | 75.2 | 22.2 | FAIL |
| usda-169262 | Okra, frozen, unprepared | 55.0 | 79.9 | 24.9 | FAIL |
| usda-169260 | Okra, raw | 65.0 | 89.3 | 24.3 | FAIL |
| usda-169094 | Olives, ripe, canned | 29.0 | 37.6 | 8.6 | pass |
| usda-169095 | Olives, ripe, canned | 34.0 | 47.0 | 13.0 | pass |
| usda-170003 | Onions, canned, solids and liquids | 21.0 | 43.2 | 22.2 | FAIL |
| usda-170100 | Onions, cooked, boiled, drained, with sa | 35.0 | 67.2 | 32.2 | FAIL |
| usda-170001 | Onions, cooked, boiled, drained, without | 35.0 | 67.2 | 32.2 | FAIL |
| usda-170101 | Onions, frozen, chopped, cooked, boiled, | 20.0 | 38.4 | 18.4 | FAIL |
| usda-170411 | Onions, frozen, chopped, cooked, boiled, | 20.0 | 38.4 | 18.4 | FAIL |
| usda-170410 | Onions, frozen, chopped, unprepared | 20.0 | 38.4 | 18.4 | FAIL |
| usda-170507 | Onions, frozen, whole, cooked, boiled, d | 18.0 | 33.6 | 15.6 | FAIL |
| usda-170413 | Onions, frozen, whole, cooked, boiled, d | 18.0 | 33.6 | 15.6 | FAIL |
| usda-170412 | Onions, frozen, whole, unprepared | 23.0 | 43.2 | 20.2 | FAIL |
| usda-170000 | Onions, raw | 25.0 | 52.8 | 27.8 | FAIL |
| usda-170005 | Onions, spring or scallions (includes to | 59.0 | 86.4 | 27.4 | FAIL |
| usda-170008 | Onions, sweet, raw | 24.0 | 38.4 | 14.4 | pass |
| usda-170007 | Onions, welsh, raw | 61.0 | 91.2 | 30.2 | FAIL |
| usda-170004 | Onions, yellow, sauteed | 24.0 | 48.0 | 24.0 | FAIL |
| usda-169099 | Orange juice, canned, unsweetened | 8.0 | 23.1 | 15.1 | FAIL |
| usda-169100 | Orange juice, chilled, includes from con | 11.0 | 23.1 | 12.1 | pass |
| usda-169920 | Orange juice, chilled, includes from con | 11.0 | 23.1 | 12.1 | pass |
| usda-169101 | Orange juice, chilled, includes from con | 11.0 | 23.1 | 12.1 | pass |
| usda-167794 | Orange juice, chilled, includes from con | 11.0 | 23.1 | 12.1 | pass |
| usda-169098 | Orange juice, raw | 9.0 | 23.1 | 14.1 | pass |
| usda-169097 | Oranges, raw, all commercial varieties | 31.0 | 29.7 | 1.3 | pass |
| usda-169916 | Oranges, raw, California, valencias | 34.0 | 33.0 | 1.0 | pass |
| usda-169918 | Oranges, raw, Florida | 23.0 | 23.1 | 0.1 | pass |
| usda-169917 | Oranges, raw, navels | 21.0 | 29.7 | 8.7 | pass |
| usda-169919 | Oranges, raw, with peel | 43.0 | 42.9 | 0.1 | pass |
| usda-169926 | Papayas, raw | 9.0 | 23.5 | 14.5 | pass |
| usda-169113 | Peaches, canned, extra heavy syrup pack, | 15.0 | 25.5 | 10.5 | pass |
| usda-169931 | Peaches, canned, extra light syrup, soli | 13.0 | 20.4 | 7.4 | pass |
| usda-169112 | Peaches, canned, heavy syrup pack, solid | 14.0 | 25.5 | 11.5 | pass |
| usda-168181 | Peaches, canned, heavy syrup, drained | 11.0 | 25.5 | 14.5 | pass |
| usda-169930 | Peaches, canned, juice pack, solids and  | 20.0 | 30.6 | 10.6 | pass |
| usda-169111 | Peaches, canned, light syrup pack, solid | 14.0 | 25.5 | 11.5 | pass |
| usda-169929 | Peaches, canned, water pack, solids and  | 14.0 | 20.4 | 6.4 | pass |
| usda-169933 | Peaches, dehydrated (low-moisture), sulf | 63.0 | 102.0 | 39.0 | FAIL |
| usda-169115 | Peaches, dried, sulfured, stewed, with a | 33.0 | 56.1 | 23.1 | FAIL |
| usda-169935 | Peaches, dried, sulfured, stewed, withou | 36.0 | 61.2 | 25.2 | FAIL |
| usda-169116 | Peaches, frozen, sliced, sweetened | 20.0 | 30.6 | 10.6 | pass |
| usda-169114 | Peaches, spiced, canned, heavy syrup pac | 13.0 | 20.4 | 7.4 | pass |
| usda-169928 | Peaches, yellow, raw | 19.0 | 45.9 | 26.9 | FAIL |
| usda-168177 | Pears, asian, raw | 13.0 | 25.5 | 12.5 | pass |
| usda-169120 | Pears, canned, extra heavy syrup pack, s | 5.0 | 10.2 | 5.2 | pass |
| usda-169937 | Pears, canned, extra light syrup pack, s | 8.0 | 15.3 | 7.3 | pass |
| usda-169939 | Pears, canned, heavy syrup pack, solids  | 5.0 | 10.2 | 5.2 | pass |
| usda-169936 | Pears, canned, juice pack, solids and li | 9.0 | 15.3 | 6.3 | pass |
| usda-169938 | Pears, canned, light syrup pack, solids  | 5.0 | 10.2 | 5.2 | pass |
| usda-169119 | Pears, canned, water pack, solids and li | 5.0 | 10.2 | 5.2 | pass |
| usda-169123 | Pears, dried, sulfured, stewed, with add | 23.0 | 45.9 | 22.9 | FAIL |
| usda-169122 | Pears, dried, sulfured, stewed, without  | 24.0 | 45.9 | 21.9 | FAIL |
| usda-169121 | Pears, dried, sulfured, uncooked | 49.0 | 96.9 | 47.9 | FAIL |
| usda-169118 | Pears, raw | 11.0 | 20.4 | 9.4 | pass |
| usda-167776 | Pears, raw, bartlett | 11.0 | 20.4 | 9.4 | pass |
| usda-167778 | Pears, raw, bosc | 10.0 | 20.4 | 10.4 | pass |
| usda-167779 | Pears, raw, green anjou | 13.0 | 20.4 | 7.4 | pass |
| usda-167777 | Pears, raw, red anjou | 10.0 | 15.3 | 5.3 | pass |
| usda-168577 | Peppers, chili, green, canned | 22.0 | 33.6 | 11.6 | pass |
| usda-170426 | Peppers, hot chili, green, canned, pods, | 28.0 | 43.2 | 15.2 | FAIL |
| usda-170497 | Peppers, hot chili, green, raw | 62.0 | 96.0 | 34.0 | FAIL |
| usda-170107 | Peppers, hot chili, red, canned, excludi | 28.0 | 43.2 | 15.2 | FAIL |
| usda-170106 | Peppers, hot chili, red, raw | 62.0 | 91.2 | 29.2 | FAIL |
| usda-168578 | Peppers, hungarian, raw | 25.0 | 38.4 | 13.4 | pass |
| usda-170080 | Peppers, jalapeno, canned, solids and li | 29.0 | 43.2 | 14.2 | pass |
| usda-170429 | Peppers, sweet, green, canned, solids an | 25.0 | 38.4 | 13.4 | pass |
| usda-170109 | Peppers, sweet, green, cooked, boiled, d | 29.0 | 43.2 | 14.2 | pass |
| usda-170428 | Peppers, sweet, green, cooked, boiled, d | 29.0 | 43.2 | 14.2 | pass |
| usda-170023 | Peppers, sweet, green, frozen, chopped,  | 29.0 | 48.0 | 19.0 | FAIL |
| usda-170516 | Peppers, sweet, green, frozen, chopped,  | 29.0 | 48.0 | 19.0 | FAIL |
| usda-170022 | Peppers, sweet, green, frozen, chopped,  | 33.0 | 52.8 | 19.8 | FAIL |
| usda-170427 | Peppers, sweet, green, raw | 92.0 | 43.2 | 48.8 | FAIL |
| usda-170024 | Peppers, sweet, green, sauteed | 84.0 | 38.4 | 45.6 | FAIL |
| usda-168546 | Peppers, sweet, red, canned, solids and  | 25.0 | 38.4 | 13.4 | pass |
| usda-170515 | Peppers, sweet, red, cooked, boiled, dra | 29.0 | 43.2 | 14.2 | pass |
| usda-170110 | Peppers, sweet, red, cooked, boiled, dra | 29.0 | 43.2 | 14.2 | pass |
| usda-168549 | Peppers, sweet, red, frozen, chopped, bo | 48.0 | 48.0 | 0.0 | pass |
| usda-168548 | Peppers, sweet, red, frozen, chopped, bo | 48.0 | 48.0 | 0.0 | pass |
| usda-168547 | Peppers, sweet, red, frozen, chopped, un | 33.0 | 52.8 | 19.8 | FAIL |
| usda-170108 | Peppers, sweet, red, raw | 50.0 | 48.0 | 2.0 | pass |
| usda-168550 | Peppers, sweet, red, sauteed | 53.0 | 48.0 | 5.0 | pass |
| usda-169383 | Peppers, sweet, yellow, raw | 31.0 | 48.0 | 17.0 | FAIL |
| usda-169942 | Persimmons, japanese, dried | 63.0 | 65.8 | 2.8 | pass |
| usda-169941 | Persimmons, japanese, raw | 26.0 | 28.2 | 2.2 | pass |
| usda-169943 | Persimmons, native, raw | 36.0 | 37.6 | 1.6 | pass |
| usda-169386 | Pickle relish, hamburger | 19.0 | 28.2 | 9.2 | pass |
| usda-168560 | Pickle relish, hot dog | 46.0 | 70.5 | 24.5 | FAIL |
| usda-168561 | Pickle relish, sweet | 11.0 | 18.8 | 7.8 | pass |
| usda-168558 | Pickles, cucumber, dill or kosher dill | 17.0 | 23.5 | 6.5 | pass |
| usda-168563 | Pickles, cucumber, dill, reduced sodium | 17.0 | 23.5 | 6.5 | pass |
| usda-169379 | Pickles, cucumber, sour | 9.0 | 14.1 | 5.1 | pass |
| usda-168562 | Pickles, cucumber, sour, low sodium | 9.0 | 14.1 | 5.1 | pass |
| usda-169378 | Pickles, cucumber, sweet | 21.0 | 28.2 | 7.2 | pass |
| usda-169380 | Pickles, cucumber, sweet, low sodium | 10.0 | 18.8 | 8.8 | pass |
| usda-168824 | Pie fillings, canned, cherry | 8.0 | 18.8 | 10.8 | pass |
| usda-175011 | Pie, apple, commercially prepared, enric | 88.0 | 89.3 | 1.3 | pass |
| usda-173239 | Pie, apple, commercially prepared, unenr | 88.0 | 89.3 | 1.3 | pass |
| usda-172778 | Pie, blueberry, commercially prepared | 86.0 | 84.6 | 1.4 | pass |
| usda-172780 | Pie, cherry, commercially prepared | 99.0 | 94.0 | 5.0 | pass |
| usda-172785 | Pie, lemon meringue, commercially prepar | 66.0 | 70.5 | 4.5 | pass |
| usda-175020 | Pie, peach | 81.0 | 89.3 | 8.3 | pass |
| usda-168559 | Pimento, canned | 34.0 | 51.7 | 17.7 | FAIL |
| usda-169945 | Pineapple, canned, extra heavy syrup pac | 9.0 | 9.9 | 0.9 | pass |
| usda-169944 | Pineapple, canned, heavy syrup pack, sol | 9.0 | 13.2 | 4.2 | pass |
| usda-169126 | Pineapple, canned, juice pack, solids an | 10.0 | 13.2 | 3.2 | pass |
| usda-169127 | Pineapple, canned, light syrup pack, sol | 9.0 | 13.2 | 4.2 | pass |
| usda-169125 | Pineapple, canned, water pack, solids an | 11.0 | 13.2 | 2.2 | pass |
| usda-169946 | Pineapple, frozen, chunks, sweetened | 12.0 | 13.2 | 1.2 | pass |
| usda-169124 | Pineapple, raw, all varieties | 21.0 | 16.5 | 4.5 | pass |
| usda-168216 | Plantains, green, boiled | 30.0 | 51.7 | 21.7 | FAIL |
| usda-169131 | Plantains, yellow, baked | 53.0 | 70.5 | 17.5 | FAIL |
| usda-169133 | Plums, canned, purple, extra heavy syrup | 8.0 | 18.8 | 10.8 | pass |
| usda-169132 | Plums, canned, purple, heavy syrup pack, | 8.0 | 18.8 | 10.8 | pass |
| usda-169951 | Plums, canned, purple, juice pack, solid | 11.0 | 23.5 | 12.5 | pass |
| usda-169952 | Plums, canned, purple, light syrup pack, | 8.0 | 18.8 | 10.8 | pass |
| usda-169950 | Plums, canned, purple, water pack, solid | 8.0 | 18.8 | 10.8 | pass |
| usda-169949 | Plums, raw | 14.0 | 32.9 | 18.9 | FAIL |
| usda-172087 | POPEYES, Coleslaw | 20.0 | 47.0 | 27.0 | FAIL |
| usda-167861 | Pork, fresh, variety meats and by-produc | 66.0 | 84.6 | 18.6 | FAIL |
| usda-170047 | Potato puffs, frozen, unprepared | 93.0 | 87.4 | 5.6 | pass |
| usda-170112 | Potatoes, baked, flesh, with salt | 87.0 | 92.0 | 5.0 | pass |
| usda-170033 | Potatoes, baked, flesh, without salt | 87.0 | 92.0 | 5.0 | pass |
| usda-170114 | Potatoes, boiled, cooked in skin, flesh, | 83.0 | 87.4 | 4.4 | pass |
| usda-170438 | Potatoes, boiled, cooked in skin, flesh, | 83.0 | 87.4 | 4.4 | pass |
| usda-170520 | Potatoes, boiled, cooked without skin, f | 76.0 | 78.2 | 2.2 | pass |
| usda-170440 | Potatoes, boiled, cooked without skin, f | 76.0 | 78.2 | 2.2 | pass |
| usda-170444 | Potatoes, canned, drained solids | 63.0 | 64.4 | 1.4 | pass |
| usda-170443 | Potatoes, canned, solids and liquids | 54.0 | 55.2 | 1.2 | pass |
| usda-170116 | Potatoes, frozen, whole, cooked, boiled, | 88.0 | 92.0 | 4.0 | pass |
| usda-170049 | Potatoes, frozen, whole, cooked, boiled, | 88.0 | 92.0 | 4.0 | pass |
| usda-170446 | Potatoes, mashed, dehydrated, prepared f | 95.0 | 82.8 | 12.2 | pass |
| usda-169372 | Potatoes, mashed, dehydrated, prepared f | 90.0 | 87.4 | 2.6 | pass |
| usda-170493 | Potatoes, mashed, home-prepared, whole m | 89.0 | 87.4 | 1.6 | pass |
| usda-168555 | Potatoes, mashed, home-prepared, whole m | 83.0 | 87.4 | 4.4 | pass |
| usda-170037 | Potatoes, mashed, home-prepared, whole m | 92.0 | 92.0 | 0.0 | pass |
| usda-169768 | Potatoes, mashed, ready-to-eat | 120.0 | 92.0 | 28.0 | FAIL |
| usda-170453 | Potatoes, o'brien, frozen, unprepared | 78.0 | 82.8 | 4.8 | pass |
| usda-170029 | Potatoes, red, flesh and skin, raw | 75.0 | 87.4 | 12.4 | pass |
| usda-170028 | Potatoes, white, flesh and skin, raw | 66.0 | 78.2 | 12.2 | pass |
| usda-169650 | Puddings, banana, dry mix, regular | 2.0 | 0.0 | 2.0 | pass |
| usda-170241 | Puddings, banana, dry mix, regular, with | 2.0 | 0.0 | 2.0 | pass |
| usda-169654 | Puddings, lemon, dry mix, instant | 0.0 | 0.0 | 0.0 | pass |
| usda-168831 | Puddings, lemon, dry mix, regular | 3.0 | 4.7 | 1.7 | pass |
| usda-170242 | Puddings, lemon, dry mix, regular, with  | 3.0 | 4.7 | 1.7 | pass |
| usda-169606 | Puddings, tapioca, dry mix | 4.0 | 4.7 | 0.7 | pass |
| usda-170243 | Puddings, tapioca, dry mix, with no adde | 4.0 | 4.7 | 0.7 | pass |
| usda-169609 | Puddings, vanilla, dry mix, regular | 13.0 | 14.1 | 1.1 | pass |
| usda-170644 | Puddings, vanilla, dry mix, regular, wit | 13.0 | 14.1 | 1.1 | pass |
| usda-169273 | Pumpkin pie mix, canned | 35.0 | 51.7 | 16.7 | FAIL |
| usda-170527 | Pumpkin, canned, with salt | 35.0 | 51.7 | 16.7 | FAIL |
| usda-168450 | Pumpkin, canned, without salt | 35.0 | 51.7 | 16.7 | FAIL |
| usda-170526 | Pumpkin, cooked, boiled, drained, with s | 23.0 | 32.9 | 9.9 | pass |
| usda-168449 | Pumpkin, cooked, boiled, drained, withou | 23.0 | 32.9 | 9.9 | pass |
| usda-168448 | Pumpkin, raw | 32.0 | 47.0 | 15.0 | pass |
| usda-170121 | Purslane, cooked, boiled, drained, with  | 58.0 | 70.5 | 12.5 | pass |
| usda-169275 | Purslane, cooked, boiled, drained, witho | 58.0 | 70.5 | 12.5 | pass |
| usda-168564 | Radicchio, raw | 34.0 | 65.8 | 31.8 | FAIL |
| usda-170122 | Radishes, oriental, cooked, boiled, drai | 22.0 | 32.9 | 10.9 | pass |
| usda-168452 | Radishes, oriental, cooked, boiled, drai | 22.0 | 32.9 | 10.9 | pass |
| usda-168451 | Radishes, oriental, raw | 20.0 | 28.2 | 8.2 | pass |
| usda-169276 | Radishes, raw | 36.0 | 32.9 | 3.1 | pass |
| usda-170081 | Radishes, white icicle, raw | 36.0 | 51.7 | 15.7 | FAIL |
| usda-168914 | Rice noodles, cooked | 95.0 | 93.6 | 1.4 | pass |
| usda-169711 | Rice, white, glutinous, unenriched, cook | 108.0 | 104.0 | 4.0 | pass |
| usda-171404 | Salad dressing, french dressing, reduced | 16.0 | 28.2 | 12.2 | pass |
| usda-171416 | Salad dressing, french, home recipe | 0.0 | 4.7 | 4.7 | pass |
| usda-171417 | Salad dressing, home recipe, vinegar and | 0.0 | 0.0 | 0.0 | pass |
| usda-171405 | Salad dressing, italian dressing, commer | 13.0 | 18.8 | 5.8 | pass |
| usda-171019 | Salad dressing, italian dressing, commer | 11.0 | 18.8 | 7.8 | pass |
| usda-171403 | Salad dressing, mayonnaise type, regular | 34.0 | 32.9 | 1.1 | pass |
| usda-171406 | Salad dressing, mayonnaise, imitation, s | 0.0 | 14.1 | 14.1 | pass |
| usda-171408 | Salad dressing, mayonnaise, imitation, s | 0.0 | 4.7 | 4.7 | pass |
| usda-173594 | Salad dressing, mayonnaise, light | 20.0 | 18.8 | 1.2 | pass |
| usda-171009 | Salad dressing, mayonnaise, regular | 57.0 | 47.0 | 10.0 | pass |
| usda-171010 | Salad dressing, mayonnaise, soybean and  | 57.0 | 51.7 | 5.3 | pass |
| usda-171007 | Salad dressing, russian dressing, low ca | 22.0 | 23.5 | 1.5 | pass |
| usda-171008 | Salad dressing, thousand island dressing | 0.0 | 37.6 | 37.6 | FAIL |
| usda-171402 | Salad dressing, thousand island, commerc | 0.0 | 51.7 | 51.7 | FAIL |
| usda-173468 | Salt, table | 0.0 | 0.0 | 0.0 | pass |
| usda-171409 | Sandwich spread, with chopped pickle, re | 39.0 | 42.3 | 3.3 | pass |
| usda-167759 | Sapodilla, raw | 13.0 | 18.8 | 5.8 | pass |
| usda-167760 | Sapote, mamey, raw | 61.0 | 70.5 | 9.5 | pass |
| usda-174527 | Sauce, ready-to-serve, pepper or hot | 16.0 | 23.5 | 7.5 | pass |
| usda-174528 | Sauce, ready-to-serve, pepper, TABASCO | 40.0 | 61.1 | 21.1 | FAIL |
| usda-169279 | Sauerkraut, canned, solids and liquids | 23.0 | 42.3 | 19.3 | FAIL |
| usda-167603 | Seaweed, Canadian Cultivated EMI-TSUNOMA | 98.0 | 89.3 | 8.7 | pass |
| usda-168457 | Seaweed, kelp, raw | 43.0 | 79.9 | 36.9 | FAIL |
| usda-169368 | Sesbania flower, cooked, steamed, with s | 62.0 | 51.7 | 10.3 | pass |
| usda-169281 | Sesbania flower, cooked, steamed, withou | 62.0 | 51.7 | 10.3 | pass |
| usda-168459 | Sesbania flower, raw | 70.0 | 61.1 | 8.9 | pass |
| usda-172329 | Shortening bread, soybean (hydrogenated) | 0.0 | 0.0 | 0.0 | pass |
| usda-172330 | Shortening cake mix, soybean (hydrogenat | 0.0 | 0.0 | 0.0 | pass |
| usda-173568 | Shortening confectionery, coconut (hydro | 0.0 | 0.0 | 0.0 | pass |
| usda-173567 | Shortening frying (heavy duty), beef tal | 0.0 | 0.0 | 0.0 | pass |
| usda-172331 | Shortening frying (heavy duty), palm | 0.0 | 0.0 | 0.0 | pass |
| usda-172333 | Shortening frying (heavy duty), soybean  | 0.0 | 0.0 | 0.0 | pass |
| usda-172332 | Shortening household soybean (hydrogenat | 0.0 | 0.0 | 0.0 | pass |
| usda-173566 | Shortening industrial, lard and vegetabl | 0.0 | 0.0 | 0.0 | pass |
| usda-173569 | Shortening industrial, soybean (hydrogen | 0.0 | 0.0 | 0.0 | pass |
| usda-172334 | Shortening, confectionery, fractionated  | 0.0 | 0.0 | 0.0 | pass |
| usda-172327 | Shortening, household, lard and vegetabl | 0.0 | 0.0 | 0.0 | pass |
| usda-171011 | Shortening, household, soybean (partiall | 0.0 | 0.0 | 0.0 | pass |
| usda-173607 | Shortening, industrial, soy (partially h | 0.0 | 0.0 | 0.0 | pass |
| usda-173597 | Shortening, industrial, soy (partially h | 0.0 | 0.0 | 0.0 | pass |
| usda-171546 | Soup, chicken and vegetable, canned, rea | 60.0 | 94.0 | 34.0 | FAIL |
| usda-172908 | Soup, chicken gumbo, canned, prepared wi | 40.0 | 51.7 | 11.7 | pass |
| usda-171537 | Soup, cream of asparagus, canned, conden | 76.0 | 84.6 | 8.6 | pass |
| usda-174549 | Soup, cream of asparagus, canned, prepar | 39.0 | 42.3 | 3.3 | pass |
| usda-171540 | Soup, cream of celery, canned, condensed | 62.0 | 61.1 | 0.9 | pass |
| usda-172907 | Soup, cream of celery, canned, prepared  | 32.0 | 32.9 | 0.9 | pass |
| usda-174553 | Soup, cream of chicken, canned, prepared | 63.0 | 65.8 | 2.8 | pass |
| usda-171155 | Soup, cream of mushroom, canned, condens | 39.0 | 65.8 | 26.8 | FAIL |
| usda-171158 | Soup, cream of potato, canned, condensed | 66.0 | 70.5 | 4.5 | pass |
| usda-172917 | Soup, cream of potato, canned, prepared  | 34.0 | 32.9 | 1.1 | pass |
| usda-174807 | Soup, egg drop, Chinese restaurant | 28.0 | 56.4 | 28.4 | FAIL |
| usda-172913 | Soup, minestrone, canned, prepared with  | 64.0 | 84.6 | 20.6 | FAIL |
| usda-172881 | Soup, tomato bisque, canned, condensed | 60.0 | 84.6 | 24.6 | FAIL |
| usda-171574 | Soup, tomato bisque, canned, prepared wi | 31.0 | 42.3 | 11.3 | pass |
| usda-174562 | Soup, turkey noodle, canned, prepared wi | 64.0 | 75.2 | 11.2 | pass |
| usda-174563 | Soup, turkey vegetable, canned, prepared | 47.0 | 61.1 | 14.1 | pass |
| usda-171161 | Soup, vegetarian vegetable, canned, cond | 81.0 | 79.9 | 1.1 | pass |
| usda-170125 | Squash, summer, all varieties, cooked, b | 32.0 | 43.2 | 11.2 | pass |
| usda-170488 | Squash, summer, all varieties, cooked, b | 32.0 | 43.2 | 11.2 | pass |
| usda-170487 | Squash, summer, all varieties, raw | 41.0 | 57.6 | 16.6 | FAIL |
| usda-168466 | Squash, summer, crookneck and straightne | 22.0 | 28.8 | 6.8 | pass |
| usda-170126 | Squash, summer, crookneck and straightne | 32.0 | 48.0 | 16.0 | FAIL |
| usda-168465 | Squash, summer, crookneck and straightne | 32.0 | 48.0 | 16.0 | FAIL |
| usda-170532 | Squash, summer, crookneck and straightne | 45.0 | 62.4 | 17.4 | FAIL |
| usda-168468 | Squash, summer, crookneck and straightne | 45.0 | 62.4 | 17.4 | FAIL |
| usda-168467 | Squash, summer, crookneck and straightne | 29.0 | 38.4 | 9.4 | pass |
| usda-168464 | Squash, summer, crookneck and straightne | 33.0 | 48.0 | 15.0 | pass |
| usda-170533 | Squash, summer, scallop, cooked, boiled, | 36.0 | 48.0 | 12.0 | pass |
| usda-169290 | Squash, summer, scallop, cooked, boiled, | 36.0 | 48.0 | 12.0 | pass |
| usda-169289 | Squash, summer, scallop, raw | 42.0 | 57.6 | 15.6 | FAIL |
| usda-170534 | Squash, summer, zucchini, includes skin, | 22.0 | 52.8 | 30.8 | FAIL |
| usda-169292 | Squash, summer, zucchini, includes skin, | 22.0 | 52.8 | 30.8 | FAIL |
| usda-170535 | Squash, summer, zucchini, includes skin, | 40.0 | 57.6 | 17.6 | FAIL |
| usda-168470 | Squash, summer, zucchini, includes skin, | 40.0 | 57.6 | 17.6 | FAIL |
| usda-168469 | Squash, summer, zucchini, includes skin, | 41.0 | 57.6 | 16.6 | FAIL |
| usda-169291 | Squash, summer, zucchini, includes skin, | 43.0 | 57.6 | 14.6 | pass |
| usda-168471 | Squash, summer, zucchini, italian style, | 36.0 | 48.0 | 12.0 | pass |
| usda-170128 | Squash, winter, acorn, cooked, baked, wi | 44.0 | 52.8 | 8.8 | pass |
| usda-169293 | Squash, winter, acorn, cooked, baked, wi | 44.0 | 52.8 | 8.8 | pass |
| usda-170129 | Squash, winter, acorn, cooked, boiled, m | 26.0 | 33.6 | 7.6 | pass |
| usda-169294 | Squash, winter, acorn, cooked, boiled, m | 26.0 | 33.6 | 7.6 | pass |
| usda-168472 | Squash, winter, acorn, raw | 31.0 | 38.4 | 7.4 | pass |
| usda-170127 | Squash, winter, all varieties, cooked, b | 35.0 | 43.2 | 8.2 | pass |
| usda-170490 | Squash, winter, all varieties, cooked, b | 35.0 | 43.2 | 8.2 | pass |
| usda-170489 | Squash, winter, all varieties, raw | 57.0 | 48.0 | 9.0 | pass |
| usda-170130 | Squash, winter, butternut, cooked, baked | 35.0 | 43.2 | 8.2 | pass |
| usda-169296 | Squash, winter, butternut, cooked, baked | 35.0 | 43.2 | 8.2 | pass |
| usda-170536 | Squash, winter, butternut, frozen, cooke | 48.0 | 57.6 | 9.6 | pass |
| usda-168474 | Squash, winter, butternut, frozen, cooke | 48.0 | 57.6 | 9.6 | pass |
| usda-168473 | Squash, winter, butternut, frozen, unpre | 69.0 | 86.4 | 17.4 | FAIL |
| usda-169295 | Squash, winter, butternut, raw | 39.0 | 48.0 | 9.0 | pass |
| usda-170538 | Squash, winter, hubbard, cooked, boiled, | 58.0 | 72.0 | 14.0 | pass |
| usda-169297 | Squash, winter, hubbard, cooked, boiled, | 58.0 | 72.0 | 14.0 | pass |
| usda-168475 | Squash, winter, hubbard, raw | 78.0 | 96.0 | 18.0 | FAIL |
| usda-170539 | Squash, winter, spaghetti, cooked, boile | 24.0 | 33.6 | 9.6 | pass |
| usda-169299 | Squash, winter, spaghetti, cooked, boile | 24.0 | 33.6 | 9.6 | pass |
| usda-169298 | Squash, winter, spaghetti, raw | 24.0 | 28.8 | 4.8 | pass |
| usda-168172 | Strawberries, canned, heavy syrup pack,  | 16.0 | 19.8 | 3.8 | pass |
| usda-168174 | Strawberries, frozen, sweetened, sliced | 15.0 | 16.5 | 1.5 | pass |
| usda-168173 | Strawberries, frozen, unsweetened | 12.0 | 13.2 | 1.2 | pass |
| usda-167762 | Strawberries, raw | 19.0 | 23.1 | 4.1 | pass |
| usda-169305 | Sweet potato, canned, mashed | 119.0 | 92.0 | 27.0 | FAIL |
| usda-170084 | Sweet potato, canned, syrup pack, draine | 77.0 | 59.8 | 17.2 | FAIL |
| usda-170083 | Sweet potato, canned, syrup pack, solids | 56.0 | 46.0 | 10.0 | pass |
| usda-168485 | Sweet potato, canned, vacuum pack | 94.0 | 78.2 | 15.8 | FAIL |
| usda-170134 | Sweet potato, cooked, baked in skin, fle | 114.0 | 92.0 | 22.0 | FAIL |
| usda-168483 | Sweet potato, cooked, baked in skin, fle | 114.0 | 92.0 | 22.0 | FAIL |
| usda-168484 | Sweet potato, cooked, boiled, without sk | 78.0 | 64.4 | 13.6 | pass |
| usda-170541 | Sweet potato, cooked, boiled, without sk | 99.0 | 64.4 | 34.6 | FAIL |
| usda-170088 | Sweet potato, cooked, candied, home-prep | 49.0 | 41.4 | 7.6 | pass |
| usda-170542 | Sweet potato, frozen, cooked, baked, wit | 103.0 | 78.2 | 24.8 | FAIL |
| usda-169307 | Sweet potato, frozen, cooked, baked, wit | 103.0 | 78.2 | 24.8 | FAIL |
| usda-169306 | Sweet potato, frozen, unprepared | 102.0 | 78.2 | 23.8 | FAIL |
| usda-168482 | Sweet potato, raw, unprepared | 89.0 | 73.6 | 15.4 | FAIL |
| usda-170681 | Syrup, NESTLE, chocolate | 75.0 | 0.0 | 75.0 | FAIL |
| usda-169925 | Tangerine juice, raw | 6.0 | 23.5 | 17.5 | FAIL |
| usda-169106 | Tangerines, (mandarin oranges), canned,  | 20.0 | 28.2 | 8.2 | pass |
| usda-169924 | Tangerines, (mandarin oranges), canned,  | 15.0 | 23.5 | 8.5 | pass |
| usda-169105 | Tangerines, (mandarin oranges), raw | 18.0 | 37.6 | 19.6 | FAIL |
| usda-169717 | Tapioca, pearl, dry | 4.0 | 9.4 | 5.4 | pass |
| usda-170543 | Taro, cooked, with salt | 28.0 | 23.5 | 4.5 | pass |
| usda-168486 | Taro, cooked, without salt | 28.0 | 23.5 | 4.5 | pass |
| usda-169308 | Taro, raw | 82.0 | 70.5 | 11.5 | pass |
| usda-170545 | Tomato juice, canned, without salt added | 26.0 | 29.7 | 3.7 | pass |
| usda-170546 | Tomato products, canned, puree, with sal | 35.0 | 56.1 | 21.1 | FAIL |
| usda-170460 | Tomato products, canned, puree, without  | 34.0 | 56.1 | 22.1 | FAIL |
| usda-170054 | Tomato products, canned, sauce | 40.0 | 39.6 | 0.4 | pass |
| usda-170085 | Tomato products, canned, sauce, spanish  | 30.0 | 46.2 | 16.2 | FAIL |
| usda-170055 | Tomato products, canned, sauce, with mus | 39.0 | 49.5 | 10.5 | pass |
| usda-170056 | Tomato products, canned, sauce, with oni | 36.0 | 52.8 | 16.8 | FAIL |
| usda-170462 | Tomato products, canned, sauce, with oni | 21.0 | 29.7 | 8.7 | pass |
| usda-170463 | Tomato products, canned, sauce, with tom | 28.0 | 42.9 | 14.9 | pass |
| usda-169074 | Tomato sauce, canned, no salt added | 36.0 | 39.6 | 3.6 | pass |
| usda-170501 | Tomatoes, crushed, canned | 40.0 | 52.8 | 12.8 | pass |
| usda-170456 | Tomatoes, green, raw | 31.0 | 39.6 | 8.6 | pass |
| usda-170502 | Tomatoes, orange, raw | 30.0 | 39.6 | 9.6 | pass |
| usda-170051 | Tomatoes, red, ripe, canned, packed in t | 27.0 | 26.4 | 0.6 | pass |
| usda-170138 | Tomatoes, red, ripe, canned, packed in t | 27.0 | 26.4 | 0.6 | pass |
| usda-170052 | Tomatoes, red, ripe, canned, stewed | 25.0 | 29.7 | 4.7 | pass |
| usda-170050 | Tomatoes, red, ripe, cooked | 28.0 | 33.0 | 5.0 | pass |
| usda-170089 | Tomatoes, red, ripe, cooked, stewed | 75.0 | 66.0 | 9.0 | pass |
| usda-170137 | Tomatoes, red, ripe, cooked, with salt | 28.0 | 33.0 | 5.0 | pass |
| usda-170457 | Tomatoes, red, ripe, raw, year round ave | 27.0 | 29.7 | 2.7 | pass |
| usda-170096 | Tomatoes, yellow, raw | 25.0 | 33.0 | 8.0 | pass |
| usda-168841 | Toppings, butterscotch or caramel | 71.0 | 56.4 | 14.6 | pass |
| usda-170467 | Turnip greens, canned, solids and liquid | 83.0 | 65.8 | 17.2 | FAIL |
| usda-170139 | Turnip greens, cooked, boiled, drained,  | 70.0 | 51.7 | 18.3 | FAIL |
| usda-170466 | Turnip greens, cooked, boiled, drained,  | 70.0 | 51.7 | 18.3 | FAIL |
| usda-170061 | Turnip greens, raw | 92.0 | 70.5 | 21.5 | FAIL |
| usda-170547 | Turnips, cooked, boiled, drained, with s | 14.0 | 32.9 | 18.9 | FAIL |
| usda-170058 | Turnips, cooked, boiled, drained, withou | 14.0 | 32.9 | 18.9 | FAIL |
| usda-170548 | Turnips, frozen, cooked, boiled, drained | 30.0 | 70.5 | 40.5 | FAIL |
| usda-170060 | Turnips, frozen, cooked, boiled, drained | 30.0 | 70.5 | 40.5 | FAIL |
| usda-170059 | Turnips, frozen, unprepared | 20.0 | 47.0 | 27.0 | FAIL |
| usda-170465 | Turnips, raw | 17.0 | 42.3 | 25.3 | FAIL |
| usda-170063 | Vegetable juice cocktail, canned | 28.0 | 43.2 | 15.2 | FAIL |
| usda-170473 | Vegetable juice cocktail, low sodium, ca | 27.0 | 43.2 | 16.2 | FAIL |
| usda-171422 | Vegetable oil, palm kernel | 0.0 | 0.0 | 0.0 | pass |
| usda-170064 | Vegetables, mixed, canned, solids and li | 60.0 | 67.2 | 7.2 | pass |
| usda-173469 | Vinegar, cider | 0.0 | 0.0 | 0.0 | pass |
| usda-170474 | Vinespinach, (basella), raw | 85.0 | 84.6 | 0.4 | pass |
| usda-167765 | Watermelon, raw | 15.0 | 28.2 | 13.2 | pass |
| usda-170885 | Whey, acid, fluid | 25.0 | 38.4 | 13.4 | pass |
| usda-171282 | Whey, sweet, fluid | 27.0 | 43.2 | 16.2 | FAIL |
| usda-170551 | Yam, cooked, boiled, drained, or baked,  | 69.0 | 70.5 | 1.5 | pass |
| usda-170072 | Yam, cooked, boiled, drained, or baked,  | 69.0 | 70.5 | 1.5 | pass |
| usda-170071 | Yam, raw | 71.0 | 70.5 | 0.5 | pass |
| usda-169358 | Yambean (jicama), cooked, boiled, draine | 17.0 | 32.9 | 15.9 | FAIL |
| usda-170074 | Yambean (jicama), cooked, boiled, draine | 17.0 | 32.9 | 15.9 | FAIL |
| usda-170073 | Yambean (jicama), raw | 17.0 | 32.9 | 15.9 | FAIL |
