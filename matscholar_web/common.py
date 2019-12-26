import dash_html_components as html


"""
Common, reusable views across apps.

Please do not define any callback logic in this file.
"""


def logo_html():
    """
    Get the matscholar logo as a centered image for an app.

    Returns:
        (dash_html_components.Div): The header.
    """

    logo = html.Img(
        src="/assets/logo.png", style={"width": "400px", "height": "65px"}
    )

    header_centering = html.Div(
        [logo],
        id="header_centering",
        className="columns is-centered is-mobile",
    )

    header_container = html.Div(
        header_centering,
        id="header_container",
        className="container has-margin-bottom-30 has-margin-top-50",
    )
    return header_container


def common_warning_html(header_txt, body_txt, width):
    """
    Get a warning box which can be used across all apps.

    Use sparingly.

    Args:
        header_txt (str): The text to include in the big header of the warning.
        body_txt (str): The main warning text body.
        width (str): The width of the warning, in column bulma syntax

    Returns:
        (dash_html_components.Div): The common warning box html block.

    """
    warning_header = html.Div(header_txt, className="is-size-3")
    warning_body = html.Div(body_txt, className="is-size-6")
    warning = html.Div(
        [warning_header, warning_body], className="notification is-danger"
    )
    warning_column = html.Div(warning, className=f"column {width}")
    warning_columns = html.Div(warning_column, className="columns is-centered")
    warning_container = html.Div(warning_columns, className="container")
    return warning_container


def common_null_warning_html(text, alignment="center", top_margin=50):
    """
    Get a null warning html block which can be used across all apps. Useful for
    when no text is entered into a box, etc.

    Args:
        text (str): The null warning text.
        alignment (str): Either "center" or "left".
        top_margin (int): The top margin, in pixels.

    Returns:
        (dash_html_components.Div): The common null warning html block.

    """
    if alignment in ["center", "left"]:
        align = "has-text-centered" if alignment == "center" else ""
    else:
        raise ValueError(
            f"Invalid alignment: {alignment}. Must be 'center' or 'left'."
        )

    null_txt = html.Div(text, className="is-size-4")
    null_container = html.Div(
        null_txt, className=f"container {align} has-margin-top-{top_margin}"
    )
    return null_container


def common_rester_error_html(text):
    """
    Get a warning for any rester error which can be used across all apps.

    Args:
        text (str): The text you want to show.

    Returns:
        (dash_html_components.Div): The rester error html block.


    """
    rester_error_txt = html.Div(text, className="is-size-4 is-danger")
    rester_error = html.Div(
        rester_error_txt,
        className="container has-text-centered has-margin-top-50",
    )
    return rester_error


def divider_html():
    """
    Get an html block divider. Can be used in any app.

    Returns:
        (dash_html_components.Div): The divider html block.

    """
    return html.Div(html.Hr(className="is-divider"))


def common_info_box_html(elements, id=None):
    """
    Get an outlined box for displaying information, such as references, about
    page stuff, etc. Can be used in any app.

    Args:
        elements ([dash_html_components.Div], dash_html_components.Div): Either
            a single dash html component or multiple in a list. These will
            be encapsulated by the box.
        id (str, None): The id you want to assign to the container of the box.

    Returns:
        container (dash_html_components.Div): an html block container for the
            box encapsulating your elements.

    """
    box = html.Div(elements, className="box")
    column = html.Div(box, className="column is-two-thirds")
    columns = html.Div(
        column, className="columns is-centered has-margin-top-50"
    )
    container = html.Div(columns, className="container", id=id)
    return container


def common_404_html():
    """
    Get a 404 error html. Can and should be used across apps. Update this
    function to update all 404 display behavior.

    Returns:
        (dash_html_components.Div): The 404 html block.

    """
    return html.Div("404", className="has-text-centered")


def common_stat_style():
    """
    The common style for info statistics.

    Should be used in a dash component className.

    Returns:
        (str): The style to be used in className.
    """
    return "has-margin-right-10 has-margin-left-10 has-text-centered has-text-weight-bold"


def common_body_style():
    """
    The common style for info body.

    Should be used in a dash component className.

    Returns:
        (str): The style to be used in className.
    """
    return "is-size-6-desktop has-margin-5"


def common_header_style():
    """
    The common style for info header.

    Should be used in a dash component className.

    Returns:
        (str): The style to be used in className.
    """
    return "is-size-5-desktop has-text-weight-bold has-margin-5"


def common_title_style():
    """
    The common style for info title.

    Should be used in a dash component className.

    Returns:
        (str): The style to be used in className.
    """
    return "is-size-2-desktop has-text-weight-bold has-margin-5"
