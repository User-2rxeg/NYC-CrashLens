import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from datetime import datetime
import re

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Load data once at startup (not in callback)
print("Loading data...")
try:
    # Load the STANDARDIZED dataset instead of merged
    df_global = pd.read_csv('cleaned_merged_standardized_data.csv', low_memory=False)
    print(f"Standardized data loaded successfully. Shape: {df_global.shape}")
    
    # Data preparation
    df_global['CRASH_DATE_x'] = pd.to_datetime(df_global['CRASH_DATE_x'], errors='coerce')
    df_global['YEAR'] = df_global['CRASH_DATE_x'].dt.year
    
    # Convert to string and handle NaN - standardized values should already be consistent
    # The standardized dataset already has cleaned categorical values
    df_global['BOROUGH'] = df_global['BOROUGH'].astype(str).replace('nan', 'Unknown')
    df_global['VEHICLE_TYPE_CODE_1'] = df_global['VEHICLE_TYPE_CODE_1'].astype(str).replace('nan', 'Unknown')
    df_global['CONTRIBUTING_FACTOR_VEHICLE_1'] = df_global['CONTRIBUTING_FACTOR_VEHICLE_1'].astype(str).replace('nan', 'Unknown')
    df_global['PERSON_TYPE'] = df_global['PERSON_TYPE'].astype(str).replace('nan', 'Unknown')
    
    # CRITICAL FIX #1: Properly handle PERSON_SEX standardization
    # The standardized dataset should have M/F values, but let's ensure consistency
    df_global['PERSON_SEX'] = df_global['PERSON_SEX'].astype(str).str.upper().str.strip()
    df_global['PERSON_SEX'] = df_global['PERSON_SEX'].replace({
        'MALE': 'M',
        'FEMALE': 'F',
        'NAN': 'Unknown',
        'UNKNOWN': 'Unknown',
        'U': 'Unknown'
    })
    
    df_global['PERSON_INJURY'] = df_global['PERSON_INJURY'].astype(str).replace('nan', 'Unknown')
    
    # Ensure numeric columns are properly typed
    df_global['NUMBER_OF_PERSONS_INJURED'] = pd.to_numeric(df_global['NUMBER_OF_PERSONS_INJURED'], errors='coerce').fillna(0)
    df_global['NUMBER_OF_PERSONS_KILLED'] = pd.to_numeric(df_global['NUMBER_OF_PERSONS_KILLED'], errors='coerce').fillna(0)
    
    print("Column names:", df_global.columns.tolist())
    print("Borough unique values:", df_global['BOROUGH'].unique()[:10])
    print("Years available:", sorted(df_global['YEAR'].dropna().unique()))
    print("Vehicle types (standardized):", df_global['VEHICLE_TYPE_CODE_1'].value_counts().head(10))
    print("Person types (standardized):", df_global['PERSON_TYPE'].value_counts())
    
    # CRITICAL FIX #2: Check gender distribution
    print("\n=== GENDER DISTRIBUTION CHECK ===")
    print(f"PERSON_SEX value counts:\n{df_global['PERSON_SEX'].value_counts()}")
    print(f"Total records: {len(df_global)}")
    print(f"Records with M: {len(df_global[df_global['PERSON_SEX'] == 'M'])}")
    print(f"Records with F: {len(df_global[df_global['PERSON_SEX'] == 'F'])}")
    print(f"Records with Unknown gender: {len(df_global[df_global['PERSON_SEX'] == 'Unknown'])}")
    
except Exception as e:
    print(f"Error loading data: {e}")
    import traceback
    traceback.print_exc()
    df_global = pd.DataFrame()

