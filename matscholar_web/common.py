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
