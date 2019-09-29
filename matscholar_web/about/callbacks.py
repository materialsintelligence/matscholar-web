from matscholar_web.constants import rester


def get_n_abstracts():

    try:
        count = rester.get_abstract_count()
    except:
        count = 0

    # take care of rester error in the meantime
    if count == 0:
        count = 5000000

    current_n_abstracts = "{:0,.0f}".format(count)
    return current_n_abstracts
