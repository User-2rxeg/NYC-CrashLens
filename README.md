# NYC CrashLens 🚗
## NYC Motor Vehicle Collisions — Interactive Data Visualization

### 🎓 Academic Information

**Institution:** The German International University  
**Faculty:** Faculty of Informatics and Computer Science  
**Course:** Data Engineering and Visualization (Winter Semester 2025)  
**Instructors:** Dr. Nada Sharaf  
**Teaching Assistants:** Mariam Ali, May Magdy, Mohamed Abdelsatar  
**Submission Date:** November 21, 2025  

---

## 📋 Project Overview

This project delivers a fully interactive web application to explore and analyze NYC motor vehicle collision data.  The system integrates both crash-level and person-level datasets from NYC Open Data, enabling users to filter, visualize, and extract insights about traffic safety patterns across New York City. 

## ⭐ Key Features

- **Multi-dimensional filtering** across time, geography, and crash characteristics
- **Natural-language search** for intuitive query building
- **Interactive dashboard** built with Plotly/Dash
- **Geographic mapping** of crash locations
- **Comprehensive metrics** at crash, person, and vehicle levels
- **KPI cards** and statistical summaries
- **CSV export** of filtered datasets

---

## 📊 Datasets

### 1. Motor Vehicle Collisions — Crashes

**Source:** [NYC Open Data (h9gi-nx95)](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95)  
**Scope:** Each row represents one crash reported by NYPD

#### Inclusion Criteria
- ≥ 1 person injured or killed, OR
- Property damage ≥ $1,000
- Requires official MV104-AN police report

#### Crash Dataset Schema

| Column | API Field | Description | Type |
|--------|-----------|-------------|------|
| `CRASH_DATE` | `crash_date` | Collision date | Timestamp |
| `CRASH_TIME` | `crash_time` | Collision time | Text |
| `BOROUGH` | `borough` | NYC borough | Text |
| `ZIP_CODE` | `zip_code` | Postal code | Text |
| `LATITUDE` | `latitude` | Geographic latitude | Float |
| `LONGITUDE` | `longitude` | Geographic longitude | Float |
| `LOCATION` | `location` | (Lat, Long) pair | Location |
| `ON_STREET_NAME` | `on_street_name` | Primary street | Text |
| `CROSS_STREET_NAME` | `cross_street_name` | Cross street | Text |
| `OFF_STREET_NAME` | `off_street_name` | Off-street address | Text |
| `NUMBER_OF_PERSONS_INJURED` | `number_of_persons_injured` | Total injured | Number |
| `NUMBER_OF_PERSONS_KILLED` | `number_of_persons_killed` | Total killed | Number |
| `NUMBER_OF_PEDESTRIANS_INJURED` | `number_of_pedestrians_injured` | Pedestrians injured | Number |
| `NUMBER_OF_PEDESTRIANS_KILLED` | `number_of_pedestrians_killed` | Pedestrians killed | Number |
| `NUMBER_OF_CYCLIST_INJURED` | `number_of_cyclist_injured` | Cyclists injured | Number |
| `NUMBER_OF_CYCLIST_KILLED` | `number_of_cyclist_killed` | Cyclists killed | Number |
| `NUMBER_OF_MOTORIST_INJURED` | `number_of_motorist_injured` | Motorists injured | Number |
| `NUMBER_OF_MOTORIST_KILLED` | `number_of_motorist_killed` | Motorists killed | Number |
| `CONTRIBUTING_FACTOR_VEHICLE_1–5` | `contributing_factor_vehicle_X` | Primary crash causes | Text |
| `COLLISION_ID` | `collision_id` | Unique crash ID | Number |
| `VEHICLE_TYPE_CODE_1–5` | `vehicle_type_code_X` | Vehicle types | Text |

### 2. Motor Vehicle Collisions — Person

**Source:** [NYC Open Data (f55k-p6yu)](https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu)  
**Scope:** Each row represents one person involved in a crash  
**Dataset Size:** ~5.83 million rows, 21 columns

#### Person Dataset Schema

| Column | Description | Type |
|--------|-------------|------|
| `UNIQUE_ID` | Unique person-level ID | Number |
| `COLLISION_ID` | Foreign key referencing crash table | Number |
| `CRASH_DATE` | Date of crash | Timestamp |
| `CRASH_TIME` | Time of crash | Text |
| `PERSON_ID` | Person identifier | Text |
| `PERSON_TYPE` | Driver/Pedestrian/Cyclist/Occupant | Text |
| `PERSON_INJURY` | Injury severity | Text |
| `VEHICLE_ID` | Vehicle reference | Text |
| `PERSON_AGE` | Age | Number |
| `EJECTION` | Ejection status | Text |
| `EMOTIONAL_STATUS` | Emotional/physical state | Text |
| `BODILY_INJURY` | Injured body region | Text |
| `POSITION_IN_VEHICLE` | Seating position | Text |
| `SAFETY_EQUIPMENT` | Airbag/seatbelt usage | Text |
| `PED_LOCATION` | Pedestrian location | Text |
| `PED_ACTION` | Pedestrian action | Text |
| `COMPLAINT` | Physical complaint | Text |
| `PED_ROLE` | Pedestrian role | Text |
| `CONTRIBUTING_FACTOR_1/2` | Crash causes | Text |
| `PERSON_SEX` | Gender | Text |

---

## 🏗️ Architecture & Pipeline

### 1. Data Ingestion
- Download datasets via NYC Open Data API
- Load into pandas DataFrames
- Log ingestion metadata

### 2. Pre-Integration Cleaning (Crash Dataset)
- Exploratory Data Analysis (EDA)
- Missing value profiling and treatment
- Outlier detection (IQR, domain rules)
- Standardize date & time formats
- Remove duplicates via `COLLISION_ID`

