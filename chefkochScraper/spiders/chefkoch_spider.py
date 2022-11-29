import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import ChefkochScraperItem

class ChefkochSpider(scrapy.Spider):
    name = "chefkochScraper"

    def start_requests(self):
        urls = [
            'https://www.chefkoch.de/rezepte/3657421550672396/One-Pot-Spaetzle-mit-Raeuchertofu.html'
        ]
        allowed_domains = ['chefkoch.de/rezepte/']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        # Create new recipe item.
        recipe = ChefkochScraperItem()

        # Get data.
        recipe_name = response.css('.recipe-header > div > h1::text').get()
        recipe_url = response.request.url
        recipe_url_id = str.split(recipe_url, '/')[-2]
        portion_size = response.css('.recipe-servings > form > input::attr(value)').get()
        rating_count = response.css('.bi-recipe-rating--closed > div.ds-rating-count > span > span:not([class^="rds-only"])::text').get()
        rating_stars = response.css('.bi-recipe-rating--closed > div.ds-rating-avg > span > strong::text').get()

        # Get ingredients and quantity.
        ingredients = []
        for row in response.css('.ingredients.table-header > tbody > tr'):
            ingredient = {}
            ingredient_volume = row.css('.td-left ::text').get()
            if ingredient_volume is None:
                ingredient_volume = ""
            ingredient_name = row.css('.td-right > span::text').get()
            if not ingredient_name:
                ingredient_name = row.css('.td-right > span > a::text').get()

            # Save each ingredient and its quantity in a dictionary. Append to ingredient list.
            ingredient_name = " ".join(ingredient_volume.split())
            ingredient_name = ingredient_name.replace(' ', '')
            ingredient[ingredient_name] = ingredient_name
            ingredients.append(ingredient)

        # Fill recipe item with scraped data.
        recipe['recipe_name'] = recipe_name
        recipe['recipe_url_id'] = recipe_url_id
        recipe['recipe_url'] = recipe_url
        recipe['portion_size'] = portion_size
        recipe['rating_count'] = rating_count
        recipe['rating_stars'] = rating_stars
        recipe['ingredients'] = ingredients

        yield recipe




