###MiniReddit (working title)
This is a small clone of the site reddit.com written using the django python web framework for a school project.

-Reid Horuff

###Setup
 * Install pip (```apt-get install pip```)
 * Install Virtualenv via pip (```pip install virtualenv```)
 * Create virtual environment and install requirements (```source create```)

###Usage
  * After the virtual environemnt has been installed (```source create```) you only need to run ```source activate``` to enter the virtualenv
  * If new dependencies have been added to requirements.pip then source create must be run again to install new dependencies
  * To get server up run ```python manage.py runserver```
  * Visit ```127.0.0.1:8000/``` in browser

###Database
  The db used is SQLite which comes bundled with Django. There is no need for an actual db server (like mySQL) so long as this code is not used in production. ie, don't do anything.

###Server
  Similarly to the db there is no need for an actual server (eg Apache) so long as this code is not used in production becuase one comes bundled with Django for development. ie, don't do anything.  

###Style
  * python
    * 2 space indent
    * camelcase classes
    * underscore variables
  * javascript
    * 2 space indent
    * camelcase everything
