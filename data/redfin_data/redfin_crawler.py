# Author: Andrew Koller

# This python scripr is used to scrape Redfin listings for Chicago, IL. The script
# scrapes the first 9 pages of each ZIP code in Chicago and saves the URLs to a file.
# The URLs are then processed through ScraperAPI to fetch the property details. The
# property details are then stored in a SQLite database.

# Resources:
# - ScraperAPI: https://www.scraperapi.com/
# https://www.scraperapi.com/solutions/real-estate-data-collection/redfin-scraper/
# - md.dhr.wtf: https://md.dhr.wtf/
# - Redfin: https://www.redfin.com/
# https://stackoverflow.com/questions/37232649/will-creating-an-sql-table-that-already-exists-overwrite-it
# https://www.sqlite.org/lang_createtable.html#the_primary_key
# https://stackoverflow.com/questions/14461851/how-to-have-an-automatic-timestamp-in-sqlite
# https://www.sqlite.org/docs.html




import requests
import re
import time
import json
import os
import sqlite3
from datetime import datetime

# NOTE: Adjust or shorten if needed; 
ZIPCODES = [
    60601, 60602, 60603, 60604, 60605, 60606, 60607, 60608, 60609, 60610,
    60611, 60612, 60613, 60614, 60615, 60616, 60617, 60618, 60619, 60620,
    60621, 60622, 60623, 60624, 60625, 60626, 60628, 60629, 60630, 60631,
    60632, 60633, 60634, 60636, 60637, 60638, 60639, 60640, 60641, 60642,
    60643, 60644, 60645, 60646, 60647, 60649, 60651, 60652, 60653, 60654,
    60655, 60656, 60657, 60659, 60660, 60661, 60664, 60666, 60668, 60669,
    60670, 60673, 60674, 60675, 60677, 60678, 60680, 60681, 60682, 60684,
    60685, 60686, 60687, 60688, 60689, 60690, 60691, 60693, 60694, 60695,
    60696, 60697, 60699, 60701
]

# We only want pages 1 to 9
# Redfin will only return a maximum of 9 pages, and when we attempt to iterate past that
# we will be redirected to the first page.
PAGE_NUMBERS = range(1, 10)


