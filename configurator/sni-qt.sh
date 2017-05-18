#!/bin/bash

add-apt-repository --yes ppa:cybre/sni-qt-eplus
apt-get -y update
apt-get -y install sni-qt:amd64 sni-qt:i386