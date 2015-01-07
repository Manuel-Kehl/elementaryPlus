#!/bin/bash

[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"

rm -rf /usr/share/icons/elementaryPlus
echo "Core icon theme removed without any errors!"
exit
