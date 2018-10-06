## **web** **sh**ell **s**cripting


### Introduction

**webshscr** is a lightweight web server useful to expose shell script via web. 
It provide user authorization and account, reserving execution of specific shell scripts to specific groups.


### Installation

*webshscr* is multiplatform; required packages are:

* [Python 2.7.x](https://www.python.org/)
* [flask](http://flask.pocoo.org/)
* [flask_login](https://flask-login.readthedocs.io/en/latest/)
* [subprocess32](https://github.com/google/python-subprocess32)
* [xmltodict](https://github.com/martinblech/xmltodict)

To install additional packages *[pip]()* can be used:  
```python -m pip install flask flask_login```  
```python -m pip install flask subprocess32```  
```python -m pip install flask xmltodict```  


### Starting **webshscr**

*webshscr* can be started as '.zip' file:  
```python webshscr.zip [<base_dir>]```  
or from source files with command:  
```python __main__.py [<base_dir>]```  
If ```<base_dir>``` is not specified, base directory is considered current directory. 

Under base directory following folders are used:  

* ```config```: contains config files
* ```scripts```: contains shell script to be called
* ```templates```: contains html templates (using [Jinja 2](http://jinja.pocoo.org/docs/2.10/) syntax)
* ```static```: contains static files called by html templates (images, .css files, .js files, etc.)


### Configurations

In config directory following files are used:  

* ```config.properties```: general configuration file.  
  *Format*: is Java properties, with indexed values in form ```key=format``` and comments starting with '#':
  - ```TLS_enabled```: [0|1] enable TLS using https (with *0* http is used)
  - ```crt_file```: optional, speciofy absolute path of Certificate File used by flask for https; if not specified and TLS is enabled, a bogus certificate is used
  - ```key_file```: optional, speciofy absolute path of Key File used by flask for https; if not specified and TLS is enabled, a bogus certificate is used
  - ```LOG_LEVEL```: optional, is logging level. Permitted levels are:  
    0: log none (*default*)  
    1: log only Warnings  
    2: log Warnings and Errors  
    3: log Warnings, Errors and Info  
    4: log Warnings, Errors, Info and Debug  
  - ```LOG_FILE```: optional, is file to store log; if not specified is  ```STDOUT```.
* ```pages.csv```: list of html pages permitted (listed in home page)  
  *Format*: is CSV with pipe separator (```|```) with headers in 1st row; following are permitted fields:
  - **page_name**: page name in html (only page name, accessed with following URL: ```http://host/pages/<html_page>```)
  - **groups**: groups separated by comma (```,```); those will be only authorized to access specified page 
  - **description**: description that appear in list automatically generated in home page 
* ```scripts.acl```: ACLs for running script files (specifying groups)  
  *Format*: fields are ```<script_name>:<groups>``` with comment lines beginning with ```#```:
  - **script_name** is filename (not path) of a script in ```scripts``` subdirectory
  - **groups**: groups separated by commas; those will be only authorized to access specified script  
* ```users.dat```: user storing users with associated password and groups  
  *Format*: ```<user>:<user/password econding>:<groups>```:
  - **user**: is user name
  - **user/password econding**: is SHA-256 encoding of sequence ```<user>:<password>```
  - **groups**: are groups containing specified user, separated by comma (```,```)



### User creation from CLI

User creation is permitted from CLI using command:
```python createuser.py <options>```
Options are:

* ```-u``` | ```--user``` <user>: specify user to create; if not specified default is *admin*
* ```-p``` | ```--password``` <pwd>: specify password *pwd* for new user; if not specified default is *admin*
* ```-g``` | ```--groups``` <group_1>,...,<group_n>: specify groups for user, separated by comma (*,*); if not specified default is *admins*
* ```-o``` | ```--output``` <out_file>: specify file for output (using format expected for *users.dat*); if not specified is printed to STDOUT


### License

This program is licensed under [GPLv3](https://www.gnu.org/licenses/gpl.txt) license; no warranty is due, but you can contact me for problem and/or clarifications.  

Commercial use is granted freely, but please inform me about this.