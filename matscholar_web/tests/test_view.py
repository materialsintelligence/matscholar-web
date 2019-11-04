import matscholar_web.view as msweb_view
from matscholar_web.tests.util import VALID_PAGES, MatScholarWebBaseTest


"""
Tests for the core dash view.
"""


class TestCoreView(MatScholarWebBaseTest):
    def test_core_views(self):
        self.run_test_for_all_functions_in_module(
            msweb_view, exclude=["nav_html"]
        )

    def test_nav_bar(self):
        f = msweb_view.nav_html
        arg_combos = [(v,) for v in VALID_PAGES]
        self.run_test_for_individual_arg_combos(f, arg_combos)

        with self.assertRaises(ValueError):
            f("/not_a_real_valid_web_url_path")
