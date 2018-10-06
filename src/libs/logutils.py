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

log_level = 0
log_out = ""

def init_log(level, out=""):
    global log_level
    global log_out
    
    log_level = level
    log_out = out

def log(level, msg):
    global log_level
    global dbg_out
    
    if level <= log_level:
        if log_out == "":
            print msg
        else:
            f = open(log_out, "a")
            f.write(msg+"\n")
            f.close()
