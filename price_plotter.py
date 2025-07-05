import pandas as pd
import matplotlib.pyplot as plt

# Define columns explicitly
colnames = ["DateTime", "Product", "Price"]

# Read CSV while skipping bad lines (for pandas < 1.3)
df = pd.read_csv(
    "price_history.csv",
    names=colnames,
    header=0,
    parse_dates=["DateTime"],
    error_bad_lines=False  # old pandas syntax
)

# Clean price column if it's a string like '₹1,39,990.00'
df["Price"] = df["Price"].replace(r"[^\d.]", "", regex=True).astype(float)

# Plot price trends for each product
for product in df["Product"].unique():
    product_df = df[df["Product"] == product]
    plt.plot(product_df["DateTime"], product_df["Price"], label=product[:50] + "...")

plt.xlabel("Date")
plt.ylabel("Price (INR)")
plt.title("Price History")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()