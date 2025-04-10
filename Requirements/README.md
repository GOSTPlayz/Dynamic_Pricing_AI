# 🧠 AI-Driven Dynamic Pricing Optimization

> End-to-end machine learning and AI project for predicting product demand and recommending optimal prices using GPT reasoning and real-time visual dashboards.

---

## 📌 Key Features
- ⚙️ Trained ML model using **PySpark** to predict product demand
- 💬 Integrated **OpenAI GPT-3.5** for pricing logic & justifications
- 📊 Built interactive dashboards in **Tabulae** for visualization
- ☁️ Used **AWS S3** for cloud data storage (optional/local)
- 📈 Automatically recommends **optimal prices** based on predicted demand & competitor pricing

--

## Folder Structure

Dynamic_Pricing_AI/
├── data/                          # Contains raw & processed data
│   └── online_retail.xlsx
│   └── ai_pricing_recommendations_final.csv
├── notebooks/                    # Optional: Jupyter analysis notebooks
│   └── exploratory_analysis.ipynb
├── scripts/                      # Python files for each stage
│   ├── data_preprocessing.py
│   ├── spark_training.py
│   ├── price_recommendation.py
│   └── openai_integration.py
├── visualizations/               # Tabulae screenshots or exports
│   └── dashboard_preview.png
├── requirements.txt              # Python dependencies
├── README.md                     # Project overview
└── .gitignore
