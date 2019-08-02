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
            style={"display": "table-cell", "width": "100%"})],
            className="row", style={"display": "table", "marginTop": "10px"}
        )

def material_search_panel():
    return html.Div([
        html.Div([html.Label("Enter a property/application to find associated materials:"),
                dcc.Input(
                    id="material-search-input",
                    type="text",
                    autofocus=True,
                    placeholder="E.g., ferroelectric, Li-ion batteries",
                    style={"width": "95%"})],
            style={"width": "500px", "display": "inline-block"}),
        html.Div([html.Label("Element filters:"),
                dcc.Input(
                    id="element-filters-input",
                    type="text",
                    autofocus=True,
                    placeholder="E.g., O, -Pb",
                    value=None,
                    style={"width": "50%"})],
            style={"width": "250px", "display": "inline-block"})], id="material-search-panel")

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

    filter_boxes_and_results = html.Div([html.Div(filter_boxes,style={'width': '20%', 'float': 'left', 'display': 'inline-block'}, id="filter-boxes"),dcc.Loading(id="loading-1", children=[html.Div(id='results',style={'width': '75%', 'float': 'right', 'display': 'inline-block'})], type="default")])
    radio = html.Div(dcc.RadioItems(id="search-radio",
                       options=[
                           {'label': "Search", 'value': "search"},
                           {"label": "Summary", "value": "summary"},
                           {"label": "Material Search", "value": "material-search"}
                       ],
                       value='search',
                       labelStyle={'display': 'inline-block'}
                       ), style={"display": "table-cell", "verticalAlign": "top", "paddingLeft": "10px", "float": "left"})
    button = html.Div(html.Button(
            "Search",
            className="button-search",
            id="search-btn", style={"height": "50px", "width": "150px", "font-size": 16}),
            style={"display": "table-cell", "verticalAlign": "top", "paddingLeft": "10px", "float": "right"})
    top = html.Div([radio, button], className="row", style={"display": "table", "marginTop": "10px", "width": "100%"})
    mat_search = material_search_panel()
    layout = html.Div([top, html.Div([search_bar, mat_search, filter_boxes_and_results], id="search-layout")])
    return layout

