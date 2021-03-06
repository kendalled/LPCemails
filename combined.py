# Kendall Jackson MIT License
# GetScraped Private v1
#parse_listing from https://github.com/scrapehero/yellowpages-scraper

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyautogui as pgui
import time
import requests
from lxml import html
import unicodecsv as csv
import argparse
import clipboard

clipboard.copy('')
categories = ['Active Life', 'Entertainment', 'Automotive', 'Beauty', 'Education', 'Event Planning & Services', 'Financial Services', 'Food', 'Health & Medical', 'Home Services', 'Hotels & Travel', 'Local Flavor', 'Local Services', 'Nightlife', 'Pets', 'Professional Services', 'Public Services & Government', 'Real Estate', 'Religious Organizations', 'Restaurants', 'Shopping']

def parse_listing(keyword,place):
    """

    Function to process yellowpage listing page
    : param keyword: search query
    : param place : place name

    """
    url = "https://www.yellowpages.com/search?search_terms={0}&geo_location_terms={1}".format(keyword,place)
    print("retrieving ",url)

    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language':'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'Host':'www.yellowpages.com',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
            }
    # Adding retries
    for retry in range(10):
        try:
            response = requests.get(url,verify=False, headers = headers )
            print("parsing page")
            if response.status_code==200:
                parser = html.fromstring(response.text)
                #making links absolute
                base_url = "https://www.yellowpages.com"
                parser.make_links_absolute(base_url)

                XPATH_LISTINGS = "//div[@class='search-results organic']//div[@class='v-card']"
                listings = parser.xpath(XPATH_LISTINGS)
                scraped_results = []

                for results in listings:
                    XPATH_BUSINESS_NAME = ".//a[@class='business-name']//text()"

                    XPATH_WEBSITE = ".//div[@class='info']//div[contains(@class,'info-section')]//div[@class='links']//a[contains(@class,'website')]/@href"

                    raw_business_name = results.xpath(XPATH_BUSINESS_NAME)

                    raw_website = results.xpath(XPATH_WEBSITE)


                    business_name = ''.join(raw_business_name).strip() if raw_business_name else None

                    website = ''.join(raw_website).strip() if raw_website else None





                    business_details = {
                                        'business_name':business_name,

                                        'website':website

                    }
                    scraped_results.append(business_details)

                #print(scraped_results)
                return scraped_results

            elif response.status_code==404:
                print("Could not find a location matching",place)
                #no need to retry for non existing page
                break
            else:
                print("Failed to process page")
                return []

        except:
            print("Failed to process page")
            return []


if __name__=="__main__":

    argparser = argparse.ArgumentParser()
    argparser.add_argument('keyword',help = 'Search Keyword')
    argparser.add_argument('place',help = 'Place Name')

    args = argparser.parse_args()
    keyword = args.keyword
    place = args.place
    scraped_data =  parse_listing(keyword,place)

    urls = []
    emails = []
    res = ''
    real_results = []
    end_results = []

    for j in range(len(scraped_data)):
        if(scraped_data[j].get('website') != None):
            urls.append(scraped_data[j].get('website'))
            details = {
                'business': scraped_data[j].get('business_name'),
                'email': ''
                }
            real_results.append(details)
    for i in range(len(urls)):

        # Click url bar
        pgui.click(1358,93)
        time.sleep(.55)

        # typewrite url
        pgui.typewrite(urls[i])
        time.sleep(0.25)

        pgui.press('\n')
        time.sleep(6.00)

        # Click extension
        pgui.click(2464, 82)
        time.sleep(.75)
        # Click copy all
        pgui.click(2423, 197)
        time.sleep(0.5)
        if(clipboard.paste()[0:clipboard.paste().find('.')+4] == res):
            emails.append(None)
            continue
        else:

            res = clipboard.paste()[0:clipboard.paste().find('.')+4]
            print(res)

            emails.append(res)


        # Rinse & Repeat
        pgui.click(1241, 53)
        time.sleep(0.15)

    for ind, email in enumerate(emails):
        real_results[ind]['email'] = email

    for ig in real_results:
        if(ig['email'] != None):
            end_results.append(ig)




    print(end_results)


    if scraped_data:
        print("Writing scraped data to %s-%s-yellowpages-scraped-emailsFINAL.csv"%(keyword,place))
        with open('%s-%s-yellowpages-scraped-emailsFINAL.csv'%(keyword,place),'wb') as csvfile:
            fieldnames = ['business', 'email']
            writer = csv.DictWriter(csvfile,fieldnames = fieldnames,quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for data in end_results:
                writer.writerow(data)





    print('Done! check the google doc.')
