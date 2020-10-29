(uniCMS) Portale PoC
--------------------

This project (uniCMS) aims to exemplify the design of a common University portal.
In it you'll find an simplified generalization of all
the entities that usually make up a Content Management System (CMS).

This platform was built on top of Django Framework, with few specialized libraries as well.

The final goal is to achieve as much as possible, writing as little code as possible and working even less!

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

# if you want to load some example datas
./manage.py loaddata ../dumps/cms.json 

./manage.py createsuperuser
./manage.py runserver
````

go to `/admin` and submit the superuser credential to start putting some data into the model.

Model
-----

This project is composed by the following applications:
- websites, where multiple sites can be defined.
- cms_context, where webpaths and EditorialBoard Users and Permissions can be defined
- cms_templates, where multiple page templates can be managed
- cms, where Editorial boards can write post and publish content in one or more contexts.

> :warning: **If you are a pure Djangoer**: You should know that templates and urls would be managed with cms_context, entirely through admin interface. We can even load third-party django applications, it is necessary to take into account configuring the url paths before defining uniCMS ones, otherwise uniCMS will intercept them and with a good chance will return to the user a page of 404.

The first one, called `cms_context`, defines the multi web site logic (multi context) we adopted.
Each context, or website, is nothing more than a
path (url). Each context has users (Editorial Board Editors) with one
of the following permissions (see `cms_context.settings.CMS_CONTEXT_PERMISSIONS`):

````
CMS_CONTEXT_PERMISSIONS = (('1', _('can edit created by him/her')),
                           ('2', _('can edit all pages in his/her context')),
                           ('3', _('can edit all pages in his/her context and descendants')),
                           ('4', _('can translate all pages in his/her context')),
                           ('5', _('can translate all pages in his/her context and descendants')),
                           ('6', _('can publish created by him/her')),
                           ('7', _('can publish all pages in his/her context')),
                           ('8', _('can publish all pages in his/her context and descendants')),
                           )
````

`cms` is the model where we've defined how we build a Page.
For us, a Page, is anything else than a composition of blocks, rendered in a
HTML template. This means that a page is a block container, in which we can
define many blocks with different order. For every page we must define
to which context it belong to and also the template that we want to adopt for HTML rendering.
Nothing prevents us from using something other than HTML, it's just python, you know.

Every block can also be localized in one or many languages, if a client browser have a
the Spanish localization the rendering system will render all the spanish
localized block, if they occour, otherwise it will switch to default
language, that's English.

Following this approach a WebSite's Home Page is nothing more than a Page object, as a container
of many Block objects, that's rendered in a fancy HTML template.


Template tags
-------------

[WiP]

A cms template can also adopt some of the template tags that come with uniCMS.
These takes as argument the following objects:

````
    'website': WebSite object (cms_context.models.Website)
    'path': request.get_full_path(), eg: "/that/resource/slug-or-whatever"
    'context': Context object (cms_context.models.WebPath)
    'page': Page object (cms.models.Page)
````

Standing on the information taked from these objects the uniCMS template tag
can create additional blocks and render many other informations.


Page Blocks
-------------

[WiP]

A configurable object that would be rendered in a specified setion of the page (as defined in template).
It can take a long Text as argument, a json objects or whatever, it dependes by Block Type.
Examples:

- A pure HTML renderer
- A complex element that take a json object in its object constructor


Context Menu
------------

[WiP]

A WebPath (context) can have multiple Menus or inherits them from its superior context.


Search Engine
-------------

[WiP]

An external storage (RDBMS or MongoDB) that takes metainformations on each
creation or modification of a page or a publication or whatever needed to be searchable.

Installing MongoDB on Debian10
````
apt install -y mongodb-org
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
apt update
apt install -y mongodb-org
````

Start MongoDB
````
systemctl daemon-reload
systemctl enable mongod
systemctl start mongod
````

Gettings started with MongoDB
````
from django.utils import timezone
import pymongo

client = pymongo.MongoClient('10.0.3.217', 27017)

# get database
mdb = client.unicms

# get collection
db = mdb.search

# check version to understand which pymongo documentation you should use!
pymongo.version

entry = {"title": "that name that likes you",
         "description": "My first blog post!",
         "content-type": "cms.",
         "content-id": "",
         "site": "www.unical.it",
         "context": "/"
         "url": "http://sdfsdf",
         "tags": ["mongodb", "python", "pymongo"],
         "date": timezone.now()}

db.insert_one(entry)

entries = [{"title": "hahaha",
            "description": "asdasd blog post!",
            "content-type": "cms.",
            "content-id": "",
            "site": "www.unical.it",
            "context": "/"
            "url": "http://sdfsdf",
            "tags": ["mongodb", "python"],
            "date": timezone.now()},
            {"title": "23423",
            "description": "a234234 blog post!",
            "content-type": "cms.",
            "content-id": "",
            "site": "www.unical.it",
            "context": "/"
            "url": "My 234blog post!",
            "tags": ["mongodb", "python"],
            "date": timezone.now()}]
db.insert_many(entries)


# how many entries do we have?
db.count_documents({})

# regexp filters
import re
regexp = re.compile('^h', re.I)
search_filter = {"title": regexp}

# date range filter
search_filter = {
        "date": {
            "$gte": timezone.datetime(2010, 4, 29),
            "$lt": timezone.datetime(2021, 4, 29)
            }
}

# exec query
for i in db.find(search_filter): print(i)

# result sliced (for pagination)
count = 1
res = db.find(search_filter)
for i in res[0:count]: print(i)
````

Todo
----

- SiteMap exporter
- Api OAS3
- Search Engine
- Custom blocks (examples and working ones)
- EditorialBoard UI with permissions
- EditorialBoard Workflow
