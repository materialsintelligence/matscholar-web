import copy
import os

from matscholar import Rester
from matscholar_web.util import load_static_data_file

"""
Load the static files for the dash app once, and not on import of
matscholar_web.

Also define all constants which are used across all apps.
"""

# All static files
db_stats = load_static_data_file("db_statistics.json")
example_searches = load_static_data_file("example_searches.json")
sample_abstracts = load_static_data_file("sample_abstracts.json")


# Artifacts for making tests run easier
fake_endpoint = "not_a_real_endpoint"
fake_api_key = "not_a_real_api_key"

# The API endpoint URL defines the Rester
endpoint = os.environ.get("MATERIALS_SCHOLAR_ENDPOINT", fake_endpoint)
api_key = os.environ.get("MATERIALS_SCHOLAR_API_KEY", fake_api_key)
rester = Rester(endpoint=endpoint, api_key=api_key)


# Artifacts for elastic testing
fake_elastic_credential = "not_a_real_elastic_credential"

# Elasticsearch credentials
elastic_host = os.environ.get("ELASTIC_HOST", fake_elastic_credential)
elastic_user = os.environ.get("ELASTIC_USER", fake_elastic_credential)
elastic_pass = os.environ.get("ELASTIC_PASS", fake_elastic_credential)

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

# The mapping of entity type to color
entity_color_map = {
    "material": "blue",
    "application": "green",
    "property": "orange",
    "phase": "red",
    "synthesis": "turq",
    "characterization": "purple",
    "descriptor": "pink",
}

# The mapping of all search filters
search_filter_color_map = copy.deepcopy(entity_color_map)
search_filter_color_map["text"] = "grey"

# The valid entity types
valid_entity_filters = list(entity_shortcode_map.keys())

# All valid search filter keys
valid_search_filters = valid_entity_filters + ["text"]

# How long before the Flask cache times out and is voided.
cache_timeout = 60

# whether there is an outage or not
outage = bool(int(os.environ.get("MATERIALS_SCHOLAR_OUTAGE", 0)))
