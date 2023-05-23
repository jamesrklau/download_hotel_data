import json
from bs4 import BeautifulSoup
import time
import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
import argparse
import requests

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


def hotel_rooms_data(href_list):
    header = True  # Boolean flag to determine if the CSV header should be included

    for i in href_list:  # Iterate over the href_list
        try:
            re = requests.get("https://www.hotels.com/" + i[1])  # Send a GET request to retrieve hotel room data
            if len(re.text.split(" rooms")) == 1:  # Check if the response contains the string " rooms"
                unit_numbers = re.text.split(" units")[0].split('"')[-1]  # Extract the number of units from the response
            else:
                for j in re.text.split(" rooms"):  # Iterate over the response to find the section with unit numbers
                    if j.split('"')[-1].isdigit():  # Check if the string is a valid number
                        unit_numbers = j.split('"')[-1]  # Extract the number of units
            mode = mode = 'w' if header else 'a'  # Determine the file write mode based on the header flag
            unit_data_list = [i[0], unit_numbers]  # Create a list with hotel name and unit numbers
            print(unit_data_list)  # Print the unit data list
            final_dataframe = pd.DataFrame([unit_data_list], columns=['Hotel', 'Units'])  # Create a DataFrame with the unit data
            final_dataframe.to_csv("hotel_units_v2.csv", index=False, header=header, mode=mode, encoding='utf-8-sig')  # Write the DataFrame to a CSV file
            header = False  # Set the header flag to False for subsequent iterations
        except:
            pass  # Skip any errors and continue to the next iteration if an exception occurs


def hotel_data():
    new_rows = 0  # Counter to track the number of new rows
    url = f'https://www.hotels.com/Hotel-Search?adults=2&d1={today_date}&d2={end_date_str}&destination=Puerto%20Rico&endDate={end_date_str}&latLong=18.2137720732822%2C-66.49002120272635&regionId=148&selected=&semdtl=&sort=RECOMMENDED&startDate={today_date}&theme=&useRewards=false&userIntent='
    #url = 'https://www.hotels.com/Hotel-Search?adults=2&children=&d1=2023-02-21&d2=2023-03-03&destination=Puerto%20Rico&endDate=2023-04-16&latLong=&pwaDialog&regionId=148&semdtl=&sort=RECOMMENDED&startDate=2023-04-14&theme=&useRewards=false&userIntent='
    driver.get(url)  # Open the specified URL in the driver
    time.sleep(5)  # Wait for 5 seconds

    try:
        soup = BeautifulSoup(driver.page_source, "html.parser")  # Create a BeautifulSoup object from the driver's page source
        print(soup.find('div', class_='uitk-text uitk-type-start uitk-type-200 uitk-type-medium uitk-text-default-theme uitk-spacing uitk-spacing-padding-blockend-one').text)
        driver.find_element(By.XPATH, "//span[text()='Hotel']").click()  # Click on the 'Hotel' span element
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        print(soup.find('div', class_='uitk-text uitk-type-start uitk-type-200 uitk-type-medium uitk-text-default-theme uitk-spacing uitk-spacing-padding-blockend-one').text)
        driver.find_element(By.XPATH, "//span[text()='Hotel resort']").click()  # Click on the 'Hotel resort' span element
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        print(soup.find('div', class_='uitk-text uitk-type-start uitk-type-200 uitk-type-medium uitk-text-default-theme uitk-spacing uitk-spacing-padding-blockend-one').text)
    except:
        pass  # Skip any errors and continue to the next step

    time.sleep(5)
    for i in range(3):  # Loop three times to show more results
        try:
            time.sleep(5)
            driver.find_element(By.XPATH, "//button[text()='Show More']").click()  # Click on the 'Show More' button
            time.sleep(3)
            soup = BeautifulSoup(driver.page_source, "html.parser")
        except:
            break  # Break the loop if an exception occurs

    soup = BeautifulSoup(driver.page_source, "html.parser")
    href_list = []
    header = False
    for i in soup.find_all('div', class_="uitk-spacing uitk-spacing-margin-blockstart-three"):
        try:
            price = i.find('div', class_='uitk-text uitk-type-600 uitk-type-bold uitk-text-emphasis-theme').text
            hotel = i.find('h2', class_="uitk-heading uitk-heading-5 overflow-wrap").text
            geography = ''
            review_line = i.find_all('span', {'class': 'is-visually-hidden'})  # Find all spans with the class 'is-visually-hidden'
            for a in i.find_all('a', href=True):
                hotel_href = a['href']  # Extract the href attribute from the 'a' element
            href_list.append([hotel, hotel_href])  # Append hotel name and href to href_list
            for j in review_line:
                if 'out of' in j.text:
                    review_data = j.text.split(" ")
                    review_num = review_data[0]
                    try:
                        if review_data[4].startswith("("):
                            review_text = ''
                            number_of_reviews = review_data[4].split("(")[1]
                        else:
                            review_text = review_data[4]
                            number_of_reviews = review_data[5].split("(")[1]
                    except:
                        review_text = ''
                        number_of_reviews = ''
            hotel_list = [price, hotel, 'hotel.com', today_date, geography, review_num, review_text, number_of_reviews]
            final_dataframe = pd.DataFrame([hotel_list], columns=['Price', 'Hotel', 'Website', 'date', 'Geography', 'Review Score', 'Review Adjective', 'Number of Reviews'])
            final_dataframe['date'] = today_date
            mode = 'w' if header else 'a'
            final_dataframe.to_csv(args.datafile, index=False, header=header, mode=mode, encoding='utf-8-sig', storage_options=storage_options)
            header = False
            print(price, "", hotel)
            new_rows = new_rows + 1
        except:
            pass  # Skip any errors and continue to the next iteration

