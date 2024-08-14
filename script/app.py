import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
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


    selected_products = st.multiselect("Select products", options=bakery['article'].unique(), default=bakery['article'].unique())
    selected_days = st.multiselect("Select weekdays", options=day_names, default=day_names)

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
        This analysis of bakery sales aims to raise awareness among the general public and industry professionals of the vital importance of data analysis in optimizing the management of food businesses. 

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
    
    st.write("""
    The plot shows significant sales peaks on August, suggesting strong demand, probably due to seasonal factors such as the summer vacations. This indicates a key period for maximizing revenues.
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
    
    st.write("""
    The hourly sales pattern shows that sales are highest in the morning, with a peak at 11am. Sales are almost non-existent between 2pm and 4pm, then pick up slightly in the evening.
    This can be useful for example to plan staffing accordingly by increasing personnel during morning peak hours and reducing it in the afternoon. Additionally, manage inventory more effectively to prevent overstocking or shortages, particularly by preparing popular items before peak sales times.
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
    
    st.write("""
    The weekly sales pattern shows that sales peak at weekends, while they are particularly low on Wednesdays. It would make sense to boost stocks and staffing levels at weekends, and stimulate sales on Wednesdays with promotions or special offers to improve profitability.    
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

    # Create Pie Chart
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.pie(top_products, labels=top_products.index, autopct='%1.1f%%', startangle=140)
    ax.set_title('Top 10 Best-Selling Products')
    st.pyplot(fig)
    
    st.subheader("Quantities Sold for Top 10 Products")
    st.table(top_products.reset_index().rename(columns={'article': 'Product', 'Quantity': 'Quantity Sold'}))

    st.write("""
    The barplot shows that among the ten best-selling products, TRADITIONAL_BAGUETTE stands out as the best-selling product.
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
    
    st.write("""
    The barplot shows that among the ten unpopular products, PLAT_6.50E stands out as the least-selling product.
    """)