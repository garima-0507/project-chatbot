# analysis.py
import pandas as pd

# ------------------ Load Datasets ------------------
CROP_DATA_PATH = "datasets/RS_Session_258_AU_1133_1.csv"
RAINFALL_DATA_PATH = "datasets/rainfall_by_districts_2019.csv"

try:
    crop_df = pd.read_csv(CROP_DATA_PATH)
    rainfall_df = pd.read_csv(RAINFALL_DATA_PATH)
except Exception as e:
    print("Error loading datasets:", e)

# ------------------ CROP ANALYSIS ------------------
def top_n_crops(n=5):
    df = crop_df.copy()
    df.columns = df.columns.str.strip().str.lower()
    prod_col = [col for col in df.columns if 'production' in col.lower()][0]
    crop_col = [col for col in df.columns if 'crop' in col.lower()][0]
    df_grouped = df.groupby(crop_col)[prod_col].sum().reset_index()
    df_grouped.rename(columns={crop_col: 'crop', prod_col: 'production'}, inplace=True)
    df_grouped = df_grouped.sort_values(by='production', ascending=False).head(n)
    df_grouped["production (million tonnes)"] = (df_grouped["production"] / 1_000_000).round(2)
    df_grouped.drop(columns=["production"], inplace=True)
    return df_grouped

def compare_crops(crop1, crop2):
    df = crop_df.copy()
    df.columns = df.columns.str.strip().str.lower()
    prod_col = [col for col in df.columns if 'production' in col.lower()][0]
    crop_col = [col for col in df.columns if 'crop' in col.lower()][0]
    df = df[[crop_col, prod_col]]
    df_crop = df[df[crop_col].str.lower().isin([crop1.lower(), crop2.lower()])]
    result = df_crop.groupby(crop_col)[prod_col].sum().reset_index()
    result["Production (Million tonnes)"] = (result[prod_col] / 1_000_000).round(2)
    result.rename(columns={crop_col: "Crop "}, inplace=True)
    result.drop(columns=[prod_col], inplace=True)
    provenance = {"file": CROP_DATA_PATH}
    return result, provenance

# ------------------ RAINFALL ANALYSIS ------------------
def compare_rainfall(district1, district2):
    df = rainfall_df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={"district": "District", "actual_rainfall (mm)": "Actual_Rainfall"})
    df_sub = df[df["District"].str.lower().isin([district1.lower(), district2.lower()])]
    provenance = {"file": RAINFALL_DATA_PATH}
    return df_sub[["District", "Actual_Rainfall"]], provenance

def top_bottom_rainfall(n=1):
    df = rainfall_df.copy()
    df.columns = df.columns.str.strip().str.lower()
    df = df.rename(columns={"district": "District", "actual_rainfall (mm)": "Actual_Rainfall"})
    top = df.sort_values(by="Actual_Rainfall", ascending=False).head(n)
    bottom = df.sort_values(by="Actual_Rainfall", ascending=True).head(n)
    provenance = {"file": RAINFALL_DATA_PATH}
    return top, bottom, provenance
