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

from utils import load_properties

CONFIG_FILE = 'config.properties'
config = {}

def cfg_init(config_dir):
    global config
    config = load_properties(config_dir + '/' + CONFIG_FILE)

def cfg_get_default(varname, default):
    global config
    if varname in config:
        return config[varname]
    else:
        return default

def cfg_get(varname):
    return cfg_get_default(varname, None)
