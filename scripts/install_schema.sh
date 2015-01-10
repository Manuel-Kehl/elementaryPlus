#!/bin/bash

SRCFILE="./scripts/apps.elementaryPlusInstaller.gschema.xml"
DSTDIR="/usr/share/glib-2.0/schemas/"
cp $SRCFILE $DSTDIR
glib-compile-schemas $DSTDIR