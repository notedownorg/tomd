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

import PyInstaller.__main__
from pathlib import Path

HERE = Path(__file__).parent.absolute()
path_to_main = str(HERE / "run.py")


def bundle():
    PyInstaller.__main__.run(
        [
            path_to_main,
            "--contents-directory",
            "tomd_internal",
            "--name",
            "tomd",
            "--noconfirm",
            # Imports that are not automatically detected
            "--hidden-import",
            "pydantic.deprecated.decorator",
            "--hidden-import",
            "skops.io._sklearn",
            "--hidden-import",
            "skops.io._quantile_forest",
            "--hidden-import",
            "skops.io.old",
            "--hidden-import",
            "skops.io.old._general_v0",
            "--hidden-import",
            "skops.io.old._numpy_v0",
            "--hidden-import",
            "skops.io.old._numpy_v1",
            "--hidden-import",
            "sklearn.metrics._pairwise_distances_reduction._datasets_pair",
            # Metadata required by transformers
            # See https://github.com/huggingface/transformers/blob/v4.45.2/src/transformers/dependency_versions_check.py#L25
            "--copy-metadata",
            "tqdm",
            "--copy-metadata",
            "regex",
            "--copy-metadata",
            "requests",
            "--copy-metadata",
            "packaging",
            "--copy-metadata",
            "filelock",
            "--copy-metadata",
            "numpy",
            "--copy-metadata",
            "tokenizers",
            "--copy-metadata",
            "huggingface-hub",
            "--copy-metadata",
            "safetensors",
            "--copy-metadata",
            "accelerate",
            "--copy-metadata",
            "pyyaml",
        ]
    )
