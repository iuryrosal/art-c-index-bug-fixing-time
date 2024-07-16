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
        analysis_options = ["General",
                           "Technic Details",
                           "IDs",
                           "BFT - Dispersion",
                           "BFT - Distribution I",
                           "BFT - Distribution II",
                           "Developer Contribution",
                           "Comments",
                           "Authors (Devs)"
                        ]
        analysis_type = st.sidebar.selectbox("Analysis Type", analysis_options)

        dataset_final = load_data()

        if analysis_type == "General":
                dataset_filtered = show_filter(dataset_final)

                analysis_general(dataset_filtered)

        elif analysis_type == "Technic Details":
                pop_up(CTA="ℹ Obtaining the database",
                        title="Details about transformations and treatments",
                        body="""The base was obtained from a merge between the snapshot and the commit. 
                                Removal of Outliers (BFT <= 95). 
                                Removal of columns: ["Owner", "Manager_x", "Manager_y", "Category_x", 
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

        elif analysis_type == "BFT - Dispersion":
                pop_up(CTA="ℹ Understand the BFT variable",
                        title="Bug-Fixing Time (BFT) Variable",
                        body="""Variable resulting from the difference between the bug report creation data (CreationDate) and the bug resolution data (ResolutionDate)
                                This variable is displayed in days.
                        """)

                dataset_filtered = show_filter(dataset_final, menu_option=analysis_type)

                analysis_timefixbug_scatters(dataset_filtered, )

        elif analysis_type == "BFT - Distribution I":
                pop_up(CTA="ℹ Understand the BFT variable",
                        title="Bug-Fixing Time (BFT) Variable",
                        body="""Variable resulting from the difference between the bug report creation data (CreationDate) and the bug resolution data (ResolutionDate)
                                This variable is displayed in days.
                        """)

                dataset_filtered = show_filter(dataset_final, menu_option=analysis_type)

                analysis_timefixbug_distributed_1(dataset_filtered)

        elif analysis_type == "BFT - Distribution II":
                pop_up(CTA="ℹ Understand the BFT variable",
                        title="Bug-Fixing Time (BFT) Variable",
                        body="""Variable resulting from the difference between the bug report creation data (CreationDate) and the bug resolution data (ResolutionDate)
                                This variable is displayed in days.
                        """)

                dataset_filtered = show_filter(dataset_final, menu_option=analysis_type)

                analysis_timefixbug_distributed_2(dataset_filtered)
        elif analysis_type == "Developer Contribution":
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
        
        elif analysis_type == "Comments":
                dataset_filtered = show_filter(dataset_final, menu_option=analysis_type)
                comments(dataset_filtered)
        
        elif analysis_type == "Authors (Devs)":
                dataset_filtered = show_filter(dataset_final, menu_option=analysis_type)
                authors_analysis(dataset_filtered)

main()