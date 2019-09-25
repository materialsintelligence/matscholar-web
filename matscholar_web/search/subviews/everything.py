import dash_html_components as html

from matscholar_web.search.subviews.abstracts import abstracts_results_html
from matscholar_web.search.subviews.entities import entities_results_html
from matscholar_web.search.subviews.materials import materials_results_html


def everything_results_html(search_text):

    scroll_down = html.Label("Scroll down for more!", className="is-size-4 has-margin-10 has-margin-bottom-20")
    entities_label = html.Label("Statistics (entities)", className="is-size-2 has-margin-10")
    materials_label = html.Label("Statistics (entities)", className="is-size-4 has-margin-10")
    abstracts_label = html.Label("Statistics (entities)", className="is-size-4 has-margin-10")

    container = html.Div(
        [
            scroll_down,
            entities_label,
            entities_results_html(search_text),
            materials_label,
            materials_results_html(search_text),
            abstracts_label,
            abstracts_results_html(search_text),
         ],
        className="container"
    )
    return container