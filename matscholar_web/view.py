import dash_core_components as dcc
import dash_html_components as html

from matscholar_web.footer import footer_html
from matscholar_web.nav import nav_html

"""
Defining the core view (layout) component for the entire app.
"""


def core_view_html():
    """
    Getting the core view component (layout) for the entire app.
    Contains the nav bar, footer, etc. All view components are either called
    (preferred) or superceded (not preferred) by this function.

    tl;dr: This function makes the html block for what you see when you load
    the webpage!

    Returns:
        core_view (dash_html_components): An html block for the entire site.

    """
    # The nav bar for all apps
    nav = nav_html()

    # The footer for all apps
    footer_interior = footer_html()
    footer_section = html.Div(footer_interior, className="section")
    footer = html.Footer(footer_section, className="footer has-margin-top-50")

    # The container for individual apps
    app_container = html.Div("", id="app_container",
                             className="container is-fluid")
    app_expander = html.Div(app_container, className="msweb-is-tall")
    app_expander_container = html.Div(
        app_expander,
        className="msweb-is-tall-container msweb-fade-in has-margin-top-50"
    )

    # External stylesheets should be linked here.
    external_stylesheets = \
        html.Link(
            href="https://fonts.googleapis.com/css?family=Ubuntu&display=swap",
            rel="stylesheet",
            className="is-hidden"
        )

    # Location defines the linking for how to change the app.
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
