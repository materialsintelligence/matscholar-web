import dash_html_components as html
import dash_core_components as dcc
from matscholar_web.static.periodic_table.periodic_table import build_periodic_table


def graph():
    return html.Div([
        dcc.Graph(
            id='heatmap',
            figure=build_periodic_table()
        )
    ], style={"padding-top": "-80px"})

def serve_layout():
    return html.Div([
        html.Div([html.Label("Enter a property/application to find associated materials:"),
                dcc.Input(
                    id="material_search_input",
                    type="text",
                    autofocus=True,
                    placeholder="E.g., ferroelectric, Li-ion batteries",
                    style={"width": "95%"})],
            style={"width": "500px", "display": "inline-block"}),
        html.Div([html.Label("Element filters:"),
                dcc.Input(
                    id="element_filters_input",
                    type="text",
                    autofocus=True,
                    placeholder="E.g., O, -Pb",
                    value=None,
                    style={"width": "50%"})],
            style={"width": "250px", "display": "inline-block"}),
        html.Div(["Include/exclude?",
                  dcc.RadioItems(id="include-radio",
                                 options=[
                                     {'label': "include", 'value': "include"},
                                     {"label": "exclude", "value": "exclude"}
                                 ],
                                 value='include',
                                 labelStyle={'display': 'inline-block'}
                                 ),
                  html.Div(id="hidden-div", style={"display": None})],
                 style={"padding-top": "30px"}),
        html.Div(children=graph(), style={"width": "90%"}, id="periodic-table"),
    html.Div(
        html.Button(
            "Material Search",
            className="button-search",
            id="material_search_btn"),
    ),
    dcc.Loading(id="loading-1", children=[html.Div(id="material_search_output")])])
