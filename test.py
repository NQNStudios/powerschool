from bs4 import *


class Assignment:

	def __init__(self, name, category, earned, possible):
		self.name = name
		self.category = category
		self.earned = self._parse_int(earned)
		self.possible = self._parse_int(possible)

	@staticmethod
	def _parse_int(string):
		return int(string) if string.isnumeric() else None

	@property
	def _is_null(self):
		return self.earned is None

	@property
	def percentage(self):
		if self._is_null:
			return None
		return 100 * self.earned / self.possible

	def __str__(self):
		earned = "--" if self._is_null else self.earned
		percentage = "--" if self._is_null else self.percentage 
		return "<{} in {}, {}/{} ({}%)>".format(self.name, self.category, earned, self.possible, percentage)


with open("test.html") as page:
	soup = BeautifulSoup(page)

grades = soup.find(id="content-main").find_all("table")[-1].find_all("tr")[1:] # all rows
grades = [	[ cell.string for cell in row.find_all("td") if cell.string ] for row in grades	] # all cells except the empty ones

def make_assignment(row):
	points = row[3].split("/")
	return Assignment(name=row[2], category=row[1], earned=points[0], possible=points[1])

grades = map(make_assignment, grades)