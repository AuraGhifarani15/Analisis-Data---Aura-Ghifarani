import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import os

st.set_page_config(layout="wide")
st.title('Analisis Data E-Commerce Anda')
st.write('Selamat datang di aplikasi Streamlit Aura. Di sini Anda bisa melihat semua hasil analisis.')

try:
    # --- Memuat data utama yang diperlukan untuk analisis (dari direktori root Colab) ---
    orders = pd.read_csv('../Data/orders_dataset.csv')
    order_items = pd.read_csv('../Data/order_items_dataset.csv')
    products = pd.read_csv('../Data/products_dataset.csv')
    customers = pd.read_csv('../Data/customers_dataset.csv')

    # --- Cleaning data orders seperti di notebook ---
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders = orders.dropna()

    # --- Persiapan Data untuk Analisis Revenue ---
    orders_items_df = pd.merge(orders, order_items, on='order_id', how='inner')
    df_revenue_analysis = pd.merge(orders_items_df, products, on='product_id', how='inner')
    df_revenue_analysis['order_purchase_timestamp'] = pd.to_datetime(df_revenue_analysis['order_purchase_timestamp'])

    # Kamus terjemahan untuk nama kategori produk (Lengkap seperti di notebook)
    category_translation = {
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
        'construcao_ferramentas_seguranca': 'Construction Tools Security',
        'ferramentas_jardim': 'Garden Tools',
        'agro_industria_e_comercio': 'Agro Industry & Commerce',
        'industria_comercio_e_negocios': 'Industry, Commerce & Business',
        'fashion_calcados': 'Fashion Footwear',
        'bebidas': 'Drinks',
        'papelaria': 'Stationery',
        'livros_interesses_gerais': 'Books General Interest',
        'fashion_underwear_e_moda_praia': 'Fashion Underwear & Beachwear',
        'perfumaria': 'Perfumery',
        'construcao_ferramentas_construcao': 'Construction Tools',
        'pet_shop': 'Pet Shop',
        'malas_acessorios': 'Luggage & Accessories',
        'portateis_casa_forno_e_cafe': 'Portable Home Oven & Coffee',
        'fashion_roupa_masculina': 'Men Fashion Clothes',
        'telefonia_fixa': 'Landline Telephony',
        'flores': 'Flowers',
        'casa_conforto': 'Home Comfort',
        'artes': 'Arts',
        'artigos_de_festas': 'Party Supplies',
        'pcs': 'PCs',
        'la_cuisine': 'La Cuisine',
        'artigos_de_natal': 'Christmas Articles',
        'eletroportateis': 'Small Appliances',
        'sinalizacao_e_seguranca': 'Signaling & Security',
        'livros_tecnicos': 'Technical Books',
        'livros_importados': 'Imported Books',
        'fashion_esporte': 'Fashion Sport',
        'fashion_roupa_feminina': 'Women Fashion Clothes',
        'construcao_ferramentas_iluminacao': 'Construction Tools Lighting',
        'moveis_cozinha_area_de_servico_jantar_e_jardim': 'Kitchen, Laundry, Dining & Garden Furniture',
        'dvds_blu_ray': 'DVDs & Blu-Ray',
        'musica': 'Music',
        'consoles': 'Consoles',
        'portateis_cozinha_e_preparadores_de_alimentos': 'Portable Kitchen & Food Processors',
        'tablets_impressao_imagem': 'Tablets, Printing & Image',
        'fraldas_higiene': 'Diapers & Hygiene',
        'fashion_underwear_e_lingerie': 'Fashion Underwear & Lingerie',
        'fashion_roupa_infanto_juvenil': 'Kids & Junior Fashion Clothes',
        'seguros_e_servicos': 'Insurance & Services',
        'moveis_quarto': 'Bedroom Furniture',
        'construcao_ferramentas_ferramentas': 'Construction Tools',
        'fashion_sport': 'Fashion Sport',
        'cds_dvds_musicais': 'CDs & DVDs Musical',
        'moveis_sala': 'Living Room Furniture',
        'audio': 'Audio',
        'alimentos': 'Food',
        'artigos_de_natal': 'Christmas Articles',
        'pc_gamer': 'PC Gamer',
        'casa_conforto_2': 'Home Comfort 2',
        'dvds_filmes': 'DVDs Movies',
        'moveis_escritorio': 'Office Furniture',
        'fraldas': 'Diapers',
        'livros_generais': 'General Books'
    }
    df_revenue_analysis['product_category_name_english'] = df_revenue_analysis['product_category_name'].map(category_translation).fillna(df_revenue_analysis['product_category_name'])

    # =========================
    # 📊 1. REVENUE ANALYSIS
    # =========================
    st.header('1. Analisis Revenue Produk')
    st.subheader('Top 10 Kategori Produk Berdasarkan Revenue')
    category_revenue = df_revenue_analysis.groupby('product_category_name_english')['price'].sum().reset_index()
    category_revenue.rename(columns={'price': 'total_revenue', 'product_category_name_english': 'product_category_name'}, inplace=True)
    category_revenue = category_revenue.sort_values(by='total_revenue', ascending=False)

    fig1, ax1 = plt.subplots(figsize=(12, 7))
    sns.barplot(x='total_revenue', y='product_category_name', data=category_revenue.head(10), palette='viridis', hue='product_category_name', legend=False, ax=ax1)
    ax1.set_title('Top 10 Product Categories by Revenue')
    ax1.set_xlabel('Total Revenue')
    ax1.set_ylabel('Product Category')
    plt.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1) # Tutup figure untuk menghemat memori

    st.subheader('Kontribusi Persentase Kategori Produk Terhadap Total Revenue (Top 5 + Lainnya)')
    top_5_categories = category_revenue.head(5)
    other_revenue = category_revenue['total_revenue'].iloc[5:].sum()
    total_overall_sales = category_revenue['total_revenue'].sum()
    other_percentage = (other_revenue / total_overall_sales) * 100

    pie_data = top_5_categories.copy()
    if not category_revenue.shape[0] <= 5:
        pie_data = pd.concat([
            pie_data,
            pd.DataFrame([{'product_category_name': 'Others', 'total_revenue': other_revenue, 'contribution_percentage': other_percentage}])
        ], ignore_index=True)

    fig2, ax2 = plt.subplots(figsize=(10, 10))
    ax2.pie(pie_data['total_revenue'], labels=pie_data['product_category_name'], autopct='%1.1f%%', startangle=140, pctdistance=0.85)
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig2.gca().add_artist(centre_circle)
    ax2.set_title('Percentage Contribution of Product Categories to Total Revenue (Top 5 + Others)')
    ax2.axis('equal')
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

    # =========================
    # 📊 2. RFM ANALYSIS
    # =========================
    st.header('2. Segmentasi Pelanggan Berdasarkan RFM')

    # Gabungkan data untuk analisis RFM (mirip dengan notebook)
    customers_orders_items_df = pd.merge(
        orders.rename(columns={'customer_id': 'customer_id_orders'}),
        order_items,
        on='order_id',
        how='inner'
    )

    customers_orders_items_df = pd.merge(
        customers,
        customers_orders_items_df,
        left_on='customer_id',
        right_on='customer_id_orders',
        how='inner'
    )

    customers_orders_items_df['order_purchase_timestamp'] = pd.to_datetime(customers_orders_items_df['order_purchase_timestamp'])

    snapshot_date = customers_orders_items_df['order_purchase_timestamp'].max() + dt.timedelta(days=1)
    last_12_months_start = snapshot_date - dt.timedelta(days=365)
    df_12_months = customers_orders_items_df[customers_orders_items_df['order_purchase_timestamp'] >= last_12_months_start]

    rfm_df = df_12_months.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': lambda date: (snapshot_date - date.max()).days,
        'order_id': 'nunique',
        'price': 'sum'
    })

    rfm_df.rename(columns={'order_purchase_timestamp': 'Recency',
                           'order_id': 'Frequency',
                           'price': 'Monetary'},
                  inplace=True)

    # Menentukan RFM Score (menggunakan 5 kuantil, dengan penanganan duplikat)
    rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], 5, labels=False, duplicates='drop')
    max_r_score_idx = rfm_df['R_Score'].max()
    rfm_df['R_Score'] = max_r_score_idx - rfm_df['R_Score'] + 1

    rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'], 5, labels=False, duplicates='drop') + 1
    rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'], 5, labels=False, duplicates='drop') + 1

    rfm_df['RFM_Segment'] = rfm_df['R_Score'].astype(str) + rfm_df['F_Score'].astype(str) + rfm_df['M_Score'].astype(str)
    rfm_df['RFM_Score'] = rfm_df[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

    # Contoh definisi segmen berdasarkan skor (seperti di notebook):
    def rfm_level(df):
        if df['R_Score'] == 5 and df['F_Score'] == 5 and df['M_Score'] == 5:
            return 'Champions'
        elif df['R_Score'] == 5 and df['F_Score'] == 5:
            return 'Loyal Customers'
        elif df['R_Score'] == 5 and df['M_Score'] == 5:
            return 'Big Spenders'
        elif df['R_Score'] == 5 and df['F_Score'] == 1:
            return 'New Customers'
        elif df['R_Score'] == 1 and df['F_Score'] == 1 and df['M_Score'] == 1:
            return 'Lost Customers'
        else:
            return 'Others'

    rfm_df['Customer_Segment'] = rfm_df.apply(rfm_level, axis=1)

    st.subheader('Distribusi RFM Score Pelanggan (12 Bulan Terakhir)')
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.histplot(rfm_df['RFM_Score'], bins=15, kde=True, ax=ax3)
    ax3.set_title('Distribusi RFM Score Pelanggan (12 Bulan Terakhir)')
    ax3.set_xlabel('RFM Score')
    ax3.set_ylabel('Jumlah Pelanggan')
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

    st.subheader('Top 10 Segmen RFM Berdasarkan Jumlah Pelanggan')
    rfm_segment_counts = rfm_df['RFM_Segment'].value_counts().head(10)
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    sns.barplot(x=rfm_segment_counts.index, y=rfm_segment_counts.values, palette='coolwarm', hue=rfm_segment_counts.index, legend=False, ax=ax4)
    ax4.set_title('Top 10 Segmen RFM Berdasarkan Jumlah Pelanggan')
    ax4.set_xlabel('RFM Segment')
    ax4.set_ylabel('Jumlah Pelanggan')
    ax4.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)

    st.subheader('Distribusi Segmen Pelanggan RFM Kustom')
    fig5, ax5 = plt.subplots(figsize=(10, 7))
    sns.countplot(y='Customer_Segment', data=rfm_df, order=rfm_df['Customer_Segment'].value_counts().index, palette='viridis', hue='Customer_Segment', legend=False, ax=ax5)
    ax5.set_title('Distribusi Segmen Pelanggan RFM Kustom')
    ax5.set_xlabel('Jumlah Pelanggan')
    ax5.set_ylabel('Segmen Pelanggan')
    plt.tight_layout()
    st.pyplot(fig5)
    plt.close(fig5)

    # =========================
    # 📊 3. Geographical Analysis for Big Spenders
    # =========================
    st.header('3. Analisis Geografis Pelanggan "Big Spenders"')

    rfm_geo_df = pd.merge(
        rfm_df,
        customers[['customer_unique_id', 'customer_city', 'customer_state']],
        on='customer_unique_id',
        how='left'
    )

    # Filter 'Big Spenders' berdasarkan definisi dari notebook
    big_spenders = rfm_geo_df[rfm_geo_df['Customer_Segment'] == 'Big Spenders']

    st.subheader('Top 10 Kota Pelanggan Big Spenders')
    fig6, ax6 = plt.subplots(figsize=(12, 7))
    sns.barplot(
        x=big_spenders['customer_city'].value_counts().head(10).index,
        y=big_spenders['customer_city'].value_counts().head(10).values,
        palette='magma',
        hue=big_spenders['customer_city'].value_counts().head(10).index,
        legend=False,
        ax=ax6
    )
    ax6.set_title('Top 10 Kota Pelanggan Big Spenders')
    ax6.set_xlabel('Kota')
    ax6.set_ylabel('Jumlah Pelanggan Big Spenders')
    ax6.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig6)
    plt.close(fig6)

    st.subheader('Top 10 Negara Bagian Pelanggan Big Spenders')
    fig7, ax7 = plt.subplots(figsize=(10, 6))
    sns.barplot(
        x=big_spenders['customer_state'].value_counts().head(10).index,
        y=big_spenders['customer_state'].value_counts().head(10).values,
        palette='viridis',
        hue=big_spenders['customer_state'].value_counts().head(10).index,
        legend=False,
        ax=ax7
    )
    ax7.set_title('Top 10 Negara Bagian Pelanggan Big Spenders')
    ax7.set_xlabel('Negara Bagian')
    ax7.set_ylabel('Jumlah Pelanggan Big Spenders')
    ax7.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig7)
    plt.close(fig7)

except FileNotFoundError:
    st.error("Beberapa file data tidak ditemukan. Pastikan 'orders_dataset.csv', 'order_items_dataset.csv', 'products_dataset.csv', dan 'customers_dataset.csv' ada di direktori yang sama dengan `app.py`.")
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat atau memproses data: {e}")
