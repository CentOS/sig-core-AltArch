#!/bin/sh
#
# usage: make-release-tarball.sh [version]

curl -O ftp://ftp.freedesktop.org/pub/mesa/$1/MesaLib-$1.tar.bz2
