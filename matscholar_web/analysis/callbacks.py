import dash_html_components as html
import string
import os
import json
import urllib
import numpy as np
from dash.dependencies import Input, Output, State

from matscholar_web.constants import rester

# Get the rester and random docs on import
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
    tagged_doc = [(token, tag) for sent in tagged_doc[0]
                  for (token, tag) in sent]
    for idx, (token, tag) in enumerate(tagged_doc):
        if idx < len(tagged_doc) - 1:
            next_token_punct = True if tagged_doc[idx +
                                                  1][
                                           0] in string.punctuation else False
        else:
            next_token_punct = False
        span = html.Span(token,
                         className="highlighted {}".format(tag),
                         style={
                             "padding-right": "0px" if next_token_punct else "4px",
                             "background-clip": "content-box"})
        highlighted_doc.append(span)
    return highlighted_doc


def get_labels():
    return [html.Span(label_mapping[key],
                      className="highlighted {}".format(key),
                      style={"padding-right": "10px",
                             "background-clip": "content-box"})
            for key in label_mapping]


def highlight_extracted(n_clicks, text, normalize):
    if n_clicks is not None:
        # Extract highlighted
        return_type = "normalized" if normalize == "yes" else "concatenated"
        result = rester.get_ner_tags([text], return_type=return_type)
        tagged_doc = result["tags"]
        relevance = result["relevance"][0]
        highlighted = highlight_entities(tagged_doc)

        # Add the warning
        if not relevance:
            warning = "WARNING!!! Our classifier has flagged this document as not relevant" \
                      " to inorganic materials science. Expect lower than optimum performance."
        else:
            warning = ""

        # Update download link
        doc = {"sentences": []}
        for sent in tagged_doc[0]:
            new_sent = []
            for token, tag in sent:
                new_sent.append({
                    "token": token,
                    "tag": tag
                })
            doc["sentences"].append(new_sent)
        json_string = json.dumps(doc)
        json_string = "data:text/csv;charset=utf-8," + \
                      urllib.parse.quote(json_string)
        return html.Div([html.Div(html.Label("Extracted Entity Tags:")),
                         html.Div(warning, style={
                             "padding-bottom": "20px", "color": "red"}),
                         html.Div(highlighted),
                         html.Div(html.Label("Labels"), style={
                             "padding-top": "15px"}),
                         html.Div(get_labels()),
                         html.Div(html.A("Download entities as json",
                                         id="entity-download-link",
                                         href=json_string,
                                         download="tagged_docs.json",
                                         target="_blank"),
                                  style={"padding-top": "15px"})])


def get_random(n_clicks):
    if n_clicks is not None:
        return np.random.choice(sample_docs)
    return ""
