#!/usr/bin/env bash

INSTALL_DIR=""

if [ "$EUID" -eq 0 ]; then
  INSTALL_DIR="/usr/bin"
else
  INSTALL_DIR="$HOME/.local/bin"
fi

cp build/src/xsgrep/xs "$INSTALL_DIR/xs"
cp build/src/xspp/xspp "$INSTALL_DIR/xspp"

if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
  echo "export PATH=\"$PATH:$INSTALL_DIR\"" >>"$HOME/.bashrc"
fi

echo "Successfully installed xs grep (xs and xspp)."
printf "\x1b[31mIf the commands 'xs' and/or 'xspp' are not available, please reload your current shell using this command:\n > source ~/.bashrc\x1b[m\n"
