import unittest

from dash.dependencies import Input, Output, State

from matscholar_web.constants import valid_search_filters
from matscholar_web.search.util import parse_search_box, get_search_field_callback_args, MatscholarWebSearchError

"""
Tests for search utilities.
"""

class TestUtils(unittest.TestCase):
    def test_parse_search_box_good(self):
        entity_examples = {
            "material: PbTe": ({"material": ["PbTe"]}, None),
            "application: thermoelectric": ({"application": ["thermoelectric"]}, None),
            "characterization: EDS": ({"characterization": ["EDS"]}, None),
            "property: dielectric constant": ({"property": ["dielectric constant"]}, None),
            "descriptor: thin film": ({"descriptor": ["thin film"]}, None),
            "synthesis: ball milling": ({"synthesis": ["ball milling"]}, None),
            "phase: perovskite": ({"phase": ["perovskite"]}, None),
            "text: whatever": ({}, "whatever"),
        }

        good_example_searches = {
            "phase: diamond, application: thermoelectric, descriptor: thin film": ({"phase": ["diamond"], "application": ["thermoelectric"], "descriptor": ["thin film"]}, None),
            "application: thermoelectric, phase: diamond": ({"phase": ["diamond"], "application": ["thermoelectric"]}, None),
            "phase: diamond application: thermoelectric": ({"phase": ["diamond"], "application": ["thermoelectric"]}, None),
            "phase: diamond, heusler application: thermoelectric": ({"phase": ["diamond", "heusler"],"application": ["thermoelectric"]}, None),
            "characterization: x-ray diffraction, EDS, material: Pb": ({"characterization": ["x-ray diffraction", "EDS"], "material": ["Pb"]}, None),
            "Application: thermoelectric CharaCterizAtion: x-ray diffraction material: PbTe": ({"application": ["thermoelectric"], "characterization": ["x-ray diffraction"], "material": ["PbTe"]}, None),
            "Application: thermoelectric, CharaCterizAtion: x-ray diffraction material: PbTe": ({"application": ["thermoelectric"], "characterization": ["x-ray diffraction"], "material": ["PbTe"]}, None),
            "descriptor:bulk, thin film property:dielectric application: thermoelectric, text: This is some raw text": ({"descriptor": ["bulk", "thin film"], "property": ["dielectric"], "application": ["thermoelectric"]}, "This is some raw text"),
            "descriptor:bulk,    thin film property:    dielectric application:  thermoelectric,     text: This is some raw text": ({"descriptor": ["bulk", "thin film"], "property": ["dielectric"], "application": ["thermoelectric"]}, "This is some raw text")

        }

        good_example_searches.update(entity_examples)

        for search, result in good_example_searches.items():
            test_entitiy_query, test_text = parse_search_box(search)
            true_entity_query, true_text = result[0], result[1]
            self.assertEqual(true_entity_query, test_entitiy_query)
            self.assertEqual(true_text, test_text)

    def test_parse_search_box_bad(self):
        bad_example_searches = [
            "blahblah",
            "1234",
            "",
            "       ",
            "traw: Zintl",
            "phase: diamond, phase: heusler",
            "application:",
            "text:",
            ":",
            "'''",
            "!@#$#$%#$^&%*#@!",
            "!",
            ":::",
            # todo: these are currently parsed but should not be
            # "application: thermoelectric, raw: This is some raw text",
            # "ttext: Zintl",
            # "322asadaphase: Zintl",
        ]

        for search in bad_example_searches:
            with self.assertRaises(MatscholarWebSearchError):
                entity_query, text = parse_search_box(search)
                print(entity_query, text)


    def test_get_search_field_callback_args(self):
        args = get_search_field_callback_args(as_type="input", return_component="value")
        self.assertEqual(len(args), len(valid_search_filters))
        self.assertTrue(all([isinstance(arg, Input) for arg in args]))

        args = get_search_field_callback_args(as_type="output", return_component="value")
        self.assertEqual(len(args), len(valid_search_filters))
        self.assertTrue(all([isinstance(arg, Output) for arg in args]))

        args = get_search_field_callback_args(as_type="state", return_component="value")
        self.assertEqual(len(args), len(valid_search_filters))
        self.assertTrue(all([isinstance(arg, State) for arg in args]))