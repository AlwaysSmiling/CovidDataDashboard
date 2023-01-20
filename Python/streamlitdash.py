import streamlit as st
import pandas as pd
import altair as alt
from millify import millify
import geopandas as gpd
import gpdvega

alt.data_transformers.enable(consolidate_datasets=False)

earthdf = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
earthdf.drop(['iso_a3', 'gdp_md_est', 'continent'], axis=1, inplace=True)

@st.cache
def transformdf(df: pd.DataFrame):
    df = df.pivot(index="Date", columns="IncomeCategory",
                  values="HighestInfected")
    df["Low income"] = df["Low income"].fillna(0)
    df["Low Class Income"] = df["Low income"] + df["Lower middle income"]
    df.drop(['Low income', 'Lower middle income'], axis=1, inplace=True)
    df.rename(columns={'High income': "High Class Income"}, inplace=True)
    df['Date'] = df.index
    df = df.melt(id_vars='Date', value_vars=[
                 'High Class Income', 'Middle Class Income', 'Low Class Income'])
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
    return df1, df2, df3, df4


df1, df2, df3, df4 = importdata()

# Title
st.title("Covid Data Dashboard")


st.header("Global Numbers")
# first table
col1, col2 = st.columns(2)
col1.metric(label=":red[**Total Covid Cases**]",
            value=millify(df1.iloc[0, 0], precision=3))
col2.metric(label=":red[**Total Covid Deaths**]",
            value=millify(df1.iloc[0, 1], precision=3))

st.header("Global Situation")
# second map
df3 = pd.merge(left=earthdf, right=df3, how='inner', left_on='name', right_on='Location')
data = gpdvega.geojson_feature(df3,"features")
map = alt.Chart(data).mark_geoshape(stroke='black', strokeWidth=0.2).project().encode(
        tooltip=['properties.name:O']
    ).properties(width=1300, height=600)

st.altair_chart(map, use_container_width=True)


tab1, tab2 = st.tabs(["Deaths by Continent", "Infected by Income"])
with tab1:
    st.subheader("Deaths by Continent")
    # third chart
    c = alt.Chart(df2).mark_bar(color='red').encode(
        x=alt.X('Continent:N', axis=alt.Axis(labelAngle=0),
                sort='-y', title="Continents"),
        y=alt.Y('TotalDeathCount:Q', axis=alt.Axis(
            format="~s"), title="Total Deaths"),
        opacity=alt.Opacity('mean(TotalDeathCount)'),
        tooltip=['Continent', 'TotalDeathCount']
    ).properties(
        width=alt.Step(50)
    )
    c = c.configure_legend(disable=True)
    c = c.configure_axis(labelFontSize=15, titleFontSize=17)

    st.altair_chart(c, use_container_width=True)

with tab2:
    st.subheader("Infected by Income")
    # fourth chart
    a = alt.Chart(transformdf(df4)).mark_area(opacity=0.4).encode(
        x=alt.X('Date:T', axis=alt.Axis(format="%m/%Y"), title="Month/Year"),
        y=alt.Y('value:Q', axis=alt.Axis(format="~s"),
                stack=None, title="Infected Count"),
        color=alt.Color('IncomeCategory:N', scale=alt.Scale(
            scheme='tableau10'), title="Income Category")
    ).properties(
        width=alt.Step(50)
    )

    a = a.configure_legend(title=None, strokeColor='gray',
                           fillColor='#EEEEEE',
                           padding=10,
                           cornerRadius=10, orient='top-left')
    a = a.configure_axis(labelFontSize=15, titleFontSize=17)

    st.altair_chart(a, use_container_width=True)
