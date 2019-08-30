from web_scraping import Scrape

chrome_driver = "::/"  # Chrome Driver filepath for webdriver
mysql_user = "root"  # MySQL username
mysql_passwd = ""  # MySQL password
mysql_db = "test"  # MySQL database

# Create Scrape object

scraper = Scrape(chrome_driver, mysql_user, mysql_passwd, mysql_db)

# Scrape example using single artist

scraper.withArtist("greenday", "punk")

# Scrape example using a dictionary

example_dict = {
    "pop": [
        "rihanna", "sia", "knowles"
    ],
    "rock": [
        "acdc", "nirvana", "queen"
    ]
}

scraper.withDictionary(example_dict)
