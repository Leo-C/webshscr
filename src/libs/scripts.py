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
import sys
import json
import xmltodict
if os.name == 'posix' and sys.version_info[0] < 3:
    import subprocess32 as subprocess
else:
    import subprocess

from utils import stripstr, dict2str
from logutils import log


ACL_SCRIPT = "scripts.acl"
ACLs = {}


class ACL:
    def __init__(self, scriptfile, groups = []):
        self._scrfile = scriptfile
        self._groups = set(groups)
    
    @property
    def script(self):
        return script._scrfile
    
    @property
    def groups(self):
        return self._groups
    
    def add_group(self, name):
        self._groups.add(name)


def init_ACLs(config_dir):
    _read_ACLs(os.path.join(config_dir, ACL_SCRIPT))

def _read_ACLs(filepath):
    global ACLs
    ACLs = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.rstrip() #removes trailing whitespace and '\n' chars
            if line.startswith("#"): continue #skips comments that starts with '#'
            fields = line.split(':')
            script = fields[0].strip()
            groups = fields[1].split(',')
            groups = map(stripstr, groups)
            ACLs[script] = ACL(script, groups)


def _prepare_args(script_dir, script, args):
    scr_args = []
    scr_args.append(os.path.join(script_dir, script))
    for n in args:
        v = args[n]
        if len(n) == 1:
            scr_args.append("-" + n)
        else:
            scr_args.append("--" + n)
        if v != "":
            scr_args.append(v)
    return scr_args

def run_script(script_dir, script, args):
    scr_args = _prepare_args(script_dir, script, args)
    log(4, "Run Script: %s" % script)
    log(4, "  with arguments: " + dict2str(args))
    try:
        if os.name == 'posix':
            cl_fd = True
        else:
            cl_fd = False
        proc = subprocess.Popen(scr_args, bufsize=10, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=cl_fd, shell=False, universal_newlines=True)
        out, err = proc.communicate()
        exitcode = proc.returncode
        return exitcode, out, err
    except OSError as ex:
        return -1, "", str(ex)

def get_ACL(scrname):
    global ACLs
    if scrname in ACLs:
        acl = ACLs[scrname]
        return acl.groups
    else:
        return None

def decode_json(str_json):
    try:
        return json.loads(str_json)
    except:
        return {}

def encode_json(dict):
    try:
        return json.dumps(dict)
    except:
        return ""

def decode_xml(str_xml):
    try:
        return xmltodict.parse(str_xml)
    except:
        return {}

def encode_xml(dict):
    try:
        return xmltodict.unparse(dict)
    except:
        return ""
