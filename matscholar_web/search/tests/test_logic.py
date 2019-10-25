from matscholar_web.constants import valid_search_filters
from matscholar_web.search.logic import (
    search_bar_live_display,
    sum_all_fields_and_buttons_n_submits,
)
from matscholar_web.tests.util import MatScholarWebBaseTest


"""
Tests for the main search callback logic.
"""


class TestSearchLogic(MatScholarWebBaseTest):
    def test_show_search_results(self):
        pass

    def test_sum_all_fields_and_buttons_n_submits(self):
        n_fields = len(valid_search_filters)
        all_n_clicks = [0] * n_fields
        self.assertEqual(
            0, sum_all_fields_and_buttons_n_submits(*all_n_clicks)
        )
        all_n_clicks = [None] * n_fields
        self.assertEqual(
            0, sum_all_fields_and_buttons_n_submits(*all_n_clicks)
        )
        all_n_clicks = [0] * n_fields
        all_n_clicks[2] = None
        self.assertEqual(
            0, sum_all_fields_and_buttons_n_submits(*all_n_clicks)
        )
        all_n_clicks[1] = 1
        self.assertEqual(
            1, sum_all_fields_and_buttons_n_submits(*all_n_clicks)
        )
        all_n_clicks = [1] * n_fields
        self.assertEqual(
            n_fields, sum_all_fields_and_buttons_n_submits(*all_n_clicks)
        )

    def test_search_bar_live_display(self):
        test_txt_src = "abcdefghi"
        ent_txts = [
            test_txt_src[i] for i, _ in enumerate(valid_search_filters)
        ]
        n_clicks = 0
        display = search_bar_live_display(n_clicks, *ent_txts)
        truth = [
            f"{valid_search_filters[i]}: {test_txt_src[i]}"
            for i, _ in enumerate(valid_search_filters)
        ]
        truth = ", ".join(truth) + ","
        self.assertEqual(truth.strip(), display.strip())
