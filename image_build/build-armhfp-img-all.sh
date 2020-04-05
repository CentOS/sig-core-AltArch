#!/bin/bash

basedir=$(dirname $(readlink -f "$0"))

if [ -n "$basedir" ];then
    cd "$basedir"
fi
if [ "$1" = "-nc" ] ;then
    comp=" $1"
fi

pushd ks
for i in *.ks;do
    ../build-armhfp-img.sh $i $comp
done
popd
