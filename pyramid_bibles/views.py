from pyramid.view import view_config
from pyramid.response import Response
import pkg_resources
import gzip
import json

# get the url for the bible verses
verses_url = pkg_resources.resource_filename('pyramid_bibles', 'static/verses.json.gz')
# open file and deserialize
all_verses = json.loads(gzip.open(verses_url).read(), encoding='utf8')
# clean up verses
all_verses = [d['fields'] for d in all_verses]

class Resource(dict):
    def __init__(self):
        for verse in all_verses:
            version = verse['version']
            book = verse['book']
            chapter = verse['chapter']
            number = verse['verse']
            text = verse['text']
            self[version][book][chapter][number] = text

verses_resource = Resource()

@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'pyramid-bibles'}


@view_config(route_name='niv', renderer='json')
def niv(request):
    """Return NIV verses"""
    verses = [verse for verse in all_verses if verse['version'] == 'NIV']
    return verses[:10]

@view_config(route_name='resource', renderer='json')
def resource(request):
    return verses_resource[:10]

