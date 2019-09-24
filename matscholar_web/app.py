import dash
from flask_caching import Cache

app = dash.Dash(
    # meta_tags=[
    #     {
    #         "name": "viewport",
    #         "content": "width=device-width, initial-scale=1"
    #     }
    # ]
)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True
app.title = "matscholar - rediscover materials"
cache = Cache(app.server, config={'CACHE_TYPE': 'simple'})