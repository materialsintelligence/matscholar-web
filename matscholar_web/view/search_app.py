import dash_html_components as html
import dash_materialsintelligence as dmi
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import json, os, random
from matscholar import Rester

VALID_FILTERS = ["material", "property", "application", "descriptor", "characterization", "synthesis", "phase"]
FILTERS_TO_KEYS = {"material": "MAT", "property":"PRO", "application": "APL", "synthesis": "SMT", "characterization": "CMT", "descriptor": "DSC", "phase": "SPL"}
KEYS_TO_FILTERS = {v: k for k,v in FILTERS_TO_KEYS.items()}
with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static','data','entities.json'),'r') as f:
    entities_dict = json.load(f)
PLACEHOLDERS = {x: entities_dict[FILTERS_TO_KEYS[x]][0]+", "+entities_dict[FILTERS_TO_KEYS[x]][1]+", ..." for x in VALID_FILTERS}
rester = Rester()

def format_result(result):
    return html.Div([dcc.Markdown("[%s](https://doi.org/%s)" %(result['doi'],result['doi']))]+
        [html.Label(KEYS_TO_FILTERS[k]+": "+", ".join([v for v in result[k]])) for k,v in result.items() if k != 'doi'],style={"padding": 0})

def results_html(results):
    return html.Div([format_result(r) for r in results],style={"padding": 5})

def filters_html(label, placeholder):
    return html.Div([
        html.Label('{}:'.format(label)),
         dcc.Dropdown(
            options=[{'label': x, 'value': x} for x in entities_dict[FILTERS_TO_KEYS[label]]],
            id=label+'-filters'
            ,
        multi=True,
        placeholder=placeholder
        ),
    ],
    style={'padding':5}
)

def serve_layout():
    buttons = [html.Div(html.Button(
                         "Search",
                         id='search-btn',
                         name="Search"
                     ),style={'textAlign':'center'})]
    buttons.append(html.Div(html.Label("Filters")))
    for f in VALID_FILTERS:
        buttons.append(filters_html(f,PLACEHOLDERS[f]))
    layout = [html.Div(buttons,style={'width': '20%', 'float': 'left', 'display': 'inline-block'}),html.Div(id='results',style={'width': '70%', 'float': 'right', 'display': 'inline-block'})]
    return html.Div(layout)

def bind(app):
    @app.callback(
        Output('results', 'children'),
        [Input('search-btn','n_clicks')],
        [State(f+'-filters', 'value') for f in VALID_FILTERS])
    def show_results(*args,**kwargs):
        if list(args)[0] is not None:
            filters = {f: list(args)[i+1] for i,f in enumerate(VALID_FILTERS) if list(args)[i+1] is not None}
            results = rester.search_ents(filters)
            return results_html(results)
