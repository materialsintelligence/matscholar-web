import os
import json
import numpy as np

from matscholar_web.analysis.view import abstracts_entities_results_html, \
    no_abstract_warning_html

# Get the rester and random docs on import
local_dir = os.path.dirname(os.path.abspath(__file__))
filename = os.path.join(local_dir, "../assets/data/sample_abstracts.json")
with open(filename, "r") as f:
    sample_docs = json.load(f)

def extracted_results(n_clicks, text, normalize):
    if n_clicks is not None:
        stripped = text if not text else text.strip()
        if stripped in [None, ""]:
            return no_abstract_warning_html()
        else:
            return abstracts_entities_results_html(text, normalize)
    else:
        return ""


def get_random(n_clicks):
    if n_clicks is not None:
        return np.random.choice(sample_docs)
    return ""
