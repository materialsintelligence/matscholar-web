import random

from matscholar.rest import MatScholarRestError
from matscholar_web.common import common_rester_error_html
from matscholar_web.constants import example_searches, valid_search_filters
from matscholar_web.search.subviews.abstracts import abstracts_results_html
from matscholar_web.search.subviews.entities import entities_results_html
from matscholar_web.search.subviews.everything import everything_results_html
from matscholar_web.search.subviews.materials import materials_results_html
from matscholar_web.search.common import cobalt_warning_html
from matscholar_web.search.util import (
    MatscholarWebSearchError,
    parse_search_box,
)
from matscholar_web.search.view import (
    malformed_query_warning_html,
    no_query_warning_html,
)


"""
Callback logic for callbacks in the search app.

Please do not define any html blocks in this file.
"""


def show_search_results(go_button_n_clicks, dropdown_value, search_text):
    """
    Determine what kind of results to show from the search text, search type,
    and number of clicks of the search button.

    Args:
        go_button_n_clicks (int): The number of clicks of the "Go" button.
        dropdown_value (str): The type of search to execute.
        search_text (str): The raw search text as entered in the search field.

    Returns:
        (dash_html_components.Div): The correct html block for the search type
            and customized according to search results from the search text.
    """
    if go_button_n_clicks in [None, 0]:
        return ""
    else:
        try:
            if not search_text:
                return no_query_warning_html()
            try:
                entity_query, raw_text = parse_search_box(search_text)
            except MatscholarWebSearchError:
                return malformed_query_warning_html(search_text)
            if dropdown_value == "abstracts":
                results = abstracts_results_html(entity_query, raw_text)
            elif dropdown_value == "materials":
                results = materials_results_html(entity_query, raw_text)
            elif dropdown_value == "entities":
                results = entities_results_html(entity_query, raw_text)
            elif dropdown_value == "everything":
                results = everything_results_html(entity_query, raw_text)
            else:
                raise ValueError(
                    f"Dropdown selection {dropdown_value} not valid!"
                )
            if is_cobalt_search(entity_query, raw_text):
                results = cobalt_warning_html(results)
            return results
        except MatScholarRestError:
            rester_error = (
                "Our database had trouble with that query. We are likely "
                "undergoing maintenance, please visit again later!"
            )
            return common_rester_error_html(rester_error)


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
    n_searches_per_input = [0 if n is None else n for n in all_n_clicks]
    n_times_searched = sum(n_searches_per_input)
    # The number of times searches total, reset the random search click
    return n_times_searched


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
    if example_search_n_clicks == 0:
        entry = ""
        for i, ent in enumerate(valid_search_filters):
            ent_txt = ent_txts[i]
            if ent_txt not in [None, "", " "]:
                entry += f"{ent}: {ent_txt}, "
        return entry
    else:
        return random.choice(example_searches)


def is_cobalt_search(entity_query, raw_text):
    if raw_text is not None:
        if 'Co' in raw_text.split() or 'cobalt' in raw_text.lower().split():
            return True

    if entity_query is not None:
        if 'material' in entity_query.keys():
            if any(['Co' in m for m in entity_query['material']]) or any(['cobalt' in m.lower() for m in entity_query['material']]):
                return True

    return False
