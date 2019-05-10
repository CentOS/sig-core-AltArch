#!/bin/bash

if [ "$1" = "-nc" ] ;then
    comp=" $1"
fi

for i in ks/*.ks;do
    ./build-armhfp-img.sh $i $comp
done
