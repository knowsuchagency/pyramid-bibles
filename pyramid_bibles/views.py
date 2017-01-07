from pyramid.view import view_config
import pkg_resources
import json


# open files and deserialize
verses = dict()
for version in ('NIV', 'MSG', 'ESV', 'NLT'):
    filepath = pkg_resources.resource_filename('pyramid_bibles', f'static/bibles/{version}/{version}.json')
    with open(filepath) as verse_file:
        verses[version] = json.load(verse_file)


class Resource:
    """A location-aware resource"""
    def __init__(self, data):
        self.data = data
        self.__parent__ = None
        self.__name__ = ''

    def __getitem__(self, item):
        if isinstance(self.data, dict):
            result = Resource(self.data[item])
            result.__parent__ = self
            result.__name__ = item
            return result
        raise KeyError

    def __repr__(self):
        if self.__parent__ is None or self.__name__ in ('NIV', 'MSG', 'ESV', 'NLT'):
            return json.dumps(tuple(self.data.keys()))
        return json.dumps(self.data)



def get_root(request):
    return Resource(verses)


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'pyramid-bibles'}


@view_config(route_name='bible', context=Resource, renderer='string')
def bible(context, request):
    """Return the bible tree"""
    return context

# @view_config(route_name='bible', context=str, renderer='string')
# def bible_verse(context, request):
#     return context


