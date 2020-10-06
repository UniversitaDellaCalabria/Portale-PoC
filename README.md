Portale PoC
-----------


This project (uniCMS) aims to exemplify the approach and design of a common University portal.
You will find in it an simplified generalization of all
the entities that usually make up a Content Management System (CMS).

This platform was built on top of Django Framework, with other few specialized libraries.

The final goal is to achieve as much as possible, writing as little code as possible and working even less!

Model
-----

We have created two applications, __cms_context__ and __cms__.

The first one, called `cms_context`, defines the multi web site logic (multi context) we adopted.
Each context, or website, is nothing more than a
path (url). Each context has users (Editorial Board Editors) with one
of the following permissions (see `cms_context.settings.CMS_CONTEXT_PERMISSIONS`):

- can edit created by him/her
- can edit all pages in his/her context
- can edit all pages in his/her context and descendants
- can edit all pages
- can edit his/her own
- can translate all pages in his/her context
- can translate all pages in his/her context and descendants
- can translate all pages
- can publish created by him/her
- can publish all pages in his/her context
- can publish all pages in his/her context and descendants
- can publish all pages

The second one, called `cms`, is the model where we've defined how we build a Page.
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



Todo
----

- SiteMap exporter
- Api OAS3
-
