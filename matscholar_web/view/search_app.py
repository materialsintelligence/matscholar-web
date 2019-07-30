import dash_html_components as html
import dash_core_components as dcc
from dash_elasticsearch_autosuggest import ESAutosuggest
from os import environ
from collections import defaultdict

#Entity categories
valid_filters = ["material", "property", "application", "descriptor", "characterization", "synthesis", "phase"]
#Corresponding elasticsearch indices for entity categories
ES_field_dict = {"material": "materials","property":"properties","application":"applications","descriptor":"descriptors","characterization":"characterization_methods","synthesis":"synthesis_methods","phase":"structure_phase_labels"}

def search_filter_box_html(label, filters=None):
    placeholders = {"material": "PbTe, graphite,...",
                    "property": "dielectric constant, melting point,...",
                    "application": "cathode, catalyst,...",
                    "descriptor": "thin film, nanoparticle,...",
                    "characterization": "photoluminescence, x-ray diffraction,...",
                    "synthesis":"sol - gel, firing,...",
                    "phase": "perovskite, wurtzite,..."}
    if not filters:
        value = ""
    else:
        value = ",".join(filters) if len(filters) > 1 else filters[0]
    textbox = html.Div([html.Label('{}:'.format(label)),
        ESAutosuggest(
            fields=['original','normalized'],
            endpoint=environ['ELASTIC_HOST']+"/"+ES_field_dict[label]+"/_search",
            defaultField='original',
            id=label+"-filters",
            placeholder=placeholders[label],
            authUser=environ['ELASTIC_USER'],
            authPass=environ['ELASTIC_PASS'],
            searchField="original.edgengram",
            value=value)
        ],
        style={'padding':5}
        )
    return textbox

def search_bar_html():
    return html.Div([
        html.Div(dcc.Input(
            id="search-input",
            type="text",
            autofocus=True,
            placeholder="Text search...",
            style={"width": "100%"}),
            style={"display": "table-cell", "width": "100%"}),
        html.Div(html.Button(
            "Search",
            className="button-search",
            id="search-btn"),
            style={"display": "table-cell", "verticalAlign": "top", "paddingLeft": "10px"})],
            className="row", style={"display": "table", "marginTop": "10px"}
        )

def serve_layout(path):
    filters = None
    if path is not None and len(path) > len("/search"):
        path = path[len("/search")+1::]
        path = path.replace("%20", " ")
        ent_type, ent, query = path.split("/")
        filters = defaultdict(list)
        filters[ent_type].append(ent)
        for key, value in eval(query):
            filters[key] += value

    search_bar = search_bar_html()
    filter_boxes = [html.Div([html.Label("Filters")])]
    if not filters:
        filter_boxes += [search_filter_box_html(label) for label in valid_filters]
    else:
        for label in valid_filters:
            if label in filters:
                filter_boxes.append(search_filter_box_html(label, filters[label]))
            else:
                filter_boxes.append(search_filter_box_html(label))

    filter_boxes_and_results = html.Div([html.Div(filter_boxes,style={'width': '25%', 'float': 'left', 'display': 'inline-block'}),dcc.Loading(id="loading-1", children=[html.Div(id='results',style={'width': '75%', 'float': 'right', 'display': 'inline-block'})], type="default")])
    layout = html.Div([search_bar, filter_boxes_and_results])
    return layout

