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
- Motor Vehicle Collisions - Vehicles (optional integration):  
  https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Vehicles/bm4k-52h4

Note: The Crashes dataset contains ~2M+ records from 2012–2025 and has missing values, duplicates, and inconsistent formatting; robust cleaning and aggregation are required.

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


5. Backend (optional)
   - using React frontend,Provide a API.JS File to connect backend with frontend

6. Frontend
   - Filter controls, search input, Generate Report button, chart area, download/export tools.

7. Deployment
   - Host on Render, Heroku, or Vercel (with API hosted separately if needed).

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
Replace the placeholders below with actual contributions before submission.

- Member A (GitHub handle: @memberA)
  - Contributions: Data ingestion, EDA, pre-integration cleaning
  - Research questions:
    1. Which borough has highest crash rate per capita?
    2. How do pedestrian crashes vary by hour?

- Member B (GitHub handle: @memberB)
  - Contributions: Integration (Persons join), aggregation, derived features
  - Research questions:
    1. Are particular contributing factors associated with fatalities?
    2. Which vehicle types are most often involved in severe crashes?

- Member C (GitHub handle: @memberC)
  - Contributions: Backend API / Dash app structure, caching, deployment
  - Research questions:
    1. Are there seasonal crash patterns?
    2. Where are spatial hotspots by street?

- Member D (GitHub handle: @memberD)
  - Contributions: Frontend visualizations, UX, search parser, README and docs
  - Research questions:
    1. How often are drivers vs pedestrians injured by borough?
    2. How do crash counts change before/after major policy changes (if data allows)?


  - All team members are in GitHub repo contributors/commit history.

