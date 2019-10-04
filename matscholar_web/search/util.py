import copy

import dash_html_components as html
from dash.dependencies import Input, Output, State

from matscholar_web.constants import valid_entity_filters
from matscholar_web.common import common_null_warning_html

MAX_N_TERMS_PER_ENTITY = 10


def get_entity_boxes_callback_args(as_type="state", return_component="value"):
    """
    Return all available entity boxes as Inputs, Outputs, or States.

    Args:
        as_type (str): "state" for State, "input" for Input, or "output" for
            Output
        return_component (str): Either "value" for the value of the search
            box or n_submit for the number of times the search box has been
            hit.

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

    filters = []
    for f in valid_entity_filters:
        filters.append(t(f + '_filters_input', return_component))
    return filters


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
    if not search_text:
        return None
    entities_text_list = search_text.split(",")
    entity_query = {k: [] for k in valid_entity_filters}
    for et in entities_text_list:
        for k in valid_entity_filters:
            entity_type_key = f"{k}:"
            if entity_type_key in et:
                query_entity_term = copy.deepcopy(et)
                query_entity_term = query_entity_term.replace(
                    entity_type_key,
                    ""
                )
                query_entity_term = query_entity_term.strip()
                entity_query[k].append(query_entity_term)

    entity_query = {k: v for k, v in entity_query.items() if v}
    return entity_query


def query_is_well_formed(entity_query):
    # An empty entity query is not malformed, just empty
    if not entity_query:
        return False

    # If any of the entity terms are longer than a certain length, it's
    # possible someone is trying to *SQL inject our API
    if any([len(v) > MAX_N_TERMS_PER_ENTITY for v in entity_query.values()]):
        return False

    # Ensure at least one of the entity query values is valid
    if any([v for v in entity_query.values()]):
        return True
    else:
        return False


def no_results_html():
    return common_null_warning_html("No results found!")


def rester_error_html():
    rester_error_txt = html.Div(
        f"Our database had trouble with that query. We are likely undergoing "
        f"maintenance, please visit again later!",
        className="is-size-4 is-danger"
    )
    rester_error = html.Div(
        rester_error_txt,
        className="container has-text-centered has-margin-top-50"
    )
    return rester_error


def results_container_class():
    return "container has-margin-top-20 has-margin-bottom-20 msweb-fade-in"


def get_results_label_html(result_type):
    if result_type == "entities":
        label_text = "Statistics (entities)"
    elif result_type == "materials":
        label_text = "Summary of Materials"
    elif result_type == "abstracts":
        label_text = "Relevant Abstracts"
    else:
        raise ValueError(f"Result type {result_type} not valid!")

    label = html.Label(label_text, className="is-size-2 has-margin-10")
    container = html.Div(label, className="has-margin-top-50")
    return container
