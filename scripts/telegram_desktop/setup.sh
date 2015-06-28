#!/bin/bash
DSTDIR=~/.TelegramDesktop/tdata/ticons
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
cd $DIR

source ../whattouse.sh

if [ $1 == "--install" ]
    then
        if [ $whatToUse == "cp" ]
            then
                cp ./icons/*.png $DSTDIR
                ln -sf $DSTDIR/ico_22_0.png $DSTDIR/icomute_22_0.png
                for((i=2; i<100; i++))
                    do
                        ln -sf $DSTDIR/ico_22_1.png $DSTDIR/ico_22_$i.png
                        ln -sf $DSTDIR/ico_22_1.png $DSTDIR/icomute_22_$i.png
                    done
        elif [ $whatToUse == "ln" ]
            then
                ln -sf $DIR/icons/*.png $DSTDIR
                ln -sf $DIR/icons/ico_22_0.png $DSTDIR/icomute_22_0.png
                for((i=2; i<100; i++))
                    do
                        ln -sf $DIR/icons/ico_22_1.png $DSTDIR/ico_22_$i.png
                        ln -sf $DIR/icons/ico_22_1.png $DSTDIR/icomute_22_$i.png
                    done
        fi
elif [ $1 == "--remove" ]
    then
        rm $DSTDIR/*.png
fi
exit
