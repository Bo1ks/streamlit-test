# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title = "銷售數據表",
                   page_icon = ":bar_chart:",
                   layout = "wide",
                   )

#要防止每跑一次streamlit就跑去讀取一次資料來源的話，可以使用@st.cache + 把讀取資料定義成函數再呼叫來進行。
df = pd.read_excel(r'C:\Users\User\Documents\test.xlsx')



#------側功能欄------
st.sidebar.header("請選擇想篩選的類別:")
city = st.sidebar.multiselect(
    "請選擇縣市:",
    options = df["City"].unique(),
    default = df["City"].unique()
    )

gender = st.sidebar.multiselect(
    "請選擇性別:",
    options = df["Gender"].unique(),
    default = df["Gender"].unique()
    )

item = st.sidebar.multiselect(
    "請選擇購買件數:",
    options = df["Items"].unique(),
    default = df["Items"].unique()
    )

df_selection = df.query(
    "City == @city & Gender == @gender & Items == @item"
    )

#st.dataframe(df_selection)



#------頂端功能欄------
st.title(":bar_chart: 銷售指標")
st.markdown("##")



#------關鍵指標------
total_items = int(df_selection["Items"].sum())
total_price = int(df_selection["Total Price"].sum())
average_items = round(df_selection["Items"].mean(), 1)
average_price = round(df_selection["Total Price"].mean(), 1)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("總銷售件數:")
    st.subheader(f"{total_items:,}件")
with middle_column:
    st.subheader("總銷售金額:")
    st.subheader(f"NTD $ {total_price:,} 元")
with right_column:
    st.subheader("平均銷售金額:")
    st.subheader(f"NTD $ {average_price:,} 元")

st.markdown("---")



#------橫條圖------
sales_by_store = (
    df_selection.groupby(by=["Store"]).sum()[["Total Price"]].sort_values(by="Total Price")
    )
fig_store = px.bar(
    sales_by_store,
    x = "Total Price",
    y = sales_by_store.index,
    orientation = "h",
    title = "<b>各店鋪銷售額</b>",
    color_discrete_sequence = ["#0083B8"] * len(sales_by_store),
    template = "plotly_white",
    )

fig_store.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis = (dict(showgrid=False))
    )

#st.plotly_chart(fig_store)



#------直線圖------

sales_by_vip = (
    df_selection.groupby(by=["VIP"]).sum()[["Total Price"]].sort_values(by="Total Price")
    )
fig_vip = px.bar(
    sales_by_vip,
    x = sales_by_vip.index,
    y = "Total Price",
    title = "<b>VIP銷售額</b>",
    color_discrete_sequence = ["#0083B8"] * len(sales_by_vip),
    template = "plotly_white",
    )

fig_vip.update_layout(
    xaxis = dict(tickmode = "linear"),
    plot_bgcolor = "rgba(0,0,0,0)",
    yaxis = (dict(showgrid=False)),
    )

#st.plotly_chart(fig_vip)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_store, use_container_width = True)
right_column.plotly_chart(fig_vip, use_container_width = True)



#------隱藏不必要的外框跟資訊------
#hide_st_style = """
#<style>
#MainMenu {visibility: hidden;}
#footer {visibility: hidden;}
#header {visibility: hidden;}
#</style>
#"""
##st.markdown(hide_st_style, unsafe_allow_html=True)



#------sss------
