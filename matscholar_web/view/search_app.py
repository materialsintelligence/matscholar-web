import dash_html_components as html
import dash_materialsintelligence as dmi
import dash_core_components as dcc
from dash.dependencies import Input
import json, os

valid_filters = ["material", "property", "application", "descriptor", "characterization", "synthesis", "phase"]

def search_filter_box_html(label):
    placeholders = {"material": "Si2Ti, graphite,...", "property": "dielectric constant, melting point,...", "application": "cathode, catalyst,...", "descriptor": "ceramics, disordered,...", "characterization": "mathematical model, x-ray diffraction,...","synthesis":"sol - gel, firing,...", "phase": "perovskite, spinel,..."}
    textbox = html.Div([html.Label('{}:'.format(label)),
        dcc.Input(
            id=label+"-filters",
            type="text",
            autofocus=True,
            placeholder=placeholders[label],
            style={"width": "100%"})
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

def serve_layout():
    search_bar = search_bar_html()
    filter_boxes = [html.Div(html.Label("Filters"))]
    filter_boxes += [search_filter_box_html(label) for label in valid_filters]

    filter_boxes_and_results = html.Div([html.Div(filter_boxes,style={'width': '25%', 'float': 'left', 'display': 'inline-block'}),html.Div(id='results',style={'width': '75%', 'float': 'right', 'display': 'inline-block'})])
    layout = html.Div([search_bar, filter_boxes_and_results])
    return layout

