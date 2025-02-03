# team_leftovers_project

# Winter 2025 – Final Project Progress Report 1

# (Andrew, Marija, and Zhenning)

## Project Description

### Research Questions & Issue Addressed

Our project investigates the relationship between neighborhood amenities and property values, considering the impact of crime statistics. Crime has a negative effect on property values, while increased access to amenities, such as restaurants, schools, healthcare facilities, and recreational centers, generally increases property values. Less well understood is how these two factors-crime and amenities-interact with each other. Specifically, we investigate how and by how much the various types of amenities-e. g. food stores, schools-would be balancing off the negative impacts caused by a high crime rate.


Our primary research question is: **How does the availability and cost of neighborhood amenities influence housing prices?** Additionally, we examine: **To what extent do different types of amenities mitigate the negative impact of crime on property values?**

### Relevance from a Social Science Perspective

Understand these relationships, and one may be able to help the policymaker, real estate investor, and urban planner in making data-driven decisions. We discretize amenities into finer categories and integrate crime statistics, adding value to the general assumption of increasing property values due to amenities. This analysis will discuss whether discretionary amenities-for example, schools-may have a higher mitigating impact on crime's effect than essential amenities, such as convenience stores.

### Key Concepts and Measurements

- **Amenities**: Defined as grocery stores, restaurants, and schools within a zip code.
- **Crime Statistics**: Measured via crime incidence data from the FBI and Chicago Police Department APIs.
- **Property Value**: Extracted from Redfin and Realtor.com to assess real estate pricing trends.

### Hypothesis

Amenities available and amenities price are positive determinants for property values; hence, areas with higher-order restaurants and a greater number of schools of excellence will have to command higher value. In contrast, high crime should deflate housing values, even though amenities are also present.

## Data Sources

| Data Source | Type | Link | Time Frame | Estimated Data Volume | Reliability Issues & Mitigation |
|------------|------|------|------------|--------------------|-----------------------------|
| Yelp API | Scraping | [Yelp API](https://www.yelp.com/developers) | 2025 | ~10,000 amenities | Data might be biased toward higher-end businesses; cross-check with Google Maps |
| Google Maps Places API | Scraping | [Google API](https://developers.google.com/maps/documentation/places/web-service/overview) | 2025 | Additional amenities | Possible location inaccuracy; verify data overlap with Yelp |
| Redfin | Scraping | [Redfin](https://www.redfin.com/) | 2025 | ~60 zip codes in Chicago | Missing values possible; supplement with Realtor.com |
| Realtor.com | Scraping | [Realtor.com](https://www.realtor.com/) | 2025 | ~60 zip codes in Chicago | Data cleaning needed to handle inconsistencies |
| FBI Crime API | API | [FBI API](https://crime-data-explorer.fr.cloud.gov/) | 2025 | Crime reports per zip code | Crime underreporting possible; validate with CPD data |
| Chicago Police API | API | [CPD Crime API](https://data.cityofchicago.org/) | 2025 | Crime reports per zip code | Ensure data consistency with FBI API |

## Data Cleaning and Wrangling

- Standardize and combine the scraped property value data from Redfin and Realtor.com.
- Aggregate amenity data at the zip code level and introduce unique identifiers.
- Geospatially match the crime data with zip codes.
- Clean the missing and duplicate data and ensure consistency in the time frame.
- Normalize the cost level of amenities and property prices to compare.

## Data Analysis and Visualization

- **Dependent Variable**: Property Value (Redfin, Realtor.com)
- **Independent Variables**: Amenity density, crime rate
- **Control Variables**: Zip code demographic data

### Planned Analysis Methods

- **Correlation analysis** for testing relationships among amenities, crime, and property values.
- **Multiple regression modeling** for quantifying the interaction effects of amenities and crime.
- **Spatial analysis** by geocoding to display trends across the zip codes in Chicago.

### Expected Visualizations

- Heatmaps of amenity density and crime data
- Scatter plots of amenity levels vs. property values
- Regression plots of the relationships between crime, amenities, and housing prices

## Responsibilities

| Team Member | Responsibilities |
|-------------|----------------|
| Andrew | Scraping Zillow and Redfin; cleaning and standardizing real estate pricing data; hosting repository |
| Maria | Accessing and organizing Chicago crime data; geocoding datasets; conducting correlation analysis     |
| Zhenning | Collecting and processing crime data; designing statistical models; collaborating on presentation |
