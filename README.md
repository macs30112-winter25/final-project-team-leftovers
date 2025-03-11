# team_leftovers_project

# **Crime, Amenities, and Housing Prices in Chicago**

## **Overview**
This project explores the relationship between crime rates, amenities (such as grocery stores, hospitals, schools, and restaurants), and housing prices in Chicago. By leveraging spatial analysis and statistical modeling, we aim to determine how these factors influence property values. 

### **Key Research Questions**
- Does proximity to certain amenities increase or decrease property values?
- How significant is crime in affecting housing prices?
- Do amenities offset the negative effects of crime, or does crime diminish the value of nearby amenities?
- What statistical relationships can we uncover in Chicago’s real estate market?

### **Main Findings Summary**

- **Crime and Housing Prices:**  
  The results from the regression analysis show a negative and statistically significant relationship between crime counts and property values, indicating that crime is significant factor influencing housing prices by itself.

- **Impact of Amenities:**  
  The restaurants (count and ratings), hospitals and grocery stores indicated a positive and statistically significant relationship with property value. This supports our hypothesis that amenity advantages compel a neighborhood, thus raising demand and prices.

- **Interaction between Restaurant and Crimes**  
  There is a significant positve interaction between restaurant and crime, indicating the presence of more restaurants could mitigate the negative effect of crime on property value.

- **Concerns about Multicollinearity:**  
  Some amenities showed multicollinearity in our preliminary models, most notably between grocery stores and hospitals, which inflated standard errors. This was managed by modifying the model using different specifications with interaction terms and reduced sets of predictors.

- **Model Fit Overall:** <br>
  According to the OLS regression, an R-squared of approximately .6 indicates that, while crime and amenities have their effects, other factors-neighborhood characteristics, public services, economic trends-must come in to varying degrees to explain price diveramce.

- **Additional Exploration after Presentation:** <br>
  We have explore a few more models involving violent crimes (vs. total crime) and adding squared term for detecting non-linearity. Please refer to the stats.ipynb for detail finding and comparison.
---

## How to Navigate the Repo
```bash
final-project-team-leftovers/
├── data/
│   ├── crime/
│   │   ├── crime.csv                      # crime data
│   │   └── get_crime.ipynb                # notebook for requesting crime data
│   ├── place_data/
│   │   ├── chicago_restaurants.csv        # restaurant data
│   │   ├── convenience_store_data.csv     # convenience store data
│   │   ├── get_place.py                   # py file for scraping place data from Google
│   │   ├── hospital_data.csv              # hospital data
│   │   └── school_data.csv                # school data
│   ├── redfin_data/
│   │   ├── [Redfin files...]
│   ├── summary_redfin.csv                 # master dataframe that contains all processed data
│   ├── process_and_combine.py             # py file for processing raw data and calculate relevant numbers
│   └── util.py                            # helper functions for process_and_combine.py
├── progress_report/
│   ├── progress_report_1.pdf
│   └── progress_report_2.pdf
├── visualization_and_stats/
│   ├── stats.ipynb                        # regression analysis
│   └── viz.ipynb                          # visualization
├── LICENSE
├── requirement.txt
└── README.md
```

---

### **How to Run the Code**
1. **Clone the repository**  
   ```bash
   git clone https://github.com/macs30112-winter25/final-project-team-leftovers.git
   cd final-project-team-leftovers
2. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
3. **Run data cleaning scripts before analysis**
   ```bash
   python redfin_data/redfin_cleaner.py
   python Google_data/process_and_combine.py
4. **Perform statistical analysis & generate visualizations**
   ```bash
   jupyter notebook visualization_and_stats/stats.ipynb
5. **Run the web scraper for updated Redfin data**
   ```bash
   python redfin_crawler.py
  

---

## **Data Sources**
Our project integrates multiple datasets to analyze the relationship between crime, amenities, and housing prices. Below are the data sources used in our analysis:

### **Real Estate Data**
- **[Redfin Housing Data](https://www.redfin.com/)**  
  - Source: Scraped from Redfin using an API.
  - Description: Contains property listings, prices, square footage, number of bedrooms/bathrooms, and location coordinates.

### **Crime Data**
- **[City of Chicago Crime Data](https://gis.chicagopolice.org/)**  
  - Source: Chicago Police Department.
  - Description: Includes reported crimes in Chicago with geolocation, crime type, and date.

### **Amenities Data**
- **[Google Places API](https://developers.google.com/maps/documentation/places/web-service/overview)**  
  - Source: Google Maps API.
  - Description: Provides locations of amenities such as grocery stores, hospitals, schools, and restaurants.
  - Data extracted for:
    - **chicago_restaurants.csv** (Restaurants)
    - **convenience_store_data.csv** (Convenience/Grocery Stores)
    - **hospital_data.csv** (Hospitals)
    - **school_data.csv** (Schools)

### **Processed and Merged Data**
- **summary_redfin.csv**  
  - Description: Final dataset merging Redfin housing data with nearby amenities and crime counts.

These sources collectively enable a detailed statistical analysis of how crime and amenities impact housing prices. 

## **Team Members and Contributions**

| **Name**             | **Contributions** |
|----------------------|------------------|
| **Marija Starovoita** | Focused on the organizational aspects of the project, including managing reports, structuring documentation, processing data, and conducting initial statistical analysis and visualizations. |
| **Andrew Koller**    | Responsible for cleaning and preprocessing the data, collecting and structuring Redfin housing data, and ensuring dataset consistency for analysis. |
| **Zhenning Liu**     | Scrape, clean, and process Google place data; compute required statistics and combine all data into one source; Further visualization; Clean summary data and finalize statistical analysis |

## **Project Presentation Links**

- **[Initial In-Class Presentation](https://docs.google.com/presentation/d/15ZbWyB3VqUQtp61funDqU-i6NCn1aETTXU1ERqfwlF8/edit?usp=sharing)** 
  Link to the first version of the in-class presentation slides.

- **[Updated Final Presentation](https://docs.google.com/presentation/d/1t65F_TXEYmy9V7WwxHWSRnGGe8f_7pgWltalqUqxLZs/edit?usp=sharing)**
  Link to the revised version of the presentation slides after incorporating feedback.

- **[Final Project Report](https://docs.google.com/document/d/1hTj_KqZCivTHqVHlx3ydViXrW40zoZmMPzagpTn9HYk/edit?usp=sharing)**
  Link to the final rpoject report, combining the project's goals, research questions, hypothesis, modeling, visualizations, and findings.

- **[Project Video](<link needed here>)**  
  Link to the project video  
  *Note: The video is not uploaded directly to the repository due to storage limitations.*

## **AI Usage** ##
- This project utilized AI primarily to debug code and interpret error messages. **Markdowner** is technically AI software, however, as it utilizes AI to turn webpage HTML into Markdown. Consequently, AI was utilized to scrape Redfin data. 
