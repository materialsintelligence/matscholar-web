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
import matscholar_web.about.view as bv
import matscholar_web.about.callbacks as bc

"""
Declarations for the core dash app.
"""

bulma = html.Link(rel='stylesheet', href='/static/css/bulma.css')
bulma_helper = html.Link(rel='stylesheet', href='/static/css/bulma-helpers.css')
# stylesheets = [bulma, bulma_helper]
custom_css = html.Link(rel='stylesheet', href='/static/css/msweb.css')
stylesheets = [bulma, bulma_helper, custom_css]
stylesheet_div = html.Div(stylesheets, className="container is-hidden")

footer_interior = get_footer()
header = get_header()
nav = get_nav()

nav_and_header_section = html.Div([header, nav], className="section")
footer_section = html.Div(footer_interior, className="section")
footer = html.Footer(footer_section, className="footer")

app_container = html.Div("", id="app_container", className="container is-fluid")
app_expander = html.Div(app_container, className="msweb-is-tall")
app_expander_container = html.Div(app_expander,
                                  className="msweb-is-tall-container")

app.layout = html.Div(
    [
        stylesheet_div,
        nav_and_header_section,
        app_expander_container,
        footer,
    ],
)


# Top level callbacks
#######################

# callbacks for loading different apps
@app.callback(
    Output('app_container', 'children'),
    [Input('url', 'pathname')]
)
def display_page(path):
    path = str(path)
    if path == "/analyze":
        return av.serve_layout()
    elif path == "/search":
        return sv.serve_layout()
    elif path == "/about":
        return bv.serve_layout()
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
    [Input('search-btn', 'n_clicks'),
     Input('text_input', 'n_submit')],
    [State("search_type_dropdown", "value"),
     State("text_input", "value")]
)
@cache.memoize(timeout=TIMEOUT)  # in seconds
def show_search_results(n_clicks, n_submit, dropdown_value, search_text):
    return scb.show_results(n_clicks, n_submit, dropdown_value, search_text)


# Analyze callbacks
#######################
@app.callback(
    Output("extract-highlighted", "children"),
    [Input("extract-button", "n_clicks")],
    [State("extract-textarea", "value"),
     State("dropdown_normalize", "value")])
def highlight_extracted(n_clicks, text, normalize):
    return acb.extracted_results(n_clicks, text, normalize)


@app.callback(
    Output('extract-textarea', 'value'),
    [Input("extract-random", 'n_clicks')])
def get_random(n_clicks):
    return acb.get_random(n_clicks)


# About page callbacks
@app.callback(
    Output('n-current-abstracts', "children"),
    [Input('url', 'pathname')]
)
def update_n_abstracts(pathname):
    if pathname == "/about":
        return bc.get_n_abstracts()
    else:
        return "3,000,000"
