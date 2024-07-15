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


    st.title("Quantidade de Commits por Prioridade ao longo do tempo (por mês)")
    st.write("Use o menu dropdown para filtrar o tipo de projeto das tasks a serem exibidas neste gráfico em específico")
    graphs.times_series(dataset=dataset, classe="Priority", date="CommitterDate")
    st.info("Se desejar visualizar melhor um determinado período, selecione dentro do gráfico")

    st.title("Estatísticas")    
    graphs.bar_categorical_count("Priority", dataset)
    graphs.bar_categorical_count("ContributionLevel", dataset)

def analysis_timefixbug_scatters(dataset):
    st.title("Seleção de Feature")
    st.write("A seleção da classe irá impactar nos gráficos de dispersão")
    classes = ["Priority", "ChangeType"]
    classe = st.selectbox("Classe Categórica", classes)
    st.title("Gráfico de Dispersão do BFT em função de variáveis de envolvimento nas issues")
    graphs.scatter(dataset=dataset, var1="BFT", var2="NoComments", classe=classe)
    graphs.scatter(dataset=dataset, var1="BFT", var2="NoCommits", classe=classe)
    graphs.scatter(dataset=dataset, var1="BFT", var2="NoAuthors", classe=classe)
    graphs.scatter(dataset=dataset, var1="BFT", var2="NoMethods", classe=classe)
    graphs.scatter(dataset=dataset, var1="BFT", var2="LoC", classe=classe)
    graphs.scatter(dataset=dataset, var1="BFT", var2="CyC", classe=classe)
    graphs.scatter(dataset=dataset, var1="BFT", var2="NoTokens", classe=classe)

    st.title("Matriz de Correlação")
    array_variables_corr = ["BFT", "NoComments", "NoAttachments", "NoAttachedPatches", 
                            "NoCommits", "NoAuthors", "NoCommitters", "NonSrcAddFiles", 
                            "NonSrcDelFiles", "NonSrcModFiles", "NonSrcAddLines", "NonSrcDelLines"]
    graphs.heatmap_corr(dataset, array_variables_corr)

def analysis_timefixbug_distributed_1(dataset):
    st.title("Distribuição de BFT")
    graphs.monovariada_numerico("BFT", dataset)

    st.title("Gráficos de Distribuição de BFT em função de variável categórica")
    graphs.violinplot_boxplot("BFT", "Priority", dataset)
    graphs.violinplot_boxplot("BFT", "ChangeType", dataset)
    graphs.violinplot_boxplot("BFT", "ContributionLevel", dataset)

def analysis_timefixbug_distributed_2(dataset):
    st.title("Gráficos de Distribuição de BFT em função de Número de Autores")
    graphs.violinplot_boxplot_split("BFT", "Priority", "AuthorsFreq", dataset)
    graphs.violinplot_boxplot_split("BFT", "ContributionLevel", "AuthorsFreq", dataset)

    st.title("Gráficos de Distribuição de BFT em função de Número de Comentários")
    graphs.violinplot_boxplot_split("BFT", "Priority", "CommentsFreq", dataset)
    graphs.violinplot_boxplot_split("BFT", "ContributionLevel", "CommentsFreq", dataset)

def top_ids(dataset, id):
    st.title(f"Top 15 - {id}")
    top = dataset.loc[dataset[f'{id}'].isin(dataset[f'{id}'].value_counts()[:15].index.tolist())]
    st.write(top[f"{id}"].value_counts())

def engagement_devs(dataset):
    st.title("Quantidade de Desenvolvedores em cada Engajamento")
    dataset_1 = dataset[["ContributionLevel", "Author"]]
    dataset_1.drop_duplicates(inplace=True)
    graphs.bar_categorical_count("ContributionLevel", dataset_1, frequency_element="Developers")

    st.title("C-index em cada Engajamento")
    st.write("Low Contribution")
    st.write(dataset.query("ContributionLevel == 'Low Contribution'")["CIndex"].describe())
    st.write("Medium Contribution")
    st.write(dataset.query("ContributionLevel == 'Medium Contribution'")["CIndex"].describe())
    st.write("High Contribution")
    st.write(dataset.query("ContributionLevel == 'High Contribution'")["CIndex"].describe())


    graphs.bar_categorical_count("ContributionLevel", dataset)

    st.title("Distribuição de Commits por Nível de Engajamento")
    graphs.heatmap_categoricals(dataset, "ContributionLevel", "Priority")

def comments(dataset):
    st.title("Distribuição de NoComments")
    graphs.monovariada_numerico("NoComments", dataset)

    st.title("Gráficos de Distribuição de NoComments em função de variável categórica")
    graphs.violinplot_boxplot("NoComments", "Priority", dataset)
    graphs.violinplot_boxplot("NoComments", "ChangeType", dataset)
    graphs.violinplot_boxplot("NoComments", "ContributionLevel", dataset)

def authors_analysis(dataset):
    st.title("Distribuição de NoAuthors")
    graphs.monovariada_numerico("NoAuthors", dataset)

    st.title("Gráficos de Distribuição de NoAuthors em função de variável categórica")
    graphs.violinplot_boxplot("NoAuthors", "Priority", dataset)
    graphs.violinplot_boxplot("NoAuthors", "ChangeType", dataset)
    graphs.violinplot_boxplot("NoAuthors", "ContributionLevel", dataset)

