#!/bin/bash

add-apt-repository --yes ppa:cybre/sni-qt-eplus
apt-get -y update
apt-get -y install sni-qt sni-qt:i386
