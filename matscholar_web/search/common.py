import dash_html_components as html

from matscholar_web.common import common_null_warning_html

"""
Common, reusable views across the search app and subviews.

Please do not define any callback logic in this file.
"""


def results_disclaimer_html():
    """
    The html block for displaying the disclaimer
    Returns:
        (dash_html_components.Div):
    """
    disclaimer = html.Span("These are incomplete results determined from limited sampling of our database. For full results, use the ")
    api_rester_link = html.A("Matscholar API", href="https://github.com/materialsintelligence/matscholar")
    return html.Div([disclaimer, api_rester_link], className="is-size-6 has-text-weight-semibold")


def no_results_html(pre_label=None):
    """
    The html block for displaying no results.

    Args:
        pre_label (dash_html_components.Div): A label to place before the
            no results html. Alters the formatting of the no results warning.

    Returns:
        (dash_html_components.Div): The html block for no results.

    """
    if pre_label is None:
        return common_null_warning_html("No results found!", alignment="center")
    else:
        common_warning = common_null_warning_html("No results found.", alignment="left", top_margin=5)
        return html.Div([pre_label, common_warning])


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
