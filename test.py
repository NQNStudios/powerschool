from bs4 import *

with open("test.html") as page:
	soup = BeautifulSoup(page)

print(soup.prettify())