"""
Copyright 2012-2017 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


class DomainObject(object):
    """ Base class for all domain objects. """
    def __init__(self, name='<no name>', url='', short_name='', *args, **kwargs):
        self.__name = name
        self.__short_name = short_name
        self.__url = url
        super(DomainObject, self).__init__(*args, **kwargs)

    def name(self):
        """ Return the name of the domain object. """
        return self.__name

    def short_name(self):
        """ Return the short name of the domain object, to be used as metric id prefix. """
        return self.__short_name

    def url(self):
        """ Return the url of the domain object. """
        return self.__url

    def __lt__(self, other):
        """ Compare names. """
        return self.name() < other.name()

    def __eq__(self, other):
        """ Compare names. """
        return self.name() == other.name() and self.short_name() == other.short_name() and self.url() == other.url()

    def __hash__(self):
        return hash(self.name() + self.short_name() + self.url())
