#!/bin/bash
cd "$(dirname "$0")"
if [[ $EUID -ne 0 ]]; then
    ./scripts/elementaryplus-installer.py
else
   echo "This script mustn't be run as root!" 1>&2
   echo "Please run again as normal user." 1>&2
fi
exit
