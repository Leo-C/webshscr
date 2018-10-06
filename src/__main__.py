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

import sys
import os
import time

from libs.config import cfg_init, cfg_get, cfg_get_default
from libs.logutils import init_log, log
from libs.pages import init_pages
from libs.users import init_users
from libs.scripts import init_ACLs
from libs.websrv import init_websrv, start_websrv


def init(config_dir):
    #init config
    cfg_init(config_dir)
    
    #init log
    logl = int(cfg_get_default("LOG_LEVEL", "0"))
    logf = cfg_get_default("LOG_FILE", "")
    init_log(logl, logf)
    
    #init pages
    init_pages(config_dir)
    
    #init users
    init_users(config_dir)
    
    #init script ACLs
    init_ACLs(config_dir)


#specify base directory as argv[1]
if __name__ == "__main__":
    if len(sys.argv) > 1:
        base_path = os.path.abspath(sys.argv[1])
        sys.path.append(base_path)
    else:
        if os.path.isabs(sys.path[0]):
            base_path = os.path.abspath(sys.path[0])
        else:
            base_path = os.path.abspath(os.getcwd())
            sys.path.append(base_path)
    config_dir = base_path + '/config'
    init(config_dir)
	
    init_websrv(base_path)
    start_websrv()
