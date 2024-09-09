import dash
from dash import dcc, html
import plotly.express as px
import geopandas as gpd
import pandas as pd

# Load the simplified GeoDataFrame
forest_data_cleaned = gpd.read_file("data/FADM_PROV_FOREST_simplified.geojson")

# Aggregate forest areas by region
region_area = forest_data_cleaned.groupby('PRV_FRST_N')['AREA_SQM'].sum().sort_values(ascending=False)
region_area_df = region_area.reset_index()

# Create the Dash app
app = dash.Dash(__name__)

# Create the map figure
map_fig = px.choropleth_mapbox(
    forest_data_cleaned,
    geojson=forest_data_cleaned.geometry.__geo_interface__,
    locations=forest_data_cleaned.index,
    hover_name="PRV_FRST_N",
    mapbox_style="open-street-map",
    zoom=4.2,
    center={"lat": 53.7267, "lon": -125.6476},
    opacity=0.5,
    color_discrete_sequence=["green"] * len(forest_data_cleaned)
)
map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800)

# Create the bar plot figure with reversed order
bar_fig = px.bar(
    region_area_df,
    x='AREA_SQM',
    y='PRV_FRST_N',
    orientation='h',
    title='Total Forest Area by Region',
    labels={'PRV_FRST_N': 'Forest Name', 'AREA_SQM': 'Area (square meters)'},
    category_orders={'PRV_FRST_N': region_area_df['PRV_FRST_N'][::-1]}  # Reverse the y-axis order
)
bar_fig.update_layout(xaxis_title="Area (square meters)", yaxis_title="Forest Name", height=800)

# Layout: Header, description, and the two graphs side by side
app.layout = html.Div([
    html.H1("Forest Area Visualization in British Columbia"),
    html.P("This dashboard visualizes forest areas by region. Click on a forest polygon to highlight it on the map."),
    
    # Text section to display the selected forest info (static message)
    html.Div(id='selected-info', style={'margin-top': '20px', 'font-weight': 'bold'},
             children="Click on a forest polygon to see more details here."),
    
    # Horizontal layout for graphs with loading messages
    html.Div([
        dcc.Loading(
            id="loading-map-plot",
            type="circle",
            children=dcc.Graph(id='map-plot', figure=map_fig)
        ),
        dcc.Loading(
            id="loading-bar-plot",
            type="circle",
            children=dcc.Graph(id='bar-plot', figure=bar_fig)
        )
    ], style={'display': 'flex', 'flex-direction': 'row'}),  # Horizontal layout
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
