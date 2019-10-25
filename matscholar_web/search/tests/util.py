import unittest

from matscholar_web.search.util import parse_search_box, get_search_field_callback_args, MatscholarWebSearchError


#     An ultra-minimal example set is:
#     example_searches = [
#         # "blahblah", # should fail
#         # "traw: Zintl", # should fail
#         "phase: diamond, application: thermoelectric, descriptor: thin film",
#         "application: thermoelectric, phase: diamond",
#         "phase: diamond application: thermoelectric",
#         "phase: diamond, heusler application: thermoelectric",
#         "phase: diamond, heusler, application: thermoelectric",
#         # "phase: diamond, phase: heusler",  # should fail
#         "characterization: x-ray diffraction, EDS, material: Pb"
#         "Application: thermoelectric CharaCterizAtion: x-ray diffraction material: PbTe"
#     ]


class TestUtils(unittest.TestCase):
    def test_parse_search_box(self):
        bad_example_saerches = [
            "blahblah",
            "traw: Zintl",
            "phase: diamond, phase: heusler",
            "descriptor:bulk, thin film property:dielectric application: thermoelectric, raw: This is some raw text"
        ]

        good_example_searches = {
            "phase: diamond, application: thermoelectric, descriptor: thin film": ({"phase": ["diamond"], "application": ["thermoelectric"], "descriptor": ["thin film"]}, None),
            "application: thermoelectric, phase: diamond": ({"phase": ["diamond"], "application": ["thermoelectric"]}, None),
            "phase: diamond application: thermoelectric": ({"phase": ["diamond"], "application": ["thermoelectric"]}, None),
            "phase: diamond, heusler application: thermoelectric": ({"phase": ["diamond", "heusler"],"application": ["thermoelectric"]}, None),
            "characterization: x-ray diffraction, EDS, material: Pb": ({"characterization": ["x-ray diffraction", "EDS"], "material": ["Pb"]}, None),
            "Application: thermoelectric CharaCterizAtion: x-ray diffraction material: PbTe": ({"application": ["thermoelectric"], "characterization": ["x-ray diffraction"], "material": ["PbTe"]}, None),
            "Application: thermoelectric, CharaCterizAtion: x-ray diffraction material: PbTe": ({"application": ["thermoelectric"], "characterization": ["x-ray diffraction"], "material": ["PbTe"]}, None),
            "descriptor:bulk, thin film property:dielectric application: thermoelectric, text: This is some raw text": ({"descriptor": ["bulk", "thin film"], "property": ["dielectric"], "application": ["thermoelectric"]}, "This is some raw text")
        }



        entity_examples = {
            "material": "PbTe",
            "application": "thermoelectric",
            "characterization": "EDS",
            "property": "dielectric constant",
            "descriptor": "thin film",
            "synthesis": "ball milling",
            "phase": "perovskite"
        }

        for search, result in good_example_searches.items():
            test_entitiy_query, test_text = parse_search_box(search)
            true_entity_query, true_text = result[0], result[1]
            self.assertEqual(true_entity_query, test_entitiy_query)
            self.assertEqual(true_text, test_text)





        # for search in bad_example_saerches:
        #     with self.assertRaises(MatscholarWebSearchError):
        #         parse_search_box(search)
