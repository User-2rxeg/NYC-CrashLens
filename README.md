# NYC Motor Vehicle Collisions — Interactive Data Visualization

Project: Data Engineering & Visualization — Milestone 1  
Course: Data Engineering and Visualization (Winter Semester 2025)  
Instructors / TAs: Dr. Nada Sharaf, Mariam Ali (TA), May Magdy (TA), Mohamed Abdelsatar (TA)  
Submission Date: 2025-11-21


Project overview
----------------
This project builds a fully interactive web application to explore and report on NYC motor vehicle collision data (Crashes + Person or Vehicles). The site allows users to filter by Borough, Year, Vehicle Type, Contributing Factor, Injury Type, or use a natural-language search to auto-apply filters. A central "Generate Report" button updates all visualizations at once. Visualizations include bar charts, time series, heatmap (day vs hour), map, and pie charts — all interactive.

Datasets and sources
--------------------
Primary datasets (NYC Open Data):
- Motor Vehicle Collisions - Crashes (primary):  
  https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95
- Motor Vehicle Collisions - Person (for integration):  
  https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu

🚗 Motor Vehicle Collisions – Person Dataset (NYC)
📌 Overview

Rows: 5.83M

Columns: 21

Each row represents a person involved in a crash (driver, passenger, pedestrian, cyclist, etc.)

This dataset is part of NYC’s public safety records and contains detailed information about individuals involved in traffic collisions.

