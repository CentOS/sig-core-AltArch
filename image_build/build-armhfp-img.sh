#!/bin/bash
ks="$1"

if [ -z "$1" ] ;then
  echo $0 path/to/file.ks
  exit 1
fi

img=$(echo $ks|rev|cut -f 1 -d "/"|rev|sed s/\.ks//g)

time appliance-creator --config=${ks} --name="CentOS-Userland-7-armv7hl-$img-1804" --version="7" --debug

