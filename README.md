analise-devbigdata
==============================

# Description
Projeto para o TCC

# Project Organization
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io

# About the study
In this study, we are intended to investigate to which extent (if exists) the social interactions correlates with the bug-fixing time and how we can visualize those interactions.

The multi-component dimension:
- The Hadoop project has four main components: CORE, YARN, HDFS, and MAP REDUCE

The multi-person dimension:
- The contributor who reports a bug
- The contributor who was assigned to a bug
- The contributors who comment on the bug report
- The contributors who commit the fixing code
*The contributors can be committers and non-committers. Some contributors have an official public role in the project (RE or QA)

The multi-version dimension:
- The project versions that are affected by a bug
- The project versions in which the bug-fixing took place
- The timeline of 10 years official project releases

Study Variables
- engagement level (independent): computes how deep a maintainer gets involved in a bug-fixing task.
- engagement frequency (independent): computes how frequently a maintainer gets engaged in bug-fixing tasks overtime after his first contribution.
- bug-fixing time (dependent): the total amount of time required to fix a bug.

Some possible research questions:
Do bugs fixed by more active maintainers correlate with bug-fixing time?
Do bugs fixed by active maintainers of multi-components correlate with bug-fixing time?
Do bugs fixed by more active maintainers correlate with presence of unit test code in fixing commits?
Do bugs fixed by more active maintainers correlate with affected versions?
Do bugs fixed by more active maintainers correlate with fixed versions?
--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
