import dash
from dash.dependencies import ClientsideFunction, Input, Output, State
from flask_caching import Cache

import matscholar_web.about.view as bv
import matscholar_web.extract.logic as el
import matscholar_web.extract.view as av
import matscholar_web.journals.view as jv
import matscholar_web.search.logic as sl
import matscholar_web.search.view as sv
from matscholar_web.common import common_404_html
from matscholar_web.constants import cache_timeout, outage
from matscholar_web.search.util import get_search_field_callback_args
from matscholar_web.view import core_view_html, outage_html, nav_html

"""
A safe place for the dash app core instance to hang out.

Also, all high level logic for every callback in the entire dash app.

Please do not define any html-returning functions in this file. Import them
from modules like common, view, or an app's view submodule.

Please see CONTRIBUTING.md before editing this file or callback element ids.
"""

################################################################################
# Dash app core instance
################################################################################
# Any external js scripts you need to define.
external_scripts = [
    "https://www.googletagmanager.com/gtag/js?id=UA-149443072-1"
]

app = dash.Dash(__name__, external_scripts=external_scripts)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True
app.title = "Matscholar - rediscover materials"

if outage:
    app.layout = outage_html()
else:
    app.layout = core_view_html()
cache = Cache(app.server, config={"CACHE_TYPE": "simple"})


################################################################################
# Top level callbacks
# callbacks for loading different apps or are present on every page
################################################################################


@app.callback(
    Output("core-app-container", "children"), [Input("core-url", "pathname")]
)
def display_app_html(path):
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


@app.callback(
    Output("core-nav-container", "children"), [Input("core-url", "pathname")]
)
def update_nav_bar_highlight(path):
    return nav_html(path)


# Animates the burger menu expansion on mobile
# See burger.js and clientside.js for more details
app.clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="animateBurgerOnClickClientsideFunction",
    ),
    Output("core-burger-trigger-cs", "value"),
    [
        Input("core-navbar-menu", "id"),
        Input("core-burger-trigger-cs", "n_clicks"),
    ],
)


################################################################################
# Search app callbacks
################################################################################


@app.callback(
    Output("search-main-bar-input", "value"),
    [Input("search-example-button", "n_clicks")]
    + get_search_field_callback_args(
        as_type="input", return_component="value"
    ),
)
def search_bar_live_display(example_search_n_clicks, *ent_txts):
    """
    Update the main search bar text live from the example search button and the
    entity fields being typed in.

    Args:
        example_search_n_clicks (int): The number of times the example search
            button was clicked.
        *ent_txts (strs): The strings for each guided search field.

    Returns:
        (str): The text to be shown in the search bar via live update.

    """
    return sl.search_bar_live_display(example_search_n_clicks, *ent_txts)


@app.callback(
    Output("search-example-button", "n_clicks"),
    get_search_field_callback_args(as_type="input"),
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


@app.callback(
    Output("search-go-button", "n_clicks"),
    [Input("search-main-bar-input", "n_submit")]
    + get_search_field_callback_args(
        as_type="input", return_component="n_submit"
    ),
    [State("search-go-button", "n_clicks")],
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
    Output("search-results-container", "children"),
    [Input("search-go-button", "n_clicks")],
    [
        State("search-type-dropdown", "value"),
        State("search-main-bar-input", "value"),
    ],
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
        # Prevent from caching on n_clicks if the results aren"t empty
        @cache.memoize(timeout=cache_timeout)
        def memoize_wrapper(dropdown_value, search_text):
            return sl.show_search_results(
                go_button_n_clicks, dropdown_value, search_text
            )

        return memoize_wrapper(dropdown_value, search_text)
    else:
        return sl.show_search_results(
            go_button_n_clicks, dropdown_value, search_text
        )


# Animates the count up for the search bar
# See count.js and clientside.js for more details
app.clientside_callback(
    ClientsideFunction(
        namespace="clientside", function_name="countSearchClientsideFunction"
    ),
    Output("search-count-abstracts-cs", "children"),
    [
        Input("core-url", "pathname"),
        Input("search-count-abstracts-cs", "id"),
        Input("search-count-abstracts-hidden-ref-cs", "id"),
    ],
)

# Rotates example searches through the search bar
# See example_searches.js and clientside.js for more details
app.clientside_callback(
    ClientsideFunction(
        namespace="clientside",
        function_name="cycleExampleSearchesClientsideFunction",
    ),
    Output("search-main-bar-input", "children"),
    [
        Input("core-url", "pathname"),
        Input("search-main-bar-input", "id"),
        Input("search-examples-hidden-ref-cs", "id"),
    ],
)


################################################################################
# Extract app callbacks
################################################################################
@app.callback(
    Output("extract-highlighted", "children"),
    [Input("extract-button", "n_clicks")],
    [
        State("extract-text-area", "value"),
        State("extract-dropdown-normalize", "value"),
    ],
)
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
        # Prevent from caching on n_clicks if the search isn"t empty
        @cache.memoize(timeout=cache_timeout)
        def memoize_wrapper(text, normalize):
            return el.extracted_results(
                extract_button_n_clicks, text, normalize
            )

        return memoize_wrapper(text, normalize)
    else:
        return el.extracted_results(extract_button_n_clicks, text, normalize)


@app.callback(
    Output("extract-text-area", "value"), [Input("extract-random", "n_clicks")]
)
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
        namespace="clientside", function_name="countStatsClientsideFunction"
    ),
    Output("about-count-materials-cs", "children"),
    [
        Input("core-url", "pathname"),
        Input("about-count-materials-cs", "id"),
        Input("about-count-abstracts-cs", "id"),
        Input("about-count-entities-cs", "id"),
        Input("about-count-materials-hidden-ref-cs", "id"),
        Input("about-count-abstracts-hidden-ref-cs", "id"),
        Input("about-count-entities-hidden-ref-cs", "id"),
    ],
)
