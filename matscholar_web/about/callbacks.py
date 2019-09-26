from matscholar_web.constants import rester


def get_n_abstracts():
    current_n_abstracts = "{:0,.0f}".format(rester.get_abstract_count())
    return current_n_abstracts