import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Solar Comparison Dashboard", layout="wide")

# --- Title ---
st.title("☀️ Cross-Country Solar Data Dashboard")
st.markdown("Compare solar metrics (GHI, DNI, DHI) across Benin, Togo, and Sierra Leone")

# --- Load data ---
@st.cache_data
def load_data():
    countries = {}
    for name in ["benin", "togo", "sierraleone"]:
        try:
            df = pd.read_csv(f"data/{name}_clean.csv")
            df["country"] = name.capitalize()
            countries[name] = df
        except FileNotFoundError:
            st.warning(f"{name}_clean.csv not found.")
    return pd.concat(countries.values(), ignore_index=True)

df = load_data()

if df.empty:
    st.error("No valid data found.")
    st.stop()

# --- Sidebar controls ---
st.sidebar.header("Filters")
metrics = ["GHI", "DNI", "DHI"]
metric = st.sidebar.selectbox("Select metric", metrics)
countries = st.sidebar.multiselect(
    "Select countries", df["country"].unique(), default=list(df["country"].unique())
)

filtered = df[df["country"].isin(countries)]

# --- Boxplot ---
st.subheader(f"📊 {metric} Distribution by Country")
fig, ax = plt.subplots(figsize=(7, 4))
sns.boxplot(x="country", y=metric, data=filtered, palette="viridis", ax=ax)
ax.set_xlabel("Country")
ax.set_ylabel(metric)
st.pyplot(fig)

# --- Summary table ---
st.subheader("📈 Summary Statistics")
summary = (
    filtered.groupby("country")[["GHI", "DNI", "DHI"]]
    .agg(["mean", "median", "std"])
    .round(2)
)
st.dataframe(summary)

# --- Average GHI ranking ---
st.subheader("🏆 Average GHI Ranking")
avg_ghi = (
    filtered.groupby("country")["GHI"].mean().sort_values(ascending=False)
)
st.bar_chart(avg_ghi)