# CRITICAL FIX #3: Enhanced search function with proper gender handling
def parse_search_query(query, df):
    """Parse natural language search queries"""
    if not query or query.strip() == "":
        return df
    
    query = query.lower().strip()
    filtered_df = df.copy()
    
    print(f"Parsing search query: '{query}'")
    print(f"Initial dataframe size: {len(filtered_df)}")
    
    # Borough detection - using standardized borough names
    borough_mapping = {
        'manhattan': 'MANHATTAN',
        'brooklyn': 'BROOKLYN',
        'queens': 'QUEENS',
        'bronx': 'BRONX',
        'staten island': 'STATEN ISLAND',
        'staten': 'STATEN ISLAND'
    }
    
    for search_term, standard_borough in borough_mapping.items():
        if search_term in query:
            print(f"Filtering by borough: {standard_borough}")
            filtered_df = filtered_df[filtered_df['BOROUGH'] == standard_borough]
            print(f"After borough filter: {len(filtered_df)}")
            break
    
    # CRITICAL FIX #4: Add gender detection to search query
    gender_keywords = {
        'male': 'M',
        'man': 'M',
        'men': 'M',
        'female': 'F',
        'woman': 'F',
        'women': 'F'
    }
    
    for keyword, gender_code in gender_keywords.items():
        if keyword in query:
            print(f"Filtering by gender keyword '{keyword}' -> '{gender_code}'")
            filtered_df = filtered_df[filtered_df['PERSON_SEX'] == gender_code]
            print(f"After gender filter: {len(filtered_df)}")
            break  # Only apply first gender match
    
    # Year detection
    year_match = re.findall(r'\b(20\d{2})\b', query)
    if year_match:
        year = int(year_match[0])
        print(f"Filtering by year: {year}")
        filtered_df = filtered_df[filtered_df['YEAR'] == year]
        print(f"After year filter: {len(filtered_df)}")
    
    # Keywords for person types - using standardized values
    if 'pedestrian' in query:
        print("Filtering by pedestrian")
        filtered_df = filtered_df[filtered_df['PERSON_TYPE'] == 'PEDESTRIAN']
        print(f"After pedestrian filter: {len(filtered_df)}")
    
    if 'cyclist' in query or 'bicycle' in query or 'bike' in query:
        print("Filtering by cyclist")
        filtered_df = filtered_df[filtered_df['PERSON_TYPE'] == 'BICYCLIST']
        print(f"After cyclist filter: {len(filtered_df)}")
    
    if 'driver' in query:
        print("Filtering by driver")
        filtered_df = filtered_df[filtered_df['PERSON_TYPE'] == 'DRIVER']
        print(f"After driver filter: {len(filtered_df)}")
    
    if 'passenger' in query:
        print("Filtering by passenger")
        filtered_df = filtered_df[filtered_df['PERSON_TYPE'] == 'PASSENGER']
        print(f"After passenger filter: {len(filtered_df)}")
    
    # Injury keywords - using standardized injury values
    if 'injured' in query or 'injury' in query:
        print("Filtering by injuries")
        filtered_df = filtered_df[
            (filtered_df['NUMBER_OF_PERSONS_INJURED'] > 0) | 
            (filtered_df['PERSON_INJURY'] == 'INJURED')
        ]
        print(f"After injury filter: {len(filtered_df)}")
    
    if 'uninjured' in query:
        print("Filtering by uninjured")
        filtered_df = filtered_df[filtered_df['PERSON_INJURY'] == 'UNINJURED']
        print(f"After uninjured filter: {len(filtered_df)}")
    
    if 'killed' in query or 'fatal' in query or 'death' in query:
        print("Filtering by fatalities")
        filtered_df = filtered_df[
            (filtered_df['NUMBER_OF_PERSONS_KILLED'] > 0) | 
            (filtered_df['PERSON_INJURY'] == 'KILLED')
        ]
        print(f"After fatality filter: {len(filtered_df)}")
    
    # Vehicle type keywords - using standardized values
    vehicle_keywords = {
        'taxi': 'TAXI',
        'sedan': 'SEDAN',
        'suv': 'SPORT UTILITY / STATION WAGON',
        'truck': 'PICK-UP TRUCK',
        'van': 'VAN',
        'bus': 'BUS',
        'motorcycle': 'MOTORCYCLE',
        'bicycle': 'BICYCLE'
    }
    
    for keyword, standard_vehicle in vehicle_keywords.items():
        if keyword in query:
            print(f"Filtering by vehicle type: {standard_vehicle}")
            filtered_df = filtered_df[filtered_df['VEHICLE_TYPE_CODE_1'] == standard_vehicle]
            print(f"After vehicle filter: {len(filtered_df)}")
            break
    
    print(f"Final filtered dataframe size: {len(filtered_df)}")
    return filtered_df

