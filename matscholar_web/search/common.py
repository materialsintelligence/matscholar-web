import dash_html_components as html

from matscholar_web.common import common_null_warning_html

"""
Common, reusable views across the search app and subviews.

Please do not define any callback logic in this file.
"""


def no_results_html():
    """
    The html block for displaying no results.

    Returns:
        (dash_html_components.Div): The html block for no results.

    """
    return common_null_warning_html("No results found!")


def results_label_html(result_type):
    """
    Get the label html block= for the results type.

    Args:
        result_type (str): The result type desired.

    Returns:
        (dash_html_components.Div): The html block for the results label by
            results type.
    """
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


def common_results_container_style():
    """
    The common style for all results types inside a container.

    Returns:
        (str): The common results container style.
    """
    return "container has-margin-top-20 has-margin-bottom-20 msweb-fade-in"
