from dash.dependencies import Input, Output, State, ClientsideFunction

from matscholar_web.app import cache
from matscholar_web.view import app
from matscholar_web.constants import cache_timeout
from matscholar_web.common import common_404_html
from matscholar_web.search.util import get_search_field_callback_args
import matscholar_web.search.callbacks as scb
import matscholar_web.search.view as sv
import matscholar_web.analysis.callbacks as acb
import matscholar_web.analysis.view as av
import matscholar_web.about.view as bv
import matscholar_web.journals.view as jv

"""
All high level logic for every callback in the entire dash app.

Please do not define any html-returning functions in this file. Import them
from modules like common, view, or an app's view submodule.
"""

# Top level callbacks
#######################
# callbacks for loading different apps or are present on every page

@app.callback(
    Output('app_container', 'children'),
    [Input('url', 'pathname')]
)
def display_page(path):
    if str(path).strip() in ["/", "/search"] or not path:
        return sv.serve_layout()
    elif path == "/analyze":
        return av.serve_layout()
    elif path == "/about":
        return bv.serve_layout()
    elif path == "/journals":
        return jv.serve_layout()
    else:
        return common_404_html()


# @app.callback(
#     Output('text_input', 'style'),  # a dummy output
#     [
#         Input('search-btn', 'n_clicks'),
#     ]
# )
# def get_ip(value):
#     import pandas as pd
#     import os
#
#     logdir = "logs"
#     logfile =
#
#     if not os.path.exists():
#         os.mkdir("logs")
#
#     if not os.path.exists
#     ip_addr = request.remote_addr
#     print(os.getcwd())
#     # df = pd.read_json("./logs/log.json")
#     # print(df)
#     print("ip address is", ip_addr)
#     return {}


# See burger.js and clientside.js for more details
# Animates the burger menu expansion on mobile
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='animateBurgerOnClickCSCallback'
    ),
    Output("primary-burger-trigger", "value"),
    [
        Input("primary-navbar-menu", 'id'),
        Input("primary-burger-trigger", 'n_clicks'),
    ]
)


# Search view callbacks
#######################
@app.callback(
    Output('text_input', 'value'),
    [Input('example-search-btn', 'n_clicks')] +
    get_search_field_callback_args(as_type="input"),
)
def search_bar_live_display(example_search_n_clicks, *ent_txts):
    return scb.search_bar_live_display(example_search_n_clicks, *ent_txts)


@app.callback(
    Output('example-search-btn', 'n_clicks'),
    get_search_field_callback_args(as_type="input")
)
def void_example_search_n_clicks_on_live_search(*ent_txts):
    return 0


# A test callback for updating guided search fields on searching
# @app.callback(
#     get_search_field_callback_args(as_type="output", return_component="value"),
#     # [Output("material_filter_input", "value")],
#     [Input('search-btn', 'n_clicks')],
#     [State('text_input', 'value')]
# )
# def something(n_clicks, text_input):
#     print(text_input)
#     return ["test"]*8


@app.callback(
    Output('search-btn', 'n_clicks'),
    [Input('text_input', 'n_submit')] +
    get_search_field_callback_args(
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
def show_search_results(n_clicks, dropdown_value, search_text):
    if search_text:
        # Prevent from caching on n_clicks if the results aren't empty
        @cache.memoize(timeout=cache_timeout)
        def memoize_wrapper(dropdown_value, search_text):
            return scb.show_results(n_clicks, dropdown_value, search_text)

        return memoize_wrapper(dropdown_value, search_text)
    else:
        return scb.show_results(n_clicks, dropdown_value, search_text)


# See count.js and clientside.js for more details
# Animates the count up for the search bar
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='countSearch'
    ),
    Output('count-search', 'children'),
    [
        Input('url', 'pathname'),
        Input('count-search', 'id'),
        Input('count-search-hidden-ref', 'id')
    ]
)

# See example_searches.js and clientside.js for more details
# Puts example searches in the search bar
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='cycleExampleSearches'
    ),
    Output('text_input', 'children'),
    [
        Input('url', 'pathname'),
        Input('text_input', 'id'),
        Input('search-examples-hidden-ref', 'id')
    ]
)


# Analyze callbacks
#######################
@app.callback(
    Output("extract-highlighted", "children"),
    [Input("extract-button", "n_clicks")],
    [State("extract-textarea", "value"),
     State("dropdown_normalize", "value")])
def highlight_extracted(n_clicks, text, normalize):
    if text:
        # Prevent from caching on n_clicks if the search isn't empty
        @cache.memoize(timeout=cache_timeout)
        def memoize_wrapper(text, normalize):
            return acb.extracted_results(n_clicks, text, normalize)

        return memoize_wrapper(text, normalize)
    else:
        return acb.extracted_results(n_clicks, text, normalize)


@app.callback(
    Output('extract-textarea', 'value'),
    [Input("extract-random", 'n_clicks')])
def get_random(n_clicks):
    return acb.get_random(n_clicks)


# About callbacks
######################

# See count.js and clientside.js for more details
# Counts up each stat in the about page introduction section
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='countStats'
    ),
    Output('count-materials', 'children'),
    [
        Input('url', 'pathname'),
        Input('count-materials', 'id'),
        Input('count-abstracts', 'id'),
        Input('count-entities', 'id'),
        Input('count-materials-hidden-ref', 'id'),
        Input('count-abstracts-hidden-ref', 'id'),
        Input('count-entities-hidden-ref', 'id')
    ]
)