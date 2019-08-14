from matscholar import Rester

# Define some variables of common interest
rester = Rester()
valid_entity_filters = ["material", "property", "application",
                        "descriptor", "characterization", "synthesis", "phase"]

highlight_mapping = {
    "material": "MAT",
    "application": "APL",
    "property": "PRO",
    "phase": "SPL",
    "synthesis": "SMT",
    "characterization": "CMT",
    "descriptor": "DSC"}
