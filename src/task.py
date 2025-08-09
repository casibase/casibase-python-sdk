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

import base64
from typing import Dict, List, Optional

import requests

from .usage_info import UsageInfo


class Task:
    def __init__(self):
        self.owner: str = ""
        self.name: str = ""
        self.createdTime: str = ""
        self.displayName: str = ""
        self.provider: str = ""
        self.providers: list[str] = []
        self.type: str = ""
        self.subject: str = ""
        self.topic: str = ""
        self.result: str = ""
        self.activity: str = ""
        self.grade: str = ""
        self.modelUsageMap: Dict[str, UsageInfo] = {}
        self.application: str = ""
        self.path: str = ""
        self.text: str = ""
        self.example: str = ""
        self.labels: list[str] = []
        self.log: str = ""

    @classmethod
    def new(cls, owner, name, created_time, display_name) -> "Task":
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        return self

    @classmethod
    def from_dict(cls, data: dict) -> Optional["Task"]:
        if data is None:
            return None
        task = cls()
        for key, value in data.items():
            if hasattr(task, key):
                setattr(task, key, value)
        return task

    def __str__(self) -> str:
        return str(self.__dict__)

    def to_dict(self) -> dict:
        data = self.__dict__.copy()
        return data


class _TaskSDK:

    @property
    def headers(self) -> Dict:
        basic_auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("utf-8")
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Basic {basic_auth}",
        }

    def get_task(self, owner: str, name: str) -> Optional[Task]:
        """
        Get a task by its owner and name.
        :param owner: The owner of the task.
        :param name: The name of the task.
        :return: The Task object if found, otherwise None.
        """
        url = f"{self.endpoint}/api/get-task"
        params = {
            "id": f"{owner}/{name}",
        }
        r = requests.get(
            url,
            headers=self.headers,
            params=params,
        )
        response = r.json()

        if response.get("status") != "ok":
            raise Exception(response.get("msg", "Failed to get task"))

        return Task.from_dict(response.get("data"))

    def get_tasks(self, owner: str) -> List[Task]:
        """
        Get a list of tasks for a specific owner.
        :param owner: The owner of the tasks.
        :return: A list of Task objects.
        """
        url = f"{self.endpoint}/api/get-tasks"
        params = {
            "owner": owner,
        }
        r = requests.get(
            url,
            headers=self.headers,
            params=params,
        )
        response = r.json()

        if response.get("status") != "ok":
            raise Exception(response.get("msg", "Failed to obtain task list"))

        tasks = []
        for task_data in response.get("data", []):
            task = Task.from_dict(task_data)
            if task:
                tasks.append(task)
        return tasks

    def add_task(self, task: Task) -> Dict:
        """
        Add a new task.
        :param task: The Task object to add.
        :return: The added Task object.
        """
        url = self.endpoint + "/api/add-task"
        data = task.to_dict()
        r = requests.post(url, json=data, headers=self.headers)
        response = r.json()
        if response.get("status") != "ok":
            raise Exception(response.get("msg"))
        return response

    def delete_task(self, task: Task) -> Dict:
        """
        Delete a task by its owner and name.
        :param task: The Task object to delete.
        :return: The response from the server.
        """
        url = self.endpoint + "/api/delete-task"
        data = task.to_dict()
        r = requests.post(url, json=data, headers=self.headers)
        response = r.json()
        if response.get("status") != "ok":
            raise Exception(response.get("msg"))
        return response

    def update_task(self, task: Task) -> Dict:
        """
        Update an existing task.
        :param task: The Task object to update.
        :return: The updated Task object.
        """
        url = self.endpoint + "/api/update-task"
        data = task.to_dict()
        params = {
            "id": f"{task.owner}/{task.name}",
        }
        r = requests.post(
            url,
            json=data,
            headers=self.headers,
            params=params,
        )
        response = r.json()
        if response.get("status") != "ok":
            raise Exception(response.get("msg"))
        return response
