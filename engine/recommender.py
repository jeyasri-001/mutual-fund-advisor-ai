import pandas as pd

df = pd.read_csv("data/recommendations.csv")

df.columns = df.columns.str.strip()
df["Risk Category"] = df["Risk Category"].str.strip().str.lower()

# Remove commas if present
df["MinAmount"] = df["MinAmount"].astype(str).str.replace(",", "")
df["MaxAmount"] = df["MaxAmount"].astype(str).str.replace(",", "")

df["MinAmount"] = pd.to_numeric(df["MinAmount"], errors="coerce")
df["MaxAmount"] = pd.to_numeric(df["MaxAmount"], errors="coerce")
df["Fund %"] = pd.to_numeric(df["Fund %"], errors="coerce")

def get_recommendation(risk_category, sip_amount):

    risk_category = risk_category.strip().lower()

    filtered = df[
        (df["Risk Category"] == risk_category) &
        (df["MinAmount"] <= sip_amount) &
        (df["MaxAmount"] >= sip_amount)
    ]

    if filtered.empty:
        return []

    result = []

    for _, row in filtered.iterrows():
        result.append({
            "fund_name": row["Fund Names"],
            "allocation": row["Fund %"]
        })

    return result