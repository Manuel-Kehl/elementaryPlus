#!/bin/bash

[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"

cp -R ../../elementaryPlus /usr/share/icons/
echo "Core icon theme installed without any errors!"
exit
