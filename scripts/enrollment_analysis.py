"""
Task 5: 2010/2013 Higher Education Enrollment Analysis
Analyzes enrollment data for top 3 countries from Task 2
Task 5b: Finds country with highest enrollment globally in 2010
"""

import requests
import pandas as pd
import duckdb
from pathlib import Path
import time

# Config
BASE_URL = "https://api.worldbank.org/v2"
DATA_DIR = Path(__file__).parent.parent / 'data'
DB_PATH = DATA_DIR / 'universities.duckdb'

# Top 3 countries from Task 2
COUNTRIES = {
    'United States': 'USA',
    'Japan': 'JPN',
    'India': 'IND'
}

def fetch_indicator(country_code, indicator_code, year):
    """Get World Bank indicator data for country and year"""
    url = f"{BASE_URL}/country/{country_code}/indicator/{indicator_code}"
    params = {'format': 'json', 'date': year}
    
    response = requests.get(url, params=params, timeout=20)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 1 and data[1]:
            return data[1][0].get('value')
    return None

def get_enrollment_data(country_code, year):
    """Get enrollment data for a specific year"""
    indicators = {
        'enrollment_rate': 'SE.TER.ENRR',
        'total_enrolled': 'SE.TER.ENRL',
        'population': 'SP.POP.TOTL'
    }
    
    result = {'year': year}
    
    for key, code in indicators.items():
        result[key] = fetch_indicator(country_code, code, year)
    
    # Calculate total_enrolled if missing but we have rate and population
    if result['total_enrolled'] is None and result['enrollment_rate'] and result['population']:
        result['total_enrolled'] = (result['enrollment_rate'] / 100) * result['population']
        result['total_enrolled_calculated'] = True
    else:
        result['total_enrolled_calculated'] = False
    
    return result

# Task 5a: Fetch data for both years
print("TASK 5a: Fetching enrollment data for top 3 countries")
print("-" * 60)

enrollment_data = []

for country_name, country_code in COUNTRIES.items():
    print(f"\n{country_name}:")
    
    # Get 2010 data
    data_2010 = get_enrollment_data(country_code, 2010)
    data_2010['country'] = country_name
    data_2010['iso_code'] = country_code
    enrollment_data.append(data_2010)
    
    if data_2010['enrollment_rate'] and data_2010['total_enrolled']:
        print(f"  2010 - Rate: {data_2010['enrollment_rate']:.2f}% | "
              f"Enrolled: {data_2010['total_enrolled']:,.0f}")
    else:
        print("  2010 - No data")
    
    # Get 2013 data
    data_2013 = get_enrollment_data(country_code, 2013)
    data_2013['country'] = country_name
    data_2013['iso_code'] = country_code
    enrollment_data.append(data_2013)
    
    if data_2013['enrollment_rate'] and data_2013['total_enrolled']:
        print(f"  2013 - Rate: {data_2013['enrollment_rate']:.2f}% | "
              f"Enrolled: {data_2013['total_enrolled']:,.0f}")
    else:
        print("  2013 - No data")

df_all = pd.DataFrame(enrollment_data)

# Show enrollment percentages
print("\n" + "=" * 60)
print("ENROLLMENT PERCENTAGES")
print("=" * 60)

for _, row in df_all.iterrows():
    if row['enrollment_rate']:
        calc_note = " (calculated)" if row.get('total_enrolled_calculated') else ""
        print(f"{row['country']} ({row['year']}): {row['enrollment_rate']:.2f}%{calc_note}")

# Compare where data exists for all three in same year
print("\n" + "=" * 60)
print("COMPARISON FOR YEARS WITH COMPLETE DATA")
print("=" * 60)

