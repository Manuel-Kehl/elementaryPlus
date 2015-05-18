#!/bin/bash

DSTDIR=~/.TelegramDesktop/tdata/ticons

if [ -d $DSTDIR ]
then
  rm $DSTDIR/* 2> /dev/null
else
  mkdir -p $DSTDIR
fi

cp *.png $DSTDIR
ln -s $DSTDIR/ico_22_0.png $DSTDIR/icomute_22_0.png

for((i=2; i<100; i++))
do
   ln -s $DSTDIR/ico_22_1.png $DSTDIR/ico_22_$i.png
   ln -s $DSTDIR/ico_22_1.png $DSTDIR/icomute_22_$i.png
done
