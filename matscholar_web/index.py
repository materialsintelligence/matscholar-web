import os

# dash
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from flask import send_from_directory

# apps
from matscholar_web.view import mat2vec_app

# callbacks
from matscholar_web.callbacks import mat2vec_callbacks

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
        src="https://s3-us-west-1.amazonaws.com/matstract/matstract_with_text.png",
        style={
         'height': '50px',
         'float': 'right',
         'max-width': "100%",
         "margin": "5px 3px 20px 5px",
         "clear": "both"
        }),
    html.H4(
        "Rediscovering Materials",
        className="headline",
        style={
            "float": "left",
            "margin": "15px 5px 10px 1px",
            "whiteSpace": "nowrap"})
], className="row")

nav = html.Nav(
        style={"margin": "10px 1px", "borderBottom": "1px solid #eee"},
        children=[
            dcc.Link("explore embeddings", href="/explore")
        ],
        id="nav_bar")

app.layout = html.Div([
    html.Div(stylesheets_links, style={"display": "none"}),
    header,
    nav,
    html.Div("", id="app_container")], className='container main-container')

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
    else:
        return mat2vec_app.serve_layout()


# setting the static path for loading css files
@app.server.route('/static/css/<path:path>')
def get_stylesheet(path):
    static_folder = os.path.join(os.getcwd(), 'matscholar_web/static/css')
    return send_from_directory(static_folder, path)


mat2vec_callbacks.bind(app)
