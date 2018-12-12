from dash.dependencies import Input, Output, State
from matscholar_web.view.materials_map_app import fig, rester


def bind(app):

    # plot materials map
    @app.callback(
        Output('materials_map', 'figure'),
        [Input('map_highlight_button', 'n_clicks')],
        [State('map_keyword', 'value')])
    def highlight_map(n_clicks, keywords):

        if n_clicks:
            response = rester.materials_map(limit=None, highlight=keywords, number_to_substring=True)
            fig["data"] = [response["plot_data"]]
            return fig
        else:
            return fig