# Layout components
def create_filter_panel():
    """Create the filter control panel"""
    return dbc.Card([
        dbc.CardHeader("Data Filters"),
        dbc.CardBody([
            # Search input
            dbc.Row([
                dbc.Col([
                    html.Label("Search Query:", className="fw-bold"),
                    dbc.Input(
                        id="search-input",
                        placeholder="e.g., 'Brooklyn 2022 pedestrian crashes'",
                        type="text"
                    ),
                    html.Small("Try: 'Brooklyn 2023', 'Manhattan pedestrian', 'Queens 2022 injured'", 
                              className="text-muted")
                ])
            ], className="mb-3"),
            
            # Borough filter
            dbc.Row([
                dbc.Col([
                    html.Label("Borough:", className="fw-bold"),
                    dcc.Dropdown(
                        id="borough-dropdown",
                        multi=True,
                        placeholder="Select boroughs..."
                    )
                ])
            ], className="mb-3"),
            
            # Year filter
            dbc.Row([
                dbc.Col([
                    html.Label("Year:", className="fw-bold"),
                    dcc.Dropdown(
                        id="year-dropdown",
                        multi=True,
                        placeholder="Select years..."
                    )
                ])
            ], className="mb-3"),
            
            # Vehicle type filter
            dbc.Row([
                dbc.Col([
                    html.Label("Vehicle Type:", className="fw-bold"),
                    dcc.Dropdown(
                        id="vehicle-dropdown",
                        multi=True,
                        placeholder="Select vehicle types..."
                    )
                ])
            ], className="mb-3"),
            
            # Person type filter
            dbc.Row([
                dbc.Col([
                    html.Label("Person Type:", className="fw-bold"),
                    dcc.Dropdown(
                        id="person-dropdown",
                        multi=True,
                        placeholder="Select person types..."
                    )
                ])
            ], className="mb-3"),
            
            # Gender filter
            dbc.Row([
                dbc.Col([
                    html.Label("Gender:", className="fw-bold"),
                    dcc.Dropdown(
                        id="gender-dropdown",
                        multi=True,
                        placeholder="Select gender..."
                    )
                ])
            ], className="mb-3"),
            
            # Contributing Factor filter
            dbc.Row([
                dbc.Col([
                    html.Label("Contributing Factor:", className="fw-bold"),
                    dcc.Dropdown(
                        id="contributing-factor-dropdown",
                        multi=True,
                        placeholder="Select contributing factors..."
                    )
                ])
            ], className="mb-3"),
            
            # Injury Type filter
            dbc.Row([
                dbc.Col([
                    html.Label("Injury Type:", className="fw-bold"),
                    dcc.Dropdown(
                        id="injury-type-dropdown",
                        multi=True,
                        placeholder="Select injury types..."
                    )
                ])
            ], className="mb-3"),
            
            # Generate Report button
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        "Generate Report",
                        id="generate-report-btn",
                        color="primary",
                        size="lg",
                        className="w-100"
                    )
                ])
            ]),
            
            # Reset filters button
            dbc.Row([
                dbc.Col([
                    dbc.Button(
                        "Reset Filters",
                        id="reset-btn",
                        color="secondary",
                        size="sm",
                        className="w-100 mt-2"
                    )
                ])
            ])
        ])
    ])

def create_kpi_cards():
    """Create KPI summary cards"""
    return dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="total-crashes", className="text-primary"),
                    html.P("Total Crashes", className="card-text")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="total-injuries", className="text-warning"),
                    html.P("Total Injuries", className="card-text")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="total-fatalities", className="text-danger"),
                    html.P("Total Fatalities", className="card-text")
                ])
            ])
        ], width=3),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="most-dangerous-borough", className="text-info"),
                    html.P("Most Dangerous Borough", className="card-text")
                ])
            ])
        ], width=3)
    ], className="mb-4")

# Main app layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("NYC CrashLens Dashboard", className="text-center mb-4"),
            html.P("Interactive exploration of NYC crash data (Standardized Dataset)", className="text-center text-muted")
        ])
    ]),
    
    # Main content
    dbc.Row([
        # Filter panel
        dbc.Col([
            create_filter_panel()
        ], width=3),
        
        # Charts area
        dbc.Col([
            # KPI cards
            create_kpi_cards(),
            
            # First row of charts
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="borough-bar-chart")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id="time-series-chart")
                ], width=6)
            ]),
            
            # Second row of charts
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="person-type-pie-chart")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id="contributing-factor-bar-chart")
                ], width=6)
            ]),
            
            # Third row - Vehicle type bar chart and Gender comparison
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="vehicle-type-bar-chart")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id="gender-comparison-chart")
                ], width=6)
            ]),
            
            # Fourth row - Map
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="crash-map")
                ], width=12)
            ])
        ], width=9)
    ])
], fluid=True)

