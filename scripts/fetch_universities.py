"""
Case Study 2: Universities API Analysis
Processes university data from local JSON and API sources
"""

import requests
import pandas as pd
import duckdb
import json
from pathlib import Path
from datetime import datetime

# Configuration
API_URL = "http://universities.hipolabs.com/search"
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
DATA_DIR.mkdir(exist_ok=True)

JSON_PATH = DATA_DIR / 'world_universities_and_domains.json'
DB_PATH = DATA_DIR / 'universities.duckdb'

print("=" * 80)
print("🎓 UNIVERSITIES API ANALYSIS")
print("=" * 80)
print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📁 Data Source: {JSON_PATH}")
print(f"📡 API (for validation): {API_URL}")
print(f"🗄️  Database: {DB_PATH}")

# ============================================================================
# TASK 1: Load data and remove 'domains' column
# ============================================================================
print("\n" + "=" * 80)
print("TASK 1: LOAD DATA & REMOVE 'DOMAINS' COLUMN")
print("=" * 80)

print(f"\n📥 Loading data from local JSON file...")

if not JSON_PATH.exists():
    print(f"✗ JSON file not found at: {JSON_PATH}")
    print("Please download from: https://github.com/Hipo/university-domains-list")
    exit(1)

try:
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"✓ Loaded {len(data):,} universities from JSON")
except Exception as e:
    print(f"✗ Error loading JSON: {e}")
    exit(1)

# Convert to DataFrame
df = pd.DataFrame(data)
print(f"✓ Converted to DataFrame: {df.shape}")

print(f"\n📋 Original columns: {list(df.columns)}")

# Remove 'domains' column
if 'domains' in df.columns:
    domains_sample = df['domains'].head(3).tolist()
    print(f"\n📦 Sample 'domains' values before removal:")
    for i, domain_list in enumerate(domains_sample, 1):
        print(f"  {i}. {domain_list}")
    
    df = df.drop(columns=['domains'])
    print(f"\n✓ Removed 'domains' column")
else:
    print(f"⚠️  'domains' column not found in data")

print(f"\n📋 Final columns: {list(df.columns)}")
print(f"📊 Final shape: {df.shape}")

# Show sample data
print(f"\n📄 Sample data after removing 'domains':")
print(df.head(3).to_string())

# ============================================================================
# TASK 2: Top 3 countries by university count
# ============================================================================
print("\n" + "=" * 80)
print("TASK 2: TOP 3 COUNTRIES BY UNIVERSITY COUNT")
print("=" * 80)

country_counts = df['country'].value_counts().head(3)

print("\n🏆 Top 3 Countries:")
top_3_results = []
for rank, (country, count) in enumerate(country_counts.items(), 1):
    print(f"  {rank}. {country}: {count:,} universities")
    top_3_results.append({
        'rank': rank,
        'country': country,
        'university_count': count
    })

top_3_df = pd.DataFrame(top_3_results)

# ============================================================================
# TASK 3: Count universities in UK, France, and China (using API)
# ============================================================================
print("\n" + "=" * 80)
print("TASK 3: UNIVERSITIES IN UK, FRANCE, AND CHINA")
print("=" * 80)

print("\n📡 Fetching country-specific data from API...")

target_countries = {
    'United Kingdom': 'United Kingdom',
    'France': 'France', 
    'China': 'China'
}

results = []

for display_name, api_country in target_countries.items():
    print(f"\n🔍 Querying API for: {display_name}")
    
    try:
        response = requests.get(
            API_URL, 
            params={'country': api_country},
            timeout=10
        )
        
        if response.status_code == 200:
            country_data = response.json()
            count = len(country_data)
            print(f"  ✓ API returned: {count:,} universities")
        else:
            print(f"  ⚠️  API failed (status {response.status_code}), using local data")
            count = len(df[df['country'] == display_name])
            print(f"  ✓ Local data: {count:,} universities")
            
    except requests.exceptions.RequestException as e:
        print(f"  ⚠️  API error: {e}")
        print(f"  ℹ️  Falling back to local data")
        count = len(df[df['country'] == display_name])
        print(f"  ✓ Local data: {count:,} universities")
    
    results.append({
        'country': display_name,
        'university_count': count,
        'analysis_date': datetime.now().strftime('%Y-%m-%d'),
        'data_source': 'API' if response.status_code == 200 else 'Local JSON'
    })

