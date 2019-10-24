import dash
from flask_caching import Cache
from dash.dependencies import Input, Output, State, ClientsideFunction

from matscholar_web.view import core_view_html
from matscholar_web.constants import cache_timeout
from matscholar_web.common import common_404_html
from matscholar_web.search.util import get_search_field_callback_args
import matscholar_web.search.logic as sl
import matscholar_web.search.view as sv
import matscholar_web.extract.logic as el
import matscholar_web.extract.view as av
import matscholar_web.about.view as bv
import matscholar_web.journals.view as jv

"""
A safe place for the dash app core instance to hang out.

Also, all high level logic for every callback in the entire dash app.

Please do not define any html-returning functions in this file. Import them
from modules like common, view, or an app's view submodule.
"""

################################################################################
# Dash app core instance
################################################################################
# Any external js scripts you need to define.
external_scripts = [
    "https://www.googletagmanager.com/gtag/js?id=UA-149443072-1"
]

app = dash.Dash(
    __name__,
    external_scripts=external_scripts
)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True
app.title = "Matscholar - rediscover materials"
app.layout = core_view_html()
cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})


################################################################################
# Top level callbacks
# callbacks for loading different apps or are present on every page
################################################################################
@app.callback(
    Output('app_container', 'children'),
    [Input('url', 'pathname')]
)
def display_page(path):
    if str(path).strip() in ["/", "/search"] or not path:
        return sv.app_view_html()
    elif path == "/extract":
        return av.app_view_html()
    elif path == "/about":
        return bv.app_view_html()
    elif path == "/journals":
        return jv.app_view_html()
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


################################################################################
# Search app callbacks
################################################################################
@app.callback(
    Output('text_input', 'value'),
    [Input('example-search-btn', 'n_clicks')] +
    get_search_field_callback_args(as_type="input"),
)
def search_bar_live_display(example_search_n_clicks, *ent_txts):
    return sl.search_bar_live_display(example_search_n_clicks, *ent_txts)


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
    return sl.consolidate_n_submit_and_clicks_to_search_button(*all_n_clicks)


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
            return sl.show_results(n_clicks, dropdown_value, search_text)

        return memoize_wrapper(dropdown_value, search_text)
    else:
        return sl.show_results(n_clicks, dropdown_value, search_text)


# See count.js and clientside.js for more details
# Animates the count up for the search bar
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='countSearchCSCallback'
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
        function_name='cycleExampleSearchesCSCallback'
    ),
    Output('text_input', 'children'),
    [
        Input('url', 'pathname'),
        Input('text_input', 'id'),
        Input('search-examples-hidden-ref', 'id')
    ]
)

################################################################################
# Analyze app callbacks
################################################################################
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
            return el.extracted_results(n_clicks, text, normalize)

        return memoize_wrapper(text, normalize)
    else:
        return el.extracted_results(n_clicks, text, normalize)


@app.callback(
    Output('extract-textarea', 'value'),
    [Input("extract-random", 'n_clicks')])
def get_random(n_clicks):
    return el.get_random(n_clicks)


################################################################################
# About app callbacks
################################################################################

# See count.js and clientside.js for more details
# Counts up each stat in the about page introduction section
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='countStatsCSCallback'
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