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

os.environ["USER_AGENT"] = (
    "tomd"  # set before importing langchain things otherwise we get a warning
)
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
    Extracts content as Markdown from a URL and prints it to stdout.

    Assumes text content by default but supports YouTube videos.
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

        content = mdformat.text(content)
        cache.set(url, content)

    with redirect_stdout(sys.stdout):
        click.echo(content)
