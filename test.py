from __future__ import division
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
		return "{} in {}, {}/{} ({}%)".format(self.name, self.category, earned, self.possible, percentage)

class Group:

	def __init__(self, assignments, class_name, teacher_name):
		self.assignments = assignments
		self.class_name = class_name
		self.teacher_name = " ".join(reversed(teacher_name.split(", ")))

	@property
	def _non_null(self):
		return list(filter(lambda assignment: not assignment._is_null, self.assignments)) # excludes "--" scores
			# TODO remove

	@property
	def _total_earned(self):
		return sum(assignment.earned for assignment in self._non_null)

	@property
	def _total_possible(self):
		return sum(assignment.possible for assignment in self._non_null)

	@property
	def score(self):
		return round(100 * self._total_earned / self._total_possible)

	def __str__(self):
		header = "{} with {}, GRADE {}%".format(self.class_name, self.teacher_name, self.score) #TODO class name
		grades = [ "{}. {}".format(i+1, assignment) for i, assignment in enumerate(self.assignments) ]
		separator = "/" * max(map(len, grades))
		grades = "\n".join(grades)
		return "\n".join( (header, separator, grades) )


with open("test.html") as page:
	soup = BeautifulSoup(page)

tables = soup.find(id="content-main").find_all("table")

info_cells = [ cell.string for cell in tables[0].find_all("tr")[-1].find_all("td") ]
class_name, teacher_name = info_cells[0], info_cells[1]

grades = tables[-1].find_all("tr")[1:] # all rows
grades = [	[ cell.string for cell in row.find_all("td") if cell.string ] for row in grades	] # all cells except the empty ones

def make_assignment(row):
	points = row[3].split("/")
	return Assignment(name=row[2], category=row[1], earned=points[0], possible=points[1])

grades = [ make_assignment(grade) for grade in grades]
group = Group(grades, class_name, teacher_name)

print(group)