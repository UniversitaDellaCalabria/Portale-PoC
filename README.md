(uniCMS) Portale PoC
--------------------

This project aims to exemplify the design of a common University Web Portal.
You'll find an simplified generalization of all
the entities that usually make up a Content Management System (CMS).

This platform was built on top of Django Framework, with few specialized libraries as well.
The final goal is to achieve as much as possible, writing as 
little code as possible and working even less, when possibile.


# Table of Contents
1. [Setup](#setup)
2. [Documentation](#unicms-documentation)
3. [Tests](#tests)
4. [Todo](#todo)


Setup
-----

````
apt install python3-pip
pip3 install virtualenv
mkdir Portale-PoC && cd "$_"
git clone https://github.com/UniversitaDellaCalabria/Portale-PoC.git
virtualenv -ppython3 env
source env/bin/activate
pip3 install -r requirements.txt
cd unicms
./manage.py migrate

# install your templates in settings.INSTALLED_APPS and then symlinks cms templates
./manage.py unicms_collect_templates -renew

# if you want to load some example datas
./manage.py loaddata ../dumps/cms.json

./manage.py createsuperuser
./manage.py runserver
````

Go to `/admin` and submit the superuser credential to start putting some data into the model.

If you want to share your example data
````
./manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude sessions --exclude admin --indent 2 > ../dumps/cms.json
````

Tests
-----

````
./manage.py test cms
````

uniCMS Documentation
--------------------

[https://unicms.readthedocs.io/](https://unicms.readthedocs.io/)

Todo
----

- SiteMap exporter
- EditorialBoard UI with permissions
- EditorialBoard Workflow
