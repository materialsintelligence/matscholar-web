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

def get_debug_stats():
    """
    Get some stats in the same format as the rester but just for debugging
    when the rester is down :(

    Returns:
        (dict): Simulated data which the rester would normally return.

    """

if __name__ == "__main__":
    stats = {}
    for count_type in ["materials", "entities", "abstracts"]:
        n = int(rester.get_db_count(count_type))
        stats[count_type] = n


    print(n_materials)