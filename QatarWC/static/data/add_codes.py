# DATA TRANSFORMATION
# Adding country codes to the teams-groups data
import pandas as pd
import sys


#print(sys.path) # Check issues with path

# Import the data 
df = pd.read_csv("teams.csv", delimiter=";")

# Add country codes to the data
def generate_country_code(country):
    """Generates the code of a country by capitalizing the first three letters"""
    return country[:3].upper()

# Add Code column to data
df['Code']=df['Team'].apply(generate_country_code)

# Replace exceptions
df = df.replace(['NET', 'IRA', 'SAU', 'JAP', 'SPA', 'COS', 'MOR', 'SWI', 'CAM', 'SER', 'SOU'],
                ['NED', 'IRN', 'KSA', 'JPN', 'ESP', 'CRC', 'MAR', 'SUI', 'CMR', 'SRB', 'KOR'])

df.iloc[6,0] = 'United States'

# Set the code column as first column (index)
df = df.set_index('Code')
print(df)

# Save data
df.to_csv("team_groups.csv")

