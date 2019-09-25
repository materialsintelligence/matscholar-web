import dash_html_components as html

from matscholar_web.search.subviews.abstracts import abstracts_results_html
from matscholar_web.search.subviews.entities import entities_results_html
from matscholar_web.search.subviews.materials import materials_results_html


def everything_results_html(search_text):

    scroll_down = html.Label("Scroll down for more!", className="is-size-4 has-margin-10 has-margin-bottom-20")
    scroll_down_container = html.Div(scroll_down)

    container = html.Div(
        [
            scroll_down_container,
            entities_results_html(search_text),
            materials_results_html(search_text),
            abstracts_results_html(search_text),
         ],
        className="container"
    )
    return container