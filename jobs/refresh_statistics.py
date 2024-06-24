import json
import os
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from matscholar_web.constants import rester

"""
Generates the data for showing database statistics (preventing redundant
rester calls and prevent having to do caching nonsense).

Output: /matscholar_web/assets/data/db_statistics.json

To be run by either:
(a) The server host running a cronjob or scheduled job automatically
(b) You, the developer, if you haven't set up automatic script running on
    deployments OR you just want to run it locally.
"""

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=17)
def scheduled_job():
    update_live_stats()


def get_timestamp():
    """
    Get the time now, formatted as YYYY/MM/DD-HH:MM:SS

    Returns:
        (str): The properly formatted date right now.

    """
    now = datetime.now()
    return now.strftime("%Y/%m/%d-%H:%M:%S")


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
                        "Concurrency and Computation",
                    ]
                    * 10,
        "timestamp": get_timestamp(),
    }
    return stats


def get_live_stats():
    """
    Get live stats from the database.

    Returns:
        (dict): The stats on the db as python native objects or primitives.

    """
    rstats = rester.get_db_stats()
    fstats = {
        "abstracts": rstats["abstract_count"],
        "materials": rstats["materials_count"],
        "entities": rstats["entities_count"],
        "journals": rester.get_journals(),
        # "journal": None,
        "timestamp": get_timestamp(),
    }

    return fstats


def update_live_stats(debug=False):
    stats = get_debug_stats() if debug else get_live_stats()

    # print(stats)

    thisdir = os.path.abspath(os.path.dirname(__file__))
    target = os.path.abspath(
        os.path.join(
            thisdir, "../matscholar_web/assets/data/db_statistics.json"
        )
    )

    with open(target, "w") as f:
        json.dump(stats, f)

    timestamp = stats["timestamp"]
    print(f"Statistics updated successfully at {timestamp}")


if __name__ == "__main__":
    # Have server deployment run automatically
    sched.start()

    # Generate it locally, manually
    # update_live_stats()
