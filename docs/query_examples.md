# Query Examples

## Connecting to the Database
```python
import duckdb

# Connect to the database
con = duckdb.connect('data/universities.duckdb')
```

## Sample Queries

### View All Tables
```sql
SHOW TABLES;
```

### Query Top 3 Countries
```sql
SELECT * 
FROM top_3_countries 
ORDER BY rank;
```

### Query UK, France, China Results
```sql
SELECT 
    country,
    university_count,
    data_source
FROM uk_france_china_counts
ORDER BY university_count DESC;
```

### Find Universities by Country
```sql
SELECT 
    name,
    country,
    alpha_two_code,
    web_pages
FROM all_universities
WHERE country = 'United Kingdom'
LIMIT 10;
```

### Count Universities by State/Province
```sql
SELECT 
    country,
    state_province,
    COUNT(*) as university_count
FROM all_universities
WHERE state_province IS NOT NULL
GROUP BY country, state_province
ORDER BY university_count DESC
LIMIT 20;
```

### Search Universities by Name
```sql
SELECT 
    name,
    country,
    web_pages
FROM all_universities
WHERE name LIKE '%Technology%'
ORDER BY country, name;
```

### Top Countries with Website Count
```sql
SELECT 
    country,
    COUNT(*) as university_count,
    SUM(LENGTH(web_pages)) as total_web_pages
FROM all_universities
GROUP BY country
ORDER BY university_count DESC
LIMIT 10;
```

## Closing Connection
```python
con.close()
```