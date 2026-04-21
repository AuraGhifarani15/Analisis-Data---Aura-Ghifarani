import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import os

# --- Page Configuration ---
st.set_page_config(layout="wide", page_title="E-Commerce Data Analysis Dashboard")
st.title("E-Commerce Data Analysis Dashboard")

# --- Data Loading ---
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, 'main_data.csv')

    df = pd.read_csv(file_path)

    date_cols = [
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date', 'shipping_limit_date'
    ]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    numerical_product_cols = [
        'product_name_lenght', 'product_description_lenght', 'product_photos_qty',
        'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'
    ]
    for col in numerical_product_cols:
        df[col] = df[col].fillna(0)

    return df

@st.cache_data
def get_translated_product_categories():
    return {
        'beleza_saude': 'Beauty & Health',
        'relogios_presentes': 'Watches & Gifts',
        'cama_mesa_banho': 'Bed, Bath & Table',
        'esporte_lazer': 'Sport & Leisure',
        'informatica_acessorios': 'Computers & Accessories',
        'moveis_decoracao': 'Furniture & Decor',
        'automotivo': 'Automotive',
        'brinquedos': 'Toys',
        'telefonia': 'Telephony',
        'utilidades_domesticas': 'Home Appliances',
        'fashion_bolsas_e_acessorios': 'Fashion Bags & Accessories',
        'eletronicos': 'Electronics',
        'eletrodomesticos': 'Home Appliances',
        'instrumentos_musicais': 'Musical Instruments',
        'consoles_games': 'Consoles & Games',
        'pet_shop': 'Pet Shop',
        'livros_interesses_gerais': 'Books',
        'perfumaria': 'Perfumery',
        'alimentos': 'Food'
    }

# --- Load Data ---
main_data_df = load_data()
category_translation = get_translated_product_categories()

main_data_df['product_category_name'] = main_data_df['product_category_name'].map(category_translation).fillna('unknown')

# --- Revenue Analysis ---
@st.cache_data
def get_revenue_analysis(df, selected_year):
    df = df[df['order_purchase_timestamp'].dt.year == selected_year]

    if df.empty:
        return pd.DataFrame(), pd.DataFrame(), "No data"

    category_revenue = df.groupby('product_category_name')['price'].sum().reset_index()
    category_revenue = category_revenue.sort_values(by='price', ascending=False)

    total = category_revenue['price'].sum()
    category_revenue['percentage'] = category_revenue['price'] / total * 100

    pie_data = category_revenue.head(5)

    return category_revenue, pie_data, None

# --- RFM Analysis ---
@st.cache_data
def get_rfm_analysis(df, snapshot_date):
    snapshot_date = pd.to_datetime(snapshot_date)

    df = df.dropna(subset=['customer_unique_id','order_purchase_timestamp','order_id','price'])

    last_12_months = snapshot_date - dt.timedelta(days=365)

    df = df[
        (df['order_purchase_timestamp'] >= last_12_months) &
        (df['order_purchase_timestamp'] < snapshot_date)
    ]

    if df.empty:
        return pd.DataFrame(), pd.DataFrame(), "No data"

    rfm = df.groupby('customer_unique_id').agg(
        Recency=('order_purchase_timestamp', lambda x: (snapshot_date - x.max()).days),
        Frequency=('order_id','nunique'),
        Monetary=('price','sum')
    )

    rfm = rfm[rfm['Monetary'] > 0]

    rfm['R'] = pd.qcut(rfm['Recency'], 5, labels=False, duplicates='drop')
    rfm['R'] = rfm['R'].max() - rfm['R'] + 1
    rfm['F'] = pd.qcut(rfm['Frequency'], 5, labels=False, duplicates='drop') + 1
    rfm['M'] = pd.qcut(rfm['Monetary'], 5, labels=False, duplicates='drop') + 1

    rfm['Score'] = rfm[['R','F','M']].sum(axis=1)

    rfm['Segment'] = rfm['Score'].apply(lambda x:
        'High Value' if x >= 12 else
        'Mid Value' if x >= 8 else
        'Low Value'
    )

    return rfm, None, None

# --- Sidebar ---
st.sidebar.header("Filter")

years = sorted(main_data_df['order_purchase_timestamp'].dt.year.dropna().unique())
selected_year = st.sidebar.selectbox("Year", years)

snapshot_date = st.sidebar.date_input("Snapshot Date", dt.date(2019,1,1))

# --- Run Analysis ---
category_revenue, pie_data, err1 = get_revenue_analysis(main_data_df, selected_year)
rfm_df, _, err2 = get_rfm_analysis(main_data_df, snapshot_date)

# --- Revenue Display ---
st.header("Revenue Analysis")

if err1:
    st.warning(err1)
else:
    fig, ax = plt.subplots()
    sns.barplot(x='price', y='product_category_name', data=category_revenue.head(10), ax=ax)
    st.pyplot(fig)

# --- RFM Display ---
st.header("RFM Analysis")

if err2:
    st.warning(err2)
else:
    fig, ax = plt.subplots()
    sns.histplot(rfm_df['Score'], bins=10, ax=ax)
    st.pyplot(fig)

    st.dataframe(rfm_df.head(20))