MONGO_URL = 'mongodb://10.0.3.217:27017'
MONGO_DB_PARAMS = dict(username='admin',
                       password='thatpassword',
                       connectTimeoutMS=5000,
                       socketTimeoutMS=5000,
                       serverSelectionTimeoutMS=5000)
MONGO_DB_NAME = 'unicms'
MONGO_COLLECTION_NAME = 'search'

MODEL_TO_MONGO_MAP = {
    'cms.Page': 'cms.search.models.page_to_entry',
    'cms.Publication': 'cms.search.models.publication_to_entry'
}

CMS_HOOKS = {
    'Publication': {
        'PRESAVE': [],
        'POSTSAVE': ['cms.search.hooks.publication_se_insert',],
        'PREDELETE': ['cms.search.hooks.searchengine_entry_remove',],
        'POSTDELETE': []
    },
    'Page': {
        'PRESAVE': [],
        'POSTSAVE': ['cms.search.hooks.page_se_insert',],
        'PREDELETE': ['cms.search.hooks.searchengine_entry_remove',],
        'POSTDELETE': []
    }
}

SEARCH_ELEMENTS_IN_PAGE = 25