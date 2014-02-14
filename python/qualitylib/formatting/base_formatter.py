'''
Copyright 2012-2014 Ministerie van Sociale Zaken en Werkgelegenheid

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
'''

import logging


class Formatter(object):  # pylint: disable=R0921
    ''' Abstract base class. '''

    sep = ''

    def process(self, report):
        ''' Return a formatted version of the report. '''
        self.__log_report(report)
        result = self.sep.join([self.prefix(report),
                                self.body(report),
                                self.postfix()])
        self.__log_report(report, done=True)
        return result

    def prefix(self, report):  # pylint: disable=W0613
        ''' Override to return a prefix for the report. '''
        raise NotImplementedError  # pragma: no cover

    def body(self, report):
        ''' Return a formatted version of the body of the report. '''
        sections = []
        for section in self.sections(report):
            self.__log_section(section)
            sections.append(self.section(report, section))
        return self.sep.join(sections)

    @staticmethod
    def sections(report):
        ''' Return the report sections to include in the report. '''
        return report.sections()

    def section(self, report, section):  # pylint: disable=W0613
        ''' Return a formatted version of the section. '''
        kpis = []
        for kpi in section:
            kpis.append(self.kpi(kpi))
        return self.sep.join(kpis)

    def kpi(self, kpi):  # pylint: disable=W0613
        ''' Return a formatted version of the kpi. '''
        raise NotImplementedError  # pragma: no cover

    @staticmethod
    def postfix():
        ''' Override to return a postfix for the report. '''
        return ''

    @classmethod
    def __log_report(cls, report, done=False):
        ''' Report progress on formatting the report. '''
        done_string = 'done ' if done else ''
        logging.info('%s %sformatting report "%s"', cls.__name__, done_string, 
                     report)

    @classmethod
    def __log_section(cls, section):
        ''' Report progress on formatting the section. '''
        title = section.title()
        if section.subtitle():  # pragma: no branch
            title += ":%s" % section.subtitle()
        logging.info('%s formatting section "%s"', cls.__name__, title)