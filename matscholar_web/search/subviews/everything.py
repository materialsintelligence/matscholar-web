import dash_html_components as html

from matscholar_web.search.subviews.abstracts import (
    abstracts_results_html,
    abstracts_no_results_html,
)
from matscholar_web.search.subviews.entities import (
    entities_results_html,
    entities_no_results_html,
)
from matscholar_web.search.subviews.materials import (
    materials_results_html,
    materials_no_results_html,
)
from matscholar_web.search.common import no_results_html

"""
Functions for defining the results container when all results are desired.

Please do not define callback logic in this file.
"""


def everything_results_html(entity_query, raw_text):
    """
    Get the html block for all results from the Rester-compatible
    entity query and text. Results are concatenated.

    Args:
        entity_query (dict): The entity query, in Rester-compatible format.
        raw_text (str, None): Any raw text to search for.

    Returns:
        (dash_html_components.Div): The results html block for all search
            types concatenated.

    """
    scroll_down_header_txt = "Scroll down for more results."
    scroll_down_header = html.Div(
        scroll_down_header_txt, className="is-size-3"
    )
    scroll_down = html.Div(
        [scroll_down_header],
        className="notification is-light has-text-centered",
    )
    scroll_down_column = html.Div(scroll_down, className="column is-half")
    scroll_down_columns = html.Div(
        scroll_down_column, className="columns is-centered"
    )
    scroll_down_container = html.Div(
        scroll_down_columns, className="container"
    )

    entities_results = entities_results_html(entity_query, raw_text)
    materials_results = materials_results_html(entity_query, raw_text)
    abstracts_results = abstracts_results_html(entity_query, raw_text)
    no_results = no_results_html(pre_label=None)

    if all(
        [
            entities_results == entities_no_results_html,
            materials_results == materials_no_results_html,
            abstracts_results == abstracts_no_results_html,
        ]
    ):
        return no_results
    else:
        container = html.Div(
            [
                scroll_down_container,
                entities_results,
                materials_results,
                abstracts_results,
            ],
            className="container",
        )
        return container
