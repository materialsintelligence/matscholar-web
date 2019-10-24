import dash_core_components as dcc
import dash_html_components as html

"""
Defining the core view (layout) component for the entire app.

Please do not define any callback logic in this file. 
"""


def core_view_html():
    """
    Getting the core view component (layout) for the entire app.
    Contains the nav bar, footer, etc. All view components are either called
    (preferred) or superceded (not preferred) by this function.

    tl;dr: This function makes the html block for what you see when you load
    the webpage!

    Returns:
        core_view (dash_html_components.Div): An html block for the entire site.

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


def nav_html():
    """
    Get the plotly html block for the nav bar.

    Returns:
        (dash_html_components.Div): The nav bar.

    """
    search = dcc.Link("Search for Materials", href="/search",
                      className="navbar-item")
    extract = dcc.Link("Analyze an Abstract", href="/extract",
                       className="navbar-item")
    introduction = dcc.Link("About", href="/about", className="navbar-item")
    journals = dcc.Link("Journals", href="/journals", className="navbar-item")
    dropdown_items = html.Div([introduction, journals],
                              className="navbar-dropdown")
    dropdown_link = html.Div("Info", className="navbar-link")
    dropdown = html.Div([dropdown_link, dropdown_items],
                        className="navbar-item has-dropdown is-hoverable")
    navbar_start = html.Div([search, extract, dropdown],
                            className="navbar-start")

    log_in = html.A("Official Support Forum",
                    href="https://materialsintelligence.discourse.group",
                    className="button is-dark is-small")
    buttons = html.Div(log_in, className="buttons")
    buttons_item = html.Div(buttons, className="navbar-item")
    navbar_end = html.Div(buttons_item, className="navbar-end")

    navbar_menu_id = "primary-navbar-menu"
    navbar_menu = html.Div([navbar_start, navbar_end], id=navbar_menu_id,
                           className="navbar-menu")

    nav_image = html.Img(
        src="/assets/logo_inverted.png",
        height=200,
    )
    nav_image_container = html.A(nav_image, className="navbar-item",
                                 href="https://github.com/materialsintelligence")

    burger = html.Span(**{"aria-hidden": True})
    nav_burger = html.A([burger] * 3, id="primary-burger-trigger",
                        role="button", className="navbar-burger",
                        **{"aria-label": "menu", "aria-expanded": False,
                           "data-target": navbar_menu_id})
    navbar_brand = html.Div([nav_image_container, nav_burger],
                            className="navbar-brand")

    nav_menu = html.Div([navbar_brand, navbar_menu],
                        className="navbar is-link is-fixed-top",
                        role="navigation", **{"aria-label": "main navigation"})
    nav_with_padding = html.Div(nav_menu, className="has-navbar-fixed-top")
    return nav_with_padding


def footer_html():
    """
    Make the footer for all apps.

    Returns:
        (dash_html_components.Div): The footer as an html block.

    """
    note_div = html.Div(
        [
            html.Span(
                "Note: This is an alpha release of Matscholar for the purpose "
                "of collecting feedback."
            )
        ],
    )

    common_footer_style = "has-text-weight-bold"

    about_matscholar = html.A(
        "About Matscholar",
        href="https://github.com/materialsintelligence/matscholar-web",
        target="_blank",
        className=common_footer_style
    )

    privacy_policy = html.A(
        "Privacy Policy",
        href='https://www.iubenda.com/privacy-policy/55585319',
        target="_blank",
        className=common_footer_style
    )

    submit_feedback = html.A(
        "Submit Feedback",
        href='https://materialsintelligence.discourse.group',
        target="_blank",
        className=common_footer_style
    )

    footer_link_tree = html.Div(
        [
            about_matscholar,
            html.Span(" | "),
            privacy_policy,
            html.Span(" | "),
            submit_feedback
        ]
    )

    footer_copyright = html.Div(
        html.Span('Copyright © 2019 - Materials Intelligence')
    )

    footer = html.Div(
        [
            note_div,
            footer_link_tree,
            footer_copyright
        ],
        id="footer_container",
        className="content has-text-centered"
    )

    footer_container = html.Div(footer)
    return footer_container
