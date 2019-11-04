import inspect
import unittest

import dash_html_components as html

"""
Utilities for running tests.
"""

VALID_PAGES = ["/search", "/extract", "/", "/about", "/journals"]


class MatScholarWebBaseTest(unittest.TestCase):
    def run_test_for_all_functions_in_module(self, module, exclude):
        """
        Run a test for every function in a module.

        Should only be run on components returning html blocks or their
        styling elements.

        Args:
            module (python module): the python module with functions to test
            exclude ([str]): A list of function names as strings to exclude
                from testing.

        Returns:
            None
        """
        functions = get_all_functions_in_module(module)
        for fname, f in functions.items():
            if fname in exclude:
                print(f"Skip: {fname}")
                continue
            else:
                print(f"Test: {fname}")
                params = inspect.signature(f).parameters
                n_args = len(params)
                if n_args == 0:  # this function takes no args
                    o = f()
                    self._basic_type_check_on_function(fname, o)
                else:
                    fake_args = ["arg"] * n_args
                    o = f(*fake_args)
                    self._basic_type_check_on_function(fname, o)

    def run_test_for_individual_arg_combos(self, f, arg_combos):
        """
        Test an individual function with specified argument combinations
        (as tuples).

        Args:
            f (python function): a python function object
            arg_combos ([tuple]): the arguments to test in the function object.
                Only works with positional arguments

        Returns:
            None

        """
        fname = f.__name__
        for arg_combo in arg_combos:
            print(f"Test: {arg_combo} in {fname}")
            o = f(*arg_combo)
            self._basic_type_check_on_function(fname, o)

    def _basic_type_check_on_function(self, fname, o):
        """
        If "_html" is in the name, make sure the function returns an html.Div
        on the function object.

        If "_style" is in the name, make sure the function returns a string
        to use as a className style.

        Otherwise, make sure the function does not return a Div.

        Args:
            fname (str): The name of the functino
            o (object): The output object of the function with fname.

        Returns:
            None

        """
        valid_html_types = (html.Div, html.Span, html.Table)
        if fname.endswith("_html"):
            self.assertTrue(isinstance(o, valid_html_types))
        elif fname.endswith("_style"):
            self.assertTrue(isinstance(o, str))
        else:
            self.assertFalse(isinstance(o, valid_html_types))


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
    name_func_tuples = [
        t for t in name_func_tuples if inspect.getmodule(t[1]) == module
    ]
    functions = dict(name_func_tuples)
    return functions
