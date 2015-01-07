#!/bin/bash

[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"

mkdir -p /usr/share/sni-qt/icons
cp ./icons/* /usr/share/sni-qt/icons/
echo "MEGAsync icons installed without any errors!"

exit
