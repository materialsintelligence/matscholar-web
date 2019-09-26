import dash_html_components as html
import os
import json
import urllib
import copy
import numpy as np

from matscholar_web.common import common_warning_html
from matscholar_web.constants import rester, entity_color_map_bulma

# Get the rester and random docs on import
local_dir = os.path.dirname(__file__)
with open(
        os.path.join(local_dir, "../static/data/extract_app_sample_docs.json"),
        "r") as f:
    sample_docs = json.load(f)

label_mapping = {
    "MAT": "material",
    "APL": "application",
    "PRO": "property",
    "SPL": "phase",
    "SMT": "synthesis",
    "CMT": "characterization",
    "DSC": "descriptor",
    "PVL": "property value",
    "PUT": "property unit",
    "O": 'other'
}

# "material": "primary",
# "application": "info",
# "property": "dark",
# "phase": "success",
# "synthesis": "link",
# "characterization": "danger",
# "descriptor": "light"

entitiy_color_map_bulma_extension = {
    "property value": "dark",
    "property unit": "black",
    "other": "white"
}

entity_color_map_bulma_extended = copy.deepcopy(entity_color_map_bulma)
entity_color_map_bulma_extended.update(entitiy_color_map_bulma_extension)


def extracted_results(n_clicks, text, normalize):
    if n_clicks is not None:
        # Extract highlighted
        return_type = "normalized" if normalize == "yes" else "concatenated"
        result = rester.get_ner_tags([text], return_type=return_type)
        tagged_doc = result["tags"]
        relevance = result["relevance"][0]
        highlighted = highlight_entities(tagged_doc)

        # Add the warning
        if not relevance:
            warning_header_txt = "Warning! Abstract not relevant."
            warning_body_txt = \
                "Our classifier has flagged this document as not relevant to " \
                "inorganic materials science. Expect lower than optimum " \
                "performance."
            warning = common_warning_html(warning_header_txt, warning_body_txt)
        else:
            warning = html.Div("")

        # Update download link
        doc = {"sentences": []}
        for sent in tagged_doc[0]:
            new_sent = []
            for token, tag in sent:
                new_sent.append({"token": token, "tag": tag})
            doc["sentences"].append(new_sent)
        json_string = json.dumps(doc)
        json_string = "data:text/csv;charset=utf-8," + \
                      urllib.parse.quote(json_string)
        download_link = html.A(
            "Download entities as json",
            id="entity-download-link",
            href=json_string,
            download="tagged_docs.json",
            target="_blank"
        )
        download_container = html.Div(
            download_link,
            className="has-text-size-4 has-margin-top 10"
        )

        label = html.Label("Extracted Entity Tags:")
        label_container = html.Div(label,
                                   className="is-size-4 has-margin-top-30")

        highlighted_container = html.Div(highlighted)

        label_label = html.Label("Labels:")
        label_label_container = html.Div(label_label,
                                         className="is-size-4 has-margin-top-30")

        entity_colormap_key = copy.deepcopy(entity_color_map_bulma_extended)
        entities_keys = []
        for e, color in entity_colormap_key.items():
            entity_key = html.Div(e, className=f"button is-{color} is-active")
            entity_key_container = html.Div(
                entity_key,
                className="flex-column is-narrow has-margin-5"
            )
            entities_keys.append(entity_key_container)

        entity_key_container = html.Div(
            entities_keys,
            className="columns is-multiline has-margin-5"
        )

        results = html.Div(
            [
                warning,
                label_container,
                highlighted_container,
                label_label_container,
                entity_key_container,
                download_container
            ]
        )
        return results
    else:
        return None


def highlight_entities(tagged_doc):
    tagged_flat1 = [i for sublist in tagged_doc for i in sublist]
    tagged_flat2 = [j for sublist in tagged_flat1 for j in sublist]
    tagged_doc = tagged_flat2

    text_size = "is-size-6"

    entities_containers = [None] * len(tagged_doc)

    for i, tagged_token in enumerate(tagged_doc):
        token, tag = tagged_token[0], tagged_token[1]
        color = entity_color_map_bulma_extended[label_mapping[tag]]

        if color == "white":
            entity_styled = html.Div(f" {token} ", className=text_size)
            entity_container = html.Div(
                entity_styled,
                className="flex-column is-narrow has-margin-5"
            )
        else:
            # the entity is other and we need to not highlight it
            entity_styled = html.Div(
                token,
                className=f"button is-{color} is-active {text_size}"
            )

            entity_container = html.Div(
                entity_styled,
                className="flex-column is-narrow has-margin-5"
            )
        entities_containers[i] = entity_container
    entities = html.Div(
        entities_containers,
        className="columns is-multiline has-margin-5"
    )
    return entities


def get_random(n_clicks):
    if n_clicks is not None:
        return np.random.choice(sample_docs)
    return ""
