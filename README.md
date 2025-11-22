The German International University
Faculty of Informatics and Computer Science

🚗 NYC Motor Vehicle Collisions — Interactive Data Visualization

Milestone 1 — Data Engineering & Visualization

Course: Data Engineering and Visualization (Winter Semester 2025)
Instructors / TAs: Dr. Nada Sharaf, Mariam Ali (TA), May Magdy (TA), Mohamed Abdelsatar (TA)
Submission Date: November 21, 2025

📋 Project Overview

This project delivers a fully interactive web application to explore and analyze NYC motor vehicle collision data. The system integrates both crash-level and person-level datasets from NYC Open Data, enabling users to filter, visualize, and extract insights about traffic safety patterns across New York City.

⭐ Key Features

Multi-dimensional filtering

Natural-language search

Interactive dashboard (Plotly / Dash)

Geographic mapping

Crash, person, and vehicle-level metrics

KPI cards and statistical summaries

CSV export of filtered datasets

📊 Datasets
1. Motor Vehicle Collisions — Crashes

Source: NYC Open Data (h9gi-nx95)
Each row = one crash reported by NYPD.

Inclusion Criteria

≥ 1 person injured or killed, OR

Property damage ≥ $1,000

Requires official MV104-AN police report

Crash Dataset Schema
Column	API Field	Description	Type
CRASH_DATE	crash_date	Collision date	Timestamp
CRASH_TIME	crash_time	Collision time	Text
BOROUGH	borough	NYC borough	Text
ZIP_CODE	zip_code	Postal code	Text
LATITUDE	latitude	Geographic latitude	Float
LONGITUDE	longitude	Geographic longitude	Float
LOCATION	location	(Lat, Long) pair	Location
ON_STREET_NAME	on_street_name	Primary street	Text
CROSS_STREET_NAME	cross_street_name	Cross street	Text
OFF_STREET_NAME	off_street_name	Off-street address	Text
NUMBER_OF_PERSONS_INJURED	number_of_persons_injured	Total injured	Number
NUMBER_OF_PERSONS_KILLED	number_of_persons_killed	Total killed	Number
NUMBER_OF_PEDESTRIANS_INJURED	number_of_pedestrians_injured	Pedestrians injured	Number
NUMBER_OF_PEDESTRIANS_KILLED	number_of_pedestrians_killed	Pedestrians killed	Number
NUMBER_OF_CYCLIST_INJURED	number_of_cyclist_injured	Cyclists injured	Number
NUMBER_OF_CYCLIST_KILLED	number_of_cyclist_killed	Cyclists killed	Number
NUMBER_OF_MOTORIST_INJURED	number_of_motorist_injured	Motorists injured	Number
NUMBER_OF_MOTORIST_KILLED	number_of_motorist_killed	Motorists killed	Number
CONTRIBUTING_FACTOR_VEHICLE_1–5	contributing_factor_vehicle_X	Primary crash causes	Text
COLLISION_ID	collision_id	Unique crash ID	Number
VEHICLE_TYPE_CODE_1–5	vehicle_type_code_X	Vehicle types	Text
2. Motor Vehicle Collisions — Person

Source: NYC Open Data (f55k-p6yu)
Each row = one person involved in a crash (driver, cyclist, pedestrian, passenger)

Dataset Info

Size: ~5.83 million rows

Columns: 21

Person Dataset Schema
Column	Description	Type
UNIQUE_ID	Unique person-level ID	Number
COLLISION_ID	Foreign key referencing crash table	Number
CRASH_DATE	Date of crash	Timestamp
CRASH_TIME	Time of crash	Text
PERSON_ID	Person identifier	Text
PERSON_TYPE	Driver / Pedestrian / Cyclist / Occupant	Text
PERSON_INJURY	Injury severity	Text
VEHICLE_ID	Vehicle reference	Text
PERSON_AGE	Age	Number
EJECTION	Ejection status	Text
EMOTIONAL_STATUS	Emotional/physical state	Text
BODILY_INJURY	Injured body region	Text
POSITION_IN_VEHICLE	Seating position	Text
SAFETY_EQUIPMENT	Airbag/seatbelt usage	Text
PED_LOCATION	Pedestrian location	Text
PED_ACTION	Pedestrian action	Text
COMPLAINT	Physical complaint	Text
PED_ROLE	Pedestrian role	Text
CONTRIBUTING_FACTOR_1/2	Crash causes	Text
PERSON_SEX	Gender	Text
🏗 Architecture & Pipeline
1. Data Ingestion

