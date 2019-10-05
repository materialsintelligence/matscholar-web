import dash_core_components as dcc
import dash_html_components as html

from matscholar_web.util import get_img_link_from_path





def get_header():
    """
    Get the plotly dash header div.

    Returns:
        (dash_html_components.Div): The header.


    """

    # link = get_img_link_from_path("matscholar_logo_v4.png")

    logo = html.Img(
        src="/assets/matscholar_logo_v4.png",
        className="has-ratio",
        height=95,
        width=467
    )

    loc = dcc.Location(id="url", refresh=False)

    header_centering = html.Div(
        [logo, loc],
        id="header_centering",
        className="columns is-centered"
    )

    header_container = html.Div(
        header_centering,
        id="header_container",
        className="container"
    )
    return header_container
