import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import geopandas as gpd
import numpy as np
import warnings

# Suppress specific warnings
warnings.simplefilter(action='ignore', category=UserWarning)

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Load the data
forest_data = gpd.read_file("data/FADM_PROV_FOREST_simplified.geojson")
wildfire_data = gpd.read_file("data/PROT_CURRENT_FIRE_PNTS_SP_simplified.geojson")

# Fill missing Termination_Date with "still active" if any are missing
wildfire_data['Termination_Date'].fillna("still active", inplace=True)

# Map FIRESTATUS to colors
status_color_map = {
    "Out": "green",
    "Under Control": "yellow",
    "Being Held": "orange",
    "Out of Control": "red",
}
wildfire_data['color'] = wildfire_data['FIRESTATUS'].map(status_color_map)

# Normalize the SIZE_HA column to control marker sizes
size_ha_log = np.log1p(wildfire_data['SIZE_HA'])
scaled_size = 6 + (size_ha_log - size_ha_log.min()) / (size_ha_log.max() - size_ha_log.min() + 1) * 9

# Create the main map figure
def create_forest_map():
    fig = go.Figure()
    fig.add_trace(go.Scattermapbox(
        lat=wildfire_data.geometry.y,
        lon=wildfire_data.geometry.x,
        mode='markers',
        marker=dict(size=scaled_size, color=wildfire_data['color']),
        hoverinfo='skip',
        name='Wildfire Locations'
    ))
    fig.add_trace(go.Choroplethmapbox(
        geojson=forest_data.geometry.__geo_interface__,
        locations=forest_data.index,
        z=[1] * len(forest_data),
        colorscale=[(0, "green"), (1, "green")],
        showscale=False,
        marker_opacity=0.5,
        name="Forest Map",
        hovertext=forest_data.apply(
            lambda row: f"Forest: {row['Forest_Name']}<br>Area: {round(row['Forest_Area']/1000000, 2)} sq km", axis=1),
        hoverinfo='text'
    ))
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=4.3,
        mapbox_center={"lat": 53.7267, "lon": -125.6476},
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        title="Forest and Wildfire Data Visualization in BC",
        height=800
    )
    return fig

def create_bar_plot(data, category, x_title, selected_forest=None):
    if selected_forest:
        data = data[data['Forest_Name'] == selected_forest]
    counts = data[category].value_counts().reset_index()
    counts.columns = [category, 'Count']
    bar_fig = go.Figure(data=[
        go.Bar(x=counts[category], y=counts['Count'], marker_color=counts[category].map(status_color_map))
    ])
    bar_fig.update_layout(
        xaxis_title=x_title,
        yaxis_title="Number of Fires",
        margin={"r": 0, "t": 30, "l": 30, "b": 30},
        height=300
    )
    return bar_fig

app.layout = html.Div([
    html.Div([
        html.H1("Forest and Wildfire Dashboard"),
        html.P("Explore wildfire incidents and forest coverage in British Columbia. Use this dashboard to understand the distribution and characteristics of wildfires across different forest regions."),
    ], style={'width': '100%', 'display': 'inline-block', 'verticalAlign': 'top', 'textAlign': 'center', 'padding': '10px'}),
    
    html.Div([
        dcc.Graph(id='forest-map', figure=create_forest_map(), style={'width': '100%', 'height': '100%'}),
    ], style={'width': '50%', 'height': '100%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),

    html.Div([
        html.Div([
            dcc.Graph(id='selected-forest-map', style={'width': '100%', 'height': '50%'}),
        ], style={'width': '100%', 'height': '40%'}),
        
        html.Div([
            dcc.Graph(id='fire-status-bar', style={'width': '50%', 'display': 'inline-block', 'height': '60%'}),
            dcc.Graph(id='fire-cause-bar', style={'width': '50%', 'display': 'inline-block', 'height': '60%'}),
        ], style={'width': '100%', 'display': 'flex', 'height': '60%'}),
    ], style={'width': '40%', 'height': '100%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),

    html.Footer([
        html.Div("Created by HanChen Wang, 2024", style={'text-align': 'center', 'padding': '10px', 'font-size': '14px', 'color': '#888'}),
    ], style={'width': '100%', 'background-color': '#f1f1f1', 'padding': '10px', 'position': 'fixed', 'bottom': 0}),
])

@app.callback(
    [Output('fire-status-bar', 'figure'),
     Output('fire-cause-bar', 'figure'),
     Output('selected-forest-map', 'figure')],
    [Input('forest-map', 'clickData'),
     Input('forest-map', 'hoverData')]
)
def update_plots(clickData, hoverData):
    selected_forest = None
    if clickData:
        selected_forest = clickData['points'][0]['hovertext'].split("<br>")[0].split(": ")[1]
    elif hoverData:
        selected_forest = hoverData['points'][0]['hovertext'].split("<br>")[0].split(": ")[1]
    
    fire_status_bar = create_bar_plot(wildfire_data, 'FIRESTATUS', "Fire Status", selected_forest)
    fire_cause_bar = create_bar_plot(wildfire_data, 'FIRE_CAUSE', "Cause of Fire", selected_forest)
    
    forest_zoomed_map = go.Figure()
    if selected_forest:
        selected_forest_data = forest_data[forest_data['Forest_Name'] == selected_forest]
        selected_wildfire_data = wildfire_data[wildfire_data['Forest_Name'] == selected_forest]
        
        if not selected_wildfire_data.empty:
            size_ha_log = np.log1p(selected_wildfire_data['SIZE_HA'])
            scale_size = 6 + (size_ha_log - size_ha_log.min()) / (size_ha_log.max() - size_ha_log.min() + 1) * 20
        else:
            scale_size = [8] * len(selected_wildfire_data)
        
        forest_zoomed_map.add_trace(go.Choroplethmapbox(
            geojson=selected_forest_data.geometry.__geo_interface__,
            locations=selected_forest_data.index,
            z=[1] * len(selected_forest_data),
            colorscale=[(0, "green"), (1, "green")],
            showscale=False,
            marker_opacity=0.5,
            name="Selected Forest",
            hovertext=selected_forest_data.apply(
                lambda row: f"Forest: {row['Forest_Name']}<br>Area: {round(row['Forest_Area']/1000000, 2)} sq km", axis=1),
            hoverinfo='text'
        ))
        
        forest_zoomed_map.add_trace(go.Scattermapbox(
            lat=selected_wildfire_data.geometry.y,
            lon=selected_wildfire_data.geometry.x,
            mode='markers',
            marker=dict(size=scale_size, color=selected_wildfire_data['color']),
            text=selected_wildfire_data.apply(
                lambda row: f"Status: {row['FIRESTATUS']}<br>"
                            f"Size: {row['SIZE_HA']} hectares<br>"
                            f"Cause: {row['FIRE_CAUSE']}<br>"
                            f"Ignition: {row['Ignition_Date']}<br>"
                            f"Termination: {row['Termination_Date']}", axis=1),
            hoverinfo='text',
            name='Wildfire Locations'
        ))
        
        forest_zoomed_map.update_layout(
            mapbox_style="open-street-map",
            mapbox_zoom=5.5,
            mapbox_center={"lat": selected_forest_data.geometry.centroid.y.values[0],
                           "lon": selected_forest_data.geometry.centroid.x.values[0]},
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            height=600
        )

    return fire_status_bar, fire_cause_bar, forest_zoomed_map

if __name__ == '__main__':
    app.run_server(debug=True)
