import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import calendar
import plotly.express as px
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="Bakery Sales Analysis", layout="wide")

# Load data
@st.cache_data
def load_data():
    bakery = pd.read_csv("../data/BakerySales.csv")
    bakery['datetime'] = pd.to_datetime(bakery['date'] + ' ' + bakery['time'])
    bakery['unit_price'] = bakery['unit_price'].str.replace('€', '').str.replace(',', '.').astype(float)
    bakery['total_price'] = bakery['Quantity'] * bakery['unit_price']
    bakery['date'] = bakery['datetime'].dt.date
    bakery['time'] = bakery['datetime'].dt.time
    bakery['hour'] = bakery['datetime'].dt.hour
    bakery['week'] = bakery['datetime'].dt.isocalendar().week
    bakery['weekday'] = bakery['datetime'].dt.weekday
    bakery['month'] = bakery['datetime'].dt.month
    return bakery

bakery = load_data()

# Define sidebar filters
day_names = list(calendar.day_name)
with st.sidebar:
    st.header("Filters")
    #date_range = st.date_input("Select date range", [bakery['date'].min(), bakery['date'].max()])

    min_date = bakery['date'].min()
    max_date = bakery['date'].max()
    
    date_range = st.date_input("Select date range", [min_date, max_date], min_value=min_date, max_value=max_date)

    selected_days = st.multiselect("Select weekdays", options=day_names, default=day_names)

    selected_products = st.multiselect("Select products", options=bakery['article'].unique(), default=bakery['article'].unique())
    
    # Filter the data
    filtered_data = bakery[(bakery['date'] >= date_range[0]) & (bakery['date'] <= date_range[1])]
    filtered_data = filtered_data[filtered_data['article'].isin(selected_products)]
    filtered_data = filtered_data[filtered_data['weekday'].apply(lambda x: calendar.day_name[x] in selected_days)]

# Main title
st.title("Bakery Sales Analysis")

# Create tabs
tab0, tab1, tab2, tab3, tab4, tab5 = st.tabs(["Introduction","Daily Sales", "Hourly Sales", "Weekly Sales", "Popular Products", "UnPopular Products"])

with tab0:
    st.header("Introduction")
    st.write(""" 
        This analysis is based on a bakery's daily sales data, making it possible to identify the most popular products, analyze hourly and weekly trends, and provide recommendations for optimizing inventory management and maximizing revenues.

        The main objectives are:
        - Reduce food waste
        - Maximize sales
        - Efficient inventory management
        - Improve customer experience         
        
        *Data source: [French Bakery Daily Sales Analysis](https://www.kaggle.com/code/clairemtian/french-bakery-daily-sales-analysis)*
    """)
    # import image
    from PIL import Image
    img = Image.open('../media/bakery.webp')
    st.image(img)

    # Display a preview of the filtered data
    st.header("Data Overview")
    st.write(filtered_data.iloc[:, 3:9].head())

    # Add a sidebar with some statistics
    st.header("Overview")
    st.write(f"Total number of unique transactions: {len(filtered_data['ticket_number'].unique())}")
    st.write(f"Sales revenue: {filtered_data['total_price'].sum():.2f} €")
    st.write(f"Unique number of products: {filtered_data['article'].nunique()}")
    st.write(f"Coverage period: from {filtered_data['date'].min()} to {filtered_data['date'].max()}")
