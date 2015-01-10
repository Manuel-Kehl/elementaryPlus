#!/bin/bash

add-apt-repository --yes ppa:cybre/sni-qt-eplus
apt-get -y update
apt-get -y install sni-qt sni-qt:i386
add-apt-repository --remove --yes ppa:cybre/sni-qt-eplus
