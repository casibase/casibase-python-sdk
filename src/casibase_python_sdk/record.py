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
from typing import Dict, Optional

import requests


class Record:
    def __init__(self):
        self.id: int = 0

        self.owner: str = ""
        self.name: str = ""
        self.createdTime: str = ""

        self.organization: str = ""
        self.clientIp: str = ""
        self.userAgent: str = ""
        self.user: str = ""
        self.method: str = ""
        self.requestUri: str = ""
        self.action: str = ""
        self.language: str = ""
        self.region: str = ""
        self.city: str = ""
        self.unit: str = ""
        self.section: str = ""

        self.object: str = ""
        self.response: str = ""

        self.provider: str = ""
        self.block: str = ""
        self.blockHash: str = ""
        self.transaction: str = ""

        self.provider2: str = ""
        self.block2: str = ""
        self.blockHash2: str = ""
        self.transaction2: str = ""

        self.isTriggered: bool = False
        self.needCommit: bool = False

    @classmethod
    def new(cls, owner, name, created_time, display_name) -> "Record":
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        return self

    @classmethod
    def from_dict(cls, data: dict) -> Optional["Record"]:
        if data is None:
            return None
        record = cls()
        for key, value in data.items():
            if hasattr(record, key):
                setattr(record, key, value)
        return record

    def __str__(self) -> str:
        return str(self.__dict__)

    def to_dict(self) -> dict:
        data = self.__dict__.copy()
        return data


class _RecordSDK:

    @property
    def headers(self) -> Dict:
        basic_auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("utf-8")
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Basic {basic_auth}",
        }

    def get_record(self, name: str) -> Optional[Record]:
        """
        Get a record by its name.
        :param name: The name of the record.
        :return: The Record object if found, otherwise None.
        """
        url = self.endpoint + "/api/get-record"
        params = {
            "id": f"{self.organization_name}/{name}",
        }
        r = requests.get(url, params)
        response = r.json()
        if response["status"] != "ok":
            raise Exception(response["msg"])
        return Record.from_dict(response["data"])

    def get_records(self, page_size: str, p: str) -> list[Record]:
        """
        Get a list of records.
        :param page_size: The number of records to return per page.
        :param p: The page number to retrieve.
        :return: A list of Record objects.
        """
        url = self.endpoint + "/api/get-records"
        params = {
            "pageSize": page_size,
            "p": p,
        }
        r = requests.get(url, params)
        response = r.json()
        if response.get("status") != "ok":
            raise Exception(response.get("msg"))
        records = []
        for record in response.get("data", []):
            records.append(Record.from_dict(record))
        return records

    def add_record(self, record: Record) -> Dict:
        """
        Add a new record.
        :param record: The Record object to add.
        :return: The added Record object.
        """
        url = self.endpoint + "/api/add-record"
        data = record.to_dict()
        r = requests.post(
            url,
            json=data,
            headers=self.headers,
        )
        response = r.json()
        if response.get("status") != "ok":
            raise Exception(response.get("msg"))
        return response

    def delete_record(self, record: Record) -> Dict:
        """
        Delete a record by its ID.
        :param record: The Record object to delete.
        :return: True if deletion was successful, otherwise False.
        """
        url = self.endpoint + "/api/delete-record"
        data = record.to_dict()
        r = requests.post(
            url,
            json=data,
            headers=self.headers,
        )
        response = r.json()
        if response.get("status") != "ok":
            raise Exception(response.get("msg"))
        return response

    def commit_record(self, record: Record) -> Dict:
        """
        Commit a record.
        :param record: The Record object to commit.
        :return: The committed Record object.
        """
        url = self.endpoint + "/api/commit-record"
        data = record.to_dict()
        r = requests.post(
            url,
            json=data,
            headers=self.headers,
        )
        response = r.json()
        if response.get("status") != "ok":
            raise Exception(response.get("msg"))
        return response

    def update_record(self, record: Record) -> Dict:
        """
        Update an existing record.
        :param record: The Record object to update.
        :return: The updated Record object.
        """
        url = self.endpoint + "/api/update-record"
        data = record.to_dict()
        params = {
            "id": f"{self.organization_name}/{record.name}",
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
