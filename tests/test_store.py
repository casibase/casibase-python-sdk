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
from src.store import Store


class StoreTest(unittest.TestCase):
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

    def test_store(self):
        owner = "admin"
        name = test_util.get_random_name("Store")
        # Add a new object
        store = Store.from_dict(
            {
                "owner": owner,
                "name": name,
                "createdTime": "2025-08-09T11:46:59+08:00",
                "displayName": "New - " + name,
                "storageProvider": "provider-storage-built-in",
                "storageSubpath": name,
                "imageProvider": "",
                "splitProvider": "Default",
                "searchProvider": "Default",
                "modelProvider": "",
                "embeddingProvider": "",
                "textToSpeechProvider": "Browser Built-In",
                "enableTtsStreaming": False,
                "speechToTextProvider": "Browser Built-In",
                "agentProvider": "",
                "memoryLimit": 5,
                "frequency": 10000,
                "limitMinutes": 10,
                "knowledgeCount": 5,
                "suggestionCount": 3,
                "welcome": "Hello",
                "welcomeTitle": "Hello, I'm Casibase AI Assistant",
                "welcomeText": "I'm here to help answer your questions",
                "prompt": "You are an expert in your field and you specialize in using your knowledge.",
                "prompts": None,
                "themeColor": "#5036d3",
                "avatar": "https://cdn.casibase.com/img/casibase.png",
                "title": "Title - " + name,
                "childStores": None,
                "childModelProviders": None,
                "showAutoRead": False,
                "disableFileUpload": False,
                "isDefault": False,
                "state": "Active",
                "chatCount": 0,
                "messageCount": 0,
                "fileTree": None,
                "propertiesMap": {},
            }
        )

        sdk = StoreTest.get_sdk()
        try:
            sdk.add_store(store)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")

        # Get all objects, check if our added object is inside the list
        try:
            stores = sdk.get_stores()
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in stores]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            store_obj = sdk.get_store(owner=owner, name=name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(store_obj.name, name)

        # Update the object
        updated_displayName = "Updated Store"
        store_obj.displayName = updated_displayName
        try:
            sdk.update_store(store_obj)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_store = sdk.get_store(owner=owner, name=name)
        except Exception as e:
            self.fail(f"Failed to get updated object: {e}")
        self.assertEqual(updated_store.displayName, updated_displayName)

        # Delete the object
        try:
            sdk.delete_store(store_obj)
        except Exception as e:
            self.fail(f"Failed to delete object: {e}")

        # Validate the deletion
        try:
            deleted_store = sdk.get_store(owner=owner, name=name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_store, "Failed to delete object, it's still retrievable")
