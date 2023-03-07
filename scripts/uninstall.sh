#!/usr/bin/env bash

INSTALL_DIR=""

if [ "$EUID" -eq 0 ]; then
  INSTALL_DIR="/usr/bin"
else
  INSTALL_DIR="$HOME/.local/bin"
fi

rm "$INSTALL_DIR/xs"
rm "$INSTALL_DIR/xspp"

echo "Successfully uninstalled xs grep (xs and xspp)."