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

import click, warnings, sys, mdformat, os
from pathlib import Path
from contextlib import redirect_stdout
from .cache import FileSystemKV
from .frontmatter import extract_metadata, add_front_matter
from .config import USER_AGENT

# Set environment variable for langchain
os.environ["USER_AGENT"] = USER_AGENT

from .youtube import extract_youtube_transcription
from .article import extract_article_remote
from .split import split

cache_dir = Path.home() / ".cache" / "tomd"
warnings.filterwarnings("ignore")


@click.command()
@click.argument("url")
@click.option(
    "--disable-cache",
    is_flag=True,
    default=False,
    help="force extraction even if cached result is present",
)
def extract(url: str, disable_cache: bool):
    """
    Extract web content as Markdown from a URL and print to stdout.

    Automatically detects and handles different content types:
    - YouTube videos: Extracts and formats video transcription
    - Web articles: Extracts main article content

    Results are cached locally for faster repeat access. Use --disable-cache to force
    fresh extraction.

    The output includes YAML frontmatter with metadata like title, source URL and
    extraction date.
    """

    content = ""
    cache = FileSystemKV(str(cache_dir.resolve()))

    if not disable_cache:
        try:
            content = cache.get(url)
            click.echo("cache hit, source previously processed", err=True)
            click.echo(content)
            return
        except:
            click.echo("cache miss, source not previously processed", err=True)

    with redirect_stdout(sys.stderr):
        match url:
            case m if "youtube.com" in m or "youtu.be" in m:
                click.echo("inferred YouTube video", err=True)
                transcript = extract_youtube_transcription(url)
                content = split(transcript)

            case _:
                click.echo(
                    "no specific format detected, defaulting to text article", err=True
                )
                content = extract_article_remote(url)

        # Format content
        content = mdformat.text(content)

        # Create metadata and add front matter
        metadata = extract_metadata(url)
        content_with_front_matter = add_front_matter(content, metadata)

        # Cache the result
        cache.set(url, content_with_front_matter)

    with redirect_stdout(sys.stdout):
        click.echo(content_with_front_matter)
