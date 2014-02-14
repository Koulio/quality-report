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

import datetime
import unittest
from qualitylib import metric, utils
from qualitylib.metric_source import TrelloUnreachableException


class FakeBoard(object):
    ''' Fake a Trello board. '''
    @staticmethod
    def url():
        ''' Return a fake url. '''
        return 'http://trello/board'
    
    @staticmethod
    def date_of_last_update():
        ''' Fake the date of the last update. '''
        return datetime.datetime.now() - datetime.timedelta(minutes=1)
    
    @staticmethod
    def over_due_or_inactive_cards_url():
        ''' Fake the url. '''
        return 'http://trello/over_due_or_inactive_cards'
    
    @staticmethod
    def nr_of_over_due_or_inactive_cards():  # pylint: disable=invalid-name
        ''' Fake the number. '''
        return 5


class UnreachableBoard(object):
    ''' Pretend that Trello is down. '''
    @staticmethod
    def url():
        ''' Fake that Trello is down. '''
        raise TrelloUnreachableException
    
    @staticmethod
    def date_of_last_update():
        ''' Fake that Trello is down. '''
        raise TrelloUnreachableException

    @staticmethod
    def nr_of_over_due_or_inactive_cards():  # pylint: disable=invalid-name
        ''' Fake that Trello is down. '''
        raise TrelloUnreachableException
    
    @staticmethod
    def over_due_or_inactive_cards_url():
        ''' Fake that Trello is down. '''
        raise TrelloUnreachableException
    

class RiskLogTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for therisk log metric. '''

    def setUp(self):  # pylint: disable=invalid-name
        self.__metric = metric.RiskLog(trello_risklog_board=FakeBoard(),
                                       wiki=None, history=None)

    def test_url(self):
        ''' Test that the url of the metric uses the url of the risk log 
            board. '''
        self.assertEqual(dict(Trello=FakeBoard().url()), self.__metric.url())
        
    def test_value(self):
        ''' Test that the value is the number of days since the last 
            update. '''
        self.assertEqual(0, self.__metric.value())


class UnreachableRiskLogTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the risk log metric when Trello is unreachable. '''

    def setUp(self):  # pylint: disable=invalid-name
        self.__metric = metric.RiskLog(trello_risklog_board=UnreachableBoard(),
                                       wiki=None, history=None)

    def test_url(self):
        ''' Test that the url of the metric uses the url of the risk log 
            board. '''
        self.assertEqual(dict(Trello='http://trello.com'),
                         self.__metric.url())
        
    def test_value(self):
        ''' Test that the value is the number of days since the last 
            update. '''
        days = (datetime.datetime.now() - datetime.datetime(1, 1, 1)).days
        self.assertEqual(days, self.__metric.value())


class ActionActivityTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the action activity metric. '''

    def setUp(self):  # pylint: disable=invalid-name
        self.__metric = metric.ActionActivity(wiki=None, history=None,
                                              trello_actions_board=FakeBoard())
        
    def test_value(self):
        ''' Test that the board has been updated today. '''
        self.assertEqual(0, self.__metric.value())
        
    def test_url(self):
        ''' Test that url of the metric is equal to the url of the board. '''
        self.assertEqual(dict(Trello=FakeBoard().url()), self.__metric.url())


class UnreachableActionActivityTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the action activity metric when Trello is 
        unreachable. '''

    def setUp(self):  # pylint: disable=invalid-name
        self.__metric = metric.ActionActivity(wiki=None, history=None,
                                trello_actions_board=UnreachableBoard())
        
    def test_value(self):
        ''' Test that the board has been updated today. '''
        days = (datetime.datetime.now() - datetime.datetime(1, 1, 1)).days
        self.assertEqual(days, self.__metric.value())
        
    def test_url(self):
        ''' Test that url of the metric is equal to the url of the board. '''
        self.assertEqual(dict(Trello='http://trello.com'), self.__metric.url())


class ActionAgeTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the action age metric. '''

    def setUp(self):  # pylint: disable=invalid-name
        self.__metric = metric.ActionAge(wiki=None, history=None,
                                         trello_actions_board=FakeBoard())
        
    def test_value(self):
        ''' Test that the metric value equals the number of over due or 
            inactive cards. '''
        self.assertEqual(FakeBoard().nr_of_over_due_or_inactive_cards(), 
                         self.__metric.value())
        
    def test_url(self):
        ''' Test that url of the metric is equal to the url for the over due
            or inactive cards. '''
        self.assertEqual(FakeBoard().over_due_or_inactive_cards_url(), 
                         self.__metric.url())
        
    def test_url_label(self):
        ''' Test that the metric has a url label. '''
        self.failUnless(self.__metric.url_label())


class UnreachableActionAgeTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the action age metric when Trello is unreachable. '''

    def setUp(self):  # pylint: disable=invalid-name
        self.__metric = metric.ActionAge(wiki=None, history=None,
                                trello_actions_board=UnreachableBoard())

    def test_value(self):
        ''' Test that the value indicates a problem. '''
        self.assertEqual(-1, self.__metric.value())
        
    def test_url(self):
        ''' Test that url of the metric is equal to the url of the board. '''
        self.assertEqual(dict(Trello='http://trello.com'), self.__metric.url())


