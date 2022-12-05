# chefkochScraper
A Python Scraper that scrapes recipies from chefkoch and saves them in a json file.
The spider used is a Crawl Spider which searches for and follows URLs to recipe pages.
The Crawl Spider does not have a limit of crawled items and thus crawls an unlimited number of recipies. To stop press CTRL + C.

## Results
Each recipe item is saved in a Python dictionary. Each recipe result includes following information:
* recipe_name
* recipe_url_id
* recipe_url
* portion_size
* rating_count
* rating_stars
* ingredients (amount and ingredient)

## CLI usage:
```
scrapy crawl chefkochScraper -o scraper.json
```
