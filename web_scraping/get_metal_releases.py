from datetime import datetime, date
import requests
import re

from bs4 import BeautifulSoup
import pandas as pd

def retrieve_data(url):

    #Send a GET request to the webpage
    response = requests.get(url)

    #Check if the request was successful (status code 200)
    if response.status_code == 200:
        #Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        #Find the table containing the releases
        table = soup.find('table', class_='table')

        #Check if the table was found
        if table:
            #Initialize lists to store data
            dates = []
            bands = []
            releases = []
            release_types = []
            genres = []

            #Find all rows in the table
            rows = table.find_all('tr')

            #Iterate over each row and extract data
            for row in rows:
                #Find all cells in the row
                cells = row.find_all('td')

                #Extract and append data to respective lists
                if len(cells) == 2:  # Ensure it's a valid row with data
                    date = cells[0].get_text(strip=True)
                    band_release = cells[1].get_text(strip=True).split(' - ', 1)
                    band = band_release[0]
                    release_match = re.search(r' - (.+?)\[', cells[1].get_text(strip=True))
                    release = release_match.group(1) if release_match else None
                    release_type_tag = cells[1].find('div', class_='col-md-1')
                    release_type = release_type_tag.get_text(strip=True) if release_type_tag else None
                    genre_tag = cells[1].find('div', class_='col-md-4')
                    genre = genre_tag.get_text(strip=True) if genre_tag else None

                    #Append data to lists
                    dates.append(date)
                    bands.append(band)
                    releases.append(release)
                    release_types.append(release_type)
                    genres.append(genre)

            #Create DataFrame
            data = {
                'Date': dates,
                'Band': bands,
                'Release': releases,
                'Release Type': release_types,
                'Genre': genres
            }
            df = pd.DataFrame(data)
            return df
        else:
            print("Table not found.")
            return None
    else:
        print("Failed to retrieve webpage.")
        return None

def clean_data(df):

    #Remove any leading and trailing whitespaces
    df['Date'] = df['Date'].str.strip()
    df['Band'] = df['Band'].str.strip()
    df['Release'] = df['Release'].str.strip()
    df['Release Type'] = df['Release Type'].str.strip()
    df['Genre'] = df['Genre'].str.strip()

    #Remove square brackets from Release Type column
    df['Release Type'] = df['Release Type'].str.replace(r'\[(.*?)\]', r'\1', regex=True)
    df['Release Type'] = df['Release Type'].str.replace('Studio', 'Studio Album')

    #Fix Date column and filter the DataFrame to keep only rows with today's date
    df['Date'] = df['Date'].apply(lambda x: '2024-' + x.split('.')[1].zfill(2) + '-' + x.split('.')[0].zfill(2))
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.date
    today = date.today()
    df = df[df['Date'] == today]

    return df

#URL of the webpage to scrape
url = 'https://metalstorm.net/events/new_releases.php?page=1'

# Retrieve data and create DataFrame
df = retrieve_data(url)
cleaned_df = clean_data(df)

#Send to my dropbox
today = date.today()
file_name = f"C:\\Users\\jibso\\Dropbox\\new_metal_releases_{today}.csv"
cleaned_df.to_csv(file_name, index=False)