class FakeArchive(object):
    ''' Fake a release archive. '''
    @staticmethod
    def date_of_most_recent_file():
        ''' Return the date of the most recent file in the archive. '''
        return datetime.datetime.now() - datetime.timedelta(minutes=1)
    
    @staticmethod
    def url():
        ''' Return a fake url. '''
        return 'http://archive'
    
    @staticmethod
    def name():
        ''' Return a fake name. '''
        return 'ABC'
    
    
class FakeJira(object):
    ''' Fake Jira. '''
    @staticmethod
    def nr_open_bugs_url():
        ''' Return a fake url for the nr of open bugs query. '''
        return 'http://openbugs/'
    
    @staticmethod
    def nr_blocking_test_issues_url():
        ''' Return a fake url for the number of blocking test issues query. '''
        return 'http://blockingissues/'
    
    @staticmethod
    def nr_open_bugs():
        ''' Return a fake number of open bugs. '''
        return 7

    @staticmethod
    def nr_blocking_test_issues():
        ''' Return a fake number of blocking test issues. '''
        return 5
        
    @staticmethod
    def nr_open_security_bugs():
        ''' Return a fake number of open security bugs. '''
        return 7

    @staticmethod
    def nr_open_security_bugs_url():
        ''' Return a fake url for the nr of open security bugs query. '''
        return 'http://opensecuritybugs/'
    

class ReleaseAgeTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the release age metric. '''

    def setUp(self):  # pylint: disable=invalid-name
        self.__metric = metric.ReleaseAge(wiki=None, history=None,
                                          release_archive=FakeArchive())
        
    def test_value(self):
        ''' Test that the value is correct. '''
        self.assertEqual(0, self.__metric.value())
        
    def test_url(self):
        ''' Test that the url is correct. '''
        self.assertEqual({'Release-archief ABC': 'http://archive'}, 
                         self.__metric.url())
        
    def test_report(self):
        ''' Test that the report is correct. '''
        self.assertEqual('De laatste ABC-release is 0 dag(en) oud.', 
                         self.__metric.report())
        
        
class OpenBugsTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the number of open bugs metric. '''

    def setUp(self):  # pylint: disable=invalid-name
        self.__metric = metric.OpenBugs(wiki=None, history=None,
                                        jira=FakeJira())
        
    def test_value(self):
        ''' Test that the value is correct. '''
        self.assertEqual(FakeJira.nr_open_bugs(), self.__metric.value())
        
    def test_url(self):
        ''' Test that the url is correct. '''
        self.assertEqual({'Jira': FakeJira.nr_open_bugs_url()}, 
                         self.__metric.url())


class OpenSecurityBugsTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the number of open security bugs metric. '''

    def setUp(self):  # pylint: disable=invalid-name
        self.__metric = metric.OpenSecurityBugs(wiki=None, history=None,
                                                jira=FakeJira())
        
    def test_value(self):
        ''' Test that the value is correct. '''
        self.assertEqual(FakeJira.nr_open_security_bugs(), 
                         self.__metric.value())
        
    def test_url(self):
        ''' Test that the url is correct. '''
        self.assertEqual({'Jira': FakeJira.nr_open_security_bugs_url()}, 
                         self.__metric.url())


class BlockingTestIssuesTest(unittest.TestCase):
    # pylint: disable=too-many-public-methods
    ''' Unit tests for the number of blocking test issues metric. '''

    def setUp(self):  # pylint: disable=invalid-name
        self.__metric = metric.BlockingTestIssues(wiki=None, history=None,
                                                  jira=FakeJira())
        
    def test_value(self):
        ''' Test that the value is correct. '''
        self.assertEqual(FakeJira.nr_blocking_test_issues(), 
                         self.__metric.value())
        
    def test_url(self):
        ''' Test that the url is correct. '''
        self.assertEqual({'Jira': FakeJira.nr_blocking_test_issues_url()}, 
                         self.__metric.url())
        
    def test_report(self):
        ''' Test that the report is correct. '''
        month = utils.format_month(utils.month_ago())
        self.assertEqual('Het aantal geopende blokkerende testbevindingen in '\
                         'de vorige maand (%s) was 5.' % month, 
                         self.__metric.report())