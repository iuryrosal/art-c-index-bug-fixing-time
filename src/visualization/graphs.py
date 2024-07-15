import matplotlib.pyplot as plt
import seaborn as sb
import plotly.express as px 
import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.io import write_image

colors_by_class = {"Priority": {"Trivial": "#FEEDDE",
                                "Minor": "#FDBE85",
                                "Major": "#FD8D3C",
                                "Normal": "#FD8D3C",
                                "Critical": "#E6550D",
                                "Blocker": "#A63603",
                                "Urgent": "#A63603"},
                  "ChangeType": {"MODIFY": "#003f5c",
                                 "ADD": "#665191",
                                 "RENAME": "#d45087",
                                 "DELETE": "#ff7c43",
                                 "UNKNOWN": "#ffa600"},
                  "ContributionLevel": {"Low Contribution": "#E5F5E0",
                                 "Medium Contribution": "#A1D99B",
                                 "High Contribution": "#31A354"},
                  "AuthorsFreq": {"1 Author": "#fc8d59", 
                                  ">=2 Authors": "#fef0d9"},
                  "CommentsFreq": {"< 20 Comments": "#fc8d59",
                                   ">= 20 Comments": "#fef0d9"}
}
PALLETE = "CMRmap_r"
PALLETE_CONTINUOS_PLOTLY = "Inferno"
PALLETE_DISCRETE_PLOTLY = px.colors.sequential.Plasma_r

order_classes = {"Priority": ["Trivial", "Minor", "Major", "Normal", "Critical", "Blocker", "Urgent"],
                 "ChangeType": ["MODIFY", "ADD", "RENAME", "DELETE", "UNKNOWN"],
                 "ContributionLevel": ["Low Contribution", "Medium Contribution", "High Contribution"],
                 "AuthorsFreq": ["1 Author", ">=2 Authors"],
                 "CommentsFreq": ["< 20 Comments", ">= 20 Comments"]
}

# ===========================
# Analise Monovariada
# ===========================


def monovariada_numerico(variable, data):
  st.write(f"{variable}")
  st.dataframe(pd.DataFrame({"Mediana": data[variable].median(), 
                              "Média": data[variable].mean(),
                              "Máx": data[variable].max(),
                              "Mín": data[variable].min(),
                              "Desvio Padrão": data[variable].std()
                              },
                              index=[0])
              )

  fig, ax = plt.subplots(figsize= (22, 10))
  fig = px.histogram(data, x=variable, hover_data=data.columns, marginal="box")
  plt.show()
  st.plotly_chart(fig)
  write_image(fig=fig, file=f"reports/figures/monovariada_numerico_{variable}.pdf", format="pdf")


def violinplot(var1, data):
  df = dataset.sort_values(by=[var_categorical])
  fig, ax = plt.subplots(figsize= (22, 10))
  fig = px.violin(df, y=var1, box=True, points="all",
                  title=f"{var1}", color_discrete_sequence=PALLETE_DISCRETE_PLOTLY)
  plt.show()
  st.plotly_chart(fig)


def bar_categorical_count(classe, dataset, frequency_element="commits"):
  fig = go.Figure()
  df = dataset.sort_values(by=[classe])
  categories = order_classes[classe]
  counts = df[classe].value_counts().to_dict()
  for category in categories:
    if category in counts.keys():
      fig.add_trace(go.Bar(x=[category],
                          y=[counts[category]],
                          name=category,
                          marker=dict(color=colors_by_class[classe][category]),
                          text=[counts[category]]
                          ))
  fig.update_layout(
    #title_text=f"Quantidade de {frequency_element} <br>por {classe}",
    xaxis_title=classe,
    yaxis_title=frequency_element,
    legend_title=classe,
    font=dict(
        family="Courier New, monospace",
        size=15
    )
  )
  st.plotly_chart(fig)
  write_image(fig=fig, file=f"reports/figures/bar_categorical_{frequency_element}_by_{classe}.pdf", format="pdf")


# ===========================
# Analise Bivariada
# ===========================


