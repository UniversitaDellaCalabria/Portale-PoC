(uniCMS) Portale PoC
--------------------

This project (uniCMS) aims to exemplify the design of a common University portal.
In it you'll find an simplified generalization of all
the entities that usually make up a Content Management System (CMS).

This platform was built on top of Django Framework, with few specialized libraries as well.

The final goal is to achieve as much as possible, writing as little code as possible and working even less!

Model
-----

This project is composed by the following applications:
- cms_context, where multiple sites, webpaths and EditorialBoard Permissions can be managed
- cms_templates, where multiple page templates can be managed
- cms_pages, where we can create a custom page with a custom template and blocks
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

`cms_pages` is the model where we've defined how we build a Page.
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
    'page': Page object (cms_pages.models.Page)
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
creation or modification of a page or a publication or whatever needed to be foundable.

Todo
----

- SiteMap exporter
- Api OAS3
- Search Engine
- Custom blocks (examples and working ones)
- EditorialBoard UI with permissions
- EditorialBoard Workflow
