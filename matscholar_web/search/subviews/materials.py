import urllib

import dash_html_components as html
import pandas as pd

from matscholar_web.constants import rester
from matscholar_web.search.common import (
    big_label_and_disclaimer_html,
    common_results_container_style,
    no_results_html,
)

"""
Functions for defining the results container when materials summary is desired.

Please do not define callback logic in this file.
"""

MAX_N_MATERIALS_IN_TABLE = 100  # the maximum number of rows shown in the table
MAX_N_DOIS_FOR_VIEWING = 5  # The maximum number of viewable DOIs on this page.

big_results_label_and_disclaimer = big_label_and_disclaimer_html("materials")
materials_no_results_html = no_results_html(
    pre_label=big_results_label_and_disclaimer
)


def materials_results_html(entity_query, raw_text):
    """
    Get the html block for materials summaru from the Rester-compatible
    entity query and text.

    Args:
        entity_query (dict): The entity query, in Rester-compatible format.
        raw_text (str, None): Any raw text to search for.

    Returns:
        (dash_html_components.Div): The materials summary html block.
    """
    results = rester.materials_search(
        entity_query, text=raw_text, top_k=MAX_N_MATERIALS_IN_TABLE
    )

    if not results:
        return materials_no_results_html
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

        # Prevent results with only oxides or elements from being shown
        # as an empty table
        if df.shape[0] == 0:
            return no_results_html(pre_label=big_results_label_and_disclaimer)

        # Update the download link
        link = make_download_link_from_all_dois_html(df)

        n_filtered_results = df.shape[0]
        if n_filtered_results >= MAX_N_MATERIALS_IN_TABLE:
            label_txt = (
                f"Showing top {MAX_N_MATERIALS_IN_TABLE} of "
                f"{n_filtered_results} materials - download csv for "
                f"full results"
            )
        else:
            label_txt = f"Showing all {n_filtered_results} results."

        label = html.Label(label_txt, className="has-margin-10")

        materials_table = materials_table_html(df, MAX_N_MATERIALS_IN_TABLE)
        materials_html = html.Div(
            children=[
                big_results_label_and_disclaimer,
                label,
                link,
                materials_table,
            ],
            className=common_results_container_style(),
        )
        return materials_html


def materials_table_html(df, limit):
    """
    Get the html block for materials summary table alone from the rester
    results.

    Args:
        df (pd.DataFrame): The pandas dataframe containing all results.
        limit (int): The maximum number of results to show in the table.

    Returns:
        (dash_html_components.Div): The materials summary table only.
    """
    header_material = html.Th("Material")
    header_counts = html.Th("Fraction of Papers")
    header_clickable = html.Th(
        f"Clickable doi links ({MAX_N_DOIS_FOR_VIEWING} examples)"
    )
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
        doi_details, doi_html_link = single_materials_details_html(dois)
        dois_cell = html.Td(doi_details)
        dois_link_cell = html.Td(doi_html_link)

        rows[i] = html.Tr(
            [material_cell, count_cell, dois_cell, dois_link_cell]
        )

    table = html.Table(
        [header] + rows,
        className="table is-fullwidth is-bordered is-hoverable is-narrow is-striped",
    )
    return html.Div(table)


def single_materials_details_html(dois):
    """
    Get the html block for a single material, along with a download link for
    it's full doi list.

    Args:
        dois ([str]): The list of dois for this material.

    Returns:
        details (dash_html_components.Div): The collapsible html block
            containing the clickable doi list for this material.
        download_link(dash_html_components.Div): The download link for all the
            fetched dois.
    """
    dois = dois[:MAX_N_MATERIALS_IN_TABLE]

    viewable_doi_links = []
    for doi in dois:
        link = html.A(
            "{}; ".format(doi),
            href="http://www.doi.org/{}".format(doi),
            target="_blank",
        )
        link_div = html.Div(link)
        viewable_doi_links.append(link_div)

    viewable_doi_links = viewable_doi_links[:MAX_N_DOIS_FOR_VIEWING]

    df = pd.DataFrame({"doi": dois})
    download_link = make_download_link_from_all_dois_html(
        df, f"Download dois as csv"
    )
    summary_txt = f"Show dois?"
    summary = html.Summary([summary_txt])
    details = html.Details([summary] + viewable_doi_links)
    doi_html_link = html.Div(download_link)
    return details, doi_html_link


def make_download_link_from_all_dois_html(df, link_text=None):
    """
    Make a download link html block from the dataframe of all results.
    This is to download all the materials results shown for all materials in
    the results.

    Args:
        df (pd.DataFrame): The dataframe containing columns "material", "count",
            and "dois".
        link_text (str): The text to use as the label for hyperlinking (ie.,
            what you click on to download).

    Returns:
        link (dash_html_components.Div): The link as an html block.
    """
    if not link_text:
        link_text = "Fetch and download all DOIs as CSV"

    csv_string = df.to_csv(index=False, encoding="utf-8")
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(
        csv_string
    )
    link = html.A(
        link_text,
        id="download-link",
        download="matscholar_data.csv",
        href=csv_string,
        target="_blank",
    )
    return link
