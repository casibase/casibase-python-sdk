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

import os
import unittest


def load_tests(loader, tests, pattern):
    top_level_dir = os.path.dirname(__file__)
    pattern = "test_*.py"
    exclude_files = []
    suite = unittest.TestSuite()

    # using loader.discover to find all test modules
    discovered_suite = loader.discover(top_level_dir, pattern=pattern)

    # add all tests to the suite
    for test in discovered_suite:
        if any(exclude_file in str(test) for exclude_file in exclude_files):
            continue
        suite.addTest(test)

    return suite
