from src.data.load_data import DataSet
from src.features.build_features import CreateFeature
from src.features.transform_data import TransformData
from src.visualization.visualize import *
from src.dash.filter import show_filter
from src.visualization import graphs
from src.visualization.front_end_features import pop_up

import streamlit as st
import os
import pandas as pd
import numpy as np
print("Todos os modulos foram carregados com sucesso")



def load_data():
    datas_sets = DataSet()
    transform_data = TransformData()
    build_features = CreateFeature()
    dataset = transform_data.data_transformation(datas_sets.commit_snapshot)
    dataset_timefixbug = build_features.build_timefixbug(dataset)
    dataset_devs_categories = build_features.build_category_dev(
            dataSetOriginal=dataset_timefixbug,
            snapshot_file=datas_sets.snapshot_file,
            commit_file=datas_sets.commit_file,
            comment_file=datas_sets.comment_file)
    dataset_Authors_Freq = build_features.build_Authors_Freq(dataset_devs_categories)
    dataset_Comments_Freq = build_features.build_Comments_Freq(dataset_Authors_Freq)
    dataset_final = transform_data.remove_outlier_timefixbug(dataset_Comments_Freq)
    return dataset_final


def main():
        analysis_options = ["Geral",
                           "Detalhes Técnicos",
                           "IDs",
                           "TimeFixBug - Dispersão",
                           "TimeFixBug - Distribuição I",
                           "TimeFixBug - Distribuição II",
                           "Engajamento de Desenvolvedores",
                           "Comentários",
                           "Autores (Devs)"
                        ]
        analysis_type = st.sidebar.selectbox("Tipo de Analise", analysis_options)

        dataset_final = load_data()

        if analysis_type == "Geral":
                dataset_filtered = show_filter(dataset_final)

                analysis_general(dataset_filtered)

        elif analysis_type == "Detalhes Técnicos":
                pop_up(CTA="ℹ Obtenção da base de dados",
                        title="Detalhes sobre as transformações e tratamentos",
                        body="""A base foi obtida a partir de um merge entre a snapshot e a commit. 
                                Remoção de Outliers (TimeFixBug <= 95). 
                                Remoção das colunas: ["Owner", "Manager_x", "Manager_y", "Category_x", 
                                "Category_y", "AffectsVersions", "FixVersions", "NoWatchers", "CommitHash", 
                                "InwardIssueLinks", "OutwardIssueLinks", "IsMergeCommit", 
                                "Project_y", "Status", "HasMergeCommit"]
                        """)

                dataset_filtered = show_filter(dataset_final)

                st.title("Preview da base filtrada")
                st.write(dataset_filtered.head(5))

                st.title("Sobre a base de dados")
                st.write(
                        "Quantidade de registros:", dataset_filtered.shape[0], 
                        "Quantidade de colunas:", dataset_filtered.shape[1]
                        )
                st.dataframe(pd.DataFrame({"Únicos": dataset_filtered.nunique(), 
                                        "Nulos": dataset_filtered.isnull().sum()}))

                st.title("Informações de colunas numéricas")
                st.write(dataset_filtered.describe())

                graphs.bar_categorical_count("ChangeType", dataset_filtered)

        elif analysis_type == "IDs":
                top_ids(dataset_final, "Reporter")
                top_ids(dataset_final, "Author")

        elif analysis_type == "TimeFixBug - Dispersão":
                pop_up(CTA="ℹ Entenda sobre a variável de TimeFixBug",
                        title="Variável Tempo de Resolução de Bug (TimeFixBug)",
                        body="""Variável obtida pela diferença entre a data de criação do report do bug (CreationDate) e a data de resolução do bug (ResolutionDate)
                                Essa variável é exibida em dias.
                        """)

                dataset_filtered = show_filter(dataset_final, menu_option=analysis_type)

                analysis_timefixbug_scatters(dataset_filtered, )

        elif analysis_type == "TimeFixBug - Distribuição I":
                pop_up(CTA="ℹ Entenda sobre a variável de TimeFixBug",
                        title="Variável Tempo de Resolução de Bug (TimeFixBug)",
                        body="""Variável obtida pela diferença entre a data de criação do report do bug (CreationDate) e a data de resolução do bug (ResolutionDate)
                                Essa variável é exibida em dias.
                        """)

                dataset_filtered = show_filter(dataset_final, menu_option=analysis_type)

                analysis_timefixbug_distributed_1(dataset_filtered)

        elif analysis_type == "TimeFixBug - Distribuição II":
                pop_up(CTA="ℹ Entenda sobre a variável de TimeFixBug",
                        title="Variável Tempo de Resolução de Bug (TimeFixBug)",
                        body="""Variável obtida pela diferença entre a data de criação do report do bug (CreationDate) e a data de resolução do bug (ResolutionDate)
                                Essa variável é exibida em dias.
                        """)

                dataset_filtered = show_filter(dataset_final, menu_option=analysis_type)

                analysis_timefixbug_distributed_2(dataset_filtered)
        elif analysis_type == "Engajamento de Desenvolvedores":
                pop_up(CTA="ℹ Entenda sobre a variável de engajamento de desenvolvedores",
                        title="Variável Engajamento de Desenvolvedores",
                        body="""Engajamento de desenvolvedores (authors) é baseado na média de frequência de commits feitos por ano em relação a todo o período mapeado.
                                **Pouco Engajado** <= 10 commits em média por ano.
                                **Engajado** > 10 e < 72 commits em média por ano. 
                                **Muito Engajado** >= 72 commits em média por ano. 
                                Os valores levam em conta a distribuição de quartis dessa frequência de commits feitos por ano.
                        """)
                dataset_filtered = show_filter(dataset_final, menu_option=analysis_type)
                engagement_devs(dataset_filtered)
        
        elif analysis_type == "Comentários":
                dataset_filtered = show_filter(dataset_final, menu_option=analysis_type)
                comments(dataset_filtered)
        
        elif analysis_type == "Autores (Devs)":
                dataset_filtered = show_filter(dataset_final, menu_option=analysis_type)
                authors_analysis(dataset_filtered)

main()