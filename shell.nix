 with import <nixpkgs> {};

(pkgs.python3.withPackages (ps: [ps.pynput])).env
