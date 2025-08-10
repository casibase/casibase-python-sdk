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

from .file import File
from .prompt import Prompt
from .properties import Properties


class Store:
    def __init__(self):
        self.owner: str = ""
        self.name: str = ""
        self.createdTime: str = ""
        self.displayName: str = ""

        self.storageProvider: str = ""
        self.storageSubpath: str = ""
        self.imageProvider: str = ""
        self.splitProvider: str = ""
        self.modelProvider: str = ""
        self.embeddingProvider: str = ""
        self.textToSpeechProvider: str = ""
        self.enableTtsStreaming: bool = False
        self.speechToTextProvider: str = ""
        self.agentProvider: str = ""

        self.memoryLimit: int = 0
        self.frequency: int = 0
        self.limitMinutes: int = 0
        self.knowledgeCount: int = 0
        self.suggestionCount: int = 0
        self.welcome: str = ""
        self.welcomeTitle: str = ""
        self.welcomeText: str = ""
        self.prompt: str = ""
        self.prompts: List[Prompt] = []
        self.themeColor: str = ""
        self.avatar: str = ""
        self.title: str = ""

        self.childStores: list[str] = []
        self.childModelProviders: list[str] = []
        self.showAutoRead: bool = False
        self.disableFileUpload: bool = False
        self.isDefault: bool = False
        self.state: str = ""

        self.chatCount: int = 0
        self.messageCount: int = 0

        self.fileTree: Optional[File] = None
        self.propertiesMap: Dict[str, Properties] = {}

    @classmethod
    def new(cls, owner, name, created_time, display_name) -> "Store":
        self = cls()
        self.owner = owner
        self.name = name
        self.createdTime = created_time
        self.displayName = display_name
        return self

    @classmethod
    def from_dict(cls, data: dict) -> Optional["Store"]:
        if data is None:
            return None
        store = cls()
        for key, value in data.items():
            if hasattr(store, key):
                setattr(store, key, value)
        return store

    def __str__(self) -> str:
        return str(self.__dict__)

    def to_dict(self) -> dict:
        data = self.__dict__.copy()
        data.pop("fileTree", None)
        return data


class _StoreSDK:
    @property
    def headers(self) -> Dict:
        basic_auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("utf-8")
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Basic {basic_auth}",
        }

    def get_store(self, owner, name) -> Optional[Store]:
        """
        Get a store by its owner and name.
        :param owner: The owner of the store.
        :param name: The name of the store.
        :return: The Store object if found, otherwise None.
        """
        url = f"{self.endpoint}/api/get-store"
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
            raise Exception(response.get("msg", "Failed to retrieve store"))

        return Store.from_dict(response.get("data"))

    def get_stores(self, page_size: int = 10, page: int = 1) -> List[Store]:
        """
        Get a list of stores.
        :param page_size: The number of stores to return per page.
        :param page: The page number to retrieve.
        :return: A list of Store objects.
        """
        url = f"{self.endpoint}/api/get-stores"
        params = {
            "pageSize": page_size,
            "p": page,
        }
        r = requests.get(
            url,
            headers=self.headers,
            params=params,
        )
        response = r.json()

        if response.get("status") != "ok":
            raise Exception(response.get("msg", "Failed to retrieve store list"))

        stores = []
        for store_data in response.get("data", []):
            store = Store.from_dict(store_data)
            if store:
                stores.append(store)
        return stores

    def add_store(self, store: Store) -> Dict:
        """
        Add a new store.
        :param store: The Store object to add.
        :return: The added Store object.
        """
        url = self.endpoint + "/api/add-store"
        data = store.to_dict()
        r = requests.post(
            url,
            json=data,
            headers=self.headers,
        )
        response = r.json()
        if response.get("status") != "ok":
            raise Exception(response.get("msg"))
        return response

    def delete_store(self, store: Store) -> Dict:
        """
        Delete a store by its owner and name.
        :param store: The Store object to delete.
        :return: The response from the server.
        """
        url = self.endpoint + "/api/delete-store"
        data = store.to_dict()
        r = requests.post(
            url,
            json=data,
            headers=self.headers,
        )
        response = r.json()
        if response.get("status") != "ok":
            raise Exception(response.get("msg"))
        return response

    def update_store(self, store: Store) -> Dict:
        """
        Update an existing store.
        :param store: The Store object to update.
        :return: The updated Store object.
        """
        url = self.endpoint + "/api/update-store"
        data = store.to_dict()
        params = {
            "id": f"{store.owner}/{store.name}",
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
