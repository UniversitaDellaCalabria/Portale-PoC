MONGO_URL = 'mongodb://10.0.3.217:27017'
MONGO_DB_PARAMS = dict(username='admin',
                       password='thatpassword',
                       connectTimeoutMS=5000,
                       socketTimeoutMS=5000,
                       serverSelectionTimeoutMS=5000)
MONGO_DB_NAME = 'unicms'
MONGO_COLLECTION_NAME = 'search'

MONGO_SEARCH_DOC_SCHEMA = {
    "title": "",
    "heading": "",
    "content_type": "",
    "content_id": "",
    "content": "",
    "sites": "",
    "urls": [],
    "tags": [],
    "categories": [],
    "indexed": "",
    "published": "",
    "viewed": 0,
    "relevance": 0,
    "language": "",
    "translations":
    [
        {
         "language": "",
         "title": "",
         "heading": "",
         "content": ""
       },
    ],
   "year": 0
}


CMS_POSTSAVE_HOOKS = {
    'Publication': 'cms_search.hooks.publication_se_index',
    'Page': 'cms_search.hooks.page_se_index',
}
