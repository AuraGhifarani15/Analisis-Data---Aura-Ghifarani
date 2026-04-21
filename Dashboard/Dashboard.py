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

# --- Data Loading and Preprocessing ---
@st.cache_data
def load_data():
    # Use os.path.dirname and os.path.join to ensure path is correct regardless of execution context
    # This part is kept as per user's confirmation that it fixes FileNotFoundError
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, 'main_data.csv')

    df = pd.read_csv(file_path)
    
    # Convert date columns (assuming these are the relevant ones from the notebook)
    date_cols = [
        'order_purchase_timestamp', 'order_approved_at',
        'order_delivered_carrier_date', 'order_delivered_customer_date',
        'order_estimated_delivery_date', 'shipping_limit_date'
    ]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce') # Use errors='coerce' to handle any parsing issues gracefully
    
    # Fill numerical product NaNs (as done in notebook cleaning)
    numerical_product_cols = [
        'product_name_lenght', 'product_description_lenght', 'product_photos_qty',
        'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'
    ]
    for col in numerical_product_cols:
        df[col] = df[col].fillna(0)

    return df

@st.cache_data
def get_translated_product_categories():
    # This dictionary is directly copied from the notebook's cleaning section to be complete
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
        'livros_intereses_gerais': 'Books General Interest',
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
    return category_translation

# --- Load Data ---
main_data_df = load_data()
category_translation = get_translated_product_categories()

# Apply product category translation after loading
main_data_df['product_category_name'] = main_data_df['product_category_name'].map(category_translation).fillna('unknown')


# --- Functions for Analysis (copied and adapted from notebook) ---

@st.cache_data
def get_revenue_analysis(df, selected_year):
    df_revenue_analysis = df[df['order_purchase_timestamp'].dt.year == selected_year].copy()
    
    if df_revenue_analysis.empty:
        return pd.DataFrame(), pd.DataFrame(), "No data available for the selected year."

    category_revenue = df_revenue_analysis.groupby('product_category_name')['price'].sum().reset_index()
    category_revenue.rename(columns={'price': 'total_revenue'}, inplace=True)
    category_revenue = category_revenue.sort_values(by='total_revenue', ascending=False)
    
    total_overall_sales = category_revenue['total_revenue'].sum()
    category_revenue['contribution_percentage'] = (category_revenue['total_revenue'] / total_overall_sales) * 100
    
    # Prepare for donut chart (Top 5 + Others)
    top_5_categories = category_revenue.head(5)
    other_revenue = category_revenue['total_revenue'].iloc[5:].sum()
    other_percentage = category_revenue['contribution_percentage'].iloc[5:].sum()

    pie_data = top_5_categories.copy()
    if not category_revenue.shape[0] <= 5:
        pie_data = pd.concat([
            pie_data,
            pd.DataFrame([{'product_category_name': 'Others', 'total_revenue': other_revenue, 'contribution_percentage': other_percentage}])
        ], ignore_index=True)
    
    return category_revenue, pie_data, None

