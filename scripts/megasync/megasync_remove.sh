#!/bin/bash

for entry in icons/*
do
  echo "$entry"
  rm /usr/share/sni-qt/$entry
done
exit
