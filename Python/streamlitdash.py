import streamlit as st
import pandas as pd
import altair as alt

df1 = pd.read_excel(
    '/home/pranjalsmiling/Projects/CovidDataDashboard/SQLServerExport.xlsx', 0)
df2 = pd.read_excel(
    '/home/pranjalsmiling/Projects/CovidDataDashboard/SQLServerExport.xlsx', 1)


st.write(df1)

c = alt.Chart(df2).mark_bar(color='red').encode(
    x=alt.X(field='Continent', sort='-y'),
    y='TotalDeathCount', 
    opacity=alt.Opacity('mean(TotalDeathCount)')
).properties(
    width=alt.Step(60)
)

st.altair_chart(c)
