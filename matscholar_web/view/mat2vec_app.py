import dash_html_components as html
import dash_core_components as dcc


def serve_layout():
    """Generates the layout dynamically on every refresh"""

    return serve_close_words()


def serve_close_words():

    return [

        html.Div([
            html.Div(dcc.Input(
                id="close_words_input",
                type="text",
                autofocus=True,
                placeholder="a single word or phrase, e.g. Fe2O3, thermoelectric, band gap, ... ",
                className="dark-input-box",
                style={"width": "100%"}),
                style={"display": "table-cell", "width": "100%"}),
            html.Div(html.Button(
                "Close words",
                className="button-search",
                id="close_words_button"),
                style={"display": "table-cell", "verticalAlign": "top", "paddingLeft": "10px"})],
            className="row", style={"display": "table", "marginTop": "10px"}),

        html.Div(
            '',
            id='close_words_container',
            style={"padding": "0px 2px"},
            className="row")
        ]
