import os
import base64

from matscholar_web.constants import ROOT_DIR

"""
Utilities for working with plotly dash.
"""


def get_img_link_from_path(filename):
    """
    Get a plotly dash compatible link for a static local image.

    Args:
        filename (str): The name of the image (MUST BE IN THE 'static' folder!

    Returns:
        logo_link (str): The formatted plotly-ready image link. Can be used in
            a plotly dash html.Img src.

    """
    img_path = os.path.join(ROOT_DIR, f"static/{filename}")
    encoded_image = base64.b64encode(open(img_path, 'rb').read())
    logo_link = 'data:image/png;base64,{}'.format(encoded_image.decode())
    return logo_link

