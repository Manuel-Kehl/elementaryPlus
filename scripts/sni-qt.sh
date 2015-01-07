#!/bin/bash

[ "$(whoami)" != "root" ] && exec sudo -- "$0" "$@"

add-apt-repository --yes ppa:rpeshkov/ppa
apt-get -y update
apt-get -y upgrade
add-apt-repository --remove --yes ppa:rpeshkov/ppa