def heatmap_combine(var1, var2, data):
    fig, ax = plt.subplots(figsize= (22, 10))
    plt.subplot(1,2,1)
    sb.heatmap(pd.crosstab(data[var1], data[var2]), annot = True, fmt = "d", cmap = "YlGnBu")
    plt.title(f"{var1} x {var2}: quantidade - N", fontsize = 16)
    plt.xlabel(" ")
    plt.ylabel(" ")


    plt.subplot(1,2,2)
    sb.heatmap(pd.crosstab(data[var1], data[var2], normalize='index')*100, annot = True, fmt = ".2f", cmap = "PuBuGn")
    #plt.title(f"{var1} x {var2}: porcentagem - %", fontsize = 16)
    plt.xlabel(" ")
    plt.ylabel(" ")

    plt.show()
    st.pyplot(fig)
    write_image(fig=fig, file=f"reports/figures/heatmap_{var1}_x_{var2}.pdf", format="pdf")


def boxplot(var1, var2, data):
  fig, ax = plt.subplots(figsize = (22, 10))
  ax = sb.boxplot(x = var1, y = var2,
                  data = data, 
                  orient ='h',
                  palette=colors_by_class[var2])
  ax.figure.set_size_inches(16, 8)
  ax.set_xlabel(f'{var1}', fontsize = 16)
  ax.set_ylabel(f'f{var2}', fontsize = 16) 
  handles, _ = ax.get_legend_handles_labels()
  plt.title(f'Box-plot de {var2} em relação à {var1}', fontsize=18)
  plt.show()
  st.pyplot(fig)


def violinplot_boxplot(var, classe, dataset):
    fig = go.Figure()
    categories = order_classes[classe]
    quartiles = []
    for category in categories:
        fig.add_trace(go.Violin(x=dataset[classe][dataset[classe] == category],
                                y=dataset[var][dataset[classe] == category],
                                name=category,
                                box_visible=True,
                                meanline_visible=True,
                                fillcolor=colors_by_class[classe][category],
                                line_color='black'))
    fig.update_layout(
      #title_text=f"Distribuição de {var}<br>em função de {classe}",
      xaxis_title=classe,
      yaxis_title=var,
      legend_title=classe,
      font=dict(
          family="Courier New, monospace",
          size=15
      )
    )
    st.plotly_chart(fig)
    write_image(fig=fig, file=f"reports/figures/violinplot_{var}_by_{classe}.pdf", format="pdf")


# ===========================
# Analise Multivariada
# ===========================


def violinplot_boxplot_split(var, classe, split, dataset):
  fig = go.Figure()
  categories = order_classes[split]
  fig.add_trace(go.Violin(x=dataset[classe][dataset[split] == categories[0]],
                          y=dataset[var][dataset[split] == categories[0]],
                          legendgroup=categories[0], scalegroup=categories[0], name=categories[0],
                          side='negative',
                          box_visible=True,
                          meanline_visible=True,
                          fillcolor=colors_by_class[split][categories[0]],
                          line_color='black'))
  fig.add_trace(go.Violin(x=dataset[classe][dataset[split] == categories[1]],
                          y=dataset[var][dataset[split] == categories[1]],
                          legendgroup=categories[1], scalegroup=categories[1], name=categories[1],
                          side='positive',
                          box_visible=True,
                          meanline_visible=True,
                          fillcolor=colors_by_class[split][categories[1]],
                          line_color='black'))
  fig.update_layout(
    #title_text=f"Distribuição de {var}<br>em função de {classe} e {split}",
    xaxis_title=classe,
    yaxis_title=var,
    legend_title=split,
    font=dict(
        family="Courier New, monospace",
        size=15
    )
  )
  st.plotly_chart(fig)
  write_image(fig=fig, file=f"reports/figures/violinplot_{var}_by_{classe}_split_{split}.pdf", format="pdf")

def scatter(var1, var2, classe, dataset):
  df = dataset.sort_values(by=[classe])
  fig = px.scatter(df, x=f"{var1}", y=f"{var2}", color=classe, 
                   color_discrete_map=colors_by_class[classe],
                   opacity=0.5
                  )
  fig.update_traces(marker=dict(size=6,
                                line=dict(width=1,
                                            color='Black')))
  fig.update_layout(
    #title_text=f"Distribuição de {var1}<br>em função de {var2}, categorizado por {classe}",
    xaxis_title=var1,
    yaxis_title=var2,
    legend_title=classe,
    font=dict(
        family="Courier New, monospace",
        size=15
    )
  )
  st.plotly_chart(fig)
  write_image(fig=fig, file=f"reports/figures/scatter_{var1}_x_{var2}_by_{classe}.pdf", format="pdf")


