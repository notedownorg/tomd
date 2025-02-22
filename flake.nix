{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    utils = { url = "github:numtide/flake-utils"; };
    licenser = { url = "github:liamawhite/licenser/3ee5a0592eedd79958227562508a62ff7e82016f"; };
  };
  outputs = { self, nixpkgs, utils, licenser }:
    utils.lib.eachDefaultSystem
      (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        with pkgs;
        {
          devShells.default = pkgs.mkShell {
            buildInputs = [
              git
              python3
              poetry
              black
              licenser.packages.${system}.default
            ];
          };
        }
      );
}