def booking_data():
    new_rows = 0  # Counter to track the number of new rows
    url = f'https://www.booking.com/searchresults.html?label=gen173nr-1DCAEoggI46AdIM1gEaLkBiAEBmAExuAEXyAEM2AED6AEB-AEDiAIBqAIDuAKI0amNBsACAdICJDZhMmQ3ZmVhLWNlNTUtNDc4ZC1hMmYwLTQwMWQwNGIxOWMzZdgCBOACAQ&sid=caca907e35d1bffb1f13d81f651d546d&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.html%3Flabel%3Dgen173nr-1DCAEoggI46AdIM1gEaLkBiAEBmAExuAEXyAEM2AED6AEB-AEDiAIBqAIDuAKI0amNBsACAdICJDZhMmQ3ZmVhLWNlNTUtNDc4ZC1hMmYwLTQwMWQwNGIxOWMzZdgCBOACAQ%3Bsid%3Dcaca907e35d1bffb1f13d81f651d546d%3Bsb_price_type%3Dtotal%26%3B&ss=puerto+rico%5C&is_ski_area=0&checkin_year={today_year}&checkin_month={today_month}&checkin_monthday={today_day}&checkout_year={today_year}&checkout_month={today_month}&checkout_monthday={end_day}&group_adults=1&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&ss_raw=p&search_pageview_id=d4b2663671c80085'
    driver.get(url)  # Open the specified URL in the driver
    time.sleep(5)  # Wait for 5 seconds

    soup = BeautifulSoup(driver.page_source, "html.parser")  # Create a BeautifulSoup object from the driver's page source
    time.sleep(3)
    print(soup.find("h1", {"class": "e1f827110f"}).text)  # Print the text of the 'h1' element with the specified class
    driver.find_element(By.XPATH, "//div[text()='Hotels']").click()  # Click on the 'Hotels' div element
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    total_count_txt = soup.find("h1", {"class": "e1f827110f"}).text  # Get the text of the 'h1' element with the specified class
    print(total_count_txt)
    print('div found: ', total_count_txt)
    total_count = [int(s) for s in total_count_txt.split() if s.isdigit()]  # Extract the integer from the text
    print('int extracted: ', total_count)
    page_num = round(total_count[0] / 25)  # Calculate the number of pages based on the total count
    print('page_num: ', page_num)
    header = False

    for j in range(page_num):  # Iterate through each page
        soup = BeautifulSoup(driver.page_source, "html.parser")
        # print('divs found on page ', j, ':', len(soup.findAll('div', {'class':'a826ba81c4'})))
        for i in range(len(soup.findAll('div', {'class': 'a826ba81c4'}))):  # Iterate through each hotel div on the page
            try:
                geography = soup.findAll('span', {'class': 'f4bd0794db b4273d69aa'})  # Find all span elements with the specified classes
                odd_index = geography[::2]  # Get odd-indexed elements from the list
                hotel = soup.findAll('div', {'class': 'fcab3ed991 a23c043802'})[i].text  # Get the text of the hotel div
                price = soup.findAll('span', {'class': 'fcab3ed991'})[i].text  # Get the text of the price span
                geography_edited = odd_index[i].text  # Get the text of the odd-indexed geography span
                review_num = soup.findAll('div', {'class': 'b5cd09854e d10a6220b4'})[i].text  # Get the text of the review number div
                review_text = soup.findAll('div', {'class': 'b5cd09854e f0d4d6a2f5 e46e88563a'})[i].text  # Get the text of the review text div
                number_of_reviews = soup.findAll('div', {'class': 'd8eab2cf7f c90c0a70d3 db63693c62'})[i].text  # Get the text of the number of reviews div
                hotel_list = [price, hotel, 'booking.com', today_date, geography_edited, review_num, review_text, number_of_reviews]  # Create a list of hotel data
                final_dataframe = pd.DataFrame([hotel_list], columns=['Price', 'Hotel', 'Website', 'date', 'Geography', 'Review Score', 'Review Adjective', 'Number of Reviews'])  # Create a DataFrame from the hotel list
                # print(final_dataframe)
                mode = 'w' if header else 'a'  # Set the mode to 'w' (write) if it's the first iteration, else 'a' (append)
                final_dataframe.to_csv(args.datafile, index=False, header=header, mode=mode, encoding='utf-8-sig', storage_options=storage_options)  # Write the DataFrame to a CSV file
                header = False
                print(price, "", hotel)
                new_rows = new_rows + 1
            except:
                # print('passed')
                pass

        time.sleep(5)
        driver.find_element(By.XPATH, '//button[@aria-label="Next page"]').click()  # Click the 'Next page' button
        time.sleep(5)
        j = j + 1

    return new_rows  # Return the number of new rows

