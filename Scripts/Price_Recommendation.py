import pandas as pd

# Load predictions from CSV
df = pd.read_csv("predicted_quantities.csv")

# AI Pricing Function
def ai_price_recommendation(predicted_qty, competitor_price):
    if predicted_qty >= 50:
        return round(competitor_price * 1.10, 2)
    elif predicted_qty >= 20:
        return round(competitor_price, 2)
    else:
        return round(competitor_price * 0.95, 2)

# Apply pricing strategy
df["recommended_price"] = df.apply(
    lambda row: ai_price_recommendation(row["prediction"], row["avg_competitor_price"]),
    axis=1
)

# Save updated file
df.to_csv("pricing_recommendations.csv", index=False)
print(" Saved: pricing_recommendations.csv")

