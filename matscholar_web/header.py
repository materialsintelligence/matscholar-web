import dash_core_components as dcc
import dash_html_components as html

from matscholar_web.app import app

import os
import base64


STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/matscholar_logo_v2_smaller.png')
encoded_image = base64.b64encode(open(STATIC_PATH, 'rb').read())


def get_header():
    """
    Get the plotly dash header div.

    Returns:
        (dash_html_components.Div): The header.


    """

    # logo_link = "https://matscholar-web.s3-us-west-1.amazonaws.com/" \
    #             "matscholar_logo+alpha.png"

    # logo_link = app.get_asset_url("matscholar_logo_v2_smaller.png")
    logo_link = 'data:image/png;base64,{}'.format(encoded_image.decode())

    img_link = html.Img(
        src=logo_link,
        # className="has-ratio",
        # height=72,
        # width=369
    )

    loc = dcc.Location(id="url", refresh=False)

    header_container = html.Div(
        [img_link, loc],
        id="header_container",
        # className="columns is-centered"
    )
    return header_container