@st.cache_data
def get_rfm_analysis(df, snapshot_date_input):
    # Convert snapshot_date_input to datetime object, assuming it's a date object from st.date_input
    snapshot_date = dt.datetime(snapshot_date_input.year, snapshot_date_input.month, snapshot_date_input.day)

    df_rfm_prep = df.copy()

    # Ensure relevant columns are not null for RFM calculation
    df_rfm_prep = df_rfm_prep.dropna(subset=['customer_unique_id', 'order_purchase_timestamp', 'order_id', 'price'])

    # Filter for the last 12 months leading up to the snapshot_date
    last_12_months_start = snapshot_date - dt.timedelta(days=365)
    df_12_months = df_rfm_prep[(df_rfm_prep['order_purchase_timestamp'] >= last_12_months_start) & 
                                (df_rfm_prep['order_purchase_timestamp'] < snapshot_date)].copy() # Ensure purchases before snapshot_date

    if df_12_months.empty:
        return pd.DataFrame(), pd.DataFrame(), "No data available for RFM calculation in the selected period."

    rfm_df = df_12_months.groupby('customer_unique_id').agg(
        Recency=('order_purchase_timestamp', lambda date: (snapshot_date - date.max()).days),
        Frequency=('order_id', 'nunique'),
        Monetary=('price', 'sum')
    )
    
    rfm_df = rfm_df[rfm_df['Monetary'] > 0] # Exclude customers with 0 monetary value

    if rfm_df.empty:
        return pd.DataFrame(), pd.DataFrame(), "No customers with monetary value found in the selected period for RFM."

    # Ensure enough unique values for qcut
    # For Recency: higher value is worse, so invert score
    # Use try-except for qcut to handle cases with too few unique values for 5 quantiles
    try:
        rfm_df['R_Score'] = pd.qcut(rfm_df['Recency'], 5, labels=False, duplicates='drop')
        max_r_score_idx = rfm_df['R_Score'].max()
        rfm_df['R_Score'] = max_r_score_idx - rfm_df['R_Score'] + 1
    except ValueError:
        rfm_df['R_Score'] = 1 # Assign a default if qcut fails

    try:
        rfm_df['F_Score'] = pd.qcut(rfm_df['Frequency'], 5, labels=False, duplicates='drop') + 1
    except ValueError:
        rfm_df['F_Score'] = 1 # Assign a default if qcut fails

    try:
        rfm_df['M_Score'] = pd.qcut(rfm_df['Monetary'], 5, labels=False, duplicates='drop') + 1
    except ValueError:
        rfm_df['M_Score'] = 1 # Assign a default if qcut fails

    rfm_df['RFM_Segment'] = rfm_df['R_Score'].astype(str) + rfm_df['F_Score'].astype(str) + rfm_df['M_Score'].astype(str)
    rfm_df['RFM_Score'] = rfm_df[['R_Score', 'F_Score', 'M_Score']].sum(axis=1)

    def rfm_level(df_row):
        if df_row['R_Score'] == 5 and df_row['F_Score'] == 5 and df_row['M_Score'] == 5:
            return 'Champions'
        elif df_row['R_Score'] == 5 and df_row['F_Score'] == 5:
            return 'Loyal Customers'
        elif df_row['R_Score'] == 5 and df_row['M_Score'] == 5:
            return 'Big Spenders'
        elif df_row['R_Score'] == 5 and df_row['F_Score'] == 1:
            return 'New Customers'
        elif df_row['R_Score'] == 1 and df_row['F_Score'] == 1 and df_row['M_Score'] == 1:
            return 'Lost Customers'
        else:
            return 'Others'

    rfm_df['Customer_Segment'] = rfm_df.apply(rfm_level, axis=1)

    # Merge RFM with customer geographical data (using original df to get customer_city/state)
    # Ensure customer_unique_id in the original df is unique before merging for geographical info
    customer_geo_info = df[['customer_unique_id', 'customer_city', 'customer_state']].drop_duplicates(subset=['customer_unique_id'])

    rfm_geo_df = pd.merge(
        rfm_df,
        customer_geo_info,
        left_index=True, # rfm_df has customer_unique_id as index
        right_on='customer_unique_id',
        how='left'
    )
    
    return rfm_df, rfm_geo_df, None


# --- Sidebar Filters ---
st.sidebar.header("Filter Options")

# --- Revenue Analysis Filters ---
st.sidebar.subheader("Revenue Analysis (Pertanyaan 1)")
available_years = sorted(main_data_df['order_purchase_timestamp'].dt.year.dropna().unique().astype(int).tolist())
selected_year_revenue = st.sidebar.selectbox(
    "Pilih Tahun untuk Analisis Revenue", 
    options=available_years,
    index=available_years.index(2017) if 2017 in available_years else (len(available_years) - 1 if available_years else 0) # Default to 2017 or last year if 2017 not found, or 0 if empty
)
num_top_categories_revenue = st.sidebar.slider(
    "Jumlah Kategori Teratas (Revenue)", 
    min_value=1, max_value=len(main_data_df['product_category_name'].unique().dropna()), value=10
)

# --- RFM Analysis Filters ---
st.sidebar.subheader("RFM Segmentation (Pertanyaan 2)")
# Default RFM snapshot date to end of 2018 as per notebook
default_rfm_date = dt.date(2019, 1, 1)
selected_snapshot_date = st.sidebar.date_input(
    "Tanggal Snapshot Analisis RFM", 
    value=default_rfm_date
)


# --- Perform Analyses based on Filters ---
category_revenue, pie_data, revenue_error_msg = get_revenue_analysis(main_data_df, selected_year_revenue)
rfm_df, rfm_geo_df, rfm_error_msg = get_rfm_analysis(main_data_df, selected_snapshot_date)


# --- Main Content - Revenue Analysis ---
st.header("1. Kategori Produk dengan Revenue Terbesar")
st.markdown("Analisis ini menunjukkan kategori produk yang menghasilkan revenue terbesar untuk tahun yang dipilih, beserta kontribusi persentasenya terhadap total penjualan.")

if revenue_error_msg:
    st.warning(revenue_error_msg)