for year in [2010, 2013]:
    df_year = df_all[df_all['year'] == year].copy()
    df_complete = df_year[df_year['total_enrolled'].notna()]
    
    if len(df_complete) == 3:
        print(f"\n{year} (complete data for all 3 countries):")
        for rank, (_, row) in enumerate(df_complete.sort_values('total_enrolled', ascending=False).iterrows(), 1):
            print(f"  {rank}. {row['country']}: {row['total_enrolled']:,.0f} students")
    else:
        print(f"\n{year}: Only {len(df_complete)}/3 countries have data")

# Task 5b: Get ALL countries' 2010 enrollment data
print("\n" + "=" * 60)
print("TASK 5b: HIGHEST ENROLLMENT GLOBALLY IN 2010")
print("=" * 60)

print("\nFetching 2010 enrollment data for all countries...")

# Get list of all countries
countries_url = f"{BASE_URL}/country?format=json&per_page=300"
response = requests.get(countries_url, timeout=20)
all_countries = []

if response.status_code == 200:
    country_data = response.json()[1]
    # Filter to actual countries (not regions/aggregates)
    all_countries = [(c['name'], c['id']) for c in country_data 
                     if c['region']['value'] != 'Aggregates']

print(f"Checking {len(all_countries)} countries...")

global_enrollment = []

for country_name, country_code in all_countries:
    enrollment = fetch_indicator(country_code, 'SE.TER.ENRL', 2010)
    
    if enrollment:
        global_enrollment.append({
            'country': country_name,
            'iso_code': country_code,
            'year': 2010,
            'total_enrolled': enrollment
        })
    
    time.sleep(0.1)  # Rate limiting

df_global = pd.DataFrame(global_enrollment)

if not df_global.empty:
    # Sort and get top country
    df_global_sorted = df_global.sort_values('total_enrolled', ascending=False)
    top_country = df_global_sorted.iloc[0]
    
    print(f"\nCountry with highest enrollment in 2010: {top_country['country']}")
    print(f"Total enrolled: {top_country['total_enrolled']:,.0f} students")
    
    print("\nTop 10 countries by enrollment (2010):")
    for rank, (_, row) in enumerate(df_global_sorted.head(10).iterrows(), 1):
        print(f"  {rank:2d}. {row['country']:<30s} {row['total_enrolled']:>15,.0f}")
    
    # Where do our top 3 rank globally?
    print("\nRankings of our top 3 countries:")
    for country_name in COUNTRIES.keys():
        country_data = df_global_sorted[df_global_sorted['country'] == country_name]
        if not country_data.empty:
            rank = df_global_sorted.index.get_loc(country_data.index[0]) + 1
            enrollment = country_data.iloc[0]['total_enrolled']
            print(f"  {rank:2d}. {country_name}: {enrollment:,.0f}")
else:
    print("\nNo global data retrieved")

# Save to database
print("\n" + "=" * 60)
print("SAVING TO DATABASE")
print("=" * 60)

con = duckdb.connect(str(DB_PATH))

# Task 5a: All data (both years)
con.execute("DROP TABLE IF EXISTS enrollment_percentages")
con.execute("CREATE TABLE enrollment_percentages AS SELECT * FROM df_all")
print("Created table: enrollment_percentages (all years)")

# Task 5b: Global highest in 2010
if not df_global.empty:
    con.execute("DROP TABLE IF EXISTS highest_enrollment_global_2010")
    con.execute("CREATE TABLE highest_enrollment_global_2010 AS SELECT * FROM df_global")
    print("Created table: highest_enrollment_global_2010")

# Verification
print("\nVerification:")
print("\nTask 5a - Enrollment data for top 3 countries:")
print(con.execute("""
    SELECT country, year, enrollment_rate, total_enrolled 
    FROM enrollment_percentages 
    ORDER BY country, year
""").df().to_string(index=False))

if not df_global.empty:
    print("\nTask 5b - Top 5 countries globally (2010):")
    print(con.execute("""
        SELECT country, total_enrolled 
        FROM highest_enrollment_global_2010 
        ORDER BY total_enrolled DESC 
        LIMIT 5
    """).df().to_string(index=False))

con.close()

print("\nTask 5 complete.")