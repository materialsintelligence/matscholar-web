import os
import copy

from matscholar import Rester

from matscholar_web.util import load_static_data_file

# Define some variables of common interest
endpoint = os.environ.get("MATERIALS_SCHOLAR_ENDPOINT")
rester = Rester(endpoint=endpoint)

# The mapping of entity type to shortcode
entity_shortcode_map = {
    "material": "MAT",
    "characterization": "CMT",
    "property": "PRO",
    "synthesis": "SMT",
    "application": "APL",
    "descriptor": "DSC",
    "phase": "SPL",

}

entity_color_map_bulma = {
    "material": "blue",
    "application": "green",
    "property": "orange",
    "phase": "red",
    "synthesis": "turq",
    "characterization": "purple",
    "descriptor": "pink"
}

search_filter_color_map = copy.deepcopy(entity_color_map_bulma)
search_filter_color_map["raw"] = "grey"

# The valid entity types
valid_entity_filters = list(entity_shortcode_map.keys())

valid_search_filters = valid_entity_filters + ["raw"]

# in seconds
cache_timeout = 60

# Static files
db_stats = load_static_data_file("db_statistics.json")
example_searches = load_static_data_file("example_searches.json")
sample_abstracts = load_static_data_file("sample_abstracts.json")