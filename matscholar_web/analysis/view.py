import json
import copy
import urllib

import dash_html_components as html
import dash_core_components as dcc
from matscholar.rest import MatScholarRestError

from matscholar_web.common import get_logo_html
from matscholar_web.common import common_null_warning_html, \
    common_warning_html, common_rester_error_html
from matscholar_web.constants import rester, entity_color_map

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

entitiy_color_map_extension = {
    "property value": "aqua",
    "property unit": "yellow",
    "other": None
}

entity_color_map_extended = copy.deepcopy(entity_color_map)
entity_color_map_extended.update(entitiy_color_map_extension)


def app_view_html():
    label = html.Label(
        "Enter a scientific abstract's text for named entity extraction:",
        className="is-size-4"
    )
    label_container = html.Div(label, className="has-margin-bottom-20 has-text-centered")

    text_area = dcc.Textarea(
        id="extract-textarea",
        spellCheck=True,
        placeholder="Paste abstract/other text here to extract named entities.",
        className="input is-info is-medium has-min-height-250"
    )
    text_area_div = html.Div(text_area, className="has-margin-5")

    convert_synonyms = dcc.Dropdown(id="dropdown_normalize",
                                    options=[
                                        {'label': "No", 'value': "no"},
                                        {"label": "Yes", "value": "yes"}
                                    ],
                                    value='no',
                                    clearable=False
                                    )

    convert_synonyms_text = html.Div("Convert synonyms?", className="is-size-6")
    convert_synonyms_container = html.Div(
        [convert_synonyms_text, convert_synonyms],
        className="is-pulled-right has-margin-5",
    )


    common_button_styling = "button is-size-4 has-margin-5"
    extract_button = html.Button(
        "Extract entities",
        id="extract-button",
        className=f"{common_button_styling} is-link"
    )

    random_abstract_button = html.Button(
        "Example",
        id="extract-random",
        className=f"{common_button_styling} is-light"
    )


    loading = dcc.Loading(
        id="loading-extract",
        children=[
            html.Div(id="extract-highlighted"),
            html.Div(id="extracted")
        ],
        type="cube",
        color="#21ff0d",
        className="msweb-fade-in"
    )

    loading_container = html.Div(loading)

    logo = get_logo_html()

    main_app_column = html.Div(
        [
            label_container,
            text_area_div,
            convert_synonyms_container,
            extract_button,
            random_abstract_button,
            loading_container
        ],
        className="column is-three-quarters"
    )

    main_app_columns = html.Div(
        [main_app_column], className="columns is-centered"
    )

    layout = html.Div(
        [
            logo,
            main_app_columns
        ],
        className="container has-margin-top-50"
    )
    return layout


def abstracts_entities_results_html(text, normalize):
    # Extract highlighted
    try:
        result = rester.get_ner_tags(text, concatenate=True, normalize=normalize)
    except MatScholarRestError:
        rester_error_txt = \
            "Our server is having trouble with that abstract. We are likely " \
            "undergoing maintenance, check back soon!"
        return common_rester_error_html(rester_error_txt)
    tagged_doc = result["tags"]
    relevance = result["relevance"]
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
    for sent in tagged_doc:
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

    entity_colormap_key = copy.deepcopy(entity_color_map_extended)
    entities_keys = []
    for e, color in entity_colormap_key.items():
        # don't need the "other" label
        if e == "other":
            continue
        entity_key = html.Div(e, className=f"is-size-4 msweb-is-{color}-txt has-text-weight-bold")
        entity_key_container = html.Div(
            entity_key,
            className="flex-column is-narrow has-margin-5 box"
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


def highlight_entities(tagged_doc):
    tagged_flat1 = [i for sublist in tagged_doc for i in sublist]
    # tagged_flat2 = [j for sublist in tagged_flat1 for j in sublist]
    tagged_doc = tagged_flat1

    text_size = "is-size-5"

    entities_containers = [None] * len(tagged_doc)

    for i, tagged_token in enumerate(tagged_doc):
        token, tag = tagged_token[0], tagged_token[1]
        color = entity_color_map_extended[label_mapping[tag]]

        if color is None:
            entity_styled = html.Div(f" {token} ", className=text_size)
            entity_container = html.Div(
                entity_styled,
                className="flex-column is-narrow has-margin-left-5 has-margin-right-5"
            )
        else:
            # the entity is other and we need to not highlight it
            entity_styled = html.Div(
                token,
                # className=f"button is-{color} is-outlined {text_size}"
                className=f"msweb-is-{color}-txt {text_size}"
            )

            entity_container = html.Div(
                entity_styled,
                className="flex-column is-narrow has-margin-left-5 has-margin-right-5 has-text-weight-bold"
            )
        entities_containers[i] = entity_container
    entities = html.Div(
        entities_containers,
        className="columns is-multiline has-margin-5"
    )
    return entities


def no_abstract_warning_html():
    return common_null_warning_html("No abstract entered!")
