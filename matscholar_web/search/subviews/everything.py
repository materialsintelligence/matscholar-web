import dash_html_components as html

from matscholar_web.search.subviews.abstracts import abstracts_results_html
from matscholar_web.search.subviews.entities import entities_results_html
from matscholar_web.search.subviews.materials import materials_results_html
from matscholar_web.search.util import no_results_html


def everything_results_html(search_text):

    scroll_link = html.A("link to entities", href="/search#entities_results")
    scroll_down = html.Label(
        scroll_link,
        className="is-size-4 has-margin-10 has-margin-top-20"
    )
    scroll_down_container = html.Div(scroll_down)
    entities_results = entities_results_html(search_text)
    materials_results = materials_results_html(search_text)
    abstracts_results = abstracts_results_html(search_text)
    all_results = [entities_results, materials_results, abstracts_results]
    no_results = no_results_html()

    if all([str(r) == str(no_results) for r in all_results]):
        return no_results
    else:
        container = html.Div(
            [
                scroll_down_container,
                entities_results,
                materials_results,
                abstracts_results,
            ],
            className="container"
        )
        return container