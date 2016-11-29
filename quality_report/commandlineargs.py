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

from argparse import ArgumentParser

import quality_report


def parse():
    """ Parse the command line arguments. """
    parser = ArgumentParser(description='Generate a quality report.')
    parser.add_argument('--project', help='folder with project definition file and history')
    parser.add_argument('--report', help='folder to write the HTML report in')
    parser.add_argument('--log', default="WARNING", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help="log level (WARNING by default)")
    parser.add_argument('--version', action='version', version=quality_report.VERSION)
    args = parser.parse_args()
    if not args.project:
        parser.error('Need a project folder')
    if not args.report:
        parser.error('Need a report folder')
    return args