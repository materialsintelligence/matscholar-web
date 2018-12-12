import os

# dash
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from flask import send_from_directory

# apps
from matscholar_web.view import mat2vec_app, materials_map_app

# callbacks
from matscholar_web.callbacks import mat2vec_callbacks, materials_map_callbacks

"""
APP CONFIG
"""

app = dash.Dash()
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True
app.title = "MatScholar - Rediscovering Materials"

# loading css files
css_files = ["skeleton.min.css", "matscholar_web.css",]
stylesheets_links = [html.Link(rel='stylesheet', href='/static/css/' + css) for css in css_files]

"""
VIEW
"""

header = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Img(
        src="https://s3.amazonaws.com/matscholar/matscholar_logo.png",
        style={
         'width': '250px',
         "display": "block",
         'max-width': "100%",
         "margin": "5px auto",
        }),
], className="row")

nav = html.Nav(
        style={
            "margin": "3px 1px",
            "padding": "3px 1px",
            "textAlign": "center"},
        children=[
            dcc.Link("explore embeddings", href="/explore"),
            html.Span(" | ", style={"color": "whitesmoke"}),
            dcc.Link("materials map", href="/materials_map"),
        ],
        id="nav_bar")

app.layout = html.Div([
        html.Div(stylesheets_links, style={"display": "none"}),
        header,
        nav,
        html.Div("", id="app_container")],
    className='container',
    style={
        "maxWidth": "1600px",
        "height": "100%",
        "width": "100%",
        "padding": "0px 5px"})

"""
CALLBACKS
"""


# callbacks for loading different apps
@app.callback(
    Output('app_container', 'children'),
    [Input('url', 'pathname')])
def display_page(path):
    path = str(path)
    if path.startswith("/explore"):
        return mat2vec_app.serve_layout()
    if path.startswith("/materials_map"):
        return materials_map_app.layout
    else:
        return mat2vec_app.serve_layout()


# setting the static path for loading css files
@app.server.route('/static/css/<path:path>')
def get_stylesheet(path):
    static_folder = os.path.join(os.getcwd(), 'matscholar_web/static/css')
    return send_from_directory(static_folder, path)


mat2vec_callbacks.bind(app)
materials_map_callbacks.bind(app)
