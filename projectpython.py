import streamlit as st
import plotly.express as px
import pandas as pd
import datetime
from PIL import Image
import plotly.graph_objects as go

#reading the data from excel
df=pd.read_excel("Adidas.xlsx")
st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
image=Image.open('logo-adidas-baru.jpg')

col1, col2 = st.columns([0.1,0.9])
with col1:
    st.image(image,width=100)

html_title = """
    <style>
    .title-test {
    font-weight : bold;
    padding : 5px;
    border-radius:6px
    }
    </style>
    <center><h1 class="title-test">Adidas Sales Performance Overview: 2020–2021</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)

# Hitung ukuran pemusatan
mean = df["TotalSales"].mean()
median = df["TotalSales"].median()

# Buat DataFrame ukuran pemusatan
central_tendency = pd.DataFrame({
    "Measure": ["Mean", "Median"],
    "TotalSales": [mean, median]
})

# Buat chart
fig5 = go.Figure(data=[
    go.Bar(
        name="Ukuran Pemusatan",
        x=central_tendency["Measure"],
        y=central_tendency["TotalSales"],
        text=[f"${val:,.0f}" for val in central_tendency["TotalSales"]],
        textposition='auto',
        marker_color=["#636EFA", "#EF553B"]
    )
])

fig5.update_layout(
    title="Ukuran Pemusatan Data Total Sales",
    yaxis_title="Total Sales ($)",
    xaxis_title="Ukuran Pemusatan",
    template="plotly_white"
)

_, col3 = st.columns([0.1, 1])
with col3:
    st.plotly_chart(fig5, use_container_width=True)

_, view6, dwn6 = st.columns([0.1, 0.45, 0.45])
with view6:
    expander = st.expander("Ukuran Pemusatan Total Sales")
    expander.write(central_tendency)

with dwn6:
    st.download_button("Download Data", data = central_tendency.to_csv().encode("utf-8"),
                       file_name="Central_Tendency_TotalSales.csv", mime="text/csv")

col4, col5, col6 = st.columns([0.1,0.45,0.45])
with col4:
    box_date = str(datetime.datetime.now().strftime("%d %B %Y"))
    st.write("Presented by Kelompok 9")

with col5:
    grouped_df = df.groupby("Product", as_index=False)["TotalSales"].sum()
    
    fig = px.bar(grouped_df, x="Product", y="TotalSales", labels={"TotalSales": "Total Sales{$}"},
                 title="Total Sales by Product", hover_data=["TotalSales"],
                 template="gridon", height=500)
    st.plotly_chart(fig, use_container_width=True)

_, view1, dwn1, view2, dwn2 = st.columns([0.15,0.20,0.20,0.20,0.20])
with view1:
    expander = st.expander("Product Sales")
    data = df[["Product","TotalSales"]].groupby(by="Product")["TotalSales"].sum()
    expander.write(data)
with dwn1:
    st.download_button("Get Data", data = data.to_csv().encode("utf-8"),
                       file_name="ProductSales.csv", mime="text/csv")


df["Month_Year"] = df["InvoiceDate"].dt.to_period("M").dt.to_timestamp()

result = df.groupby("Month_Year")["TotalSales"].sum().reset_index()

result["Month_Year_Str"] = result["Month_Year"].dt.strftime("%b'%y")

with col6:
    fig1 = px.line(result, x="Month_Year_Str", y="TotalSales", 
                   title="Total Sales Over Time", template="gridon")
    st.plotly_chart(fig1, use_container_width=True)

with view2:
    expander = st.expander("Monthly Sales")
    data=result
    expander.write (data)
with dwn2:
    st.download_button("Get Data", data=result.to_csv().encode("utf-8"),
                        file_name="Monthly Sales.csv", mime ="text/csv")  

st.divider()

result1 = df.groupby(by="State")[["TotalSales", "UnitsSold"]].sum().reset_index()

#add the units sold as a line chart on a secondary y-axis
fig3 = go.Figure()
fig3.add_trace(go.Bar(x=result1["State"],y=result1["TotalSales"],name="Total Sales"))
fig3.add_trace(go.Scatter(x=result1["State"],y=result1["UnitsSold"],mode="lines",name="Units Sold",yaxis="y2"))
fig3.update_layout(
    title="Total Sales and Units Sold by State",
    xaxis = dict(title="State"),
    yaxis=dict(title="Total Sales", showgrid = False),
    yaxis2 = dict(title="Units Sold", overlaying="y", side = "right"),
    template = "gridon",
    legend = dict (x=1,y=1.1)
)
_, col7 = st.columns([0.1,1])
with col7:
    st.plotly_chart(fig3,use_container_width=True)

_, view3, dwn3 = st.columns([0.5, 0.45, 0.45])
with view3:
    expander = st.expander("View Data for Sales by Units Sold")
    expander.write(result1)
with dwn3:
    st.download_button("Get Data", data = result1.to_csv().encode("utf-8"),
                       file_name = "Sales_by_UnitsSold.csv", mime="text/csv")

st.divider()

# Hitung total Operating Profit per Retailer
op_by_retailer = df.groupby("Retailer")["OperatingProfit"].sum().reset_index()

# Buat chart
fig_op = px.bar(
    op_by_retailer,
    x="Retailer",
    y="OperatingProfit",
    title="Operating Profit by Retailer",
    labels={"OperatingProfit": "Operating Profit ($)"},
    template="gridon",
    color="Retailer"
)

# Tampilkan chart di Streamlit
_, col_op = st.columns([0.1, 1])
with col_op:
    st.plotly_chart(fig_op, use_container_width=True)

# Tambahkan opsi lihat & download data
_, view_op, dwn_op = st.columns([0.1, 0.45, 0.45])
with view_op:
    expander = st.expander("View Data for Operating Profit by Retailer")
    expander.write(op_by_retailer)

with dwn_op:
    st.download_button("Download Data", data=op_by_retailer.to_csv().encode("utf-8"),
                       file_name="OperatingProfit_by_Retailer.csv", mime="text/csv")


_, col8 = st.columns([0.1, 1])
treemap = df[["State", "Product", "TotalSales"]].groupby(by=["State", "Product"])["TotalSales"].sum().reset_index()

def format_sales(value):
    if value >= 0:
        return '{:.2f} Lakh'.format(value / 1_000_00)

treemap["TotalSales (Formatted)"] = treemap["TotalSales"].apply(format_sales)

fig4 = px.treemap(
    treemap, 
    path=["State", "Product"], 
    values="TotalSales",
    hover_name="TotalSales (Formatted)",
    hover_data=["TotalSales (Formatted)"],
    color="Product", 
    height=700, 
    width=600
)

fig4.update_traces(textinfo="label+value")

with col8:
    st.subheader(":point_right: Total Sales by State and Product in Treemap")
    st.plotly_chart(fig4, use_container_width=True)

_, view4, dwn4 = st.columns([0.1, 0.45, 0.45])
with view4:
    result2 = df[["State", "Product", "TotalSales"]].groupby(by=["State", "Product"])["TotalSales"].sum()
    expander = st.expander("View data for Total Sales by State and Product")
    expander.write(result2)

with dwn4:
    st.download_button("Get Data", data = result2.to_csv().encode("utf-8"),
                       file_name="Sales_by_State.csv", mime="text/csv")
    

st.divider()