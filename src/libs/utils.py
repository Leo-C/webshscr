'''
Copyright 2017 - LC

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

import io
import json


def load_properties(filename):
    props = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip() #removes trailing whitespace and '\n' chars
            
            if "=" not in line: continue #skips blanks and comments w/o =
            if line.startswith("#"): continue #skips comments that starts with '#'
            
            k, v = line.split("=", 1)
            props[k] = v
    
    return props

def merge_dicts(*dicts):
    d = {}
    for idx in range(1, len(dicts)):
        for k, v in dicts[idx].iteritems():
            d[k] = v
    
    return d

def string_properties(outstr):
    props = {}
    buf = io.StringIO(unicode(outstr))
    
    for line in f:
        line = line.rstrip() #removes trailing whitespace and '\n' chars
        if "=" not in line: continue #skips blanks and comments w/o =
        k, v = line.split("=", 1)
        props[k] = v
    
    buf.close()
    
    return props

def stripstr(str):
    return str.strip()

def get_dict_default(dict, key, default):
    if key in dict:
        return dict[key]
    else:
        return default

def dict2str(dict):
    return json.dumps(dict)
