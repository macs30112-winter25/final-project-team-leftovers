# team_leftovers_project

## Crime, Amenities, and Housing Prices in Chicago

# **Crime, Amenities, and Housing Prices in Chicago**

## **Overview**
This project explores the relationship between crime rates, amenities (such as grocery stores, hospitals, schools, and restaurants), and housing prices in Chicago. By leveraging spatial analysis and statistical modeling, we aim to determine how these factors influence property values. 

### **Key Research Questions**
- Does proximity to certain amenities increase or decrease property values?
- How significant is crime in affecting housing prices?
- Do amenities offset the negative effects of crime, or does crime diminish the value of nearby amenities?
- What statistical relationships can we uncover in Chicago’s real estate market?

### **Main Findings**
- **Crime negatively impacts property values**, with a measurable decrease in price per square foot as crime rates increase.
- **Amenities generally increase property values**, especially grocery stores, hospitals, and highly rated restaurants.
- **Interactions between crime and amenities are complex**—while amenities can offset crime’s negative effects, high crime rates still suppress the value boost from amenities.
- **OLS regression models** show significant correlations between crime, amenities, and housing prices, while visualizations highlight spatial trends.

---

## **Repository Structure**
This repository contains all datasets, scripts, and reports related to our analysis.

## Components

### Python Files
- **get_places.py:**  
  Uses the Google Places API to scrape nearby amenities.
  
- **count_amenities.py:**  
  Counts the surrounding amenities for each listing and concatenates these counts to the Redfin data.
  
- **get_crime_data.ipynb:**  
  Scrapes crime data using the Chicago PD API.
  
- **util.py:**  
  Provides helper functions for `count_amenities.py`.
  
- **redfin_crawler.py:**  
  Scrapes Redfin data using a Scrapper API.

### Data

#### Google Data
- **chicago_restaurant.csv:**  
  Contains restaurant data.
  
- **convenience_or_grocery_store.csv:**  
  Contains convenience store data.
  
- **hospital_data.csv:**  
  Contains hospital data.
  
- **school_data.csv:**  
  Contains school data.
  
- **summary_redfin:**  
  A summary dataset that combines Redfin data with amenities counts.

#### Redfin Data
- **redfin_cleaned_v1.csv:**  
  Contains an initial cleaned version of the Redfin housing data, with key variables such as price, square footage, number of bedrooms and bathrooms, and geographic coordinates.

- **redfin_cleaned_v2.csv:**  
  A further refined version of the housing dataset with additional cleaning, removal of outliers, and formatted variables for analysis.

- **redfin_cleaner_v1.ipynb:**  
  A Jupyter Notebook used for cleaning and preprocessing the Redfin dataset, including handling missing values and standardizing variable formats.

- **redfin_cleaner_v2.ipynb:**  
  An improved cleaning script that incorporates additional filtering and formatting of Redfin data for integration into the analysis.

#### Visualization and Statistics
- **stats.ipynb:**  
  Contains all statistical analysis, including correlation matrices, regression models, and visualizations that explore the relationship between crime, amenities, and housing prices.

- **determine_distance.ipynb:**  
  A script to compute distances between properties and various amenities, aiding in spatial analysis.

#### Other Files
- **requirement.txt:**  
  Lists all necessary dependencies and library versions required to reproduce the analysis.

- **README.md:**  
  Provides an overview of the project, how to navigate the repository, and instructions for running the analysis.

---

### **How to Run the Code**
1. **Clone the repository**  
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/final-project-team-leftovers.git
   cd final-project-team-leftovers
2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
4. **Run data cleaning scripts before analysis**
   python redfin_data/redfin_cleaner.py
   python Google_data/process_and_combine.py
5. **Perform statistical analysis & generate visualizations**
   jupyter notebook visualization_and_stats/stats.ipynb
6. **Run the web scraper for updated Redfin data**
   python redfin_crawler.py

This version is now fully tailored to **final-project-team-leftovers**, matching your repository structure and ensuring smooth execution. Let me know if you need further refinements!
