import dash
from flask_caching import Cache

"""
A safe place for the dash app to hang out.
"""

# Any external js scripts you need to define.
external_scripts = [
    "https://www.googletagmanager.com/gtag/js?id=UA-149443072-1"
]

app = dash.Dash(
    __name__,
    external_scripts=external_scripts
)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True
app.title = "matscholar - rediscover materials"
cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})

