#!/usr/bin/env python
# -*- coding: utf-8 -*-
import shutil
import csv
import os
import logging
from urllib.request import urlretrieve
from bs4 import BeautifulSoup

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)

# The url to scrape and the header of the table we want.
URL = "https://en.wikipedia.org/wiki/Road_safety_in_Europe"
TABLE_HEADER = "European Union Road Safety Facts and Figures"
HEADERS = ["Country", "Year", "Area", "Population", "GDP per capita",
           "Population density", "Vehicle ownership", "Total road deaths",
           "Road deaths per Million Inhabitants"]


if not os.path.exists("../data"):
    os.mkdir("../data")

if not os.path.exists("temp"):
    os.mkdir("temp")

cache = os.path.join("temp", "Road_safety_in_Europe.html")


def download_html():
    logger.info(f"Retrieving {URL}")
    urlretrieve(URL, cache)


def extract_table():
    logger.info("Starting data cleaning")
    page = open(cache, encoding="utf-8").read()
    soup = BeautifulSoup(page, 'html.parser')
    table_list = soup.find_all('table')
    table_list = [t for t in table_list if t.caption is not None]
    table = None

    # check for the right table
    for t in table_list:
        if str(t.caption.string).strip().lower() == TABLE_HEADER.lower():
            table = t.find_next('tbody')
            break


    # parse table
    rows = []
    data_rows = table.find_all('tr')

    for row in data_rows:
        country_data = [ele.text.strip() for ele in row.find_all('td')]
        if len(country_data) == 0:  # skip empty rows
            continue
        country_data.insert(1, "2018")      # insert year column
        country_data.pop(7)                 # remove raod length column
        country_data = country_data[:-2]    # remove last two columns

        # loop through each data point and clean
        for i in range(len(country_data)):
            # replace commas
            country_data[i] = country_data[i].replace(',', '')
            # remove brackets and everything in it
            if (index := country_data[i].find('(')) != -1:
                country_data[i] = country_data[i][:index].strip()
            # reomve '†'
            if (index := country_data[i].find('†')) != -1:
                country_data[i] = country_data[i][:index].strip()
            # faulty repr for Germany's population
            # fix all rows except where . is expected.
            if i != 0 and i != 2:
                country_data[i] = country_data[i].replace('.', '')
            
        rows.append(country_data)

    # sort by "Road deaths per Million Inhabitants"
    # located at the last index of each list.
    rows.sort(key=lambda x: x[-1])

    with open("../data/eu_road_safety.csv", 'w', newline="") as output:
        writer = csv.writer(output)
        writer.writerow(HEADERS)
        writer.writerows(rows)
    
    logger.info("Finished extracting data to data/ directory")

    logger.info("Deleting temp/ directory")
    shutil.rmtree("temp")
    logger.info("Finished deleting temp/ directory")

        
def main():
    download_html()
    extract_table()

if __name__ == '__main__':
    main()