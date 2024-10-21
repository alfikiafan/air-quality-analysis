import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from tqdm import tqdm

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    data_dir = Path('..\data')
    
    if not data_dir.exists():
        raise FileNotFoundError(f"Direktori {data_dir} tidak ditemukan. Pastikan path benar.")
    
    csv_files = list(data_dir.glob('*.csv'))
    
    if not csv_files:
        raise FileNotFoundError(f"Tidak ada file CSV ditemukan di direktori {data_dir}.")
    
    df_list = []

    for file in tqdm(csv_files, desc="Membaca file CSV"):
        try:
            df = pd.read_csv(file)
            df['DateTime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']], errors='coerce').dt.floor('s')
            df_list.append(df)
        except Exception as e:
            st.write(f"Gagal membaca {file.name}: {e}")
    
    if df_list:
        combined_df = pd.concat(df_list, ignore_index=True)
    else:
        raise ValueError("Tidak ada data yang berhasil dibaca.")
    
    numerical_cols = combined_df.select_dtypes(include=['int64', 'float64']).columns.tolist()

    combined_df[numerical_cols] = combined_df[numerical_cols].fillna(combined_df[numerical_cols].median())

    categorical_cols = combined_df.select_dtypes(include=['object']).columns.tolist()

    for column in categorical_cols:
        mode_value = combined_df[column].mode()[0]
        combined_df[column] = combined_df[column].fillna(mode_value)

    def remove_outliers(df, column):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

    cols_to_check = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']

    for col in cols_to_check:
        combined_df = remove_outliers(combined_df, col)
        
    return combined_df

# Load the data
combined_df = load_data()

# Mendefinisikan tiga tahun terakhir data global
end_date = combined_df['DateTime'].max()
start_date = end_date - pd.DateOffset(years=3)
three_year_df = combined_df[(combined_df['DateTime'] >= start_date) & (combined_df['DateTime'] <= end_date)].copy()

# Sidebar untuk navigasi
# st.sidebar.image("../images/logo.png")
st.sidebar.title("Menu Navigasi")
menu = st.sidebar.selectbox("Pilih Menu:", ["Home", "Lihat Dataset", "Pertanyaan Satu", "Pertanyaan Dua", "Pertanyaan Tiga", "Binning", "Kesimpulan"])

# Halaman Home
if menu == "Home":
    st.title("Proyek Analisis Data: Air Quality Dataset")
    st.markdown("""
    **Pertanyaan Bisnis:** \n
    1. Bagaimana pengaruh kecepatan angin (WSPM) terhadap penyebaran konsentrasi PM2.5 selama musim panas (Juni hingga Agustus) di masing-masing stasiun pengukuran?
    2. Bagaimana konsentrasi NO2 dan CO mempengaruhi kualitas udara secara keseluruhan di stasiun-stasiun urban selama tiga tahun terakhir?
    3. Bagaimana pengaruh suhu (TEMP) dan kelembaban udara (DEWP) terhadap konsentrasi PM10 dan SO2 di berbagai stasiun pengukuran selama lima tahun terakhir?
    """)
    st.subheader("Deskripsi Data")
    st.write(combined_df.describe())
    st.subheader("Dataframe")
    st.dataframe(combined_df.head())

# Halaman Lihat Dataset
elif menu == "Lihat Dataset":
    st.title("Lihat Dataset")
    st.dataframe(combined_df.head())

