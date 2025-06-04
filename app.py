import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulasi Pajak UMKM", layout="centered")

st.title("💰 Simulasi Pajak 0.5% UMKM & Freelancer")
st.markdown("Simulasikan berapa pajak final yang harus kamu bayarkan berdasarkan omzet per bulan sepanjang tahun.")

@st.cache_data
def load_data():
    df = pd.read_csv("omzet_umkm.csv")
    # Pastikan omzet bulanan berupa numeric
    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

df = load_data()
nama_list = df["Nama"].tolist()

selected_nama = st.selectbox("Pilih Nama UMKM / Freelancer:", nama_list)

row = df[df["Nama"] == selected_nama].iloc[0, 1:]
omzet_bulanan = row.values
bulan = row.index.tolist()

# (Optional) urutkan bulan jika kolom bukan urut alami
# urutan_bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
# df.columns = pd.CategoricalIndex(df.columns, categories=urutan_bulan, ordered=True)

pajak_bulanan = omzet_bulanan * 0.005
total_omzet = omzet_bulanan.sum()
total_pajak = pajak_bulanan.sum()

st.subheader(f"📊 Ringkasan untuk {selected_nama}")
st.write(f"Total Omzet Tahunan: **Rp {total_omzet:,.0f}**")
st.write(f"Total Pajak (0.5%): **Rp {total_pajak:,.0f}**")

grafik_df = pd.DataFrame({
    "Bulan": bulan,
    "Omzet": omzet_bulanan,
    "Pajak (0.5%)": pajak_bulanan
})

fig, ax1 = plt.subplots(figsize=(10, 5))

color_omzet = "tab:blue"
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Omzet (Rp)", color=color_omzet)
ax1.bar(grafik_df["Bulan"], grafik_df["Omzet"], color=color_omzet, label="Omzet")
ax1.tick_params(axis='y', labelcolor=color_omzet)

ax2 = ax1.twinx()
color_pajak = "tab:orange"
ax2.plot(grafik_df["Bulan"], grafik_df["Pajak (0.5%)"], color=color_pajak, marker="o", label="Pajak (0.5%)")
ax2.set_ylabel("Pajak (Rp)", color=color_pajak)
ax2.tick_params(axis='y', labelcolor=color_pajak)

fig.tight_layout()
st.pyplot(fig)

st.caption("Data ini adalah simulasi dan bukan data pajak sebenarnya.")