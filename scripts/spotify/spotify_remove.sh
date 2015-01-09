#!/bin/bash

tmp_dir="/tmp/elementaryPlus/spotify"
cd $tmp_dir
cp resources_old.zip /opt/spotify/spotify-client/Data/resources.zip
rm -rf $tmp_dir
exit
