#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import datetime

from langstrothclient.tests.unit import utils
from langstrothclient.tests.unit.v1 import fakes
from langstrothclient.v1 import outages


class OutagesTest(utils.TestCase):

    def setUp(self):
        super().setUp()
        self.cs = fakes.FakeClient()

    def test_outage_list(self):
        ol = self.cs.outages.list()
        self.cs.assert_called('GET', '/v1/outages/')
        for o in ol:
            self.assertIsInstance(o, outages.Outage)
        self.assertEqual(3, len(ol))

    def test_outage_get(self):
        o = self.cs.outages.get(123)
        self.cs.assert_called('GET', '/v1/outages/123/')
        self.assertIsInstance(o, outages.Outage)
        self.assertEqual(123, o.id)

    def test_attrs(self):
        o = self.cs.outages.get(123)
        self.assertIsInstance(o.scheduled_start, datetime.datetime)
        self.assertIsInstance(o.updates[0].time, datetime.datetime)

        self.assertEqual(3, o.severity)
        self.assertEqual('Severe', o.severity_display)
        self.assertEqual('Scheduled', o.scheduled_display)
        self.assertEqual('Completed', o.status_display)
        self.assertEqual(
            datetime.datetime(2023, 9, 14, 10, 39, 51,
                              tzinfo=datetime.timezone(
                                  datetime.timedelta(seconds=36000))),
            o.start)
        self.assertEqual(
            datetime.datetime(2023, 10, 3, 16, 27, 52,
                              tzinfo=datetime.timezone(
                                  datetime.timedelta(seconds=36000))),
            o.end)
