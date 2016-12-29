"""
Copyright 2012-2016 Ministerie van Sociale Zaken en Werkgelegenheid

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
from __future__ import absolute_import

from . import metric


class LowerIsBetterMetric(metric.Metric):
    """ Metric for which a lower value means the metric is scoring better. """

    perfect_value = 0

    def value(self):
        raise NotImplementedError  # pragma: no cover

    def _is_below_target(self):
        """ Return whether the metric meets or exceeds the target. """
        # The metric is below target when the actual value is *higher*
        # than the target value, because the target value is the maximum value
        return not(self.perfect_value <= self.value() <= self.target()) or \
            super(LowerIsBetterMetric, self)._is_below_target()

    def _needs_immediate_action(self):
        """ Return whether the metric scores so bad that immediate action is required. """
        return not(self.perfect_value <= self.value() <= self.low_target()) or \
            super(LowerIsBetterMetric, self)._needs_immediate_action()

    def _is_value_better_than(self, target):
        return self.perfect_value <= self.value() <= target


class HigherIsBetterMetric(metric.Metric):
    """ Metric for which a higher value means the metric is scoring better. """

    def value(self):
        raise NotImplementedError  # pragma: no cover

    def _is_below_target(self):
        """ Return whether the metric meets or exceeds the target. """
        # The metric is below target when the actual value is *lower*
        # than the target value, because the target value is the minimum value
        return self.value() < self.target() or super(HigherIsBetterMetric, self)._is_below_target()

    def _needs_immediate_action(self):
        """ Return whether the metric scores so bad that immediate action is required. """
        return self.value() < self.low_target() or super(HigherIsBetterMetric, self)._needs_immediate_action()

    def _is_value_better_than(self, target):
        return self.value() >= target