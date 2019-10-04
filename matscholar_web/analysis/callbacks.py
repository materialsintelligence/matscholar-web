import os
import json
import numpy as np

from matscholar_web.analysis.view import abstracts_entities_results_html, \
    no_abstract_warning_html

# Get the rester and random docs on import
local_dir = os.path.dirname(__file__)
with open(
        os.path.join(local_dir, "../static/data/extract_app_sample_docs.json"),
        "r") as f:
    sample_docs = json.load(f)


def extracted_results(n_clicks, text, normalize):
    if n_clicks is not None:
        print(str(text).strip() in ["", None], "going to return no abstract")
        if str(text).strip() in ["", None]:
            print("going to return no abstract")
            return no_abstract_warning_html()
        else:
            return abstracts_entities_results_html(text, normalize)
    else:
        return None


def get_random(n_clicks):
    if n_clicks is not None:
        return np.random.choice(sample_docs)
    return ""
