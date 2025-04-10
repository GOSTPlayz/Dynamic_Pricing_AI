from dotenv import load_dotenv
import os
import openai
import pandas as pd
import time


openai.api_key= "OPENAI_API_KEY"
#Replace OPENAI_API_KEY with your OPENAI api KEY.


# Load data
df = pd.read_csv("predicted_quantities.csv").head(20)  # Limit to 10 rows for testing

#  Cache storage (in-memory dictionary)
response_cache = {}

#  Function with caching and explanation
def get_ai_price_and_explanation(product, predicted_qty, competitor_price):
    key = f"{product}_{predicted_qty}_{competitor_price}"

    # Check cache first
    if key in response_cache:
        return response_cache[key]

    # Generate prompt
    prompt = (
        f"You are a pricing strategist. "
        f"For product '{product}', the predicted demand is {predicted_qty:.0f} units. "
        f"The competitor offers it at ${competitor_price:.2f}. "
        f"What is the optimal selling price, and why? Return your answer in this format:\n\n"
        f"Recommended Price: $XX.XX\nExplanation: <reason>"
    )

    # Send to OpenAI
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=150
        )

        reply = response['choices'][0]['message']['content'].strip()

        # Parse result
        if "Recommended Price:" in reply:
            price_line, explanation_line = reply.split("Explanation:", 1)
            recommended_price = float(price_line.split("$")[-1].strip())
            explanation = explanation_line.strip()
        else:
            recommended_price = competitor_price
            explanation = "Fallback: Could not extract answer."

    except Exception as e:
        recommended_price = competitor_price
        explanation = f"Error: {e}"

    # Cache result
    response_cache[key] = (recommended_price, explanation)
    return recommended_price, explanation

#  Apply to DataFrame
df["ai_price"] = None
df["explanation"] = None


for idx, row in df.iterrows():
    try:
        price, reason = get_ai_price_and_explanation(
            row["StockCode"], row["prediction"], row["avg_competitor_price"]
        )
        df.at[idx, "ai_price"] = price
        df.at[idx, "explanation"] = reason

        print(f" [{idx}] Processed {row['StockCode']} - Price: ${price}")
    except Exception as e:
        df.at[idx, "ai_price"] = row["avg_competitor_price"]
        df.at[idx, "explanation"] = f"Error: {e}"
        print(f" [{idx}] Error for {row['StockCode']}: {e}")

    time.sleep(21)  # Wait ~21 seconds per request (to stay under 3 RPM)


#  Save result
df.to_csv("ai_pricing_explained.csv", index=False)
print(" AI recommendations with explanations saved to 'ai_pricing_explained.csv'")