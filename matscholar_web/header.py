import dash_core_components as dcc
import dash_html_components as html


def get_header():
    """
    Get the plotly dash header div.
    Returns:
        (dash_html_components.Div): The header.
    """

    logo = html.Img(
        src="/assets/logo_highres.png",
        className="has-ratio",
        height=125,
        width=800,
    )

    header_centering = html.Div(
        [logo],
        id="header_centering",
        className="columns is-centered is-desktop"
    )

    header_container = html.Div(
        header_centering,
        id="header_container",
        className="container has-margin-bottom-10 has-margin-top-80"
    )
    return header_container