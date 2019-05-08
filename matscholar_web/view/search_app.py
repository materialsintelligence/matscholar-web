import dash_html_components as html
import dash_materialsintelligence as dmi
import dash_core_components as dcc
from dash.dependencies import Input
import json, os

placeholders = {"material": "Si2Ti, graphite,...", "property": "dielectric constant, melting point,...", "application": "cathode, catalyst,...", "descriptor": "ceramics, disordered,...", "characterization": "mathematical model, x-ray diffraction,...","synthesis":"sol - gel, firing,...", "phase": "perovskite, spinel,..."}


def filters_html(label, placeholder,dropdown_options):
    return html.Div([
        html.Label('{}:'.format(label)),
         dcc.Dropdown(
            options=dropdown_options[label],
            id=label+'-filters'
            ,
        multi=True,
        placeholder=placeholder,
        style={"width": "100%"}
        ),
    ],
    style={'padding':5}
)

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

def serve_layout(valid_filters,dropdown_options):
    search_bar = search_bar_html()
    buttons = [html.Div(html.Label("Filters"))]
    for f in valid_filters:
        buttons.append(filters_html(f,placeholders[f],dropdown_options))
    buttons_and_results = html.Div([html.Div(buttons,style={'width': '25%', 'float': 'left', 'display': 'inline-block'}),html.Div(id='results',style={'width': '75%', 'float': 'right', 'display': 'inline-block'})])
    layout = html.Div([search_bar, buttons_and_results])
    return layout

