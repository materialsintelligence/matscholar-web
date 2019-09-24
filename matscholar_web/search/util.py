from dash.dependencies import Input, Output, State
from matscholar_web.constants import valid_entity_filters


def get_entity_boxes_callback_args(as_type="state"):
    """
    Return all available entity boxes as Inputs, Outputs, or States.

    Args:
        as_type (str): "state" for State, "input" for Input, or "output" for
            Output

    Returns:
        (list): The list of inputs, states, or outputs plotly dash dependency
            objects on the search page.
    """
    type_dict = {
        "state": State,
        "output": Output,
        "input": Input
    }
    t = type_dict[as_type]
    return [t(f + '_filters_input', 'value') for f in valid_entity_filters]
