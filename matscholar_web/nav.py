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

    search = dcc.Link("App: Search for Materials", href="/search", className="navbar-item")
    analyze = dcc.Link("App: Analyze an Abstract", href="/analyze", className="navbar-item")
    introduction = dcc.Link("Overview", href="/overview", className="navbar-item")
    journals = dcc.Link("Journals", href="/journals", className="navbar-item")
    dropdown_items = html.Div([introduction, journals], className="navbar-dropdown")
    dropdown_link = html.Div("Info", className="navbar-link")
    dropdown = html.Div([dropdown_link, dropdown_items], className="navbar-item has-dropdown is-hoverable")
    navbar_start = html.Div([search, analyze, dropdown], className="navbar-start")
    navbar_end = html.Div("", className="navbar-end")
    navbar_menu = html.Div([navbar_start, navbar_end], className="navbar-menu")
    nav_image = html.Img(
        src="/assets/logo_inverted.png",
        className="navbar-item has-width-250 has-50",
    )

    burger = html.Span("", **{"aria-hidden": True})
    nav_burger = html.A([burger] * 3, role="button", className="navbar-burger", **{"aria-label": "menu", "aria-expanded": False})
    navbar_brand = html.Div([nav_image, nav_burger], className="navbar-brand")
    nav_menu = html.Div([navbar_brand, navbar_menu], className="navbar is-link")
    return nav_menu
