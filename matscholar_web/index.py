import os

import dash_html_components as html
from dash.dependencies import Input, Output, State
from flask import send_from_directory

from matscholar_web.app import app, cache
from matscholar_web.constants import TIMEOUT
from matscholar_web.footer import get_footer
from matscholar_web.header import get_header
from matscholar_web.nav import get_nav
from matscholar_web.search.util import get_entity_boxes_callback_args
import matscholar_web.search.callbacks as search_callbacks
import matscholar_web.search.view as search_view
import matscholar_web.analysis.callbacks as analysis_callbacks
import matscholar_web.analysis.view as analysis_view

"""
Declarations for the core dash app.
"""

bulma = html.Link(rel='stylesheet', href='/static/css/bulma.css')
bulma_helper = html.Link(rel='stylesheet', href='/static/css/bulma-helpers.css')
stylesheets = [bulma, bulma_helper]
stylesheet_div = html.Div(stylesheets, className="container is-hidden")

footer = get_footer()
header = get_header()
nav = get_nav()

nav_and_header_section = html.Div([header, nav], className="section")

app_container = html.Div("", id="app_container")


# import dash_core_components as dcc
# input_form = dcc.Input(className="input is-success")
# test_div = html.Div("this is a test section", style={"font-size": "9px"})
# t_search_container = html.Div()

app.layout = html.Div(
    [
        stylesheet_div,
        nav_and_header_section,
        app_container,
        footer
    ],
    className="container"
)


# Top level callbacks
#######################
# callbacks for loading different apps
@app.callback(
    Output('app_container', 'children'),
    [Input('url', 'pathname'), Input('url', 'search')])
def display_page(path, search):
    path = str(path)
    if path.startswith("/analyze"):
        return analysis_view.serve_layout()
    else:
        return search_view.serve_layout(search)


# setting the static path for loading css files
@app.server.route('/static/css/<path:path>')
def get_stylesheet(path):
    static_folder = os.path.join(os.getcwd(), 'matscholar_web/static/css')
    return send_from_directory(static_folder, path)


# setting the static path for robots.txt
@app.server.route('/robots.txt')
def get_robots():
    static_folder = os.path.join(os.getcwd(), 'matscholar_web/static')
    path = "robots.txt"
    return send_from_directory(static_folder, path)


# Search view callbacks
#######################
@app.callback(
    Output('text_input', 'value'),
    get_entity_boxes_callback_args(as_type="input")
)
def live_display_entity_searches(*ent_txts):
    return search_callbacks.live_display_entity_searches(*ent_txts)


@app.callback(
    Output('entities_results', 'children'),
    [Input('search-btn', 'n_clicks')],
    [State("advanced_search_types_radio", "value"),
     State("text_input", "value"),
     State("anonymous_formula_input", "value"),
     State("element_filters_input", "value")] +
    get_entity_boxes_callback_args(as_type="state")
)
@cache.memoize(timeout=TIMEOUT)  # in seconds
def show_entities_results(*args):
    return search_callbacks.show_entities_results(*args)


@app.callback(
    Output('materials_results', 'children'),
    [Input('search-btn', 'n_clicks')],
    [State("advanced_search_types_radio", "value"),
     State("text_input", "value"),
     State("anonymous_formula_input", "value"),
     State("element_filters_input", "value")] +
    get_entity_boxes_callback_args(as_type="state")
)
@cache.memoize(timeout=TIMEOUT)  # in seconds
def show_materials_results(*args):
    return search_callbacks.show_materials_results(*args)


@app.callback(
    Output('abstracts_results', 'children'),
    [Input('search-btn', 'n_clicks')],
    [State("advanced_search_types_radio", "value"),
     State("text_input", "value"),
     State("anonymous_formula_input", "value"),
     State("element_filters_input", "value")] +
    get_entity_boxes_callback_args(as_type="state")
)
@cache.memoize(timeout=TIMEOUT)  # in seconds
def show_abstracts_results(*args):
    return search_callbacks.show_abstracts_results(*args)


@app.callback(
    [Output("abstracts_results", "style"), Output(
        "materials_results", "style"),
     Output("statistics_results", "style")],
    [Input("advanced_search_types_radio", "value")],
    [State("advanced_search_types_radio", "value")]
)
def toggle_search_type(radio_type, radio_val):
    return search_callbacks.toggle_search_type(radio_type, radio_val)


# Analyze callbacks
#######################
@app.callback(
    Output("extract-highlighted", "children"),
    [Input("extract-button", "n_clicks")],
    [State("extract-textarea", "value"),
     State("normalize-radio", "value")])
def highlight_extracted(n_clicks, text, normalize):
    return analysis_callbacks.highlight_extracted(n_clicks, text, normalize)


@app.callback(
  Output('extract-textarea', 'value'),
  [Input("extract-random", 'n_clicks')])
def get_random(n_clicks):
    return analysis_callbacks.get_random(n_clicks)