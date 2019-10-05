import os

import dash_core_components as dcc
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
import matscholar_web.about.callbacks as bcb
import matscholar_web.about.view as bv

"""
Declarations for the core dash app.
"""

footer_interior = get_footer()
header = get_header()
nav = get_nav()

nav_and_header_section = html.Div([header, nav], className="section")
footer_section = html.Div(footer_interior, className="section")
footer = html.Footer(footer_section, className="footer has-margin-top-50")

app_container = html.Div("", id="app_container", className="container is-fluid")
app_expander = html.Div(app_container, className="msweb-is-tall")
app_expander_container = html.Div(app_expander,
                                  className="msweb-is-tall-container msweb-fade-in")

location = dcc.Location(id="url", refresh=False)

app.layout = html.Div(
    [
        location,
        nav_and_header_section,
        app_expander_container,
        footer,
    ],
)


# Hacks
##########
# Nonsense for getting around plotly's terrible aversion to custom javascript
@app.callback(
    Output('js-counting', 'run'),
    [Input('url', 'pathname')]
)
def js_count_statistics(path):
    # print(f"path, {path}, {str(path).strip() == '/about'}")
    if str(path).strip() == "/about":
        # print('k')
        return bcb.get_counting_callbacks()
    else:
        return ""


# Top level callbacks
#######################
# callbacks for loading different apps

@app.callback(
    Output('app_container', 'children'),
    [Input('url', 'pathname')]
)
def display_page(path):
    # print(f"displaying page {path}")
    # path = str(path)
    if path.strip() in ["/", "", "/search"]:
        return sv.serve_layout()
    elif path == "/analyze":
        return av.serve_layout()
    elif path == "/about":
        return bv.serve_layout()
    else:
        return html.Div("404", className="has-text-centered")


# setting the static path for robots.txt
@app.server.route('/robots.txt')
def get_robots():
    static_folder = os.path.join(os.getcwd(), 'matscholar_web/assets')
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
    Output('search-btn', 'n_clicks'),

    [Input('text_input', 'n_submit')] +
    get_entity_boxes_callback_args(
        as_type="input",
        return_component="n_submit"),
    [State('search-btn', 'n_clicks')]
)
def consolidate_n_submit_and_clicks_to_search_btn(*all_n_clicks):
    return scb.consolidate_n_submit_and_clicks_to_search_button(*all_n_clicks)


@app.callback(
    Output('search_results', 'children'),
    [Input('search-btn', 'n_clicks')],
    [State("search_type_dropdown", "value"),
     State("text_input", "value")]
)
@cache.memoize(timeout=TIMEOUT)
def show_search_results(n_clicks, dropdown_value, search_text):
    return scb.show_results(n_clicks, dropdown_value, search_text)


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
