# Copyright 2025 Notedown Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Configuration settings for tomd.
"""

# Version information
try:
    from importlib.metadata import version

    VERSION = version("tomd")
except ImportError:  # Fallback for PyInstaller bundle
    VERSION = "0.1.0"  # This will be replaced during build

# HTTP request settings
USER_AGENT = f"tomd/{VERSION}"

# Default HTTP headers for all requests
DEFAULT_HEADERS = {"User-Agent": USER_AGENT}
