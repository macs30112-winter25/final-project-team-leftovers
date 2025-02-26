import pandas as pd
import numpy as np
import geopandas as gpd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from shapely.geometry import Point

try:
    crime_data = pd.read_csv("crime.csv")
    grocery_data = pd.read_csv("grocery store_data_demo.csv")
    hospital_data = pd.read_csv("hospital_data.csv")
    school_data = pd.read_csv("school_data.csv")
    redfin_data = pd.read_csv("redfin_cleaned_v2.csv")
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit()

required_columns = {
    "redfin": ["Address", "price", "sq_ft", "Latitude", "Longitude"],
    "crime": ["Latitude", "Longitude"],
    "grocery": ["Latitude", "Longitude"],
    "hospital": ["Latitude", "Longitude"],
    "school": ["Latitude", "Longitude"]
}

def validate_columns(df, name, required_cols):
    for col in required_cols:
        if col not in df.columns:
            print(f"Error: Column '{col}' missing in {name} dataset")
            exit()

validate_columns(redfin_data, "redfin", required_columns["redfin"])
validate_columns(crime_data, "crime", required_columns["crime"])
validate_columns(grocery_data, "grocery", required_columns["grocery"])
validate_columns(hospital_data, "hospital", required_columns["hospital"])
validate_columns(school_data, "school", required_columns["school"])

redfin_gdf = gpd.GeoDataFrame(redfin_data, geometry=gpd.points_from_xy(redfin_data.Longitude, redfin_data.Latitude), crs="EPSG:4326")
crime_gdf = gpd.GeoDataFrame(crime_data, geometry=gpd.points_from_xy(crime_data.Longitude, crime_data.Latitude), crs="EPSG:4326")
grocery_gdf = gpd.GeoDataFrame(grocery_data, geometry=gpd.points_from_xy(grocery_data.Longitude, grocery_data.Latitude), crs="EPSG:4326")
hospital_gdf = gpd.GeoDataFrame(hospital_data, geometry=gpd.points_from_xy(hospital_data.Longitude, hospital_data.Latitude), crs="EPSG:4326")
school_gdf = gpd.GeoDataFrame(school_data, geometry=gpd.points_from_xy(school_data.Longitude, school_data.Latitude), crs="EPSG:4326")

def count_nearby(geo_df1, geo_df2, radius=500):
    geo_df1 = geo_df1.to_crs(epsg=3857)
    geo_df2 = geo_df2.to_crs(epsg=3857)
    geo_df2["buffer"] = geo_df2.geometry.buffer(radius)
    geo_df2 = geo_df2.set_geometry("buffer")
    joined = gpd.sjoin(geo_df1, geo_df2, how="left", predicate="within")
    return joined.groupby(joined.index).size().reindex(geo_df1.index, fill_value=0)

redfin_gdf["crime_count"] = count_nearby(redfin_gdf, crime_gdf)
redfin_gdf["grocery_count"] = count_nearby(redfin_gdf, grocery_gdf)
redfin_gdf["hospital_count"] = count_nearby(redfin_gdf, hospital_gdf)
redfin_gdf["school_count"] = count_nearby(redfin_gdf, school_gdf)

redfin_gdf.dropna(subset=["price", "sq_ft"], inplace=True)
redfin_gdf["price_per_sq_m"] = redfin_gdf["price"] / redfin_gdf["sq_ft"] * 10.764

full_data = redfin_gdf[["price_per_sq_m", "crime_count", "grocery_count", "hospital_count", "school_count"]]

if not full_data.empty:
    corr_matrix = full_data.corr()
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.xticks(rotation=30, ha="right") 
    plt.yticks(rotation=0)  
    plt.subplots_adjust(bottom=0.25)  
    plt.title("Correlation Matrix: Crime, Amenities, and Property Prices")
    plt.show()
else:
    print("Error: No data available after merging.")
    exit()

X = full_data[["crime_count", "grocery_count", "hospital_count", "school_count"]]
y = full_data["price_per_sq_m"]
X = sm.add_constant(X)

model = sm.OLS(y, X).fit()
print(model.summary())

for column in ["crime_count", "school_count", "hospital_count", "grocery_count"]:
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=full_data, x=column, y="price_per_sq_m")
    plt.title(f"{column.replace('_', ' ').title()} vs Property Price per Square Meter")
    plt.xlabel(column.replace('_', ' ').title())
    plt.ylabel("Avg Price per Sq Meter")
    plt.show()