import dash_html_components as html
import dash_core_components as dcc


def serve_layout():
    label = html.Label(
        "Enter text for named entity extraction:",
        className="is-size-4 has-margin-5"
    )

    random_abstract_button = html.Button(
        "Use a random abstract",
        id="extract-random",
        className="button is-warning is-size-6 is-pulled-right has-margin-5"
    )

    text_area = dcc.Textarea(
        id="extract-textarea",
        style={"width": "100%"},
        spellCheck=True,
        placeholder="Paste abstract/other text here to extract named entities.",
        className="input is-info is-medium has-min-height-250"
    )
    text_area_div = html.Div(text_area)

    convert_synonyms = dcc.Dropdown(id="dropdown_normalize",
                                    options=[
                                        {'label': "No", 'value': "no"},
                                        {"label": "Yes", "value": "yes"}
                                    ],
                                    value='no',
                                    )
    convert_synonyms_text = html.Div("Convert synonyms?", className="is-size-6")
    convert_synonyms_container = html.Div(
        [convert_synonyms_text, convert_synonyms],
        className="is-pulled-right has-margin-5",
    )

    extract_button = html.Button(
        "Extract entities",
        id="extract-button",
        className="button is-link is-size-4 has-margin-5"
    )
    loading = dcc.Loading(
        id="loading-extract",
        children=[
            html.Div(id="extract-highlighted"),
            html.Div(id="extracted")
        ],
        type="graph"
             # 'graph', 'cube', 'circle', 'dot'
    )

    loading_container = html.Div(loading)

    layout = html.Div(
        [
            label,
            random_abstract_button,
            text_area_div,
            convert_synonyms_container,
            extract_button,
            loading_container
        ],
        className="container has-margin-top-50"
    )
    return layout