elif not category_revenue.empty:
    st.subheader(f"Top {num_top_categories_revenue} Kategori Produk berdasarkan Revenue ({selected_year_revenue})")
    st.dataframe(category_revenue.head(num_top_categories_revenue))

    col1_rev, col2_rev = st.columns(2)

    with col1_rev:
        fig_bar_rev, ax_bar_rev = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x='total_revenue', y='product_category_name', 
            data=category_revenue.head(num_top_categories_revenue), 
            palette='viridis', ax=ax_bar_rev
        )
        ax_bar_rev.set_title(f'Top {num_top_categories_revenue} Kategori Produk berdasarkan Revenue ({selected_year_revenue})')
        ax_bar_rev.set_xlabel('Total Revenue')
        ax_bar_rev.set_ylabel('Kategori Produk')
        st.pyplot(fig_bar_rev)

    with col2_rev:
        fig_pie_rev, ax_pie_rev = plt.subplots(figsize=(8, 8))
        ax_pie_rev.pie(
            pie_data['contribution_percentage'], 
            labels=pie_data['product_category_name'], 
            autopct='%1.1f%%', startangle=140, pctdistance=0.85
        )
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig_pie_rev.gca().add_artist(centre_circle)
        ax_pie_rev.set_title(f'Kontribusi Persentase Kategori Produk terhadap Total Revenue ({selected_year_revenue} - Top 5 + Lainnya)')
        ax_pie_rev.axis('equal') # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig_pie_rev)
else:
    st.info("Tidak ada data revenue untuk ditampilkan berdasarkan filter.")


# --- Main Content - RFM Segmentation ---
st.header("2. Segmentasi Pelanggan Berdasarkan RFM")
st.markdown(f"Segmentasi pelanggan menggunakan model RFM dalam 12 bulan terakhir sebelum tanggal snapshot **{selected_snapshot_date}**.")

if rfm_error_msg:
    st.warning(rfm_error_msg)
elif not rfm_df.empty:
    # RFM specific filters in sidebar
    st.sidebar.subheader("Filter Tampilan RFM")
    all_customer_segments = rfm_df['Customer_Segment'].unique().tolist()
    selected_customer_segments = st.sidebar.multiselect(
        "Pilih Segmen Pelanggan RFM",
        options=all_customer_segments,
        default=all_customer_segments # Select all by default
    )
    
    filtered_rfm_df = rfm_df[rfm_df['Customer_Segment'].isin(selected_customer_segments)]
    
    st.subheader("Distribusi RFM Scores")
    fig_hist_rfm, ax_hist_rfm = plt.subplots(figsize=(10, 6))
    sns.histplot(filtered_rfm_df['RFM_Score'], bins=15, kde=True, ax=ax_hist_rfm)
    ax_hist_rfm.set_title(f'Distribusi RFM Score Pelanggan (Snapshot {selected_snapshot_date})')
    ax_hist_rfm.set_xlabel('RFM Score')
    ax_hist_rfm.set_ylabel('Jumlah Pelanggan')
    st.pyplot(fig_hist_rfm)

    col1_rfm, col2_rfm = st.columns(2)

    with col1_rfm:
        st.subheader("Top 10 Segmen RFM Berdasarkan Jumlah Pelanggan")
        rfm_segment_counts = filtered_rfm_df['RFM_Segment'].value_counts().head(10)
        if not rfm_segment_counts.empty:
            fig_bar_segment, ax_bar_segment = plt.subplots(figsize=(12, 6))
            sns.barplot(x=rfm_segment_counts.index, y=rfm_segment_counts.values, palette='coolwarm', ax=ax_bar_segment)
            ax_bar_segment.set_title(f'Top 10 Segmen RFM Berdasarkan Jumlah Pelanggan (Snapshot {selected_snapshot_date})')
            ax_bar_segment.set_xlabel('Segmen RFM')
            ax_bar_segment.set_ylabel('Jumlah Pelanggan')
            ax_bar_segment.tick_params(axis='x', rotation=45)
            st.pyplot(fig_bar_segment)
        else:
            st.info("Tidak ada segmen RFM untuk ditampilkan.")

    with col2_rfm:
        st.subheader("Distribusi Segmen Pelanggan Kustom")
        customer_segment_counts = filtered_rfm_df['Customer_Segment'].value_counts()
        if not customer_segment_counts.empty:
            fig_bar_cust_segment, ax_bar_cust_segment = plt.subplots(figsize=(10, 7))
            sns.countplot(y='Customer_Segment', data=filtered_rfm_df, order=customer_segment_counts.index, palette='viridis', ax=ax_bar_cust_segment)
            ax_bar_cust_segment.set_title(f'Distribusi Segmen Pelanggan RFM Kustom (Snapshot {selected_snapshot_date})')
            ax_bar_cust_segment.set_xlabel('Jumlah Pelanggan')
            ax_bar_cust_segment.set_ylabel('Segmen Pelanggan')
            st.pyplot(fig_bar_cust_segment)
        else:
            st.info("Tidak ada segmen pelanggan kustom untuk ditampilkan.")
            
    st.subheader("Statistik RFM per Segmen Paling Bernilai")
    # Using the original rfm_df for stats to show overall valuable segments, not just filtered ones for plots
    valuable_segments_stats = rfm_df.groupby('RFM_Segment').agg(
        Recency_mean=('Recency', 'mean'),
        Frequency_mean=('Frequency', 'mean'),
        Monetary_mean=('Monetary', 'mean'),
        Customer_Count=('RFM_Segment', 'count')
    ).sort_values('Monetary_mean', ascending=False).head(10)
    st.dataframe(valuable_segments_stats)

