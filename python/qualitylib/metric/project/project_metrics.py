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

from qualitylib import utils
from qualitylib.metric import LowerIsBetterMetric
from qualitylib.metric.metric_source_mixin import \
    TrelloActionsBoardMetricMixin, JiraMetricMixin
from qualitylib.metric_source import TrelloUnreachableException
from qualitylib.metric.quality_attributes import PROJECT_MANAGEMENT, PROGRESS, \
    TEST_QUALITY, SECURITY
import datetime


class RiskLog(LowerIsBetterMetric):
    ''' Metric for measuring the number of days since the risk log was last
        updated. '''

    norm_template = 'Het risicolog wordt minimaal een keer per %(target)d ' \
        'dagen bijgewerkt. Meer dan %(low_target)d dagen niet bijgewerkt is ' \
        'rood.'
    template = 'Het risicolog is %(value)d dagen geleden (op %(date)s) voor ' \
        'het laatst bijgewerkt.'
    target_value = 14
    low_target_value = 28
    quality_attribute = PROJECT_MANAGEMENT
    
    def __init__(self, *args, **kwargs):
        self.__trello_risklog_board = kwargs.pop('trello_risklog_board')
        super(RiskLog, self).__init__(*args, **kwargs)

    def value(self):
        return (datetime.datetime.now() - self._date()).days

    def _date(self):
        try:
            return self.__trello_risklog_board.date_of_last_update()
        except TrelloUnreachableException:
            return datetime.datetime.min

    def url(self):
        try:
            url = self.__trello_risklog_board.url()
        except TrelloUnreachableException:
            url = 'http://trello.com'
        return dict(Trello=url)


class ActionActivity(TrelloActionsBoardMetricMixin, LowerIsBetterMetric):
    ''' Metric for measuring the number of days since the actions were last
        updated. '''

    norm_template = 'De actie- en besluitenlijst wordt minimaal een keer ' \
        'per %(target)d dagen bijgewerkt. Meer dan %(low_target)d dagen ' \
        'niet bijgewerkt is rood.'
    template = 'De actie- en besluitenlijst is %(value)d dagen geleden ' \
        '(op %(date)s) voor het laatst bijgewerkt.'
    target_value = 7
    low_target_value = 14
    quality_attribute = PROJECT_MANAGEMENT

    def value(self):
        return (datetime.datetime.now() - self._date()).days

    def _date(self):
        try:
            return self._trello_actions_board.date_of_last_update()
        except TrelloUnreachableException:
            return datetime.datetime.min

    def url(self):
        try:
            url = self._trello_actions_board.url()
        except TrelloUnreachableException:
            url = 'http://trello.com'
        return dict(Trello=url)


class ActionAge(TrelloActionsBoardMetricMixin, LowerIsBetterMetric):
    ''' Metric for measuring the age of individual actions. '''

    norm_template = 'Geen van de acties en besluiten in de actie- en ' \
        'besluitenlijst is te laat of te lang (14 dagen) niet bijgewerkt.' \
        'Meer dan %(low_target)d acties te laat of te lang niet bijgewerkt ' \
        'is rood.'
    template = '%(value)d acties uit de actie- en besluitenlijst zijn te ' \
        'laat of te lang (14 dagen) niet bijgewerkt.'
    target_value = 0
    low_target_value = 3
    quality_attribute = PROJECT_MANAGEMENT

    def value(self):
        try:
            return self._trello_actions_board.nr_of_over_due_or_inactive_cards()
        except TrelloUnreachableException:
            return -1

    def url(self):
        try:
            return self._trello_actions_board.over_due_or_inactive_cards_url()
        except TrelloUnreachableException:
            return dict(Trello='http://trello.com')

    def url_label(self):
        return 'Niet bijgewerkte of te late acties'


class ReleaseAge(LowerIsBetterMetric):
    ''' Metric for measuring the age of the last release. '''
    
    norm_template = 'De laatste release is niet ouder dan %(target)d ' \
        'dagen. Ouder dan %(low_target)d dagen is rood.'
    template = 'De laatste %(archive_name)s-release is %(value)d dag(en) oud.'
    target_value = 3 * 7
    low_target_value = 4 * 7
    quality_attribute = PROGRESS
    
    def __init__(self, *args, **kwargs):
        self.__release_archive = kwargs.pop('release_archive')
        super(ReleaseAge, self).__init__(*args, **kwargs)

    def value(self):
        return (datetime.datetime.now() - self._date()).days
    
    def _date(self):
        return self.__release_archive.date_of_most_recent_file()
        
    def url(self):
        return {'Release-archief %s' % self.__release_archive.name(): 
                self.__release_archive.url()}
        
    def _parameters(self):  
        # pylint: disable=protected-access
        parameters = super(ReleaseAge, self)._parameters()
        parameters['archive_name'] = self.__release_archive.name()
        return parameters


class OpenBugs(JiraMetricMixin, LowerIsBetterMetric):
    ''' Metric for measuring the number of open bug reports. '''
    
    norm_template = 'Het aantal open bug reports is minder dan %(target)d. ' \
       'Meer dan %(low_target)d is rood.'
    template = 'Het aantal open bug reports is %(value)d.'
    target_value = 50
    low_target_value = 100
    quality_attribute = PROGRESS
    
    def value(self):
        return self._jira.nr_open_bugs()
    
    def url(self):
        return {'Jira': self._jira.nr_open_bugs_url()}
    
    
class OpenSecurityBugs(JiraMetricMixin, LowerIsBetterMetric):
    ''' Metric for measuring the number of open security bugs. '''
    
    norm_template = 'Het aantal beveiliging bug reports dat meer dan een ' \
        'sprint open staat is minder dan %(target)d. Meer dan %(low_target)d ' \
        'is rood.'
    template = 'Het aantal beveiliging bug reports dat meer dan een sprint ' \
        'open staat is %(value)d.'
    target_value = 0
    low_target_value = 3
    quality_attribute = SECURITY

    def value(self):
        return self._jira.nr_open_security_bugs()
    
    def url(self):
        return {'Jira': self._jira.nr_open_security_bugs_url()}
    

class BlockingTestIssues(JiraMetricMixin, LowerIsBetterMetric):
    ''' Metric for measuring the number of blocking test issues opened the
        previous month. '''
    
    norm_template = 'Het aantal geopende blokkerende testbevindingen is ' \
        'maximaal %(target)d. Meer dan %(low_target)d is rood.'
    template = 'Het aantal geopende blokkerende testbevindingen in de vorige ' \
        'maand (%(month)s) was %(value)d.'
    target_value = 0
    low_target_value = 1
    quality_attribute = TEST_QUALITY
    
    def value(self):
        return self._jira.nr_blocking_test_issues()
    
    def url(self):
        return {'Jira': self._jira.nr_blocking_test_issues_url()}
    
    def _parameters(self):
        # pylint: disable=protected-access
        parameters = super(BlockingTestIssues, self)._parameters()
        parameters['month'] = utils.format_month(utils.month_ago())
        return parameters