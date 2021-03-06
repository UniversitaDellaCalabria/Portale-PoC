Installing MongoDB on Debian10
````
apt -y install gnupg wget
wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
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

Setup ACL and permissions, using mongo CLI
````
use admin
db.createUser(
  {
    user: "admin",
    pwd: passwordPrompt(), // or cleartext password
    roles: [ { role: "userAdminAnyDatabase", db: "admin" }, "readWriteAnyDatabase" ]
  }
)
exit

#restart mongodb
mongo --port 27017  --authenticationDatabase "admin" -u "admin" -p

# add development/usage roles
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

# try to connect
mongo --port 27017  --authenticationDatabase "unicms" -u "unicms_search" -p thatpassword
````

Setup pymongo and run your first connection
````
from django.utils import timezone
import pymongo

client_params = dict(username='admin',
                     password='thatpassword',
                     connectTimeoutMS=5000,
                     socketTimeoutMS=5000,
                     serverSelectionTimeoutMS=5000)
client = pymongo.MongoClient('mongodb://10.0.3.217:27017', **client_params)

# get database
mdb = client.unicms

# get collection
collection = mdb.search

# check version to understand which pymongo documentation you should use!
pymongo.version


collection.insert_one(entry)

entries = [{"title": "that name that likes you",
            "heading": "My first blog post!",
            "content-type": "cms.",
            "content-id": "",
            "content": "that long full text",
            "site": "www.unical.it",
            "webpath": "/",
            "urls": ["http://sdfsdf"],
            "tags": ["mongodb", "python", "pymongo"],
            "indexed": timezone.now(),
            "published": "2020-11-09T13:35:44Z",
            "viewed": 0,
            "relevance": 10,
            "language": "italian",
            "translations":
              [
                {
                  "language": "english",
                  "title": "that title",
                  "heading": "that head",
                  "content": "There is nothing more surreal than reality."
                },
                {
                  "language": "french",
                  "content": "Il n'y a rien de plus surréaliste que la réalité."
                }
              ],
            "year": 2020
            },
            {"title": "Hot summer",
            "heading": "secondo e via",
            "content-type": "cms.",
            "content-id": "",
            "content": "Ciao, io sono giuseppe. Olè, olà.",
            "site": "www.unical.it",
            "webpath": "/",
            "urls": ["http://sdfsdf"],
            "tags": ["mongodb", "python", "pymongo"],
            "indexed": timezone.now(),
            "published": "2020-11-09T13:35:44Z",
            "viewed": 0,
            "relevance": 5,
            "language": "italian",
            "translations":
                      [
                        {
                          "language": "english",
                          "title": "that title 2",
                          "heading": "that head 2",
                          "content": "That's giuseppe"
                        },
                        {
                          "language": "french",
                          "content": "blah blah blah"
                        }
                      ],
            "year": 2018
            }]
collection.insert_many(entries)
````

A full-text index would be created on top of this schema.
````
# using pymongo

from pymongo import TEXT
collection.create_index([('title', TEXT),
                         ('heading', TEXT),
                         ('content', TEXT),
                         ('translations.title', TEXT),
                         ('translations.heading', TEXT),
                         ('translations.content', TEXT),
                         ('year', 1)],
                         default_language="italian")

# drop indexes
collection.drop_indexes()

collection.find_one({"$text": {"$search": "post"}})

collection.find_one({'year': 2018, $text: {$search: "my blog"}}, {'relevance': {$meta: "textRelevance"}})

````
Let's search for something ...
````
# fulltext search

search_q = {'year': 2018,
            '$text': {'$search': "e via"}}
collection.find_one(search_q, {'relevance': {'$meta': "textScore"}})

collection.find(search_q, {'relevance': {'$meta': "textScore"}}).\
           sort([('relevance', {'$meta': 'textScore'})])

# how many entries do we have?
collection.count_documents({})

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
for i in collection.find(search_filter): print(i)

# result sliced (for pagination)
count = 1
res = collection.find(search_filter)
for i in res[0:count]: print(i)
````
