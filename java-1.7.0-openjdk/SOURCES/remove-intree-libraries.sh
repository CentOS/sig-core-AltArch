#!/bin/sh

ZIP_SRC=openjdk/jdk/src/share/native/java/util/zip/zlib
JPEG_SRC=openjdk/jdk/src/share/native/sun/awt/image/jpeg/jpeg-6b
GIF_SRC=openjdk/jdk/src/share/native/sun/awt/giflib
PNG_SRC=openjdk/jdk/src/share/native/sun/awt/libpng
LCMS_SRC=openjdk/jdk/src/share/native/sun/java2d/cmm/lcms
PCSC_SRC=openjdk/jdk/src/solaris/native/sun/security/smartcardio/MUSCLE

echo "Removing built-in libs (they will be linked)"

echo "Removing zlib"
if [ ! -d ${ZIP_SRC} ]; then
	echo "${ZIP_SRC} does not exist. Refusing to proceed."
	exit 1
fi	
rm -rvf ${ZIP_SRC}

echo "Removing libjpeg"
if [ ! -f ${JPEG_SRC}/jdhuff.c ]; then # some file that sound definitely exist
	echo "${JPEG_SRC} does not contain jpeg sources. Refusing to proceed."
	exit 1
fi	

rm -rvf ${JPEG_SRC}

echo "Removing giflib"
if [ ! -d ${GIF_SRC} ]; then
	echo "${GIF_SRC} does not exist. Refusing to proceed."
	exit 1
fi	
rm -rvf ${GIF_SRC}

echo "Removing libpng"
if [ ! -d ${PNG_SRC} ]; then
	echo "${PNG_SRC} does not exist. Refusing to proceed."
	exit 1
fi	
rm -rvf ${PNG_SRC}

# LCMS 2 is disabled until security issues are resolved
if [ ! true ]; then
echo "Removing lcms"
if [ ! -d ${LCMS_SRC} ]; then
	echo "${LCMS_SRC} does not exist. Refusing to proceed."
	exit 1
fi	
rm -vf ${LCMS_SRC}/cmscam02.c
rm -vf ${LCMS_SRC}/cmscgats.c
rm -vf ${LCMS_SRC}/cmscnvrt.c
rm -vf ${LCMS_SRC}/cmserr.c
rm -vf ${LCMS_SRC}/cmsgamma.c
rm -vf ${LCMS_SRC}/cmsgmt.c
rm -vf ${LCMS_SRC}/cmsintrp.c
rm -vf ${LCMS_SRC}/cmsio0.c
rm -vf ${LCMS_SRC}/cmsio1.c
rm -vf ${LCMS_SRC}/cmslut.c
rm -vf ${LCMS_SRC}/cmsmd5.c
rm -vf ${LCMS_SRC}/cmsmtrx.c
rm -vf ${LCMS_SRC}/cmsnamed.c
rm -vf ${LCMS_SRC}/cmsopt.c
rm -vf ${LCMS_SRC}/cmspack.c
rm -vf ${LCMS_SRC}/cmspcs.c
rm -vf ${LCMS_SRC}/cmsplugin.c
rm -vf ${LCMS_SRC}/cmsps2.c
rm -vf ${LCMS_SRC}/cmssamp.c
rm -vf ${LCMS_SRC}/cmssm.c
rm -vf ${LCMS_SRC}/cmstypes.c
rm -vf ${LCMS_SRC}/cmsvirt.c
rm -vf ${LCMS_SRC}/cmswtpnt.c
rm -vf ${LCMS_SRC}/cmsxform.c
rm -vf ${LCMS_SRC}/lcms2.h
rm -vf ${LCMS_SRC}/lcms2_internal.h
rm -vf ${LCMS_SRC}/lcms2_plugin.h
fi

echo "Removing libpcsc headers"
if [ ! -d ${PCSC_SRC} ]; then
	echo "${PCSC_SRC} does not exist. Refusing to proceed."
	exit 1
fi	
rm -rvf ${PCSC_SRC}
