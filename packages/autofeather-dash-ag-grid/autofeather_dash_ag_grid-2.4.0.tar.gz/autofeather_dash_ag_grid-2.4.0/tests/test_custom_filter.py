from dash import Dash, html
import dash_ag_grid as dag
import plotly.express as px
import pandas as pd

from . import utils


df = px.data.election()
default_display_cols = ["district_id"]
other_cols = ["district", "winner"]

df = pd.concat([df, pd.DataFrame({"district": ["test"]})])


def test_fi002_custom_filter(dash_duo):
    app = Dash(__name__)

    app.layout = html.Div(
        [
            dag.AgGrid(
                id="grid",
                rowData=df.to_dict("records"),
                columnDefs=[
                    {
                        "headerName": col.capitalize(),
                        "field": col,
                        "filterParams": {"function": "filterParams()"},
                        "filter": "agNumberColumnFilter",
                    }
                    for col in default_display_cols
                ]
                + [
                    {
                        "headerName": col.capitalize(),
                        "field": col,
                        "filterParams": {
                            "filterOptions": ["contains", "startsWith", "endsWith"],
                            "defaultOption": "endsWith",
                        },
                        "filter": True,
                    }
                    for col in other_cols
                ],
                defaultColDef={"floatingFilter": True},
            )
        ]
    )

    dash_duo.start_server(app)

    grid = utils.Grid(dash_duo, "grid")

    grid.wait_for_cell_text(0, 1, "101-Bois-de-Liesse")

    grid.set_filter(0, "12")

    grid.wait_for_cell_text(0, 1, "11-Sault-au-Récollet")
    grid.wait_for_rendered_rows(2)

    grid.set_filter(0, "")
    grid.wait_for_cell_text(0, 1, "101-Bois-de-Liesse")

    grid.set_filter(1, "t")
    grid.set_filter(2, "e")
    grid.wait_for_cell_text(0, 1, "11-Sault-au-Récollet")
    grid.wait_for_rendered_rows(8)

def test_fi003_custom_filter(dash_duo):
    app = Dash(__name__)

    df = pd.read_json('https://www.ag-grid.com/example-assets/olympic-winners.json', convert_dates=False)

    rowData = df.to_dict('records')

    columnDefs = [
        {'field': 'age', 'filter': 'agNumberColumnFilter'},
        {'field': 'country', 'minWidth': 150},
        {'field': 'year', 'filter': {'function': 'YearFilter'}},
        {
            'field': 'date',
            'minWidth': 130,
            'filter': 'agDateColumnFilter',
        },
        {'field': 'sport'},
        {'field': 'gold', 'filter': 'agNumberColumnFilter'},
        {'field': 'silver', 'filter': 'agNumberColumnFilter'},
        {'field': 'bronze', 'filter': 'agNumberColumnFilter'},
        {'field': 'total', 'filter': 'agNumberColumnFilter'},
    ]

    defaultColDef = {
        'editable': True,
        'sortable': True,
        'flex': 1,
        'minWidth': 100,
        'filter': True,
        'resizable': True,
    }

    app.layout = html.Div(
        [
            dag.AgGrid(
                id="grid",
                columnDefs=columnDefs,
                rowData=rowData,
                defaultColDef=defaultColDef
            ),
        ]
    )

    dash_duo.start_server(app)

    grid = utils.Grid(dash_duo, "grid")

    grid.wait_for_cell_text(0, 0, "23")

    dash_duo.find_element('.ag-header-cell[aria-colindex="3"] .ag-icon-menu').click()

    dash_duo.find_element('.ag-filter label:nth-child(2)').click()

    grid.wait_for_cell_text(0, 0, "27")

    dash_duo.find_element('.ag-filter label:nth-child(1)').click()

    grid.wait_for_cell_text(0, 0, "23")