# Callback to populate dropdown options
@callback(
    [Output('borough-dropdown', 'options'),
     Output('year-dropdown', 'options'),
     Output('vehicle-dropdown', 'options'),
     Output('person-dropdown', 'options'),
     Output('gender-dropdown', 'options'),
     Output('contributing-factor-dropdown', 'options'),
     Output('injury-type-dropdown', 'options')],
    Input('borough-dropdown', 'id')
)
def update_dropdown_options(_):
    if df_global.empty:
        return [], [], [], [], [], [], []
    
    print("Updating dropdown options from standardized dataset...")
    
    # Borough options - standardized values
    boroughs = df_global['BOROUGH'].unique()
    boroughs = [b for b in boroughs if str(b) not in ['Unknown', 'UNKNOWN', 'None', '', 'nan']]
    borough_options = [{'label': str(b), 'value': str(b)} for b in sorted(boroughs)]
    print(f"Borough options: {len(borough_options)} - {borough_options}")
    
    # Year options
    years = df_global['YEAR'].dropna().unique()
    year_options = [{'label': int(y), 'value': int(y)} for y in sorted(years)]
    print(f"Year options: {len(year_options)}")
    
    # Vehicle type options - standardized values (top 15)
    vehicles = df_global['VEHICLE_TYPE_CODE_1'].value_counts().head(15).index.tolist()
    vehicles = [v for v in vehicles if str(v) not in ['Unknown', 'UNKNOWN', 'None', '', 'nan']]
    vehicle_options = [{'label': str(v), 'value': str(v)} for v in vehicles]
    print(f"Vehicle options (standardized): {len(vehicle_options)} - {[v['label'] for v in vehicle_options]}")
    
    # Person type options - standardized values
    persons = df_global['PERSON_TYPE'].unique()
    persons = [p for p in persons if str(p) not in ['Unknown', 'UNKNOWN', 'None', '', 'nan']]
    person_options = [{'label': str(p), 'value': str(p)} for p in sorted(persons)]
    print(f"Person options (standardized): {len(person_options)} - {[p['label'] for p in person_options]}")
    
    # Gender options - simple labels without counts
    gender_counts = df_global['PERSON_SEX'].value_counts()
    gender_options = []
    if gender_counts.get('M', 0) > 0:
        gender_options.append({'label': 'Male', 'value': 'M'})
    if gender_counts.get('F', 0) > 0:
        gender_options.append({'label': 'Female', 'value': 'F'})
    
    print(f"Gender options: {gender_options}")
    
    # Contributing Factor options - standardized values (top 15)
    factors = df_global['CONTRIBUTING_FACTOR_VEHICLE_1'].value_counts().head(15).index.tolist()
    factors = [f for f in factors if str(f) not in ['Unknown', 'UNKNOWN', 'None', '', 'nan', 'UNSPECIFIED']]
    contributing_factor_options = [{'label': str(f), 'value': str(f)} for f in factors]
    print(f"Contributing Factor options (standardized): {len(contributing_factor_options)}")
    
    # Injury Type options - standardized values
    if 'PERSON_INJURY' in df_global.columns:
        injuries = df_global['PERSON_INJURY'].unique()
        injuries = [i for i in injuries if str(i) not in ['Unknown', 'UNKNOWN', 'None', '', 'nan']]
        injury_type_options = [{'label': str(i), 'value': str(i)} for i in sorted(injuries)]
        print(f"Injury Type options (standardized): {len(injury_type_options)} - {[i['label'] for i in injury_type_options]}")
    else:
        injury_type_options = []
        print("PERSON_INJURY column not found")

    return borough_options, year_options, vehicle_options, person_options, gender_options, contributing_factor_options, injury_type_options


# Reset filters callback
@callback(
    [Output('search-input', 'value'),
     Output('borough-dropdown', 'value'),
     Output('year-dropdown', 'value'),
     Output('vehicle-dropdown', 'value'),
     Output('person-dropdown', 'value'),
     Output('gender-dropdown', 'value'),
     Output('contributing-factor-dropdown', 'value'),
     Output('injury-type-dropdown', 'value')],
    Input('reset-btn', 'n_clicks'),
    prevent_initial_call=True
)
def reset_filters(n_clicks):
    return "", None, None, None, None, None, None, None

