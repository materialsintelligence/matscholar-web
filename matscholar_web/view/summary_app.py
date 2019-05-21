import dash_html_components as html
import dash_core_components as dcc
from matscholar_web.view.search_app import search_filter_box_html

VALID_FILTERS = ["material", "property", "application", "descriptor", "characterization", "synthesis", "phase"]

def search_filter_box_html(label):
    placeholders = {"material": "PbTe, graphite,...",
                    "property": "dielectric constant, melting point,...",
                    "application": "cathode, catalyst,...",
                    "descriptor": "thin film, nanoparticle,...",
                    "characterization": "photoluminescence, x-ray diffraction,...",
                    "synthesis":"sol - gel, firing,...",
                    "phase": "perovskite, wurtzite,..."}
    textbox = html.Div([html.Label('{}:'.format(label)),
        dcc.Input(
            id="{}-summary".format(label),
            type="text",
            autofocus=True,
            placeholder=placeholders[label],
            style={"width": "100%"})
        ],
        style={'padding': 5}
        )
    return textbox

def serve_layout():
    filter_boxes = html.Div([html.Div(search_filter_box_html(label), style={"width": "25%"})
                             for label in VALID_FILTERS], style={"width:":"100%",
                                                                 "display": "flex",
                                                                 "flex-direction": "row",
                                                                 "flex-wrap": "wrap"})
    return html.Div([filter_boxes,
                     html.Div(html.Button(
                              "Generate summary",
                              className="button-search",
                              id="summary-btn"),
                              style={"display": "table-cell", "verticalAlign": "top", "paddingLeft": "10px"}),
                    html.Div("", id="summary-results", className="row")]
                    )
