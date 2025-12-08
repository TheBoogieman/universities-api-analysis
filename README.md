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

(To be populated after analysis completion)

### Top 3 Countries by University Count
1. TBD
2. TBD
3. TBD

### UK, France, China Comparison
- United Kingdom: TBD universities
- France: TBD universities
- China: TBD universities

## 🏗️ Architecture
```
API Source → Python ETL → Pandas Processing → DuckDB Storage
     ↓           ↓              ↓                  ↓
 REST API    requests      Data Cleaning      Analytical
             library      Transformation       Database
```

## 📈 Data Pipeline

1. **Extract**: Fetch data from Universities API
2. **Transform**: 
   - Remove unnecessary columns
   - Clean and validate data
   - Aggregate by country
3. **Load**: Store in DuckDB for querying

## 🧪 Data Quality

- Total universities: TBD
- Countries covered: TBD
- Data completeness: TBD%
- Missing values: TBD

## 🎓 Learning Objectives

- REST API integration and error handling
- Data manipulation with pandas
- Embedded database usage (DuckDB)
- ETL pipeline design
- Data quality validation

## 📝 Development Log

- [ ] API exploration and data profiling
- [ ] Main ETL script development
- [ ] Data cleaning implementation
- [ ] Aggregation and analysis
- [ ] Database persistence
- [ ] Documentation and findings
- [ ] Optional: Historical enrollment analysis

## 🤝 Contributing

This is a portfolio project, but feedback and suggestions are welcome!

## 📄 License

MIT License - see LICENSE file for details

## 👤 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your Profile](https://linkedin.com/in/your-profile)

**API Source**: [Universities API by hipolabs](http://universities.hipolabs.com)
**Data Engineering Case Study Series**