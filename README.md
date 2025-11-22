# NYC Motor Vehicle Collisions — Interactive Data Visualization

**Project:** Data Engineering & Visualization — Milestone 1  
**Course:** Data Engineering and Visualization (Winter Semester 2025)  
**Instructors / TAs:** Dr. Nada Sharaf, Mariam Ali (TA), May Magdy (TA), Mohamed Abdelsatar (TA)  
**Submission Date:** 2025-11-21

---

## 📋 Project Overview

This project builds a fully interactive web application to explore and report on NYC motor vehicle collision data. The application integrates crash and person-level data from NYC Open Data, enabling users to filter, analyze, and visualize traffic safety patterns by borough, time period, vehicle type, contributing factors, and injury severity.

**Key Capabilities:**
- Multi-dimensional filtering and natural language search
- Interactive visualizations (heatmaps, line charts, bar charts, geographic maps)
- Dynamic report generation with KPI metrics
- Data export functionality (CSV)

---

## 📊 Datasets and Sources

### Primary Datasets (NYC Open Data)

#### 1. Motor Vehicle Collisions - Crashes (Main Dataset)
- **Source:** [NYC Open Data - Motor Vehicle Collisions - Crashes](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95)
- **Description:** Detailed information about motor vehicle crash events reported by the NYPD
- **Record Definition:** Each row represents a single crash event
- **Inclusion Criteria:** Collisions where at least one person was injured/killed OR property damage ≥ $1,000
- **Documentation:** Requires formal MV104-AN police report

**Crash Dataset Schema (29 Columns)**

| Column Name | API Field Name | Description | Data Type |
|---|---|---|---|
| CRASH_DATE | crash_date | Date of collision | Floating Timestamp |
| CRASH_TIME | crash_time | Time of collision | Text |
| BOROUGH | borough | NYC borough where crash occurred | Text |
| ZIP_CODE | zip_code | Postal code of the crash location | Text |
| LATITUDE | latitude | Geographic latitude (EPSG 4326) | Number |
| LONGITUDE | longitude | Geographic longitude (EPSG 4326) | Number |
| LOCATION | location | Coordinate pair | Location |
| ON_STREET_NAME | on_street_name | Street where collision occurred | Text |
| CROSS_STREET_NAME | cross_street_name | Nearest cross street | Text |
| OFF_STREET_NAME | off_street_name | Street address if known | Text |
| NUMBER_OF_PERSONS_INJURED | number_of_persons_injured | Total injured | Number |
| NUMBER_OF_PERSONS_KILLED | number_of_persons_killed | Total killed | Number |
| NUMBER_OF_PEDESTRIANS_INJURED | number_of_pedestrians_injured | Pedestrians injured | Number |
| NUMBER_OF_PEDESTRIANS_KILLED | number_of_pedestrians_killed | Pedestrians killed | Number |
| NUMBER_OF_CYCLIST_INJURED | number_of_cyclist_injured | Cyclists injured | Number |
| NUMBER_OF_CYCLIST_KILLED | number_of_cyclist_killed | Cyclists killed | Number |
| NUMBER_OF_MOTORIST_INJURED | number_of_motorist_injured | Vehicle occupants injured | Number |
| NUMBER_OF_MOTORIST_KILLED | number_of_motorist_killed | Vehicle occupants killed | Number |
| CONTRIBUTING_FACTOR_VEHICLE_1 | contributing_factor_vehicle_1 | Primary cause for vehicle 1 | Text |
| CONTRIBUTING_FACTOR_VEHICLE_2 | contributing_factor_vehicle_2 | Primary cause for vehicle 2 | Text |
| CONTRIBUTING_FACTOR_VEHICLE_3 | contributing_factor_vehicle_3 | Primary cause for vehicle 3 | Text |
| CONTRIBUTING_FACTOR_VEHICLE_4 | contributing_factor_vehicle_4 | Primary cause for vehicle 4 | Text |
| CONTRIBUTING_FACTOR_VEHICLE_5 | contributing_factor_vehicle_5 | Primary cause for vehicle 5 | Text |
| COLLISION_ID | collision_id | Unique crash identifier (Primary Key) | Number |
| VEHICLE_TYPE_CODE_1 | vehicle_type_code1 | Vehicle type (car, bicycle, truck, etc.) | Text |
| VEHICLE_TYPE_CODE_2 | vehicle_type_code2 | Vehicle type #2 | Text |
| VEHICLE_TYPE_CODE_3 | vehicle_type_code_3 | Vehicle type #3 | Text |
| VEHICLE_TYPE_CODE_4 | vehicle_type_code_4 | Vehicle type #4 | Text |
| VEHICLE_TYPE_CODE_5 | vehicle_type_code_5 | Vehicle type #5 | Text |

