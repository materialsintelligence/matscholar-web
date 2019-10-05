import dash_core_components as dcc
import dash_html_components as html


def get_header():
    """
    Get the plotly dash header div.

    Returns:
        (dash_html_components.Div): The header.
    """

    logo = html.Img(
        src="/assets/logo.png",
        className="has-ratio",
        height=95,
        width=467
    )

    header_centering = html.Div(
        [logo],
        id="header_centering",
        className="columns is-centered"
    )

    header_container = html.Div(
        header_centering,
        id="header_container",
        className="container"
    )
    return header_container
