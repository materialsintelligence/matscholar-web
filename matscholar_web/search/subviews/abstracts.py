import dash_html_components as html
import pandas as pd

from matscholar_web.constants import rester, valid_entity_filters, entity_color_map
from matscholar_web.search.common import common_results_container_style, no_results_html, get_results_label_html

"""
Functions for defining the results container when abstract results are desired.

Please do not define callback logic in this file.
"""

MAX_N_ABSTRACTS_RETRIEVED = 200  # the number of abstracts retrieved via api
MAX_N_ABSTRACTS_SHOWN = 20  # the number of abstracts actually shown


def abstracts_results_html(entity_query, raw_text):
    """
    Get the html block for abstracts results from the Rester-compatible
    entity query and text.

    Args:
        entity_query (dict): The entity query, in Rester-compatible format.
        raw_text (str, None): Any raw text to search for.

    Returns:
        (dash_html_components.Div): The abstracts results html block.

    """
    results = rester.abstracts_search(
        entity_query,
        text=raw_text,
        top_k=MAX_N_ABSTRACTS_RETRIEVED
    )

    if not results:
        return no_results_html()
    else:
        df = pd.DataFrame(results)
        n_raw_results = df.shape[0]

        if df.empty:
            return no_results_html()

        df['authors'] = df['authors'].apply(format_authors)

        n_formatted_results = min(len(df), MAX_N_ABSTRACTS_SHOWN)
        formatted_results = [None] * n_formatted_results

        if n_raw_results >= MAX_N_ABSTRACTS_SHOWN:
            label_txt = \
                f"Showing {n_formatted_results} of many results. For full " \
                f"results, use the "
            label_link = html.A(
                'Matscholar API.',
                href='https://github.com/materialsintelligence/matscholar'
            )
            label = html.Label([label_txt, label_link])
        else:
            label_txt = f"Showing all {n_raw_results} results."
            label = html.Label(label_txt)

        entities_keys = []
        for e in valid_entity_filters:
            color = entity_color_map[e]
            entity_colored = html.Div(e, className=f"msweb-is-{color}-txt is-size-5 has-text-weight-bold")
            entity_key = html.Div(entity_colored, className=f"box has-padding-5")
            entity_key_container = html.Div(entity_key, className="flex-column is-narrow has-margin-5")
            entities_keys.append(entity_key_container)
        entity_key_container = html.Div(entities_keys, className="columns is-multiline has-margin-5")


        for i in range(n_formatted_results):
            formatted_results[i] = format_result_html(df.iloc[i])
        paper_table = html.Table(formatted_results, className="table is-fullwidth is-bordered is-hoverable is-narrow is-striped")

        big_results_label = get_results_label_html("abstracts")
        return html.Div(
            [big_results_label, label, entity_key_container, paper_table],
            className=common_results_container_style()
        )


def format_result_html(result):
    """
    Converts a single row of the abstracts results dataframe and gives back
    the plotly dash html row to be formatted in a table of abstracts.

    Title of the paper is the first line
    Author 1, Author 2... - Title of Journal, Year - Publisher
    First 200 characters of abstract.
    Entities

    Args:
        result (pd.Series: Row of dataframe to be formatted for display.

    Returns:
        (dash_html_components.Tr): The table row html block for the formatted
            result.
    """

    title_link = html.A(
        result['title'],
        href=result["link"],
        target="_blank",
    )

    title = html.Div(
        title_link,
        className="is-size-4 has-text-link has-text-weight-bold"
    )

    # Format the 2nd line "authors - journal, year" with ellipses for overflow
    characters_remaining = 90  # max line length
    characters_remaining -= 5  # spaces, '-', and ','

    year = result['year']
    characters_remaining -= 4

    journal = result['journal']
    if len(journal) > 20:
        journal = journal if len(journal) < 33 else journal[0:30] + "..."
    characters_remaining -= len(journal)

    authors = result["authors"]
    full_author_list = authors.split(", ")
    num_authors = len(full_author_list)
    reduced_author_list = []
    while len(full_author_list) > 0:
        author = full_author_list.pop(0)
        if characters_remaining > len(author):
            reduced_author_list.append(author)
            characters_remaining -= len(author) + 2
    authors = ", ".join(reduced_author_list)
    if len(reduced_author_list) < num_authors:
        authors += "..."

    ajy = "{} - {}, {}".format(authors, journal, year)
    authors_journal_and_year = html.Div(
        ajy,
        className="is-size-5 msweb-is-dark-green-txt"
    )

    abstract_txt = result["abstract"]
    abstract = html.Div(abstract_txt, className="is-size-6")

    label_mapping = {
        "material": "MAT_summary",
        "application": "APL_summary",
        "property": "PRO_summary",
        "phase": "SPL_summary",
        "synthesis": "SMT_summary",
        "characterization": "CMT_summary",
        "descriptor": "DSC_summary"}

    entities = []
    for f in valid_entity_filters:
        for e in result[label_mapping[f]]:
            color = entity_color_map[f]
            ent_txt = html.Span(e, className=f"msweb-is-{color}-txt has-text-weight-semibold")
            entity = html.Div(
                ent_txt,
                className="box has-padding-5"
            )
            entity_container = html.Div(entity, className="flex-column is-narrow has-margin-5")
            entities.append(entity_container)

    entities = html.Div(entities, className="columns is-multiline has-margin-5")

    entities_label = html.Div(
        "Extracted entities:",
        className="has-margin-5 has-text-weight-bold"
    )
    paper_div = html.Div(
        [title, authors_journal_and_year, abstract, entities_label, entities],
        className="has-margin-10"
    )

    table_cell = html.Td(paper_div)
    return html.Tr(table_cell)


def format_authors(author_list):
    """
    Format the authors to a readable list for later formatting.

    Args:
        author_list (str, [str]): The "dirty" list of strings or string
            containing all author names.

    Returns:
        [str]: The "clean" list of author names.
    """
    if isinstance(author_list, (list, tuple)):
        return ", ".join([format_authors(author) for author in author_list])
    else:
        if ", " in author_list:
            author_list = author_list.split(", ")
            author_list.reverse()
            author_list = " ".join(author_list)
        elif "," in author_list:
            author_list = author_list.split(",")
            author_list.reverse()
            author_list = " ".join(author_list)
        return author_list