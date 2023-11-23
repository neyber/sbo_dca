import streamlit as st
import plotly.express as px
import pandas as pd
import warnings
import locale

warnings.filterwarnings('ignore')

st.set_page_config(page_title="SBO - DCA", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: INDICADOR SBO - DCA")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

fl = st.file_uploader(":file_folder: Subir Archivo",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df1 = pd.read_excel(filename, sheet_name=0, header=0)
    df2 = pd.read_excel(filename, sheet_name=1, header=0)
    df3 = pd.read_excel(filename, sheet_name=2, header=0)
    df4 = pd.read_excel(filename, sheet_name=3, header=0)
else:
    df1 = pd.read_excel("SBO - DCA 2023.xlsx", sheet_name=0, header=0)
    df2 = pd.read_excel("SBO - DCA 2023.xlsx", sheet_name=1, header=0)
    df3 = pd.read_excel("SBO - DCA 2023.xlsx", sheet_name=2, header=0)
    df4 = pd.read_excel("SBO - DCA 2023.xlsx", sheet_name=3, header=0)
  
sites = df1["SITE"].unique()

periodos = pd.Series(df1["PERIODO"].unique().astype(str)).str[:4].unique()

col1, col2 = st.columns((2))

with col1:
    site = st.selectbox("SITE", sites)

with col2:
    periodo = st.selectbox("PERIODO", periodos)
    
site_condition_df1 = df1["SITE"] == site
periodo_condition_df1 = df1["PERIODO"].astype(str).str.startswith(periodo)
combined_condition_df1 = site_condition_df1 & periodo_condition_df1
filtered_df1 = df1[combined_condition_df1]
group_df1 = filtered_df1.groupby(["EVALUADOR"])[["SBO", "DCA"]].sum().reset_index()
group_df1["SBO"] = group_df1["SBO"] / 7 * 100
group_df1["DCA"] = group_df1["DCA"] / (7*7) * 100
result_df1 = group_df1.rename(columns={"SBO": "% Cumplimiento YTD SBO", "DCA": "% Cumplimiento YTD DCA"})

st.header("_SBO - DCA_", divider='grey')
st.table(result_df1)

periodo_condition_df2 = df2["PERIODO"].astype(str).str.startswith(periodo)
filtered_df2 = df2[periodo_condition_df2]
group_df2 = filtered_df2.groupby(["EVALUADOR", "OBJ"])[["SBO"]].sum().reset_index()
group_df2["% AVANCE"] = group_df2["SBO"]/group_df2["OBJ"]*100

st.header("_SAFE TRAVEL FV_", divider='grey')
st.table(group_df2)

locale.setlocale(locale.LC_TIME, 'es_ES')

df2['PERIODO'] = pd.to_datetime(df2['PERIODO'], format='%Y%m')
df2['PERIODO'] = df2['PERIODO'].dt.strftime('%b').str.upper()
month_order = [
    'ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN', 'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'
]
df2['PERIODO'] = pd.Categorical(df2["PERIODO"], categories=month_order, ordered=True)
ventas_df2 = df2.groupby(['PERIODO'])[['SBO']].sum().reset_index()
ventas_df2 = ventas_df2.sort_values(by='PERIODO')
ventas_df2 = ventas_df2.reset_index(drop=True)

st.subheader('_Performance SBO Ventas_')
fig = px.bar(ventas_df2, x=ventas_df2['PERIODO'], y=ventas_df2['SBO'])
st.plotly_chart(fig, use_container_width=True)

periodo_condition_df3 = df3["PERIODO"].astype(str).str.startswith(periodo)
tipo_auditoria_condition_df3 = df3['TIPO AUDITORIA'] == 'Supervisor OP Tercero'
filtered_df3 = df3[periodo_condition_df3 & tipo_auditoria_condition_df3]
group_df3 = filtered_df3.groupby(["SITE", "OBJ"])[["SBO"]].sum().reset_index()
group_df3["% AVANCE"] = group_df3["SBO"]/group_df3["OBJ"]*100

st.header("_SUPERVISOR OP TERCERO_", divider='grey')
st.table(group_df3)

periodo_condition_df3 = df3["PERIODO"].astype(str).str.startswith(periodo)
tipo_auditoria_condition_df3 = df3['TIPO AUDITORIA'] == 'SAFE TRAVEL WPS'
filtered_df3 = df3[periodo_condition_df3 & tipo_auditoria_condition_df3]
group_df3 = filtered_df3.groupby(["SITE", "OBJ"])[["SBO"]].sum().reset_index()
group_df3["% AVANCE"] = group_df3["SBO"]/group_df3["OBJ"]*100

st.header("_SAFE TRAVEL WPS_", divider='grey')
st.table(group_df3)

df3['PERIODO'] = pd.to_datetime(df3['PERIODO'], format='%Y%m')
df3['PERIODO'] = df3['PERIODO'].dt.strftime('%b').str.upper()
df3['PERIODO'] = pd.Categorical(df3["PERIODO"], categories=month_order, ordered=True)
ventas_df3 = df3.groupby(['PERIODO', 'SITE'])[['SBO']].sum().reset_index()
ventas_df3 = ventas_df3.sort_values(by='PERIODO')
ventas_df3 = ventas_df3.reset_index(drop=True)

fig = px.bar(ventas_df3, x='PERIODO', y='SBO', color='SITE',
             labels={'SBO': 'Sales', 'PERIODO': 'Month'},
             category_orders={'PERIODO': month_order},
             height=600)

fig.update_layout(barmode='stack')

st.subheader('_Performance SBO Safe Travel WPS_')
st.plotly_chart(fig, use_container_width=True)

periodo_condition_df4 = df4["PERIODO"].astype(str).str.startswith(periodo)
filtered_df4 = df4[periodo_condition_df4]
group_df4 = filtered_df4.groupby(["SITE", "OBJ"])[["SBO"]].sum().reset_index()
group_df4["% AVANCE"] = group_df4["SBO"]/group_df4["OBJ"]*100

st.header("_MERCH_", divider='grey')
st.table(group_df4)

df4['PERIODO'] = pd.to_datetime(df4['PERIODO'], format='%Y%m')
df4['PERIODO'] = df4['PERIODO'].dt.strftime('%b').str.upper()
df4['PERIODO'] = pd.Categorical(df4["PERIODO"], categories=month_order, ordered=True)
ventas_df4 = df4.groupby(['PERIODO', 'SITE'])[['SBO']].sum().reset_index()
ventas_df4 = ventas_df4.sort_values(by='PERIODO')
ventas_df4 = ventas_df4.reset_index(drop=True)

fig = px.bar(ventas_df4, x='PERIODO', y='SBO', color='SITE',
             labels={'SBO': 'Sales', 'PERIODO': 'Month'},
             category_orders={'PERIODO': month_order},
             height=600)

fig.update_layout(barmode='stack')

st.subheader('_SBO Mercaderistas_')
st.plotly_chart(fig, use_container_width=True)