import os
from matscholar import Rester

# Define some variables of common interest
rester = Rester(endpoint="https://staging.matscholar.com")

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