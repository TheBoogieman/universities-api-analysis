# Task 5: 2010 Higher Education Enrollment Analysis

## Objective
Analyze 2010 higher education enrollment data for the top 3 countries identified in Task 2.

## Methodology

### Data Source
- **API**: World Bank Open Data API
- **Indicators Used**:
  - `SE.TER.ENRR` - School enrollment, tertiary (% gross)
  - `SE.TER.ENRL` - School enrollment, tertiary (total count)
  - `SP.POP.TOTL` - Total population

### Top 3 Countries (from Task 2)
| Country        | Number of Universities |
|----------------|-------------------------|
| United States  | 2,349                   |
| Japan          | 572                     |
| India          | 474                     |

## Data Quality Notes

### Limitations
- Some 2010 data was missing for USA and Japan
- Enrollment for USA was missing for 2013, had to be calculated

### Alternative Data Sources Considered
- OECD Education Statistics
- UNESCO Institute for Statistics
- National education ministries

## Database Tables

- `enrollment_percentages` - Enrollment rates for all 3 countries (2010 preferred with 2013 as fallback year)
- `highest_enrollment_global_2010` - Enrollment data for all universities for 2010

## Insights
### ENROLLMENT PERCENTAGES
Note: Enrollment rate for USA 2013 was calculated due to missing data.

| Country        | Year | Enrollment Rate |
|----------------|------|------------------|
| United States  | 2010 | NaN              |
| United States  | 2013 | 88.73%           |
| Japan          | 2010 | NaN              |
| Japan          | 2013 | 62.84%           |
| India          | 2010 | 18.54%           |
| India          | 2013 | 24.16%           |

### COMPARISON FOR YEARS WITH COMPLETE DATA

Note: For 2010 only 2/3 countries have data, so we compared 2013

#### Task 5a - Enrollment data for top 3 countries:
| Country        | Year | Enrollment Rate | Total Enrolled |
|----------------|------|------------------|----------------|
| India          | 2010 | 18.541767        | 20,740,740     |
| India          | 2013 | 24.163833        | 28,175,140     |
| Japan          | 2010 | NaN              | 3,836,314      |
| Japan          | 2013 | 62.838188        | 3,862,749      |
| United States  | 2010 | NaN              | NaN            |
| United States  | 2013 | 88.726418        | 281,019,900    |


#### Task 5b - Top 5 countries globally (2010):
| Country   | Total Enrolled |
|-----------|----------------|
| China     | 31,046,735     |
| India     | 20,740,740     |
| Brazil    | 6,552,707      |
| Indonesia | 5,001,048      |
| Japan     | 3,836,314      |
