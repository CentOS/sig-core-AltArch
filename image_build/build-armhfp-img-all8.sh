#!/bin/bash

for i in ks8/*.ks;do
#img=$(echo $ks|rev|cut -f 1 -d "/"|rev|sed s/\.ks//g)
sudo ./build-armhfp-img8.sh $i -nc #>$img.log 2>&1
done
