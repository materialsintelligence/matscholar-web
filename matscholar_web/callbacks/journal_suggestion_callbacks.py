from dash.dependencies import Input, Output, State
import dash_html_components as html
from matscholar import Rester


def bind(app):
    @app.callback(
        Output('similar-journal-table', 'children'),
        [Input('similar-journal-button', 'n_clicks')],
        [State('similar-journal-textarea', 'value')]
    )
    def update_table(n_clicks, text):
        r = Rester()

        journals = r.get_journals(text)
        print(journals)
        return html.Table(
            # Header
            [html.Tr([html.Th('Suggested Journals'), html.Th('Cosine Similarity')])] +
            # Body
            [html.Tr([html.Td(journals[0][0]), html.Td(journals[0][1])])] +
            [html.Tr([html.Td(journals[1][0]), html.Td(journals[1][1])])] +
            [html.Tr([html.Td(journals[2][0]), html.Td(journals[2][1])])] +
            [html.Tr([html.Td(journals[3][0]), html.Td(journals[3][1])])] +
            [html.Tr([html.Td(journals[4][0]), html.Td(journals[4][1])])] +
            [html.Tr([html.Td(journals[5][0]), html.Td(journals[5][1])])] +
            [html.Tr([html.Td(journals[6][0]), html.Td(journals[6][1])])] +
            [html.Tr([html.Td(journals[7][0]), html.Td(journals[7][1])])] +
            [html.Tr([html.Td(journals[8][0]), html.Td(journals[8][1])])] +
            [html.Tr([html.Td(journals[9][0]), html.Td(journals[9][1])])]
        )

    #@cache.memoize(timeout=600)
    #@app.callback(
     #  Output('similar-journals-table-cosine', 'children'),
      # [Input('similar-journal-button', 'n_clicks')],
       #[State('similar-journal-textarea', 'value')]
    #)
    #def update_search_table(n_clicks, text):
     #   return journal_suggestion_app.generate_table_cosine(text)
