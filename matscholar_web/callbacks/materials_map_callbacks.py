from dash.dependencies import Input, Output, State
from matscholar_web.view.materials_map_app import fig
from matscholar import Rester
import matplotlib.colors as colors
import matplotlib.pyplot as plt

rester = Rester()


def bind(app):

    # plot materials map
    @app.callback(
        Output('materials_map', 'figure'),
        [Input('map_highlight_button', 'n_clicks')],
        [State('map_keyword', 'value')])
    def highlight_map(_, keywords):

        response = rester.materials_map(limit=None, highlight=keywords, number_to_substring=True, dims=3)

        # TODO remove this when multiple word queries are handled well
        if len(response["processed_highlight"][0]) <= 1:
            fig["data"] = [response["plot_data"]]

        # TODO check out why this comes as a list??
        if "type" in response["plot_data"]:
            fig["data"][0]["type"] = response["plot_data"]["type"][0]

        scores = response["plot_data"]["marker"]["color"]

        # formatting the tooltip text
        fig["data"][0]["text"] = ["{}<br>score: {:.2f}".format(t, c) for t, c
                               in zip(*[response["plot_data"]["text"], scores])]
        fig["data"][0]["hoverinfo"] = "text"

        # setting tooltip background for the 3D scatter (doesn't work automatically)
        cmap = plt.cm.get_cmap(response["plot_data"]["marker"]["colorscale"].lower())
        minc, maxc = min(scores), max(scores)

        fig["data"][0]["hoverlabel"] = dict(
            bgcolor=["rgb({},{},{})".format(*cmap((c-minc)/(maxc-minc))[:3]*255) for c in scores])

        return fig
