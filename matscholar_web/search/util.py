import copy

import dash_html_components as html
from dash.dependencies import Input, Output, State

from matscholar_web.constants import valid_entity_filters


def get_entity_boxes_callback_args(as_type="state"):
    """
    Return all available entity boxes as Inputs, Outputs, or States.

    Args:
        as_type (str): "state" for State, "input" for Input, or "output" for
            Output

    Returns:
        (list): The list of inputs, states, or outputs plotly dash dependency
            objects on the search page.
    """
    type_dict = {
        "state": State,
        "output": Output,
        "input": Input
    }
    t = type_dict[as_type]
    return [t(f + '_filters_input', 'value') for f in valid_entity_filters]


def parse_search_box(search_text):
    """
    Parse the entity search text box

    Args:
        search_text (Str): The text in the search box, e.g.
            "material: PbTe, property: thermoelectric"

    Returns:
        entity_query (dict): The entities from the search text in dict format,
            e.g., {"material": "PbTe", "property": "thermoelectric"}

    Returns:

    """
    entities_text_list = search_text.split(",")
    entity_query = {k: [] for k in valid_entity_filters}
    for et in entities_text_list:
        for k in valid_entity_filters:
            entity_type_key = f"{k}:"
            if entity_type_key in et:
                query_entity_term = copy.deepcopy(et)
                query_entity_term = query_entity_term.replace(entity_type_key,
                                                              "").strip()
                entity_query[k].append(query_entity_term)
    entity_query = {k: v for k, v in entity_query.items() if v}
    return entity_query


def no_results():
    no_results_text = html.Div(
        f"No results found!",
        className="is-size-4"
    )
    no_results_container = html.Div(
        no_results_text,
        className="container has-text-centered has-margin-top-50"
    )
    return no_results_container


def results_container_class():
    return "container has-margin-top-20 has-margin-bottom-20"


def get_results_label_html(result_type):
    if result_type == "entities":
        label_text = "Statistics (entities)"
    elif result_type == "materials":
        label_text = "Similar Materials"
    elif result_type == "abstracts":
        label_text = "Relevant Abstracts"
    else:
        raise ValueError(f"Result type {result_type} not valid!")

    label = html.Label(label_text, className="is-size-2 has-margin-10")
    container = html.Div(label, className="has-margin-top-50")
    return container