parser = argparse.ArgumentParser(
    description="Booking.com Scraper"
)

parser.add_argument("-o", "--datafile", type=str, required=True, help="Booking.com data file name.")  # Add an argument for the data file name

parser.add_argument(
    "--log",
    type=lambda a: json.loads(a),
    help="Log results to log DB. Use LOG_API_URL environment variable to change url.",
)  # Add an argument for logging options

args = parser.parse_args()  # Parse the command-line arguments

storage_options = (
    {"key": AWS_ACCESS_KEY_ID, "secret": AWS_SECRET_ACCESS_KEY}  # Set storage options if the datafile starts with "s3://"
    if args.datafile.startswith("s3://")
    else None
)

headers = {'User-Agent': 'Mozilla/5.0'}  # Set the user agent for requests
today_date = time.strftime("%Y-%m-%d")  # Get the current date in the format "YYYY-MM-DD"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36"  # Set the user agent string
date_1 = datetime.datetime.strptime(today_date, "%Y-%m-%d")  # Convert the current date string to a datetime object
end_date = date_1 + datetime.timedelta(days=10)  # Add 10 days to the current date
end_date_str = end_date.strftime("%Y-%m-%d")  # Convert the end date to a string in the format "YYYY-MM-DD"

today_year = today_date[:4]  # Extract the year from the current date
today_month = today_date[5:7]  # Extract the month from the current date
today_day = today_date[8:10]  # Extract the day from the current date

end_year = end_date_str[:4]  # Extract the year from the end date
end_month = end_date_str[5:7]  # Extract the month from the end date
end_day = str(int(today_date[8:10]) + 1)  # Calculate the next day

all_hotel_data = pd.read_csv(
    args.datafile, storage_options=storage_options, on_bad_lines='skip'
)  # Read the hotel data from the specified data file

header = False  # Initialize a header variable to track if headers need to be written

print(f"------Data for {all_hotel_data['date'].iloc[-1]} already downloaded-------")  # Print a message indicating that data for the latest date has already been downloaded

dt = pd.Timestamp.now()  # Get the current timestamp
new_rows = 0  # Counter to track the number of new rows
error_count = 0  # Counter to track the number of errors

if all_hotel_data['date'].iloc[-1] != today_date:  # Check if data for the current date has already been downloaded
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)  # Initialize a Firefox WebDriver
    try:
        booking_row_count = booking_data()  # Scrape booking data and get the number of new rows
        new_rows += booking_row_count
    except:
        error_count += 1  # Increment the error count if an error occurs

    try:
        hotels_row_count = hotel_data()  # Scrape hotel data and get the number of new rows
        new_rows += hotels_row_count
    except:
        error_count += 1  # Increment the error count if an error occurs

    all_hotel_data = pd.read_csv(
        args.datafile, storage_options=storage_options, on_bad_lines='skip'
    )  # Read the updated hotel data from the data file

    all_hotel_data['Price'] = all_hotel_data['Price'].str.replace(r'\D', '')  # Remove non-digit characters from the "Price" column
    all_hotel_data.to_csv(args.datafile, index=False, encoding='utf-8-sig', storage_options=storage_options)  # Save the updated data to the data file

