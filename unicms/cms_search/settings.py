MONGO_URL = 'mongodb://10.0.3.217:27017'
MONGO_DB_PARAMS = dict(username='admin',
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

CMS_POSTSAVE_HOOKS = {
    'Publication': 'cms_search.hooks.publication_se_index',
    'Page': 'cms_search.hooks.page_se_index',
}
