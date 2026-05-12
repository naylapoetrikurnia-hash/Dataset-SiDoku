import streamlit as st
import pandas as pd
import plotly.express as px

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Inventory & Sales Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# ======================================================
# LOAD DATA
# ======================================================

df = pd.read_csv("data/sales_clean.csv")

# ======================================================
# FEATURE ENGINEERING
# ======================================================

# convert tanggal
df["SalesDate"] = pd.to_datetime(df["SalesDate"])

# bulan
df["Month"] = df["SalesDate"].dt.strftime("%b")

# nama hari
df["Weekday"] = df["SalesDate"].dt.day_name()

# total revenue
df["Revenue"] = df["SalesQuantity"] * df["SalesPrice"]

# weekday / weekend
df["DayType"] = df["SalesDate"].dt.dayofweek.apply(
    lambda x: "Weekend" if x >= 5 else "Weekday"
)

# kategori harga
def categorize_price(price):
    if price < 20:
        return "Low"
    elif price < 50:
        return "Medium"
    else:
        return "High"

df["PriceCategory"] = df["SalesPrice"].apply(categorize_price)

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.title("Sales Analytics")

    st.markdown("### Dashboard Filter")

    # filter tanggal
    date_range = st.date_input(
        "Pilih Rentang Tanggal",
        [
            df["SalesDate"].min(),
            df["SalesDate"].max()
        ]
    )

    # filter kategori harga
    category_filter = st.multiselect(
        "Kategori Harga",
        options=df["PriceCategory"].unique(),
        default=df["PriceCategory"].unique()
    )

# ======================================================
# FILTER DATA
# ======================================================

filtered_df = df.copy()

if len(date_range) == 2:
    filtered_df = filtered_df[
        (filtered_df["SalesDate"] >= pd.to_datetime(date_range[0])) &
        (filtered_df["SalesDate"] <= pd.to_datetime(date_range[1]))
    ]

filtered_df = filtered_df[
    filtered_df["PriceCategory"].isin(category_filter)
]

# ======================================================
# FONT AWESOME
# ======================================================

st.markdown("""
<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
""", unsafe_allow_html=True)

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

.main {
    background-color: #F4F8FB;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    background: linear-gradient(135deg,#001D39,#0A4174);
    padding: 40px;
    border-radius: 24px;
    color: white;
    margin-bottom: 30px;
    box-shadow: 0 18px 40px rgba(0,0,0,0.18);
}

.hero-title {
    font-size: 40px;
    font-weight: 800;
    line-height: 1.2;
}

.hero-text {
    font-size: 17px;
    opacity: 0.92;
    margin-top: 12px;
    line-height: 1.7;
}

.highlight-box {
    background: rgba(123,189,232,0.12);
    border: 1px solid rgba(255,255,255,0.08);
    border-left: 6px solid #4E8EA2;
    padding: 18px;
    border-radius: 18px;
    margin-top: 25px;
}

.highlight-item {
    margin-bottom: 12px;
    font-size: 16px;
}

.highlight-item i {
    margin-right: 10px;
}

.section-title {
    font-size: 30px;
    font-weight: 700;
    color: #001D39;
    margin-top: 45px;
    margin-bottom: 15px;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg,#ffffff,#F4F8FB);
    border: 1px solid #d7e6f0;
    backdrop-filter: blur(12px);
    padding: 24px;
    border-radius: 22px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.04);
    transition: 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 14px 28px rgba(0,0,0,0.08);
}
            
[data-testid="stMetricLabel"] {
    font-size: 15px;
    color: #64748b;
    font-weight: 600;
}

[data-testid="stMetricValue"] {
    font-size: 34px;
    font-weight: 800;
    color: #001D39;
}
            
