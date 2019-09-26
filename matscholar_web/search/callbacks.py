from matscholar_web.constants import valid_entity_filters
from matscholar_web.search.view import malformed_query_warning_html, \
    no_query_warning_html, loading_wrapper_html
from matscholar_web.search.subviews.abstracts import abstracts_results_html
from matscholar_web.search.subviews.materials import materials_results_html
from matscholar_web.search.subviews.entities import entities_results_html
from matscholar_web.search.subviews.everything import everything_results_html
from matscholar_web.search.subviews.nothing import no_selection_html
from matscholar_web.search.util import query_is_well_formed, parse_search_box


def show_results(n_clicks, dropdown_value, search_text):
    print(f"nclicks is {n_clicks}")
    if n_clicks in [None, 0]:
        return None
    else:
        if dropdown_value in ['no_selection', None]:
            return no_selection_html()

        entity_query = parse_search_box(search_text)
        if not search_text:
            return no_query_warning_html()
        elif not query_is_well_formed(entity_query):
            return malformed_query_warning_html(search_text)
        else:
            if dropdown_value == 'abstracts':
                r = abstracts_results_html(search_text)
            elif dropdown_value == 'materials':
                r = materials_results_html(search_text)
            elif dropdown_value == 'entities':
                r = entities_results_html(search_text)
            elif dropdown_value == 'everything':
                r = everything_results_html(search_text)
            else:
                raise ValueError(
                    f"Dropdown selection {dropdown_value} not valid!"
                )
            wrapper = loading_wrapper_html(r)
            return wrapper


def search_bar_live_display(*ent_txts):
    entry = ""
    for i, ent in enumerate(valid_entity_filters):
        ent_txt = ent_txts[i]
        if ent_txt not in [None, "", " "]:
            entry += f"{ent}: {ent_txt}, "
    return entry
