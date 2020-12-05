from cms.models import Page
from cms_search import mongo_collection
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'uniCMS Search Pages Indexer'

    def add_arguments(self, parser):
        parser.epilog='Example: ./manage.py cms_search -y 2020 [-m N] [-d N]'
        parser.add_argument('-type', type=str, required=False,
                            default='cms.Publication',
                            help="eg: cms.Page")
        parser.add_argument('-y', type=int, required=True, 
                            help="Year, eg: 2020")
        parser.add_argument('-m', type=int, required=False, 
                            help="Month, eg: 4")
        parser.add_argument('-d', type=int, required=False, 
                            help="Day, eg: 12")
        parser.add_argument('-show', required=False, action="store_true",
                            help="it only print out the entries")
        parser.add_argument('-purge', required=False, action="store_true",
                            help="purge all the entries")
        parser.add_argument('-build', required=False, action="store_true",
                            help="build entries indexes")
        parser.add_argument('-debug', required=False, action="store_true",
                            help="see debug messages")

    def handle(self, *args, **options):
        collection = mongo_collection()
        query = {'content_type': options['type']}
        count = collection.find(query).count()
        
        # show
        if options['show']:
            for i in collection.find(query):
                print(i)
            print(f'-- {count} elements. --')
        
        # purge
        if options['purge']:
            collection.delete_many(query)
            print(f'-- Deleted {count} elements. --')
        
        # rebuild
        data = []
        if options['build']:
            for page in Page.objects.filter(is_active=true):
                if page.is_publicable():
                    entry = ''
                    data.append(entry)
