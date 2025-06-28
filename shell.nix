{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python313Packages.faster-whisper
    python313Packages.requests
    python313Packages.flask
  ];

  shellHook = ''
    fish
  '';
}
