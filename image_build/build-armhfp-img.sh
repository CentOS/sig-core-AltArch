#!/bin/bash

if [ -z "$1" ] ;then
  echo $0 path/to/file.ks
  exit 1
fi
if [ "$2" = "-nc" ] ;then
  comp=" --no-compress"
fi
ks="$1"

img=$(echo $ks|rev|cut -f 1 -d "/"|rev|sed s/\.ks//g)

time appliance-creator$comp --config=${ks} --name="CentOS-Userland-7-armv7hl-$img-2003" --version="7" --debug 2>&1 | tee $img.log
