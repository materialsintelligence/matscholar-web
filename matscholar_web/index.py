import os
from os import environ

import dash
import dash_auth
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import send_from_directory
from flask_caching import Cache

from matscholar_web.view import search_view, analysis_view
from matscholar_web.footer import get_footer
from matscholar_web.header import get_header
from matscholar_web.nav import get_nav
from matscholar_web.callbacks import search_view_callbacks, analysis_callbacks
"""
Declarations for the core dash app.
"""

"""
APP CONFIG
"""

app = dash.Dash(
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1"
        }
    ]
)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True
app.title = "matscholar - rediscover materials"
cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})

# Authentication
VALID_USERNAME_PASSWORD_PAIRS = [
    [environ['MATERIALS_SCHOLAR_WEB_USER'],
     environ['MATERIALS_SCHOLAR_WEB_PASS']]]
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

stylesheet = html.Link(rel='stylesheet', href='/static/css/bulma.css')
stylesheet_div = html.Div(stylesheet, className="container is-hidden")

"""
VIEW
"""

app_container = html.Div("", id="app_container")
footer = get_footer()
header = get_header()
nav = get_nav()

app.layout = html.Div(
    [
        stylesheet_div,
        header,
        nav,
        app_container,
        footer
    ],
    className="container"
)

"""
CALLBACKS
"""


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


search_view_callbacks.bind(app, cache)
analysis_callbacks.bind(app)


# setting the static path for robots.txt
@app.server.route('/robots.txt')
def get_robots():
    static_folder = os.path.join(os.getcwd(), 'matscholar_web/static')
    path = "robots.txt"
    return send_from_directory(static_folder, path)
