import dash_html_components as html

from matscholar_web.common import common_null_warning_html


"""
Common, reusable views across the search app and subviews.

Please do not define any callback logic in this file.
"""


def big_label_and_disclaimer_html(label_txt):
    """
    Get the html block results big label and disclaimer for a particular
    search.

    Args:
        label_txt (str): The key for generating a results label.

    Returns:
        (dash_html_components.Div): The html block for the big label and
            disclaimer

    """
    big_results_label = results_label_html(label_txt)
    disclaimer = results_disclaimer_html()
    return html.Div([big_results_label, disclaimer])


def results_disclaimer_html():
    """
    The html block for displaying the disclaimer

    Returns:
        (dash_html_components.Div): The html block results disclaimer.
    """
    disclaimer = html.Span(
        "These are incomplete results determined from limited sampling of our database. For full results, use the "
    )
    api_rester_link = html.A(
        "Matscholar API",
        href="https://github.com/materialsintelligence/matscholar",
    )
    return html.Div(
        [disclaimer, api_rester_link],
        className="is-size-6 has-text-weight-semibold",
    )


def no_results_html(pre_label=None):
    """
    The html block for displaying no results.

    Args:
        pre_label (None, dash_html_components.Div): A label to place before the
            no results html. Alters the formatting of the no results warning.

    Returns:
        (dash_html_components.Div): The html block for no results.

    """
    if pre_label is None:
        return common_null_warning_html(
            "No results found!", alignment="center"
        )
    else:
        common_warning = common_null_warning_html(
            "No results found.", alignment="left", top_margin=5
        )
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


def cobalt_warning_html(results):
    """
    Add a warning to results on searches for cobalt/cobalt containing materials

    Args:
        results (dash_html_components.Div): The results div
    Returns:
        (dash_html_components.Div): The html block for the cobalt warning
        label
    """

    cobalt_warning_txt = "60% of the world's cobalt is mined in the DRC, often using forced, compulsory, or child labour in highly unsafe conditions. No current oversight of the cobalt supply chain exists which would allow the sourcing of guaranteed ethically mined cobalt. Please consider using alternatives to cobalt wherever possible."

    cobalt_warning_header = html.Div(cobalt_warning_txt, className="is-size-0")
    cobalt_warning = html.Div(
        [cobalt_warning_header],
        className="has-background-grey-lighter has-text-centered",
    )
    cobalt_warning_column = html.Div(
        cobalt_warning, className="column is-half"
    )
    cobalt_warning_columns = html.Div(
        cobalt_warning_column, className="columns is-centered"
    )
    cobalt_warning_container = html.Div(
        cobalt_warning_columns, className="container"
    )

    wrapped_results = html.Div(
        [cobalt_warning_container, results], className="container"
    )
    return wrapped_results
