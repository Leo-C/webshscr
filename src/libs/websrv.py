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
import ssl
import jinja2
from flask import Flask, flash, redirect, url_for, render_template, request, session, abort, make_response
from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from config import cfg_get, cfg_get_default
from users import get_user_names, get_user, create_user, add_or_modify_user, del_user
from pages import get_pages, get_page
from scripts import get_ACL, decode_json, encode_json, decode_xml, encode_xml, run_script
from logutils import log
from utils import get_dict_default, stripstr, dict2str


web_app = Flask("__main__")
login_manager = LoginManager()
dir_scripts = ""

def init_websrv(base_path):
    global web_app
    global login_manager
    global dir_scripts
    
    dir_scripts = os.path.join(base_path, "scripts")
    app_name = cfg_get("AppName")
    #web_app = Flask(appname)
    web_app.secret_key = os.urandom(16)
    #login_manager = LoginManager()
    login_manager.init_app(web_app)
    login_manager.login_view = "/login"
    #set static directory
    web_app.static_folder = os.path.join(base_path, "static")
    #set template directory
    dir_tmpl = os.path.join(base_path, "templates")
    tmpl_loader = jinja2.ChoiceLoader([ jinja2.FileSystemLoader([dir_tmpl]) ])
    web_app.jinja_loader = tmpl_loader

def start_websrv():
    global web_app
    
    TLSproto = cfg_get_default("TLS_enabled", "")
    crt_file = cfg_get_default("crt_file", "")
    key_file = cfg_get_default("key_file", "")
    
    if TLSproto == "1":
        if os.path.isfile(crt_file) and os.path.isfile(key_file):
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_cert_chain(crt_file, key_file)
            web_app.run(host="0.0.0.0", port=443, ssl_context=context, debug=False)
        else:
            web_app.run(host="0.0.0.0", port=80, ssl_context='adhoc', debug=False)
    else:
        web_app.run(host='0.0.0.0', port=80, debug=False)

@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    return redirect("/login")

@web_app.route('/')
@login_required
def home():
    title = cfg_get("AppTitle")
    pages = []
    
    is_admin = current_user.has_group("admins")
    if is_admin:
        pages.append((url_for('handle_users'), "Manage Users"))
    
    pg = get_pages()
    for p in pg:
        page = get_page(p)
        if current_user.has_groups(page.ACL):
            print("TP1")
            pages.append((url_for('render_page', htmlfile=page.template), page.description))
    
    return render_template('home.html', title=title, pages=pages)

@web_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        name = request.form['username']
        passw = request.form['password']
        user = get_user(name)
        
        if user == None:
            flash('Wrong User!', 'error')
            return redirect("/login")
        else:
            user.verify_password(passw)
            if user.is_authenticated:
                login_user(user)
                return redirect("/")
            else:
                flash('Wrong Password!', 'error')
                return redirect("/login")
    else:
        return render_template("login.html", title=cfg_get("AppTitle"))

@web_app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")

def get_users(is_admin):
    if is_admin:
        names = get_user_names()
    else:
        names = []
        names.append(current_user.name)
    users = []
    for name in names:
        users.append((name, ",".join(get_user(name).groups)))
    
    return users
        
