# chefkochScraper
A Python Scraper that scrapes recipies from chefkoch and saves them in a json file.
The type of spider is a "Crawl Spider" which searches for URLs of recipe pages. The spider follows those and extracts information about recipies.
The Crawl Spider does not have a limit of crawled items and thus crawls an unlimited number of recipies. To stop, press CTRL + C.

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
