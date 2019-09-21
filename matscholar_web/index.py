import os
import json
from os import environ

# dash
import dash
import dash_auth
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from flask import send_from_directory
from flask_caching import Cache
from matscholar.rest import Rester
from matscholar.rest import MatScholarRestError

# apps
from matscholar_web.view import search_view, analysis_view

# callbacks
from matscholar_web.callbacks import search_view_callbacks, analysis_callbacks

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
    [environ['MATERIALS_SCHOLAR_WEB_USER'], environ['MATERIALS_SCHOLAR_WEB_PASS']]]
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

# loading css files
# css_files = ["skeleton.min.css", "matscholar_web.css", ]
css_files = ["bulma.css"]
stylesheets_links = [
    html.Link(rel='stylesheet', href='/static/css/' + css) for css in css_files]

"""
VIEW
"""

header_contianer = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Img(
        src="https://matscholar-web.s3-us-west-1.amazonaws.com/matscholar_logo+alpha.png",
        style={
            'width': '350px',
            "display": "block",
            'max-width': "100%",
            "margin": "5px auto",
        })],
    id="header_container",
    className="row")

nav = html.Nav(
    style={
        "margin": "3px 1px",
        "padding": "3px 1px",
        "textAlign": "center"},
    children=[
        dcc.Link("search", href="/search"),
        html.Span(" | ", style={"color": "whitesmoke"}),
        dcc.Link("analyze", href="/analyze"),
        html.Span(" | ", style={"color": "whitesmoke"}),
    ],
    id="nav_bar")

footer_container = html.Div([
    html.Div(className="row"),
    html.Div(
        [html.Span("Note: This is an alpha release of Matscholar for the purpose of collecting feedback.")],
        className="row"),
    html.Div([
        html.A("About Matscholar",
               href="https://github.com/materialsintelligence/matscholar-web",
               target="_blank"),
        html.Span(" | "),
        html.A("Privacy Policy",
               href='https://www.iubenda.com/privacy-policy/55585319',
               target="_blank"),
        html.Span(" | "),
        html.A("Submit Feedback",
               href='https://github.com/materialsintelligence/matscholar-web/issues',
               target="_blank")],
        className="row"),
    html.Div(html.Span('Copyright © 2019 - Materials Intelligence'))],
    id="footer_container",
    className="row",
    style={
        "color": "grey",
        "textAlign": "center",
        "width": "100%"})

app.layout = html.Div([
    html.Div(stylesheets_links, style={"display": "none"}),
    header_contianer,
    nav,
    html.Div("", id="app_container"),
    footer_container],
    className='container',
    style={
        "maxWidth": "1600px",
        "height": "100%",
        "width": "100%",
        # "margin-top": "10%",
        # "margin-bottom": "20%",
        # "margin-right": "20%",
        # "margin-left": "20%",
        "padding": "5px 5px",
    })

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
