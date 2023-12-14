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

import json

from nectarclient_lib import base


class OutageUpdate(base.Resource):

    date_fields = ['time']

    def __repr__(self):
        return "<OutageUpdate %s>" % self.time


class Outage(base.Resource):

    date_fields = ['scheduled_start', 'scheduled_end', 'start', 'end']

    def __init__(self, manager, info, loaded=False, resp=None):
        super().__init__(manager, info, loaded, resp)
        raw_updates = self.updates
        self.updates = []
        for update in raw_updates:
            self.updates.append(OutageUpdate(manager, update))

    def __repr__(self):
        return "<Outage %s>" % self.id


class OutageManager(base.BasicManager):

    base_url = 'v1/outages'
    resource_class = Outage

    def update(self, outage_id, **kwargs):
        data = json.dumps(kwargs)
        return self._update(f"/{self.base_url}/{outage_id}/", data=data)
