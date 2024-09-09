import dash
from dash import dcc
from dash import html
import plotly.express as px
import geopandas as gpd

# Initialize the Dash app
app = dash.Dash(__name__)

# Import data
forest_data = gpd.read_file("data/FADM_PROV_FOREST")
forest_data = forest_data.to_crs("EPSG:4326")

# Map visualization using Plotly
fig = px.choropleth(forest_data, geojson=forest_data.geometry, locations=forest_data.index, 
                    color="AREA_SQM", hover_name="PRV_FRST_N")

# Layout of the app
app.layout = html.Div([
    dcc.Graph(id='forest-map', figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
