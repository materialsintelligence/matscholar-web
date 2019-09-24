import dash_core_components as dcc
import dash_html_components as html


def get_header():
    """
    Get the plotly dash header div.

    Returns:
        (dash_html_components.Div): The header.


    """

    logo_link = "https://matscholar-web.s3-us-west-1.amazonaws.com/" \
                "matscholar_logo+alpha.png"

    img_link = html.Img(
        src=logo_link,
    )

    loc = dcc.Location(id="url", refresh=False)

    header_container = html.Div(
        [img_link, loc],
        id="header_container",
    )
    return header_container
