from bs4 import BeautifulSoup
from scrapingant_client import ScrapingAntClient

import pandas as pd
from datetime import datetime
import os

output_folder = os.path.join('C:/', 'Users', 'Alex', 'Documents')

# scrape today's bookings
today_date = datetime.now().date().strftime('%Y-%m-%d')
print("scraping today's booking: ", today_date)

# spaces
spaces = {66460: '5980 McLaughin',
          36149: '78 Martin Ross',
          39456: '1225 Kennedy',
          64892: '1698 Bayly'
         }

# not secure to store like this lol
token="APIKEY"

def get_url(today_date, spaceid):
    url = f'https://skedda.com/booking?spaceviewid={spaceid}&viewdate={today_date}'
    return url

def get_page_content(url, token, bookings_placeholder, spaceid):
    # every time we make this call, it uses 10 API credits; we get 10k credits each month
    client = ScrapingAntClient(token=token)
    page_content = client.general_request(url).content
    
    # everything below we're just extracting info from returned page_content
    soup = BeautifulSoup(page_content)
    
    # if things break, this pattern probably changed
    results = soup.find(id="ember-root-element")
    time_results = results.find_all(name="span", class_="fw-semi-bold")
    
    for time in time_results:
        bookings.append((time.text, spaceid))
        
    return bookings

def format_datatable(bookings):
    booking_df = pd.DataFrame(bookings, columns=['times', 'spaceid'])
    booking_df['space'] = booking_df['spaceid'].replace(spaces)
    booking_df[['start_time', 'end_time']] = booking_df['times'].str.split('–', 1, expand=True)
    booking_df['start_time'] = pd.to_datetime(booking_df['start_time'])
    booking_df['end_time'] = pd.to_datetime(booking_df['end_time'])
    return booking_df

# loop through all spaces
bookings = []
for spaceid in spaces:
    url = get_url(today_date=today_date, spaceid=spaceid)
    print("got url for", spaceid, spaces.get(spaceid))
    bookings = get_page_content(url=url, token=token, bookings_placeholder=bookings, spaceid=spaceid)
    print("finished scraping", spaceid, spaces.get(spaceid))

booking_df = format_datatable(bookings)

booking_df.to_csv(os.path.join(output_folder, f'scraped_{today_date}.csv'), index=False)
print("file saved")