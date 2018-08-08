import scrapy
from scrapy import Spider, Request
from tripadvisor.items import TripadvisorItem
import re
import pandas as pd

#Important!! Make sure the name of this class not the same as the TripadvisorItem (otherwise youget item error)
class TripadvisorSpiderItem(scrapy.Spider): 
	name = 'tripadvisor_spider'
	allowed_domains = ['tripadvisor.com']
	start_urls = ['https://www.tripadvisor.com/Hotel_Review-g187497-d228507-Reviews-Barcelo_Sants-Barcelona_Catalonia.html']

	def parse(self, response):
	
		#first thing we need to do is to load all the links from the hotels that we got from selenium
		hotels = pd.read_csv(r'C:\Users\natxo\OneDrive\4_NYCDSA\4_NYCDSA_Bootcamp\0_Projects\2_Scraping\Scraping\tripadvisor_scrapy\Full Hotel list with Links.csv', header=None, names = ['Hotel Name', 'Price (USD)', 'Number of reviews', 'Reviews rating (out of 5)','Ranking (best value)','Link'])
		

		hotels_urls = hotels.Link.tolist()
		

		# Yield the requests to different search result urls, 
		# using parse_result_page function to parse the response.
		for url in hotels_urls:
			
			print(url)
			
			yield Request(url=url, callback=self.parse_hotel_page)




	def parse_hotel_page(self, response):


		#First the address
		try:
			h_street = response.xpath('//span[@class="detail"]/span[1]/text()').extract_first()
			h_locality = response.xpath('//span[@class="detail"]/span[2]/text()').extract_first()
			h_country = response.xpath('//span[@class="detail"]/span[3]/text()').extract_first()
			h_address = h_street + str(' , ') + h_locality + h_country
		except:
			h_address = 'NaN'

		#print(h_address)
				
		#More info about the hotel itself
		try:
			h_star = response.xpath('//div[@data-element=".starContents"]/@class').extract_first()
			#h_star = ui_star_rating star_40
			h_star = re.findall(r'\d{2}', h_star) #finds two digits
			h_star = (float(''.join(map(str, h_star))))/10 #divides by 10 and to float
		except:
			h_star = 'NaN'
		
		try:
			h_ranking_users = response.xpath('//b[@class="rank"]/text()').extract_first()
			#h_ranking_users = #181
			h_ranking_users = int(h_ranking_users.replace('#',''))
		except:
			h_ranking_users = 'NaN'

		
		#and indpeth reviews information

		try:
			r_excellent = response.xpath('//div[@data-tracker="Excellent"]/span[2]/text()').extract_first()
			r_very_good = response.xpath('//div[@data-tracker="Very good"]/span[2]/text()').extract_first()
			r_average = response.xpath('//div[@data-tracker="Average"]/span[2]/text()').extract_first()
			r_poor = response.xpath('//div[@data-tracker="Poor"]/span[2]/text()').extract_first()
			r_terrible = response.xpath('//div[@data-tracker="Terrible"]/span[2]/text()').extract_first()

			#we reformat the results
			r_excellent = int(r_excellent.replace(',',''))
			r_very_good = int(r_very_good.replace(',',''))
			r_average = int(r_average.replace(',',''))
			r_poor = int(r_poor.replace(',',''))
			r_terrible = int(r_terrible.replace(',',''))
		except:
			r_excellent = 'NaN'
			r_very_good = 'NaN'
			r_average = 'NaN'
			r_poor = 'NaN'
			r_terrible = 'NaN'


		#print(r_excellent)

		item = TripadvisorItem()
		item['h_address'] = h_address
		item['h_star'] = h_star
		item['h_ranking_users'] = h_ranking_users
		item['r_excellent'] = r_excellent
		item['r_very_good'] = r_very_good
		item['r_average'] = r_average
		item['r_poor'] = r_poor
		item['r_terrible'] = r_terrible
		item['h_link'] = response.url



		yield item 



