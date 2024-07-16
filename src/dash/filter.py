import streamlit as st 

def show_filter(dataset, menu_option=None):
    dataset_filtered = dataset
    
    st.sidebar.title("Filter Options")

    info_filter = st.sidebar.empty()
    
    ###################
    # OPÇÕES DE FILTRO
    ###################
    if menu_option == "BFT - Distribuição I" or menu_option == "BFT - Distribuição II" or menu_option == "BFT - Dispersão":
        st.sidebar.write("BFT range")

        time_fix_selected = st.sidebar.slider("Escolha o intervalo de BFT desejado", 0, 100, [0, 100], step=10)
        after_time_fix = dataset_filtered["BFT"] >= time_fix_selected[0]
        before_time_fix = dataset_filtered["BFT"] <= time_fix_selected[1]
        between_two_times = after_time_fix & before_time_fix
        dataset_filtered = dataset_filtered.loc[between_two_times]

    st.sidebar.write("CommitterDate range")

    year_selected = st.sidebar.slider("Choose the desired year", 2008, 2019, [2008, 2019])

    modules = ["Hadoop Core", "HDFS", "YARN", "MapReduce"]
    modules.insert(0, "All")
    modules_filter = st.sidebar.selectbox("Modules", modules)

    st.sidebar.write("Authors e Reporters")
    authors = dataset["Author"].drop_duplicates(keep="last").values.tolist()
    authors.insert(0, "All")
    author_filter = st.sidebar.selectbox("Author", authors)

    reporters = dataset["Reporter"].drop_duplicates(keep="last").values.tolist()
    reporters.insert(0, "All")
    reporter_filter = st.sidebar.selectbox("Reporter", reporters)

    if menu_option != "Contribution Level":
        st.sidebar.write("Contribution Level")
        engajaments = ["All", "High Contribution", "Medium Contribution", "Low Contribution"]
        engajament_filter = st.sidebar.selectbox("ContributionLevel", engajaments)

        if engajament_filter != "All":
            dataset_filtered = dataset_filtered[dataset_filtered.ContributionLevel == engajament_filter]
    
    ########################
    # APLICAÇÃO DE FILTROS
    #########################
    if modules_filter != "All":
        dataset_filtered = dataset_filtered[dataset_filtered.Project == modules_filter]
    if author_filter != "All":
        dataset_filtered = dataset_filtered[dataset_filtered.Author == author_filter]
    if reporter_filter != "All":
        dataset_filtered = dataset_filtered[dataset_filtered.Reporter == reporter_filter]

    after_start_date = dataset_filtered["CommitterDate"].dt.year >= year_selected[0]
    before_end_date = dataset_filtered["CommitterDate"].dt.year <= year_selected[1]
    between_two_dates = after_start_date & before_end_date
    dataset_filtered = dataset_filtered.loc[between_two_dates]

    info_filter.info(f"""
                    ℹ️ The database is being filtered by Author **{author_filter}** and 
                    by Reporter **{reporter_filter}**.
                    Considering commits between **{year_selected[0]}** and **{year_selected[1]}**.
                    """)

    return dataset_filtered