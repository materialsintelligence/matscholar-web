import dash_html_components as html
import dash_core_components as dcc
from matscholar_web.view.search_app import search_filter_box_html
from dash_elasticsearch_autosuggest import ESAutosuggest
from os import environ


VALID_FILTERS = ["material", "property", "application", "descriptor", "characterization", "synthesis", "phase"]
ES_field_dict = {"material": "materials","property":"properties","application":"applications","descriptor":"descriptors","characterization":"characterization methods","synthesis":"synthesis methods","phase":"structure phase labels"}


def search_filter_box_html(label):
    placeholders = {"material": "PbTe, graphite,...",
                    "property": "dielectric constant, melting point,...",
                    "application": "cathode, catalyst,...",
                    "descriptor": "thin film, nanoparticle,...",
                    "characterization": "photoluminescence, x-ray diffraction,...",
                    "synthesis":"sol - gel, firing,...",
                    "phase": "perovskite, wurtzite,..."}
    textbox = html.Div([html.Label('{}:'.format(label)),
         ESAutosuggest(
            fields=['original','normalized'],
            endpoint="https://7092c099e3d606dec7363473782f6e83.us-west-1.aws.found.io:9243/"+ES_field_dict[label]+"/_search",
            defaultField='original',
            id=label+"-summary",
            placeholder=placeholders[label],
            authUser=environ['ELASTIC_USER'],
            authPass=environ['ELASTIC_PASS'],
            searchField="original.edgengram",
            value="")
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
                    dcc.Loading(id="loading-1", children=[html.Div("", id="summary-results", className="row")])]
                    )
