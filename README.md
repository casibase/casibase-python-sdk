# casibase-python-sdk

[![build Status](https://github.com/casdoor/casdoor-python-sdk/actions/workflows/build.yml/badge.svg)](https://github.com/casdoor/casdoor-python-sdk/actions/workflows/build.yml)
[![Coverage Status](https://coveralls.io/repos/github/casdoor/casdoor-python-sdk/badge.svg)](https://coveralls.io/github/casdoor/casdoor-python-sdk)
[![Version](https://img.shields.io/pypi/v/casibase-python-sdk.svg)](https://pypi.org/project/casibase-python-sdk)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/casibase-python-sdk.svg)](https://pypi.org/project/casibase-python-sdk)
[![Pyversions](https://img.shields.io/pypi/pyversions/casibase-python-sdk.svg)](https://pypi.org/project/casibase-python-sdk)
[![Download](https://static.pepy.tech/badge/casibase-python-sdk)](https://pypi.org/project/casibase-python-sdk/)
[![License](https://img.shields.io/pypi/l/casibase-python-sdk.svg)](https://pypi.org/project/casibase-python-sdk/)
[![Discord](https://img.shields.io/discord/1022748306096537660?logo=discord&label=discord&color=5865F2)](https://discord.gg/5rPsrAzK7S)
This is the Python SDK for Casibase, which allows you to easily call Casibase's API.

casibase-python-sdk is available on PyPI:

```console
pip install casibase-python-sdk
```

Casibase SDK is simple to use. We will show you the steps below.

## Step1. Init Config

Initialization requires 5 parameters, which are all str type:

| Name (in order)  | Must | Description                                         |
| ---------------- | ---- | --------------------------------------------------- |
| endpoint         | Yes  | Casdoor Server Url, such as `https://demo-admin.casibase.com` |
| client_id        | Yes  | Application.client_id                               |
| client_secret    | Yes  | Application.client_secret                           |
| org_name         | Yes  | Organization name                                   |
| application_name | Yes  | Application name                                    |

```python
from casibase_python_sdk import CasibaseSDK

sdk = CasibaseSDK(
    endpoint,
    client_id,
    client_secret,
    organization_name,
    application_name,
)

```

## Step2. Record Operations  

Used for logging operations, blockchain events, etc.  

- Create: `record = Record.new(...)`; `sdk.add_record(record)`  
- Query: `record_obj = sdk.get_record("name")`  
- Update: `record_obj.attr = "new_val"`; `sdk.update_record(record_obj)`  
- Delete: `sdk.delete_record(record_obj)`  

## Step3. Store Operations  

Used for managing knowledge bases, model configurations, etc.  

- Create: `store = Store.new(...)`; `sdk.add_store(store)`  
- Query: `store_obj = sdk.get_store(owner="admin", name="name")`  
- Update: `store_obj.attr = "new_val"`; `sdk.update_store(store_obj)`  
- Delete: `sdk.delete_store(store_obj)`  

## Step4. Task Operations  

Used for managing tasks, jobs, etc.  

- Create: `task = Task.new(...)`; `sdk.add_task(task)`  
- Query: `task_obj = sdk.get_task(owner="admin", name="name")`  
- Update: `task_obj.attr = "new_val"`; `sdk.update_task(task_obj)`  
- Delete: `sdk.delete_task(task_obj)`  