else:
    st.info("Tidak ada data RFM untuk ditampilkan berdasarkan filter.")

# --- Main Content - Advanced Analysis (Big Spenders Geo) ---
st.header("3. Analisis Lanjutan: Geografi Pelanggan 'Big Spenders'")
st.markdown("Visualisasi ini menunjukkan distribusi geografis pelanggan dalam segmen 'Big Spenders' atau segmen yang dipilih.")

if rfm_error_msg: # Re-use RFM error check as rfm_geo_df depends on rfm_df
    st.warning(rfm_error_msg)
elif not rfm_geo_df.empty:
    st.sidebar.subheader("Filter Geografi Pelanggan")
    # Get unique customer segments for the selectbox, ensuring 'Big Spenders' is an option
    all_segments_for_geo = rfm_geo_df['Customer_Segment'].unique().tolist()
    
    # Ensure 'Big Spenders' is in the list of segments, otherwise default to first available
    default_geo_segment_index = 0
    if 'Big Spenders' in all_segments_for_geo:
        default_geo_segment_index = all_segments_for_geo.index('Big Spenders')
    elif all_segments_for_geo: # If 'Big Spenders' not present, default to the first available segment
        default_geo_segment_index = 0
    else:
        st.info("Tidak ada segmen pelanggan yang tersedia untuk analisis geografis.")
        st.stop() # Stop execution if no segments are available

    selected_geo_segment = st.sidebar.selectbox(
        "Pilih Segmen Pelanggan untuk Analisis Geografis",
        options=all_segments_for_geo,
        index=default_geo_segment_index
    )
    
    filtered_geo_segment_df = rfm_geo_df[rfm_geo_df['Customer_Segment'] == selected_geo_segment].copy()
    
    num_top_geo = st.sidebar.slider(
        f"Jumlah Top Kota/Negara Bagian untuk '{selected_geo_segment}'", 
        min_value=1, max_value=20, value=10
    )

    if not filtered_geo_segment_df.empty:
        col1_geo, col2_geo = st.columns(2)

        with col1_geo:
            st.subheader(f"Top {num_top_geo} Kota Pelanggan '{selected_geo_segment}'")
            city_counts = filtered_geo_segment_df['customer_city'].value_counts().head(num_top_geo)
            if not city_counts.empty:
                fig_city, ax_city = plt.subplots(figsize=(12, 7))
                sns.barplot(x=city_counts.index, y=city_counts.values, palette='magma', ax=ax_city)
                ax_city.set_title(f'Top {num_top_geo} Kota Pelanggan {selected_geo_segment}')
                ax_city.set_xlabel('Kota')
                ax_city.set_ylabel(f'Jumlah Pelanggan {selected_geo_segment}')
                plt.setp(ax_city.get_xticklabels(), rotation=45, ha='right')
                st.pyplot(fig_city)
            else:
                st.info(f"Tidak ada data kota untuk segmen '{selected_geo_segment}'.")


        with col2_geo:
            st.subheader(f"Top {num_top_geo} Negara Bagian Pelanggan '{selected_geo_segment}'")
            state_counts = filtered_geo_segment_df['customer_state'].value_counts().head(num_top_geo)
            if not state_counts.empty:
                fig_state, ax_state = plt.subplots(figsize=(10, 6))
                sns.barplot(x=state_counts.index, y=state_counts.values, palette='viridis', ax=ax_state)
                ax_state.set_title(f'Top {num_top_geo} Negara Bagian Pelanggan {selected_geo_segment}')
                ax_state.set_xlabel('Negara Bagian')
                ax_state.set_ylabel(f'Jumlah Pelanggan {selected_geo_segment}')
                plt.setp(ax_state.get_xticklabels(), rotation=45, ha='right')
                st.pyplot(fig_state)
            else:
                st.info(f"Tidak ada data negara bagian untuk segmen '{selected_geo_segment}'.")
    else:
        st.info(f"Tidak ada pelanggan dalam segmen '{selected_geo_segment}' untuk ditampilkan.")
else:
    st.info("Tidak ada data RFM geografis untuk ditampilkan berdasarkan filter.")