#-------------------------------------------------------------------------------
# System Imports
#-------------------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver import FirefoxOptions

#-------------------------------------------------------------------------------
# Local Imports
#-------------------------------------------------------------------------------

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
	driver.get("http://www.python.org")
	driver.get("https://docker-curriculum.com/#docker-on-aws")

	# Parse the source...

	# Load into DB...


	# Clean up...

	driver.close()

