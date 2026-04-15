import pandas as pd

df = pd.read_csv("data/funds_knowledge.csv")

def search_funds(query):
    query = query.lower()

    results = df[
        df["name"].str.lower().str.contains(query)
    ]

    if results.empty:
        # fallback: partial match
        results = df[
            df.apply(lambda row: any(word in str(row).lower() for word in query.split()), axis=1)
        ]

    return results.head(2).to_dict(orient="records")