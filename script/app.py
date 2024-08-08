# Import libraries
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

# Main title
st.title("Bakery Sales Analysis")

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Daily Sales", "Popular Products", "Hourly Sales", "Weekly Sales", "Analyses Supplémentaires"])

with tab1:
    st.header("Daily Sales")
    
    daily_sales = bakery.groupby('date')['total_price'].sum().reset_index()
    
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
    st.header("Popular Products")
    
    top_products = bakery.groupby('article')['Quantity'].sum().sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    top_products.plot(kind='bar', ax=ax)
    ax.set_title('Top 10 Best-Selling Products')
    ax.set_xlabel('Product')
    ax.set_ylabel('Total quantity sold')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
    
    st.write("""
    The barplot shows that among the ten best-selling products, TRADITIONAL_BAGUETTE stands out as the best-selling product.
    """)

with tab3:
    st.header("Hourly Sales")
    
    hourly_sales = bakery.groupby('hour')['total_price'].sum()
    
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

with tab4:
    st.header("Weekly Sales")
    
    week_sales = bakery.groupby('weekday')['total_price'].sum()
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

with tab5:
    st.header("Analyses Supplémentaires")
    
    # Monthly sales trend
    monthly_sales = bakery.groupby('month')['total_price'].sum().reset_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(monthly_sales['month'], monthly_sales['total_price'], marker='o')
    ax.set_title('Tendance des Ventes Mensuelles')
    ax.set_xlabel('Mois')
    ax.set_ylabel('Ventes Totales (€)')
    ax.set_xticks(range(1, 13))
    st.pyplot(fig)
    
    st.write("""
    Ce graphique montre l'évolution des ventes mensuelles.
    Il permet d'identifier les mois les plus performants et les variations saisonnières sur l'ensemble de l'année.
    """)
    
    # Extract category from 'article' and compute total sales per category
    bakery['category'] = bakery['article'].apply(lambda x: x.split()[0])
    category_sales = bakery.groupby('category')['total_price'].sum().sort_values(ascending=False)

    # Select top 15 categories
    top_20_categories = category_sales.head(15)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    top_20_categories.plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title('Répartition des Ventes par Catégorie de Produits')
    ax.set_ylabel('')  # Hide y-label
    st.pyplot(fig)

    st.write("""
    Ce graphique en camembert montre la répartition des ventes totales par catégorie de produits.
    Il permet d'identifier les catégories les plus importantes en termes de chiffre d'affaires.
    """)
    
    # Correlation heatmap
    correlation = bakery[['Quantity', 'unit_price', 'total_price', 'hour', 'week']].corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Carte de Corrélation')
    st.pyplot(fig)
    
    st.write("""
    Cette carte de chaleur montre les corrélations entre différentes variables.
    Elle permet d'identifier les relations potentielles entre la quantité vendue, le prix unitaire, le prix total, l'heure de la journée et la semaine de l'année.
    """)

# Add a sidebar with some statistics
st.sidebar.header("Statistiques Générales")
st.sidebar.write(f"Nombre total de transactions: {len(bakery)}")
st.sidebar.write(f"Chiffre d'affaires total: {bakery['total_price'].sum():.2f} €")
st.sidebar.write(f"Nombre de produits uniques: {bakery['article'].nunique()}")
st.sidebar.write(f"Période couverte: du {bakery['date'].min()} au {bakery['date'].max()}")