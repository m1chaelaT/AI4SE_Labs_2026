Translate each question into one SQLite query. Write the queries yourself, not with a script.

Tables: RESTAURANT(ID, NAME, FOOD_TYPE, CITY_NAME, RATING), LOCATION(RESTAURANT_ID, HOUSE_NUMBER, STREET_NAME, CITY_NAME), GEOGRAPHIC(CITY_NAME, COUNTY, REGION)
All text values are lowercase. Regions such as "napa valley" are stored in GEOGRAPHIC.REGION.

For each question, think step by step:
1. Remove the parts of the question that are unrelated to the search.
2. Identify the filters: city or region, street, food type, rating, "best".
3. Map each filter to a column and write the query. It returns `LOCATION.HOUSE_NUMBER, RESTAURANT.NAME` without DISTINCT.
4. Check that no filter is missing or added.

Input: column `question` in `Week_03_Prompting/Assignments/Task_2/data/restaurants_dataset.csv` (do not read the `result` column).
Output: `Week_03_Prompting/Assignments/Task_2/predictions/predictions_P3_CoT.csv` with columns `question,predicted_sql`, one row per question. Write a short note on steps 1–2 for each question to `reasoning_P3_CoT.txt` in the same folder.