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
def display_app(path):
    """
    Updates which app is shown.

    Args:
        path (str): The path the browser is currently showing. For example,
            "/search".

    Returns:
        (dash_html_components.Div): The app being shown, or a 404.
    """
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


# Animates the burger menu expansion on mobile
# See burger.js and clientside.js for more details
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
    """
    Update the main search bar text live from the example search button and the
    entity fields being typed in.

    Args:
        example_search_n_clicks (int): The number of times the example search
            button was clicked.
        *ent_txts (strs): The strings for each entity guided search field.

    Returns:
        (str): The text to be shown in the search bar via live update.

    """
    return sl.search_bar_live_display(example_search_n_clicks, *ent_txts)


@app.callback(
    Output('example-search-btn', 'n_clicks'),
    get_search_field_callback_args(as_type="input")
)
def void_example_search_n_clicks_on_live_search(*ent_txts):
    """
    Reset the number of example search button clicks when any search is changed
    via the guided search fields.

    Args:
        *ent_txts: The entity texts, though it does not matter what they
            actually are.
    Returns:
        (int): The number of clicks to set the example search button n_clicks
            to.
    """
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
def sum_all_fields_and_buttons_n_submits(*all_n_clicks):
    """
    Sum the guided search fields and main search field and "Go" button n_submits
    and n_clicks to a single n_clicks number for the Go button. Thus the user
    can hit enter on any guided search field or the main box and the app will
    act like you are hitting the go button.

    Args:
        *all_n_clicks (ints): Integers representing the number of times each
            guided search field or main search bar or Go button was
            clicked/entered.

    Returns:
        n_times_searched (int): The total number of times a search was executed.
            If this is voided correctly in another callback, it will be either
            0 or 1.
    """
    return sl.sum_all_fields_and_buttons_n_submits(*all_n_clicks)


@app.callback(
    Output('search_results', 'children'),
    [Input('search-btn', 'n_clicks')],
    [State("search_type_dropdown", "value"),
     State("text_input", "value")]
)
def show_search_results(go_button_n_clicks, dropdown_value, search_text):
    """
    Determine what kind of results to show from the search text, search type,
    and number of clicks of the search button. Cache if necessary using flask.

    Args:
        go_button_n_clicks (int): The number of clicks of the "Go" button.
        dropdown_value (str): The type of search to execute.
        search_text (str): The raw search text as entered in the search field.

    Returns:
        (dash_html_components.Div): The correct html block for the search type
            and customized according to search results from the search text.
    """
    if search_text:
        # Prevent from caching on n_clicks if the results aren't empty
        @cache.memoize(timeout=cache_timeout)
        def memoize_wrapper(dropdown_value, search_text):
            return sl.show_search_results(go_button_n_clicks, dropdown_value, search_text)
        return memoize_wrapper(dropdown_value, search_text)
    else:
        return sl.show_search_results(go_button_n_clicks, dropdown_value, search_text)


# Animates the count up for the search bar
# See count.js and clientside.js for more details
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
# Extract app callbacks
################################################################################
@app.callback(
    Output("extract-highlighted", "children"),
    [Input("extract-button", "n_clicks")],
    [State("extract-textarea", "value"),
     State("dropdown_normalize", "value")])
def extracted_results(extract_button_n_clicks, text, normalize):
    """
    Get the extracted results from the extract app via clicks and the entered
    text, along with the normalize dropdown.

    Args:
        extract_button_n_clicks (int): The number of clicks of the extract
            button.
        text (str): The text entered in the text box, to extract.
        normalize (bool): The normalize string to pass to the rester.

    Returns:
        (dash_html_components, str): The extracted results html block.
    """
    if text:
        # Prevent from caching on n_clicks if the search isn't empty
        @cache.memoize(timeout=cache_timeout)
        def memoize_wrapper(text, normalize):
            return el.extracted_results(extract_button_n_clicks, text, normalize)

        return memoize_wrapper(text, normalize)
    else:
        return el.extracted_results(extract_button_n_clicks, text, normalize)


@app.callback(
    Output('extract-textarea', 'value'),
    [Input("extract-random", 'n_clicks')])
def get_random_abstract(random_button_n_clicks):
    """
    Get a random abstract for the random button.

    Args:
        random_button_n_clicks (int): The number of clicks of the random button.

    Returns:
        (str): The text of a random abstract.
    """
    return el.get_random_abstract(random_button_n_clicks)


################################################################################
# About app callbacks
################################################################################

# Counts up each stat in the about page introduction section
# See count.js and clientside.js for more details
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