# Main callback for updating all charts
@callback(
    [Output('total-crashes', 'children'),
     Output('total-injuries', 'children'),
     Output('total-fatalities', 'children'),
     Output('most-dangerous-borough', 'children'),
     Output('borough-bar-chart', 'figure'),
     Output('time-series-chart', 'figure'),
     Output('person-type-pie-chart', 'figure'),
     Output('contributing-factor-bar-chart', 'figure'),
     Output('vehicle-type-bar-chart', 'figure'),
     Output('gender-comparison-chart', 'figure'),
     Output('crash-map', 'figure')],
    Input('generate-report-btn', 'n_clicks'),
    [dash.dependencies.State('search-input', 'value'),
     dash.dependencies.State('borough-dropdown', 'value'),
     dash.dependencies.State('year-dropdown', 'value'),
     dash.dependencies.State('vehicle-dropdown', 'value'),
     dash.dependencies.State('person-dropdown', 'value'),
     dash.dependencies.State('gender-dropdown', 'value'),
     dash.dependencies.State('contributing-factor-dropdown', 'value'),
     dash.dependencies.State('injury-type-dropdown', 'value')],
    prevent_initial_call=False
)
def update_dashboard(n_clicks, search_query, boroughs, years, vehicles, persons, genders, contributing_factors, injury_types):
    if df_global.empty:
        empty_fig = go.Figure()
        empty_fig.add_annotation(text="No data available", x=0.5, y=0.5, showarrow=False)
        return "0", "0", "0", "N/A", empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig
    
    try:
        df = df_global.copy()
        print(f"\n=== Update Dashboard Called (Standardized Data) ===")
        print(f"Initial data shape: {df.shape}")
        print(f"Search query: {search_query}")
        print(f"Borough filter: {boroughs}")
        print(f"Year filter: {years}")
        print(f"Vehicle filter: {vehicles}")
        print(f"Person filter: {persons}")
        print(f"Gender filter: {genders}")
        print(f"Contributing Factor filter: {contributing_factors}")
        print(f"Injury Type filter: {injury_types}")
        
        # Apply search filter first
        if search_query and search_query.strip():
            df = parse_search_query(search_query, df)
            print(f"After search query: {df.shape}")
        
        # Apply dropdown filters - all using standardized values
        if boroughs:
            print(f"Applying borough filter: {boroughs}")
            df = df[df['BOROUGH'].isin([str(b) for b in boroughs])]
            print(f"After borough dropdown filter: {df.shape}")
        
        if years:
            print(f"Applying year filter: {years}")
            df = df[df['YEAR'].isin([int(y) for y in years])]
            print(f"After year filter: {df.shape}")
        
        if vehicles:
            print(f"Applying vehicle filter: {vehicles}")
            df = df[df['VEHICLE_TYPE_CODE_1'].isin([str(v) for v in vehicles])]
            print(f"After vehicle filter: {df.shape}")
        
        if persons:
            print(f"Applying person filter: {persons}")
            df = df[df['PERSON_TYPE'].isin([str(p) for p in persons])]
            print(f"After person filter: {df.shape}")
        
        # CRITICAL FIX #8: Enhanced gender filtering with validation
        if genders:
            print(f"Applying gender filter: {genders}")
            print(f"Before gender filter - PERSON_SEX values: {df['PERSON_SEX'].value_counts().to_dict()}")
            df = df[df['PERSON_SEX'].isin([str(g) for g in genders])]
            print(f"After gender filter: {df.shape}")
            print(f"After gender filter - PERSON_SEX values: {df['PERSON_SEX'].value_counts().to_dict()}")
        
        if contributing_factors:
            print(f"Applying contributing factor filter: {contributing_factors}")
            df = df[df['CONTRIBUTING_FACTOR_VEHICLE_1'].isin([str(c) for c in contributing_factors])]
            print(f"After contributing factor filter: {df.shape}")
        
        if injury_types and 'PERSON_INJURY' in df.columns:
            print(f"Applying injury type filter: {injury_types}")
            df = df[df['PERSON_INJURY'].isin([str(i) for i in injury_types])]
            print(f"After injury type filter: {df.shape}")
        
        # Check if we have any data left
        if len(df) == 0:
            print("WARNING: No data remaining after filters!")
            empty_fig = go.Figure()
            empty_fig.add_annotation(
                text="No data matches the selected filters.<br>Try adjusting your filter criteria.",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
            return "0", "0", "0", "N/A", empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig
        
        # Calculate KPIs
        total_crashes = len(df)
        total_injuries = int(df['NUMBER_OF_PERSONS_INJURED'].sum())
        total_fatalities = int(df['NUMBER_OF_PERSONS_KILLED'].sum())
        
        # Most dangerous borough
        if len(df) > 0:
            borough_danger = df.groupby('BOROUGH')['NUMBER_OF_PERSONS_KILLED'].sum()
            borough_danger = borough_danger[~borough_danger.index.isin(['Unknown', 'UNKNOWN'])]
            most_dangerous = borough_danger.idxmax() if len(borough_danger) > 0 and borough_danger.max() > 0 else "N/A"
        else:
            most_dangerous = "N/A"
        
        # 1. Borough Bar Chart
        if len(df) > 0:
            borough_counts = df['BOROUGH'].value_counts().head(10)
            # Exclude Unknown
            borough_counts = borough_counts[~borough_counts.index.isin(['Unknown', 'UNKNOWN'])]
            
            borough_bar_fig = px.bar(
                x=borough_counts.index,
                y=borough_counts.values,
                title="Crashes by Borough (Top 10)",
                labels={'x': 'Borough', 'y': 'Number of Crashes'},
                color=borough_counts.values,
                color_continuous_scale='Reds'
            )
            borough_bar_fig.update_layout(
                xaxis_title="Borough",
                yaxis_title="Number of Crashes",
                showlegend=False
            )
        else:
            borough_bar_fig = go.Figure()
            borough_bar_fig.add_annotation(text="No data matches the selected filters", x=0.5, y=0.5, showarrow=False)
    
        # 2. Time series chart
        if len(df) > 0 and 'YEAR' in df.columns:
            yearly_counts = df['YEAR'].value_counts().sort_index()
            time_fig = px.line(
                x=yearly_counts.index,
                y=yearly_counts.values,
                title="Crashes Over Time",
                labels={'x': 'Year', 'y': 'Number of Crashes'},
                markers=True
            )
            time_fig.update_layout(
                xaxis_title="Year",
                yaxis_title="Number of Crashes"
            )
        else:
            time_fig = go.Figure()
            time_fig.add_annotation(text="No temporal data available", x=0.5, y=0.5, showarrow=False)
        
        # 3. Person Type Pie Chart - using standardized values
        if len(df) > 0:
            person_counts = df['PERSON_TYPE'].value_counts().head(6)
            # Filter out Unknown
            person_counts = person_counts[~person_counts.index.isin(['Unknown', 'UNKNOWN'])]
            
            pie_fig = px.pie(
                values=person_counts.values,
                names=person_counts.index,
                title="Person Type Distribution (Standardized)",
                hole=0.3  # Creates a donut chart
            )
            pie_fig.update_traces(textposition='inside', textinfo='percent+label')
        else:
            pie_fig = go.Figure()
            pie_fig.add_annotation(text="No data available", x=0.5, y=0.5, showarrow=False)
        
        # 4. Contributing Factor Bar Chart - using standardized values
        if len(df) > 0:
            factor_counts = df['CONTRIBUTING_FACTOR_VEHICLE_1'].value_counts().head(10)
            # Filter out Unknown and Unspecified
            factor_counts = factor_counts[~factor_counts.index.isin(['Unknown', 'UNKNOWN', 'UNSPECIFIED'])]
            
            factor_bar_fig = px.bar(
                x=factor_counts.values,
                y=factor_counts.index,
                title="Top Contributing Factors (Standardized)",
                labels={'x': 'Number of Crashes', 'y': 'Contributing Factor'},
                orientation='h',
                color=factor_counts.values,
                color_continuous_scale='Blues'
            )
            factor_bar_fig.update_layout(
                xaxis_title="Number of Crashes",
                yaxis_title="Contributing Factor",
                showlegend=False,
                height=400
            )
        else:
            factor_bar_fig = go.Figure()
            factor_bar_fig.add_annotation(text="No data available", x=0.5, y=0.5, showarrow=False)
        
        # 5. Vehicle Type Bar Chart - using standardized values
        if len(df) > 0:
            vehicle_counts = df['VEHICLE_TYPE_CODE_1'].value_counts().head(10)
            # Filter out Unknown
            vehicle_counts = vehicle_counts[~vehicle_counts.index.isin(['Unknown', 'UNKNOWN'])]
            
            vehicle_bar_fig = px.bar(
                x=vehicle_counts.index,
                y=vehicle_counts.values,
                title="Top Vehicle Types Involved in Crashes (Standardized)",
                labels={'x': 'Vehicle Type', 'y': 'Number of Crashes'},
                color=vehicle_counts.values,
                color_continuous_scale='Greens'
            )
            vehicle_bar_fig.update_layout(
                xaxis_title="Vehicle Type",
                yaxis_title="Number of Crashes",
                showlegend=False,
                xaxis_tickangle=-45,
                height=400
            )
        else:
            vehicle_bar_fig = go.Figure()
            vehicle_bar_fig.add_annotation(text="No data available", x=0.5, y=0.5, showarrow=False)
        
        # 6. Gender Comparison Chart - using standardized M/F values
        if len(df) > 0 and 'PERSON_SEX' in df.columns and 'PERSON_INJURY' in df.columns:
            # Use the FILTERED data (respects gender dropdown)
            # Only show M/F, exclude Unknown
            gender_df = df[df['PERSON_SEX'].isin(['M', 'F'])].copy()
            
            print(f"\n=== GENDER CHART DEBUG ===")
            print(f"Filtered data for gender chart: {len(gender_df)} records")
            print(f"Gender distribution: {gender_df['PERSON_SEX'].value_counts().to_dict()}")
            
            if len(gender_df) > 0:
                # Initialize result dictionary for both genders (even if one is filtered out)
                gender_data = {
                    'Female': {'Uninjured': 0, 'Injured': 0, 'Killed': 0},
                    'Male': {'Uninjured': 0, 'Injured': 0, 'Killed': 0}
                }
                
                # Process each gender that exists in filtered data
                for sex_code, sex_label in [('F', 'Female'), ('M', 'Male')]:
                    sex_df = gender_df[gender_df['PERSON_SEX'] == sex_code]
                    
                    if len(sex_df) > 0:
                        # Count by PERSON_INJURY standardized values
                        gender_data[sex_label]['Uninjured'] = len(sex_df[sex_df['PERSON_INJURY'] == 'UNINJURED'])
                        gender_data[sex_label]['Injured'] = len(sex_df[sex_df['PERSON_INJURY'] == 'INJURED'])
                        gender_data[sex_label]['Killed'] = len(sex_df[sex_df['PERSON_INJURY'] == 'KILLED'])
                        
                        # If no explicit injury classification, use aggregated counts
                        if gender_data[sex_label]['Injured'] == 0:
                            gender_data[sex_label]['Injured'] = int(sex_df['NUMBER_OF_PERSONS_INJURED'].sum())
                        if gender_data[sex_label]['Killed'] == 0:
                            gender_data[sex_label]['Killed'] = int(sex_df['NUMBER_OF_PERSONS_KILLED'].sum())
                        
                        # Calculate uninjured as remainder if not explicitly coded
                        total_sex = len(sex_df)
                        if gender_data[sex_label]['Uninjured'] == 0:
                            gender_data[sex_label]['Uninjured'] = max(0, 
                                total_sex - gender_data[sex_label]['Injured'] - gender_data[sex_label]['Killed'])
                
                print(f"Gender data calculated: {gender_data}")
                
                # Only include genders that have data
                gender_labels = []
                uninjured_values = []
                injured_values = []
                killed_values = []
                
                for gender in ['Female', 'Male']:
                    total_for_gender = (gender_data[gender]['Uninjured'] + 
                                      gender_data[gender]['Injured'] + 
                                      gender_data[gender]['Killed'])
                    if total_for_gender > 0:
                        gender_labels.append(gender)
                        uninjured_values.append(gender_data[gender]['Uninjured'])
                        injured_values.append(gender_data[gender]['Injured'])
                        killed_values.append(gender_data[gender]['Killed'])
                
                if len(gender_labels) > 0:
                    # Create the chart
                    gender_fig = go.Figure()
                    
                    # Add traces with consistent formatting
                    gender_fig.add_trace(go.Bar(
                        name='Uninjured',
                        x=gender_labels,
                        y=uninjured_values,
                        marker_color='lightgreen',
                        text=[f'{int(val):,}' for val in uninjured_values],
                        textposition='outside',
                        textfont=dict(size=14, color='black')
                    ))
                    
                    gender_fig.add_trace(go.Bar(
                        name='Injuries',
                        x=gender_labels,
                        y=injured_values,
                        marker_color='orange',
                        text=[f'{int(val):,}' for val in injured_values],
                        textposition='outside',
                        textfont=dict(size=14, color='black')
                    ))
                    
                    gender_fig.add_trace(go.Bar(
                        name='Fatalities',
                        x=gender_labels,
                        y=killed_values,
                        marker_color='red',
                        text=[f'{int(val):,}' for val in killed_values],
                        textposition='outside',
                        textfont=dict(size=14, color='black')
                    ))
                    
                    # Build title based on filters
                    title_parts = ['Gender Comparison']
                    if genders:
                        gender_names = ['Male' if g == 'M' else 'Female' for g in genders]
                        title_parts.append(f"({', '.join(gender_names)} Only)")
                    
                    gender_fig.update_layout(
                        title=dict(
                            text=' - '.join(title_parts),
                            font=dict(size=18)
                        ),
                        xaxis_title='Gender',
                        yaxis_title='Count',
                        barmode='group',
                        height=500,
                        font=dict(size=16),
                        legend=dict(
                            font=dict(size=14),
                            orientation="h",
                            yanchor="bottom",
                            y=1.02,
                            xanchor="right",
                            x=1
                        ),
                        yaxis=dict(tickformat=",d")
                    )
                    
                    print(f"Gender chart created with labels: {gender_labels}")
                else:
                    gender_fig = go.Figure()
                    gender_fig.add_annotation(
                        text="No gender data available for selected filters",
                        x=0.5, y=0.5,
                        showarrow=False,
                        font=dict(size=16)
                    )
            else:
                gender_fig = go.Figure()
                gender_fig.add_annotation(
                    text="No valid gender data (M/F) in filtered results",
                    x=0.5, y=0.5,
                    showarrow=False,
                    font=dict(size=16)
                )
        else:
            gender_fig = go.Figure()
            gender_fig.add_annotation(
                text="Gender or injury data not available",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=16)
            )
        
        # 7. Map (sample data for performance)
        if len(df) > 0 and 'LATITUDE' in df.columns and 'LONGITUDE' in df.columns:
            map_df = df.dropna(subset=['LATITUDE', 'LONGITUDE'])
            # Filter out invalid coordinates
            map_df = map_df[
                (map_df['LATITUDE'] >= 40.5) & 
                (map_df['LATITUDE'] <= 40.9) &
                (map_df['LONGITUDE'] >= -74.25) & 
                (map_df['LONGITUDE'] <= -73.7)
            ]
            
            if len(map_df) > 0:
                sample_size = min(1000, len(map_df))
                map_df = map_df.sample(n=sample_size, random_state=42)
                
                map_fig = px.scatter_mapbox(
                    map_df,
                    lat="LATITUDE",
                    lon="LONGITUDE",
                    hover_data=["BOROUGH", "VEHICLE_TYPE_CODE_1"],
                    zoom=10,
                    height=400,
                    title=f"Crash Locations (Sample of {sample_size} crashes)",
                    color_discrete_sequence=["red"]
                )
                map_fig.update_layout(
                    mapbox_style="open-street-map",
                    mapbox=dict(center=dict(lat=40.7, lon=-74.0))
                )
            else:
                map_fig = go.Figure()
                map_fig.add_annotation(text="No valid location data available", x=0.5, y=0.5, showarrow=False)
        else:
            map_fig = go.Figure()
            map_fig.add_annotation(text="No location data available", x=0.5, y=0.5, showarrow=False)
        
        print(f"=== Results (Standardized Data) ===")
        print(f"Crashes: {total_crashes:,}, Injuries: {total_injuries:,}, Fatalities: {total_fatalities:,}")
        print(f"Most dangerous borough: {most_dangerous}")
        
        return (
            f"{total_crashes:,}",
            f"{total_injuries:,}",
            f"{total_fatalities:,}",
            most_dangerous,
            borough_bar_fig,
            time_fig,
            pie_fig,
            factor_bar_fig,
            vehicle_bar_fig,
            gender_fig,
            map_fig
        )
    
    except Exception as e:
        print(f"ERROR in update_dashboard: {e}")
        import traceback
        traceback.print_exc()
        
        empty_fig = go.Figure()
        empty_fig.add_annotation(
            text=f"Error processing data: {str(e)}<br>Check console for details",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color='red')
        )
        return "Error", "Error", "Error", "Error", empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
