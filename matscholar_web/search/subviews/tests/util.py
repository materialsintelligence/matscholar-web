from matscholar_web.constants import (
    api_key,
    endpoint,
    fake_api_key,
    fake_endpoint,
)

# Argument combinations valid for all subviews test functions.

common_arg_combos = [
    ({"material": ["PbTe", "SnSe"]}, None),
    ({"characterization": ["positron"]}, "positron emission tomography"),
    ({"material": ["graphene"], "descriptor": ["doped"]}, None),
    ({}, "Ceder"),
]

all_rester_requirements_defined = (
    api_key
    and endpoint
    and api_key != fake_api_key
    and endpoint != fake_endpoint
)
