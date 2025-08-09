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

import random

TestEndpoint = "https://demo-admin.casibase.com"
TestClientId = "af6b5aa958822fb9dc33"
TestClientSecret = "8bc3010c1c951c8d876b1f311a901ff8deeb93bc"
TestOrganization = "casbin"
TestApplication = "app-casibase"


def get_random_code(length):
    std_nums = "0123456789"
    result = "".join(random.choice(std_nums) for _ in range(length))
    return result


def get_random_name(prefix):
    return f"{prefix}_{get_random_code(6)}"
