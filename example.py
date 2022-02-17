from csu.scraper import CSUUtilityScraper
import os

username=os.getenv("CSU_USERNAME")
password=os.getenv("CSU_PASSWORD")
if __name__ == "__main__":
    c = CSUUtilityScraper(username=username, password=password)
    c.get_gas()
