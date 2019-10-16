import dash_core_components as dcc
import dash_html_components as html


def get_logo():
    """
    Get the plotly dash header div.
    Returns:
        (dash_html_components.Div): The header.
    """

    logo = html.Img(
        src="/assets/logo_header.png",
        # className="has-ratio",
        # width="400px",
        # height="62px",
    )

    header_centering = html.Div(
        [logo],
        id="header_centering",
        className="columns is-centered is-mobile"
    )

    header_container = html.Div(
        header_centering,
        id="header_container",
        className="container has-margin-bottom-10 has-margin-top-80"
    )
    return header_container