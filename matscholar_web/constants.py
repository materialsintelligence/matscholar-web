import os
import json

from matscholar import Rester

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

# the absolute path of this root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# in seconds
TIMEOUT = 60

# Stats data, shared among all apps and views
def get_stats_data():
    _topdir = os.path.abspath(os.path.dirname(__file__))
    _target = os.path.abspath(
        os.path.join(_topdir, "assets/data/db_statistics.json")
    )
    with open(_target, "r") as f:
        stats = json.load(f)
    return stats

db_stats = get_stats_data()