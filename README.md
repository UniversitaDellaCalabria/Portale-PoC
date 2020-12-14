(uniCMS) Portale PoC
--------------------

This project aims to exemplify the design of a common University WebSite Portal.
You'll find an simplified generalization of all
the entities that usually make up a Content Management System (CMS).

This platform was built on top of Django Framework, with few specialized libraries as well.
The final goal is to achieve as much as possible, writing as little code as possible and working even less, when possibile.

# Table of Contents
1. [Setup](#setup)
2. [Model](#model)
3. [Template tags](#template-tags)
4. [Page Blocks](#fourth-examplehttpwwwfourthexamplecom)
5. [Handlers](#handlers)
6. [Middlewares](#middlewares)
7. [Menu and Navigation Bars](#menu)
8. [Search Engine](#search-engine)
9. [Urls](#urls)
10. [Api OAS3](#api)
11. [Post Pre Save Hooks](#post-pre-save-hooks)
12. [Todo](#todo)


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
./manage.py unicms_collect_templates # use -renew to purge and create again all

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

#### Redis Cache

uniCMS can cache response, these are the relevant parameters
````
################
# Django related
################

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://10.0.3.89:6379/unicms",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
            # improve resilience
            "IGNORE_EXCEPTIONS": True,
            "SOCKET_CONNECT_TIMEOUT": 2,  # seconds
            "SOCKET_TIMEOUT": 2,  # seconds
        }
    }
}
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True

######################
# Redis uniCMS related
######################

CMS_CACHE_ENABLED = True

CMS_CACHE_KEY_PREFIX = 'unicms_'
# in seconds
CMS_CACHE_TTL = 25
# set to 0 means infinite
CMS_MAX_ENTRIES = 0
# request.get_raw_uri() that matches the following would be ignored by cache ...
CMS_CACHE_EXCLUDED_MATCHES =  ['/search?',]
````

#### MongoDB
uniCMS default search engine is built on top of mongodb.
Install and configure mongodb
````
apt install -y gnupg wget
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
apt update
apt install -y mongodb-org

systemctl daemon-reload
systemctl enable mongod
systemctl start mongod
````

Create your defaults users, using mongo CLI
````
use admin
db.createUser(
  {
    user: "admin",
    pwd: "thatpassword"
    roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
  }
)

use unicms
db.createUser(
  {
    user: "unicms",
    pwd:  "thatpassword",
    roles: [{ role: "readWrite", db: "unicms" }]
  }
)

db.createUser(
  {
    user: "unicms_search",
    pwd:  "thatpassword",
    roles: [{ role: "read", db: "unicms" }]
  }
)

exit
````
Configure connection and defaults in settings.py
````
MONGO_URL = 'mongodb://10.0.3.217:27017'
MONGO_CONNECTION_PARAMS = dict(username='admin',
                               password='thatpassword',
                               connectTimeoutMS=5000,
                               socketTimeoutMS=5000,
                               serverSelectionTimeoutMS=5000)
MONGO_DB_NAME = 'unicms'
MONGO_COLLECTION_NAME = 'search'
MODEL_TO_MONGO_MAP = {
    'cms.Page': 'cms_search.models.page_to_entry',
    'cms.Publication': 'cms_search.models.publication_to_entry'
}
````


Create your fulltext indexes. Default_language is italian by default.
````
./manage.py cms_search_create_mongo_index -default_language english
````

Model
-----

This project is composed by the following applications:
- websites, where multiple sites can be defined.
- cms_contexts, where webpaths and EditorialBoard Users and Permissions can be defined
- cms_templates, where multiple page templates and page blocks can be managed
- cms_medias, specialized app for management, upload and navigation of media files.
- cms_menus, specialized app for navigation bar creation and management.
- cms_carousels, specialized app for Carousel and Slider creation and management.
- cms, where Editorial boards can create Pages and News to be published in one or more Contexts.


> :warning: **If you are a pure Djangoer**: 

You should know that templates and urls would be managed with cms_context, entirely through admin interface. 
We can even load third-party django applications, it's necessary to take into account that you should configured your django urls
paths before defining uniCMS ones, otherwise uniCMS will intercept them and with a good chance will 
return to the user a page of 404. You can even set `CMS_PATH_PREFIX` to a desidered value, eg: `portale/`, to 
restrict uniCMS url matching to a specified namespace.

The module `cms_contexts` defines the multiple website management (multi contexts) we have adopted.
Each context mail ches a Path and a web page, it's nothing more than a
webpath. Each context has users (Editorial Board Editors) with one or more
of the following permissions (see `cms_context.settings.CMS_CONTEXT_PERMISSIONS`):

````
CMS_CONTEXT_PERMISSIONS = (('1', _('can edit created by him/her in his/her context')),
                           ('2', _('can edit all pages in his/her context')),
                           ('3', _('can edit all pages in his/her context and descendants')),
                           ('4', _('can translate all pages in his/her context')),
                           ('5', _('can translate all pages in his/her context and descendants')),
                           ('6', _('can publish created by him/her in his/her context')),
                           ('7', _('can publish all pages in his/her context')),
                           ('8', _('can publish all pages in his/her context and descendants')),
                           )
````

`cms` is the model where we've defined how we build a Page or a Publication.
For us, a Page, is anything else than a composition of blocks, rendered in a
HTML base template. This means that a page is a block container, in which we can
define many blocks with different order. For every page we must define
to which context (webpath) it belong to and also the template that we want to adopt for HTML rendering.
Nothing prevents us from using something other than HTML, it's just python, you know.

Menus, Carosules, Publications and Categories can also be localized in one or many languages via Web 
Backend, if a client browser have a Spanish localization the rendering system will render all the spanish
localized block, if they occour, otherwise it will switch to default
language.

All the gettext values defined in our static html template will be handled as django localization use to do.

Template tags
-------------

[WiP]

A cms template or a HTML page block can also adopt some of the template tags that come with uniCMS.
UniCMS template context takes at least the following objects:

````
    'website': WebSite object (cms_context.models.Website)
    'path': request.get_full_path(), eg: "/that/resource/slug-or-whatever"
    'webpath': Context object (cms_contexts.models.WebPath)
    'page': Page object (cms.models.Page)
````

Standing on the informations taken from these objects uniCMS also adopts some other custom templatetags, as follow.
These templatetags will also work in Page Blocks that would take, optionally, a html template as argument.

`cms_templates`
- supported_languages: get settings.LANGUAGES_CODE to templates

`cms_menus`
- `load_menu`: eg, `{% load_menu section='menu-1' template="main_menu.html" %}`

`cms_carousels`
- `load_carousel`: similar to `load_menu`

`cms_contexts`
- `language_menu`: an usage example here:
   ````
       {% language_menu as language_urls %}
       {% for lang,url in language_urls.items %}
       <li><a class="list-item" href="{{ url }}"><span>{{ lang }}</span></a></li>
       {% endfor %}
   ````
- `breadcrumbs`: `{% breadcrumbs template="breadcrumbs.html" %}`
   if template argument will be absent it will rely on `breadcrumbs.html` template.
- `call`: `{% call obj=pub method='get_url_list' category_name=cat %}`
    Call any object method and also pass to it whatever `**kwargs`.

`cms`
- `load_blocks`: `{% load_blocks section='slider' %}`
  it would be configured in the base templates and defines where the blocks would be rendered.
  it takes `section` as argument, to query/filter only the blocks that belongs to that section.
- `load_publications_preview`: `{% load_publications_preview template="publications_preview.html" %}`
    - additional paramenters:
        template,
        section
        number=5
        in_evidence=False
        categories_csv="Didattica,Ricerca"
        tags_csv="eventi,ricerca"


Handlers
--------

There are cases in which it is necessary to create specialized applications, 
with templates and templatetags, detached from the pages configured within the CMS. 
Think, for example, to `cms.handlers` which manages the pages for navigating 
publications (List) and opening a publication (View).

In this case the handlers have to be registered in `settings.py`, as follow:

````
CMS_PUBLICATION_VIEW_PREFIX_PATH = 'contents/news/view/'
CMS_PUBLICATION_LIST_PREFIX_PATH = 'contents/news/list'
CMS_PUBLICATION_URL_LIST_REGEXP = f'^(?P<context>[\/a-zA-Z0-9\.\-\_]*)({CMS_PUBLICATION_LIST_PREFIX_PATH})/?$'
CMS_PUBLICATION_URL_VIEW_REGEXP = f'^(?P<context>[\/a-zA-Z0-9\.\-\_]*)({CMS_PUBLICATION_VIEW_PREFIX_PATH})(?P<slug>[a-z0-9\-]*)'

CMS_HANDLERS_PATHS = [CMS_PUBLICATION_VIEW_PREFIX_PATH,
                      CMS_PUBLICATION_LIST_PREFIX_PATH]
CMS_APP_REGEXP_URLPATHS = {
    'cms.handlers.PublicationViewHandler' : CMS_PUBLICATION_URL_VIEW_REGEXP,
    'cms.handlers.PublicationListHandler' : CMS_PUBLICATION_URL_LIST_REGEXP,
}
````

The paths defined in `CMS_HANDLERS_PATHS`  make up the list of 
reserved words, to be considered during validation on save, in `cms_context.models.WebPath`. 
They compose a list of reserved words that cannot be used 
as path value in `cms_context.models.WebPath`.


Middlewares
-----------

`cms_contexts.middleware.detect_language_middleware`:
   detects the browser user language checking both `?lang=` request arg 
   and the web browser default language. It's needed to 
   handle Menu, Carousel and Publication localizations.

`show_template_blocks_sections`:
   toggles, for staff users, the display of block sections in pages.

`show_cms_draft_mode`:
   toggles, for staff users, the draft view mode in pages.


Page Blocks
-------------

[WiP]

A configurable object that would be rendered in a specified section of the page (as defined in its base template).
It can take a long Text as content, a json objects or whatever, it dependes by Block Type.
Examples:

- A pure HTML renderer
- A Specialized Block element that take a json object in its object constructor

The following descriptions covers some HTML blocks.
As we can see the HTML blocks in uniCMS have a full support of Django templatetags and template context.


*Load Image slider (Carousel) configured for the Page*
````
{% load unicms_carousels %}
{% load_carousel section='slider' template="unical_portale_hero.html" %}

<script>
$(document).ready(function() {
  $("#my-slider").owlCarousel({
      navigation : true, // Show next and prev buttons
      loop: true,
      slideSpeed : 300,
      paginationSpeed : 400,
      autoplay: true,
      items : 1,
      itemsDesktop : false,
      itemsDesktopSmall : false,
      itemsTablet: false,
      itemsMobile : false,
      dots: false
  });
});
</script>
````

*Load Publication preview in a Page*
it widely use the load_publications_preview templatetag, this 
template tags loads all the pubblication related to the WebPath (CMS Context) 
of the Page.

````
{% load unicms_blocks %}
            <div class="row negative-mt-5 mb-3" >
                <div class="col-12 col-md-3">
                    <div class="section-title-label px-3 py-1">
                        <h3>Unical <span class="super-bold">world</span></h3>
                    </div>
                </div>
            </div>

            <div class="row">
                <div class="col-12 col-lg-9">
                    {% load_publications_preview template="publications_preview_v3.html" %}
                </div>
                <div class="col-12 col-lg-3">
                    {% include "unical_portale_agenda.html" %}
                </div>
            </div>
````

*Youtube iframes*
As simple as possibile, that bunch of HTML lines.
````
<div class="row">
<div class="col-12 col-md-6">
<iframe width="100%" height="315" src="https://www.youtube.com/embed/ArpMSujC8mM" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
 <div class="col-12 col-md-6">
<iframe width="100%" height="315" src="https://www.youtube.com/embed/xrjjJGqZpcU" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
 </div>
````


Menu
----
[WiP]

A WebPath (context) can have multiple Menus and Navigation bars, but also Footers.
Menu can be fetched through Rest API `/api/menu/<menu_id:int>` and also updated/created through this resources.

Each menu items can have three kinds of links: url, page, publication.
Each menu items can get additional contents (`inherited_contents`) from a publication, this means that
a presentation url, or a subheading or whatever belonging to a publication can be made accessible during a 
menu items representation. Think about presentati in images, additional links ...


Urls
----

[WiP]

All the urls that matches the namespace configured in the `urls.py` of the master project
will be handled by uniCMS. uniCMS can match two kind of resources:

1. WebPath (Context) corresponsing at a single Page (Home page and its childs)
2. Application Handlers, an example would be Pubblication List and Views resources

for these latter uniCMS uses some reserved words, as prefix, to deal with specialized url routings.
in the settings file we would configure these. See [Handlers](#handlers) for example.

See `cms.settings` as example.
See `cms.views.cms_dispatcher` to see how an http request is intercepted and handled by uniCMS to know if use an Handler or a Standard Page as response.


Search Engine
-------------

uniCMS uses MongoDB as search engine, it was adopted in place of others search engines like Elastic Search or Sorl, for the following reasons:

- The documents stored are really small, few kilobytes (BSON storage)
- collections would be populated on each creation/change event by on_save hooks
- each entry is composed following a small schema, this would reduce storage usage increasing the performances at the same time

Technical specifications are available in [MongoDB Official Documentation](https://docs.mongodb.com/manual/core/index-text/).
Some usage example also have been posted [here](https://code.tutsplus.com/tutorials/full-text-search-in-mongodb--cms-24835).

An document would be as follows (see `cms_search.models`)

````
entry = {
            "title": "Papiri, Codex, Libri. La attraverso labora lorem ipsum",
            "heading": "Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.",
            "content_type": "cms.Publication",
            "content_id": "1",
            "image": "/media/medias/2020/test_news_1.jpg",
            "content": "<p>Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?</p><p>&lt;h1&gt;This HTML is escaped by default!&lt;/h1&gt;</p><p>&nbsp;</p>",
            "sites": [
                "test.unical.it"
            ],
            "urls": [
                "//test.unical.it/portale/dipartimenti/dimes/contents/news/view/unical-campus-1",
                "//test.unical.it/portale/contents/news/view/unical-campus-1"
            ],
            "tags": [],
            "categories": [
                "Didattica"
            ],
            "indexed": "2020-12-09T15:00:18.151000",
            "published": "2020-11-09T13:24:35",
            "viewed": 0,
            "relevance": 0.5714285714285714,
            "language": "italian",
            "translations": [
                {
                    "language": "english",
                    "title": "gdfg",
                    "subheading": "dfgdfgdf",
                    "content": "<p>dfgdfgdfg</p>"
                }
            ],
            "day": 9,
            "month": 11,
            "year": 2020
        },
````

#### Search Engine CLI

Publication and Page models (`cms.models`) configures by default some save_hooks, like the search engine indexers.
Search Engine indexes can be rebuilt with a management command (SE cli):

````
./manage.py cms_search_content_sync -y 2020 -type cmspublications.Publication -d 1 -y 2020 -m 11 -show
````

Purge all the entries and renew them
````
# all Pages
./manage.py cms_search_content_sync -y 2020 -type cmspages.Page -purge -insert -show

# everything in that year
./manage.py cms_search_content_sync  -purge -y 2020

# a single month
./manage.py cms_search_content_sync -y 2020 -type cmspublications.Publication -m 12 -y 2020 -purge -insert
````



`cms_search_content_sync` rely on `settings.MODEL_TO_MONGO_MAP`:
```
MODEL_TO_MONGO_MAP = {
    'cmspages.Page': 'cms_search.models.page_to_entry',
    'cmspublications.Publication': 'cms_search.models.publication_to_entry'
}
````


### Behavior

Let's suppose we are searching these words upon the previous entry.
These all matches:

- "my blog"
- "than reality"
- "rien la reliti"
- "my!"

These will not match:

- 'rien -"de plus"'
- '"my!"'
- '-nothing'

As we can see symbols like `+` and `-` will exlude or include words.
Specifying "some bunch of words" will match the entire sequence.
That's something very similar to something professional 😎.


Post Pre Save Hooks
-------------------
By default Pages and Publications call pre and post save hooks.
Django signals are registered in `cms_search.signals`.
In `settings.py` we can register as many as desidered hooks to one or more 
models, Django signals will load them on each pre/post save/delete event.

````
CMS_HOOKS = {
    'Publication': {
        'PRESAVE': [],
        'POSTSAVE': ['cms_search.hooks.publication_se_insert',],
        'PREDELETE': ['cms_search.hooks.searchengine_entry_remove',],
        'POSTDELETE': []
    },
    'Page': {
        'PRESAVE': [],
        'POSTSAVE': ['cms_search.hooks.page_se_insert',],
        'PREDELETE': ['cms_search.hooks.searchengine_entry_remove',],
        'POSTDELETE': []
    }
}
```` 


Api
---

see `/openapi.json` and `/openapi` for OpenAPI v3 Schema.


Todo
----

- SiteMap exporter
- Search Engine
- EditorialBoard UI with permissions
- EditorialBoard Workflow