### 3. Integration (Crashes + Person)
- Join on `COLLISION_ID`
- Validate 1-to-many relationships
- Track unmatched rows & join-induced data loss

### 4. Post-Integration Cleaning
- Fix data type mismatches
- Handle missing values introduced by the join
- Remove redundant/inconsistent columns
- Create derived features (severity metrics, categories)

### 5. Backend (FastAPI/Flask)
- Endpoints for aggregated crash statistics
- Query filtering by borough, vehicle type, injury type, etc.
- Caching for repeated queries

### 6. Frontend (Plotly Dash)
- Multi-filter interactive dashboard
- KPI cards
- Time-series trends
- Borough comparisons
- Heatmaps and geographic maps
- Natural-language search interpretation

### 7. Deployment
- Deploy using Vercel, Render, or Heroku
- CI/CD automatic deployment workflow

---

## 🎨 Dashboard Features

### Filters
- Borough selection
- Year range
- Person type (driver, pedestrian, cyclist)
- Injury severity
- Vehicle type
- Contributing factors
- Natural-language search

### Visualizations
- **KPI Cards:** Total crashes, injuries, fatalities
- **Bar Charts:** Borough comparisons, vehicle types, contributing factors
- **Line Charts:** Yearly and monthly trends
- **Heatmap:** Day × hour crash intensity
- **Geographic Map:** Latitude/longitude clustering
- **Pie Charts:** Distribution analysis
- **Small Multiples:** (Optional) Comparative views

### Interactivity
- Dashboard updates on "Generate Report" action
- Reset filters functionality
- Live search interpretation
- CSV export capability

---

## 🔍 Natural Language Search

The parser intelligently extracts and recognizes: 

- **Boroughs:** Brooklyn, Queens, Manhattan, Bronx, Staten Island
- **Years:** 2020, 2021, 2022, etc.
- **Person Types:** pedestrian, cyclist, driver, passenger
- **Injury Keywords:** fatal, injured, killed, unharmed
- **Vehicle Types:** truck, sedan, SUV, bus, motorcycle
- **Contributing Factors:** alcohol, speeding, distracted, failure to yield

### Example Query
**Input:** "Show pedestrian crashes in Brooklyn in 2022"  
**Interpreted as:**
- Borough = Brooklyn
- Person Type = Pedestrian
- Year = 2022

---

## 📈 Research Questions

| # | Research Question | Visualization |
|---|------------------|---------------|
| **RQ1** | Which borough has the highest number of traffic crashes in the past five years? | Bar Chart (Crashes per Borough) |
| **RQ2** | Are traffic crashes increasing or decreasing over the years? | Line Chart (Year vs Number of Crashes) |
| **RQ3** | **Borough–Severity Trends:** How have total crashes, injuries, and fatalities evolved over the years in each borough, and which borough shows the fastest increase or decrease in crash severity? | Multi-line Chart |
| **RQ4** | **Vehicle Type vs Injury Severity:** Which vehicle types (e.g., sedan, SUV, bus, truck) are most associated with serious injuries and fatalities compared to property-damage-only crashes? | Stacked Bar Chart |
| **RQ5** | **Top Contributing Factors by Borough:** Are the top contributing factors (e.g., driver inattention, failure to yield, unsafe speed) the same across all boroughs, or do certain boroughs have distinct dominant risk factors? | Grouped Bar Chart / Heatmap |
| **RQ6** | **Person Type Risk Profile:** How does crash outcome differ between drivers, passengers, cyclists, and pedestrians in terms of probability of injury or fatality? | Grouped Bar Chart |
| **RQ7** | **Gender and Injury Outcomes:** After controlling for person type and borough, is there a significant difference between male and female persons in the likelihood of being uninjured, injured, or killed in a crash? | Faceted Bar Chart |
| **RQ8** | **Pedestrian & Cyclist Safety Over Time:** How have crashes involving pedestrians and cyclists changed over the years in each borough, and which boroughs show improvement vs deterioration in vulnerable road-user safety? | Multi-line Chart |
| **RQ9** | What is the relationship between vehicle type and the type of injuries (driver, pedestrian, cyclist)? | Grouped Bar Chart (Vehicle Type vs Injury Type) |
| **RQ10** | Which vehicle type is most involved in crashes across different boroughs, and does its involvement change over time? | Heatmap / Small Multiples |

---

## 👥 Team Contributions

### **Abdelmonem Sayed** (13006494)
- Pre-integration cleaning (All)



### **Ramez Mokbil** (13007430)

- Post-integration cleaning and validation
- Handling join-induced missing value


### **Seif Saad** (14004494)

- Backend 
- Deployment
- Crash–Person dataset integration (`COLLISION_ID`)


### **Eyad Ahmed** (13005238)

- Data ingestion and retrieval
- Exploratory Data Analysis (EDA)
- Research questions implementation & Formulation
- README structuring and documentation


### **Ahmed Amr** (13007323)

- Frontend visualization refinement (charts, KPIs, layout)
- Frontend dashboard and visual components



- Interactive visualizations (Plotly)
---

## 🚀 Getting Started

### Prerequisites
```bash
python >= 3.8
pandas
plotly
dash
fastapi or flask
```

### Installation
```bash
# Clone the repository
git clone https://github.com/User-2rxeg/NYC-CrashLens.git

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### Access the Dashboard
Navigate to `http://localhost:8050` in your web browser

---

## 📝 License

This project is developed as part of academic coursework at The German International University. 

---

## 🙏 Acknowledgments

- NYC Open Data for providing comprehensive collision datasets
- Course instructors and TAs for guidance and support
- The German International University for academic resources
