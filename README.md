# Forest and Wildfire Dashboard

## Project Overview

The Forest and Wildfire Dashboard is an interactive web application built with Python Dash and Plotly to visualize and analyze wildfire incidents and forest coverage in British Columbia (BC), Canada. This dashboard allows users to explore wildfire data, view forest coverage, and analyze fire status and causes across different forest regions.

### Features
- Interactive map showing wildfire locations and forest boundaries.
- Date range slider to filter wildfires by ignition and termination dates.
- Detailed bar plots showing the distribution of fire statuses and causes.
- Dynamic updates based on user interactions with the map and date slider.

## Installation

### Prerequisites

Ensure you have Python 3.7 or later installed. You will also need to install the following Python packages:
- Dash
- Plotly
- Geopandas
- Pandas
- NumPy
- Dash Bootstrap Components

You can install the required packages using pip:

```bash
pip install dash plotly geopandas pandas numpy dash-bootstrap-components
```

### Data Files

Download the necessary data files and place them in a `data` directory within your project. The files required are:
- `FADM_PROV_FOREST_simplified.geojson`: Forest data.
- `PROT_CURRENT_FIRE_PNTS_SP_simplified.geojson`: Wildfire data.

You can download these files from [BC Data Catalogue](https://catalogue.data.gov.bc.ca/dataset).

## Usage

To run the dashboard, execute the following Python script:

```python
python app.py
```

This will start a local server, and you can view the dashboard in your web browser at `http://127.0.0.1:8050`.

### How It Works

1. **Main Map**: Displays the forest and wildfire data on an interactive map. Wildfire locations are marked with different colors based on their status.
2. **Focused Map**: Allows users to select a date range and interact with the map to view detailed information about a specific forest. The focused map updates with selected forest data, fire status, and cause.
3. **Date Slider**: Filter the wildfire data based on the selected date range to analyze incidents within that period.
4. **Bar Plots**: Show the distribution of fire statuses and causes based on the selected date range and forest region.

## Data Sources

- **Forest Data**: [BC Forest Data](https://catalogue.data.gov.bc.ca/dataset/fadm-prov-forest-simplified)
- **Wildfire Data**: [BC Wildfire Data](https://catalogue.data.gov.bc.ca/dataset/prot-current-fire-pnts-sp-simplified)

## Acknowledgments

This project was created by HanChen Wang in 2024. The data used is publicly available and provided by the Government of British Columbia.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.