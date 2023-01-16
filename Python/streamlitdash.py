import streamlit as st
import pandas as pd
import altair as alt

df1 = pd.read_excel('/home/pranjalsmiling/Projects/CovidDataDashboard/SQLServerExport.xlsx', 0)
df2 = pd.read_excel('/home/pranjalsmiling/Projects/CovidDataDashboard/SQLServerExport.xlsx', 1)
df3 = pd.read_excel('/home/pranjalsmiling/Projects/CovidDataDashboard/SQLServerExport.xlsx', 2)
df4 = pd.read_excel('/home/pranjalsmiling/Projects/CovidDataDashboard/SQLServerExport.xlsx', 3)


st.write(df1)

c = alt.Chart(df2).mark_bar().encode( # type: ignore 
    x='Continent', y='TotalDeathCount'
)

st.altair_chart(c)