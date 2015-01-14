#! /usr/bin/env python3

import extract
import sys
from parse import Group

if __name__ == '__main__':
    class_score_details = extract.important_class_details(2)

    for score_details in class_score_details:
        group = Group.import_from_html(score_details)

        print(group, file=sys.stderr)
