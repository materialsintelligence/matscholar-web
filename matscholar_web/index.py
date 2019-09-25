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
import matscholar_web.search.callbacks as scb
import matscholar_web.search.view as sv
import matscholar_web.analysis.callbacks as acb
import matscholar_web.analysis.view as av

"""
Declarations for the core dash app.
"""

bulma = html.Link(rel='stylesheet', href='/static/css/bulma.css')
bulma_helper = html.Link(rel='stylesheet', href='/static/css/bulma-helpers.css')
# stylesheets = [bulma, bulma_helper]
custom_css = html.Link(rel='stylesheet', href='/static/css/msweb.css')
stylesheets = [bulma, bulma_helper, custom_css]
stylesheet_div = html.Div(stylesheets, className="container is-hidden")

footer = get_footer()
header = get_header()
nav = get_nav()

nav_and_header_section = html.Div([header, nav], className="section")
footer_section = html.Div(footer, className="section")
app_container = html.Div("", id="app_container", className="container is-fluid")

app.layout = html.Div(
    [
        stylesheet_div,
        nav_and_header_section,
        app_container,
        footer_section,
    ],
)


# Top level callbacks
#######################

# callbacks for loading different apps
@app.callback(
    Output('app_container', 'children'),
    [Input('url', 'pathname'), Input('url', 'search')],
    # [State('url', 'pathname'), State('app_container', "children")]
)
def display_page(path, search):
    path = str(path)
    if path.startswith("/analyze"):
        return av.serve_layout()
    elif path.startswith("/search"):
        return sv.serve_layout(search)
    else:
        return html.Div("404", className="has-text-centered")


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
def search_bar_live_display(*ent_txts):
    return scb.search_bar_live_display(*ent_txts)


@app.callback(
    Output('search_results', 'children'),
    [Input('search-btn', 'n_clicks')],
    [State("search_type_dropdown", "value"),
     State("text_input", "value")]
)
@cache.memoize(timeout=TIMEOUT)  # in seconds
def show_search_results(n_clicks, dropdown_value, search_text):
    return scb.show_results(n_clicks, dropdown_value, search_text)


@app.callback(
    [Output("abstracts_results", "style"),
     Output("materials_results", "style"),
     Output("statistics_results", "style")],
    [Input("search_type_dropdown", "value")],
    # [State("search_type_dropdown", "value")],
)
def dropdown_search_type(search_type):
    return scb.dropdown_search_type(search_type)


# Analyze callbacks
#######################
@app.callback(
    Output("extract-highlighted", "children"),
    [Input("extract-button", "n_clicks")],
    [State("extract-textarea", "value"),
     State("normalize-radio", "value")])
def highlight_extracted(n_clicks, text, normalize):
    return acb.highlight_extracted(n_clicks, text, normalize)


@app.callback(
    Output('extract-textarea', 'value'),
    [Input("extract-random", 'n_clicks')])
def get_random(n_clicks):
    return acb.get_random(n_clicks)