Download datasets via NYC Open Data API

Load into pandas

Log ingestion metadata

2. Pre-Integration Cleaning (Crash Dataset)

Exploratory Data Analysis (EDA)

Missing value profiling and treatment

Outlier detection (IQR, domain rules)

Standardize date & time formats

Remove duplicates via COLLISION_ID

3. Integration (Crashes + Person)

Join on COLLISION_ID

Validate 1-to-many relationships

Track unmatched rows & join-induced data loss

4. Post-Integration Cleaning

Fix data type mismatches

Handle missing values introduced by the join

Remove redundant/inconsistent columns

Create derived features (severity metrics, categories)

5. Backend (FastAPI / Flask)

Endpoints for aggregated crash statistics

Query filtering by borough, vehicle type, injury type, etc.

Caching for repeated queries

6. Frontend (Plotly Dash)

Multi-filter interactive dashboard

KPI cards

Time-series trends

Borough comparisons

Heatmaps and geographic maps

Natural-language search interpretation

7. Deployment

Deploy using Vercel, Render, or Heroku

CI/CD automatic deployment workflow

🎨 Dashboard Features
Filters

Borough

Year

Person Type

Injury Type

Vehicle Type

Contributing Factor

Natural-language search

Visualizations

KPI Cards (total crashes, injuries, fatalities)

Bar Charts (borough, vehicle type, contributing factors)

Line Charts (yearly and monthly trends)

Heatmap (day × hour intensity)

Geographic Map (lat/long cluster)

Pie charts

Optional small multiples

Interactivity

Dashboard updates only on Generate Report

Reset filters

Live search interpretation

CSV export

🔍 Natural Language Search

The parser intelligently extracts:

Recognizes

Boroughs: Brooklyn, Queens, Manhattan…

Years: 2020, 2021…

Person types: pedestrian, cyclist, driver…

Injury keywords: fatal, injured, killed…

Vehicle types: truck, sedan, SUV…

Contributing factors: alcohol, speeding, distracted…

Example Input

"Show pedestrian crashes in Brooklyn in 2022"
Interpreted as:

Borough = Brooklyn

Person Type = Pedestrian

Year = 2022

📈 Research Questions
#	Research Question	Visualization
RQ1	Which borough has the highest number of crashes in the past 5 years?	Bar Chart
RQ2	Are crashes increasing or decreasing over time?	Line Chart
RQ3	Evolution of crashes, injuries, and fatalities by borough	Multi-line Chart
RQ4	Which vehicle types are most linked to severe injuries/fatalities?	Stacked Bar
RQ5	Do contributing factors vary significantly across boroughs?	Grouped Bar / Heatmap
RQ6	Injury likelihood by person type	Grouped Bar
RQ7	Gender vs injury likelihood (controlled by person type & borough)	Faceted Bar
RQ8	Pedestrian and cyclist crash trends over time	Multi-line Chart
RQ9	Relationship between vehicle type & injury type	Grouped Bar
RQ10	Vehicle type involvement across boroughs over time	Heatmap / Small Multiples

👥 Team Contributions
Abdelmonem Sayed (13006494)

Data ingestion and retrieval

Exploratory Data Analysis (EDA)

Pre-integration cleaning

Research questions:

Borough crash rate per capita

Pedestrian crashes by hour of day

Ramez Mokbil

Crash–Person dataset integration (COLLISION_ID)

Derived feature engineering

Aggregation logic for backend analytics

Data integrity checks

Seif Saad

Backend API architecture (FastAPI/Flask)

Caching layer for performance

Deployment & CI/CD setup

Eyad Ahmed (13005238)

Frontend dashboard and visual components

Interactive visualizations (Plotly)

Natural-language search parser

Project documentation and README writing

Ahmed Amr

Frontend visualization refinement (charts, KPIs, layout)

Research question formulation

README structuring and documentation

Post-integration cleaning and validation

Handling join-induced missing values

Resolving redundant or inconsistent columns after integration
