#!/bin/bash

pwd
#pkexec policy
SRCFILE="$1/scripts/postinst/apps.elementaryPlusInstaller.policy"
DSTDIR="/usr/share/polkit-1/actions/"
cp $SRCFILE $DSTDIR

#glib2 schema
SRCFILE="$1/scripts/postinst/apps.elementaryPlusInstaller.gschema.xml"
DSTDIR="/usr/share/glib-2.0/schemas/"
cp $SRCFILE $DSTDIR
glib-compile-schemas $DSTDIR

echo "First run: done!"
