import dash_html_components as html
import dash_core_components as dcc


def serve_layout():
    return html.Div([html.Div([
        html.Label("Enter text for named entity extraction:", style={"float": "left"}),
        html.Button("Choose a random abstract", id="extract-random", style={"float": "right"})],
        style={"width": "100%", "vertical-align": "bottom"}),
        html.Div([dcc.Textarea(id="extract-textarea",
                               style={"width": "100%"},
                               autoFocus=True,
                               spellCheck=True,
                               wrap=True,
                               placeholder="Paste abstract/other text here to extract named entity mentions."
                               )]),
        html.Div(["Convert synonyms?",
                  dcc.RadioItems(id="normalize-radio",
                                 options=[
                                     {'label': "No", 'value': "no"},
                                     {"label": "Yes", "value": "yes"}
                                 ],
                                 value='no',
                                 labelStyle={'display': 'inline-block'}
                                 )]),
        html.Div([html.Button("EXTRACT", className="button-search", id="extract-button")],
                 style={"padding-top": "0px", "padding-bottom": "15px"}),
        dcc.Loading(id="loading-extract",
                    children=[
                        html.Div(id="extract-highlighted",
                                 style={"width": "90vw", "word-wrap": "break-word", "word-break": "break-all"}),
                        html.Div(id="extracted")],
                    type="default")])
