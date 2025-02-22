import os
import pandas as pd
from util import count_amenities_for_house, filter_types_inplace, highest_crime_proportion_for_house

sample_house_lat = 41.8781
sample_house_lon = -87.6298

current_directory = os.getcwd()

# --- Process Restaurant Data ---
file_path = os.path.join(current_directory, "Google_data", "chicago_restaurants.csv")

df_restaurants = pd.read_csv(file_path, header=None, on_bad_lines='skip')
# restaurant data does not have column name when I write csv
df_restaurants.columns = ["Name", "Business Status", "Address", "Price Level", "Rating", "Total Ratings", "Types", "Latitude", "Longitude"]
df_restaurants['Latitude'] = pd.to_numeric(df_restaurants['Latitude'], errors='coerce')
df_restaurants['Longitude'] = pd.to_numeric(df_restaurants['Longitude'], errors='coerce')

# --- Process Convenience/Grocery Store Data ---
store_file = os.path.join(current_directory, "Google_data", "convenience_or_grocery_store_data.csv")
store_columns = ["Name", "Business Status", "Address", "Price Level", "Rating", "Total Ratings", "Types", "Latitude", "Longitude"]
df_stores = pd.read_csv(store_file, header=None, on_bad_lines='skip')
df_stores.columns = store_columns
df_stores['Latitude'] = pd.to_numeric(df_stores['Latitude'], errors='coerce')
df_stores['Longitude'] = pd.to_numeric(df_stores['Longitude'], errors='coerce')
# Define allowed types for filtering.
allowed_store_types = {"supermarket", "grocery_or_supermarket", "drugstore", "convenience_store"}
# Filter the Types column in place.
filter_types_inplace(df_stores, allowed_store_types, column="Types")
# Remove duplicates
df_stores.drop_duplicates(
    subset=["Name", "Business Status", "Address", "Price Level", "Rating", "Total Ratings", "Latitude", "Longitude"],
    inplace=True
)
df_stores.drop(columns=["Types"], inplace=True)

# --- Process School Data ---
school_file = os.path.join(current_directory, "Google_data", "school_data.csv")
df_schools = pd.read_csv(school_file, on_bad_lines='skip')

df_schools['Latitude'] = pd.to_numeric(df_schools['Latitude'], errors='coerce')
df_schools['Longitude'] = pd.to_numeric(df_schools['Longitude'], errors='coerce')

df_schools.drop_duplicates(
    subset=["Name", "Business Status", "Address", "Price Level", "Rating", "Total Ratings", "Latitude", "Longitude"],
    inplace=True
)
df_schools.drop(columns=["Types"], inplace=True)

# --- Process Crime data ---
crime_file = os.path.join(current_directory, "Google_data", "crime.csv")
df_crime = pd.read_csv(crime_file, on_bad_lines='skip')
df_crime['Latitude'] = pd.to_numeric(df_crime['latitude'], errors='coerce')
df_crime['Longitude'] = pd.to_numeric(df_crime['longitude'], errors='coerce')


# --- Sample House Coordinate and Counting ---
sample_house_lat = 41.8781
sample_house_lon = -87.6298

restaurant_count = count_amenities_for_house(sample_house_lat, sample_house_lon, df_restaurants, radius_km=1.0)
store_count = count_amenities_for_house(sample_house_lat, sample_house_lon, df_stores, radius_km=10)
school_count = count_amenities_for_house(sample_house_lat, sample_house_lon, df_schools, radius_km=1.0)
crime_count = count_amenities_for_house(sample_house_lat, sample_house_lon, df_crime, radius_km=1.0)
crime_type, crime_prop = highest_crime_proportion_for_house(sample_house_lat, sample_house_lon, df_crime, radius_km=1.0)

print(f"Number of restaurants within 1 km of sample house ({sample_house_lat}, {sample_house_lon}): {restaurant_count}")
print(f"Number of convenience/grocery stores within 10 km of sample house ({sample_house_lat}, {sample_house_lon}): {store_count}")
print(f"Number of schools within 1 km of sample house ({sample_house_lat}, {sample_house_lon}): {school_count}")
print(f"Crime incidents within 1 km: {crime_count}")
print(f"Most prevalent crime type within 1 km: {crime_type} with proportion {crime_prop:.2f}")

# --- Process house file when Andrew upload the data ---
houses_file_path = ''  # Replace with actual houses CSV path when available.
if os.path.exists(houses_file_path):
    df_houses = pd.read_csv(houses_file_path)
    df_houses['num_restaurants_within_1km'] = df_houses.apply(
        lambda row: count_amenities_for_house(row['latitude'], row['longitude'], df_restaurants, radius_km=1.0),
        axis=1
    )
    df_houses['num_stores_within_1km'] = df_houses.apply(
        lambda row: count_amenities_for_house(row['latitude'], row['longitude'], df_stores, radius_km=1.0),
        axis=1
    )
    df_houses['num_schools_within_1km'] = df_houses.apply(
    lambda row: count_amenities_for_house(row['latitude'], row['longitude'], df_schools, radius_km=1.0),
    axis=1
)
    df_houses['num_crimes_within_1km'] = df_houses.apply(
    lambda row: count_amenities_for_house(row['latitude'], row['longitude'], df_crime, radius_km=1.0),
    axis=1
)
    df_houses[['most_prevalent_crime', 'crime_proportion']] = df_houses.apply(
    lambda row: pd.Series(highest_crime_proportion_for_house(row['latitude'], row['longitude'], df_crime, radius_km=1.0)),
    axis=1 # the helper function returns a tuple, so need to convert it to series for pandas to allocate into two columns
)
    print("Houses DataFrame with counts (first 10 rows):")
    print(df_houses[['latitude', 'longitude', 'num_restaurants_within_1km', 'num_stores_within_1km', 'num_schools_within_1km']].head(10))
else:
    print("Houses file not found. Running single house test only.")