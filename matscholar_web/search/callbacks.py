import dash_html_components as html
import dash_core_components as dcc

from matscholar_web.constants import valid_entity_filters
from matscholar_web.search.subviews.abstracts import \
    abstracts_results_html
from matscholar_web.search.subviews.materials import \
    materials_results_html
from matscholar_web.search.subviews.entities import \
    entities_results_html


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
    else:
        return hidden_style, hidden_style, visible_style


def show_results(n_clicks, dropdown_value, search_text):
    if n_clicks in [None, 0]:
        return None
    else:
        if dropdown_value == 'abstracts':
            return abstracts_results_html(search_text)
        if dropdown_value == 'materials':
            return materials_results_html(search_text)
        if dropdown_value == 'entities':
            return entities_results_html(search_text)

# def show_abstracts_results(n_clicks, dropdown_value, search_text):
#     if n_clicks not in [None, 0]:
#         if dropdown_value == 'abstracts':
#             return abstracts_results_html(search_text)
#
#
# def show_materials_results(n_clicks, dropdown_value, search_text):
#     if n_clicks not in [None, 0]:
#         if dropdown_value == 'materials':
#             return materials_results_html(search_text)
#             # return html.Div("Test OUTPUT!", className="is-size-1")
#
#
# def show_entities_results(n_clicks, dropdown_value, search_text):
#     if n_clicks not in [None, 0]:
#         if dropdown_value == 'entities':
#             return entities_results_html(search_text)


def search_bar_live_display(*ent_txts):
    entry = ""
    for i, ent in enumerate(valid_entity_filters):
        ent_txt = ent_txts[i]
        if ent_txt not in [None, "", " "]:
            entry += f"{ent}: {ent_txt}, "
    return entry
