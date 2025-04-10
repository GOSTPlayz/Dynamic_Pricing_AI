import pandas as pd
import numpy as np
import os
# Step 1: Load the dataset
file_path = r"your\path\to\online_retail.xlsx"
print(os.path.exists(file_path))  # This should print True
sheet_name = "Year 2010-2011"
# sheet_name = "Year 2009-2010" if you want to create a new sheet using the data from the year 2009-2010.

df = pd.read_excel(file_path, sheet_name=sheet_name)

# Step 2: Clean data (drop rows where Price is missing or zero)
df = df.dropna(subset=["Price"])
df = df[df["Price"] > 0]

# Step 3: Generate competitor prices (±10% variation)
np.random.seed(42)  # For reproducibility
df["competitor_price"] = df["Price"] * (1 + np.random.uniform(-0.1, 0.1, size=len(df)))

# Optional: Round for realism
df["competitor_price"] = df["competitor_price"].round(2)

# Step 4: Save updated dataset to a new file
output_file = "online_retail_with_competitor.xlsx"
df.to_excel(output_file, index=False)

print(f"Updated dataset saved as '{output_file}' with {len(df)} rows.")
