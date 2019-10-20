import dash_html_components as html

"""
Common, reusable views across apps.
"""


def common_warning_html(header_txt, body_txt):
    warning_header = html.Div(header_txt, className="is-size-3")
    warning_body = html.Div(body_txt, className="is-size-6")
    warning = html.Div(
        [
            warning_header,
            warning_body
        ],
        className="notification is-danger"
    )
    warning_column = html.Div(warning, className="column is-half")
    warning_columns = html.Div(warning_column, className="columns is-centered")
    warning_container = html.Div(warning_columns, className="container")
    return warning_container


def common_null_warning_html(text):
    null_txt = html.Div(
        text,
        className="is-size-4"
    )
    null_container = html.Div(
        null_txt,
        className="container has-text-centered has-margin-top-50"
    )
    return null_container


def common_rester_error_html(text):
    rester_error_txt = html.Div(text, className="is-size-4 is-danger")
    rester_error = html.Div(
        rester_error_txt,
        className="container has-text-centered has-margin-top-50"
    )
    return rester_error


def divider_html():
    return html.Hr(className="is-divider")


def common_info_box(elements, id=None):
    box = html.Div(elements, className="box")
    column = html.Div(box, className="column is-two-thirds")
    columns = html.Div(column, className="columns is-centered has-margin-top-50")
    container = html.Div(columns, className="container", id=id)
    return container


def common_stat_style():
    return "has-margin-right-10 has-margin-left-10 has-text-centered has-text-weight-bold"


def common_body_style():
    return "is-size-6-desktop has-margin-5"


def common_header_style():
    return "is-size-5-desktop has-text-weight-bold has-margin-5"


def common_title_style():
    return "is-size-2-desktop has-text-weight-bold has-margin-5"
