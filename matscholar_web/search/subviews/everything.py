import dash_html_components as html

from matscholar_web.search.subviews.abstracts import abstracts_results_html
from matscholar_web.search.subviews.entities import entities_results_html
from matscholar_web.search.subviews.materials import materials_results_html


def everything_results_html(search_text):

    scroll_down = html.Label("Scroll down for more!", className="is-size-4 has-margin-10 has-margin-bottom-20")
    scroll_down_container = html.Div(scroll_down)

    entities_label = html.Label("Statistics (entities)", className="is-size-2 has-margin-10")
    entities_label_container = html.Div(entities_label, className="has-margin-top-50")

    materials_label = html.Label("Similar Materials", className="is-size-2 has-margin-10")
    materials_label_container = html.Div(materials_label, className="has-margin-top-50")

    abstracts_label = html.Label("Relevant Abstracts", className="is-size-2 has-margin-10")
    abstracts_lable_container = html.Div(abstracts_label, className="has-margin-top-50")


    container = html.Div(
        [
            entities_label_container,
            scroll_down_container,
            entities_results_html(search_text),
            materials_label_container,
            materials_results_html(search_text),
            abstracts_lable_container,
            abstracts_results_html(search_text),
         ],
        className="container"
    )
    return container