def times_series(dataset, classe, date):
  grouped = dataset.groupby([classe, pd.Grouper(key=date, freq='M')])['Committer'].count().reset_index().sort_values(date)
  grouped[f"{date}"] = grouped[f"{date}"].dt.strftime('%m-%Y')
  grouped = grouped.rename(columns={'Committer': 'Quant de Commits', f"{date}": f"Mês/Ano {date}"})

  fig = go.Figure()
  for category in order_classes[classe]:
    fig.add_trace(go.Scatter(x=grouped[f"Mês/Ano {date}"][grouped[classe]==category], 
                             y=grouped["Quant de Commits"][grouped[classe]==category],
                             mode='lines',
                             name=category,
                             line=dict(color=colors_by_class[classe][category])
                            )
                )
  fig.update_layout(
    #title_text=f"Distribuição de Commits médios por mês <br>em função do {date}, categorizado por {classe}",
    xaxis_title=date,
    yaxis_title="Commits médios por mês",
    legend_title=classe,
    font=dict(
        family="Courier New, monospace",
        size=15
    )
  )
  fig.update_xaxes(categoryorder='array', categoryarray=grouped[f"Mês/Ano {date}"].tolist())
  st.plotly_chart(fig)


def heatmap_corr(dataset, array_variables):
  correlacao_snapshot = dataset[array_variables]
  corr = correlacao_snapshot.corr()
  mask = np.triu(np.ones_like(corr, dtype=bool))
  f, ax = plt.subplots(figsize=(11, 9))
  cmap = sb.diverging_palette(220, 20, as_cmap=True)
  sb.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
              square=True, linewidths=.5, cbar_kws={"shrink": .5})
  plt.title('Correlação entre as variáveis numéricas')
  plt.show()
  st.pyplot(f)


def heatmap_categoricals(dataset, cat1, cat2):
    st.markdown(f"## {cat1}  x  {cat2}")
    fig, axes = plt.subplots(1, 2, figsize = (15, 10))
    plt.subplot(1, 1, 1)
    freq_two_class = dataset[[cat1, cat2]].value_counts().to_frame('counts').reset_index()
    freq_dataframe = pd.pivot_table(freq_two_class, values="counts", index=cat1, columns=cat2, aggfunc=np.sum)
    st.write(freq_dataframe)
    fig = px.imshow(freq_dataframe, text_auto=True, aspect="auto", color_continuous_scale=px.colors.sequential.Greens)
    # plt.title(f"Distribuição de Atividades - {cat1} x {cat2}")
    fig.update_layout(
        yaxis = dict(
                        categoryorder="category ascending",
                        ticktext=["High", "Low", "Medium"],
                        tickvals=[0, 1, 2]
        )
    )
    st.plotly_chart(fig)
    write_image(fig=fig, file=f"reports/figures/heatmap_{cat1}_x_{cat2}.pdf", format="pdf")


def slope_chart(dataset, class_, var1, var2):
  counts_var1 = dataset[class_].value_counts().to_dict()
  counts_var2 = dataset[class_].value_counts().to_dict()

  colors = ['#87B38D', '#477998', '#291F1E', '#BC9CB0', '#A3333D']
  classe = dataset[f"{class_}"].values
  fig, ax = plt.subplots(1, figsize=(10,10))
  for i, v in enumerate(classe):
      temp = dataset[dataset[f'{class_}'] == v]
      plt.plot(temp[f"{var1}"], counts[v], color=colors[i], lw=2.5)

      plt.text(temp[f"{var1}"]+0.02, 
              counts[v], 
              '{:,.2f}'.format(counts[v]))

      plt.text(temp[f"{var1}"]-0.02, 
              counts[v], 
              '{:,.2f}'.format(counts[v]), 
              va='center', ha='right')

      correction = 0
      if v == 'Canada': correction = 500
      plt.text(2018.5, 
              temp.Value.values[1] - correction, 
              v, color=colors[i],
              va='center', ha='center', fontsize=15)
  # plt.xlim(2017.5,2019.5)
  plt.xticks(["N° Desenvolvedores", "N° Commits"])
  plt.yticks([])
  # grid
  ax.xaxis.grid(color='black', linestyle='solid', 
                which='both', alpha=0.9)
  # remove spines
  ax.spines['right'].set_visible(False)
  ax.spines['left'].set_visible(False)
  ax.spines['bottom'].set_visible(False)
  ax.spines['top'].set_visible(False)
  plt.title('Engajamento e Numero de Commits em relação a Composição\n', loc='left', fontsize=20)
  plt.show()