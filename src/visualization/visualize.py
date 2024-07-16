from src.visualization import graphs

import streamlit as st
import plotly.express as px 
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sb
import numpy as np


def analysis_general(dataset):
    # st.title("Quantidade de Commits por Projeto ao longo do tempo (por mês)")
    # st.write("Use o menu dropdown para filtrar o tipo de prioridade das tasks a serem exibidas neste gráfico em específico")
    # priority = st.selectbox(
    #     "Selecione a Prioridade",
    #     [" ", "Blocker", "Critical", "Major", "Minor", "Trivial"]
    # )
    # if priority != " ":
    #     dataset = dataset[dataset["Priority"] == priority]
    # graphs.times_series(dataset=dataset, classe="Project", date="CommitterDate")
    # st.info("Se desejar visualizar melhor um determinado período, selecione dentro do gráfico")


    st.title("Number of Commits per Priority over time (per month)")
    st.write("Use the dropdown menu to filter the project type of tasks to be displayed on this specific chart")
    graphs.times_series(dataset=dataset, classe="Priority", date="CommitterDate")
    st.info("If you want to better visualize a certain period, select it within the chart")

    st.title("Statistics")    
    graphs.bar_categorical_count("Priority", dataset)
    graphs.bar_categorical_count("ContributionLevel", dataset)

def analysis_timefixbug_scatters(dataset):
    st.title("Feature Selection")
    st.write("Class selection will impact scatterplots")
    classes = ["Priority", "ChangeType"]
    classe = st.selectbox("Categorical Class", classes)
    st.title("BFT Scatterplot depending on variables involved in issues")
    graphs.scatter(dataset=dataset, var1="BFT", var2="NoComments", classe=classe)
    graphs.scatter(dataset=dataset, var1="BFT", var2="NoCommits", classe=classe)
    graphs.scatter(dataset=dataset, var1="BFT", var2="NoAuthors", classe=classe)
    graphs.scatter(dataset=dataset, var1="BFT", var2="NoMethods", classe=classe)
    graphs.scatter(dataset=dataset, var1="BFT", var2="LoC", classe=classe)
    graphs.scatter(dataset=dataset, var1="BFT", var2="CyC", classe=classe)
    graphs.scatter(dataset=dataset, var1="BFT", var2="NoTokens", classe=classe)

    st.title("Correlation Matrix")
    array_variables_corr = ["BFT", "NoComments", "NoAttachments", "NoAttachedPatches", 
                            "NoCommits", "NoAuthors", "NoCommitters", "NonSrcAddFiles", 
                            "NonSrcDelFiles", "NonSrcModFiles", "NonSrcAddLines", "NonSrcDelLines"]
    graphs.heatmap_corr(dataset, array_variables_corr)

def analysis_timefixbug_distributed_1(dataset):
    st.title("BFT Distribution")
    graphs.monovariada_numerico("BFT", dataset)

    st.title("BFT Distribution Graphs as a function of categorical variable")
    graphs.violinplot_boxplot("BFT", "Priority", dataset)
    graphs.violinplot_boxplot("BFT", "ChangeType", dataset)
    graphs.violinplot_boxplot("BFT", "ContributionLevel", dataset)

def analysis_timefixbug_distributed_2(dataset):
    st.title("BFT Distribution Charts as a function of Number of Authors")
    graphs.violinplot_boxplot_split("BFT", "Priority", "AuthorsFreq", dataset)
    graphs.violinplot_boxplot_split("BFT", "ContributionLevel", "AuthorsFreq", dataset)

    st.title("BFT Distribution Charts as a function of Number of Comments")
    graphs.violinplot_boxplot_split("BFT", "Priority", "CommentsFreq", dataset)
    graphs.violinplot_boxplot_split("BFT", "ContributionLevel", "CommentsFreq", dataset)

def top_ids(dataset, id):
    st.title(f"Top 15 - {id}")
    top = dataset.loc[dataset[f'{id}'].isin(dataset[f'{id}'].value_counts()[:15].index.tolist())]
    st.write(top[f"{id}"].value_counts())

def engagement_devs(dataset):
    st.title("Number of Developers at each contribution level")
    dataset_1 = dataset[["ContributionLevel", "Author"]]
    dataset_1.drop_duplicates(inplace=True)
    graphs.bar_categorical_count("ContributionLevel", dataset_1, frequency_element="Developers")

    st.title("C-index in each Contribution Level")
    st.write("Low Contribution")
    st.write(dataset.query("ContributionLevel == 'Low Contribution'")["CIndex"].describe())
    st.write("Medium Contribution")
    st.write(dataset.query("ContributionLevel == 'Medium Contribution'")["CIndex"].describe())
    st.write("High Contribution")
    st.write(dataset.query("ContributionLevel == 'High Contribution'")["CIndex"].describe())


    graphs.bar_categorical_count("ContributionLevel", dataset)

    st.title("Distribution of Commits by Contribution Level")
    graphs.heatmap_categoricals(dataset, "ContributionLevel", "Priority")

def comments(dataset):
    st.title("Distribution of NoComments")
    graphs.monovariada_numerico("NoComments", dataset)

    st.title("NoComments Distribution Graphs as a function of categorical variable")
    graphs.violinplot_boxplot("NoComments", "Priority", dataset)
    graphs.violinplot_boxplot("NoComments", "ChangeType", dataset)
    graphs.violinplot_boxplot("NoComments", "ContributionLevel", dataset)

def authors_analysis(dataset):
    st.title("Distribution of NoAuthors")
    graphs.monovariada_numerico("NoAuthors", dataset)

    st.title("NoAuthors Distribution Graphs as a function of categorical variable")
    graphs.violinplot_boxplot("NoAuthors", "Priority", dataset)
    graphs.violinplot_boxplot("NoAuthors", "ChangeType", dataset)
    graphs.violinplot_boxplot("NoAuthors", "ContributionLevel", dataset)

