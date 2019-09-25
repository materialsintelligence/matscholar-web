import dash_html_components as html

from matscholar_web.search.subviews.abstracts import abstracts_results_html
from matscholar_web.search.subviews.entities import entities_results_html
from matscholar_web.search.subviews.materials import materials_results_html
from matscholar_web.search.util import get_results_label_html


def everything_results_html(search_text):

    scroll_down = html.Label("Scroll down for more!", className="is-size-4 has-margin-10 has-margin-bottom-20")
    scroll_down_container = html.Div(scroll_down)

    entities_label = get_results_label_html("entities")
    materials_label = get_results_label_html("materials")
    abstracts_label = get_results_label_html("abstracts")

    container = html.Div(
        [
            entities_label,
            scroll_down_container,
            entities_results_html(search_text),
            materials_label,
            materials_results_html(search_text),
            abstracts_label,
            abstracts_results_html(search_text),
         ],
        className="container"
    )
    return container