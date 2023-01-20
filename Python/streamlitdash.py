import streamlit as st
import pandas as pd
import altair as alt
from millify import millify

@st.cache
def transformdf(df: pd.DataFrame):
    df = df.pivot(index="Date", columns="IncomeCategory", values="HighestInfected")
    df["Low income"] = df["Low income"].fillna(0)
    df["Low Class Income"] = df["Low income"] + df["Lower middle income"]
    df.drop(['Low income','Lower middle income'], axis=1, inplace=True)
    df.rename(columns={'High income': "High Class Income"}, inplace=True)
    df['Date'] = df.index
    df = df.melt(id_vars='Date', value_vars=['High Class Income', 'Middle Class Income', 'Low Class Income'])
    return df

@st.cache
def importdata():
    df1 = pd.read_excel(
    '/home/pranjalsmiling/Projects/CovidDataDashboard/SQLServerExport.xlsx', 0)
    df2 = pd.read_excel(
    '/home/pranjalsmiling/Projects/CovidDataDashboard/SQLServerExport.xlsx', 1)
    df3 = pd.read_excel(
    '/home/pranjalsmiling/Projects/CovidDataDashboard/SQLServerExport.xlsx', 2)
    df4 = pd.read_excel(
    '/home/pranjalsmiling/Projects/CovidDataDashboard/SQLServerExport.xlsx', 3)
    return df1,df2,df3,df4

df1,df2,df3,df4 = importdata()

#Title
st.title("Covid Data Dashboard")


st.header("Global Numbers")
#first table
col1, col2 = st.columns(2)
col1.metric(label=":red[**Total Covid Cases**]", value=millify(df1.iloc[0,0], precision=3))
col2.metric(label=":red[**Total Covid Deaths**]", value=millify(df1.iloc[0,1], precision=3))

st.header("Global Situation")
#TODO: Complete the map part.
#second map
map = alt.Chart().mark_geoshape().encode(

)

tab1, tab2 = st.tabs(["Deaths by Continent","Infected by Income"])
#TODO: format axis labels/legends correctly
with tab1:
    st.subheader("Deaths by Continent")
    #third chart
    c = alt.Chart(df2).mark_bar(color='red').encode(
        x=alt.X('Continent:N', sort='-y', title="Continents"),
        y=alt.Y('TotalDeathCount:Q', title="Total Deaths"),
        opacity=alt.Opacity('mean(TotalDeathCount)')
    ).properties(
        width=alt.Step(50)
    )
    c = c.configure_legend(disable=True)
    st.altair_chart(c, use_container_width=True)

with tab2:    
    st.subheader("Infected by Income")
    #fourth chart
    a = alt.Chart(transformdf(df4)).mark_area(opacity=0.3).encode(
        x=alt.X('Date:T', title="Month/Year"),
        y=alt.Y('value:Q', stack=None, title="Infected Count"),
        color='IncomeCategory:N'
    ).properties(
        width=alt.Step(50)
    )

    a = a.configure_legend(disable=True)
    st.altair_chart(a, use_container_width=True)