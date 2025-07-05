import pandas as pd

# Define expected columns
expected_columns = ["DateTime", "Product", "Price"]

# Try to read the file, skipping bad lines
df = pd.read_csv("price_history.csv", names=expected_columns, header=0, error_bad_lines=False)

# Drop rows with missing or malformed Price values
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df.dropna(subset=["Price"], inplace=True)

# Convert DateTime column to datetime format
df["DateTime"] = pd.to_datetime(df["DateTime"], errors="coerce")
df.dropna(subset=["DateTime"], inplace=True)

# Save cleaned data
df.to_csv("price_history_cleaned.csv", index=False)
print("✅ Cleaned data saved to 'price_history_cleaned.csv'")