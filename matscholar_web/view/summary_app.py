import dash_html_components as html
import dash_materialsintelligence as dmi

VALID_FILTERS = ["material", "property", "application", "descriptor", "characterization", "synthesis", "phase"]

def serve_layout(path=None):
    if path is not None and len(path) > len("/search"):
        path = path[len("/search")+1::]
        path = path.replace("%20", " ")
    options = []
    value = options
    if path is not None:
        filter_value_material = path.split("/")
        if len(filter_value_material) == 3:
            options = [{'label': 'material:' + filter_value_material[2],
                        'value': 'material:' + filter_value_material[2]},
                       {'label': filter_value_material[0] + ':' + filter_value_material[1],
                        'value': filter_value_material[0] + ':' + filter_value_material[1]}]
            value = options
    return html.Div([html.Div(dmi.DropdownCreatable(
        options=options,
        multi=True,
        promptText="Add filter ",
        className="search-filters",
        placeholder="filter:value1,value2",
        value=value,
        id='search_filters'),
    ),
    html.Div(
        'Valid filters: ' + ', '.join(VALID_FILTERS),
        style={"color": "grey", "padding": "10px 1px", "fontSize": "10pt"},
        className="row"),
    html.Div(html.Button(
        "Generate summary",
        className="button-search",
        id="search_btn"),
        style={"display": "table-cell", "verticalAlign": "top", "paddingLeft": "10px"}),
    html.Div("", id="search_results", className="row")],
    )
