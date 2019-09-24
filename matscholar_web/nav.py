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
    search = dcc.Link("search", href="/search")
    divider = html.Span(" | ")
    analyze = dcc.Link("analyze", href="/analyze")
    nav = html.Nav(children=[search, divider, analyze])
    nav_columns=html.Div(nav, className="column is-narrow")
    nav_container = html.Div(nav_columns, className="columns is-centered")
    return nav_container