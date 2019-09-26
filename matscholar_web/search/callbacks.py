from matscholar_web.constants import valid_entity_filters
from matscholar_web.search.view import malformed_query_warning_html, \
    no_query_warning_html
from matscholar_web.search.subviews.abstracts import abstracts_results_html
from matscholar_web.search.subviews.materials import materials_results_html
from matscholar_web.search.subviews.entities import entities_results_html
from matscholar_web.search.subviews.everything import everything_results_html
from matscholar_web.search.subviews.nothing import no_selection_html
from matscholar_web.search.util import query_is_well_formed, parse_search_box


def dropdown_search_type(search_type):
    """
    Toggle the search type using the search type buttons
    """
    visible_style = {}
    hidden_style = {"display": "none"}
    if search_type == "abstracts":
        return visible_style, hidden_style, hidden_style
    elif search_type == "materials":
        return hidden_style, visible_style, hidden_style
    elif search_type == "entities":
        return hidden_style, hidden_style, visible_style
    elif search_type == "everything":
        return visible_style, visible_style, visible_style


def show_results(n_clicks, dropdown_value, search_text):
    if n_clicks in [None, 0]:
        return None
    else:
        entity_query = parse_search_box(search_text)
        if not entity_query:
            return no_query_warning_html()
        elif not query_is_well_formed(entity_query):
            return malformed_query_warning_html(search_text)
        else:
            if dropdown_value == 'abstracts':
                return abstracts_results_html(search_text)
            if dropdown_value == 'materials':
                return materials_results_html(search_text)
            if dropdown_value == 'entities':
                return entities_results_html(search_text)
            if dropdown_value == 'everything':
                return everything_results_html(search_text)
            if dropdown_value == 'no_selection':
                return no_selection_html()
            else:
                raise ValueError("No valid dropdown value selected!")


def search_bar_live_display(*ent_txts):
    entry = ""
    for i, ent in enumerate(valid_entity_filters):
        ent_txt = ent_txts[i]
        if ent_txt not in [None, "", " "]:
            entry += f"{ent}: {ent_txt}, "
    return entry
