
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulasi Pajak UMKM", layout="centered")

st.title("💰 Simulasi Pajak 0.5% UMKM & Freelancer")
st.markdown("Simulasikan berapa pajak final yang harus kamu bayarkan berdasarkan omzet per bulan sepanjang tahun.")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("omzet_umkm.csv")
    return df

df = load_data()
nama_list = df["Nama"].tolist()

# Pilih nama
selected_nama = st.selectbox("Pilih Nama UMKM / Freelancer:", nama_list)

# Filter data sesuai nama
row = df[df["Nama"] == selected_nama].iloc[0, 1:]
omzet_bulanan = row.values
bulan = row.index.tolist()

# Hitung pajak 0.5%
pajak_bulanan = omzet_bulanan * 0.005
total_omzet = omzet_bulanan.sum()
total_pajak = pajak_bulanan.sum()

# Tampilkan info
st.subheader(f"📊 Ringkasan untuk {selected_nama}")
st.write(f"Total Omzet Tahunan: **Rp {total_omzet:,.0f}**")
st.write(f"Total Pajak (0.5%): **Rp {total_pajak:,.0f}**")

# Buat dataframe untuk grafik
grafik_df = pd.DataFrame({
    "Bulan": bulan,
    "Omzet": omzet_bulanan,
    "Pajak (0.5%)": pajak_bulanan
})

# Visualisasi
st.subheader("📈 Grafik Omzet dan Pajak per Bulan")
fig, ax = plt.subplots()
grafik_df.plot(x="Bulan", y=["Omzet", "Pajak (0.5%)"], kind="bar", ax=ax)
ax.set_ylabel("Rupiah")
ax.set_title(f"Omzet & Pajak Bulanan - {selected_nama}")
st.pyplot(fig)

st.caption("Data ini adalah simulasi dan bukan data pajak sebenarnya.")
