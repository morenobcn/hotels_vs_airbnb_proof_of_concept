from selenium import webdriver
from scrapy import Spider, Request
import time
import re
import csv


#First we need to specifu where the webdriver is, we will be using Chrome
#all the options are to avoid errors
#the prefs means we wont be loading images which will speed up the process a lot
#the second set of options is to avoid some errors I found during the process

chromeOptions = webdriver.ChromeOptions()
prefs = {'profile.managed_default_content_settings.images':2}
chromeOptions.add_experimental_option("prefs", prefs)
chromeOptions.add_argument('--ignore-certificate-errors')
chromeOptions.add_argument('--ignore-ssl-errors')
chromeOptions.add_argument('--user-agent="Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 640 XL LTE) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10166"')

driver = webdriver.Chrome(r'C:\Users\natxo\git_proj\chromedriver.exe',chrome_options=chromeOptions)




# Go to the page that we want to scrape
driver.get("https://www.tripadvisor.com/Hotels-g187497-oa390-Barcelona_Catalonia-Hotels.html")

#we save this opened window as the first tab
window_before = driver.window_handles[0]
#print (window_before)


#Click the Hotels buttons to make sure we just get back the hotels
hotels_button = driver.find_element_by_xpath('//div[@data-tracker="HOTEL"]')
hotels_button.click()

time.sleep(3)


##### How to select the dates ###

#Lets pick the dates, we first open the calendar
check_in_button = driver.find_element_by_xpath('//div[@class="picker-body"][1]')
check_in_button.click()
time.sleep(3)

#we navigate in the calendar pick for the next month, we will to click this button as many times as necessary depending on how far 
#we are picking the month
next_month_button = driver.find_element_by_xpath('//div[@class="rsdc-next rsdc-nav ui_icon single-chevron-right"]')
next_month_button.click()
time.sleep(2)
next_month_button.click()
time.sleep(2)

#And then we pick a date
check_in_date = driver.find_element_by_xpath('//span[@data-date="2018-10-22"]')
check_in_date.click()

time.sleep(8)





# Page index used to keep track of where we are.
number_of_pages = driver.find_element_by_xpath('//a[@class="pageNum last taLnk "]').text
number_of_pages = int(number_of_pages)
print(number_of_pages)
index = 1



# CSV where we will be saving all of our data
csv_file = open('hotel_list.csv', 'w', newline ='')
writer = csv.writer(csv_file)


# We want to start the first two pages.
# If everything works, we will change it to while True



while index <= number_of_pages:
	try:
		print("Scraping Page number " + str(index) + ' of ' + str(number_of_pages))
		print('='*50)
		index = index + 1
		# Find all the reviews. The find_elements function will return a list of selenium select elements.
		# Check the documentation here: http://selenium-python.readthedocs.io/locating-elements.html
		h_list = driver.find_elements_by_xpath('//div[@class="prw_rup prw_meta_hsx_responsive_listing ui_section listItem"]')
		


		for hotel in h_list:
			
			#now we run within each page to look for all the hotels and its main characteristics, name, price, and so
			hotel_dict = {}


			#There is always name of the hotel
			h_name= hotel.find_element_by_xpath('.//div[@class="listing_title"]/a').text #we use relative paths here now
			h_link = hotel.find_element_by_xpath('.//div[@class="listing_title"]/a').get_attribute('href')
						
			
			#To consider also hotels wihtout price or nay other type of informnation we use try statements
			try:
				h_price = hotel.find_element_by_xpath('.//div[@data-sizegroup="mini-meta-price"]').text
				# h_price = $198 or $1,065
				h_price = list(map(lambda x: int(x), re.findall('\d', h_price)))
				h_price = int(''.join(map(str, h_price)))
			except:
				h_price = 'NaN' 

			try:
				h_rating = hotel.find_element_by_xpath('.//div[@class="info-col"]//span').get_attribute('alt')
				#h_rating = 4.5 of 5 bubbles
				h_rating = float(h_rating.replace(' of 5 bubbles',''))
			except:
				h_rating = 'NaN'

			try:
				h_total_reviews = hotel.find_element_by_xpath('.//a[@class="review_count"]').text
				#h_total_reviews = 1,553 reviews
				h_total_reviews = list(map(lambda x: int(x), re.findall('\d', h_total_reviews)))
				h_total_reviews = int(''.join(map(str, h_total_reviews)))
			except:
				h_total_reviews = 'NaN'

			try:
				h_rank = hotel.find_element_by_xpath('.//div[@class="popindex"]').text
				#h_rank = #30 Best Value of 518 hotels in Barcelona
				h_rank = h_rank.split(' ',1)[0]
				h_rank = int(h_rank.replace('#', ''))
			except:
				h_rank = 'NaN'
			
			#Lets save all this data into our dictionary

			hotel_dict['Hotel Name'] = h_name
			hotel_dict['Price (USD)'] = h_price
			hotel_dict['Number of reviews'] = h_total_reviews
			hotel_dict['Reviews rating (out of 5)'] = h_rating
			hotel_dict['Ranking (best value)'] = h_rank
			hotel_dict['Hotel Link'] = h_link


			#save each row with all the data in the csv file we created
			writer.writerow(hotel_dict.values())

		# Locate the next button element on the page and then call `button.click()` to click it.
		try:
			next_button = driver.find_element_by_xpath('//a[@class="nav next taLnk ui_button primary"]')
			#We use this method of clicking cos the original one nex_button.click() gave me error
			driver.execute_script("arguments[0].click();", next_button)
			time.sleep(10)

		except:
			print('You sucessfullly scraped all the hotels from the list')
		
		

	except Exception as e:
			print(e)
			csv_file.close()
			driver.close()
			driver.quit()
			break




