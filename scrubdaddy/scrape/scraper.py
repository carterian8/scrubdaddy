#-------------------------------------------------------------------------------
# System Imports
#-------------------------------------------------------------------------------

import bs4
from datetime import datetime, timezone
import re
from selenium import webdriver
from selenium.webdriver import FirefoxOptions

#-------------------------------------------------------------------------------
# Local Imports
#-------------------------------------------------------------------------------

from . import database
from ..utils import logger

################################################################################
################################################################################
# ...
#
def run(args):
	"""
	"""

	# Create the logger...
	logr = logger.get_logger(__name__, level=args["log_level"])

	# Create the selenium webdriver...

	logr.info("Creating the webdriver...")
	opts = FirefoxOptions()
	opts.add_argument("--headless")
	driver = webdriver.Firefox(options=opts)

	# Get the page source HTML...

	logr.info("Geting the page source(s)...")
	driver.get("https://www.gunbroker.com/Ammunition/search")

	# Parse the source...

	soup = bs4.BeautifulSoup(driver.page_source, features="html.parser")
	for div in soup.findAll('div', class_=re.compile("listing\\s")):

		# Extract the url for the item...
		a = div.find("a", href=re.compile("/item/\\d+"))
		logr.debug("Extracting info for {}".format(a["href"]))

		# Get the HTML source for the item...
		driver.get("https://www.gunbroker.com{}".format(a["href"]))
		item_soup = bs4.BeautifulSoup(
			driver.page_source,
			features="html.parser"
		)

		# Extract product information...

		timestamp = datetime.now(timezone.utc).strftime("%d-%m-%Y_%H:%M:%S%z")
		sold = (item_soup.find("div", class_="alert sold-item") is not None)
		item_id = None
		price = None
		manufacturer = None
		model = None
		calibur = None
		num_rounds = None
		buying_format = None
		listing_details = None
		condition = None
		min_bid = None
		bid_count = None

		# Load into DB...


	# Clean up...

	driver.close()

