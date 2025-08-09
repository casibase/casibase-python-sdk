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

import datetime
import unittest

import tests.test_util as test_util
from src.main import CasibaseSDK
from src.task import Task


class TaskTest(unittest.TestCase):
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

    def test_task(self):
        name = test_util.get_random_name("Task")
        # Add a new object
        task = Task.new(
            owner="admin",
            name=name,
            created_time=datetime.datetime.now().isoformat(),
            display_name=name,
        )

        sdk = TaskTest.get_sdk()
        try:
            sdk.add_task(task=task)
        except Exception as e:
            self.fail(f"Failed to add object: {e}")

        # Get all objects, check if our added object is inside the list
        try:
            tasks = sdk.get_tasks("admin")
        except Exception as e:
            self.fail(f"Failed to get objects: {e}")
        names = [item.name for item in tasks]
        self.assertIn(name, names, "Added object not found in list")

        # Get the object
        try:
            task_obj = sdk.get_task("admin", name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertEqual(task_obj.name, name)

        # Update the object
        updated_display_name = "Updated Task"
        task_obj.displayName = updated_display_name
        try:
            sdk.update_task(task=task_obj)
        except Exception as e:
            self.fail(f"Failed to update object: {e}")

        # Validate the update
        try:
            updated_task = sdk.get_task("admin", name)
        except Exception as e:
            self.fail(f"Failed to get updated object: {e}")
        self.assertEqual(updated_task.displayName, updated_display_name)

        # Delete the object
        try:
            sdk.delete_task(task=task)
        except Exception as e:
            self.fail(f"Failed to delete object: {e}")

        # Validate the deletion
        try:
            deleted_task = sdk.get_task("admin", name)
        except Exception as e:
            self.fail(f"Failed to get object: {e}")
        self.assertIsNone(deleted_task, "Failed to delete object, it's still retrievable")
