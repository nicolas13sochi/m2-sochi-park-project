Python 3.10.x
Django 5.1.4
DRF 3.15.1

local set up:

- clone project
- create virtual environment (/env/) with python3.11.x (python3.11 -m venv env) in root project folder
- activate env (on macOS: "source env/bin/activate", use "deactivate" to deactivate env)
- install dependencies: "pip3 install -r requirements.txt"
- create and set up your ".env" file in core settings folder. See example.env to configure env
- collect static files: "python3 manage.py collectstatic"
- migrate tables: "python3 manage.py migrate"
- run server: "python3 manage.py runserver"
- run celery worker: "celery -A m2sochiparkproject worker -l info --logfile=logs/celery.log --detach"
- run celery beat: "celery -A m2sochiparkproject beat -l info --logfile=logs/celery.beat.log --detach"
- CSS styles write in SCSS files and compile it to CSS 
    - Install sass: https://sass-lang.com/install (e.g. brew install sass/sass/sass)
    - execute command sass static/scss/style.scss static/css/style.css --watch
- To clear migrations: 
    - 'find . -path "*/migrations/*.py" -not -name "__init__.py" -delete'
    - 'find . -path "*/migrations/*.pyc" -delete'

create new project:

- clone repo: "git clone https://github.com/nicolas13sochi/n13-django-template"
- rename m2sochiparkproject folders with yourproject: "mv m2sochiparkproject yourproject"
- replace in code all files names: "m2sochiparkproject" to "yourproject"
- clear migrations (OPTIONALLY):
    - 'find . -path "*/migrations/*.py" -not -name "__init__.py" -delete'
    - 'find . -path "*/migrations/*.pyc" -delete'
- create migrations (OPTIONALLY): "python3 manage.py makemigrations"
- migrate tables: "python3 manage.py migrate"
- remove .git history: "rm -R .git"
- init git: "git init"
- enjoy: setup yourproject as you wish