from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd

# 1. Load the saved village data
df = joblib.load("village_data.pkl")

# 2. Create FastAPI app
app = FastAPI(title="Village Search API")

# 3. Search endpoint
@app.get("/search/")
def search_location(location_name: str):
    location_name_lower = location_name.lower()
    
    # Exact matches (case-insensitive)
    exact_matches = df[df['location'].str.lower() == location_name_lower]
    
    # Partial matches excluding exact matches
    partial_matches = df[
        (df['location'].str.contains(location_name, case=False, na=False)) & 
        (df['location'].str.lower() != location_name_lower)
    ]
    
    # Limit partial matches to 5
    partial_matches = partial_matches.head(5)
    
    # Combine results: exact first, then partial
    combined_results = pd.concat([exact_matches, partial_matches])
    
    if combined_results.empty:
        raise HTTPException(status_code=404, detail="Location not found.")
    
    return combined_results.to_dict(orient='records')
