import unittest

import matscholar_web.search.subviews.everything as msweb_ssv
from matscholar_web.constants import api_key, endpoint
from matscholar_web.search.subviews.tests.util import common_arg_combos
from matscholar_web.tests.util import MatScholarWebBaseTest


"""
Tests for the everything subview of search.
"""


class TestSearchEverythingSubview(MatScholarWebBaseTest):
    @unittest.skipIf(
        not api_key and not endpoint, "API access and endpoint not set."
    )
    def test_everything_results_html(self):
        """
        This generally tests everything in the subview since all functions are
        dependent on the single results html.

        Hence we don't need run_test_for_all_functions_in_submodule.
        """
        f = msweb_ssv.everything_results_html
        self.run_test_for_individual_arg_combos(f, common_arg_combos)
