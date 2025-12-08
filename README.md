# Universities API Analysis

A data engineering project that fetches, processes, and analyzes global universities data from a REST API.

## 📋 Project Overview

This project demonstrates ETL capabilities by working with the Universities API to answer specific business questions about global higher education institutions.

### Business Questions
1. ✅ Data Cleaning: Remove the "domains" column
2. ✅ Top Performers: Which three countries have the most universities?
3. ✅ Specific Analysis: How many universities are in the UK, France, and China?
4. ✅ Data Persistence: Store results in a database
5. ⏳ (Optional) Historical Analysis: 2010 enrollment statistics

## 🛠️ Tech Stack

- **Python 3.11+** - Core programming language
- **requests** - REST API interaction
- **pandas** - Data manipulation and analysis
- **DuckDB** - Embedded analytical database
- **Jupyter** - Interactive exploration

## 📡 Data Sources

### Primary Source: Local JSON File
- **Source**: [University Domains List by Hipo](https://github.com/Hipo/university-domains-list)
- **File**: `data/world_universities_and_domains.json`
- **Usage**: Tasks 1 & 2 (comprehensive dataset)
- **Reason**: More reliable than API, contains complete data

### Secondary Source: REST API
- **Endpoint**: http://universities.hipolabs.com/search
- **Usage**: Task 3 (country-specific queries with fallback)
- **Parameters**: `?country={country_name}`

## 🔄 Hybrid Approach

The solution uses a hybrid approach for maximum reliability:
1. **Local JSON**: Primary data source for comprehensive analysis
2. **API Queries**: Validation and country-specific data (with fallback)
3. **DuckDB**: Persistent storage for results

## 📁 Project Structure
```
universities-api-analysis/
├── data/                        # Folder to hold local json, because full API extract fails
├── scripts/
│   ├── fetch_universities.py    # Main ETL script
│   └── analyze_universities.py  # Additional analysis
├── notebooks/
│   └── 01_api_exploration.ipynb # Interactive exploration
├── data/
│   └── universities.duckdb      # Output database (gitignored)
├── docs/
│   └── analysis_results.md      # Analysis findings
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/<your-username>/universities-api-analysis.git
cd universities-api-analysis
```

2. Create and activate virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Analysis
```bash
# Run the main analysis script
python scripts/fetch_universities.py
```

### Exploring the Data
```bash
# Launch Jupyter notebook
jupyter notebook notebooks/01_api_exploration.ipynb
```

### Querying Results
```python
import duckdb

# Connect to the database
con = duckdb.connect('data/universities.duckdb')

# View Task 3 results
con.execute("""
    SELECT * FROM universities.uk_france_china_counts
""").df()

# Explore all universities
con.execute("""
    SELECT country, COUNT(*) as count
    FROM universities.all_universities
    GROUP BY country
    ORDER BY count DESC
    LIMIT 10
""").df()
```

## 📊 Key Findings

### Task 1: Data Cleaning
✅ Successfully removed 'domains' column from dataset
- Original columns: 7 (including domains)
- Final columns: 6 (domains removed)
- Total universities: [X,XXX]

### Task 2: Top 3 Countries by University Count

 rank       country  university_count
    1 United States              2349
    2         Japan               572
    3         India               474

### Task 3: UK, France, China Comparison

       country  university_count data_source
         China               398         API
        France               297         API
United Kingdom               195         API

### Task 4: Database Storage
✅ Successfully stored all results in DuckDB

**Tables Created**:
- `all_universities` - [10,191] rows
- `top_3_countries` - 3 rows
- `uk_france_china_counts` - 3 rows

### Additional Insights

**Global Coverage**:
- Total countries represented: [202]
- Total universities analyzed: [10,191]

**Top 10 Countries**:
           country  count
     United States   2349
             Japan    572
             India    474
             China    398
           Germany    318
Russian Federation    309
            France    297
Korea, Republic of    244
    United Kingdom    195
              Iran    193

## 🎓 Analysis Date
December 8, 2024

## 🏗️ Architecture
```
API Source → Python ETL → Pandas Processing → DuckDB Storage
     ↓           ↓              ↓                  ↓
 REST API    requests      Data Cleaning      Analytical
 LOCAL JSON  library      Transformation       Database
```

## 📈 Data Pipeline

1. **Extract**: Fetch data from Universities API/manual json download
2. **Transform**: 
   - Remove unnecessary columns
   - Clean and validate data
   - Aggregate by country
3. **Load**: Store in DuckDB for querying

## 🎓 Learning Objectives

- REST API integration and error handling
- Data manipulation with pandas
- Embedded database usage (DuckDB)
- ETL pipeline design
- Data quality validation

## 📝 Development Log

- [x] API exploration and data profiling
- [x] Main ETL script development
- [x] Data cleaning implementation
- [x] Aggregation and analysis
- [x] Database persistence
- [x] Documentation and findings
- [x] Optional: Historical enrollment analysis

## 🤝 Contributing

This is a portfolio project, but feedback and suggestions are welcome!

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

**Aydin Aksoy**
- GitHub: [@yTheBoogieman](https://github.com/TheBoogieman)
- LinkedIn: [Aydin Aksoy](https://www.linkedin.com/in/ayd%C4%B1n-aksoy-138714106/)

**API Source**: [Universities API by hipolabs](http://universities.hipolabs.com)
