import numpy as np

from matscholar_web.constants import sample_abstracts
from matscholar_web.extract.view import (
    extract_entities_results_html,
    no_abstract_warning_html,
    journal_suggestions_html,
)

"""
Callback logic for callbacks in the extract app.

Please do not define any html blocks in this file.
"""


def extracted_results(
    extract_button_n_clicks, suggest_button_n_clicks, text, normalize
):
    """
    Get the extracted entities or the journal suggestion results from the
    extract app via clicks and the entered text, along with the
    normalize dropdown.

    Args:
        extract_button_n_clicks (int): The number of clicks of the extract
            button.
        suggest_button_n_clicks (int): the number of clicks of the suggest
            button
        text (str): The text entered in the text box, to extract.
        normalize (bool): The normalize string to pass to the rester.

    Returns:
        (dash_html_components, str): The extracted results html block.
    """
    if extract_button_n_clicks is None and suggest_button_n_clicks is None:
        return ""
    else:
        stripped = text if not text else text.strip()
        if stripped in [None, ""]:
            return no_abstract_warning_html()
        else:
            if (
                extract_button_n_clicks is not None
                and extract_button_n_clicks > 0
            ):
                return extract_entities_results_html(text, normalize)
            elif (
                suggest_button_n_clicks is not None
                and suggest_button_n_clicks > 0
            ):
                return journal_suggestions_html(text)
            else:
                return ""


def get_random_abstract(random_button_n_clicks):
    """
    Get a random abstract for the random button.

    Args:
        random_button_n_clicks (int): The number of clicks of the random button.

    Returns:
        (str): The text of a random abstract.

    """
    if random_button_n_clicks not in [None, 0]:
        return np.random.choice(sample_abstracts)
    return ""
