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
import getopt
import hashlib


def usage():
    print("Produce and emit a row in user.dat format")
    print("If output is not specified, is printed on stdout")
    print("If some option is not specified, default is used (admin/admin/admins)")
    print("Syntax: %s options")
    print("  -u or --user")
    print("  -p or --password")
    print("  -g or --groups")
    print("  -o or --output")

def calculate_user_record(user, password, groups):
    hash_pwd = hashlib.sha256(user + ":" + password).hexdigest()
    return user + ":" + hash_pwd + ":" + ",".join(groups)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:p:g:o:", ["user=", "password=", "groups=", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        sys.exit(1)
    
    user = "admin"
    password = "admin"
    groups = "admins"
    output = ""
    for o, a in opts:
        if o in ("-u", "--user"):
            user = a
        elif o in ("-p", "--password"):
            password = a
        elif o in ("-g", "--groups"):
            groups = a
        elif o in ("-o", "--output"):
            output = a
        else:
            assert False, "unhandled option"
    
    groups = groups.split(',')
    groups = map(lambda x: x.strip(), groups)
    s = calculate_user_record(user, password, groups)
    if output == "":
        print(s)
    else:
        try:
            f = open(output, 'wa')
            f.write(s)
            f.close()
        except Exception as err:
            print str(err)
    
if __name__ == "__main__":
    main()
