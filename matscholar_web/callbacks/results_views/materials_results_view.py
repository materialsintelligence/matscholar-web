from matscholar import Rester
import dash_html_components as html
import dash_core_components as dcc
import json
import pandas as pd
import urllib
from matscholar_web.base import *


def get_details(dois):
    return html.Details([
        html.Summary('Show dois?'),
        html.Span([html.A("{}; ".format(doi), href="http://www.doi.org/{}".format(doi), target="_blank")
                   for doi in dois[:20]],
                  style={"white-space": "nowrap"})
    ])


def gen_output_matsearch(result):
    table = html.Table(
        [html.Tr([html.Th("Material"), html.Th("Counts"), html.Th("Clickable doi links",
                                                                  style={"white-space": "nowrap"})])] +
        [html.Tr([
            html.Td(mat),
            html.Td(count), html.Td(get_details(dois))])
            for mat, count, dois in result],
        style={"width": "100px"})
    return html.Div(table, style={"width": "100px"})


def gen_df(result):
    mats = [mat for mat, _, _ in result]
    counts = [count for _, count, _ in result]
    dois = [" ".join(dois) for _, _, dois in result]
    df = pd.DataFrame()
    df["Material"] = mats
    df["counts"] = counts
    df["dois"] = dois
    return df


def materials_results_html(*args, **kwargs):
    text = str(args[0][0])
    anonymous_formula = [s.strip() for s in args[0][1].split(
        ',')] if not args[0][1] in [None, ''] else []
    element_filters = [s.strip() for s in args[0][2].split(
        ',')] if not args[0][2] in [None, ''] else []
    entities = {f: [s.strip() for s in args[0][i + 3].split(',')] for i, f in enumerate(
        valid_entity_filters) if ((args[0][i + 3] is not None) and (args[0][i + 3].split(',') != ['']))}
    try:
        entities['material'] = entities['material'] + anonymous_formula
    except KeyError:
        entities['material'] = anonymous_formula
    results = rester.materials_search(
        entities, text=text, elements=element_filters, top_k=None)
    if results is not None:
        result = [(r['material'], r['count'], r['dois']) for r in results
                  if (not r['material'].isupper()) and len(r['material']) > 2 and "oxide" not in r['material']]

        # Update the download link
        df = gen_df(result)
        csv_string = df.to_csv(index=False, encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8," + \
            urllib.parse.quote(csv_string)
        return html.Div([html.Label("Showing top 20 materials - download csv for full results" if df.shape[0] >= 20 else ""),
                         html.A("Download data as csv",
                                id="download-link",
                                download="matscholar_data.csv",
                                href=csv_string,
                                target="_blank"),
                         gen_output_matsearch(result[:20])])
    else:
        return "No Results"