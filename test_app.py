import pytest
from dash.testing.application_runners import import_app

# Test to check if the Dash app's forest map is rendered
@pytest.mark.parametrize("app", ["app"], indirect=True)
def test_forest_map_rendered(dash_duo):
    # Start the Dash app
    app = import_app('app')

    # Start the Dash app in a separate process
    dash_duo.start_server(app)

    # Wait for the forest map to render (graph with id "forest-map")
    dash_duo.wait_for_element_by_id("forest-map", timeout=10)

    # Check if the forest map is present in the page
    forest_map = dash_duo.find_element("#forest-map")
    assert forest_map is not None, "The forest map was not rendered on the page."

    # Optionally, you can also take a screenshot to verify the visual output
    dash_duo.percy_snapshot("forest_map_rendered")
