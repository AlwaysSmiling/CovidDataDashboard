import streamlit as st
import pandas as pd
import altair as alt
from millify import millify

st. set_page_config(layout="wide")      #set to wide mode

@st.cache
def importdata():
    # import spreadsheets from excel

    df1 = pd.read_excel(
        'https://github.com/AlwaysSmiling/CovidDataDashboard/blob/9083b04ba6f32de98f3b9a34d646f0a9ff9ab404/SQLServerExport.xlsx', 0)
    df2 = pd.read_excel(
        'https://github.com/AlwaysSmiling/CovidDataDashboard/blob/9083b04ba6f32de98f3b9a34d646f0a9ff9ab404/SQLServerExport.xlsx', 1)
    df3 = pd.read_excel(
        'https://github.com/AlwaysSmiling/CovidDataDashboard/blob/9083b04ba6f32de98f3b9a34d646f0a9ff9ab404/SQLServerExport.xlsx', 2)
    df4 = pd.read_excel(
        'https://github.com/AlwaysSmiling/CovidDataDashboard/blob/9083b04ba6f32de98f3b9a34d646f0a9ff9ab404/SQLServerExport.xlsx', 3)

    # preprocess some df3

    df3.rename({'Location': 'Country', 'HighestInfectionCount': '# of Infected',
               'PercentPopulationInfected': '% Population Infected'}, axis=1, inplace=True)
    df3.at[58, 'Country'] = "United States of America"
    df3.at[219, 'Country'] = "Dem. Rep. Congo"
    df3.at[205, 'Country'] = "Central African Rep."
    df3.at[211, 'Country'] = "S. Sudan"

    # preprocess some df4

    df4 = df4.pivot(index="Date", columns="IncomeCategory",
                    values="HighestInfected")
    df4["Low income"] = df4["Low income"].fillna(0)
    df4["Low Class Income"] = df4["Low income"] + df4["Lower middle income"]
    df4.drop(['Low income', 'Lower middle income'], axis=1, inplace=True)
    df4.rename(columns={'High income': "High Class Income"}, inplace=True)
    df4['Date'] = df4.index
    df4 = df4.melt(id_vars='Date', value_vars=[
        'High Class Income', 'Middle Class Income', 'Low Class Income'])
    return df1, df2, df3, df4


df1, df2, df3, df4 = importdata()


st.title("Covid Data Dashboard")            #title


st.header("Global Numbers")                 #first header for counters
col1, col2 = st.columns(2)
col1.metric(label=":red[**Total Covid Cases**]",            #total cases
            value=millify(df1.iloc[0, 0], precision=3))
col2.metric(label=":red[**Total Covid Deaths**]",           #total deaths
            value=millify(df1.iloc[0, 1], precision=3))



st.header("Global Situation")               #second header for map
sphere = alt.sphere()
graticule = alt.graticule()
source = alt.topo_feature(
    'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json', 'countries')

map = alt.layer(
    alt.Chart(sphere).mark_geoshape(fill='lightblue').encode(       #bottom layer, SEA
        tooltip=alt.TooltipValue(value=None)
    ),
    alt.Chart(graticule).mark_geoshape(stroke='white', strokeWidth=0.2).encode(     #next layer, lat, long
        tooltip=alt.TooltipValue(value=None)
    ),
    alt.Chart(source).mark_geoshape(stroke='black').encode(         #top layer, countries
        color=alt.Color('# of Infected:Q',
                        scale=alt.Scale(scheme='yelloworangered')),
        tooltip=alt.Tooltip(['Country:N', 'Population:Q',
                             '# of Infected:Q', '% Population Infected:Q'])
    ).transform_lookup(
        lookup='properties.name',
        from_=alt.LookupData(df3, 'Country', [
                             '% Population Infected', 'Population', 'Country', '# of Infected'])
    )
).project(
    'naturalEarth1'                     #type of projection
).properties(
    width=1300, height=600
).configure_legend(
    strokeColor='gray',
    fillColor='#EEEEEE',
    padding=10,
    cornerRadius=15
)

st.altair_chart(map, use_container_width=True)


tab1, tab2 = st.tabs(["Deaths by Continent", "Infected by Income"])         #two tabs for last two charts
with tab1:                                                                  #tab1
    st.subheader("Deaths by Continent")
    c = alt.Chart(df2).mark_bar(color='red').encode(
        x=alt.X('Continent:N', axis=alt.Axis(labelAngle=0),
                sort='-y', title="Continents"),
        y=alt.Y('TotalDeathCount:Q', axis=alt.Axis(
            format="~s"), title="Total Deaths"),
        opacity=alt.Opacity('mean(TotalDeathCount)'),
        tooltip=['Continent', 'TotalDeathCount']
    ).properties(
        width=alt.Step(50),
        height=600
    )
    c = c.configure_legend(disable=True)
    c = c.configure_axis(labelFontSize=15, titleFontSize=17)

    st.altair_chart(c, use_container_width=True)

with tab2:                                                                  #tab2
    st.subheader("Infected by Income")
    a = alt.Chart(df4).mark_area(opacity=0.4).encode(
        x=alt.X('Date:T', axis=alt.Axis(format="%m/%Y"), title="Month/Year"),
        y=alt.Y('value:Q', axis=alt.Axis(format="~s"),
                stack=None, title="Infected Count"),
        color=alt.Color('IncomeCategory:N', scale=alt.Scale(
            scheme='tableau10'), title="Income Category")
    ).properties(
        width=alt.Step(50),
        height=600
    ).interactive()

    a = a.configure_legend(title=None, strokeColor='gray',
                           fillColor='#EEEEEE',
                           padding=10,
                           cornerRadius=10, orient='top-left')
    a = a.configure_axis(labelFontSize=15, titleFontSize=17)

    st.altair_chart(a, use_container_width=True)
