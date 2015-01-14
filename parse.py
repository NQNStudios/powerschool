#! /usr/bin/env python3
from bs4 import *
import sys
if len(sys.argv) is 1:
	filepath = "class.html" #if no .html file provided as an argument, parse class.html
else:
	filepath = sys.argv[1]

class Assignment:

	def __init__(self, name, category, earned, possible, real):
		self.name = name
		self.category = category
		self.earned = self._parse_int(earned)
		self.possible = self._parse_int(possible)
		self.real = real

	@staticmethod
	def _parse_int(string):
		return int(string) if string.isnumeric() else None

	@property
	def _is_null(self):
		return self.earned is None

	@property
	def _is_extra_credit(self):
		return self.possible is 0

	@property
	def percentage(self):
		if self._is_null or self._is_extra_credit:
			return None
		return round(100 * self.earned / self.possible)

	def __str__(self):
		earned = "--" if self._is_null else self.earned
		percentage = "--" if self._is_null else self.percentage 
		return "({}) {}, {}/{} ({}%)".format(self.category, self.name, earned, self.possible, percentage)


class Group:

	def __init__(self, assignments, class_name, teacher_name):
		self.assignments = assignments
		self.class_name = class_name
		self.teacher_name = " ".join(reversed(teacher_name.split(", ")))

	@staticmethod
	def import_from_html(page):
		soup = BeautifulSoup(page)
		tables = soup.find(id="content-main").find_all("table")
		info_cells = [ cell.string for cell in tables[0].find_all("tr")[-1].find_all("td") ]
		class_name, teacher_name = info_cells[0], info_cells[1]
		grades = tables[-1].find_all("tr")[1:] # all rows
		grades = [	[ cell.string for cell in row.find_all("td") if cell.string ] for row in grades	] # all cells except the empty ones

		def make_assignment(row):
			points = row[3].split("/")
			if len(points) is 1:
				points.append("0") #extra credit assignment
			return Assignment(name=row[2], category=row[1], earned=points[0], possible=points[1], real=True)

		grades = [ make_assignment(grade) for grade in grades]
		return Group(grades, class_name, teacher_name)

	@property
	def categories(self):
		return set(assignment.category for assignment in assignments)
	
	@property
	def _non_null(self):
		return filter(lambda assignment: not assignment._is_null, self.assignments) # excludes "--" scores

	@property
	def _real(self):
		return filter(lambda assignment: assignment.real, self.assignments)

	@property
	def _total_earned(self):
		return sum(assignment.earned for assignment in self._non_null)

	@property
	def _total_possible(self):
		return sum(assignment.possible for assignment in self._non_null)

	@property
	def score(self):
		return round(100 * self._total_earned / self._total_possible)

	def add_assignment(self, assignment):
		self.assignments += assignment

	def __str__(self):
		header = "{} with {}, GRADE {}%".format(self.class_name, self.teacher_name, self.score)
		grades = [ "{}. {}".format(i+1, assignment) for i, assignment in enumerate(self.assignments) ]
		separator = "/" * max(map(len, grades))
		grades = "\n".join(grades)
		return "\n".join( (header, separator, grades) )


if __name__ == '__main__':
    with open(filepath) as page:
        group = Group.import_from_html(page)
        print(group)
