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

import datetime, sys, requests
from typing import Dict, Any, Optional
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from .config import DEFAULT_HEADERS


def extract_title_from_html(url: str) -> Optional[str]:
    """
    Extract the title from a webpage's HTML.

    Args:
        url: The URL to fetch and extract title from

    Returns:
        The extracted title or None if not found/error occurs
    """
    try:
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Try to get title from various sources in order of preference

        # 1. Open Graph title (often more descriptive)
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            return og_title["content"].strip()

        # 2. Twitter card title
        twitter_title = soup.find("meta", attrs={"name": "twitter:title"})
        if twitter_title and twitter_title.get("content"):
            return twitter_title["content"].strip()

        # 3. Standard HTML title tag
        if soup.title and soup.title.string:
            return soup.title.string.strip()

        # 4. First h1 tag
        h1 = soup.find("h1")
        if h1 and h1.text:
            return h1.text.strip()

        return None

    except Exception as e:
        print(f"Error extracting title from HTML: {e}", file=sys.stderr)
        return None


def extract_metadata(url: str, title: Optional[str] = None) -> Dict[str, Any]:
    """
    Extract metadata for front matter from a URL and optional title.
    If title is not provided, attempts to extract it from the HTML.

    Args:
        url: The source URL
        title: Optional title, if already extracted

    Returns:
        Dictionary containing metadata for front matter
    """
    metadata = {
        "url": url,
        "date_extracted": datetime.datetime.now().strftime("%Y-%m-%d"),
    }

    # Handle title extraction
    if title:
        metadata["title"] = title
    else:
        # Try to extract title from HTML
        extracted_title = extract_title_from_html(url)
        if extracted_title:
            metadata["title"] = extracted_title

    return metadata


def add_front_matter(content: str, metadata: Dict[str, Any]) -> str:
    """
    Adds YAML front matter to markdown content.

    Args:
        content: The markdown content
        metadata: Dictionary of metadata to include in front matter

    Returns:
        Content with front matter prepended
    """

    # Build the front matter
    front_matter_lines = ["---"]
    for key, value in metadata.items():
        if isinstance(value, str):
            # Escape quotes in string values
            value = value.replace('"', '\\"')
            front_matter_lines.append(f'{key}: "{value}"')
        else:
            front_matter_lines.append(f"{key}: {value}")
    front_matter_lines.append("---")
    front_matter_lines.append("")  # Empty line after front matter

    # Combine front matter with content
    return "\n".join(front_matter_lines) + "\n" + content
