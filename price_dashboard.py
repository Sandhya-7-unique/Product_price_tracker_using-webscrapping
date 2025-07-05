import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from PIL import Image


# Show an image banner at the top of the dashboard
#st.image("assets/banner.png", width=400)

# Load cleaned data
df = pd.read_csv("price_history_cleaned.csv", parse_dates=["DateTime"])

# Ensure Price is numeric
df["Price"] = pd.to_numeric(df["Price"], errors='coerce')
df = df.dropna(subset=["Price"])

st.title("Price Tracker Dashboard")
image = Image.open("assets/banner.png")
st.image(image, use_column_width=100)
# Product selection dropdown
products = df["Product"].unique()
selected_product = st.selectbox("Select Product", products)

# Filter data by selected product
product_df = df[df["Product"] == selected_product]

# Date range limits
min_date = product_df["DateTime"].min().date()
max_date = product_df["DateTime"].max().date()

# Use session state for date range persistence
if 'date_range' not in st.session_state:
    st.session_state.date_range = [min_date, max_date]

date_range = st.date_input(
    "Select date range",
    value=st.session_state.date_range,
    min_value=min_date,
    max_value=max_date,
    key="date_range_selector"
)

# Update session state
st.session_state.date_range = date_range

# Latest price for alert
latest_price = product_df.sort_values("DateTime", ascending=False).iloc[0]["Price"]

# Alert price input
alert_price = st.number_input(
    f"Set alert price for '{selected_product}' (₹):",
    min_value=0.0,
    step=1.0,
    value=float(product_df["Price"].min())
)

# Show alert if latest price drops below alert price
if latest_price < alert_price:
    st.success(f"🚨 Price Alert! Latest price ₹{latest_price:.2f} is below your alert price ₹{alert_price:.2f}!")
else:
    st.info(f"Latest price is ₹{latest_price:.2f}. No alert triggered.")

# Filter and plot data
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if start_date > end_date:
        st.error("⚠️ Please select a valid date range where start date is before end date.")
    else:
        filtered_df = product_df[(product_df["DateTime"] >= start_date) & (product_df["DateTime"] <= end_date)]

        st.write(f"Filtered rows count: {len(filtered_df)}")

        if not filtered_df.empty:
            st.subheader("Price Statistics")
            st.write(f"**Minimum Price:** ₹{filtered_df['Price'].min():.2f}")
            st.write(f"**Maximum Price:** ₹{filtered_df['Price'].max():.2f}")
            st.write(f"**Average Price:** ₹{filtered_df['Price'].mean():.2f}")

            st.subheader("Price Trend Chart")
            fig, ax = plt.subplots()
            ax.plot(filtered_df["DateTime"], filtered_df["Price"], marker='o', linestyle='-')
            ax.set_xlabel("Date")
            ax.set_ylabel("Price (₹)")
            ax.set_title(f"Price Trend for {selected_product}")
            plt.xticks(rotation=45)
            plt.tight_layout()
            st.pyplot(fig)

# Debug / data info section (optional)
st.header("Data Sample")
st.dataframe(df.head(10))

st.header("Data Columns and Types")
st.write(df.dtypes)

st.header("Unique Products")
st.write(df["Product"].unique())

st.header("Date Range in Data")
st.write(df["DateTime"].min(), df["DateTime"].max())











