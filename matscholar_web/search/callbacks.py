import random

from matscholar.rest import MatScholarRestError

from matscholar_web.common import common_rester_error_html
from matscholar_web.constants import valid_entity_filters, example_searches
from matscholar_web.search.view import malformed_query_warning_html, \
    no_query_warning_html
from matscholar_web.search.subviews.abstracts import abstracts_results_html
from matscholar_web.search.subviews.materials import materials_results_html
from matscholar_web.search.subviews.entities import entities_results_html
from matscholar_web.search.subviews.everything import everything_results_html
from matscholar_web.search.util import query_is_well_formed, parse_search_box


def show_results(n_clicks, dropdown_value, search_text):
    if n_clicks in [None, 0]:
        return ""
    else:
        try:
            if not search_text:
                return no_query_warning_html()

            entity_query = parse_search_box(search_text)
            if not query_is_well_formed(entity_query):
                return malformed_query_warning_html(search_text)
            else:
                if dropdown_value == 'abstracts':
                    results = abstracts_results_html(search_text)
                elif dropdown_value == 'materials':
                    results = materials_results_html(search_text)
                elif dropdown_value == 'entities':
                    results = entities_results_html(search_text)
                elif dropdown_value == 'everything':
                    results = everything_results_html(search_text)
                else:
                    raise ValueError(
                        f"Dropdown selection {dropdown_value} not valid!"
                    )
                return results
        except MatScholarRestError:
            rester_error = \
                "Our database had trouble with that query. We are likely " \
                "undergoing maintenance, please visit again later!"
            return common_rester_error_html(rester_error)


def consolidate_n_submit_and_clicks_to_search_button(*all_n_clicks):
    n_searches_per_input = [0 if n is None else n for n in all_n_clicks]
    n_times_searched = sum(n_searches_per_input)
    # The number of times searches total, reset the random search click
    return n_times_searched, 0


def search_bar_live_display(example_search_n_clicks, *ent_txts):
    if example_search_n_clicks not in [None, 0]:
        return random.choice(example_searches)
    else:
        entry = ""
        for i, ent in enumerate(valid_entity_filters):
            ent_txt = ent_txts[i]
            if ent_txt not in [None, "", " "]:
                entry += f"{ent}: {ent_txt}, "
        return entry


def reset_example_n_clicks_on_search_or_live_update():
    return 0
