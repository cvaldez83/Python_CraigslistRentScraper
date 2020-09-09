# Python_CraigslistRentScraper
Scrapes craigslist posts for rental properties

## Setup
1. setup python environment and install dependencies shown in requirements.txt
2. edit the 'cities' python list inside of the config.py file with the names of the cities you're interested in scraping
   * Note: city names need to be the same as craigslist shows in url (e.g. sandiego for https://sandiego.craigslist.org)

### Crontab command to run on the 1st of every month at 4 am
0 4 1 * * /home/<your_username>/Python_CraigslistRentScraper/venv/bin/python /home/<your_username>/Python_CraigslistRentScraper/main.py

### Crontab command to run once a day at 4am
0 4 * * * /home/<your_username>/Python_CraigslistRentScraper/venv/bin/python /home/<your_username>/Python_CraigslistRentScraper/main.py
