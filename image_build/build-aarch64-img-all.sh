#!/bin/bash -x

basedir=$(dirname $(readlink -f "$0"))

if [ -n "$basedir" ];then
    cd "$basedir"
fi
if [ "$1" = "-nc" ] ;then
    comp=" $1"
fi

pushd ks.aarch64
for i in *.ks;do
    sudo ../build-aarch64-img.sh $i $comp
done
popd
