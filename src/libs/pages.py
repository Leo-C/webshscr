'''
Copyright 2018 - LC

This file is part of webshscr.

webshscr is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

webshscr is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with webshscr.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import csv

from utils import stripstr


PAGES_FILE = "pages.csv" #format: <html_template_file>|<group_1>,...,<group_n>|<Description>
Pages = {}
lstPages = []

class Page:
    def __init__(self, template, description):
        self._template = template
        self._description = description
        self._groups = set()
    
    def add_group(self, name):
        self._groups.add(name)
    
    @property
    def template(self):
        return self._template
    
    @property
    def description(self):
        return self._description
    
    @property
    def ACL(self):
        return self._groups
    
    def group_enabled(self, group):
        return name in self._groups
    
    def groups_enabled(self, groups):
        return len(self._groups.intersection(set(groups))) > 0


def init_pages(config_dir):
    _read_pages(os.path.join(config_dir, PAGES_FILE))

def _read_pages(filepath):
    global Pages
    global lstPages
    
    Pages = {}
    lstPages = []
    with open(filepath, 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter='|', quotechar='"')
        header = csv_reader.next()
        for row in csv_reader:
            if len(row) >= 3:
                page = Page(row[0].strip(), row[2])
                groups = row[1].split(',')
                groups = map(stripstr, groups)
                for group in groups:
                    page.add_group(group)
                Pages[page.template] = page
                lstPages.append(page.template)

def get_pages():
    return lstPages

def get_page(template):
    global Pages
    
    if template in Pages:
        return Pages[template]
    else:
        return None
