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



from .. import metric
from ..domain import Requirement


class TrackSpirit(Requirement):
    """ Track the team spirit. """
    _name = 'Track spirit'
    _metric_classes = (metric.TeamSpirit, metric.TeamSpiritAge)


class TrackAbsence(Requirement):
    """ Track the absence of team members. """
    _name = 'Track absence'
    _metric_classes = (metric.TeamAbsence,)
