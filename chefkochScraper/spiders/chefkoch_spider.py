from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import ChefkochScraperItem
import logging

class ChefkochSpider(CrawlSpider):

    # Set basic info.
    name = "chefkochScraper"
    allowed_domains = ["chefkoch.de"]
    start_urls = ['https://www.chefkoch.de/rs/s0/Rezepte.html']
    logging.basicConfig(filename="scraping_log.txt", level=logging.DEBUG)

    # Define rules for the crawlspider.
    rules = (
        Rule(LinkExtractor(allow="chefkoch.de/rezepte/"), callback="parse_item"),
    )

    def parse_item(self, response):

        # Return back to recipe page upon 404.
        if response.status == 404:
            yield response.follow("https://www.chefkoch.de/rezepte/", callback=self.parse_item)


        # Exclude subscription-based recipies.
        exclude_plus_recipies = response.css('.plus-subscription-card').get()
        if not exclude_plus_recipies:

            # Create new recipe item.
            recipe = ChefkochScraperItem()

            # Get data.
            recipe_name = response.css('.recipe-header > div > h1::text').get()

            # Only continue to scrape if there is a recipe name.
            if recipe_name:
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
                    ingredient_volume = " ".join(ingredient_volume.split())
                    ingredient_name = ingredient_name.replace(' ', '')
                    ingredient[ingredient_name] = ingredient_volume
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

                # Find next url on page.
                next_url = response.css('a[href^="https://www.chefkoch.de/rezepte/"]').get()
                logging.info("NEXT URL: " + next_url)

                # Go to next page, is there is non, return to recipe overview page.
                if next_url is not None:
                    yield response.follow(next_url, callback=self.parse_item)
                else:
                    yield response.follow("https://www.chefkoch.de/rezepte/", callback=self.parse_item)
