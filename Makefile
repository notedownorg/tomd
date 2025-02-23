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

.PHONY: clean build format licenser

hygiene: licenser format

dirty:
	git diff --exit-code

licenser:
	nix develop --command licenser apply -r "Notedown Authors"

format:
	nix develop --command poetry lock
	nix develop --command black .

clean:
	rm -rf build __pycache__ dist

build:
	nix develop --command poetry install
	nix develop --command poetry run bundle

install: build
	sudo rm -rf /usr/local/bin/tomd*
	sudo cp -r dist/tomd/* /usr/local/bin
	sudo chmod +x /usr/local/bin/tomd
