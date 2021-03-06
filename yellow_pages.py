#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import html
import unicodecsv as csv
import argparse

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
					print(scraped_results)
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

	if scraped_data:
		print("Writing scraped data to %s-%s-yellowpages-scraped-data.csv"%(keyword,place))
		with open('%s-%s-yellowpages-scraped-data.csv'%(keyword,place),'wb') as csvfile:
			fieldnames = ['business_name','website']
			writer = csv.DictWriter(csvfile,fieldnames = fieldnames,quoting=csv.QUOTE_ALL)
			writer.writeheader()
			for data in scraped_data:
				writer.writerow(data)
