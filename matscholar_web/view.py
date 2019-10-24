import dash_core_components as dcc
import dash_html_components as html

from matscholar_web.footer import footer_html
from matscholar_web.nav import nav_html

"""
Defining the core view components for the dahs app.
"""


def core_view_html():
    footer_interior = footer_html()
    nav = nav_html()
    footer_section = html.Div(footer_interior, className="section")
    footer = html.Footer(footer_section, className="footer has-margin-top-50")

    app_container = html.Div("", id="app_container",
                             className="container is-fluid")
    app_expander = html.Div(app_container, className="msweb-is-tall")
    app_expander_container = html.Div(
        app_expander,
        className="msweb-is-tall-container msweb-fade-in has-margin-top-50"
    )

    external_stylesheets = \
        html.Link(
            href="https://fonts.googleapis.com/css?family=Ubuntu&display=swap",
            rel="stylesheet",
            className="is-hidden"
        )

    location = dcc.Location(id="url", refresh=False)

    core_view = html.Div(
        [
            external_stylesheets,
            location,
            nav,
            app_expander_container,
            footer,
        ],
        className="msweb-background"
    )
    return core_view