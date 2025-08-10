# Copyright 2025 The Casibase Authors. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .record import _RecordSDK
from .store import _StoreSDK
from .task import _TaskSDK


class CasibaseSDK(_StoreSDK, _TaskSDK, _RecordSDK):

    def __init__(
        self, endpoint: str, client_id: str, client_secret: str, organization_name: str, application_name: str
    ):
        self.endpoint = endpoint
        self.client_id = client_id
        self.client_secret = client_secret
        self.organization_name = organization_name
        self.application_name = application_name
