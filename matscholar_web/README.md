# Structure of the project

## The `/` folder

Running the app.
```
/app.py
```
```
(my_virtualenv) python app.py
```

## The `/matscholar_web` folder
The assets folder is special. The other folders are modular apps. 
The python files are common parts of the website across all apps.
```
matscholar_web
├── about          # about app
├── analysis       # analysis app
├── app.py         # the core dash instance. don't mess with this
├── assets         # static assets, not an app.
├── common.py      # common html-defining functions among all apps or main view
├── constants.py   # constant quantities
├── footer.py      # the footer
├── index.py       # (IMPORTANT): all high-level callback I/Os and the main layout of the webpage.
├── journals       # the journals app
├── logo.py        # the logo
├── nav.py         # the nav bar
├── search         # the search app
└── util.py        # non-html defining util functions
```

Please keep the functions which return dash html blocks (e.g., those in 
`common.py`) and those which do not (e.g., `util.py`) **separate** and 
in the correct file in a logical manner.


## Inside an app folder

In this example we'll show the most complex app, `search`.

Other apps may not have all the parts here. But no forseeable app should
require more than the 4 files here (outside of the subviews folder).

```
search
├── callbacks.py   # the callbacks
├── common.py      # common html-defining functions among all views
├── subviews       # add a modular view here if your view.py gets too long
├── util.py        # non html-defining util functions
└── view.py        # html-defining functions defining the layout of the app. 
```

### Files with functions defining dash HTML blocks
***Only* functions which define html blocks should be found in these files.**

#### `common.py`
Common functions for defining *dash html blocks* among one or more views.
**Every** function in this file should define a dash html block.

#### `view.py`
Dash html-defining functions defining the main layout of the app. May 
call functions from `subviews` module. **Must** define a `serve_layout` 
function which defines the entire app in an html block.

#### All files in `subviews`
Each file in subviews defines html-defining functions which are used
in a modular fashion by the `view.py` file in the app. You don't need
to use `subviews` if everything can fit in your `view.py` file.
```
subviews
├── abstracts.py
├── entities.py
├── everything.py
└── materials.py
```

### Files with functions *not* defining dash HTML blocks
***No* functions which return html blocks should be found in these files.**

#### `callbacks.py`
Defines the core callback logic for the html elements laid out in this
app's `view.py` and `subviews`. **Should not define any html elements
itself - only reference those from view, subviews, and common.**

#### `util.py`
Common functions for processing and defining non-html blocks. **No**
function in this file should define a dash html block.



# Running this app:
The following environment variables must be defined:

- ELASTIC_HOST - The ElasticSearch host url
- ELASTIC_PASS - The ElasticSearch host password
- ELASTIC_USER - The ElasticSearch username
- MATERIALS_SCHOLAR_API_KEY - The Matscholar API key to use in the rester
- MATERIALS_SCHOLAR_ENDPOINT - The API endpoint URL for Matscholar
- MATERIALS_SCHOLAR_WEB_USER (not needed) - for frontend-based auth
- MATERIALS_SCHOLAR_WEB_PASS (not needed) - for frontend-based auth
- TF_SERVING_URL - The url serving the NER tensorflow model.