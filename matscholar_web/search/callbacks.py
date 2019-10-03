from matscholar.rest import MatScholarRestError

from matscholar_web.constants import valid_entity_filters
from matscholar_web.search.view import malformed_query_warning_html, \
    no_query_warning_html
from matscholar_web.search.subviews.abstracts import abstracts_results_html
from matscholar_web.search.subviews.materials import materials_results_html
from matscholar_web.search.subviews.entities import entities_results_html
from matscholar_web.search.subviews.everything import everything_results_html
from matscholar_web.search.util import query_is_well_formed, parse_search_box, \
    rester_error_html


def show_results(n_clicks, dropdown_value, search_text):
    if n_clicks in [None, 0]:
        return None
    else:
        try:
            entity_query = parse_search_box(search_text)
            if not entity_query:
                return no_query_warning_html()
            elif not query_is_well_formed(entity_query):
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
            return rester_error_html()


def consolidate_n_submit_and_clicks_to_search_button(*all_n_clicks):
    n_searches_per_input = [0 if n is None else n for n in all_n_clicks]
    n_times_searched = sum(n_searches_per_input)
    return n_times_searched


def search_bar_live_display(*ent_txts):
    entry = ""
    for i, ent in enumerate(valid_entity_filters):
        ent_txt = ent_txts[i]
        if ent_txt not in [None, "", " "]:
            entry += f"{ent}: {ent_txt}, "
    return entry
