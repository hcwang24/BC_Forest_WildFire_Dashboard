import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import geopandas as gpd
import pandas as pd

# Load the simplified GeoDataFrame for forests
forest_data_cleaned = gpd.read_file("data/FADM_PROV_FOREST_simplified.geojson")

# Load the wildfire data
wildfire_data = gpd.read_file("data/PROT_CURRENT_FIRE_PNTS_SP")
wildfire_data = wildfire_data.to_crs("EPSG:4326")  # Ensure same CRS as forest data

# Aggregate forest areas by region
region_area = forest_data_cleaned.groupby('PRV_FRST_N')['AREA_SQM'].sum().sort_values(ascending=True)
region_area_df = region_area.reset_index()

# Create the initial map figure for forests
map_fig = px.choropleth_mapbox(
    forest_data_cleaned,
    geojson=forest_data_cleaned.geometry.__geo_interface__,
    locations=forest_data_cleaned.index,
    hover_name="PRV_FRST_N",
    mapbox_style="open-street-map",
    zoom=4.3,
    center={"lat": 53.7267, "lon": -125.6476},
    opacity=0.5,
    color_discrete_sequence=["green"] * len(forest_data_cleaned)
)

map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=800)

# Create the initial bar plot figure with reversed order
bar_fig = px.bar(
    region_area_df,
    x='AREA_SQM',
    y='PRV_FRST_N',
    orientation='h',
    title='Total Forest Area by Region',
    labels={'PRV_FRST_N': 'Forest Name', 'AREA_SQM': 'Area (square meters)'}
)
bar_fig.update_layout(xaxis_title="Area (square meters)", yaxis_title="Forest Name", height=800)

# Create the initial map figure for wildfires
fire_plot_fig = px.scatter_mapbox(
    wildfire_data,
    lat=wildfire_data.geometry.y,
    lon=wildfire_data.geometry.x,
    color='FIRESTATUS',  # Color by fire status (active or not)
    color_discrete_map={'Active': 'red', 'Out': 'gray'},
    hover_name='FIRE_NO',
    mapbox_style="open-street-map",
    zoom=4,
    center={"lat": 53.7267, "lon": -125.6476},
    opacity=0.7
)
fire_plot_fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=800,
    coloraxis_colorbar=dict(title=None, tickvals=[], ticks='')  # Remove color legend
)

# Create the Dash app
app = dash.Dash(__name__)

# Layout: Header, description, and the three graphs
app.layout = html.Div([
    html.H1("Forest and Wildfire Visualization in British Columbia"),
    html.P("This dashboard visualizes forest areas by region and current wildfire locations. Click on a forest polygon to highlight the corresponding bar."),
    
    # Text section to display the selected forest info (static message)
    html.Div(id='selected-info', style={'margin-top': '20px', 'font-weight': 'bold'},
             children="Click on a forest polygon to see more details here."),
    
    # Horizontal layout for forest and bar plots, with the wildfire plot below
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
    
    # Static plot for wildfire data
    dcc.Loading(
        id="loading-fire-plot",
        type="circle",
        children=dcc.Graph(id='fire-plot', figure=fire_plot_fig)
    )
])

# Callback to update the bar plot based on map click
@app.callback(
    Output('bar-plot', 'figure'),
    Output('selected-info', 'children'),
    Input('map-plot', 'clickData')
)
def update_bar_plot(clickData):
    # Default bar colors (all bars are blue)
    colors_bar = ["blue"] * len(region_area_df)
    selected_text = "Click on a forest polygon to see more details here."

    if clickData is not None:
        selected_region = clickData['points'][0]['hovertext']  # Get the region clicked on the map

        # Update bar plot colors
        if selected_region in region_area_df['PRV_FRST_N'].values:
            selected_bar_index = region_area_df[region_area_df['PRV_FRST_N'] == selected_region].index[0]
            colors_bar = ["red" if i == selected_bar_index else "blue" for i in range(len(region_area_df))]
        
            # Update text with selected forest info
            selected_forest = forest_data_cleaned[forest_data_cleaned['PRV_FRST_N'] == selected_region]
            if not selected_forest.empty:
                selected_forest = selected_forest.iloc[0]
                forest_name = selected_forest['PRV_FRST_N']
                forest_area = selected_forest['AREA_SQM']
                forest_location = selected_forest.geometry.centroid
                selected_text = f"Selected Forest: {forest_name}, Area: {forest_area:.2f} sqm, Location: ({forest_location.y:.4f}, {forest_location.x:.4f})"

    # Create updated bar plot figure
    bar_fig_updated = px.bar(
        region_area_df,
        x='AREA_SQM',
        y='PRV_FRST_N',
        orientation='h',
        title='Total Forest Area by Region',
        labels={'PRV_FRST_N': 'Forest Name', 'AREA_SQM': 'Area (square meters)'}
    )
    bar_fig_updated.update_layout(xaxis_title="Area (square meters)", yaxis_title="Forest Name", height=800)
    bar_fig_updated.update_traces(marker_color=colors_bar)
    
    return bar_fig_updated, selected_text

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
