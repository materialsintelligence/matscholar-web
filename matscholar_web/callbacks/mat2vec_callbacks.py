from dash.dependencies import Input, Output, State
import dash_html_components as html
from matscholar import Rester
from matscholar.utils import parse_word_expression
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

            positive, negative = parse_word_expression(word.strip())
            result = r.close_words(positive=positive, negative=negative, top_k=8, ignore_missing=True)

            # TODO get rid of this when the combined embeddings are handled well
            if len(result["positive"]) > 1 or len(result["negative"]) > 0:
                return html.Span(
                    'No single word or phrase found for "{}" in the vocabulary'.format(word.strip()),
                    style={"color": "#16ADAF"}
                )

            close_words = result["close_words"]
            scores = result["scores"]
            if negative:
                title = "Closest words to {} - {}".format(
                    " + ".join(['"'+w.replace("_", " ")+'"' for w in result["positive"]]),
                    " - ".join(['"' + w.replace("_", " ") + '"' for w in result["negative"]])
                )
            else:
                title = "Closest words to {}".format(
                    " + ".join(['"' + w.replace("_", " ") + '"' for w in result["positive"]])
                )

            return dt.DataTable(
                        data=[{"wordphrase": "{}. {}".format(i+1, w.replace("_", " ")),
                               "Score": "{:.3f}".format(scores[i])}
                              for i, w in enumerate(close_words)],
                        columns=[{"name": title, "id": "wordphrase"},
                                 {"name": "Score", "id": "Score"}],
                        style_as_list_view=True,
                        style_header={
                            'backgroundColor': 'rgb(0, 0, 0)',
                            'color': '#16ADAF'},
                        style_cell={
                            'backgroundColor': 'rgb(0, 0, 0)',
                            'textAlign': 'left',
                            'color': 'whitesmoke',
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