def init_database(db_path):
    
    """
    Initialize SQLite database with required tables.
    
    Args:
        db_path (str): The path to the SQLite database file.
    
    Output:
        Initializes the database with a `properties` table if it doesn't exist.
    
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # Create properties table if it doesn't exist
    # We store the URL, data, and created_at timestamp
    # url is the primary key to prevent duplicates
    c.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            url TEXT PRIMARY KEY,
            data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()


def extract_redfin_urls(content):
    """
    Extract Redfin URLs from markdown content.
    
    Args:
        content (str): Markdown content

    Returns:
        list: A list of Redfin URLs.
    """
    pattern = r'\((/IL/Chicago/.*?/home/\d+)'
    return ['https://redfin.com' + path for path in re.findall(pattern, content)]


def scrape_zipcode(zipcode):
    """
    For a given ZIP, fetch pages until we detect a redirect or find all listings.
    Returns a list of URLs and saves them to a ZIP-specific file. 

    md.dhr.wtf is a free scraping tool that we utilized to bypass Redfin's bot detection. 
    It returns the Redfin page HTML as markdown. md.dhr.wtf was chosen because it is 
    free.

    Args:
        zipcode (int): The ZIP code to scrape.

    Outputs:
        urls_file (str): The filename containing the URLs.
        all_urls (list): A list of all URLs found.

    """
    all_urls = set()
    urls_file = f"urls_{zipcode}.txt"
    
    # Load existing URLs if file exists
    if os.path.exists(urls_file):
        with open(urls_file, 'r') as f:
            all_urls.update(line.strip() for line in f)
    
    # Keep track of previous page's URLs
    previous_page_urls = set()  
    
    for page in PAGE_NUMBERS:
        # Build the URL for this page
        # This is where we use md.dhr.wtf to bypass bot detection. All we need to do is
        # add the redfin URL to the end of the md.dhr.wtf URL.
        if page == 1:
            # The first page of a Redfin search page does not have a page number in the URL
            url = f"https://md.dhr.wtf/?url=https://www.redfin.com/zipcode/{zipcode}"
        else:
            # Subsequent URLs have the page number in the URL
            url = f"https://md.dhr.wtf/?url=https://www.redfin.com/zipcode/{zipcode}/page-{page}"
        
        print(f"\nFetching {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            content = response.text
            
            # Extract URLs for current page using the regex function
            current_page_urls = set(extract_redfin_urls(content))
            
            # If no URLs found, skip to next zipcode
            if not current_page_urls:
                print(f"No listings found on page {page}. Moving to next zipcode.")
                break
            
            # Check if we're seeing the same URLs as the previous page
            if current_page_urls == previous_page_urls:
                print(f"Duplicate page detected. Moving to next zipcode.")
                break
            
            # Store current page URLs for next iteration's comparison
            previous_page_urls = current_page_urls
            
            # Add new URLs to our set
            new_urls = current_page_urls - all_urls
            if new_urls:
                all_urls.update(new_urls)
                with open(urls_file, 'a') as f:
                    for url in new_urls:
                        f.write(url + '\n')
                print(f"Found {len(new_urls)} new URLs on page {page}")
            else:
                print("No new URLs found on this page")
            
            # Check if this is likely the last page (fewer than 40 listings)
            # While there can be a maximum of 9 pages, it is possible that Redfin 
            # does not have 9 pages worth of listings. If there aren't enough listings
            # to fill 9 pages, and we attempt to iterate to a new page that doesn't exist,
            # we will be redirected to the first page. To combat this, we check to see 
            # Number of listings available on the page, and if there are fewer than 40,
            # This indicates the end of the available listings for the ZIP code.
            if len(current_page_urls) < 40:
                print(f"Found {len(current_page_urls)} listings (< 40). This is the last page.")
                break
            
            # Sleep to respect rate limits
            time.sleep(12)
            
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            continue
    
    print(f"\nFound {len(all_urls)} total unique URLs in {zipcode}")
    return urls_file, list(all_urls)


def process_property_urls(api_key, input_file, db_path='redfin_properties.db'):
    """
    Process all Redfin URLs from the input file through ScraperAPI and save to SQLite 
    database.
    
    Args:
        api_key (str): ScraperAPI API key
        input_file (str): File containing Redfin URLs (one per line)
        db_path (str): Path to SQLite database file
    
    Returns:
        int: Number of URLs processed
        Updates the SQLite database with property details.
    """
    if not os.path.exists(input_file):
        print(f"Input file {input_file} not found")
        return
    
    # Initialize database and create tables
    init_database(db_path)
    
    # Get processed URLs from database
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT url FROM properties')
    processed_urls = {row[0] for row in c.fetchall()}
    conn.close()
    
    # Read and process URLs
    with open(input_file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    total_urls = len(urls)
    processed_count = 0
    
    for url in urls:
        if url in processed_urls:
            print(f"Skipping already processed URL: {url}")
            processed_count += 1
            continue
            
        print(f"Processing: {url} ({processed_count + 1}/{total_urls})")
        # Here we fetch the property details using the ScraperAPI function 
        details = fetch_property_details(url, api_key)
        
        # If details are found, store them in the database
        if details:
            store_property_data(details, db_path)
            processed_urls.add(url)
            processed_count += 1
            
        # Sleep to respect rate limits
        time.sleep(2)
    
    print(f"Processed {processed_count}/{total_urls} URLs for {input_file}")
    return processed_count


def fetch_property_details(url, api_key):
    """
    Fetch detailed property information from ScraperAPI's Redfin endpoint.
    
    Args:
        url (str): Redfin property URL
        api_key (str): ScraperAPI API key
        
    Returns:
        dict: Property details or None if request fails
    """

    # Format payload for ScraperAPI
    payload = {
        'api_key': api_key,
        'url': url,
        'output_format': 'json',
        'autoparse': 'true'
    }
    
    try:
        r = requests.get('https://api.scraperapi.com/structured/redfin/forsale', 
                        params=payload, 
                        timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Error fetching details for {url}: {str(e)}")
        return None


def store_property_data(details, db_path):
    """
    Store property data in SQLite database.
    
    Args:
        details (dict): Property details
        db_path (str): Path to SQLite database file
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        # Create table if it doesn't exist (as a safeguard from overwriting)
        # On the first couple scrapes, I did not have IF NOT EXISTS in the SQL query
        # and the table was overwritten. VERY FRUSTURATING. This safeguard prevents 
        # that from happening
        c.execute('''
            CREATE TABLE IF NOT EXISTS properties (
                url TEXT PRIMARY KEY,
                data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert or update property data
        c.execute('''
            INSERT OR REPLACE INTO properties (url, data)
            VALUES (?, ?)
        ''', (details['url'], json.dumps(details)))
        
        conn.commit()
    except Exception as e:
        print(f"Error storing property data: {str(e)}")
        conn.rollback()
    finally:
        conn.close()


def main():
    api_key = ''
    
    # Create directories to store URLs
    os.makedirs("urls", exist_ok=True)
    os.makedirs("urls/processed", exist_ok=True)
    
    # Initialize database at startup
    init_database('redfin_properties.db')
    
    total_processed = 0
    
    for zc in ZIPCODES:
        print(f"\n====== Working on ZIP: {zc} ======")
        urls_file, urls = scrape_zipcode(zc)

        if urls:
            print(f"Found {len(urls)} URLs in {zc}. Starting processing...")
            
            processed = process_property_urls(api_key, urls_file)
            total_processed += processed
            
            # Move processed file to a 'processed' directory
            try:
                os.rename(urls_file, f"urls/processed/{urls_file}")
                print(f"Moved {urls_file} to processed directory")
            except Exception as e:
                print(f"Error moving file: {str(e)}")
        else:
            print(f"No listings found for ZIP {zc}.")
    
    print(f"\nTotal URLs processed across all ZIP codes: {total_processed}")

if __name__ == "__main__":
    main()
