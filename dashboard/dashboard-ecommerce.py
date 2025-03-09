import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

@st.cache_data
def load_data():
    # df = pd.read_csv("D:/dicoding/dataset e-commerce.csv")
    df = pd.read_csv("dataset e-commerce.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_purchase_month'] = df['order_purchase_timestamp'].dt.to_period('M')
    return df
df = load_data()

def cre_top_products(df):
    top_products = (
        df.groupby('product_category_name_english')
        .agg(total_sold=('order_id', 'size'), avg_price=('price', 'mean'))
        .sort_values(by='total_sold', ascending=False)
        .reset_index()
    )
    return top_products

def classify_review(score):
    if score in [1, 2]:
        return 'Tidak Puas'
    elif score == 3:
        return 'Netral'
    else:
        return 'Puas'

top_products = cre_top_products(df)
categories = top_products['product_category_name_english'].tolist()
df['satisfaction_category'] = df['review_score'].apply(classify_review)
satisfaction_distribution = df['satisfaction_category'].value_counts(normalize=True) * 100
review_avg = df.groupby('product_category_name_english')['review_score'].mean().sort_values()

# Layout Dashboard
st.title("📊 Proyek Analisis E-Commerce")
st.markdown("Dashboard ini menampilkan **analisis kategori produk terlaris, tren penjualan, kategori produk dengan nilai ulasan tertinggi dan terendah, dan tingkat kepuasan pelanggan**")


st.subheader("🏆 Kategori Produk Terlaris")
num_products = st.slider("Pilih jumlah kategori produk untuk ditampilkan", min_value=3, max_value=15, value=10, step=1)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(
    x="total_sold", 
    y="product_category_name_english", 
    data=top_products.head(num_products), 
    palette="Blues_r", 
    ax=ax
)
ax.set_title(f"Top {num_products} Kategori Produk Terlaris", fontsize=14, fontweight="bold")
ax.set_xlabel("Total Terjual")
ax.set_ylabel("Kategori Produk")
ax.grid(axis="x", linestyle="--", alpha=0.7)
st.pyplot(fig)


st.subheader("📈 Rekap Penjualan Kategori Produk")
selected_category = st.selectbox('Pilih Kategori Produk', categories)

trend = df[df['product_category_name_english'] == selected_category] \
    .groupby('order_purchase_month')['order_id'].size()

fig, ax = plt.subplots(figsize=(10, 5))
trend.plot(marker='o', ax=ax, color='tab:blue')
ax.set_title(f'Penjualan Bulanan: {selected_category}', fontsize=14, fontweight="bold")
ax.set_ylabel('Total Penjualan')
ax.set_xlabel('Bulan')
ax.grid(True)
st.pyplot(fig)

st.subheader("💬 Analisis Ulasan Produk")
st.markdown("Berikut adalah **Top 10 Produk dengan Rata-rata Nilai Ulasan Tertinggi & Terendah**")

top_n = 10
top_best = review_avg.sort_values(ascending=False).head(top_n)
top_worst = review_avg.sort_values(ascending=True).head(top_n)

st.markdown(f"**{top_n} Produk dengan Nilai Ulasan Tertinggi**")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=top_best.values, y=top_best.index, palette="Greens_r", ax=ax)
ax.set_xlabel("Rata-rata Review Score")
ax.set_ylabel(None)
ax.set_xlim(0, 5)
ax.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(fig)

st.markdown(f"**{top_n} Produk dengan Nilai Ulasan Terendah**")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=top_worst.values, y=top_worst.index, palette="Reds_r", ax=ax)
ax.set_xlabel("Rata-rata Review Score")
ax.set_ylabel(None)
ax.set_xlim(0, 5)
ax.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(fig)


st.subheader("😊 Tingkat Kepuasan Pelanggan")
st.markdown("Berikut adalah distribusi kepuasan pelanggan berdasarkan ulasan pelanggan")

fig, ax = plt.subplots(figsize=(4, 4))  
colors = ["#2E86C1", "#C0392B", "#F39C12"] 

wedges, texts, autotexts = ax.pie(
    satisfaction_distribution.values, 
    labels=satisfaction_distribution.index, 
    autopct='%1.1f%%', 
    startangle=90, 
    colors=colors, 
    wedgeprops={'edgecolor': 'black'},  
    textprops={'fontsize': 8}  
)

for autotext in autotexts:
    autotext.set_color('white')  
    autotext.set_fontsize(8) 

ax.set_title('Kepuasan Pelanggan', fontsize=10, fontweight="bold")
st.pyplot(fig)


st.markdown("### 📌 Insight dari Analisis")
st.markdown("""
- Produk dengan **penjualan tertinggi** umumnya memiliki daya tarik lebih besar bagi pelanggan.
- Tren penjualan produk tertentu bisa mengalami **fluktuasi** pada periode tertentu.
- **Kategori produk dengan ulasan tertinggi** bisa dijadikan referensi untuk strategi pemasaran.
- **Kategori produk dengan ulasan terendah** bisa  evaluasi kembail agar pelanggan bisa mendapatkan pengalaman belanja yang lebih baik.
- **Distribusi kepuasan pelanggan** memberikan gambaran tentang tingkat kepercayaan konsumen terhadap layanan.
""")
