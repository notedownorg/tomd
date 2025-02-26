# tomd

Extract Markdown from various sources and print it to `stdout`.

## Supported sources

- Text/HTML websites
- YouTube
- More coming soon...

## Installation

Once more stable there will be actual releases but right now you need to clone the repo and run `make install`. Note: requires the [`Nix`](https://nixos.org/download/) package manager so only currently supported on `Linux`, `macOS` and `WSL2`.

## Usage

Run the command to extract Markdown from the passed source and print it to `stdout`.

```sh 
tomd "https://brooker.co.za/blog/2023/09/21/audience.html" # text/html
tomd "https://youtu.be/B0yAy2j-9V0" # YouTube
```
