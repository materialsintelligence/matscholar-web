import unittest

import matscholar_web.extract.view as msweb_eview
from matscholar_web.tests.util import (
    MatScholarWebBaseTest,
    all_rester_requirements_defined,
)

"""
Tests for the extract app view.
"""

# Functions to exclude from this test
EXCLUDE = ["highlight_entities_html", "journal_suggestions_html"]


class TestExtractViews(MatScholarWebBaseTest):
    def test_extract_view(self):
        self.run_test_for_all_functions_in_module(msweb_eview, EXCLUDE)

    def test_highlight_entities_html(self):
        f = msweb_eview.highlight_entities_html
        example_1 = [[["PbTe", "MAT"], ["is", "O"]], [["cool", "O"]]]
        example_2 = [[["testing", "APL"]]]
        examples = [example_1, example_2]
        arg_combos = [(e,) for e in examples]
        self.run_test_for_individual_arg_combos(f, arg_combos)

    @unittest.skipIf(
        not all_rester_requirements_defined, "API access and endpoint not set."
    )
    def test_journal_suggestions_html(self):
        f = msweb_eview.journal_suggestions_html
        text1 = "We derive an effective classical model to describe the Mott transition of the half-filled one-band Hubbard model in the framework of the dynamical mean-field theory with hybridization expansion of the continuous time quantum Monte Carlo. We find a simple two-body interaction of exponential form and reveal a classical correspondence of the Mott transition driven by a logarithmically divergent interaction length. Our paper provides an alternative angle to view the Mott physics and suggests a renewed possibility to extend the application of the quantum-to-classical mapping in understanding condensed-matter physics."
        text2 = "Not a real abstract"
        arg_combos = [(text1,), (text2,)]
        self.run_test_for_individual_arg_combos(f, arg_combos)
