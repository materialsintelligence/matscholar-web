import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ClientsideFunction

from matscholar_web.app import app, cache
from matscholar_web.constants import cache_timeout
from matscholar_web.footer import get_footer
from matscholar_web.nav import get_nav
from matscholar_web.search.util import get_search_field_callback_args
import matscholar_web.search.callbacks as scb
import matscholar_web.search.view as sv
import matscholar_web.analysis.callbacks as acb
import matscholar_web.analysis.view as av
import matscholar_web.about.view as bv
import matscholar_web.journals.view as jv

"""
Declarations for the core dash app.
"""

footer_interior = get_footer()
nav = get_nav()
footer_section = html.Div(footer_interior, className="section")
footer = html.Footer(footer_section, className="footer has-margin-top-50")

app_container = html.Div("", id="app_container", className="container is-fluid")
app_expander = html.Div(app_container, className="msweb-is-tall")
app_expander_container = html.Div(app_expander,
                                  className="msweb-is-tall-container msweb-fade-in")


external_stylesheets = \
    html.Link(
        href="https://fonts.googleapis.com/css?family=Ubuntu&display=swap",
        rel="stylesheet",
        className="is-hidden"
    )

location = dcc.Location(id="url", refresh=False)

app.layout = html.Div(
    [
        external_stylesheets,
        location,
        nav,
        app_expander_container,
        footer,
    ],
    className="msweb-background"
)


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
    elif path== "/journals":
        return jv.serve_layout()
    else:
        return html.Div("404", className="has-text-centered")


# See count.js and clientside.js for more details
# Animates the count up for the search bar
app.clientside_callback(
    ClientsideFunction(
        namespace='clientside',
        function_name='animateBurgerOnClickCSCallback'
    ),
    Output("primary-navbar-menu", 'children'),
    [
        Input("primary-navbar-menu", 'id'),
        Input("primary-burger-trigger", 'id'),
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
    # Prevent from caching on n_clicks
    @cache.memoize(timeout=cache_timeout)
    def memoize_wrapper(dropdown_value, search_text):
        return scb.show_results(n_clicks, dropdown_value, search_text)

    return memoize_wrapper(dropdown_value, search_text)


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
    # Prevent from caching on n_clicks
    @cache.memoize(timeout=cache_timeout)
    def memoize_wrapper(text, normalize):
        return acb.extracted_results(n_clicks, text, normalize)
    return memoize_wrapper(text, normalize)


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
