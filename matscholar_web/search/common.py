
import dash_html_components as html

from matscholar_web.common import common_null_warning_html

"""
Common, reusable views across the search app and subviews.

Please do not define any callback logic in this file.
"""


def no_results_html():
    return common_null_warning_html("No results found!")


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
