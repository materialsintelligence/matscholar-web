import dash_core_components as dcc
import dash_html_components as html

layout = html.Div([
    html.Div([
        html.Div([
            html.P('Matscholar Journal Suggestion: find journals based on your abstract.')
        ], style={'margin-left': '10px'}),
        html.Label('Enter an abstract to find relevant journals:'),
        html.Div(dcc.Textarea(id='similar-journal-textarea',
                              style={"width": "100%"},
                              autoFocus=True,
                              spellCheck=True,
                              wrap=True,
                              placeholder='Paste abstract/other text here.'
                              )),
        html.Div([html.Button('Find Journals', id='similar-journal-button'),
                  ]),
        html.Div([
            html.Table(id='similar-journal-table'),
            html.Table(id='similar-journals-table-cosine')
        ], className='row', style={"overflow": "scroll"}),
    ], className='twelve columns')
])