import dash_html_components as html
import dash_core_components as dcc

from matscholar_web.constants import valid_entity_filters
from matscholar_web.search.subviews.abstracts import \
    abstracts_results_html
from matscholar_web.search.subviews.materials import \
    materials_results_html
from matscholar_web.search.subviews.entities import \
    entities_results_html


def toggle_search_type(radio_type, radio_val):
    """
    Toggle the search type using the search type buttons
    """
    visible_style = {'width': '75%',
                     'float': 'right', 'display': 'inline-block'}
    hidden_style = {"display": "none"}
    if radio_val == "abstracts":
        return visible_style, hidden_style, hidden_style
    elif radio_val == "materials":
        return hidden_style, visible_style, hidden_style
    else:
        return hidden_style, hidden_style, visible_style


# def show_abstracts_results(*args):
#     """
#     Perform a search for abstracts and display the results
#     """
#     if args[0] is not None:
#         if args[1] == 'abstracts':
#             return abstracts_results_html(list(args)[2:])
#
#
# def show_materials_results(*args):
#     if args[0] is not None:
#         if args[1] == 'materials':
#             return materials_results_html(list(args)[2:])


def show_entities_results(n_clicks, dropdown_value, search_text):
    if n_clicks not in [None, 0]:
        if dropdown_value == 'entities':
            print(f"From search callbacks: The args are {n_clicks, dropdown_value, search_text}")
            return entities_results_html(n_clicks, dropdown_value, search_text)
            # return html.Div("Test OUTPUT!", className="is-size-1")


def live_display_entity_searches(*ent_txts):
    entry = ""
    for i, ent in enumerate(valid_entity_filters):
        ent_txt = ent_txts[i]
        if ent_txt not in [None, "", " "]:
            entry += f"{ent}: {ent_txt}, "
    return entry

