# Bakery Sales Analysis

## Description

This repository contains a Streamlit app for analyzing bakery sales data. The app offers insights into daily, hourly, and weekly sales trends, as well as identifying the most and least popular products.

You can view the deployed application here: [Bakery Sales Analysis](https://bakerysales.streamlit.app/).

## Features

- **Daily Sales Analysis**: Visualize daily sales pattern.
- **Hourly Sales Analysis**: Visualize hourly sales pattern.
- **Weekly Sales Analysis**: Visualize weekly sales pattern.
- **Popular Products**: Analyze the top 10 best-selling products with a Treemap/Barplot visualization.
- **Unpopular Products**: Analyze the 10 least popular products with a bar chart visualization.

## Prerequisites

This project uses a Conda environment to manage dependencies. You can create and activate this environment using the provided `environment.yml` file.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/bakery-sales-analysis.git
    ```

2. **Navigate to the project directory**:

    ```bash
    cd bakery-sales-analysis
    ```

3. **Create and activate the Conda environment**:

    ```bash
    conda env create -f environment.yml
    conda activate bakery
    ```

## Usage

1. **Run the Streamlit application locally**:

    Ensure you're in the project directory and the Conda environment is activated, then launch the Streamlit app with:

    ```bash
    streamlit run script/app.py
    ```

2. **Access the application**:

    Once the application is running, open a web browser and go to: [http://localhost:8501](http://localhost:8501).

3. **Access the online application**:

    You can also access the hosted version of the application via this link: [Bakery Sales Analysis](https://bakerysales.streamlit.app/).

## File Structure

- `environment.yml` : Conda environment configuration file.
- `data/BakerySales.csv` : CSV file containing the sales data.
- `media/bakery.webp` : Image used in the introduction.
- `script/app.py` : Main script containing the Streamlit application code.
- `script/requirements.txt` : Additional Python packages that can be installed via pip.

## Data

Source: [French Bakery Daily Sales Analysis](https://www.kaggle.com/code/clairemtian/french-bakery-daily-sales-analysis).

