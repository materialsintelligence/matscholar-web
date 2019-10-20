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
    # search_button = html.Button(
    #     "Search For Materials App",
    #     className="button is-link is-size-6 has-margin-5"
    # )
    # analyze_button = html.Button(
    #     "Analyze An Abstract App",
    #     className="button is-success is-size-6 has-margin-5"
    # )
    # about_button = html.Button(
    #     "About Matscholar",
    #     className="button is-light is-size-6 has-margin-5"
    # )

    search = dcc.Link("Search for Materials", href="/search", className="navbar-item")
    analyze = dcc.Link("Analyze an Abstract", href="/analyze", className="navbar-item")
    introduction = dcc.Link("About", href="/about", className="navbar-item")
    journals = dcc.Link("Journals", href="/journals", className="navbar-item")
    dropdown_items = html.Div([introduction, journals], className="navbar-dropdown")
    dropdown_link = html.Div("Info", className="navbar-link")
    dropdown = html.Div([dropdown_link, dropdown_items], className="navbar-item has-dropdown is-hoverable")
    navbar_start = html.Div([search, analyze, dropdown], className="navbar-start")

    log_in = html.A("Our Github", href="https://github.com/materialsintelligence", className="button is-light")
    buttons = html.Div(log_in, className="buttons")
    buttons_item = html.Div(buttons, className="navbar-item")
    navbar_end = html.Div(buttons_item, className="navbar-end")

    navbar_menu_id = "primary-navbar-menu"
    navbar_menu = html.Div([navbar_start, navbar_end], id=navbar_menu_id, className="navbar-menu")

    nav_image = html.Img(
        src="/assets/logo_inverted.png",
        height=200,
    )
    nav_image_container = html.A(nav_image, className="navbar-item")

    burger = html.Span(**{"aria-hidden": True})
    nav_burger = html.A([burger] * 3, id="primary-burger-trigger", role="button", className="navbar-burger", **{"aria-label": "menu", "aria-expanded": False, "data-target": navbar_menu_id})
    navbar_brand = html.Div([nav_image_container, nav_burger], className="navbar-brand")

    nav_menu = html.Div([navbar_brand, navbar_menu], className="navbar is-link is-fixed-top", role="navigation", **{"aria-label": "main navigation"})
    nav_with_padding = html.Div(nav_menu, className="has-navbar-fixed-top")
    return nav_with_padding
