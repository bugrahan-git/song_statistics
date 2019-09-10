import mysql.connector
from web_scraping import Scrape


db = mysql.connector.connect(
                host="localhost",
                user="root",		# MySQL username
                passwd="",		# MySQL password
                database="test" 	# Database name
            )

chrome_driver = "::/"  # Chrome Driver path for webdriver

# Create Scrape object

scraper = Scrape(chrome_driver, db)

# Scrape example using single artist

scraper.scrape_artist("greenday", "punk")

# Scrape example using a dictionary

example_dict = {
    "pop": [
        "rihanna", "sia", "knowles"
    ],
    "rock": [
        "acdc", "nirvana", "queen"
    ]
}

scraper.scrape_dictionary(example_dict)
