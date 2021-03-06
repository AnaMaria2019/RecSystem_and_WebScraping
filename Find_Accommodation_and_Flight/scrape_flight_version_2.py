from selenium import webdriver
import time
from bs4 import BeautifulSoup

""" Retrieve the Web Page """

from_airport = 'BUH'
to_airport = 'MIL'
from_date = '2020-11-20'
to_date = '2020-11-22'
url = 'https://www.momondo.ro/flight-search/{}-{}/{}/{}?sort=bestflight_a'.format(from_airport, to_airport, from_date, to_date)
reloads = 200  # set the number of times to reload
pause = 1.5    # initial time interval between reloads
opts = webdriver.FirefoxOptions()
opts.headless = True
driver = webdriver.Firefox(
    executable_path=
    "\\1_Ana\\3_Info\\11_Facultate\\1_Licenta\\Lucrare_de_Licenta\\1_Aplicatie\\RecSystem_and_WebScraping\\geckodriver.exe"
)

# Load Momondo.ro page
driver.get(url)
time.sleep(25)

driver.find_element_by_xpath(
    "//button[contains(@id, '-accept')]"
).click()
time.sleep(4)
page = driver.page_source
# driver.close()

""" Helper functions """


def string_to_int(s):
    n = 0
    for c in s:
        if c.isdigit():
            n = n * 10 + int(c)

    return n


def get_data_from_flight(flight):
    flight_depart_time = flight.find('span', {"class": "depart-time"}).get_text()
    flight_depart_time = flight_depart_time.replace('\n', '')
    flight_arrival_time = flight.find('span', {"class": "arrival-time"}).get_text()
    flight_arrival_time = flight_arrival_time.replace('\n', '')
    flight_company = flight.find('div', {"class": "bottom"}).get_text()
    flight_company = flight_company.replace('\n', '')

    return flight_depart_time, flight_arrival_time, flight_company


""" Start working with BeautifulSoup """

soup = BeautifulSoup(page, 'html.parser')

# print(soup)
flight_grid = soup.find_all('div', {"class": "inner-grid keel-grid"})
ind = 0
curr_flight = flight_grid[ind]
best = curr_flight.find('div', {"class": "bfLabel bf-best"})

""" Problem! There is not a best label at the best flight! """
while best is None:
    ind += 1
    curr_flight = flight_grid[ind]
    best = curr_flight.find('div', {"class": "bfLabel bf-best"})


flight = curr_flight.find_all('div', {"class": "result-column"})[0]
# print(flight)

flight1 = flight.find_all('div', {"class": "section times"})[0]
# print(flight1)
print()
print('For first flight:')
flight1_depart_time, flight1_arrival_time, flight1_company = get_data_from_flight(flight1)
print('Depart time: ', flight1_depart_time)
print('Arrival time:', flight1_arrival_time)
print('Company:', flight1_company)

flight2 = flight.find_all('div', {"class": "section times"})[1]
# print(flight2)
print()
print('For second flight:')
flight2_depart_time, flight2_arrival_time, flight2_company = get_data_from_flight(flight2)
print('Depart time: ', flight2_depart_time)
print('Arrival time:', flight2_arrival_time)
print('Company:', flight2_company)

price_span = curr_flight.find('span', id=lambda x: x and x.endswith('-price-text'))
price = price_span.get_text()
provider_name = curr_flight.find('span', {'class': "providerName"}).get_text().replace('\n', '')
print('Price {} using the provider {}'.format(price, provider_name))
link = curr_flight.find('a', id=lambda x: x and x.endswith('-booking-link'))
href = link['href']
book_flight_link = "https://www.momondo.ro/" + href
print(book_flight_link)