# Pertanyaan Satu: Pengaruh kecepatan angin (WSPM) terhadap PM2.5
elif menu == "Pertanyaan Satu":
    st.title("Pengaruh Kecepatan Angin terhadap Konsentrasi PM2.5 selama Musim Panas")
    
    # Filter data untuk musim panas (Juni, Juli, Agustus)
    summer_df = combined_df[combined_df['DateTime'].dt.month.isin([6, 7, 8])]
    
    # Scatter plot WSPM vs PM2.5
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=summer_df, x='WSPM', y='PM2.5', hue='station', alpha=0.5)
    plt.title('Pengaruh Kecepatan Angin (WSPM) terhadap Konsentrasi PM2.5 selama Musim Panas')
    plt.xlabel('Kecepatan Angin (WSPM) [m/s]')
    plt.ylabel('Konsentrasi PM2.5 [µg/m³]')
    plt.legend(title='Stasiun')
    st.pyplot(plt)

    # Korelasi WSPM dengan PM2.5
    corr = summer_df[['WSPM', 'PM2.5']].corr()
    st.write("Korelasi antara WSPM dan PM2.5:", corr)
    plt.figure(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Korelasi antara WSPM dan PM2.5')
    st.pyplot(plt)

    # Penjelasan
    st.markdown("""**1. Pengaruh Kecepatan Angin (WSPM) terhadap Konsentrasi PM2.5:**  
- Pada kecepatan angin rendah (< 1 m/s), terlihat bahwa konsentrasi PM2.5 cenderung lebih tinggi di hampir semua stasiun pengukuran. Hal ini menunjukkan bahwa ketika angin lemah, partikel PM2.5 cenderung terakumulasi di atmosfer.
- Pada kecepatan angin yang lebih tinggi (> 3 m/s), konsentrasi PM2.5 cenderung sedikit menurun, namun tidak signifikan. Ini menunjukkan bahwa peningkatan kecepatan angin dapat sedikit membantu penyebaran polutan, tetapi pengaruhnya tidak terlalu besar.
- Heatmap korelasi menunjukkan bahwa korelasi antara kecepatan angin (WSPM) dan konsentrasi PM2.5 adalah -0.14, yang merupakan korelasi negatif lemah.
    """)

# Pertanyaan Dua: Pengaruh NO2 dan CO terhadap kualitas udara
elif menu == "Pertanyaan Dua":
    st.title("Pengaruh Konsentrasi NO2 dan CO terhadap Kualitas Udara di Stasiun Urban")

    # Filter data untuk tiga tahun terakhir
    end_date = combined_df['DateTime'].max()
    start_date = end_date - pd.DateOffset(years=3)
    three_year_df = combined_df[(combined_df['DateTime'] >= start_date) & (combined_df['DateTime'] <= end_date)].copy()

    # Membuat kolom AQI sederhana berdasarkan PM2.5 dan PM10
    three_year_df['AQI'] = three_year_df[['PM2.5', 'PM10']].max(axis=1)

    # Scatter Plot: NO2 vs AQI
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=three_year_df, x='NO2', y='AQI', hue='station', alpha=0.6)
    plt.title('Pengaruh NO2 terhadap AQI selama Tiga Tahun Terakhir')
    plt.xlabel('Konsentrasi NO2 [µg/m³]')
    plt.ylabel('Indeks Kualitas Udara (AQI)')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

    # Scatter Plot: CO vs AQI
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=three_year_df, x='CO', y='AQI', hue='station', alpha=0.6)
    plt.title('Pengaruh CO terhadap AQI selama Tiga Tahun Terakhir')
    plt.xlabel('Konsentrasi CO [µg/m³]')
    plt.ylabel('Indeks Kualitas Udara (AQI)')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

    # Heatmap Korelasi antara NO2, CO, dan AQI
    plt.figure(figsize=(6, 4))
    corr = three_year_df[['NO2', 'CO', 'AQI']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Korelasi antara NO2, CO, dan AQI')
    plt.tight_layout()
    st.pyplot(plt)

    # Penjelasan
    st.markdown("""**2. Pengaruh Konsentrasi NO2 dan CO terhadap Kualitas Udara di Stasiun Urban:**
- Pada konsentrasi NO2 lebih dari 40 µg/m³, kualitas udara secara umum sangat buruk (AQI di atas 150). Ini menunjukkan bahwa NO2 adalah salah satu faktor utama yang memengaruhi kualitas udara.
- Hampir semua stasiun memiliki pola serupa, tetapi Wanshouxigong terlihat memiliki konsentrasi NO2 dan AQI yang tinggi.
- Pada konsentrasi CO di atas 1000 µg/m³, AQI hampir selalu berada di atas 150, menunjukkan kondisi kualitas udara yang tidak sehat. Dengan meningkatnya konsentrasi CO, kualitas udara semakin buruk.
- Beberapa stasiun seperti Wanshouxigong juga mendominasi dengan konsentrasi CO yang tinggi dan kualitas udara yang buruk.
- Korelasi antara NO2 dan AQI adalah 0.52, yang menunjukkan hubungan positif moderat. Ini berarti bahwa peningkatan NO2 secara konsisten berkorelasi dengan penurunan kualitas udara (AQI meningkat).
- Korelasi antara CO dan AQI adalah 0.61, yang lebih kuat dibandingkan NO2. Ini menunjukkan bahwa CO memiliki pengaruh yang lebih besar terhadap penurunan kualitas udara.
- Korelasi antara NO2 dan CO adalah 0.60, menunjukkan bahwa kedua polutan ini cenderung muncul bersama dalam tingkat yang tinggi.
    """)

# Pertanyaan Tiga: Pengaruh suhu (TEMP) dan kelembaban udara (DEWP) terhadap PM10 dan SO2
elif menu == "Pertanyaan Tiga":
    st.title("Pengaruh Suhu dan Kelembaban Udara terhadap Konsentrasi PM10 dan SO2")

    # Filter data untuk lima tahun terakhir
    start_date_5yr = end_date - pd.DateOffset(years=5)
    five_year_df = combined_df[(combined_df['DateTime'] >= start_date_5yr) & (combined_df['DateTime'] <= end_date)]

    # Scatter Plot: TEMP vs PM10
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=five_year_df, x='TEMP', y='PM10', hue='station', alpha=0.6)
    plt.title('Pengaruh Suhu (TEMP) terhadap Konsentrasi PM10')
    plt.xlabel('Suhu (TEMP) [°C]')
    plt.ylabel('Konsentrasi PM10 [µg/m³]')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

    # Scatter Plot: DEWP vs SO2
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=five_year_df, x='DEWP', y='SO2', hue='station', alpha=0.6)
    plt.title('Pengaruh Kelembaban Udara (DEWP) terhadap Konsentrasi SO2')
    plt.xlabel('Kelembaban Udara (DEWP) [°C]')
    plt.ylabel('Konsentrasi SO2 [µg/m³]')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

    # Heatmap Korelasi antara TEMP, DEWP, PM10, dan SO2
    plt.figure(figsize=(6, 5))
    corr = five_year_df[['TEMP', 'DEWP', 'PM10', 'SO2']].corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Korelasi antara TEMP, DEWP, PM10, dan SO2')
    plt.tight_layout()
    st.pyplot(plt)

    # Penjelasan
    st.markdown("""**3. Pengaruh Suhu (TEMP) dan Kelembaban Udara (DEWP) terhadap Konsentrasi PM10 dan SO2:**
- Pada suhu di atas 20°C, banyak stasiun menunjukkan konsentrasi PM10 yang lebih tinggi, terutama di Wanshouxigong. Kemungkinan suhu tinggi membantu mengangkat dan menyebarkan partikel debu, atau bisa juga disebabkan oleh peningkatan aktivitas manusia pada suhu yang lebih tinggi.
- Scatter plot menunjukkan bahwa peningkatan kelembaban udara (DEWP) cenderung berhubungan dengan penurunan konsentrasi SO2.
- Pada kelembaban tinggi (DEWP di atas 0°C), konsentrasi SO2 cenderung lebih rendah, menunjukkan bahwa kelembaban mungkin membantu menghilangkan gas SO2 dari atmosfer. Hal ini dapat diakibatkan oleh interaksi gas dengan uap air atau proses pembentukan asam sulfat.
- Korelasi positif sebesar 0.16 menunjukkan bahwa peningkatan suhu memiliki pengaruh kecil namun tetap signifikan terhadap peningkatan konsentrasi PM10.
- Korelasi negatif sebesar -0.28 menunjukkan bahwa ketika kelembaban udara meningkat, konsentrasi SO2 cenderung menurun, yang konsisten dengan scatter plot yang menunjukkan pengurangan SO2 pada kelembaban tinggi.
    """)

