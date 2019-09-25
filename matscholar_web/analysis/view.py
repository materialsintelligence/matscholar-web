import dash_html_components as html
import dash_core_components as dcc


def serve_layout():
    label = html.Label("Enter text for named entity extraction:")

    random_abstract_button = html.Button("Choose a random abstract",
                                         id="extract-random")
    label_and_random_abstract_button = html.Div([label, random_abstract_button])

    text_area = dcc.Textarea(
        id="extract-textarea",
        style={"width": "100%"},
        spellCheck=True,
        placeholder="Paste abstract/other text here to extract named entities."
    )
    text_area_div = html.Div(text_area)

    convert_synonyms = dcc.RadioItems(id="normalize-radio",
                                      options=[
                                          {'label': "No", 'value': "no"},
                                          {"label": "Yes", "value": "yes"}
                                      ],
                                      value='no',
                                      labelStyle={'display': 'inline-block'}
                                      )
    convert_synonyms_text = html.Div("Convert synonyms?")
    convert_synonyms_container = html.Div(
        [convert_synonyms_text, convert_synonyms])

    extract_button = html.Button("EXTRACT", className="button-search",
                                 id="extract-button")
    loading = dcc.Loading(
        id="loading-extract",
        children=[
            html.Div(id="extract-highlighted"),
            html.Div(id="extracted")
        ],
        type="default"
    )

    loading_container = html.Div(loading)

    layout = html.Div(
        [
            label_and_random_abstract_button,
            text_area_div,
            convert_synonyms_container,
            extract_button,
            loading_container
        ]
    )
    return layout
