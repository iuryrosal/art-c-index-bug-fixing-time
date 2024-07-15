How Can We Measure Developer Contribution and How Does It Affect Bug-Fixing Time? The Case of the Apache Hadoop Project
==============================

# Description
Code project for the study and production of the article "How Can We Measure Developer Contribution and How Does It Affect Bug-Fixing Time? The Case of the Apache Hadoop Project".

# Project Organization
------------

    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
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
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │
    └── pyproject.toml            <- File responsible for configuring the Poetry virtual environment

# About the study
Context: Open-source (OS) projects rely heavily on collaborative developer contributions for various development activities, including bug fixing. While many studies have explored different factors influencing bug fixing, to the best of our knowledge, none have explicitly analyzed how developer contribution relates to bug priority and affects bug resolution time. Consequently, understanding the interplay between different levels of developer contribution and bug priority on bug resolution time remains unclear. Goal: This study aims to investigate the effects of developer contribution on bug resolution time within the Apache Hadoop project, considering the different bug priorities. Method: We conducted an exploratory
study analyzing 10,375 bug reports from four projects within the Hadoop project. We performed a detailed analysis of how bug priority and developer contribution relate, utilizing a novel index (c-score) proposed by us that incorporates metrics such as comments, commits, and authors. Additionally, we analyzed correlations be-
tween bug priority, developer contributions, and bug resolution times. Results: We found that bugs with a greater community involvement measured by the number of commits, comments, and authors do not necessarily have a shorter bug resolution time. Finally, different levels of developer contribution, as measured by the
c-score, influence bug resolution times variably across bug priority categories. Conclusion: This study contributes by: (i) proposing a metric (c-index) for the level of developer contribution in free software projects; (ii) identifying how varying levels of developer contributions influence bug resolution time; and (iii) highlighting the use of community involvement metrics and their role in bug resolution efficiency. We expect that our findings underscore the importance of understanding bug resolution dynamics in OS projects,
particularly emphasizing aspects related to developer contributions.

# Instructions
To generate the dashboard locally and generate the same graphs as the study produced, it is necessary to install Poetry on your machine (allowing dependency management within a virtual environment).

Run the ```poetry build``` command to generate the virtual environment with the necessary dependencies, and then ```poetry shell``` to start the virtual environment.

After that, just run the command ```streamlit run main.py``` to host the dashboard locally and access it from localhost.

All graphs generated are saved in reports/figures and you can download the png of the graphs from the dashboard itself.





--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
