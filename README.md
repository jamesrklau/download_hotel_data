
# Booking.com Scraper
This script is designed to scrape hotel data from the websites hotels.com and booking.com. It retrieves information such as prices, hotel names, review scores, and the number of reviews and stores it in a CSV file.

# Prerequisites
Python 3.6 or higher
Libraries: json, bs4, time, datetime, pandas, selenium, webdriver_manager, argparse, requests
# Installation
Clone the repository or download the script.
Install the required libraries using pip:
```
Copy code
pip install beautifulsoup4 pandas selenium webdriver_manager requests
```

#Usage
Run the script from the command line with the following options:
```
php
Copy code
python scraper.py -o <datafile>
```
-o, --datafile: Specify the name of the data file where the scraped data will be stored. This argument is required.
# Notes
Before running the script, make sure to set the following environment variables:
AWS_ACCESS_KEY_ID: Access key ID for AWS (if using S3 storage)
AWS_SECRET_ACCESS_KEY: Secret access key for AWS (if using S3 storage)
The script uses Selenium with Firefox webdriver to interact with the websites. Make sure you have the latest version of Firefox installed, or update the webdriver accordingly.
The script retrieves hotel data from hotels.com and booking.com. You can modify the URLs in the script to scrape data for different locations or dates.
The scraped data includes hotel prices, names, websites, dates, geography, review scores, review adjectives, and the number of reviews. The data is stored in a CSV file specified by the datafile argument.
The script prints the scraped data to the console as well.
# Examples
Scrape hotel data from booking.com and store it in a file named booking_data.csv:
```
Copy code
python scraper.py -o booking_data.csv
```
Scrape hotel data from hotels.com and store it in a file named hotels_data.csv:
```
Copy code
python scraper.py -o hotels_data.csv
```
Please note that the script may take some time to run, depending on the number of hotels and pages to scrape.