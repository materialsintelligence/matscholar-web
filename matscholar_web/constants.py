import os

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
    "material": "primary",
    "application": "info",
    "property": "dark",
    "phase": "success",
    "synthesis": "link",
    "characterization": "danger",
    "descriptor": "warning"
}


# The valid entity types
valid_entity_filters = list(entity_shortcode_map.keys())

# in seconds
TIMEOUT = 60

# Static files
db_stats = load_static_data_file("db_statistics.json")
example_searches = load_static_data_file("example_searches.json")
sample_abstracts = load_static_data_file("sample_abstracts.json")