.ai-box {
    background: linear-gradient(135deg,#001D39,#0A4174);
    padding: 35px;
    border-radius: 24px;
    color: white;
    margin-top: 25px;
    box-shadow: 0 12px 30px rgba(0,0,0,0.12);
}
            
hr {
    border: none;
    height: 1px;
    background: #dbe7ef;
    margin-top: 50px;
    margin-bottom: 60px;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# HERO SECTION
# ======================================================

st.markdown("""
<div class="hero">

<div style="display:flex; align-items:center; gap:22px;">

<div style="
background: rgba(255,255,255,0.15);
width:95px;
height:95px;
border-radius:24px;
display:flex;
align-items:center;
justify-content:center;
backdrop-filter: blur(10px);
border:1px solid rgba(255,255,255,0.18);
">

<i class="fa-solid fa-chart-pie"
style="
font-size:42px;
color:white;
"></i>

</div>

<div>

<div class="hero-title">
Inventory & Sales Analysis Dashboard
</div>

<div class="hero-text">
Dashboard ini digunakan untuk menganalisis pola penjualan,
tren revenue, performa produk, dan kategori harga
berdasarkan dataset Inventory Analysis Case Study.
</div>
            
<hr style="
border:none;
height:1px;
background:rgba(255,255,255,0.12);
margin-top:18px;
margin-bottom:20px;
">

</div>

</div>

<div class="highlight-box">

<div class="highlight-item">
<i class="fa-solid fa-boxes-stacked"></i>
Menganalisis distribusi dan performa produk penjualan.
</div>

<div class="highlight-item">
<i class="fa-solid fa-chart-column"></i>
Mengidentifikasi tren revenue dan aktivitas transaksi.
</div>

<div class="highlight-item">
<i class="fa-solid fa-money-bill-trend-up"></i>
Mendukung pengambilan keputusan berbasis data analytics.
</div>

</div>

</div>
""", unsafe_allow_html=True)

# ======================================================
# SALES PERFORMANCE OVERVIEW
# ======================================================

total_revenue = filtered_df["Revenue"].sum()

total_transactions = len(filtered_df)

best_selling_product = (
    filtered_df.groupby("Description")["SalesQuantity"]
    .sum()
    .sort_values(ascending=False)
    .index[0]
)

top_category = (
    filtered_df["PriceCategory"]
    .mode()[0]
)

st.markdown("""
<div class="section-title">
Sales Performance Overview
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Revenue",
    f"${total_revenue:,.0f}"
)

col2.metric(
    "Total Transactions",
    f"{total_transactions:,}"
)

col3.metric(
    "Best Selling Product",
    best_selling_product
)

col4.metric(
    "Top Price Category",
    top_category
)

st.markdown("<hr>", unsafe_allow_html=True)

# ======================================================
# REVENUE TREND ANALYSIS
# ======================================================

st.markdown("""
<div class="section-title">
📈 Revenue Trend Analysis
</div>
""", unsafe_allow_html=True)

monthly_revenue = (
    filtered_df.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

month_order = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

monthly_revenue["Month"] = pd.Categorical(
    monthly_revenue["Month"],
    categories=month_order,
    ordered=True
)

monthly_revenue = monthly_revenue.sort_values("Month")

fig = px.line(
    monthly_revenue,
    x="Month",
    y="Revenue",
    markers=True,
    template="plotly_white",
)

fig.update_traces(
    line=dict(width=4, color="#0A4174"),
    marker=dict(
        size=10,
        color="#7BBDE8",
        line=dict(width=2,color="#0A4174")
    )
)

fig.update_layout(
    height=500,
    title="Monthly Revenue Trend",
    title_font_size=24,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=20,r=20,t=60,b=20)
)

st.plotly_chart(fig, use_container_width=True)

monthly_revenue_value = (
    filtered_df.groupby("Month")["Revenue"]
    .sum()
)

highest_month = monthly_revenue_value.idxmax()
lowest_month = monthly_revenue_value.idxmin()

highest_value = monthly_revenue_value.max()
lowest_value = monthly_revenue_value.min()

st.markdown(f"""
<div class="highlight-box" style="
background: rgba(255,255,255,0.75);
color:#001D39;
border:1px solid #d5e5ef;
backdrop-filter: blur(10px);
line-height:1.7;
">

<b>Insight:</b><br>

Revenue tertinggi terjadi pada bulan <b>{highest_month}</b>
dengan total revenue sebesar
<b>${highest_value:,.0f}</b>.

Sedangkan revenue terendah terjadi pada bulan
<b>{lowest_month}</b> dengan total revenue sebesar
<b>${lowest_value:,.0f}</b>.

</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ======================================================
# TOP SELLING PRODUCTS
# ======================================================

st.markdown("""
<div class="section-title">
🏆 Top Selling Products
</div>
""", unsafe_allow_html=True)

top_products = (
    filtered_df.groupby("Description")["SalesQuantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_products,
    x="SalesQuantity",
    y="Description",
    orientation="h",
    template="plotly_white",
    text="SalesQuantity",
    color="SalesQuantity",
    color_continuous_scale=[
    "#BDD8E9",
    "#7BBDE8",
    "#49769F",
    "#0A4174"
]
)

fig.update_layout(
    height=600,
    title="Top 10 Best Selling Products",
    title_font_size=24,
    yaxis_title="Product",
    xaxis_title="Total Sales Quantity",
    coloraxis_showscale=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=20,r=20,t=60,b=20)
)

fig.update_traces(
    textposition="outside",
    marker_line_width=0
)

fig.update_yaxes(categoryorder="total ascending")

st.plotly_chart(fig, use_container_width=True)

top_product = top_products.iloc[0]["Description"]
top_sales = top_products.iloc[0]["SalesQuantity"]

st.markdown(f"""
<div class="highlight-box" style="
background: rgba(255,255,255,0.75);
color:#001D39;
border:1px solid #d5e5ef;
backdrop-filter: blur(10px);
line-height:1.7;
">

<b>Insight:</b><br>

Produk <b>{top_product}</b> memiliki jumlah penjualan
tertinggi dengan total
<b>{top_sales:,.0f}</b> transaksi.

</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ======================================================
# TOP REVENUE PRODUCTS
# ======================================================

st.markdown("""
<div class="section-title">
💰 Top Revenue Products
</div>
""", unsafe_allow_html=True)

top_revenue_products = (
    filtered_df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig = px.bar(
    top_revenue_products,
    x="Revenue",
    y="Description",
    orientation="h",
    template="plotly_white",
    text="Revenue",
    color="Revenue",
    color_continuous_scale=[
    "#BDD8E9",
    "#6EA2B3",
    "#4E8EA2",
    "#0A4174"
]
)

fig.update_traces(
    texttemplate='$%{text:,.0f}',
    textposition="outside",
    marker_line_width=0
)

fig.update_layout(
    height=600,
    title="Top 10 Products by Revenue",
    title_font_size=24,
    yaxis_title="Product",
    xaxis_title="Total Revenue",
    plot_bgcolor="white",
    paper_bgcolor="white",
    coloraxis_showscale=False,
    margin=dict(l=20,r=20,t=60,b=20)
)

fig.update_yaxes(categoryorder="total ascending")

st.plotly_chart(fig, use_container_width=True)

top_rev_product = top_revenue_products.iloc[0]["Description"]
top_rev_value = top_revenue_products.iloc[0]["Revenue"]

st.markdown(f"""
<div class="highlight-box" style="
background: rgba(255,255,255,0.75);
color:#001D39;
border:1px solid #d5e5ef;
backdrop-filter: blur(10px);
line-height:1.7;
">

<b>Insight:</b><br>

Produk <b>{top_rev_product}</b> menghasilkan revenue
tertinggi sebesar
<b>${top_rev_value:,.0f}</b>.

</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ======================================================
# PRICE CATEGORY ANALYSIS
# ======================================================

st.markdown("""
<div class="section-title">
🍩 Price Category Analysis
</div>
""", unsafe_allow_html=True)

price_category = (
    filtered_df.groupby("PriceCategory")["SalesQuantity"]
    .sum()
    .reset_index()
)

fig = px.pie(
    price_category,
    names="PriceCategory",
    values="SalesQuantity",
    hole=0.6,
    color="PriceCategory",
    color_discrete_map={
        "Low": "#BDD8E9",
        "Medium": "#7BBDE8",
        "High": "#0A4174"
    }
)

fig.update_traces(
    textposition="inside",
    textinfo="percent+label"
)

fig.update_layout(
    height=500,
    title="Sales Distribution by Price Category",
    title_font_size=24,
    showlegend=False,
    paper_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)

dominant_category = (
    price_category.sort_values(
        by="SalesQuantity",
        ascending=False
    )
    .iloc[0]["PriceCategory"]
)

st.markdown(f"""
<div class="highlight-box" style="
background: rgba(255,255,255,0.75);
color:#001D39;
border:1px solid #d5e5ef;
backdrop-filter: blur(10px);
line-height:1.7;
">

<b>Insight:</b><br>

Kategori harga <b>{dominant_category}</b>
mendominasi aktivitas transaksi penjualan
dibanding kategori lainnya.

</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ======================================================
# WEEKDAY VS WEEKEND ANALYSIS
# ======================================================

st.markdown("""
<div class="section-title">
📅 Weekday vs Weekend Analysis
</div>
""", unsafe_allow_html=True)

day_analysis = (
    filtered_df.groupby("DayType")["SalesQuantity"]
    .sum()
    .reset_index()
)

fig = px.bar(
    day_analysis,
    x="DayType",
    y="SalesQuantity",
    color="DayType",
    text="SalesQuantity",
    template="plotly_white",
    color_discrete_map={
        "Weekday": "#4E8EA2",
        "Weekend": "#0A4174"
    }
)

fig.update_traces(
    textposition="outside",
    marker_line_width=0
)

fig.update_layout(
    height=500,
    title="Transaction Activity: Weekday vs Weekend",
    title_font_size=24,
    xaxis_title="Day Type",
    yaxis_title="Total Transactions",
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=20,r=20,t=60,b=20)
)

st.plotly_chart(fig, use_container_width=True)

weekday_value = day_analysis[
    day_analysis["DayType"] == "Weekday"
]["SalesQuantity"].values[0]

weekend_value = day_analysis[
    day_analysis["DayType"] == "Weekend"
]["SalesQuantity"].values[0]

st.markdown(f"""
<div class="highlight-box" style="
background: rgba(255,255,255,0.75);
color:#001D39;
border:1px solid #d5e5ef;
backdrop-filter: blur(10px);
line-height:1.7;
">

<b>Insight:</b><br>

Aktivitas transaksi weekday lebih tinggi
dengan total
<b>{weekday_value:,.0f}</b> transaksi,
dibanding weekend sebesar
<b>{weekend_value:,.0f}</b>.

</div>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ======================================================
# FINAL BUSINESS INSIGHT
# ======================================================

st.markdown("""
<div class="section-title" style="
margin-bottom:22px;
">
💡 Final Business Insight
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="ai-box" style="
padding:38px;
">

<h2 style="
margin-top:0;
font-size:38px;
line-height:1.3;
margin-bottom:34px;
">
🧠 Business Analytics Summary
</h2>

<div style="
font-size:17px;
color:white;
font-weight:500;
">

📈 Revenue tertinggi terjadi pada bulan
<b>{highest_month}</b>.

🏆 Produk dengan performa terbaik adalah
<b>{top_product}</b>.

🛍️ Kategori paling dominan yaitu
<b>{dominant_category}</b>.

</div>

</div>
""", unsafe_allow_html=True)

top_day = (
    day_analysis.sort_values(
        by="SalesQuantity",
        ascending=False
    )
    .iloc[0]["DayType"]
)

# ======================================================
# STRATEGIC RECOMMENDATION
# ======================================================

st.markdown(f"""
<div style="
background: linear-gradient(
135deg,
rgba(189,216,233,0.22),
rgba(123,189,232,0.10)
);
padding:38px;
border-radius:24px;
border:1px solid rgba(78,142,162,0.25);
margin-top:16px;
backdrop-filter: blur(14px);
box-shadow:0 10px 25px rgba(0,0,0,0.05);
">

<h2 style="
margin-top:0;
font-size:38px;
line-height:1.3;
margin-bottom:34px;
color:#0A4174;
">
🚀 Strategic Recommendation
</h2>

<div style="
font-size:17px;
color:#334155;
font-weight:500;
">

<div style="margin-bottom:20px; line-height:1.7;">
• Fokuskan promosi pada produk dengan revenue tertinggi
untuk meningkatkan profit secara signifikan.
</div>

<div style="margin-bottom:20px; line-height:1.7;">
• Tingkatkan ketersediaan stok kategori medium
karena memiliki permintaan transaksi paling dominan.
</div>

<div style="margin-bottom:20px; line-height:1.7;">
• Maksimalkan campaign akhir tahun saat tren revenue
mengalami peningkatan tertinggi.
</div>

<div style="line-height:1.7;">
• Optimalkan aktivitas operasional pada <b>{top_day}</b>
karena transaksi lebih aktif dibanding periode lainnya.
</div>

</div>

</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.sidebar.markdown("""
<div style='font-size:13px; color:gray;'>

Inventory Analysis Dashboard<br>
Data Analytics & Visualization Project<br><br>

</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='text-align:center;
margin-top:40px;
color:gray;
font-size:14px;'>

Inventory & Sales Analysis Dashboard • 2026

</div>
""", unsafe_allow_html=True)