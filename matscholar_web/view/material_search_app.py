import dash_html_components as html
import dash_core_components as dcc

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
                    style={"width": "50%"})],
            style={"width": "250px", "display": "inline-block"}),
    html.Div(
        html.Button(
            "Material Search",
            className="button-search",
            id="material_search_btn"),
    ),
    html.Div(id="material_search_output")])
