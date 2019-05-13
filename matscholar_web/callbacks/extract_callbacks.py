import dash_html_components as html
import string
import os
import json
import numpy as np
from dash.dependencies import Input, Output, State
from matscholar.rest import Rester

# Get the rester and random docs on import
rester = Rester()
local_dir = os.path.dirname(__file__)
with open(os.path.join(local_dir, "../static/data/sample_docs.json"), "r") as f:
    sample_docs = json.load(f)

label_mapping = {
    "MAT": "Material",
    "APL": "Application",
    "PRO": "Property",
    "SPL": "Phase",
    "SMT": "Synthesis",
    "CMT": "Characterization",
    "DSC": "Descriptor",
    "PVL": "Property value",
    "PUT": "Property unit"}

def highlight_entities(tagged_doc):
    highlighted_doc = []
    tagged_doc = [(token, tag) for sent in tagged_doc[0] for (token, tag) in sent]
    for idx, (token, tag) in enumerate(tagged_doc):
        if idx < len(tagged_doc) - 1:
            next_token_punct = True if tagged_doc[idx+1][0] in string.punctuation else False
        else:
            next_token_punct = False
        span = html.Span(token,
                         className="highlighted {}".format(tag),
                         style={"padding-right": "0px" if next_token_punct else "4px",
                                "background-clip": "content-box"})
        highlighted_doc.append(span)
    return highlighted_doc

def get_labels():
    return [html.Span(label_mapping[key],
                      className="highlighted {}".format(key),
                      style={"padding-right": "10px", "background-clip": "content-box"})
            for key in label_mapping]

def bind(app):
    ### Extract App Callbacks ###
    @app.callback(
        Output("extract-highlighted", "children"),
        [Input("extract-button", "n_clicks")],
        [State("extract-textarea", "value"),
         State("normalize-radio", "value")])
    def highlight_extracted(n_clicks, text, normalize):
        if n_clicks is not None:
            return_type = "normalized" if normalize == "yes" else "concatenated"
            tagged_doc = rester.get_ner_tags([text], return_type=return_type)
            highlighted = highlight_entities(tagged_doc)
            return html.Div([html.Div(html.Label("Extracted Entity Tags:")),
                             html.Div(highlighted),
                             html.Div(html.Label("Labels"), style={"padding-top": "15px"}),
                             html.Div(get_labels())])
    @app.callback(
        Output('extract-textarea', 'value'),
        [Input("extract-random", 'n_clicks')])
    def get_random(n_clicks):
        if n_clicks is not None:
            return np.random.choice(sample_docs)
        return ""

