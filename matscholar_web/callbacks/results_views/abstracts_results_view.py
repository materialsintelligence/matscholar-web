from matscholar import Rester
import dash_html_components as html
import dash_core_components as dcc
import json
import pandas as pd
import urllib
from matscholar_web.base import *


max_results = 50

label_mapping = {
    "material": "MAT_summary",
    "application": "APL_summary",
    "property": "PRO_summary",
    "phase": "SPL_summary",
    "synthesis": "SMT_summary",
    "characterization": "CMT_summary",
    "descriptor": "DSC_summary"}


def abstracts_results_html(*args, **kwargs):
    text = str(args[0][0])
    anonymous_formula = args[0][1]
    element_filters = [s.strip() for s in args[0][2].split(
        ',')] if not args[0][2] in [None, ''] else []
    entities = {f: [s.strip() for s in args[0][i + 3].split(',')] for i, f in enumerate(
        valid_entity_filters) if ((args[0][i + 3] is not None) and (args[0][i + 3].split(',') != ['']))}
    results = rester.abstracts_search(
        entities, text=text, elements=element_filters, top_k=max_results)
    return results_html(results)


def highlight_material(body, material):
    highlighted_phrase = html.Mark(material)
    if len(material) > 0 and material in body:
        chopped = body.split(material)
        newtext = []
        for piece in chopped[:-1]:
            newtext.append(piece)
            newtext.append(highlighted_phrase)
        newtext.append(chopped[-1])
        return newtext
    return body


def generate_nr_results(n):
    """
    Generates a message to be displayed at top of results page.
    Args:
        n (int): Number of results returned.
    Returns:
        (str or list) Message to be displayed.
    """
    if n == 0:
        return "No Results"
    elif n >= max_results:
        return ['Showing {} of > {:,} results. For full results, use the '.format(max_results, n),
                html.A('Matscholar API.', href='https://github.com/materialsintelligence/matscholar')]
    else:
        return 'Showing {} of {:,} results'.format(min(max_results, n), n)


def format_result(result):
    """
    Takes in one row of a dataframe and formats it for display in the
    search results table.
    Title of the paper is the first line
    Author 1, Author 2... - Title of Journal, Year - Publisher
    First 200 characters of abstract.
    Entities
    Args:
        result: Row of dataframe to be formatted for display.
    Returns:
        html.Div of formatted result
    """

    columns = ['title', 'authors', 'year', 'journal', 'abstract', ]

    title = html.Div(html.A(result['title'],
                            href=result["link"],
                            target="_blank",
                            style={"font-size": "120%"}
                            )
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
    authors_journal_and_year = html.Div(ajy, style={"color": "green"})
    abstract = html.Div(result["abstract"])

    entities = []
    for f in valid_entity_filters:
        for e in result[label_mapping[f]]:
            entities.append(html.Span(e,
                                      className="highlighted {}".format(
                                          highlight_mapping[f]),
                                      style={"padding-right": "4px",
                                             "background-clip": "content-box"}))
    entities = html.Div(entities)

    return html.Tr(html.Td(html.Div([title,
                                     authors_journal_and_year,
                                     abstract,
                                     entities])))


def format_authors(author_list):
    if isinstance(author_list, (list, tuple)):
        return(", ".join([format_authors(author) for author in author_list]))
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


def results_html(results, max_rows=max_results):
    columns = ['title', 'authors', 'year',
               'journal', 'abstract']
    formattedColumns = ['Title', 'Authors',
                        'Year', 'Journal', 'Abstract (preview)']
    print(results)
    if results is not None:
        df = pd.DataFrame(results)
    else:
        pd.DataFrame()
    if not df.empty:
        df['authors'] = df['authors'].apply(format_authors)
        hm = highlight_material

        results = [format_result(df.iloc[i])
                   for i in range(min(len(df), max_rows))]
        return html.Div([html.Label(generate_nr_results(len(results)), id="number_results"), html.Table(
            # Header
            # [html.Tr([html.Th(formattedColumns[i]) for i,col in enumerate(columns)])] +
            # Body
            results,
            id="table-element")])
    return html.Div([html.Label(generate_nr_results(len(results)), id="number_results"),
                     html.Table(id="table-element")])
