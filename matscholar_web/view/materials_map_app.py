import dash_html_components as html
import dash_core_components as dcc


fig_layout = {
    'hovermode': 'closest',
    'showlegend': False,
    'margin': dict(
        l=0, r=0, b=0, t=0,
    ),
    "plot_bgcolor": "#000",
    "paper_bgcolor": "#000",
    'xaxis': {
        "autorange": True,
        "showgrid": False,
        "zeroline": False,
        "showline": False,
        "ticks": '',
        "showticklabels": False,
        "title": "",
    },
    'yaxis': {
        "autorange": True,
        "showgrid": False,
        "zeroline": False,
        "showline": False,
        "ticks": '',
        "showticklabels": False,
        "title": "",
    }
}

fig_layout["scene"] = dict(
    xaxis=fig_layout["xaxis"],
    yaxis=fig_layout["yaxis"],
    zaxis=fig_layout["xaxis"],
)

fig = dict(data=[], layout=fig_layout)
layout = [
    html.Div([
        html.Div(dcc.Input(
            id="map_keyword",
            type="text",
            autofocus=True,
            placeholder="a single word or phrase, e.g. battery, alloys, perovskite, "
                        "luminescent, solar cell, LiFePO4, ...",
            className="dark-input-box",
            style={"width": "100%"}),
            style={"display": "table-cell", "width": "100%"}),
        html.Div(html.Button(
            "Highlight",
            className="button-search",
            id="map_highlight_button"),
            style={"display": "table-cell", "verticalAlign": "top", "paddingLeft": "10px"})],
        className="row", style={"display": "table", "marginTop": "10px"}
    ),
    dcc.Graph(
            id='materials_map',
            figure=fig,
            style={"height:": "100vh"}),
]


