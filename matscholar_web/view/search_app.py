import dash_html_components as html
import dash_materialsintelligence as dmi
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

VALID_FILTERS = ["material", "property", "application", "descriptor", "characterization", "synthesis", "phase"]

def search_html():
    return html.Div([
        html.Div(dcc.Input(
            id="search_input",
            type="text",
            autofocus=True,
            placeholder="Text search...",
            style={"width": "100%"}),
            style={"display": "table-cell", "width": "100%"}),
        html.Div(html.Button(
            "Search",
            className="button-search",
            id="search_btn"),
            style={"display": "table-cell", "verticalAlign": "top", "paddingLeft": "10px"})],
            className="row", style={"display": "table", "marginTop": "10px"}
        )

def filters_html(label, placeholder):
    return html.Div([
        html.Label('Add filters for {}'.format(label)),
         dcc.Dropdown(
            options=[
                {'label': 'sputtering', 'value': 'sputtering'},
                {'label': 'sintering', 'value': 'sintering'},
                {'label': 'MOCVD', 'value': 'MOCVD'}
            ],
        multi=True,
        placeholder=placeholder
        ),
    ],
    style={'width':'50%'}
)

def serve_layout():
    return html.Div([search_html(),
                     html.Div(html.Button(
                         'Material',
                         id='filters-btn'
                     )),
                     html.Div("", id='filters')])

def bind(app):
    @app.callback(
        Output('filters', 'children'),
        [Input('filters-btn', 'n_clicks')])
    def show_filters(n_clicks):
        if n_clicks is not None:
            return filters_html('material', 'Al2O3, alumina ...')


# def serve_layout(path=None):
#     if path is not None and len(path) > len("/search"):
#         path = path[len("/search")+1::]
#         path = path.replace("%20", " ")
#     options = []
#     value = options
#     if path is not None:
#         filter_value_material = path.split("/")
#         if len(filter_value_material) == 3:
#             options = [{'label': 'material:' + filter_value_material[2],
#                         'value': 'material:' + filter_value_material[2]},
#                        {'label': filter_value_material[0] + ':' + filter_value_material[1],
#                         'value': filter_value_material[0] + ':' + filter_value_material[1]}]
#             value = options
#     return html.Div([search_html(),
#         html.Div(dmi.DropdownCreatable(
#         options=options,
#         multi=True,
#         promptText="Add filter ",
#         className="search-filters",
#         placeholder="filter:value1,value2",
#         value=value,
#         id='search_filters'),
#     ),
#     html.Div(
#         'Valid filters: ' + ', '.join(VALID_FILTERS),
#         style={"color": "grey", "padding": "10px 1px", "fontSize": "10pt"},
#         className="row"),
#     html.Div(html.Button(
#         "Generate summary",
#         className="button-search",
#         id="search_btn"),
#         style={"display": "table-cell", "verticalAlign": "top", "paddingLeft": "10px"}),
#     html.Div("", id="search_results", className="row"),
#
#     ])
