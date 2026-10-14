Instruction: From a question/request writen in natural language generate a coresponding SQL query. Do not use script to generate the query , generate them all on your own.

Context: You are working with a relational database containing information about restaurants, their locations, and geographical areas. Use only the tables and columns defined in the schema 

Database schema:
RESTAURANT(ID, NAME, FOOD_TYPE, CITY_NAME, RATING)
LOCATION(RESTAURANT_ID, HOUSE_NUMBER, STREET_NAME, CITY_NAME)
GEOGRAPHIC(CITY_NAME, COUNTY, REGION)

Input: A natural language request describing the information that we want to get from the database.

Output: Return the result in CSV format with exactly two columns: natural_language and sql_query. Each row must contain the original natural-language request and the corresponding SQL SELECT query. Include a header row. Generate one row for each request. Escape quotation marks and other special characters according to CSV rules.
