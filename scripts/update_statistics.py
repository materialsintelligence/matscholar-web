from datetime import datetime

from matscholar_web.constants import rester
"""
Generates the data for showing database statistics (preventing redundant
rester calls and prevent having to do caching nonsense).

Output: /matscholar_web/assets/data/db_statistics.json

To be run by either:
(a) The server host upon deployment (e.g., Heroku postdeploy)
(b) You, the developer, if you haven't set up automatic script running on
    deployments OR you just want to run it locally.
"""

def get_timestamp():
    """
    Get the time now, formatted as YYYY/MM/DD-HH:MM:SS

    Returns:
        (str): The properly formatted date right now.

    """
    now = datetime.now()
    now.strftime("%Y/%m/%d-%H:%M:%S")

def get_debug_stats():
    """
    Get some stats in the same format as the rester but just for debugging
    when the rester is down :(

    Returns:
        (dict): Simulated data which get_live_stats would normally return.

    """
    stats = {
        "materials": 298616,
        "entities": 525690,
        "abstracts": 4951267,
        "journals": [
            "Journal of Materials Chemistry, A",
            "Journal of Materials Chemistry, B",
            "Journal of Materials Chemistry, C",
            "Materials Horizons",
            "Nature",
            "Nature Materials",
            "Computational Materials Science",
            "Journal of Materials, Physics",
            "Science",
            "Nature Machine Intelligence",
            "Physical Review A",
            "Physical Review B",
            "Physical Review Letters",
            "Energy and Environmental Science",
            "Frontiers in Materials",
            "Joule",
            "Matter",
            "Cell",
            "Angewandte Chemie International Edition",
            "Advanced Functional Materials",
            "Chemistry of Materials",
            "Journal of Solid State Chemistry",
            "Apl Materials",
            "Nature Scientific Data",
            "Electrochemistry Communications",
            "Concurrency and Computation"
        ] * 20,
        "timestamp": get_timestamp()

    }


def get_live_stats():
    """
    Get live stats from the database.

    Returns:
        (dict): The stats on the db as python native objects or primitives.

    """
    stats = {}
    for count_type in ["materials", "entities", "abstracts"]:
        n = int(rester.get_db_count(count_type))
        stats[count_type] = n

    stats["journals"] = rester.get_journals()
    stats["timestamp"] = get_timestamp()
    return stats



if __name__ == "__main__":



    print(n_materials)