print("\n📊 Final University Counts:")
for result in results:
    print(f"  {result['country']}: {result['university_count']:,} universities ({result['data_source']})")

# Create results DataFrame
results_df = pd.DataFrame(results)

# ============================================================================
# TASK 4: Write results to database
# ============================================================================
print("\n" + "=" * 80)
print("TASK 4: WRITE TO DATABASE")
print("=" * 80)

print(f"\n🗄️  Connecting to DuckDB: {DB_PATH}")
con = duckdb.connect(str(DB_PATH))

# Write full dataset (without domains) - no schema, just tables
print("\n📊 Writing full universities dataset...")
con.execute("DROP TABLE IF EXISTS all_universities")
con.execute("CREATE TABLE all_universities AS SELECT * FROM df")
row_count = con.execute("SELECT COUNT(*) FROM all_universities").fetchone()[0]
print(f"✓ Wrote {row_count:,} rows to all_universities")

# Write Task 2 results (Top 3 countries)
print("\n📊 Writing Task 2 results (Top 3 countries)...")
con.execute("DROP TABLE IF EXISTS top_3_countries")
con.execute("CREATE TABLE top_3_countries AS SELECT * FROM top_3_df")
row_count = con.execute("SELECT COUNT(*) FROM top_3_countries").fetchone()[0]
print(f"✓ Wrote {row_count} rows to top_3_countries")

# Write Task 3 results (UK, France, China)
print("\n📊 Writing Task 3 results (UK, France, China)...")
con.execute("DROP TABLE IF EXISTS uk_france_china_counts")
con.execute("CREATE TABLE uk_france_china_counts AS SELECT * FROM results_df")
row_count = con.execute("SELECT COUNT(*) FROM uk_france_china_counts").fetchone()[0]
print(f"✓ Wrote {row_count} rows to uk_france_china_counts")

# Verify the data
print("\n✅ Verification - Task 2 (Top 3):")
verification = con.execute("""
    SELECT * FROM top_3_countries
    ORDER BY rank
""").fetchdf()
print(verification.to_string(index=False))

print("\n✅ Verification - Task 3 (UK, France, China):")
verification = con.execute("""
    SELECT country, university_count, data_source 
    FROM uk_france_china_counts
    ORDER BY university_count DESC
""").fetchdf()
print(verification.to_string(index=False))

# Additional insights
print("\n📊 Additional Insights:")

# Total countries
total_countries = con.execute("""
    SELECT COUNT(DISTINCT country) as country_count
    FROM all_universities
""").fetchone()[0]
print(f"  Total countries: {total_countries}")

# Top 10 countries
print("\n🌍 Top 10 Countries by University Count:")
top_10 = con.execute("""
    SELECT country, COUNT(*) as count
    FROM all_universities
    GROUP BY country
    ORDER BY count DESC
    LIMIT 10
""").fetchdf()
print(top_10.to_string(index=False))

con.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("📋 SUMMARY")
print("=" * 80)

print(f"""
✅ Task 1: Loaded data from local JSON and removed 'domains' column
✅ Task 2: Identified top 3 countries by university count
✅ Task 3: Counted universities in UK, France, and China (API + fallback)
✅ Task 4: Wrote results to DuckDB database

📊 Database Tables Created:
  1. all_universities ({len(df):,} rows)
  2. top_3_countries (3 rows)
  3. uk_france_china_counts (3 rows)

🗄️  Database Location: {DB_PATH}
📁 Source Data: {JSON_PATH}
""")

print("=" * 80)
print("✓ ANALYSIS COMPLETE")
print("=" * 80)
print(f"⏰ Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")