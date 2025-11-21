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
    df_global = pd.read_csv('cleaned_merged_data.csv', low_memory=False)
    print(f"Data loaded successfully. Shape: {df_global.shape}")
    
    # Data preparation
    df_global['CRASH_DATE_x'] = pd.to_datetime(df_global['CRASH_DATE_x'], errors='coerce')
    df_global['YEAR'] = df_global['CRASH_DATE_x'].dt.year
    
    # Convert to string and handle NaN
    df_global['BOROUGH'] = df_global['BOROUGH'].astype(str).replace('nan', 'Unknown')
    df_global['VEHICLE_TYPE_CODE_1'] = df_global['VEHICLE_TYPE_CODE_1'].astype(str).replace('nan', 'Unknown')
    df_global['CONTRIBUTING_FACTOR_VEHICLE_1'] = df_global['CONTRIBUTING_FACTOR_VEHICLE_1'].astype(str).replace('nan', 'Unknown')
    df_global['PERSON_TYPE'] = df_global['PERSON_TYPE'].astype(str).replace('nan', 'Unknown')
    df_global['PERSON_SEX'] = df_global['PERSON_SEX'].astype(str).replace('nan', 'Unknown')
    
    # Ensure numeric columns are properly typed
    df_global['NUMBER_OF_PERSONS_INJURED'] = pd.to_numeric(df_global['NUMBER_OF_PERSONS_INJURED'], errors='coerce').fillna(0)
    df_global['NUMBER_OF_PERSONS_KILLED'] = pd.to_numeric(df_global['NUMBER_OF_PERSONS_KILLED'], errors='coerce').fillna(0)
    
    print("Column names:", df_global.columns.tolist())
    print("Borough unique values:", df_global['BOROUGH'].unique()[:10])
    print("Years available:", sorted(df_global['YEAR'].dropna().unique()))
    
except Exception as e:
    print(f"Error loading data: {e}")
    df_global = pd.DataFrame()

