#-------------------------------------------------------------------------------
# System Imports
#-------------------------------------------------------------------------------

import bs4
from datetime import datetime, timezone
import demjson
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
	for div in soup.findAll('div', class_=re.compile(r"listing\s")):

		# Extract the url for the item...
		a = div.find("a", href=re.compile(r"/item/\d+"))
		logr.debug("Extracting info for {}".format(a["href"]))

		# Get the HTML source for the item...
		driver.get("https://www.gunbroker.com{}".format(a["href"]))
		item_soup = bs4.BeautifulSoup(
			driver.page_source,
			features="html.parser"
		)

		# Find specific script tag containing the info...

		product_info_regex = r"""
			.+dataLayer\.push\((\s+)?(?P<json>{(\s+)?item:(\s+)?{(\s+).+}).+
		"""
		script_tag = item_soup.find(
			"script", 
			text=re.compile(product_info_regex, re.VERBOSE)
		)
		
		err_str = "Script tag not extracted for {}".format(a["href"])
		if script_tag:
			script_tag_text = "".join(script_tag.contents)
			product_info_pattern = re.compile(product_info_regex, re.VERBOSE)
			match = product_info_pattern.search(script_tag_text)
			err_str = "No match found for script tag text {}".format(a["href"])
			
		if match is None:
			logr.error(err_str)
			continue

		# Extract product information...

		num_rounds_div = item_soup.find("div", id="divICValue_NumberOfRounds")

		item_js_dict = demjson.decode(match.group("json"))
		product_info = dict()
		product_info["timestamp"] 		= datetime.now(timezone.utc).strftime("%Y-%m-%d_%H:%M:%S%z")
		product_info["sold"] 			= (item_soup.find("div", class_="alert sold-item") is not None)
		product_info["item_id"] 		= item_js_dict["item"]["itemID"]
		product_info["category_id"]		= item_js_dict["item"]["categoryID"]
		product_info["price_usd"] 		= item_js_dict["item"]["price"]
		product_info["manufacturer"] 	= item_js_dict["item"]["manufacturer"]
		product_info["model"] 			= None
		product_info["caliber"] 		= item_js_dict["item"]["caliber"]
		product_info["num_rounds"] 		= num_rounds_div["title"] if num_rounds_div else None
		product_info["buying_format"] 	= None # Auction or not
		product_info["listing_details"] = None # More elaborate
		product_info["condition"] 		= None # Condition is only a number
		product_info["min_bid"] 		= None # necessary?
		product_info["bid_count"]		= None # necessary?

		logr.debug(product_info)
		break

		# Load into DB...


	# Clean up...

	driver.close()

