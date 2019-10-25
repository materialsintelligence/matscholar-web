# Contributing to matscholar_web

#### Development on this repository is limited to internal collaborators at this time.

### Internal collaborators: how to make a PR

- Use the Google Code style for all of your code. Find an example [here.](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html)
- Your code should have (4) spaces instead of tabs.
- **Write tests** for new features! Good tests are 100%, absolutely necessary for good code. We use the python `unittest` framework -- see some of the other tests in this repo for examples, or review the [Hitchhiker's guide to python](https://docs.python-guide.org/writing/tests/) for some good resources on writing good tests.
- Understand your contributions will fall under the same license as this repo.

When you submit your PR, our CI service will automatically run your tests.
We welcome good discussion on the best ways to write your code, and the comments on your PR are an excellent area for discussion.

#### References
This document was adapted from the open-source contribution guidelines for Facebook's Draft, as well as briandk's [contribution template](https://gist.github.com/briandk/3d2e8b3ec8daf5a27a62).


# Structure of the project

## General
Views (html-defining functions) and callback logic is separated. Apps 
are modular and are self contained in their app folders. All apps generally
follow the same scheme for file naming and structure. The `matscholar_web/app.py`
file houses all the callbacks and individual apps define the callback logic.

### Naming
- Functions defining dash html components or core components should end with `_html`
- Functions defining styles should end with `_style`


#### Callback element IDs:

Our Dash element ids are set according to a **strict** naming scheme. Please adhere to it.

- Only use hyphens for separating words, not underscores. This is to make them easily searchable and replaceble in text even if a related Python variable is similarly named.
- `"core-*"`: ids on the main page, regardless of app.
- `"search-*"`: ids on the search app
- `"extract-*"`: ids on the extract app
- `"about-*"`: ids on the about app
- `"journal-*"`: ids on the journal app
- `"*-cs"`: indicates an id is used in a clientside callback. Probably don't
    mess with it!
- `"*-hidden-ref*"`: A hidden reference for another id.

#### View files (html-defining functions)
- `view.py` files are for the views (html-defining functions)
- `subviews` submodules are for if the view file gets too long
- `common.py` files are for commonly used html views

#### Callback and logic files (no html-defining functions)
- `logic.py` the callback logic for all callbacks
- `util.py` utils helping the callback logic or views

This structure is consistent across all the apps. It is mostly consistent across the top level directory except for `logic` which is encapsulated by the little needed logic in `app.py` 


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
├── about           # the about app
├── app.py          # the file running the app and defining all high-level callback I/Os
├── assets          # a special folder holding all static assets
├── common.py       # common html elements reusable by all apps
├── constants.py    # constant values to be interpreted once, not defined in __init__.py to avoid running on import
├── extract         # the extract app
├── journals        # the journals app
├── search          # the search app
├── tests           # tests for the top level modules
├── util.py         # utilities reusable by all apps or the top level modules
└── view.py         # top-level views of the website
```

`app` contains the core dash instance as well as all callback I/O. The actual logic
for all callbacks can be found inside an app's `logic` modules.

Please keep the functions which define dash html blocks and styles 
(e.g., those in `common.py`) and those which do not 
(e.g., `util.py`) **separate** and in the correct file in a logical manner.


## Inside an app folder

In this example we'll show the most complex app, `search`.

Other apps may not have all the parts here. But no forseeable app should
require more than the 4 files here (outside of the subviews folder).

```
search
├── logic.py       # the callbacks logic
├── common.py      # common html-defining functions among all views
├── subviews       # add a modular view here if your view.py gets too long
├── util.py        # non html-defining util functions
└── view.py        # html-defining functions defining the layout of the app. 
```

### Files with functions defining dash HTML blocks
***Only* functions which define html blocks or styles should be found in these files.**

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

#### `logic.py`
Defines the core callback logic for the html elements laid out in this
app's `view.py` and `subviews`. **Should not define any html elements
itself - only reference those from view, subviews, and common.**

#### `util.py`
Common functions for processing and defining non-html blocks. **No**
function in this file should define a dash html block.

## The `matscholar_web/assets` folder:

Contains all custom local JS and CSS for the project. All of the 
static data is in `data`. Also contains all local static images.

JS files are atomic according to what they
do. `burger.js` operates the burger menu. `count.js` makes the counting
animation. `clientside.js` connects the various files to Dash's clientside
callbacks. 

There are 3 CSS files. `bulma.css` houses most of the styles needed
to be used as `classNames` in Dash. `bulma-helpers.css` can be mainly
used for forcing margins etc. when you have *no* other option. 
`msweb.css` is the custom classes we define and should be kept as short
as possible.


# Running this app:
The following environment variables must be defined:

- `ELASTIC_HOST` - The ElasticSearch host url
- `ELASTIC_PASS` - The ElasticSearch host password
- `ELASTIC_USER` - The ElasticSearch username
- `MATERIALS_SCHOLAR_API_KEY` - The Matscholar API key to use in the rester
- `MATERIALS_SCHOLAR_ENDPOINT` - The API endpoint URL for Matscholar
- `MATERIALS_SCHOLAR_WEB_USER` (not needed) - for frontend-based auth
- `MATERIALS_SCHOLAR_WEB_PASS` (not needed) - for frontend-based auth
- `TF_SERVING_URL` - The url serving the NER tensorflow model.