# Search function
def parse_search_query(query, df):
    """Parse natural language search queries"""
    if not query or query.strip() == "":
        return df
    
    query = query.lower().strip()
    filtered_df = df.copy()
    
    print(f"Parsing search query: '{query}'")
    print(f"Initial dataframe size: {len(filtered_df)}")
    
    # Borough detection
    boroughs = ['manhattan', 'brooklyn', 'queens', 'bronx', 'staten island']
    for borough in boroughs:
        if borough in query:
            print(f"Filtering by borough: {borough}")
            filtered_df = filtered_df[filtered_df['BOROUGH'].str.lower().str.contains(borough, na=False)]
            print(f"After borough filter: {len(filtered_df)}")
    
    # Year detection
    year_match = re.findall(r'\b(20\d{2})\b', query)
    if year_match:
        year = int(year_match[0])
        print(f"Filtering by year: {year}")
        filtered_df = filtered_df[filtered_df['YEAR'] == year]
        print(f"After year filter: {len(filtered_df)}")
    
    # Keywords for person types
    if 'pedestrian' in query:
        print("Filtering by pedestrian")
        print("Person type values:", filtered_df['PERSON_TYPE'].unique()[:10])
        filtered_df = filtered_df[filtered_df['PERSON_TYPE'].str.lower().str.contains('pedestrian', na=False)]
        print(f"After pedestrian filter: {len(filtered_df)}")
    
    if 'cyclist' in query or 'bicycle' in query:
        print("Filtering by cyclist")
        filtered_df = filtered_df[filtered_df['PERSON_TYPE'].str.lower().str.contains('cyclist|bicycle', na=False)]
        print(f"After cyclist filter: {len(filtered_df)}")
    
    if 'driver' in query:
        print("Filtering by driver")
        filtered_df = filtered_df[filtered_df['PERSON_TYPE'].str.lower().str.contains('driver', na=False)]
        print(f"After driver filter: {len(filtered_df)}")
    
    # Injury keywords
    if 'injured' in query or 'injury' in query:
        print("Filtering by injuries")
        filtered_df = filtered_df[filtered_df['NUMBER_OF_PERSONS_INJURED'] > 0]
        print(f"After injury filter: {len(filtered_df)}")
    
    if 'killed' in query or 'fatal' in query or 'death' in query:
        print("Filtering by fatalities")
        filtered_df = filtered_df[filtered_df['NUMBER_OF_PERSONS_KILLED'] > 0]
        print(f"After fatality filter: {len(filtered_df)}")
    
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
            html.P("Interactive exploration of NYC crash data", className="text-center text-muted")
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
                    dcc.Graph(id="vehicle-type-pie-chart")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id="contributing-factor-bar-chart")
                ], width=6)
            ]),
            
            # Third row - Gender comparison and map
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id="gender-comparison-chart")
                ], width=6),
                dbc.Col([
                    dcc.Graph(id="crash-map")
                ], width=6)
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
    
    print("Updating dropdown options...")
    
    # Borough options
    boroughs = df_global['BOROUGH'].unique()
    boroughs = [b for b in boroughs if str(b) not in ['Unknown', 'None', '', 'nan']]
    borough_options = [{'label': str(b), 'value': str(b)} for b in sorted(boroughs)]
    print(f"Borough options: {len(borough_options)}")
    
    # Year options
    years = df_global['YEAR'].dropna().unique()
    year_options = [{'label': int(y), 'value': int(y)} for y in sorted(years)]
    print(f"Year options: {len(year_options)}")
    
    # Vehicle type options (top 15)
    vehicles = df_global['VEHICLE_TYPE_CODE_1'].value_counts().head(15).index.tolist()
    vehicles = [v for v in vehicles if str(v) not in ['Unknown', 'None', '', 'nan']]
    vehicle_options = [{'label': str(v), 'value': str(v)} for v in vehicles]
    print(f"Vehicle options: {len(vehicle_options)}")
    
    # Person type options
    persons = df_global['PERSON_TYPE'].unique()
    persons = [p for p in persons if str(p) not in ['Unknown', 'None', '', 'nan']]
    person_options = [{'label': str(p), 'value': str(p)} for p in sorted(persons)]
    print(f"Person options: {len(person_options)}")
    
    # Gender options
    gender_options = [
        {'label': 'Male', 'value': 'M'},
        {'label': 'Female', 'value': 'F'}
    ]
    print(f"Gender options: {len(gender_options)}")
    
    # Contributing Factor options (top 15)
    factors = df_global['CONTRIBUTING_FACTOR_VEHICLE_1'].value_counts().head(15).index.tolist()
    factors = [f for f in factors if str(f) not in ['Unknown', 'None', '', 'nan', 'UNSPECIFIED']]
    contributing_factor_options = [{'label': str(f), 'value': str(f)} for f in factors]
    print(f"Contributing Factor options: {len(contributing_factor_options)}")
    
    # Injury Type options
    if 'PERSON_INJURY' in df_global.columns:
        injuries = df_global['PERSON_INJURY'].unique()
        injuries = [i for i in injuries if str(i) not in ['Unknown', 'None', '', 'nan']]
        injury_type_options = [{'label': str(i), 'value': str(i)} for i in sorted(injuries)]
        print(f"Injury Type options: {len(injury_type_options)}")
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
     Output('vehicle-type-pie-chart', 'figure'),
     Output('contributing-factor-bar-chart', 'figure'),
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
        return "0", "0", "0", "N/A", empty_fig, empty_fig, empty_fig, empty_fig, empty_fig, empty_fig
    
    df = df_global.copy()
    print(f"\n=== Update Dashboard Called ===")
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
    
    # Apply dropdown filters
    if boroughs:
        df = df[df['BOROUGH'].isin([str(b) for b in boroughs])]
        print(f"After borough dropdown filter: {df.shape}")
    
    if years:
        df = df[df['YEAR'].isin([int(y) for y in years])]
        print(f"After year filter: {df.shape}")
    
    if vehicles:
        df = df[df['VEHICLE_TYPE_CODE_1'].isin([str(v) for v in vehicles])]
        print(f"After vehicle filter: {df.shape}")
    
    if persons:
        df = df[df['PERSON_TYPE'].isin([str(p) for p in persons])]
        print(f"After person filter: {df.shape}")
    
    if genders:
        df = df[df['PERSON_SEX'].isin([str(g) for g in genders])]
        print(f"After gender filter: {df.shape}")
    
    if contributing_factors:
        df = df[df['CONTRIBUTING_FACTOR_VEHICLE_1'].isin([str(c) for c in contributing_factors])]
        print(f"After contributing factor filter: {df.shape}")
    
    if injury_types and 'PERSON_INJURY' in df.columns:
        df = df[df['PERSON_INJURY'].isin([str(i) for i in injury_types])]
        print(f"After injury type filter: {df.shape}")
    
    # Calculate KPIs
    total_crashes = len(df)
    total_injuries = int(df['NUMBER_OF_PERSONS_INJURED'].sum())
    total_fatalities = int(df['NUMBER_OF_PERSONS_KILLED'].sum())
    
    # Most dangerous borough
    if len(df) > 0:
        borough_danger = df.groupby('BOROUGH')['NUMBER_OF_PERSONS_KILLED'].sum()
        borough_danger = borough_danger[borough_danger.index != 'Unknown']
        most_dangerous = borough_danger.idxmax() if len(borough_danger) > 0 and borough_danger.max() > 0 else "N/A"
    else:
        most_dangerous = "N/A"
    
    # 1. Borough Bar Chart
    if len(df) > 0:
        borough_counts = df['BOROUGH'].value_counts().head(10)
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
    
    # 3. Vehicle Type Pie Chart
    if len(df) > 0:
        vehicle_counts = df['VEHICLE_TYPE_CODE_1'].value_counts().head(8)
        # Filter out Unknown
        vehicle_counts = vehicle_counts[vehicle_counts.index != 'Unknown']
        
        pie_fig = px.pie(
            values=vehicle_counts.values,
            names=vehicle_counts.index,
            title="Vehicle Type Distribution (Top 8)",
            hole=0.3  # Creates a donut chart
        )
        pie_fig.update_traces(textposition='inside', textinfo='percent+label')
    else:
        pie_fig = go.Figure()
        pie_fig.add_annotation(text="No data available", x=0.5, y=0.5, showarrow=False)
    
    # 4. Contributing Factor Bar Chart
    if len(df) > 0:
        factor_counts = df['CONTRIBUTING_FACTOR_VEHICLE_1'].value_counts().head(10)
        # Filter out Unknown and Unspecified
        factor_counts = factor_counts[~factor_counts.index.isin(['Unknown', 'UNSPECIFIED'])]
        
        factor_bar_fig = px.bar(
            x=factor_counts.values,
            y=factor_counts.index,
            title="Top Contributing Factors",
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
    
    # 5. Gender Comparison Chart
    if len(df) > 0 and 'PERSON_SEX' in df.columns:
        # Filter out Unknown values
        gender_df = df[df['PERSON_SEX'].isin(['M', 'F'])]
        
        if len(gender_df) > 0:
            # Calculate stats by gender
            gender_stats = gender_df.groupby('PERSON_SEX').agg({
                'COLLISION_ID': 'count',
                'NUMBER_OF_PERSONS_INJURED': 'sum',
                'NUMBER_OF_PERSONS_KILLED': 'sum'
            }).reset_index()
            
            gender_stats.columns = ['Gender', 'Total Involved', 'Injuries', 'Fatalities']
            gender_stats['Gender'] = gender_stats['Gender'].replace({'M': 'Male', 'F': 'Female'})
            
            # Create grouped bar chart
            gender_fig = go.Figure()
            gender_fig.add_trace(go.Bar(
                name='Total Involved',
                x=gender_stats['Gender'],
                y=gender_stats['Total Involved'],
                marker_color='lightblue'
            ))
            gender_fig.add_trace(go.Bar(
                name='Injuries',
                x=gender_stats['Gender'],
                y=gender_stats['Injuries'],
                marker_color='orange'
            ))
            gender_fig.add_trace(go.Bar(
                name='Fatalities',
                x=gender_stats['Gender'],
                y=gender_stats['Fatalities'],
                marker_color='red'
            ))
            
            gender_fig.update_layout(
                title='Gender Comparison: Involvement, Injuries & Fatalities',
                xaxis_title='Gender',
                yaxis_title='Count',
                barmode='group',
                height=400
            )
        else:
            gender_fig = go.Figure()
            gender_fig.add_annotation(text="No gender data available", x=0.5, y=0.5, showarrow=False)
    else:
        gender_fig = go.Figure()
        gender_fig.add_annotation(text="No gender data available", x=0.5, y=0.5, showarrow=False)
    
    # 6. Map (sample data for performance)
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
    
    print(f"=== Results ===")
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
        gender_fig,
        map_fig
    )

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)