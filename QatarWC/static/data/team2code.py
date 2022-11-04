# Replace country names with codes in the fixtures data
from csv import reader
import pandas as pd

# Import the country-code data
countries = []
codes = []
with open("team_groups.csv") as file:
    for row in reader(file):
        countries.append(row[1])
        codes.append(row[0])

# Replace code for country in fixtures data
df = pd.read_csv("fixtures.csv", delimiter=";")
df = df.replace(countries, codes)

# Change date format (for SQL)
df['date'] = pd.to_datetime(df.date, infer_datetime_format=True)
print(df)

# Save data
df.to_csv("fixtures.csv", index=False)