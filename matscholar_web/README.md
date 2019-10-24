### Structure of the project

#### `/`

Running the app.
```
/app.py
```
```
(my_virtualenv) python app.py
```

#### `/matscholar_web`
The assets folder is special. The other folders are modular apps. 
The python files are common parts of the website across all apps.
```
├── about          # about app
├── analysis       # analysis app
├── app.py         # the core dash instance. don't mess with this
├── assets         # static assets, not an app.
├── common.py      # common html-returning functions among all apps or main view
├── constants.py   # constant quantities
├── footer.py      # the footer
├── index.py       # (IMPORTANT): all high-level callback I/Os and the main layout of the webpage.
├── journals       # the journals app
├── logo.py        # the logo
├── nav.py         # the nav bar
├── search         # the search app
└── util.py        # non-html returning util functions
```



### Running this app:
The following environment variables must be defined:

- ELASTIC_HOST - The ElasticSearch host url
- ELASTIC_PASS - The ElasticSearch host password
- ELASTIC_USER - The ElasticSearch username
- MATERIALS_SCHOLAR_API_KEY - The Matscholar API key to use in the rester
- MATERIALS_SCHOLAR_ENDPOINT - The API endpoint URL for Matscholar
- MATERIALS_SCHOLAR_WEB_USER (not needed) - for frontend-based auth
- MATERIALS_SCHOLAR_WEB_PASS (not needed) - for frontend-based auth
- TF_SERVING_URL - The url serving the NER tensorflow model.