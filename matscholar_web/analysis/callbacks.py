import numpy as np

from matscholar_web.analysis.view import abstracts_entities_results_html, \
    no_abstract_warning_html
from matscholar_web.constants import sample_abstracts


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
        return np.random.choice(sample_abstracts)
    return ""
