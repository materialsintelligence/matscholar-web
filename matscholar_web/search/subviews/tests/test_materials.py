import unittest

from matscholar_web.tests.util import MatScholarWebBaseTest
import matscholar_web.search.subviews.materials as msweb_ssm
from matscholar_web.constants import api_key, endpoint

"""
Tests for the abstracts subview of search.
"""

# Functions to exclude from this test
EXCLUDE = []


class TestSearchMaterialsSubview(MatScholarWebBaseTest):
    def test_materials_subviews(self):
        self.run_test_for_all_functions_in_module(msweb_ssm, EXCLUDE)

    @unittest.skipIf(not api_key and not endpoint, "API access and endpoint not set.")
    def test_materials_results_html(self):
        f = msweb_ssm.materials_results_html

        arg_combos = [
            ({"material": ["PbTe", "SnSe"]}, None),
            ({"characterization": ["positron"]}, "positron emission tomography"),
            ({"material": ["graphene"], "descriptor": ["doped"]}, None),
            ({}, "Ceder")

        ]
        self.run_test_for_individual_arg_combos(f, arg_combos)
