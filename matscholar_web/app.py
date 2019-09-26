import dash
from flask_caching import Cache

"""
A safe place for the dash app to hang out.
"""

app = dash.Dash()
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True
app.title = "matscholar - rediscover materials"
cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})