import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('ejemplo_datos.csv')

def grafica():
    st.write('#### Grafica')
    st.dataframe(df)

    # Grafica 1
    df_group = (
        df.groupby(['grupo_poblacional', 'categoria_grupo'])['incidentes_mes']
        .sum()
        .reset_index()
        .sort_values('incidentes_mes', ascending=False)
    )

    fig = px.bar(
        df_group,
        x='grupo_poblacional',
        y='incidentes_mes',
        color='categoria_grupo',
        title='Incidentes de ciberacoso por grupo',
        labels={'incidentes_mes': 'Incidentes', 'grupo_poblacional': 'Grupo'}
    )
    st.plotly_chart(fig)