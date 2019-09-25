import dash_html_components as html
import dash_core_components as dcc

"""
Functions for defining navigation bar components.
"""


def get_nav():
    """
    Get the plotly html object for the nav bar.

    Returns:
        (dash_html_components.Div): The nav bar.

    """
    search_button = html.Button(
        "Search For Materials App",
        className="button is-link disabled is-size-6 has-margin-5"
    )
    analyze_button = html.Button(
        "Analyze An Abstract App",
        className="button is-warning is-size-6 has-margin-5"
    )

    search = dcc.Link(search_button, href="/search")
    analyze = dcc.Link(analyze_button, href="/analyze")

    search_container = html.Div(search)
    analyze_container = html.Div(analyze)

    nav = html.Nav(
        children=[search_container, analyze_container],
        className="columns is-centered"
    )
    nav_container = html.Div(nav, className="container has-margin-10 is-fluid")
    return nav_container
