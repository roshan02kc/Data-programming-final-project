import pandas as pd  
import plotly.express as px  
import streamlit as st  

st.set_page_config(page_title="NEPSE", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache
def get_data_from_excel():
    df = pd.read_excel(
        io="stock_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:Y",
        nrows=1000,
    )
 
    return df

df = get_data_from_excel()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
symbol = st.sidebar.multiselect(
    "Select the Symbol:",
    options=df["Symbol"].unique(),
    default=df["Symbol"].unique()
)

df_selection = df.query(
    "Symbol == @symbol"
)

# ---- MAINPAGE ----
st.title(":bar_chart: Nepal Stock Exchange")
st.markdown("##")

# TOP KPI's
total_turnover = float(df_selection["Turnover"].sum())
total_qty = int(df_selection["Qty"].sum())


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Turnover:")
    st.subheader(f"Nepalese  रु {total_turnover:,}")
with middle_column:
    st.subheader("")
    #st.subheader(f"US $ {average_sale_by_transaction}")
with right_column:
    st.subheader("Total Volume Transaction:")
    st.subheader(f"Count ={total_qty:,}")

st.markdown("""---""")

# Company turnover [BAR CHART]
company_turnover = (
    df_selection.groupby(by=["Symbol"]).sum()[["Turnover"]].sort_values(by="Turnover")
)
fig_company_turnover = px.bar(
    company_turnover,
    x="Turnover",
    y=company_turnover.index,
    orientation="h",
    title="<b>Company Turnover</b>",
    color_discrete_sequence=["#0083B8"] * len(company_turnover),
    template="plotly_white",
)
fig_company_turnover.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

# Company Qty sales [BAR CHART]
company_qty = (
    df_selection.groupby(by=["Symbol"]).sum()[["Qty"]].sort_values(by="Qty")
)
fig_company_qty = px.bar(
    company_qty,
    x=company_qty.index,
    y="Qty",
    orientation="v",
    title="<b>Total Volume Transaction</b>",
    color_discrete_sequence=["#0083B8"] * len(company_qty),
    template="plotly_white",
)
fig_company_qty.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)



left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_company_qty, use_container_width=True)
right_column.plotly_chart(fig_company_turnover, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
