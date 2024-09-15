# BC Forest and Wildfire Dashboard

## Project Overview

The **BC Forest and Wildfire Dashboard** is an interactive web application developed using Python Dash and Plotly. It provides a comprehensive visualization and analysis tool for wildfire incidents and forest coverage in British Columbia (BC), Canada. Users can explore wildfire data, examine forest boundaries, and analyze fire statuses and causes across different regions.

<img src="demo/demo.png" width="1000" height="500"/>

### Features

- **Interactive Map**: Visualizes wildfire locations and forest boundaries.
- **Date Range Slider**: Filters wildfires based on ignition and termination dates.
- **Dynamic Updates**: Updates the dashboard based on user interactions with the map and date slider.
- **Detailed Analysis**: Bar plots showing the distribution of fire statuses and causes.

## Deployment

This dashboard is deployed and accessible online at: [BC Forest and Wildfire Dashboard](https://bc-forest-wildfire-dashboard.onrender.com)

Visit the link to explore forest coverage and wildfire incidents in British Columbia.

## Installation

### Prerequisites

Make sure you have Python 3.7 or later installed. You will need to install the following Python packages:
- Dash
- Plotly
- Geopandas
- Pandas
- NumPy
- Dash Bootstrap Components

Install the required packages using pip:

```bash
pip install dash plotly geopandas pandas numpy dash-bootstrap-components
```

### Data Files

Download the necessary data files and place them in a `data` directory within your project. The required files are:
- `FADM_PROV_FOREST.geojson`: Forest data.
- `PROT_CURRENT_FIRE_PNTS_SP.geojson`: Wildfire data.

Download these files from the [BC Data Catalogue](https://catalogue.data.gov.bc.ca/dataset).

## Usage

To run the dashboard, execute the following Python script:

```bash
python app.py
```

This will start a local server, and you can access the dashboard in your web browser at `http://127.0.0.1:8050`.

### How It Works

1. **Main Map**: Displays both forest and wildfire data. Wildfire locations are color-coded based on their status.
2. **Focused Map**: Allows users to select a date range and interact with the map to view detailed information about a specific forest. Updates include selected forest data, fire status, and cause.
3. **Date Slider**: Enables filtering of wildfire data based on the selected date range.
4. **Bar Plots**: Show the distribution of fire statuses and causes based on the selected date range and forest region.

## Data Sources

- **Forest Data**: [BC Forest Data](https://catalogue.data.gov.bc.ca/dataset/fadm-provincial-forest)
- **Wildfire Data**: [BC Wildfire Data](https://catalogue.data.gov.bc.ca/dataset/bc-wildfire-fire-locations-current)

## Acknowledgments

This project was created by HanChen Wang in 2024. The data used is publicly available and provided by the Government of British Columbia.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