#### 2. Motor Vehicle Collisions - Person (Integration Dataset)
- **Source:** [NYC Open Data - Motor Vehicle Collisions - Person](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu)
- **Description:** Individual-level data for all persons involved in crashes (drivers, passengers, pedestrians, cyclists)
- **Record Definition:** Each row represents one person involved in a crash
- **Size:** ~5.83 million rows
- **Columns:** 21

**Person Dataset Schema (21 Columns)**

| Column Name | API Field Name | Description | Data Type |
|---|---|---|---|
| UNIQUE_ID | unique_id | Unique record code for each person (Primary Key) | Number |
| COLLISION_ID | collision_id | Crash ID, matches the crash table (Foreign Key) | Number |
| CRASH_DATE | crash_date | Date of the collision | Floating Timestamp |
| CRASH_TIME | crash_time | Time of the collision | Text |
| PERSON_ID | person_id | System-assigned ID for the person | Text |
| PERSON_TYPE | person_type | Bicyclist, Occupant, Pedestrian, etc. | Text |
| PERSON_INJURY | person_injury | Injured, killed, unspecified | Text |
| VEHICLE_ID | vehicle_id | Vehicle linked to this person (Foreign Key) | Text |
| PERSON_AGE | person_age | Age based on date of birth | Number |
| EJECTION | ejection | Ejection status (none, partial, fully ejected) | Text |
| EMOTIONAL_STATUS | emotional_status | Apparent condition (death, unconscious, etc.) | Text |
| BODILY_INJURY | bodily_injury | Injured body part (head, face, neck, etc.) | Text |
| POSITION_IN_VEHICLE | position_in_vehicle | Seating position (#1-8) | Text |
| SAFETY_EQUIPMENT | safety_equipment | Equipment used (seat belt, airbag, etc.) | Text |
| PED_LOCATION | ped_location | Pedestrian location (intersection, non-intersection) | Text |
| PED_ACTION | ped_action | Pedestrian action (walking with/against signal, etc.) | Text |
| COMPLAINT | complaint | Type of physical complaint | Text |
| PED_ROLE | ped_role | Role (pedestrian, witness, skater, etc.) | Text |
| CONTRIBUTING_FACTOR_1 | contributing_factor_1 | Primary crash cause associated with the person | Text |
| CONTRIBUTING_FACTOR_2 | contributing_factor_2 | Secondary crash cause | Text |
| PERSON_SEX | person_sex | Gender of the person | Text |

---

## 🏗️ Architecture & Technical Components

### Data Pipeline (ETL)

1. **Data Ingestion**
   - Fetch datasets from NYC Open Data URLs via API
   - Load into pandas DataFrames for processing
   - Document data retrieval metadata and timestamps

2. **Pre-Integration Cleaning (Crashes Dataset)**
   - **Exploratory Data Analysis (EDA):** Descriptive statistics, distributions, missing value patterns, outlier detection
   - **Missing Value Handling:** Justify drop vs. impute decisions based on column semantics
   - **Outlier Detection & Treatment:** Use IQR, domain knowledge, and statistical methods
   - **Format Standardization:** Harmonize date formats, string cases, and categorical values
   - **Duplicate Removal:** Identify and remove exact duplicates by COLLISION_ID

3. **Integration (Crashes + Person join)**
   - Join Person dataset with Crashes dataset on COLLISION_ID
   - Validate join cardinality and data integrity
   - Document join strategy and any data loss

4. **Post-Integration Cleaning**
   - Resolve new missing values introduced by joins
   - Remove redundant or inconsistent columns
   - Fix data type mismatches
   - Create derived features (e.g., crash severity score)

5. **Backend (API & Aggregation)**
   - Build REST API endpoints for filtered queries
   - Implement caching for common aggregations
   - Support dynamic aggregation by borough, year, vehicle type, injury type, etc.

6. **Frontend (Visualization & UX)**
   - Interactive dashboard with Plotly/Dash or similar framework
   - Multi-select dropdown filters
   - Natural language search parser
   - Dynamic report generation on button click

7. **Deployment**
   - Host on Render, Heroku, or Vercel
   - Ensure CI/CD pipeline for testing and updates

---

## 🎨 Website Features & User Experience

### Controls & Filters

- **Multi-select Dropdowns:**
  - Borough (Manhattan, Brooklyn, Queens, Bronx, Staten Island)
  - Year (full range of data)
  - Vehicle Type (sedan, SUV, bus, truck, bicycle, motorcycle, etc.)
  - Contributing Factor (speeding, distracted, alcohol, failure to yield, etc.)
  - Injury Type (uninjured, injured, killed)
  - Person Type (driver, passenger, pedestrian, cyclist)

- **Search Input:** Free-text natural language query
- **Generate Report Button:** Central control to apply filters and update all visualizations
- **Reset Filters Button:** Clear all selections
- **Download/Export:** CSV export of filtered dataset sample

### Interactive Visualizations

- **KPI Cards:** 
  - Total matched records
  - Total injuries
  - Total fatalities
  
- **Bar Charts:**
  - Crashes by Borough (top-N)
  - Crashes by Vehicle Type
  - Crashes by Contributing Factor

- **Line Charts:**
  - Crashes over time (monthly/weekly) with zoom and pan
  - Trends by borough

- **Heatmap:**
  - Day-of-week × Hour-of-day crash intensity

- **Geographic Map:**
  - Sampled scatter plot or clustered points (latitude/longitude)
  - Interactive tooltips with crash details

- **Pie Charts:**
  - Injury type distribution
  - Person type distribution

- **Optional Advanced Visualizations:**
  - Stacked bar charts
  - Treemaps
  - Small multiples by borough

### Interactivity Behavior

- Dashboard is non-reactive until user clicks "Generate Report"
- Generate Report applies all active dropdown filters and/or parsed search filters
- All charts are requested and updated in a single API call
- Charts feature hover tooltips, zoom capabilities, and optional cross-filtering
- Clear loading indicators displayed while reports are generated

---

## 🔍 Search Parsing Behavior

### Natural Language Search Parser

The search mode maps natural-language queries into concrete filter selections. A keyword and pattern-based parser detects:

- **Borough Names:** "Brooklyn", "Queens", "Manhattan", "Bronx", "Staten Island"
- **Years:** 4-digit patterns (e.g., 2022)
- **Person Types:** "pedestrian", "cyclist", "driver", "passenger"
- **Injury Keywords:** "injured", "killed", "severe", "fatal", "uninjured"
- **Vehicle Types:** "taxi", "bus", "motorcycle", "truck", "sedan", "SUV"
- **Contributing Factors:** "speeding", "distracted", "alcohol", "failure to yield", "reckless"

### Search UX

- When "Generate Report" is clicked with an active search query, the app displays an **interpretation preview**  
  *(Example: "Interpreted: Borough=Brooklyn, Year=2022, PersonType=Pedestrian")*
- User-selected dropdowns take precedence over parsed search results when both exist
- Invalid or unrecognized terms are noted and ignored gracefully

---

## 📈 Research Questions

| # | Research Question | Visualization(s) |
|---|---|---|
| **RQ1** | Which borough has the highest number of traffic crashes in the past five years? | Bar Chart (Crashes per Borough) |
| **RQ2** | Are traffic crashes increasing or decreasing over the years? | Line Chart (Year vs. Number of Crashes) |
| **RQ3** | How have total crashes, injuries, and fatalities evolved over the years in each borough, and which borough shows the fastest increase or decrease in crash severity? | Multi-line chart (Borough Trends) |
| **RQ4** | Which vehicle types (sedan, SUV, bus, truck) are most associated with serious injuries and fatalities compared to property-damage-only crashes? | Grouped/Stacked Bar Chart |
| **RQ5** | Are the top contributing factors the same across all boroughs, or do certain boroughs have distinct dominant risk factors? | Heatmap or Grouped Bar Chart |
| **RQ6** | How does crash outcome differ between drivers, passengers, cyclists, and pedestrians in terms of probability of injury or fatality? | Grouped Bar Chart (Person Type vs. Injury Severity) |
| **RQ7** | After controlling for person type and borough, is there a significant difference between male and female persons in injury likelihood? | Faceted Bar Charts by Person Type |
| **RQ8** | How have crashes involving pedestrians and cyclists changed over the years in each borough? | Multi-line Chart (Vulnerable Road User Trends) |
| **RQ9** | What is the relationship between vehicle type and the type of injuries (driver, pedestrian, cyclist)? | Grouped Bar Chart (Vehicle Type × Injury Type) |
| **RQ10** | Which vehicle type is most involved in crashes across different boroughs, and does its involvement change over time? | Heatmap or Small Multiples |

---

## 📦 Deliverables Included in This Repository

- **Data Processing Notebooks:** EDA, cleaning, and integration code (Jupyter)
- **Backend API:** Flask/FastAPI application with endpoints for filtered queries
- **Frontend Application:** Dash/Plotly dashboard with interactive controls and visualizations
- **Data Documentation:** Schema descriptions, data quality reports, integration justifications
- **Deployment Configuration:** Environment files, Docker configuration, hosting setup
- **README & Project Documentation:** This file and supplementary docs

---

## 👥 Team Contributions

### Abdelomonem Sayed (13006494)
- **Contributions:** Data ingestion, EDA, pre-integration cleaning
- **Research Questions:**
  1. Which borough has the highest crash rate per capita?
  2. How do pedestrian crashes vary by hour of day?

### Ramez Mokbil (1300[X])
- **Contributions:** Integration (Persons join), aggregation, derived feature engineering
- **Research Questions:**
  1. [To be completed]
  2. [To be completed]

### Seif Saad (1300[X])
- **Contributions:** Backend API structure, data caching, deployment and DevOps
- **Research Questions:**
  1. [To be completed]
  2. [To be completed]

### Eyad Ahmed (13005238)
- **Contributions:** Frontend visualizations, UX design, search parser implementation, README and documentation
- **Research Questions:**
  1. [To be completed]
  2. [To be completed]

**Note:** All team members appear in the repository commit history and contributor list.

---

## ✅ Quality Standards

This project adheres to the following quality benchmarks:

- ✅ **Thorough Exploratory Data Analysis (EDA)** with relevant statistics and visualizations
- ✅ **Effective Pre- and Post-Integration Cleaning** with proper handling of missing values, outliers, and inconsistencies
- ✅ **High-Quality Integration** with clear joins, justified data sources, and demonstrable added value
- ✅ **Descriptive Markdown Documentation** explaining exploration, cleaning, and integration steps
- ✅ **Justified Decision Making** with discussion of alternatives and insights
- ✅ **Complete Contributor History** with all team members represented in commits

---

## 🚀 Getting Started (Future Implementation)

```bash
# Clone repository
git clone https://github.com/User-2rxeg/NYC-CrashLens.git
cd NYC-CrashLens

# Install dependencies
pip install -r requirements.txt

# Run data pipeline
python scripts/etl_pipeline.py

# Start backend API
python app.py

# Access dashboard
# Dashboard will be available at http://localhost:8050
