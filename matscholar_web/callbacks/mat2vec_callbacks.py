from dash.dependencies import Input, Output, State
from matscholar import Rester
import dash_table as dt


def bind(app):
    # updates similar words
    @app.callback(
        Output('close_words_container', 'children'),
        [Input('close_words_button', 'n_clicks')],
        [State('close_words_input', 'value')])
    def get_close_words(_, word):

        if word is not None and word != "":

            r = Rester()

            result = r.close_words(word.strip(), top_k=8)
            close_words = result["close_words"]
            scores = result["scores"]
            title = "Closest words to {}".format(" + ".join(['"'+w.replace("_", " ")+'"'
                                                             for w in result["sentence"]]))

            return dt.DataTable(
                        data=[{"wordphrase": "{}. {}".format(i+1, w.replace("_", " ")),
                               "Score": "{:.3f}".format(scores[i])}
                              for i, w in enumerate(close_words)],
                        columns=[{"name": title, "id": "wordphrase"},
                                 {"name": "Score", "id": "Score"}],
                        style_cell={
                            'textAlign': 'left',
                            'padding': "2px 10px",
                            "whiteSpace": "normal"},
                        style_cell_conditional=[
                            {'if': {'column_id': 'Score'},
                             'width': '70px', 'textAlign': 'center'},
                        ],
                        css=[{
                            'selector': '.dash-cell div.dash-cell-value',
                            'rule': 'display: inline; white-space: inherit; ' +
                                    'overflow: inherit; text-overflow: inherit;'
                        }],
                        id='analogies_table')
        else:
            return ""
