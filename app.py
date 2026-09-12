import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Cloud Sales Data Analytics",
    page_icon="☁️",
    layout="wide"
)

# Load dataset
df = pd.read_csv("sales_data.csv")
df["Date"] = pd.to_datetime(df["Date"])

# Title
st.title("☁️ Cloud Sales Data Analytics")
st.markdown("### Cloud-based Sales Performance Dashboard")

# Sidebar filters
st.sidebar.header("🔎 Filters")

regions = ["All"] + sorted(df["Region"].unique().tolist())
selected_region = st.sidebar.selectbox("Select Region", regions)

categories = ["All"] + sorted(df["Category"].unique().tolist())
selected_category = st.sidebar.selectbox("Select Category", categories)

# Apply filters
filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

# KPI calculations
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order_ID"].nunique()
total_quantity = filtered_df["Quantity"].sum()

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
col2.metric("📈 Total Profit", f"₹{total_profit:,.0f}")
col3.metric("🛒 Total Orders", total_orders)
col4.metric("📦 Quantity Sold", total_quantity)

st.divider()

# Monthly Sales
monthly_sales = (
    filtered_df.groupby(filtered_df["Date"].dt.strftime("%B"))["Sales"]
    .sum()
    .reset_index()
)

month_order = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

monthly_sales["Month"] = pd.Categorical(
    monthly_sales["Date"],
    categories=month_order,
    ordered=True
)

monthly_sales = monthly_sales.sort_values("Month")

fig_month = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="📅 Monthly Sales Trend"
)

st.plotly_chart(fig_month, use_container_width=True)

# Two-column charts
col1, col2 = st.columns(2)

with col1:
    region_sales = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig_region = px.bar(
        region_sales,
        x="Region",
        y="Sales",
        title="🌍 Region-wise Sales"
    )

    st.plotly_chart(fig_region, use_container_width=True)

with col2:
    category_sales = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig_category = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        title="📊 Category-wise Sales"
    )

    st.plotly_chart(fig_category, use_container_width=True)

# Product performance
st.subheader("🏆 Product Performance")

product_sales = (
    filtered_df.groupby("Product")
    .agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    )
    .reset_index()
    .sort_values("Sales", ascending=False)
)

fig_product = px.bar(
    product_sales,
    x="Product",
    y="Sales",
    title="Top Products by Sales"
)

st.plotly_chart(fig_product, use_container_width=True)

# Sales data table
st.subheader("📋 Sales Data")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

# Footer
st.divider()
st.caption("CCS335 Cloud Computing | Cloud Sales Data Analytics Project")