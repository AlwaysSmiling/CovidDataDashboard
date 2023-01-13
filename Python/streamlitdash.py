import streamlit as st
import pandas as pd


totaldeathsdf = pd.read_excel('/home/pranjalsmiling/Projects/CovidDataDashboard/SQLServerExport.xlsx')
st.write(totaldeathsdf)