📊 Data Schema (21 Columns)
Column Name	API Field Name	Description	Data Type
UNIQUE_ID	unique_id	Unique record code for each person (Primary Key)	Number
COLLISION_ID	collision_id	Crash ID, matches the crash table (Foreign Key)	Number
CRASH_DATE	crash_date	Date of the collision	Floating Timestamp
CRASH_TIME	crash_time	Time of the collision	Text
PERSON_ID	person_id	System-assigned ID for the person	Text
PERSON_TYPE	person_type	Bicyclist, Occupant, Pedestrian, etc.	Text
PERSON_INJURY	person_injury	Injured, killed, unspecified	Text
VEHICLE_ID	vehicle_id	Vehicle linked to this person (Foreign Key)	Text
PERSON_AGE	person_age	Age based on date of birth	Number
EJECTION	ejection	Ejection status (none, partial, fully ejected)	Text
EMOTIONAL_STATUS	emotional_status	Apparent condition (death, unconscious, etc.)	Text
BODILY_INJURY	bodily_injury	Injured body part (head, face, neck, etc.)	Text
POSITION_IN_VEHICLE	position_in_vehicle	Seating position (#1-8)	Text
SAFETY_EQUIPMENT	safety_equipment	Equipment used (seat belt, airbag, etc.)	Text
PED_LOCATION	ped_location	Pedestrian location (intersection, non-intersection)	Text
PED_ACTION	ped_action	Pedestrian action (walking with/against signal, etc.)	Text
COMPLAINT	complaint	Type of physical complaint	Text
PED_ROLE	ped_role	Role (pedestrian, witness, skater, etc.)	Text
CONTRIBUTING_FACTOR_1	contributing_factor_1	Primary crash cause associated with the person	Text
CONTRIBUTING_FACTOR_2	contributing_factor_2	Secondary crash cause	Text
PERSON_SEX	person_sex	Gender of the person	Text


Motor Vehicle Collisions – Crashes (NYC)
📌 Overview

This dataset contains detailed information about motor vehicle crash events reported by the NYPD.
Each row represents a single crash, not individuals or vehicles.

The dataset includes all police-reported collisions where:

At least one person is injured or killed, or

Property damage is $1000+

👉 These collisions require a formal MV104-AN police report.



📊 Crash Dataset Schema (29 Columns)
Column Name	API Field Name	Description	Data Type
CRASH DATE	crash_date	Date of collision	Floating Timestamp
CRASH TIME	crash_time	Time of collision	Text
BOROUGH	borough	NYC borough where crash occurred	Text
ZIP CODE	zip_code	Postal code of the crash location	Text
LATITUDE	latitude	Geographic latitude (EPSG 4326)	Number
LONGITUDE	longitude	Geographic longitude (EPSG 4326)	Number
LOCATION	location	Coordinate pair	Location
ON STREET NAME	on_street_name	Street where collision occurred	Text
CROSS STREET NAME	off_street_name	Nearest cross street	Text
OFF STREET NAME	cross_street_name	Street address if known	Text
NUMBER OF PERSONS INJURED	number_of_persons_injured	Total injured	Number
NUMBER OF PERSONS KILLED	number_of_persons_killed	Total killed	Number
NUMBER OF PEDESTRIANS INJURED	number_of_pedestrians_injured	Pedestrians injured	Number
NUMBER OF PEDESTRIANS KILLED	number_of_pedestrians_killed	Pedestrians killed	Number
NUMBER OF CYCLIST INJURED	number_of_cyclist_injured	Cyclists injured	Number
NUMBER OF CYCLIST KILLED	number_of_cyclist_killed	Cyclists killed	Number
NUMBER OF MOTORIST INJURED	number_of_motorist_injured	Vehicle occupants injured	Number
NUMBER OF MOTORIST KILLED	number_of_motorist_killed	Vehicle occupants killed	Number
CONTRIBUTING FACTOR VEHICLE 1	contributing_factor_vehicle_1	Primary cause for vehicle 1	Text
CONTRIBUTING FACTOR VEHICLE 2	contributing_factor_vehicle_2	Primary cause for vehicle 2	Text
CONTRIBUTING FACTOR VEHICLE 3	contributing_factor_vehicle_3	Primary cause for vehicle 3	Text
CONTRIBUTING FACTOR VEHICLE 4	contributing_factor_vehicle_4	Primary cause for vehicle 4	Text
CONTRIBUTING FACTOR VEHICLE 5	contributing_factor_vehicle_5	Primary cause for vehicle 5	Text
COLLISION_ID	collision_id	Unique crash identifier	Number
VEHICLE TYPE CODE 1	vehicle_type_code1	Vehicle type (car, bicycle, truck, etc.)	Text
VEHICLE TYPE CODE 2	vehicle_type_code2	Vehicle type #2	Text
VEHICLE TYPE CODE 3	vehicle_type_code_3	Vehicle type #3	Text
VEHICLE TYPE CODE 4	vehicle_type_code_4	Vehicle type #4	Text
VEHICLE TYPE CODE 5	vehicle_type_code_5	Vehicle type #5	Text

Architecture & components (non-code)
------------------------------------
Logical layers:

1. Data ingestion
   - Read Dataset from its Link/URL.

2. Pre-integration cleaning (ETL)

• Explore the Data: Use descriptive statistics and initial plots to understand the datasets structure,issues, and patterns.:

• Pre-Integration Cleaing:

– Handle missing values (justify drop vs. impute).
– Detect and address outliers (e.g., IQR, domain rules).
– Standardize formats (dates, strings, categories).
– Remove duplicates.

4. Integration
• Integrate Additional Data: Join with related NYC Open Data table (Person via COLLISION_ID). Document integration steps and justify choices.

• Post-Integration Cleaning (Required): After joining, resolve:

– New missing values from joins.
– Inconsistent or redundant columns.
– Data type mismatches.



6. Frontend

- Multiple dropdown filters (e.g., Borough, Year, Vehicle Type, Contributing Factor, Injury Type) allowing users to dynamically filter data.

– A search mode, where users can type queries (e.g., “Brooklyn 2022 pedestrian crashes”) that automatically apply filters.

– A central “Generate Report” button that, when clicked, dynamically updates all visualizations based on selected filters or search terms.

– Visualizations should include a variety of chart types, such as bar charts, line charts, heatmaps, maps, or pie charts, and must offer interactivity (hover, zoom, or filter updates).

7. Deployment
   - Hosted on Render, Heroku, or Vercel.

Data cleaning & integration summary (what will be done)
-------------------------------------------------------


Website features & UX
---------------------
Controls:
- Multi-select dropdowns:
  - Borough, Year, Vehicle Type, Contributing Factor, Injury Type
- Search input (free-text)
- Generate Report button (central control)
- Reset filters button
- Download / export filtered dataset sample (CSV)

Visualizations (interactive):
- KPI cards: matched records, total injuries, fatalities
- Bar chart: crashes by Borough (top-N)
- Line chart: crashes over time (monthly or weekly) with zoom/pan
- Heatmap: day-of-week × hour-of-day intensity
- Map: sampled scatter or clustered points (lat/lon) with tooltips
- Pie chart: injury type distribution
- Optional: stacked bars, treemap, small multiples

Interactivity behavior:
- Nothing updates until the user clicks "Generate Report".
- Generate Report applies dropdown filters and/or parsed search filters and requests aggregated data for all charts in a single request.
- Charts include hover tooltips and zoom. Clicking a chart element could optionally filter other charts (advanced).
- The app shows clear loading indicators while reports are being generated.

Search parsing behavior
-----------------------
Search mode maps natural-language queries into concrete filter selections. For Milestone 1 a robust keyword & pattern-based parser will be implemented:
- Detect borough names (e.g., "Brooklyn", "Queens").
- Detect 4-digit years (e.g., 2022).
- Detect person types: pedestrian, cyclist, driver.
- Detect injury keywords: injured, killed, severe, fatal.
- Detect vehicle type keywords: taxi, bus, motorcycle, truck.
- Detect contributing factors keywords: speeding, distracted, alcohol, failure to yield.

UX for search:
- When Generate Report is clicked and a search query exists, the app shows an interpretation preview (e.g., "Interpreted: Borough=Brooklyn, Year=2022, PersonType=Pedestrian") and then applies filters.
- User-selected dropdowns take precedence over parsed results when both exist.



Deliverables included in this repository
---------------------------------------


Team contributions (template)
-----------------------------


- Abdelomonem Sayed (13006494)

  - Contributions: Data ingestion, EDA, pre-integration cleaning

  - Research questions:
  
    1. Which borough has highest crash rate per capita?
    2. How do pedestrian crashes vary by hour?

- Ramez Mokbil (1300)

  - Contributions: Integration (Persons join), aggregation, derived features

  - Research questions:

    1. 
    2. 

- Seif Saad (1300)

  - Contributions: Backend API / Dash app structure, caching, deployment

  - Research questions:
    1. 
    2. 

- Eyad Ahmed (13005238)

- Contributions: Frontend visualizations, UX, search parser, README and docs

- Research questions:
    1. 
    2. 


RQ1 — Which borough has the highest number of traffic crashes in the past five years?

Visualization: Bar Chart (Crashes per Borough)

RQ2 — Are traffic crashes increasing or decreasing over the years?

Visualization: Line Chart (Year vs Number of Crashes)

RQ3 - Borough–Severity Trends

How have total crashes, injuries, and fatalities evolved over the years in each borough, and which borough shows the fastest increase or decrease in crash severity?

RQ4 - Vehicle Type vs Injury Severity

Which vehicle types (e.g., sedan, SUV, bus, truck) are most associated with serious injuries and fatalities compared to property-damage-only crashes?

RQ5 - Top Contributing Factors by Borough

Are the top contributing factors (e.g., driver inattention, failure to yield, unsafe speed) the same across all boroughs, or do certain boroughs have distinct dominant risk factors?

RQ6 - Person Type Risk Profile

How does crash outcome differ between drivers, passengers, cyclists, and pedestrians in terms of probability of injury or fatality?

RQ7 - Gender and Injury Outcomes

After controlling for person type and borough, is there a significant difference between male and female persons in the likelihood of being uninjured, injured, or killed in a crash?

RQ8 - Pedestrian & Cyclist Safety Over Time

How have crashes involving pedestrians and cyclists changed over the years in each borough, and which boroughs show improvement vs deterioration in vulnerable road-user safety?

RQ9 — What is the relationship between vehicle type and the type of injuries (driver, pedestrian, cyclist)?

Visualization: Grouped Bar Chart (Vehicle Type vs Injury Type)

RQ10 - Which vehicle type is most involved in crashes across different boroughs, and does its involvement change over time?

Visualization:

– Thorough exploratory data analysis (EDA) with relevant statistics and visualizations.


– Effective pre- and post-integration cleaning (e.g., appropriate handling of missing values,
outliers, and inconsistencies).

– Quality of integration: clear joins, justified data sources, and added value.

• Descriptive Markdown Cells: Document exploration, cleaning, and integration steps. Justify
decisions (e.g., why drop vs. impute nulls?), discuss alternatives considered, and explain how insights
were reached.:


  - All team members are in GitHub repo contributors/commit history.