# Halaman Binning
elif menu == "Binning":
    st.title("Analisis Clustering Lanjutan - Binning")

    # Buat binning untuk NO2
    def classify_no2(no2_value):
        if no2_value < 40:
            return 'Rendah'
        elif no2_value <= 80:
            return 'Sedang'
        else:
            return 'Tinggi'

    # Buat binning untuk CO
    def classify_co(co_value):
        if co_value < 1000:
            return 'Rendah'
        elif co_value <= 2000:
            return 'Sedang'
        else:
            return 'Tinggi'

    # Buat binning untuk Suhu (TEMP)
    def classify_temp(temp_value):
        if temp_value < 0:
            return 'Dingin'
        elif temp_value <= 20:
            return 'Sedang'
        else:
            return 'Panas'

    # Buat binning untuk Kelembaban (DEWP)
    def classify_dewp(dewp_value):
        if dewp_value < 0:
            return 'Kelembaban Rendah'
        elif dewp_value <= 10:
            return 'Kelembaban Sedang'
        else:
            return 'Kelembaban Tinggi'

    # Terapkan binning ke dataset
    three_year_df['NO2_Category'] = three_year_df['NO2'].apply(classify_no2)
    three_year_df['CO_Category'] = three_year_df['CO'].apply(classify_co)
    three_year_df['TEMP_Category'] = three_year_df['TEMP'].apply(classify_temp)
    three_year_df['DEWP_Category'] = three_year_df['DEWP'].apply(classify_dewp)

    # Lihat distribusi NO2, CO, TEMP, dan DEWP setelah binning
    print(three_year_df['NO2_Category'].value_counts())
    print(three_year_df['CO_Category'].value_counts())
    print(three_year_df['TEMP_Category'].value_counts())
    print(three_year_df['DEWP_Category'].value_counts())

    # Visualisasi hasil binning
    plt.figure(figsize=(10,6))
    sns.countplot(data=three_year_df, x='NO2_Category', order=['Rendah', 'Sedang', 'Tinggi'])
    plt.title('Distribusi Data Berdasarkan Kategori NO2')
    plt.xlabel('Kategori NO2')
    plt.ylabel('Jumlah Data')
    plt.tight_layout()
    st.pyplot(plt)

    plt.figure(figsize=(10,6))
    sns.countplot(data=three_year_df, x='CO_Category', order=['Rendah', 'Sedang', 'Tinggi'])
    plt.title('Distribusi Data Berdasarkan Kategori CO')
    plt.xlabel('Kategori CO')
    plt.ylabel('Jumlah Data')
    plt.tight_layout()
    st.pyplot(plt)

    plt.figure(figsize=(10,6))
    sns.countplot(data=three_year_df, x='TEMP_Category', order=['Dingin', 'Sedang', 'Panas'])
    plt.title('Distribusi Data Berdasarkan Kategori Suhu')
    plt.xlabel('Kategori Suhu')
    plt.ylabel('Jumlah Data')
    plt.tight_layout()
    st.pyplot(plt)

    plt.figure(figsize=(10,6))
    sns.countplot(data=three_year_df, x='DEWP_Category', order=['Kelembaban Rendah', 'Kelembaban Sedang', 'Kelembaban Tinggi'])
    plt.title('Distribusi Data Berdasarkan Kategori Kelembaban Udara')
    plt.xlabel('Kategori Kelembaban Udara')
    plt.ylabel('Jumlah Data')
    plt.tight_layout()
    st.pyplot(plt)

    # Penjelasan
    st.markdown("""**4. Analisis Clustering Lanjutan - Binning:**
- Sebagian besar data menunjukkan bahwa konsentrasi NO2 berada di kategori rendah (<40 µg/m³), yang berarti mayoritas waktu, kualitas udara terkait NO2 berada pada level yang relatif aman. Namun, ada sekitar 20,069 data dengan konsentrasi NO2 yang tinggi (>80 µg/m³), yang mungkin mengindikasikan periode atau lokasi tertentu yang rentan terhadap peningkatan polusi NO2.
- Konsentrasi CO sebagian besar berada dalam kategori rendah (<1000 µg/m³), dengan hanya 3,625 data yang menunjukkan tingkat CO yang tinggi (>2000 µg/m³). Ini menunjukkan bahwa polusi CO jarang mencapai level yang membahayakan, dan kebanyakan waktu kualitas udara terkait CO cukup baik.
- Sebagian besar data menunjukkan kondisi suhu yang sedang (0-20°C), tetapi jumlah data untuk suhu panas (>20°C) juga signifikan. Ini menunjukkan bahwa data banyak diambil dari kondisi suhu yang cukup bervariasi, dan hampir sepertiga dari data menunjukkan suhu yang relatif panas, yang dapat berkontribusi terhadap peningkatan polusi seperti PM10. Suhu dingin (<0°C) relatif lebih jarang terjadi dalam dataset.
- Kelembaban udara menunjukkan distribusi yang cukup seimbang antara kelembaban rendah dan kelembaban tinggi, dengan lebih sedikit data untuk kelembaban sedang (0-10°C). Ini menunjukkan bahwa kondisi kelembaban udara cenderung berada di salah satu ekstrem (rendah atau tinggi), yang dapat berpengaruh pada konsentrasi polutan seperti SO2 yang cenderung berkurang pada kelembaban tinggi.
    """)

# Kesimpulan
elif menu == "Kesimpulan":
    st.title("Kesimpulan")
    st.markdown("""
1. Peningkatan kecepatan angin memang memiliki sedikit efek dalam mengurangi konsentrasi PM2.5, tetapi pengaruhnya sangat terbatas. Ada faktor lain yang mungkin lebih dominan dalam penyebaran polutan PM2.5.
2. Baik NO2 maupun CO memiliki pengaruh signifikan terhadap kualitas udara, dengan CO yang memiliki dampak sedikit lebih kuat. Keduanya berkorelasi positif dengan AQI, sehingga peningkatan konsentrasi kedua polutan ini akan berdampak negatif pada kualitas udara.
3. Suhu dan kelembaban memiliki pengaruh terhadap konsentrasi polutan. Suhu yang lebih tinggi cenderung meningkatkan konsentrasi PM10, sementara kelembaban yang lebih tinggi cenderung menurunkan konsentrasi SO2.
    """)
