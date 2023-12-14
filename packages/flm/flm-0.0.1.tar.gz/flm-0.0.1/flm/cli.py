#!/usr/bin/env python

"""
Copyright.

Licensed under the Apache License, Version 2.0 (the "License"); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at:

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations
under the License.
"""

from argparse import ArgumentParser
from flm.get_banner import get_banner
from pkg_resources import get_distribution

package_version = get_distribution('flm').version


def main():
    """
    Package's entry point.

    Here, application's settings are read from the command line.
    """
    parser = ArgumentParser(
        description='flm - CLI',
        prog='flm'
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s ' + package_version
    )

    parser.add_argument(
        '-b',
        '--banner',
        action='store_true',
        help="Print flm's banner"
    )

    args = parser.parse_args()

    # print("baremagic called with the folowing parameters")
    # print(parser.parse_args())

    if args.banner:
        print(get_banner())
        exit()
