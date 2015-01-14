#! /usr/bin/env python3

from splinter import Browser
from bs4 import BeautifulSoup
import re

search_term = 2

def visit_home(browser):
    browser.visit('https://powerschool.slcschools.org/guardian/home.html')

def log_in(browser):
    browser.fill('account', 'NN501621')
    browser.fill('pw', 'roy501621111')
    browser.find_by_id('btn-enter').click()

def find_content_table(soup):
    """Finds the main content table for class info from the homepage"""

    container = soup.body.find(id='container')
    content_main = container.find(id='content-main')
    quick_lookup = container.find(id='quickLookup')

    def has_class(tag):
        return tag.has_attr('class')

    grid = quick_lookup.find(has_class)
    table_body = grid.tbody

    return table_body

def find_class_rows(content_table):
    """Finds the class rows from the homepage main content table"""

    rows = content_table.find_all('tr')
    return rows[3:-1] # retrieve only rows containing class info

def find_grade_columns(class_row):
    """Finds the grade columns from a class info table row"""

    columns = class_row.find_all('td')
    return columns[12:-2] # return only columns containing grade links

def find_term_grades(home_html, term_num):
    """Finds grade boxes from the desired school term"""

    soup = BeautifulSoup(home_html)

    table = find_content_table(soup)

    class_rows = find_class_rows(table)

    term_grades = [ ]

    for class_row in class_rows:
        grade_columns = find_grade_columns(class_row)

        term_grades.append(grade_columns[term_num - 1])
        
    return term_grades

def is_grade_A(term_grade):
    """Determines if a term grade is an A"""

    A_regex = '^A[0-9]*$' # the letter A followed immediately by a multi-digit number

    return re.search(A_regex, term_grade.text)

def is_grade_null(term_grade):
    """Determines if a term grade is null (--)"""

    null_regex = '^--$'

    return re.search(null_regex, term_grade.text)

def class_details_html(browser, term_grade):
    """Returns the HTML content of the class details page for the given term grade"""
    
    visit_home(browser)

    browser.find_link_by_href(term_grade.a['href']).click()

    return browser.html

def important_class_details(term_num):
    """Returns a list containing the HTML content of every class details page
    for class that does not have an "A" grade"""

    important_details = [ ]

    with Browser() as browser:
        visit_home(browser)
        log_in(browser)
        home_html = browser.html

        for term_grade in find_term_grades(home_html, term_num):
            if not (is_grade_A(term_grade) or is_grade_null(term_grade)):
                important_details.append(class_details_html(browser, term_grade))

    return important_details