with tab1:
    st.header("Daily Sales")
    
    daily_sales = filtered_data.groupby('date')['total_price'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(daily_sales['date'], daily_sales['total_price'])
    ax.set_title('Daily Sales')
    ax.set_xlabel('Date')
    ax.set_ylabel('Total Sales (€)')
    plt.xticks(rotation=45)
    st.pyplot(fig)
    
    # Extract the peak day and its sales
    peak_day = daily_sales.loc[daily_sales['total_price'].idxmax()]

    st.write(f"""
    During the period from **{date_range[0]}** to **{date_range[1]}**, the highest sales were recorded on **{peak_day['date']}** with a total of **{peak_day['total_price']:.2f} €**.
    This peak indicates that this day had exceptional sales, possibly due to special events or promotions.
    """)

with tab2:
    st.header("Hourly Sales")
    
    hourly_sales = filtered_data.groupby('hour')['total_price'].sum()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    hourly_sales.plot(kind='bar', ax=ax)
    ax.set_title('Hourly sales pattern')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Total sales (€)')
    st.pyplot(fig)
    
    # Extract the peak hour and its sales
    peak_hour = hourly_sales.idxmax()
    peak_hour_sales = hourly_sales.max()

    st.write(f"""
    During the period from **{date_range[0]}** to **{date_range[1]}**, the highest sales occurred at **{peak_hour}:00**, with a total of **{peak_hour_sales:.2f} €**.
    This suggests that **{peak_hour}:00** is a peak time for sales, indicating higher customer traffic at this hour.
    """)

with tab3:
    st.header("Weekly Sales")
    
    week_sales = filtered_data.groupby('weekday')['total_price'].sum()
    week_sales.index = week_sales.index.map(lambda x: calendar.day_name[x])

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(week_sales.index, week_sales.values)
    ax.set_title('Weekly sales pattern')
    ax.set_xlabel('Day')
    ax.set_ylabel('Total Sales (€)')
    st.pyplot(fig)
    
    # Extract the peak day and its sales
    peak_day = week_sales.idxmax()
    peak_day_sales = week_sales.max()

    st.write(f"""
    During the period from **{date_range[0]}** to **{date_range[1]}**, the highest sales were recorded on **{peak_day}**, with a total of **{peak_day_sales:.2f} €**.
    This indicates that **{peak_day}** is a key day for sales. You might consider focusing resources and promotions on this day to maximize sales.
    """)

with tab4:
    st.header("Popular Products")
    
    top_products = filtered_data.groupby('article')['Quantity'].sum().sort_values(ascending=False).head(10)
    top_products = top_products.astype(int)
    fig, ax = plt.subplots(figsize=(10, 6))
    top_products.plot(kind='bar', ax=ax)
    ax.set_title('Top 10 Best-Selling Products')
    ax.set_xlabel('Product')
    ax.set_ylabel('Total quantity sold')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

    st.subheader("Treemap of Quantities Sold for Top 10 Products")
    treemap_fig = px.treemap(top_products.reset_index(), 
                             path=['article'], 
                             values='Quantity', 
                             title='')
    st.plotly_chart(treemap_fig)
    
    # Extract the top-selling product and its quantity
    top_product = top_products.idxmax()
    top_product_quantity = top_products.max()

    st.write(f"""
    During the selected period from **{date_range[0]}** to **{date_range[1]}**, **{top_product}** was the best-selling product, with a total of **{top_product_quantity}** units sold.
    This product's popularity suggests strong customer preference, making it crucial to ensure its availability.
    """)

with tab5:
    st.header("UnPopular Products")
    
    unpopular_products = filtered_data.groupby('article')['Quantity'].sum().sort_values(ascending=True).head(10)
    unpopular_products = unpopular_products.astype(int)

    fig, ax = plt.subplots(figsize=(10, 6))
    unpopular_products.plot(kind='bar', ax=ax)
    ax.set_title('The 10 Unpopular Products')
    ax.set_xlabel('Product')
    ax.set_ylabel('Total quantity sold')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    
    st.subheader("Quantities Sold for the 10 UnPopular Products")
    st.table(unpopular_products.reset_index().rename(columns={'article': 'Product', 'Quantity': 'Quantity Sold'}))
    
    # Extract the least popular product and its quantity
    least_popular_product = unpopular_products.idxmin()
    least_popular_quantity = unpopular_products.min()
    
    st.write(f"""
    During the selected period from **{date_range[0]}** to **{date_range[1]}**, **{least_popular_product}** was the least popular product, with only **{least_popular_quantity}** units sold.
    This suggests potential issues with this product, such as pricing, visibility, or customer preference, that may need to be addressed.
    """)