@web_app.route("/users", methods=['GET', 'POST'])
@login_required
def handle_users():
    is_admin = current_user.has_group("admins")
    
    if request.method == "POST":
        action = get_dict_default(request.form, "action", "")
        name = get_dict_default(request.form, "user", "")
        pwd1 = get_dict_default(request.form, "password1", "")
        pwd2 = get_dict_default(request.form, "password2", "")
        groups = get_dict_default(request.form, "groups", "")
        
        if action == "create" or action == "update":
            if name != "" and pwd1 != "" and pwd2 != "":
                if (not is_admin) and (name != current_user.name):
                    flash("Operation permitted only to Administrators", "error")
                    return render_template("users.html", title=cfg_get("AppTitle"), users=get_users(is_admin))
                else:
                    if pwd1 != pwd2:
                        flash("Passwords are different!", "error")
                        return render_template("users.html", title=cfg_get("AppTitle"), users=get_users(is_admin))
                    else:
                        user = create_user(name, pwd1)
                        if is_admin:
                            grps = groups.split(',')
                            grps = map(stripstr, grps)
                        else:
                            grps = current_user.groups
                        for grp in grps:
                            user.add_group(grp)
                        add_or_modify_user(user)
                        if action == "create":
                            flash("User '%s' created" % name, "info")
                        else:
                            flash("User '%s' modified" % name, "info")
                        return render_template("users.html", title=cfg_get("AppTitle"), users=get_users(is_admin))
            else:
                flash("All fields must be compiled!", "error")
                return render_template("users.html", title=cfg_get("AppTitle"), users=get_users(is_admin))
        elif action == "delete":
            if name != "":
                if (not is_admin) and (name != current_user.name):
                    flash("Operation permitted only to Administrators", "error")
                    return render_template("users.html", title=cfg_get("AppTitle"), users=get_users(is_admin))
                else:
                    del_user(name)
                    flash("User '%s' deleted" % name, "info")
                    return render_template("users.html", title=cfg_get("AppTitle"), users=get_users(is_admin))
            else:
                flash("User name missing!" % name, "error")
                return render_template("users.html", title=cfg_get("AppTitle"), users=get_users(is_admin))
        else:
            return ("Internal Server Error", 500, {})
    else:
        return render_template("users.html", title=cfg_get("AppTitle"), users=get_users(is_admin))

@web_app.route("/pages/<string:htmlfile>")
@login_required
def render_page(htmlfile):
    log(4, "template page: %s" % htmlfile)
    page = get_page(htmlfile)
    if page == None:
        return ("NOT FOUND", 404, {})
    else:
        if current_user.has_groups(page.ACL):
            return render_template(htmlfile, title=cfg_get("AppTitle"))
        else:
            return ("FORBIDDEN", 403, {})

@web_app.route("/script.form/<string:scrname>", methods=['GET', 'POST'])
@login_required
def script_form(scrname):
    global dir_scripts
    
    acl = get_ACL(scrname)
    if acl == None:
        return ("NOT FOUND", 404, {})
    else:
        log(4, "running script_form() ...")
        if current_user.has_groups(acl):
            log(4, request.args)
            
            (code, out, err) = run_script(dir_scripts, scrname, request.args)
            if code == 0:
                log(1, out)
                return make_response(str(code) + '\n' + out, 200)
            else:
                return make_response(str(code) + '\n' + err, 200)
                log(3, err)
        else:
            return ("FORBIDDEN", 403, {})

@web_app.route("/script.json/<string:scrname>", methods=['POST'])
@login_required
def script_json(scrname):
    global dir_scripts
    
    acl = get_ACL(scrname)
    if acl == None:
        return ("NOT FOUND", 404, {})
    else:
        log(4, "running script_json() ...")
        if current_user.has_groups(acl):
            try:
                args = decode_json(request.data)
                (code, out, err) = run_script(dir_scripts, scrname, args)
                res = {"code": code, "out": out, "err": err}
                log(4, "result = " + dict2str(res))
                if code == 0:
                    log(4, out)
                    return make_response(encode_json(res), 200)
                else:
                    log(3, err)
                    return make_response(encode_json(res), 200)
            except Exception as err:
                log(1, str(err))
                return ("Internal Server Error", 500, {})
        else:
            return ("FORBIDDEN", 403, {})

@web_app.route("/script.xml/<string:scrname>", methods=['POST'])
@login_required
def script_xml(scrname):
    global dir_scripts
    
    acl = get_ACL(scrname)
    if acl == None:
        return ("NOT FOUND", 404, {})
    else:
        log(4, "running script_json() ...")
        if current_user.has_groups(acl):
            try:
                args = decode_xml(request.data)
                (code, out, err) = run_script(dir_scripts, scrname, args)
                res = {"response": {"code": code, "out": out, "err": err}}
                log(4, "result = " + dict2str(res))
                if code == 0:
                    log(4, out)
                    return make_response(encode_xml(res), 200)
                else:
                    log(3, err)
                    return make_response(encode_xml(res), 200)
            except Exception as err:
                log(1, str(err))
                return ("Internal Server Error", 500, {})
        else:
            return ("FORBIDDEN", 403, {})
