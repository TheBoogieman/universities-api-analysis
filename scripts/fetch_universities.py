"""
Case Study 2: Universities API Analysis
Fetches and processes university data from hipolabs API
"""

import requests
import pandas as pd
import duckdb
from pathlib import Path
from datetime import datetime

# Configuration
API_URL = "http://universities.hipolabs.com/search"
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / 'universities.duckdb'

print("=" * 80)
print("🎓 UNIVERSITIES API ANALYSIS - CASE STUDY 2")
print("=" * 80)
print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"📡 API: {API_URL}")
print(f"🗄️  Database: {DB_PATH}")

# ============================================================================
# TASK 1: Fetch data and remove 'domains' column
# ============================================================================
print("\n" + "=" * 80)
print("TASK 1: FETCH DATA & REMOVE 'DOMAINS' COLUMN")
print("=" * 80)

print("\n📥 Fetching data from API...")
try:
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"✗ API request failed: {e}")
    exit(1)

data = response.json()
print(f"✓ Retrieved {len(data):,} universities")

# Convert to DataFrame
df = pd.DataFrame(data)
print(f"✓ Converted to DataFrame: {df.shape}")

print(f"\n📋 Original columns: {list(df.columns)}")

# Remove 'domains' column
if 'domains' in df.columns:
    df = df.drop(columns=['domains'])
    print(f"✓ Removed 'domains' column")
else:
    print(f"⚠️  'domains' column not found")

print(f"📋 Final columns: {list(df.columns)}")
print(f"📊 Final shape: {df.shape}")

# ============================================================================
# TASK 2: Top 3 countries by university count
# ============================================================================
print("\n" + "=" * 80)
print("TASK 2: TOP 3 COUNTRIES BY UNIVERSITY COUNT")
print("=" * 80)

country_counts = df['country'].value_counts().head(3)

print("\n🏆 Top 3 Countries:")
for rank, (country, count) in enumerate(country_counts.items(), 1):
    print(f"  {rank}. {country}: {count:,} universities")

# ============================================================================
# TASK 3: Count universities in UK, France, and China
# ============================================================================
print("\n" + "=" * 80)
print("TASK 3: UNIVERSITIES IN UK, FRANCE, AND CHINA")
print("=" * 80)

target_countries = ['United Kingdom', 'France', 'China']

print("\n📊 University Counts:")
results = []

for country in target_countries:
    count = len(df[df['country'] == country])
    print(f"  {country}: {count:,} universities")
    results.append({
        'country': country,
        'university_count': count,
        'analysis_date': datetime.now().strftime('%Y-%m-%d')
    })

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

# Create schema
con.execute("CREATE SCHEMA IF NOT EXISTS universities")

# Write full dataset (without domains)
print("\n📊 Writing full universities dataset...")
con.execute("DROP TABLE IF EXISTS universities.all_universities")
con.execute("CREATE TABLE universities.all_universities AS SELECT * FROM df")
row_count = con.execute("SELECT COUNT(*) FROM universities.all_universities").fetchone()[0]
print(f"✓ Wrote {row_count:,} rows to universities.all_universities")

# Write Task 3 results
print("\n📊 Writing Task 3 results...")
con.execute("DROP TABLE IF EXISTS universities.uk_france_china_counts")
con.execute("CREATE TABLE universities.uk_france_china_counts AS SELECT * FROM results_df")
row_count = con.execute("SELECT COUNT(*) FROM universities.uk_france_china_counts").fetchone()[0]
print(f"✓ Wrote {row_count} rows to universities.uk_france_china_counts")

# Verify the data
print("\n✅ Verification:")
verification = con.execute("""
    SELECT * FROM universities.uk_france_china_counts
    ORDER BY university_count DESC
""").fetchdf()
print(verification.to_string(index=False))

con.close()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("📋 SUMMARY")
print("=" * 80)

print(f"""
✅ Task 1: Removed 'domains' column from dataset
✅ Task 2: Identified top 3 countries by university count
✅ Task 3: Counted universities in UK, France, and China
✅ Task 4: Wrote results to DuckDB database

📊 Database Tables Created:
  1. universities.all_universities ({len(df):,} rows)
  2. universities.uk_france_china_counts (3 rows)

🗄️  Database Location: {DB_PATH}
""")

print("=" * 80)
print("✓ ANALYSIS COMPLETE")
print("=" * 80)
print(f"⏰ Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")