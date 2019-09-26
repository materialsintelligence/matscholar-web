from matscholar_web.constants import rester


def get_n_abstracts():
    count = rester.get_abstract_count()

    # take care of rester error in the meantime
    if count == 0:
        count = 3000000

    current_n_abstracts = "{:0,.0f}".format(count)
    return current_n_abstracts
