# NYC Motor Vehicle Collisions — Interactive Data Visualization

Project: Data Engineering & Visualization — Milestone 1  
Course: Data Engineering and Visualization (Winter Semester 2025)  
Instructors / TAs: Dr. Nada Sharaf, Mariam Ali (TA), May Magdy (TA), Mohamed Abdelsatar (TA)  
Submission Date: 2025-11-21

---

Table of contents
- Project overview
- Datasets and sources
- Goals & research questions
- Architecture & components (non-code)
- Data cleaning & integration summary
- Website features & UX
- Search parsing behavior
- How to run locally (setup & commands)
- Deployment instructions (Render / Heroku / Vercel notes)
- Performance & scaling recommendations
- Testing & validation checklist
- Deliverables included in repo
- Team contributions (template)
- Acceptance criteria & grading checklist
- Known limitations & future work
- License & contact

---

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

Goals & research questions
--------------------------
Primary goal:
- Clean and integrate Crashes with Persons (and optionally Vehicles), then provide an interactive website enabling dynamic exploration and reporting.

Each team member must propose at least 2 research questions. Example research questions (pick / adapt):
- Which borough has the highest crash rate per capita per year? (requires population baseline)
- How do pedestrian-involved crash counts vary by hour of day and borough?
- Which contributing factors are most associated with severe injuries or fatalities?
- Are there seasonal patterns in crash frequency (monthly patterns 2012–2025)?
- Which streets/zipcodes are persistent crash hotspots?

Architecture & components (non-code)
------------------------------------
Logical layers:
1. Data ingestion
   - Download raw CSVs and store under `raw_data/` for reproducibility.
2. Pre-integration cleaning (ETL)
   - Parse dates, standardize strings (BOROUGH, VEHICLE_TYPE), remove duplicates, handle missing geocoordinates, create derived fields (CRASH_YEAR, HOUR, DAY_OF_WEEK, INJURY_TYPE).
   - Document drop vs impute decisions in the notebook.
3. Integration
   - Join crashes with persons (key: COLLISION_ID or UNIQUE_KEY). Recommended: left join crashes <- persons, and aggregate persons/vehicles into per-collision summary fields (total_injured, has_pedestrian, top_vehicle_type).
4. Storage/Serving
   - For milestone: cleaned integrated dataset stored as Parquet/CSV under `data/`.
   - Pre-aggregated tables for performance (monthly, borough counts, heatmap).
5. Backend (optional)
   - If using React frontend, provide a small API (Flask/FastAPI) with endpoints that accept filter payloads and return aggregated JSON for charts.
   - If using Dash, app can perform server-side aggregation with pandas directly.
6. Frontend
   - Filter controls, search input, Generate Report button, chart area, download/export tools.
7. Deployment
   - Host on Render, Heroku, or Vercel (with API hosted separately if needed).

Data cleaning & integration summary (what will be done)
-------------------------------------------------------
Pre-integration cleaning:
- Standardize column names, trim whitespace, and normalize casing.
- Parse CRASH_DATE and CRASH_TIME to datetime and derive CRASH_YEAR, MONTH, HOUR, DAY_OF_WEEK.
- Normalize categorical values (e.g., BOROUGH values -> Title case, map empty/unknown tokens to "Unknown").
- Remove duplicates based on UNIQUE_KEY / COLLISION_ID.
- Handle missing values:
  - Geolocation missing: leave for aggregated analyses but drop for map visualizations.
  - Injury counts missing: set to 0 if safe or label Unknown; decisions documented in notebook.
- Outlier detection:
  - Remove records with lat/lon far outside NYC bounds, future dates (> 2025), and impossibly large counts.
- Create derived summary fields: total_persons_injured, total_persons_killed, has_pedestrian_involved, vehicle_type_summary.

Integration (post-join):
- Left-join persons (and vehicles if used) to crashes.
- Aggregate persons-level information into collision-level summaries to avoid blow-up of rows and simplify filtering.
- Resolve new nulls introduced by join (e.g., collisions with no person rows) and document choices.

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


Testing & validation checklist
------------------------------
- Data integrity:
  - Row counts before/after cleaning noted in notebook.
  - Null-value report for key fields (LAT/LON, BOROUGH, INJURY counts).
  - Join validation: number of unique COLLISION_IDs before/after join.
- Functionality:
  - Dropdowns populate from dataset values at startup (/filters/options endpoint or computed in app).
  - Search parser tested against sample queries.
  - Generate Report triggers update of all charts and KPI cards.
  - Map renders in deployed environment and tiles load.
- Usability:
  - Loading indicators present.
  - Clear error messages when query returns zero records.
  - Reset filters works.

Deliverables included in this repository
---------------------------------------
- notebooks/
  - 0_data_ingest_and_cleaning.ipynb — EDA, cleaning, and integration steps with markdown explanations (required)
  - 1_additional_analysis.ipynb — exploratory visualizations supporting cleaning decisions and research questions
- app.py or frontend/ + api/ depending on chosen stack
- data_processing.py (or scripts/prepare_data.py) — ETL helper functions
- data/
  - cleaned.parquet (or instructions to download fresh)
- requirements.txt
- Procfile (for Heroku deployment)
- README.md (this file)
- LICENSE (recommended)
- docs/ (optional: wireframes, parser spec)
- .github/ (optional: issue templates or CI)

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

Acceptance criteria & grading checklist
--------------------------------------
(To be used by graders — ensure each item is addressed)
- Notebook:
  - Dataset overview and EDA present.
  - Pre-integration cleaning: missing values & outliers handled and justified.
  - Integration: joins executed and rationale documented.
  - Post-integration cleaning steps documented.
- Website:
  - Multi-dropdown filters implemented and working.
  - Natural-language search mode implemented.
  - Central Generate Report button updates all visualizations.
  - At least 4 chart types implemented (bar, line, heatmap, map, pie).
  - Interactivity available (hover, zoom, tooltips).
  - Deployed live link provided and working.
- Code & repo:
  - Modular, commented code and descriptive variable names.
  - README with setup & deployment details, team contributions, research questions.
  - All team members are in GitHub repo contributors/commit history.

