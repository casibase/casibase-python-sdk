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

import unittest

import tests.test_util as test_util
from src.main import CasibaseSDK
from src.record import Record


class RecordTest(unittest.TestCase):
    @staticmethod
    def get_sdk():
        sdk = CasibaseSDK(
            test_util.TestEndpoint,
            test_util.TestClientId,
            test_util.TestClientSecret,
            test_util.TestOrganization,
            test_util.TestApplication,
        )
        return sdk

    def test_record(self):
        name = test_util.get_random_name("Record")
        sdk = RecordTest.get_sdk()

        # Add a new object
        record = Record.from_dict(
            {
                "owner": sdk.organization_name,
                "name": name,
                "createdTime": "2025-08-04T14:50:41+08:00",
                "organization": sdk.organization_name,
                "clientIp": "115.233.205.178",
                "userAgent": "",
                "user": "admin",
                "method": "POST",
                "requestUri": "/api/signout",
                "action": "signout",
                "language": "en",
                "region": "China",
                "city": "N/A",
                "unit": "",
                "section": "",
                "object": "",
                "response": '{"status":"ok","msg":""}',
                "provider": "provider_blockchain_chainmaker",
                "block": "",
                "blockHash": "",
                "transaction": "",
                "provider2": "provider_blockchain_ethereum",
                "block2": "",
                "blockHash2": "",
                "transaction2": "",
                "isTriggered": False,
                "needCommit": False,
            }
        )

        try:
            result = sdk.add_record(record)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")
        name = result.get("data2").get("name")
        self.assertNotEqual(name, "", "Failed to add object, name is empty")

        # Get all objects, check if our added object is inside the list
        try:
            records = sdk.get_records("500", "1")
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in records]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            record_obj = sdk.get_record(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(record_obj.name, name)

        # Update the object
        update_language = "zh"
        record_obj.language = update_language
        try:
            sdk.update_record(record_obj)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_record = sdk.get_record(name)
        except Exception as e:
            self.fail(f"Failed to get updated object: {e}")
        self.assertEqual(updated_record.language, update_language)

        # Delete the object
        try:
            sdk.delete_record(record_obj)
        except Exception as e:
            self.fail(f"Failed to delete object: {e}")

        # Validate the deletion
        try:
            deleted_record = sdk.get_record(name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_record, "Failed to delete object, it's still retrievable")
