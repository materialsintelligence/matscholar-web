import inspect

"""
Utilities for running tests.
"""


def get_all_functions_in_module(module):
    """
    Get all the functions in a module.

    Will only get functions defined _in that module_! If they are imported
    from elsewhere they will not be fetched!

    Args:
        module (python module): The module.

    Returns:
        functions ({str: function}): A dictionary of function names and the
            first-class function objects.
    """
    name_func_tuples = inspect.getmembers(module, inspect.isfunction)
    name_func_tuples = [t for t in name_func_tuples if
                        inspect.getmodule(t[1]) == module]
    functions = dict(name_func_tuples)
    return functions
