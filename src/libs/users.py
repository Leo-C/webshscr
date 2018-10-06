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

import hashlib
import os

from flask_login import UserMixin

from utils import stripstr

USER_FILE = "users.dat" #format: user:sha256(pwd):group_1,...group_n
filepath = ""
Users = {}

class User(UserMixin):
    def __init__(self, name, hash_pwd, groups = []):
        self._name = name
        self._hash_pwd = hash_pwd
        self._groups = set(groups)
        self._authenticated = False
    
    @property
    def name(self):
        return self._name
    
    @property
    def hash_pwd(self):
        return self._hash_pwd
    
    @property
    def groups(self):
        return self._groups
    
    def add_group(self, name):
        self._groups.add(name)
    
    def has_group(self, name):
        return name in self._groups
    
    def has_groups(self, groups):
        return len(self._groups.intersection(set(groups))) > 0
    
    def verify_password(self, password):
        check = (self._hash_pwd == hashlib.sha256(self._name + ":" + password).hexdigest())
        self._authenticated = check
        return check
    
    #subsequent override UserMixin methods
    def get_id(self):
        return unicode(self._name)
    
    @property
    def is_authenticated(self):
        return self._authenticated

def init_users(config_dir):
    global USER_FILE
    global filepath
    
    filepath = os.path.join(config_dir, USER_FILE)
    _read_users()

def _read_users():
    global filepath
    global Users
    
    Users = {}
    with open(filepath, 'r') as f:
        for line in f:
            line = line.rstrip() #removes trailing whitespace and '\n' chars
            if line.startswith("#"): continue #skips comments that starts with '#'
            fields = line.split(':')
            if len(fields) >= 3:
                name = fields[0].strip()
                hash_pwd = fields[1].strip()
                groups = fields[2].split(',')
                groups = map(stripstr, groups)
                user = User(name, hash_pwd, groups)
                Users[name] = user

def _write_users():
    global filepath
    global Users
    
    with open(filepath, 'w') as f:
        for name in Users:
            user = Users[name]
            line = user.name + ":" + user.hash_pwd + ":" + ",".join(user.groups)
            f.write(line+'\n')

def get_user_names():
    return Users.keys()

def get_user(name):
    global Users
    
    if name in Users:
        return Users[name]
    else:
        return None

def create_user(name, password):
    return User(name, hashlib.sha256(name + ":" + password).hexdigest())

def add_or_modify_user(user):
    global Users
    
    Users[user.name] = user
    _write_users()

def del_user(name):
    if name in Users:
        del Users[name]
        _write_users()
