

import scrapy


class TripadvisorItem(scrapy.Item):
	h_link = scrapy.Field()
	h_address = scrapy.Field()
	h_star = scrapy.Field()
	h_ranking_users = scrapy.Field()
	r_excellent = scrapy.Field()
	r_very_good = scrapy.Field()
	r_average = scrapy.Field()
	r_poor = scrapy.Field()
	r_terrible = scrapy.Field()
