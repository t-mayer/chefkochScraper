# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChefkochScraperItem(scrapy.Item):
    recipe_name = scrapy.Field()
    recipe_url_id = scrapy.Field()
    recipe_url = scrapy.Field()
    portion_size = scrapy.Field()
    rating_count = scrapy.Field()
    rating_stars = scrapy.Field()
    ingredients = scrapy.Field()
