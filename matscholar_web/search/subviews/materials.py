import urllib

import pandas as pd
import dash_html_components as html

from matscholar_web.constants import rester
from matscholar_web.search.util import parse_search_box
from matscholar_web.search.common import no_results_html, \
    results_container_class, get_results_label_html

MAX_N_MATERIALS_IN_TABLE = 100
MAX_N_DOIS_FOR_VIEWING = 5


def materials_results_html(entity_query, raw_text):
    results = rester.materials_search(entity_query, text=raw_text, top_k=MAX_N_MATERIALS_IN_TABLE)
    if not results:
        return no_results_html()
    else:
        materials = []
        counts = []
        dois = []

        for i, r in enumerate(results):
            material = r["material"]
            elemental = len(material) <= 2
            oxide = "oxide" in material
            uppercase = material.isupper()
            if not uppercase and not oxide and not elemental:
                materials.append(material)
                counts.append(r["count"])
                dois.append(r["dois"])


        df = pd.DataFrame(
            {"material": materials, "count": counts, "dois": dois}
        )

        # Update the download link
        link = get_csv_download_link_from_df(df)

        n_filtered_results = df.shape[0]
        if n_filtered_results >= MAX_N_MATERIALS_IN_TABLE:
            label_txt = f"Showing top {MAX_N_MATERIALS_IN_TABLE} of " \
                        f"{n_filtered_results} materials - download csv for " \
                        f"full results"
        else:
            label_txt = f"Showing all {n_filtered_results} results."

        label = html.Label(label_txt, className="has-margin-10")

        # reformatted_result = [(materials[i], counts[i], dois[i]) for i in range(n_filtered_results)]


        materials_table = get_materials_table(df, MAX_N_MATERIALS_IN_TABLE)
        big_results_label = get_results_label_html("materials")
        materials_html = html.Div(
            children=[big_results_label, label, link, materials_table],
            className=results_container_class()
        )
        return materials_html


def get_materials_table(df, limit):
    header_material = html.Th("Material")
    header_counts = html.Th("Count")
    header_clickable = html.Th(f"Clickable doi links ({MAX_N_DOIS_FOR_VIEWING} examples)")
    header_downloadable = html.Th("Download all dois as file")

    header = html.Tr(
        [header_material, header_counts, header_clickable, header_downloadable]
    )

    n_results = min(df.shape[0], limit)

    rows = [None] * n_results
    for i in range(n_results):
        material_cell = html.Td(df["material"].iloc[i])
        count_cell = html.Td(df["count"].iloc[i])

        dois = df["dois"].iloc[i]
        doi_details, doi_html_link = get_details(dois)
        dois_cell = html.Td(doi_details)
        dois_link_cell = html.Td(doi_html_link)

        rows[i] = html.Tr([material_cell, count_cell, dois_cell, dois_link_cell])

    table = html.Table([header] + rows, className="table is-fullwidth is-bordered is-hoverable is-narrow is-striped")
    return html.Div(table)

def get_details(dois):
    dois = dois[:MAX_N_MATERIALS_IN_TABLE]

    viewable_doi_links = []
    for doi in dois:
        link = html.A(
            "{}; ".format(doi),
            href = "http://www.doi.org/{}".format(doi),
            target = "_blank"
        )
        link_div = html.Div(link)
        viewable_doi_links.append(link_div)

    viewable_doi_links = viewable_doi_links[:MAX_N_DOIS_FOR_VIEWING]

    df = pd.DataFrame({"doi": dois})
    download_link = get_csv_download_link_from_df(
        df,
        f"Download dois as csv"
    )

    summary_txt = f'Show dois?'
    summary = html.Summary([summary_txt])
    details = html.Details([summary] + viewable_doi_links)
    doi_html_link = html.Div(download_link)
    return details, doi_html_link

def get_csv_download_link_from_df(df, link_text=None):
    if not link_text:
        link_text = "Fetch and download all DOIs as CSV"

    csv_string = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + \
                 urllib.parse.quote(csv_string)
    link = html.A(
        link_text,
        id="download-link",
        download="matscholar_data.csv",
        href=csv_string,
        target="_blank"
    )
    return link