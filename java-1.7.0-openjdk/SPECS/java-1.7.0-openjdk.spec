# If debug is 1, OpenJDK is built with all debug info present.
%global debug 0

# we remove the build id notes explicitly to avoid generating (potentially
# conflicting) files in the -debuginfo package
%undefine _missing_build_ids_terminate_build

%global icedtea_version 2.6.12
%global hg_tag icedtea-{icedtea_version}

%global aarch64			aarch64 arm64 armv8
#sometimes we need to distinguish big and little endian PPC64
%global ppc64le			ppc64le
%global ppc64be			ppc64 ppc64p7
%global multilib_arches %{power64} sparc64 x86_64 
%global jit_arches		%{ix86} x86_64 sparcv9 sparc64 %{ppc64be} %{ppc64le} %{aarch64}

# With disabled nss is NSS deactivated, so in NSS_LIBDIR can be wrong path
# the initialisation must be here. LAter the pkg-connfig have bugy behaviour
#looks liekopenjdk RPM specific bug
# Always set this so the nss.cfg file is not broken
%global NSS_LIBDIR %(pkg-config --variable=libdir nss)
%global NSS_LIBS %(pkg-config --libs nss)
%global NSS_CFLAGS %(pkg-config --cflags nss-softokn)
# see https://bugzilla.redhat.com/show_bug.cgi?id=1332456
%global NSSSOFTOKN_BUILDTIME_NUMBER %(pkg-config --modversion nss-softokn || : )
%global NSS_BUILDTIME_NUMBER %(pkg-config --modversion nss || : )
#this is worakround for processing of requires during srpm creation
%global NSSSOFTOKN_BUILDTIME_VERSION %(if [ "x%{NSSSOFTOKN_BUILDTIME_NUMBER}" == "x" ] ; then echo "" ;else echo ">= %{NSSSOFTOKN_BUILDTIME_NUMBER}" ;fi)
%global NSS_BUILDTIME_VERSION %(if [ "x%{NSS_BUILDTIME_NUMBER}" == "x" ] ; then echo "" ;else echo ">= %{NSS_BUILDTIME_NUMBER}" ;fi)

# In some cases, the arch used by the JDK does
# not match _arch.
# Also, in some cases, the machine name used by SystemTap
# does not match that given by _build_cpu
%ifarch x86_64
%global archbuild amd64
%global archinstall amd64
%global stapinstall x86_64
%endif
%ifarch ppc
%global archbuild ppc
%global archinstall ppc
%global archdef PPC
%global stapinstall powerpc
%endif
%ifarch %{ppc64be}
%global archbuild ppc64
%global archinstall ppc64
%global archdef PPC
%global stapinstall powerpc
%endif
%ifarch %{ppc64le}
%global archbuild ppc64le
%global archinstall ppc64le
%global archdef PPC64
%global stapinstall powerpc
%endif
%ifarch %{ix86}
%global archbuild i586
%global archinstall i386
%global stapinstall i386
%endif
%ifarch ia64
%global archbuild ia64
%global archinstall ia64
%global stapinstall ia64
%endif
%ifarch s390
%global archbuild s390
%global archinstall s390
%global archdef S390
%global stapinstall s390
%endif
%ifarch s390x
%global archbuild s390x
%global archinstall s390x
%global archdef S390
%global stapinstall s390
%endif
%ifarch %{arm}
%global archbuild arm
%global archinstall arm
%global archdef ARM
%global stapinstall arm
%endif
%ifarch %{aarch64}
%global archbuild aarch64
%global archinstall aarch64
%global archdef AARCH64
%global stapinstall arm64
%endif
# 32 bit sparc, optimized for v9
%ifarch sparcv9
%global archbuild sparc
%global archinstall sparc
%global stapinstall %{_build_cpu}
%endif
# 64 bit sparc
%ifarch sparc64
%global archbuild sparcv9
%global archinstall sparcv9
%global stapinstall %{_build_cpu}
%endif
%ifnarch %{jit_arches}
%global archbuild %{_arch}
%global archinstall %{_arch}
%endif

%if %{debug}
%global debugbuild debug_build
%else
%global debugbuild %{nil}
%endif

# If hsbootstrap is 1, build HotSpot alone first and use that in the bootstrap JDK
# You can turn this on to avoid issues where HotSpot is broken in the bootstrap JDK
%ifarch %{jit_arches}
%global hsbootstrap 0
%else
%global hsbootstrap 0
%endif

%if %{debug}
%global buildoutputdir openjdk/build/linux-%{archbuild}-debug
%else
%global buildoutputdir openjdk/build/linux-%{archbuild}
%endif

%global with_pulseaudio 1

%ifarch %{jit_arches}
%global with_systemtap 1
%else
%global with_systemtap 0
%endif

# Convert an absolute path to a relative path.  Each symbolic link is
# specified relative to the directory in which it is installed so that
# it will resolve properly within chrooted installations.
%global script 'use File::Spec; print File::Spec->abs2rel($ARGV[0], $ARGV[1])'
%global abs2rel %{__perl} -e %{script}

# Hard-code libdir on 64-bit architectures to make the 64-bit JDK
# simply be another alternative.
%global LIBDIR       %{_libdir}
#backuped original one
%ifarch %{multilib_arches}
%global syslibdir       %{_prefix}/lib64
%global _libdir         %{_prefix}/lib
%else
%global syslibdir       %{_libdir}
%endif

# Standard JPackage naming and versioning defines.
%global origin          openjdk
%global updatever       161
%global buildver        00
# Keep priority on 7digits in case updatever>9
%global priority        1700%{updatever}
%global javaver         1.7.0

%global sdkdir          %{uniquesuffix}
%global jrelnk          jre-%{javaver}-%{origin}-%{version}-%{release}.%{_arch}

%global jredir          %{sdkdir}/jre
%global sdkbindir       %{_jvmdir}/%{sdkdir}/bin
%global jrebindir       %{_jvmdir}/%{jredir}/bin
%global jvmjardir       %{_jvmjardir}/%{uniquesuffix}

%global rpm_state_dir %{_localstatedir}/lib/rpm-state/

%global fullversion     %{name}-%{version}-%{release}

%global uniquesuffix          %{fullversion}.%{_arch}
#we can copy the javadoc to not arched dir, or made it not noarch
%global uniquejavadocdir       %{fullversion}

%ifarch %{jit_arches}
# Where to install systemtap tapset (links)
# We would like these to be in a package specific subdir,
# but currently systemtap doesn't support that, so we have to
# use the root tapset dir for now. To distinquish between 64
# and 32 bit architectures we place the tapsets under the arch
# specific dir (note that systemtap will only pickup the tapset
# for the primary arch for now). Systemtap uses the machine name
# aka build_cpu as architecture specific directory name.
%global tapsetroot /usr/share/systemtap
%global tapsetdir %{tapsetroot}/tapset/%{stapinstall}
%endif

# Prevent brp-java-repack-jars from being run.
%global __jar_repack 0

Name:    java-%{javaver}-%{origin}
Version: %{javaver}.%{updatever}
Release: %{icedtea_version}.0%{?dist}
# java-1.5.0-ibm from jpackage.org set Epoch to 1 for unknown reasons,
# and this change was brought into RHEL-4.  java-1.5.0-ibm packages
# also included the epoch in their virtual provides.  This created a
# situation where in-the-wild java-1.5.0-ibm packages provided "java =
# 1:1.5.0".  In RPM terms, "1.6.0 < 1:1.5.0" since 1.6.0 is
# interpreted as 0:1.6.0.  So the "java >= 1.6.0" requirement would be
# satisfied by the 1:1.5.0 packages.  Thus we need to set the epoch in
# JDK package >= 1.6.0 to 1, and packages referring to JDK virtual
# provides >= 1.6.0 must specify the epoch, "java >= 1:1.6.0".
Epoch:   1
Summary: OpenJDK Runtime Environment
Group:   Development/Languages

License:  ASL 1.1 and ASL 2.0 and GPL+ and GPLv2 and GPLv2 with exceptions and LGPL+ and LGPLv2 and MPLv1.0 and MPLv1.1 and Public Domain and W3C
URL:      http://openjdk.java.net/

# Source from upstream IcedTea 2.x project. To regenerate, use
# VERSION=icedtea-${icedtea_version} FILE_NAME_ROOT=openjdk-${VERSION}
# REPO_ROOT=<path to checked-out repository> generate_source_tarball.sh
Source0:  openjdk-icedtea-%{icedtea_version}.tar.xz

# README file
# This source is under maintainer's/java-team's control
Source2:  README.src

# Sources 6-12 are taken from hg clone http://icedtea.classpath.org/hg/icedtea7
# Unless said differently, there is directory with required sources which should be enough to pack/rename

# Class rewrite to rewrite rhino hierarchy
Source5: class-rewriter.tar.gz

# Systemtap tapsets. Zipped up to keep it small.
# last update from IcedTea 2.6.10
Source6: systemtap-tapset-2.6.12.tar.xz

# .desktop files. 
Source7:  policytool.desktop
Source77: jconsole.desktop

# nss configuration file
Source8: nss.cfg

# FIXME: Taken from IcedTea snapshot 877ad5f00f69, but needs to be moved out
# hg clone -r 877ad5f00f69 http://icedtea.classpath.org/hg/icedtea7
Source9: pulseaudio.tar.gz

# Removed libraries that we link instead
Source10: remove-intree-libraries.sh

#http://icedtea.classpath.org/hg/icedtea7/file/933d082ec889/fsg.sh
# file to clean tarball, should be ketp updated as possible
Source1111: fsg.sh

# Remove build ids from binaries
Source11: remove-buildids.sh

# Ensure we aren't using the limited crypto policy
Source12: TestCryptoLevel.java

Source13: java-abrt-launcher

Source20: repackReproduciblePolycies.sh

# RPM/distribution specific patches

# Allow TCK to pass with access bridge wired in
Patch1:   java-1.7.0-openjdk-java-access-bridge-tck.patch

# Disable access to access-bridge packages by untrusted apps
Patch3:   java-1.7.0-openjdk-java-access-bridge-security.patch

# Ignore AWTError when assistive technologies are loaded 
Patch4:   java-1.7.0-openjdk-accessible-toolkit.patch

# Build docs even in debug
Patch5:   java-1.7.0-openjdk-debugdocs.patch

# Add debuginfo where missing
Patch6:   %{name}-debuginfo.patch

#
# OpenJDK specific patches
#

# Add rhino support
Patch100: rhino.patch

Patch106: %{name}-freetype-check-fix.patch

# allow to create hs_pid.log in tmp (in 700 permissions) if working directory is unwritable
Patch200: abrt_friendly_hs_log_jdk7.patch

#
# Optional component packages
#

# Make the ALSA based mixer the default when building with the pulseaudio based
# mixer
Patch300: pulse-soundproperties.patch

# Make the curves reported by Java's SSL implementation match those of NSS
Patch400: rh1022017.patch

# Temporary patches

# PR2809: Backport "8076221: Disable RC4 cipher suites" (will appear in 2.7.0)
Patch500: pr2809.patch
# PR3393, RH1273760: Support using RSAandMGF1 with the SHA hash algorithms in the PKCS11 provider (will appear in 2.7.0)
Patch501: pr3393-rh1273760.patch
# PR3497: AArch64: Adapt to 8002074: Support for AES on SPARC
Patch502: pr3497.patch

# End of tmp patches

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc-c++
BuildRequires: alsa-lib-devel
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: giflib-devel
# LCMS 2 is disabled until security issues are resolved
#BuildRequires: lcms2-devel >= 2.5
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXp-devel
BuildRequires: libXt-devel
BuildRequires: libXtst-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: wget
BuildRequires: xorg-x11-proto-devel
BuildRequires: ant
BuildRequires: libXinerama-devel
# Provides lsb_release for generating distro id in jdk_generic_profile.sh
BuildRequires: redhat-lsb-core
BuildRequires: rhino
BuildRequires: zip
BuildRequires: fontconfig
BuildRequires: xorg-x11-fonts-Type1
BuildRequires: zlib > 1.2.3-6
# Require a build JDK which has a working jar uf (PR1437 / RH1207129)
BuildRequires: java-1.7.0-openjdk-devel >= 1.7.0.111-2.6.7.2
BuildRequires: fontconfig
BuildRequires: at-spi-devel
BuildRequires: gawk
BuildRequires: pkgconfig >= 0.9.0
BuildRequires: xorg-x11-utils
# Requirements for setting up the nss.cfg
BuildRequires: nss-devel
# Required for NIO2
BuildRequires: libattr-devel
# Build requirements for SunEC system NSS support
BuildRequires: nss-softokn-freebl-devel >= 3.16.1
# Required for smartcard support
BuildRequires: pcsc-lite-devel
# Required for SCTP support
BuildRequires: lksctp-tools-devel
# Required for fallback native proxy support
BuildRequires: GConf2-devel
# PulseAudio build requirements.
%if %{with_pulseaudio}
BuildRequires: pulseaudio-libs-devel >= 0.9.11
%endif
# Zero-assembler build requirement.
%ifnarch %{jit_arches}
BuildRequires: libffi-devel >= 3.0.10
%endif

# cacerts build requirement.
BuildRequires: openssl
# execstack build requirement.
# no prelink on ARM yet
%ifnarch %{arm} %{aarch64} %{ppc64le}
BuildRequires: prelink
%endif
%ifarch %{jit_arches}
#systemtap build requirement.
BuildRequires: systemtap-sdt-devel
%endif

Requires: fontconfig
Requires: xorg-x11-fonts-Type1
#requires rest of java
Requires: %{name}-headless = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless = %{epoch}:%{version}-%{release}


# Standard JPackage base provides.
Provides: jre-%{javaver}-%{origin} = %{epoch}:%{version}-%{release}
Provides: jre-%{origin} = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver} = %{epoch}:%{version}-%{release}
Provides: java-%{javaver} = %{epoch}:%{version}-%{release}
Provides: jre = %{javaver}
Provides: java-%{origin} = %{epoch}:%{version}-%{release}
Provides: java = %{epoch}:%{javaver}
# Standard JPackage extensions provides.
Provides: java-fonts = %{epoch}:%{version}

# Obsolete older 1.6 packages as it cannot use the new bytecode
# Obsoletes: java-1.6.0-openjdk
# Obsoletes: java-1.6.0-openjdk-demo
# Obsoletes: java-1.6.0-openjdk-devel
# Obsoletes: java-1.6.0-openjdk-javadoc
# Obsoletes: java-1.6.0-openjdk-src

%description
The OpenJDK runtime environment.

%package headless
Summary: The OpenJDK runtime environment without audio and video support
Group:   Development/Languages

# LCMS 2 is disabled until security issues are resolved
#Requires: lcms2 >= 2.5
Requires: libjpeg = 6b
# Require /etc/pki/java/cacerts.
Requires: ca-certificates
# Require jpackage-utils for ant.
Requires: jpackage-utils >= 1.7.3-1jpp.2
# Require zoneinfo data provided by tzdata-java subpackage.
Requires: tzdata-java
# there is need to depnd on exact version of nss
Requires: nss %{NSS_BUILDTIME_VERSION}
Requires: nss-softokn %{NSSSOFTOKN_BUILDTIME_VERSION}
# tool to copy jdk's configs - should be Recommends only, but then only dnf/yum eforce it, not rpm transaction and so no configs are persisted when pure rpm -u is run. I t may be consiedered as regression
Requires:	copy-jdk-configs >= 2.2
OrderWithRequires: copy-jdk-configs
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(post):   chkconfig >= 1.7
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(postun):   chkconfig >= 1.7

Provides: jre-%{javaver}-%{origin}-headless = %{epoch}:%{version}-%{release}
Provides: jre-%{origin}-headless = %{epoch}:%{version}-%{release}
Provides: jre-%{javaver}-headless = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-headless = %{epoch}:%{version}-%{release}
Provides: jre-headless = %{epoch}:%{javaver}
Provides: java-%{origin}-headless = %{epoch}:%{version}-%{release}
Provides: java-headless = %{epoch}:%{javaver}
# Standard JPackage extensions provides.
Provides: jndi = %{epoch}:%{version}
Provides: jndi-ldap = %{epoch}:%{version}
Provides: jndi-cos = %{epoch}:%{version}
Provides: jndi-rmi = %{epoch}:%{version}
Provides: jndi-dns = %{epoch}:%{version}
Provides: jaas = %{epoch}:%{version}
Provides: jsse = %{epoch}:%{version}
Provides: jce = %{epoch}:%{version}
Provides: jdbc-stdext = 4.1
Provides: java-sasl = %{epoch}:%{version}

%description headless
The OpenJDK runtime environment without audio and video 

%package devel
Summary: OpenJDK Development Environment
Group:   Development/Tools

# Require base package.
Requires:         %{name} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless = %{epoch}:%{version}-%{release}
# Post requires alternatives to install tool alternatives.
Requires(post):   %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(post):   chkconfig >= 1.7
# Postun requires alternatives to uninstall tool alternatives.
Requires(postun): %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(postun):   chkconfig >= 1.7

# Standard JPackage devel provides.
Provides: java-sdk-%{javaver}-%{origin} = %{epoch}:%{version}
Provides: java-sdk-%{javaver} = %{epoch}:%{version}
Provides: java-sdk-%{origin} = %{epoch}:%{version}
Provides: java-sdk = %{epoch}:%{javaver}
Provides: java-%{javaver}-devel = %{epoch}:%{version}
Provides: java-devel-%{origin} = %{epoch}:%{version}
Provides: java-devel = %{epoch}:%{javaver}


%description devel
The OpenJDK development tools.

%package demo
Summary: OpenJDK Demos
Group:   Development/Languages

Requires: %{name} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless = %{epoch}:%{version}-%{release}

%description demo
The OpenJDK demos.

%package src
Summary: OpenJDK Source Bundle
Group:   Development/Languages

Requires: %{name} = %{epoch}:%{version}-%{release}

%description src
The OpenJDK source bundle.

%package javadoc
Summary: OpenJDK API Documentation
Group:   Documentation
Requires: jpackage-utils
BuildArch: noarch

OrderWithRequires: %{name}-headless = %{epoch}:%{version}-%{release}
# Post requires alternatives to install javadoc alternative.
Requires(post):   %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(post):   chkconfig >= 1.7
# Postun requires alternatives to uninstall javadoc alternative.
Requires(postun): %{_sbindir}/alternatives
# in version 1.7 and higher for --family switch
Requires(postun):   chkconfig >= 1.7

# Standard JPackage javadoc provides.
Provides: java-javadoc = %{epoch}:%{version}-%{release}
Provides: java-%{javaver}-javadoc = %{epoch}:%{version}-%{release}

%description javadoc
The OpenJDK API documentation.

%package accessibility
Summary: OpenJDK accessibility connector
Requires: java-atk-wrapper
Requires: %{name} = %{epoch}:%{version}-%{release}
OrderWithRequires: %{name}-headless = %{epoch}:%{version}-%{release}

%description accessibility
Enables accessibility support in OpenJDK by using java-at-wrapper. This allows compatible at-spi2 based accessibility programs to work for AWT and Swing-based programs.
Please note, the java-atk-wrapper is still in beta, and also OpenJDK itself is still in phase of tuning to be working with accessibility features.
Although working pretty fine, there are known issues with accessibility on, so do not rather install this package unless you really need.

%prep
%setup -q -c -n %{uniquesuffix} -T -a 0
# https://bugzilla.redhat.com/show_bug.cgi?id=1189084
prioritylength=`expr length %{priority}`
if [ $prioritylength -ne 7 ] ; then
 echo "priority must be 7 digits in total, violated"
 exit 14
fi
cp %{SOURCE2} .

# OpenJDK patches
%patch100

# pulseaudio support
%if %{with_pulseaudio}
%patch300
%endif

# Temporary fixes
%patch500
%patch501
%patch502
# End of temporary fixes

# ECC fix
%patch400

# Add systemtap patches if enabled
%if %{with_systemtap}
%endif

# Remove libraries that are linked
sh %{SOURCE10}

# Extract the rewriter (to rewrite rhino classes)
tar xzf %{SOURCE5}

# Extract systemtap tapsets
%if %{with_systemtap}

tar xf %{SOURCE6}

for file in tapset/*.in; do

    OUTPUT_FILE=`echo $file | sed -e s:%{javaver}\.stp\.in$:%{version}-%{release}.stp:g`
    sed -e s:@ABS_SERVER_LIBJVM_SO@:%{_jvmdir}/%{sdkdir}/jre/lib/%{archinstall}/server/libjvm.so:g $file > $file.1
# FIXME this should really be %if %{has_client_jvm}
%ifarch %{ix86}
    sed -e s:@ABS_CLIENT_LIBJVM_SO@:%{_jvmdir}/%{sdkdir}/jre/lib/%{archinstall}/client/libjvm.so:g $file.1 > $OUTPUT_FILE
%else
    sed -e '/@ABS_CLIENT_LIBJVM_SO@/d' $file.1 > $OUTPUT_FILE
%endif
    sed -i -e s:@INSTALL_ARCH_DIR@:%{archinstall}:g $OUTPUT_FILE
    sed -i -e s:@prefix@:%{_jvmdir}/%{sdkdir $suffix}/:g $OUTPUT_FILE

done

%endif

# Pulseaudio
%if %{with_pulseaudio}
tar xzf %{SOURCE9}
%endif


%patch3
%patch4

%if %{debug}
%patch5
%patch6
%endif

%patch106
%patch200

%build
# How many cpu's do we have?
export NUM_PROC=`/usr/bin/getconf _NPROCESSORS_ONLN 2> /dev/null || :`
export NUM_PROC=${NUM_PROC:-1}

# Build IcedTea and OpenJDK.
%ifarch s390x sparc64 alpha %{power64} %{aarch64}
export ARCH_DATA_MODEL=64
%endif
%ifarch alpha
export CFLAGS="$CFLAGS -mieee"
%endif

CFLAGS="$CFLAGS -fstack-protector-strong"
export CFLAGS

# Build the re-written rhino jar
mkdir -p rhino/{old,new}

# Compile the rewriter
(cd rewriter 
 javac com/redhat/rewriter/ClassRewriter.java
)

# Extract rhino.jar contents and rewrite
(cd rhino/old 
 jar xf /usr/share/java/rhino.jar
)

java -cp rewriter com.redhat.rewriter.ClassRewriter \
    $PWD/rhino/old \
    $PWD/rhino/new \
    org.mozilla \
    sun.org.mozilla

(cd rhino/old
 for file in `find -type f -not -name '*.class'` ; do
     new_file=../new/`echo $file | sed -e 's#org#sun/org#'`
     mkdir -pv `dirname $new_file`
     cp -v $file $new_file
     sed -ie 's#org\.mozilla#sun.org.mozilla#g' $new_file
 done
)

(cd rhino/new
   jar cfm ../rhino.jar META-INF/MANIFEST.MF sun
)

export SYSTEM_JDK_DIR=/usr/lib/jvm/java-1.7.0-openjdk

# Temporary workaround for ppc64le ; RH1191652
# Need to work around the jre arch directory being
# ppc64 instead of the expected ppc64le
# Taken from IcedTea7 bootstrap-directory-stage1 & PR1765
%ifarch %{ppc64le}
STAGE1_BOOT_RUNTIME=jdk/jre/lib/rt.jar
mkdir -p jdk/bin
ln -sfv ${SYSTEM_JDK_DIR}/bin/java jdk/bin/java
ln -sfv ${SYSTEM_JDK_DIR}/bin/javah jdk/bin/javah
ln -sfv ${SYSTEM_JDK_DIR}/bin/rmic jdk/bin/rmic
ln -sfv ${SYSTEM_JDK_DIR}/bin/jar jdk/bin/jar
ln -sfv ${SYSTEM_JDK_DIR}/bin/native2ascii jdk/bin/native2ascii
ln -sfv ${SYSTEM_JDK_DIR}/bin/javac jdk/bin/javac
ln -sfv ${SYSTEM_JDK_DIR}/bin/javap jdk/bin/javap
ln -sfv ${SYSTEM_JDK_DIR}/bin/idlj jdk/bin/idlj
mkdir -p jdk/lib/modules
mkdir -p jdk/jre/lib && \
cp ${SYSTEM_JDK_DIR}/jre/lib/rt.jar ${STAGE1_BOOT_RUNTIME} && \
chmod u+w ${STAGE1_BOOT_RUNTIME}
mkdir -p jdk/lib && \
ln -sfv ${SYSTEM_JDK_DIR}/lib/tools.jar jdk/lib/tools.jar ; \
# Workaround some older ppc64le builds installing to 'ppc64' rather than 'ppc64le'
if test -d ${SYSTEM_JDK_DIR}/jre/lib/ppc64 ; then \
  ln -sfv ${SYSTEM_JDK_DIR}/jre/lib/ppc64 \
    jdk/jre/lib/%{archinstall} ; \
else \
  ln -sfv ${SYSTEM_JDK_DIR}/jre/lib/%{archinstall} \
    jdk/jre/lib/ ; \
fi
if ! test -d jdk/jre/lib/%{archinstall}; \
  then \
  ln -sfv ./%{archbuild} \
    jdk/jre/lib/%{archinstall}; \
fi
mkdir -p jdk/include && \
for i in ${SYSTEM_JDK_DIR}/include/*; do \
  test -r ${i} | continue; \
  i=`basename ${i}`; \
  rm -f jdk/include/${i}; \
  ln -sv ${SYSTEM_JDK_DIR}/include/${i} jdk/include/${i}; \
done;
export JDK_TO_BUILD_WITH=${PWD}/jdk
%else
export JDK_TO_BUILD_WITH=${SYSTEM_JDK_DIR}
%endif


pushd openjdk >& /dev/null

export ALT_BOOTDIR="$JDK_TO_BUILD_WITH"

# Save old umask as jdk_generic_profile overwrites it
oldumask=`umask`

# Set generic profile
%ifnarch %{jit_arches}
export ZERO_BUILD=true
%endif
# LCMS 2 is disabled until security issues are resolved
export LCMS_CFLAGS="disabled"
export LCMS_LIBS="disabled"
export PKGVERSION="rhel-%{release}-%{_arch} u%{updatever}-b%{buildver}"

source jdk/make/jdk_generic_profile.sh

# Restore old umask
umask $oldumask

# LCMS 2 is disabled until security issues are resolved
export SYSTEM_LCMS=false

%if %{hsbootstrap}

mkdir bootstrap

make \
  UNLIMITED_CRYPTO=true \
  ANT="/usr/bin/ant" \
  DISTRO_NAME="Red Hat Enterprise Linux 7" \
  DISTRO_PACKAGE_VERSION="${PKGVERSION}" \
  JDK_UPDATE_VERSION=`printf "%02d" %{updatever}` \
  JDK_BUILD_NUMBER=b`printf "%02d" %{buildver}` \
  JRE_RELEASE_VERSION=%{javaver}_`printf "%02d" %{updatever}`-b`printf "%02d" %{buildver}` \
  MILESTONE="fcs" \
  ALT_PARALLEL_COMPILE_JOBS="$NUM_PROC" \
  HOTSPOT_BUILD_JOBS="$NUM_PROC" \
  STATIC_CXX="false" \
  RHINO_JAR="$PWD/../rhino/rhino.jar" \
  GENSRCDIR="$PWD/generated.build" \
  FT2_CFLAGS="`pkg-config --cflags freetype2` " \
  FT2_LIBS="`pkg-config --libs freetype2` " \
  DEBUG_CLASSFILES="true" \
  DEBUG_BINARIES="true" \
  STRIP_POLICY="no_strip" \
  JAVAC_WARNINGS_FATAL="false" \
  INSTALL_LOCATION=%{_jvmdir}/%{sdkdir} \
  SYSTEM_NSS="true" \
  NSS_LIBS="%{NSS_LIBS} -lfreebl" \
  NSS_CFLAGS="%{NSS_CFLAGS}" \
  ECC_JUST_SUITE_B="true" \
  SYSTEM_GSETTINGS="true" \
  BUILD_JAXP=false BUILD_JAXWS=false BUILD_LANGTOOLS=false BUILD_JDK=false BUILD_CORBA=false \
  ALT_JDK_IMPORT_PATH=${JDK_TO_BUILD_WITH} ALT_OUTPUTDIR=${PWD}/bootstrap \
  %{debugbuild}

export VM_DIR=bootstrap-vm/jre/lib/%{archinstall}/server
cp -dR $(readlink -e ${SYSTEM_JDK_DIR}) bootstrap-vm
rm -vf ${VM_DIR}/libjvm.so
if [ ! -e ${VM_DIR} ] ; then mkdir -p ${VM_DIR}; fi
cp -av bootstrap/hotspot/import/jre/lib/%{archinstall}/server/libjvm.so ${VM_DIR}

export ALT_BOOTDIR=${PWD}/bootstrap-vm
  
%endif

# ENABLE_FULL_DEBUG_SYMBOLS=0 is the internal HotSpot option
# to turn off the stripping of debuginfo. FULL_DEBUG_SYMBOLS
# does the same for product builds, but is ignored on non-product builds.
make \
  UNLIMITED_CRYPTO=true \
  ANT="/usr/bin/ant" \
  DISTRO_NAME="Red Hat Enterprise Linux 7" \
  DISTRO_PACKAGE_VERSION="${PKGVERSION}" \
  JDK_UPDATE_VERSION=`printf "%02d" %{updatever}` \
  JDK_BUILD_NUMBER=b`printf "%02d" %{buildver}` \
  JRE_RELEASE_VERSION=%{javaver}_`printf "%02d" %{updatever}`-b`printf "%02d" %{buildver}` \
  MILESTONE="fcs" \
  ALT_PARALLEL_COMPILE_JOBS="$NUM_PROC" \
  HOTSPOT_BUILD_JOBS="$NUM_PROC" \
  STATIC_CXX="false" \
  RHINO_JAR="$PWD/../rhino/rhino.jar" \
  GENSRCDIR="$PWD/generated.build" \
  FT2_CFLAGS="`pkg-config --cflags freetype2` " \
  FT2_LIBS="`pkg-config --libs freetype2` " \
  DEBUG_CLASSFILES="true" \
  DEBUG_BINARIES="true" \
  STRIP_POLICY="no_strip" \
  JAVAC_WARNINGS_FATAL="false" \
  INSTALL_LOCATION=%{_jvmdir}/%{sdkdir} \
  SYSTEM_NSS="true" \
  NSS_LIBS="%{NSS_LIBS} -lfreebl" \
  NSS_CFLAGS="%{NSS_CFLAGS}" \
  ECC_JUST_SUITE_B="true" \
  SYSTEM_GSETTINGS="true" \
  %{debugbuild}

popd >& /dev/null

export JAVA_HOME=$(pwd)/%{buildoutputdir}/j2sdk-image

# Install java-abrt-launcher
mkdir  $JAVA_HOME/jre-abrt
mkdir  $JAVA_HOME/jre-abrt/bin
mv $JAVA_HOME/jre/bin/java $JAVA_HOME/jre-abrt/bin/java
ln -s %{_jvmdir}/%{sdkdir}/jre/lib $JAVA_HOME/jre-abrt/lib
cat %{SOURCE13} | sed -e s:@JAVA_PATH@:%{_jvmdir}/%{sdkdir}/jre-abrt/bin/java:g -e s:@LIB_DIR@:%{LIBDIR}/libabrt-java-connector.so:g >  $JAVA_HOME/jre/bin/java
chmod 755 $JAVA_HOME/jre/bin/java

# Install nss.cfg right away as we will be using the JRE above
cp -a %{SOURCE8} $JAVA_HOME/jre/lib/security/
sed -i -e s:@NSS_LIBDIR@:%{NSS_LIBDIR}:g $JAVA_HOME/jre/lib/security/nss.cfg

# Build pulseaudio and install it to JDK build location
%if %{with_pulseaudio}
pushd pulseaudio
make JAVA_HOME=$JAVA_HOME -f Makefile.pulseaudio
cp -pPRf build/native/libpulse-java.so $JAVA_HOME/jre/lib/%{archinstall}/
cp -pPRf build/pulse-java.jar $JAVA_HOME/jre/lib/ext/
popd
%endif

# Copy tz.properties
echo "sun.zoneinfo.dir=/usr/share/javazi" >> $JAVA_HOME/jre/lib/tz.properties

#remove all fontconfig files. This change should be usptreamed soon
rm -f %{buildoutputdir}/j2re-image/lib/fontconfig*.properties.src
rm -f %{buildoutputdir}/j2re-image/lib/fontconfig*.bfc
rm -f %{buildoutputdir}/j2sdk-image/jre/lib/fontconfig*.properties.src
rm -f %{buildoutputdir}/j2sdk-image/jre/lib/fontconfig*.bfc
rm -f %{buildoutputdir}/lib/fontconfig*.properties.src
rm -f %{buildoutputdir}/lib/fontconfig*.bfc

# Check unlimited policy has been used
$JAVA_HOME/bin/javac -d . %{SOURCE12}
$JAVA_HOME/bin/java TestCryptoLevel

sh %{SOURCE11} ${JAVA_HOME}

%check
export JAVA_HOME=$(pwd)/%{buildoutputdir $suffix}/j2sdk-image


%install
rm -rf $RPM_BUILD_ROOT
STRIP_KEEP_SYMTAB=libjvm*

# There used to be a link to the soundfont.
# This is now obsolete following the inclusion of 8140620/PR2710

pushd %{buildoutputdir}/j2sdk-image

#install jsa directories so we can owe them
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{archinstall}/server/
mkdir -p $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/%{archinstall}/client/

  # Install main files.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  cp -a jre-abrt bin include lib src.zip $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
  cp -a jre/bin jre/lib $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}
  cp -a ASSEMBLY_EXCEPTION LICENSE THIRD_PARTY_README $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}

%ifarch %{jit_arches}
  # Install systemtap support files.
  install -dm 755 $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/tapset
  cp -a $RPM_BUILD_DIR/%{uniquesuffix}/tapset/*.stp $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/tapset/
  install -d -m 755 $RPM_BUILD_ROOT%{tapsetdir}
  pushd $RPM_BUILD_ROOT%{tapsetdir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{sdkdir}/tapset %{tapsetdir})
    ln -sf $RELATIVE/*.stp .
  popd
%endif

  # Install cacerts symlink.
  rm -f $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security/cacerts
  pushd $RPM_BUILD_ROOT%{_jvmdir}/%{jredir}/lib/security
    RELATIVE=$(%{abs2rel} %{_sysconfdir}/pki/java \
      %{_jvmdir}/%{jredir}/lib/security)
    ln -sf $RELATIVE/cacerts .
  popd

  # Install extension symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{jvmjardir}
  pushd $RPM_BUILD_ROOT%{jvmjardir}
    RELATIVE=$(%{abs2rel} %{_jvmdir}/%{jredir}/lib %{jvmjardir})
    ln -sf $RELATIVE/jsse.jar jsse-%{version}.jar
    ln -sf $RELATIVE/jce.jar jce-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-ldap-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-cos-%{version}.jar
    ln -sf $RELATIVE/rt.jar jndi-rmi-%{version}.jar
    ln -sf $RELATIVE/rt.jar jaas-%{version}.jar
    ln -sf $RELATIVE/rt.jar jdbc-stdext-%{version}.jar
    ln -sf jdbc-stdext-%{version}.jar jdbc-stdext-3.0.jar
    ln -sf $RELATIVE/rt.jar sasl-%{version}.jar
    for jar in *-%{version}.jar
    do
      if [ x%{version} != x%{javaver} ]
      then
        ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|-%{javaver}.jar|g")
      fi
      ln -sf $jar $(echo $jar | sed "s|-%{version}.jar|.jar|g")
    done
  popd

  # Install JCE policy symlinks.
  install -d -m 755 $RPM_BUILD_ROOT%{_jvmprivdir}/%{uniquesuffix}/jce/vanilla

  # Install versioned symlinks.
  pushd $RPM_BUILD_ROOT%{_jvmdir}
    ln -sf %{jredir} %{jrelnk}
  popd

  pushd $RPM_BUILD_ROOT%{_jvmjardir}
    ln -sf %{sdkdir} %{jrelnk}
  popd

  # Remove javaws man page
  rm -f man/man1/javaws*

  # Install man pages.
  install -d -m 755 $RPM_BUILD_ROOT%{_mandir}/man1
  for manpage in man/man1/*
  do
    # Convert man pages to UTF8 encoding.
    iconv -f ISO_8859-1 -t UTF8 $manpage -o $manpage.tmp
    mv -f $manpage.tmp $manpage
    install -m 644 -p $manpage $RPM_BUILD_ROOT%{_mandir}/man1/$(basename \
      $manpage .1)-%{uniquesuffix}.1
  done

  # Install demos and samples.
  cp -a demo $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}
  mkdir -p sample/rmi
  mv bin/java-rmi.cgi sample/rmi
  cp -a sample $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}

popd


# Install Javadoc documentation.
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}
cp -a %{buildoutputdir}/docs $RPM_BUILD_ROOT%{_javadocdir}/%{uniquejavadocdir}

# Install icons and menu entries.
for s in 16 24 32 48 ; do
  install -D -p -m 644 \
    openjdk/jdk/src/solaris/classes/sun/awt/X11/java-icon${s}.png \
    $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/${s}x${s}/apps/java-%{javaver}.png
done

# Install desktop files.
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/{applications,pixmaps}
for e in %{SOURCE7} %{SOURCE77} ; do
    sed -i "s/#ARCH#/%{_arch}-%{release}/g" $e
    sed -i "s|/usr/bin|%{sdkbindir}/|g" $e
    desktop-file-install --vendor=%{uniquesuffix} --mode=644 \
        --dir=$RPM_BUILD_ROOT%{_datadir}/applications $e
done

# Install /etc/.java/.systemPrefs/ directory
# See https://bugzilla.redhat.com/show_bug.cgi?id=741821
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/.java/.systemPrefs

# Find JRE directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type d \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}.files-headless
# Find JRE files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{jredir} -type f -o -type l \
  | grep -v jre/lib/security \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  > %{name}.files.all
#split %{name}.files to %{name}.files-headless and %{name}.files
#see https://bugzilla.redhat.com/show_bug.cgi?id=875408
NOT_HEADLESS=\
"%{_jvmdir}/%{uniquesuffix}/jre/lib/%{archinstall}/libjsoundalsa.so 
%{_jvmdir}/%{uniquesuffix}/jre/lib/%{archinstall}/libpulse-java.so 
%{_jvmdir}/%{uniquesuffix}/jre/lib/%{archinstall}/libsplashscreen.so 
%{_jvmdir}/%{uniquesuffix}/jre/lib/%{archinstall}/libjavagtk.so
%{_jvmdir}/%{uniquesuffix}/jre/lib/%{archinstall}/xawt/libmawt.so
%{_jvmdir}/%{uniquesuffix}/jre/bin/policytool
%{_jvmdir}/%{uniquesuffix}/jre-abrt/lib/%{archinstall}/libjsoundalsa.so 
%{_jvmdir}/%{uniquesuffix}/jre-abrt/lib/%{archinstall}/libpulse-java.so 
%{_jvmdir}/%{uniquesuffix}/jre-abrt/lib/%{archinstall}/libsplashscreen.so 
%{_jvmdir}/%{uniquesuffix}/jre-abrt/lib/%{archinstall}/libjavagtk.so
%{_jvmdir}/%{uniquesuffix}/jre-abrt/lib/%{archinstall}/xawt/libmawt.so"
#filter  %{name}.files from  %{name}.files.all to  %{name}.files-headless
ALL=`cat %{name}.files.all`
for file in $ALL ; do 
  INLCUDE="NO" ; 
  for blacklist in $NOT_HEADLESS ; do
#we can not match normally, because rpmbuild will evaluate !0 result as script failure
    q=`expr match "$file" "$blacklist"` || :
    l=`expr length  "$blacklist"` || :
    if [ $q -eq $l  ]; then 
      INLCUDE="YES" ; 
    fi;
  done
    if [ "x$INLCUDE" = "xNO"  ]; then 
      echo "$file" >> %{name}.files-headless
    else
      echo "$file" >> %{name}.files
    fi
done
# Find demo directories.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample -type d \
  | sed 's|'$RPM_BUILD_ROOT'|%dir |' \
  > %{name}-demo.files

# FIXME: remove SONAME entries from demo DSOs.  See
# https://bugzilla.redhat.com/show_bug.cgi?id=436497

# Find non-documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample \
  -type f -o -type l | sort \
  | grep -v README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  >> %{name}-demo.files
# Find documentation demo files.
find $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/demo \
  $RPM_BUILD_ROOT%{_jvmdir}/%{sdkdir}/sample \
  -type f -o -type l | sort \
  | grep README \
  | sed 's|'$RPM_BUILD_ROOT'||' \
  | sed 's|^|%doc |' \
  >> %{name}-demo.files

# intentionally after the files generation, as it goes to separate package
# Create links which leads to separately installed java-atk-bridge and allow configuration
# links points to java-atk-wrapper - an dependence
  pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/%{archinstall}
    ln -s %{syslibdir}/java-atk-wrapper/libatk-wrapper.so.0 libatk-wrapper.so
  popd
  pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/ext
     ln -s %{syslibdir}/java-atk-wrapper/java-atk-wrapper.jar  java-atk-wrapper.jar
  popd
  pushd $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir}/lib/
    echo "#Config file to  enable java-atk-wrapper" > accessibility.properties
    echo "" >> accessibility.properties
    echo "assistive_technologies=org.GNOME.Accessibility.AtkWrapper" >> accessibility.properties
    echo "" >> accessibility.properties
  popd

bash %{SOURCE20} $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir} %{javaver}
# https://bugzilla.redhat.com/show_bug.cgi?id=1183793
touch -t 201401010000 $RPM_BUILD_ROOT/%{_jvmdir}/%{jredir $suffix}/lib/security/java.security

# intentioanlly only for non-debug
%pretrans headless -p <lua>
-- see https://bugzilla.redhat.com/show_bug.cgi?id=1038092 for whole issue
-- see https://bugzilla.redhat.com/show_bug.cgi?id=1290388 for pretrans over pre
-- if copy-jdk-configs is in transaction, it installs in pretrans to temp
-- if copy_jdk_configs is in temp, then it means that copy-jdk-configs is in tranasction  and so is
-- preferred over one in %%{_libexecdir}. If it is not in transaction, then depends 
-- whether copy-jdk-configs is installed or not. If so, then configs are copied
-- (copy_jdk_configs from %%{_libexecdir} used) or not copied at all
local posix = require "posix"
local debug = false

SOURCE1 = "%{rpm_state_dir}/copy_jdk_configs.lua"
SOURCE2 = "%{_libexecdir}/copy_jdk_configs.lua"

local stat1 = posix.stat(SOURCE1, "type");
local stat2 = posix.stat(SOURCE2, "type");

  if (stat1 ~= nil) then
  if (debug) then
    print(SOURCE1 .." exists - copy-jdk-configs in transaction, using this one.")
  end;
  package.path = package.path .. ";" .. SOURCE1
else 
  if (stat2 ~= nil) then
  if (debug) then
    print(SOURCE2 .." exists - copy-jdk-configs alrady installed and NOT in transation. Using.")
  end;
  package.path = package.path .. ";" .. SOURCE2
  else
    if (debug) then
      print(SOURCE1 .." does NOT exists")
      print(SOURCE2 .." does NOT exists")
      print("No config files will be copied")
    end
  return
  end
end
-- run contetn of included file with fake args
arg = {"--currentjvm", "%{uniquesuffix %{nil}}", "--jvmdir", "%{_jvmdir %{nil}}", "--origname", "%{name}", "--origjavaver", "%{javaver}", "--arch", "%{_arch}", "--temp", "%{rpm_state_dir}/%{name}.%{_arch}"}
require "copy_jdk_configs.lua"

%post 
update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
exit 0


%post headless
%ifarch %{jit_arches}
# MetaspaceShared::generate_vtable_methods not implemented for PPC JIT
%ifnarch %{power64}
#see https://bugzilla.redhat.com/show_bug.cgi?id=513605
%{jrebindir}/java -Xshare:dump >/dev/null 2>/dev/null
%endif
%endif

ext=.gz
alternatives \
  --install %{_bindir}/java java %{jrebindir}/java %{priority} --family %{name}.%{_arch} \
  --slave %{_jvmdir}/jre jre %{_jvmdir}/%{jredir} \
  --slave %{_jvmjardir}/jre jre_exports %{jvmjardir} \
  --slave %{_bindir}/keytool keytool %{jrebindir}/keytool \
  --slave %{_bindir}/orbd orbd %{jrebindir}/orbd \
  --slave %{_bindir}/pack200 pack200 %{jrebindir}/pack200 \
  --slave %{_bindir}/rmid rmid %{jrebindir}/rmid \
  --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir}/rmiregistry \
  --slave %{_bindir}/servertool servertool %{jrebindir}/servertool \
  --slave %{_bindir}/tnameserv tnameserv %{jrebindir}/tnameserv \
  --slave %{_bindir}/unpack200 unpack200 %{jrebindir}/unpack200 \
  --slave %{_mandir}/man1/java.1$ext java.1$ext \
  %{_mandir}/man1/java-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/keytool.1$ext keytool.1$ext \
  %{_mandir}/man1/keytool-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/orbd.1$ext orbd.1$ext \
  %{_mandir}/man1/orbd-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/pack200.1$ext pack200.1$ext \
  %{_mandir}/man1/pack200-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/rmid.1$ext rmid.1$ext \
  %{_mandir}/man1/rmid-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/rmiregistry.1$ext rmiregistry.1$ext \
  %{_mandir}/man1/rmiregistry-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/servertool.1$ext servertool.1$ext \
  %{_mandir}/man1/servertool-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/tnameserv.1$ext tnameserv.1$ext \
  %{_mandir}/man1/tnameserv-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/unpack200.1$ext unpack200.1$ext \
  %{_mandir}/man1/unpack200-%{uniquesuffix}.1$ext

for X in %{origin} %{javaver} ; do
  alternatives \
    --install %{_jvmdir}/jre-"$X" \
    jre_"$X" %{_jvmdir}/%{jredir} %{priority} --family %{name}.%{_arch} \
    --slave %{_jvmjardir}/jre-"$X" \
    jre_"$X"_exports %{jvmjardir}
done

update-alternatives --install %{_jvmdir}/jre-%{javaver}-%{origin} jre_%{javaver}_%{origin} %{_jvmdir}/%{jrelnk} %{priority} --family %{name}.%{_arch} \
--slave %{_jvmjardir}/jre-%{javaver}       jre_%{javaver}_%{origin}_exports      %{jvmjardir}

update-desktop-database %{_datadir}/applications &> /dev/null || :

/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

# see pretrans where this file is declared
# also see that pretrans is only for nondebug
if [ ! "%1" == %{debug_suffix} ]; then
  if [ -f %{_libexecdir}/copy_jdk_configs_fixFiles.sh ] ; then
    sh  %{_libexecdir}/copy_jdk_configs_fixFiles.sh %{rpm_state_dir}/%{name}.%{_arch}  %{_jvmdir}/%{sdkdir %%1}
  fi
fi


exit 0

%postun
update-desktop-database %{_datadir}/applications &> /dev/null || :

if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

exit 0


%postun headless
  alternatives --remove java %{jrebindir}/java
  alternatives --remove jre_%{origin} %{_jvmdir}/%{jredir}
  alternatives --remove jre_%{javaver} %{_jvmdir}/%{jredir}
  alternatives --remove jre_%{javaver}_%{origin} %{_jvmdir}/%{jrelnk}

exit 0

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :



%post devel
ext=.gz
alternatives \
  --install %{_bindir}/javac javac %{sdkbindir}/javac %{priority} --family %{name}.%{_arch} \
  --slave %{_jvmdir}/java java_sdk %{_jvmdir}/%{sdkdir} \
  --slave %{_jvmjardir}/java java_sdk_exports %{_jvmjardir}/%{sdkdir} \
  --slave %{_bindir}/appletviewer appletviewer %{sdkbindir}/appletviewer \
  --slave %{_bindir}/apt apt %{sdkbindir}/apt \
  --slave %{_bindir}/extcheck extcheck %{sdkbindir}/extcheck \
  --slave %{_bindir}/idlj idlj %{sdkbindir}/idlj \
  --slave %{_bindir}/jar jar %{sdkbindir}/jar \
  --slave %{_bindir}/jarsigner jarsigner %{sdkbindir}/jarsigner \
  --slave %{_bindir}/javadoc javadoc %{sdkbindir}/javadoc \
  --slave %{_bindir}/javah javah %{sdkbindir}/javah \
  --slave %{_bindir}/javap javap %{sdkbindir}/javap \
  --slave %{_bindir}/jcmd jcmd %{sdkbindir}/jcmd \
  --slave %{_bindir}/jconsole jconsole %{sdkbindir}/jconsole \
  --slave %{_bindir}/jdb jdb %{sdkbindir}/jdb \
  --slave %{_bindir}/jhat jhat %{sdkbindir}/jhat \
  --slave %{_bindir}/jinfo jinfo %{sdkbindir}/jinfo \
  --slave %{_bindir}/jmap jmap %{sdkbindir}/jmap \
  --slave %{_bindir}/jps jps %{sdkbindir}/jps \
  --slave %{_bindir}/jrunscript jrunscript %{sdkbindir}/jrunscript \
  --slave %{_bindir}/jsadebugd jsadebugd %{sdkbindir}/jsadebugd \
  --slave %{_bindir}/jstack jstack %{sdkbindir}/jstack \
  --slave %{_bindir}/jstat jstat %{sdkbindir}/jstat \
  --slave %{_bindir}/jstatd jstatd %{sdkbindir}/jstatd \
  --slave %{_bindir}/native2ascii native2ascii %{sdkbindir}/native2ascii \
  --slave %{_bindir}/policytool policytool %{sdkbindir}/policytool \
  --slave %{_bindir}/rmic rmic %{sdkbindir}/rmic \
  --slave %{_bindir}/schemagen schemagen %{sdkbindir}/schemagen \
  --slave %{_bindir}/serialver serialver %{sdkbindir}/serialver \
  --slave %{_bindir}/wsgen wsgen %{sdkbindir}/wsgen \
  --slave %{_bindir}/wsimport wsimport %{sdkbindir}/wsimport \
  --slave %{_bindir}/xjc xjc %{sdkbindir}/xjc \
  --slave %{_mandir}/man1/appletviewer.1$ext appletviewer.1$ext \
  %{_mandir}/man1/appletviewer-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/apt.1$ext apt.1$ext \
  %{_mandir}/man1/apt-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/extcheck.1$ext extcheck.1$ext \
  %{_mandir}/man1/extcheck-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jar.1$ext jar.1$ext \
  %{_mandir}/man1/jar-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jarsigner.1$ext jarsigner.1$ext \
  %{_mandir}/man1/jarsigner-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/javac.1$ext javac.1$ext \
  %{_mandir}/man1/javac-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/javadoc.1$ext javadoc.1$ext \
  %{_mandir}/man1/javadoc-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/javah.1$ext javah.1$ext \
  %{_mandir}/man1/javah-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/javap.1$ext javap.1$ext \
  %{_mandir}/man1/javap-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jconsole.1$ext jconsole.1$ext \
  %{_mandir}/man1/jconsole-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jdb.1$ext jdb.1$ext \
  %{_mandir}/man1/jdb-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jhat.1$ext jhat.1$ext \
  %{_mandir}/man1/jhat-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jinfo.1$ext jinfo.1$ext \
  %{_mandir}/man1/jinfo-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jmap.1$ext jmap.1$ext \
  %{_mandir}/man1/jmap-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jps.1$ext jps.1$ext \
  %{_mandir}/man1/jps-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jrunscript.1$ext jrunscript.1$ext \
  %{_mandir}/man1/jrunscript-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jsadebugd.1$ext jsadebugd.1$ext \
  %{_mandir}/man1/jsadebugd-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jstack.1$ext jstack.1$ext \
  %{_mandir}/man1/jstack-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jstat.1$ext jstat.1$ext \
  %{_mandir}/man1/jstat-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/jstatd.1$ext jstatd.1$ext \
  %{_mandir}/man1/jstatd-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/native2ascii.1$ext native2ascii.1$ext \
  %{_mandir}/man1/native2ascii-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/policytool.1$ext policytool.1$ext \
  %{_mandir}/man1/policytool-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/rmic.1$ext rmic.1$ext \
  %{_mandir}/man1/rmic-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/schemagen.1$ext schemagen.1$ext \
  %{_mandir}/man1/schemagen-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/serialver.1$ext serialver.1$ext \
  %{_mandir}/man1/serialver-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/wsgen.1$ext wsgen.1$ext \
  %{_mandir}/man1/wsgen-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/wsimport.1$ext wsimport.1$ext \
  %{_mandir}/man1/wsimport-%{uniquesuffix}.1$ext \
  --slave %{_mandir}/man1/xjc.1$ext xjc.1$ext \
  %{_mandir}/man1/xjc-%{uniquesuffix}.1$ext

for X in %{origin} %{javaver} ; do
  alternatives \
    --install %{_jvmdir}/java-"$X" \
    java_sdk_"$X" %{_jvmdir}/%{sdkdir} %{priority} --family %{name}.%{_arch} \
    --slave %{_jvmjardir}/java-"$X" \
    java_sdk_"$X"_exports %{_jvmjardir}/%{sdkdir}
done

update-alternatives --install %{_jvmdir}/java-%{javaver}-%{origin} java_sdk_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir} %{priority} --family %{name}.%{_arch} \
--slave %{_jvmjardir}/java-%{javaver}-%{origin}       java_sdk_%{javaver}_%{origin}_exports      %{_jvmjardir}/%{sdkdir}

update-desktop-database %{_datadir}/applications &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

exit 0

%postun devel
  alternatives --remove javac %{sdkbindir}/javac
  alternatives --remove java_sdk_%{origin} %{_jvmdir}/%{sdkdir}
  alternatives --remove java_sdk_%{javaver} %{_jvmdir}/%{sdkdir}
  alternatives --remove java_sdk_%{javaver}_%{origin} %{_jvmdir}/%{sdkdir}

update-desktop-database %{_datadir}/applications &> /dev/null || :

if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

exit 0

%posttrans  devel
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%post javadoc
alternatives \
  --install %{_javadocdir}/java javadocdir %{_javadocdir}/%{uniquejavadocdir}/api \
  %{priority} --family %{name}

exit 0

%postun javadoc
  alternatives --remove javadocdir %{_javadocdir}/%{uniquejavadocdir}/api

exit 0


%files -f %{name}.files
%{_datadir}/icons/hicolor/*x*/apps/java-%{javaver}.png

# important note, see https://bugzilla.redhat.com/show_bug.cgi?id=1038092 for whole issue 
# all config/norepalce files (and more) have to be declared in pretrans. See pretrans
%files headless  -f %{name}.files-headless
%defattr(-,root,root,-)
%doc %{_jvmdir}/%{sdkdir}/ASSEMBLY_EXCEPTION
%doc %{_jvmdir}/%{sdkdir}/LICENSE
%doc %{_jvmdir}/%{sdkdir}/THIRD_PARTY_README
%dir %{_jvmdir}/%{sdkdir}
%dir %{_jvmdir}/%{sdkdir}/jre/lib/
%dir %{_jvmdir}/%{sdkdir}/jre/lib/%{archinstall}
%ifarch x86_64
%dir %{_jvmdir}/%{sdkdir}/jre/lib/%{archinstall}/xawt
%endif
%{_jvmdir}/%{jrelnk}
%{_jvmjardir}/%{jrelnk}
%{_jvmprivdir}/*
%{jvmjardir}
%dir %{_jvmdir}/%{jredir}/lib/security
%{_jvmdir}/%{jredir}/lib/security/cacerts
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/policy/unlimited/US_export_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/policy/unlimited/local_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/policy/limited/US_export_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/policy/limited/local_policy.jar
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.policy
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/java.security
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/blacklisted.certs
%config(noreplace) %{_jvmdir}/%{jredir}/lib/logging.properties
%{_mandir}/man1/java-%{uniquesuffix}.1*
%{_mandir}/man1/keytool-%{uniquesuffix}.1*
%{_mandir}/man1/orbd-%{uniquesuffix}.1*
%{_mandir}/man1/pack200-%{uniquesuffix}.1*
%{_mandir}/man1/rmid-%{uniquesuffix}.1*
%{_mandir}/man1/rmiregistry-%{uniquesuffix}.1*
%{_mandir}/man1/servertool-%{uniquesuffix}.1*
%{_mandir}/man1/tnameserv-%{uniquesuffix}.1*
%{_mandir}/man1/unpack200-%{uniquesuffix}.1*
%config(noreplace) %{_jvmdir}/%{jredir}/lib/security/nss.cfg
# removed %%{_jvmdir}/%%{jredir}/lib/audio/
# see soundfont in %%install
%ifarch %{jit_arches}
%attr(664, root, root) %ghost %{_jvmdir}/%{jredir}/lib/%{archinstall}/server/classes.jsa
%attr(664, root, root) %ghost %{_jvmdir}/%{jredir}/lib/%{archinstall}/client/classes.jsa
%endif
%{_jvmdir}/%{jredir}/lib/%{archinstall}/server/
%{_jvmdir}/%{jredir}/lib/%{archinstall}/client/
%{_sysconfdir}/.java/
%{_sysconfdir}/.java/.systemPrefs
%{_jvmdir}/%{sdkdir}/jre-abrt


%files devel
%defattr(-,root,root,-)
%doc %{_jvmdir}/%{sdkdir}/ASSEMBLY_EXCEPTION
%doc %{_jvmdir}/%{sdkdir}/LICENSE
%doc %{_jvmdir}/%{sdkdir}/THIRD_PARTY_README
%dir %{_jvmdir}/%{sdkdir}/bin
%dir %{_jvmdir}/%{sdkdir}/include
%dir %{_jvmdir}/%{sdkdir}/lib
%ifarch %{jit_arches}
%dir %{_jvmdir}/%{sdkdir}/tapset
%endif
%{_jvmdir}/%{sdkdir}/bin/*
%{_jvmdir}/%{sdkdir}/include/*
%{_jvmdir}/%{sdkdir}/lib/*
%ifarch %{jit_arches}
%{_jvmdir}/%{sdkdir}/tapset/*.stp
%endif
%{_jvmjardir}/%{sdkdir}
%{_datadir}/applications/*jconsole.desktop
%{_datadir}/applications/*policytool.desktop
%{_mandir}/man1/appletviewer-%{uniquesuffix}.1*
%{_mandir}/man1/apt-%{uniquesuffix}.1*
%{_mandir}/man1/extcheck-%{uniquesuffix}.1*
%{_mandir}/man1/idlj-%{uniquesuffix}.1*
%{_mandir}/man1/jar-%{uniquesuffix}.1*
%{_mandir}/man1/jarsigner-%{uniquesuffix}.1*
%{_mandir}/man1/javac-%{uniquesuffix}.1*
%{_mandir}/man1/javadoc-%{uniquesuffix}.1*
%{_mandir}/man1/javah-%{uniquesuffix}.1*
%{_mandir}/man1/javap-%{uniquesuffix}.1*
%{_mandir}/man1/jconsole-%{uniquesuffix}.1*
%{_mandir}/man1/jcmd-%{uniquesuffix}.1*
%{_mandir}/man1/jdb-%{uniquesuffix}.1*
%{_mandir}/man1/jhat-%{uniquesuffix}.1*
%{_mandir}/man1/jinfo-%{uniquesuffix}.1*
%{_mandir}/man1/jmap-%{uniquesuffix}.1*
%{_mandir}/man1/jps-%{uniquesuffix}.1*
%{_mandir}/man1/jrunscript-%{uniquesuffix}.1*
%{_mandir}/man1/jsadebugd-%{uniquesuffix}.1*
%{_mandir}/man1/jstack-%{uniquesuffix}.1*
%{_mandir}/man1/jstat-%{uniquesuffix}.1*
%{_mandir}/man1/jstatd-%{uniquesuffix}.1*
%{_mandir}/man1/native2ascii-%{uniquesuffix}.1*
%{_mandir}/man1/policytool-%{uniquesuffix}.1*
%{_mandir}/man1/rmic-%{uniquesuffix}.1*
%{_mandir}/man1/schemagen-%{uniquesuffix}.1*
%{_mandir}/man1/serialver-%{uniquesuffix}.1*
%{_mandir}/man1/wsgen-%{uniquesuffix}.1*
%{_mandir}/man1/wsimport-%{uniquesuffix}.1*
%{_mandir}/man1/xjc-%{uniquesuffix}.1*
%ifarch %{jit_arches}
%{tapsetroot}
%endif

%files demo -f %{name}-demo.files
%defattr(-,root,root,-)
%doc %{_jvmdir}/%{sdkdir}/LICENSE

%files src
%defattr(-,root,root,-)
%doc README.src
%{_jvmdir}/%{sdkdir}/src.zip

%files javadoc
%defattr(-,root,root,-)
%doc %{_javadocdir}/%{uniquejavadocdir}
%doc %{buildoutputdir}/j2sdk-image/jre/LICENSE

%files accessibility
%{_jvmdir}/%{jredir}/lib/%{archinstall}/libatk-wrapper.so
%{_jvmdir}/%{jredir}/lib/ext/java-atk-wrapper.jar
%{_jvmdir}/%{jredir}/lib/accessibility.properties

%changelog
* Tue Nov 28 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.161-2.6.12.0
- Remove superfluous %%1 from policy JAR file path.
- Resolves: rhbz#1499207

* Tue Nov 28 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.161-2.6.12.0
- Add missing implementation of Matcher::pass_original_key_for_aes() on AArch64 (PR3497)
- Resolves: rhbz#1499207

* Tue Nov 28 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.161-2.6.12.0
- Update location of policy JAR files following 8157561.
- Resolves: rhbz#1499207

* Tue Nov 28 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.161-2.6.12.0
- Fix name of SystemTap tarball, following update.
- Resolves: rhbz#1499207

* Tue Nov 28 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.161-2.6.12.0
- Bump to 2.6.12 and u161b00.
- Update SystemTap tapsets to version in IcedTea 2.6.12pre01 to fix RH1492139.
- Drop 8185716 patch, now applied upstream.
- Update location of OpenJDK zlib system library source code in remove-intree-libraries.sh
- Resolves: rhbz#1499207

* Wed Aug 02 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.151-2.6.11.1
- Apply fix for 8185716 so ppc uses correct ins_encode format
- Resolves: rhbz#1466509

* Wed Aug 02 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.151-2.6.11.1
- Bump to 2.6.11 and u151b00.
- Update java-access-bridge-security.patch to apply against 2.6.11.
- Drop 7177216 merge fix which is applied upstream.
- Resolves: rhbz#1466509

* Tue Jun 13 2017 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.141-2.6.10.5
- make to use latest c-j-c and so fix persisting issues with java.security and other configfiles
- aligned with this change, applied repackReproduciblePolycies.sh
- 1183793 is missing blocker
- Resolves: rhbz#1448880

* Wed Jun 07 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.141-2.6.10.4
- Fix merge error with "native2ascii changes file permissions of input file"
- Resolves: rhbz#1446700

* Wed May 17 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.141-2.6.10.3
- Add support for using RSAandMGF1 with the SHA hash algorithms in the PKCS11 provider 
- Resolves: rhbz#1273760

* Wed May 03 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.141-2.6.10.2
- Bump to u141b02 to include S8011123 fix for TCK failure.
- Resolves: rhbz#1438751

* Thu Apr 27 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.141-2.6.10.1
- Bump to u141b01 to include S8043723 fix for s390.
- Resolves: rhbz#1438751

* Thu Apr 27 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.141-2.6.10.1
- Bump to 2.6.10 and u141b00.
- Add more detailed output to fsg.sh and generate_source_tarball.sh.
- Update md5sum list with checksum for the new java.security file.
- Drop 8173783 backport which is now applied upstream.
- Resolves: rhbz#1438751

* Wed Apr 05 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.131-2.6.9.3
- Backport "8173783: IllegalArgumentException: jdk.tls.namedGroups"
- Apply backports before local RPM fixes so they will be the same as when applied upstream
- Adjust RH1022017 following application of 8173783
- Resolves: rhbz#1422738

* Tue Apr 04 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.131-2.6.9.2
- Introduce stapinstall variable to set SystemTap arch directory correctly (e.g. arm64 on aarch64)
- Update jstack tapset to handle AArch64
- Handle unsupported architectures by calling the error function rather than a parse failure
- ABS_JAVA_HOME_DIR is no longer used in the updated tapsets
- Resolves: rhbz#1373986

* Tue Feb 07 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.131-2.6.9.1
- Bump to 2.6.9 and u131b00.
- Remove patch application debris in fsg.sh.
- Re-generate PR2809 and RH1022017 against 2.6.9.
- Update md5sum list with checksum for the new java.security file.
- Add blacklisted.certs to installation file list.
- Resolves: rhbz#1410612

* Mon Jan 09 2017 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.121-2.6.8.1
- Bump release for rhel-7.4 branch. Fix "luncher" typo.
- Resolves: rhbz#1383251

* Mon Oct 31 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.121-2.6.8.0
- Turn off HotSpot bootstrap to see if it resolves build issues.
- Resolves: rhbz#1381990

* Fri Oct 28 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.121-2.6.8.0
- Bump to 2.6.8 and u121b00.
- Drop patches (S7081817, S8140344, S8145017 and S8162344) applied upstream.
- Update md5sum list with checksum for the new java.security file.
- Resolves: rhbz#1381990

* Mon Sep 05 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.111-2.6.7.7
- Rebuild java-1.7.0-openjdk for GCC aarch64 stack epilogue code generation fix (RH1372747)
- Resolves: rhbz#1350042

* Wed Aug 31 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.111-2.6.7.6
- declared check_sum_presented_in_spec and used in prep and check
- it is checking that latest packed java.security is mentioned in listing
- Resolves: rhbz#1350042

* Wed Aug 31 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.111-2.6.7.6
- New variable, @prefix@, needs to be substituted in tapsets (rhbz1371005)
- Resolves: rhbz#1350042

* Wed Aug 31 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.111-2.6.7.5
- Change to disable RC4 did not add MD5 checksum of previous java.security file from 2016/01
- Resolves: rhbz#1350042

* Tue Jul 26 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.111-2.6.7.4
- Require a version of java-1.7.0-openjdk-devel with a working jar uf
- Use readlink rather than a wildcard to resolve the system JDK directory
- Resolves: rhbz#1350042

* Fri Jul 22 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.111-2.6.7.3
- Add additional changes to 8162344 to fix issues which only show up on a full build.
- Resolves: rhbz#1350042

* Fri Jul 22 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.111-2.6.7.3
- Bump to jdk7u111 b01 to fix TCK regressions (7081817 & 8162344)
- Resolves: rhbz#1350042

* Thu Jul 21 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.111-2.6.7.2
- Reset permissions of resources.jar to avoid it only being readable by root (PR1437).
- Resolves: rhbz#1350042

* Wed Jul 20 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.111-2.6.7.1
- Bump to 2.6.7 and u111b00.
- Update SystemTap bundle with fix for PR3091/RH1204159
- Drop patches (PR2938, PR2939, PR3012, PR3013 and PR1437) applied upstream.
- Resolves: rhbz#1350042

* Thu Jun 30 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.101-2.6.6.6
- Add fix for PR1437 which reapplies 7175845 fix lost in merge.
- Resolves: rhbz#1207129

* Thu Jun 30 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.101-2.6.6.6
- Add fix for 8069181/PR3012 and pre-requisites from PR3013.
- Add bug information for backports from last CPU.
- Resolves: rhbz#1015612

* Tue Jun 21 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.101-2.6.6.4
- luascripts extracted and used from separate package
- added requirement on at least build time nss
- added --family and dependence on chkconfig >=1.7
- in adition, family is restricted by arch
- Resolves: rhbz#1296441
- Resolves: rhbz#1296413

* Tue Jun 07 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.101-2.6.6.3
- added requires for copy-jdk-configs, to help with https://projects.engineering.redhat.com/browse/RCM-3654
- Resolves: rhbz#1296441

* Tue Apr 19 2016 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.101-2.6.6.2
- added Patch666 fontpath.patch to fix tck regressions
- Resolves: rhbz#1325428

* Mon Apr 18 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.101-2.6.6.1
- Fix ztos handling in templateTable_ppc_64.cpp to be same as others in 7.
- Resolves: rhbz#1325428

* Mon Apr 18 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.101-2.6.6.1
- Bump to 2.6.6 and u101b00.
- Drop AArch64 patch (PR2914) included in 2.6.6
- Drop a leading zero from the priority as the update version is now three digits
- Update PR2809 patch to apply against 2.6.6.
- Resolves: rhbz#1325428

* Mon Apr 18 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.99-2.6.5.5
- Backout S4858370.
- Resolves: rhbz#1284948

* Wed Apr 06 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.99-2.6.5.4
- Replace 8146709 backout with fix from Andrew Haley
- Resolves: rhbz#1310061

* Tue Apr 05 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.99-2.6.5.3
- Backout 8146709 to try and fix build on AArch64
- Resolves: rhbz#1310061

* Mon Apr 04 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.99-2.6.5.2
- Add fix for S4858370.
- Resolves: rhbz#1284948

* Thu Mar 24 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.99-2.6.5.1
- Bump to 2.6.5 and u99b00.
- Correct check for fsg.sh in tarball creation script
- Drop AArch64 ADRP backports (8143067, 8146709) included in 2.6.5
- Resolves: rhbz#1320659

* Thu Mar 03 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.95-2.6.4.3
- Add AArch64 ADRP backports
- Resolves: rhbz#1310061

* Wed Jan 27 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.95-2.6.4.2
- Disable RC4 by default.
- Resolves: rhbz#1302385

* Tue Jan 19 2016 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.95-2.6.4.1
- Bump to 2.6.4 and u95b00.
- Backport tarball creation script from OpenJDK 8 RPMs and update fsg.sh to work with it.
- Drop 8072932or8074489 patch as applied upstream in u91b01.
- Add MD5 checksums for last two version of the java.security file.
- Correct date of ChangeLog entry below.
- Resolves: rhbz#1295769

* Thu Nov 12 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.91-2.6.2.4
- fixed headless to become headless again
 - jre/lib/archinstall/libjavagtk.so
 - jre/bin/policytool
 - jre-abrt/lib/archinstall/libjavagtk.so
 - all three added to not headless exclude list
- see rhbz1141123
- Resolves: rhbz#1278987

* Tue Oct 20 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.91-2.6.2.3
- added and applied patch500 8072932or8074489.patch to fix tck failure
- Resolves: rhbz#1271923

* Mon Oct 19 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.91-2.6.2.2
- Turn off deletion of in-tree LCMS sources as we now need them.
- Resolves: rhbz#1271923

* Mon Oct 19 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.91-2.6.2.1
- Bump to 2.6.2 and u91b00.
- Disable system LCMS 2 for now until security of it can be verified.
- Drop patches for PR2560/RH1245855 as now applied upstream.
- Sync minor changes from RHEL 6 spec file.
- Resolves: rhbz#1271923

* Wed Oct 14 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.85-2.6.1.7
- removed link to soundfont. Unused in rhel7 and will be fixed upstream
- Resolves: rhbz#1257653

* Mon Aug 31 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.85-2.6.1.6
- bumped release to allow update testing of previous chnageset
- Resolves: rhbz#1235159

* Mon Aug 31 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.85-2.6.1.5
- removed rm -rf in headless post
- Resolves: rhbz#1235159

* Mon Jul 27 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.85-2.6.1.4
- Backport JDWP null fixes.
- Resolves: rhbz#1245855

* Thu Jul 23 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.85-2.6.1.3
- Backport fixes for debugger crash
- Resolves: rhbz#1245855

* Sat Jul 11 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.85-2.6.1.2
- Bump upstream tarball to u25b01 to fix issue with 8075374 backport.
- Resolves: rhbz#1235159

* Thu Jul 09 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.85-2.6.1.1
- Update OpenJDK tarball so correct version is used.
- Resolves: rhbz#1235159

* Thu Jul 09 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.85-2.6.1.0
- Add additional java.security md5sum from January CPU
- Resolves: rhbz#1235159

* Thu Jul 09 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.85-2.6.1.0
- Bump to 2.6.1 and u85b00.
- Resolves: rhbz#1235159

* Wed Jul 08 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.80-2.6.0.1
- Pass SYSTEM_GSETTINGS="true" to the OpenJDK build to explicitly enable the GSettings API.
- Resolves: rhbz#1194226

* Wed Jul 08 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.80-2.6.0.0
- Add GConf2-devel dependency for native proxy fallback support.
- Remove libxslt dependency pulled in from IcedTea builds.
- Reduce redhat-lsb dependency to redhat-lsb-core (lsb_release)
- Resolves: rhbz#1194226

* Wed Jul 08 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.80-2.6.0.0
- Bump to 2.6.0 and u80b32.
- Drop upstreamed patches and separate AArch64 HotSpot.
- Add dependencies on pcsc-lite-devel (PR2496) and lksctp-tools-devel (PR2446)
- Only run -Xshare:dump on JIT archs other than power64 as port lacks support
- Update remove-intree-libraries script to cover LCMS and PCSC headers.
- Resolves: rhbz#1194226

* Wed Jun 24 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.79-2.5.5.4
- Fix name resolution when /etc/resolv.conf lists an IPv6 nameserver
- Resolves: rhbz#1203666

* Wed Apr 29 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.79-2.5.5.3
- Re-based SunEC changes onto latest RPM from private branch
- Resolves: rhbz#1121210

* Fri Apr 24 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.79-2.5.5.2
- Fix crash on ppc64le when running Apache Oozie
- Resolves: rhbz#1201393

* Fri Apr 10 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.79-2.5.5.1
- repacked sources
- Resolves: rhbz#1209073

* Tue Apr 07 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.79-2.5.5.0
- Bump to 2.5.5 using OpenJDK 7u79 b14.
- Update OpenJDK tarball creation comments
- Remove test case for RH1191652 now fix has been verified.
- Drop AArch64 version of RH1191652 HotSpot patch as included upstream.
- Resolves: rhbz#1209073

* Wed Mar 04 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.7
- ppc64le now has pulseaudio
- Resolves: rhbz#1191652

* Tue Mar 03 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.6
- Fix use of unapproved bug ID (resolved as duplicate) in changelog entry.
- Resolves: rhbz#1191652

* Tue Mar 03 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.6
- Provide AArch64 version of RH1191652 HotSpot patch.
- Resolves: rhbz#1191652

* Fri Feb 27 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Turn off hsbootstrap on all archs
- Resolves: rhbz#1191652

* Fri Feb 27 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Add missing bracket.
- Resolves: rhbz#1191652

* Fri Feb 27 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Turn off hsbootstrap on all archs
- Resolves: rhbz#1191652

* Fri Feb 27 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Add missing bracket.
- Resolves: rhbz#1191652

* Fri Feb 27 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Ensure VM directory exists before copying libjvm.so
- Resolves: rhbz#1191652

* Fri Feb 27 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Fix path to libjvm.so used in hsbootstrap to a more general one.
- Resolves: rhbz#1191652

* Thu Feb 26 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Fix hsbootstrap option on ppc64le where JDK_TO_BUILD_WITH is changed.
- Print uname to feedback to upstream OpenJDK.
- Resolves: rhbz#1191652

* Thu Feb 26 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Test a hsbootstrap build on ppc64le
- Resolves: rhbz#1191652

* Fri Feb 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Adjust archbuild instead as JDK build is now using ppc64le
- Resolves: rhbz#1191652

* Fri Feb 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Add ppc64le defines for javax.sound
- Resolves: rhbz#1191652

* Fri Feb 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Add jvm.cfg for ppc64le
- Resolves: rhbz#1191652

* Fri Feb 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Adjust archbuild instead as JDK build is now using ppc64le
- Resolves: rhbz#1191652

* Fri Feb 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Add ppc64le defines for javax.sound
- Resolves: rhbz#1191652

* Fri Feb 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Add jvm.cfg for ppc64le
- Resolves: rhbz#1191652

* Fri Feb 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Add patch for RH1191652 on the JDK side
- Resolves: rhbz#1191652

* Fri Feb 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Adjust archinstall and ppc64le workaround to establish jre/lib/ppc64le
- Resolves: rhbz#1191652

* Fri Feb 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Fix patch for RH1191652 to override LIBARCH on ppc64le as there is no BUILDARCH
- Resolves: rhbz#1191652

* Fri Feb 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Fix patch for RH1191652 to apply against 2.5 (original against HEAD)
- Resolves: rhbz#1191652

* Fri Feb 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Fix patch for RH1191652 to override LIBARCH on ppc64le as there is no BUILDARCH
- Resolves: rhbz#1191652

* Fri Feb 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Fix patch for RH1191652 to apply against 2.5 (original against HEAD)
- Resolves: rhbz#1191652

* Fri Feb 13 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.5
- Use arch name of ppc64le on ppc64le rather than ppc64.
- Resolves: rhbz#1191652

* Mon Feb 02 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.4
- Symlink ppc64 directory to ppc64le
- Run test application to print architecture-specific paths stored in the JDK
- Resolves: rhbz#1191652

* Tue Jan 27 2015 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.75-2.5.4.3
- removed source14 remove-origin-from-rpaths (1169097)
- removed build requirement for chrpath
- Resolves: rhbz#1180298

* Fri Jan 16 2015 Severin Gehwolf <sgehwolf@redhat.com> - 1:1.7.0.75-2.5.4.2
- Replace unmodified java.security file via headless post scriptlet.
- Resolves: rhbz#1180298

* Sun Jan 11 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.1
- Fix macro expansion in changelog
- Resolves: rhbz#1180298

* Fri Jan 09 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.1
- Fix elliptic curve list as part of fsg.sh
- Resolves: rhbz#1180298

* Fri Jan 09 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.1
- Bump release so that the RHEL 7.1 version is built on AArch64.
- Resolves: rhbz#1180298

* Fri Jan 09 2015 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.75-2.5.4.0
- Bump to 2.5.4 using OpenJDK 7u75 b13.
- Bump AArch64 port to 2.6.0pre17.
- Fix abrt_friendly_hs_log_jdk7.patch to apply again and enable on all archs.
- Remove OpenJDK 8 / AArch64 version of PStack patch as this is no longer needed.
- Resolves: rhbz#1180298

* Tue Dec 16 2014 Jiri Vanek <jvanek@redhat.com> - 1:1.7.0.71-2.5.3.4
- aarch64 sources updated to most recent stable tag
- adapted patch4030 PStack-808293-aarch64.patch
- removed upstreamed CPU patches (patch500-509, 20141014*)
- Resolves: rhbz#1125260

* Mon Oct 06 2014 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.71-2.5.3.3
- Set ENABLE_FULL_DEBUG_SYMBOLS=0 for aarch64 to retain debuginfo in files.
- Resolves: rhbz#1148894

* Sat Oct 04 2014 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.71-2.5.3.2
- Add HS security patches for aarch64.
- Resolves: rhbz#1148894

* Fri Oct 03 2014 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.71-2.5.3.1
- Bump to 2.5.3 for latest security fixes.
- Remove obsolete patches and CFLAGS which are now upstream.
- Add hsbootstrap option to pre-build HotSpot when required.
- Resolves: rhbz#1148894

* Thu Oct 02 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1.7.0.65-2.5.1.12
- Bump release for self-build.
- Resolves: RHBZ#1125557.

* Tue Sep 23 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1.7.0.65-2.5.1.11
- Add hotspot compiler flag -fno-tree-vectorize which fixes the segfault in
  the bytecode verifier on ppc/ppc64.

* Tue Sep 23 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1.7.0.65-2.5.1.10
- Add patches for PPC zero build.
- Fixes stack overflow problem. See RHBZ#1015432.
- Fixes missing memory barrier in Atomic::xchg*
- Fixes missing PPC32/PPC64 defines for Zero builds on power.

* Mon Sep 22 2014 Severin Gehwolf <sgehwolf@redhat.com> - 1.7.0.65-2.5.1.9
- Remove obsolete PPC/PPC64 patches.

* Thu Sep 11 2014 Omair Majid <omajid@redhat.com> - 1.7.0.65-2.5.1.8
- Update aarch64 port to jdk7u60_b04_aarch64_834
- Resolves: rhbz#1082779

* Tue Aug 19 2014 Jiri Vanek  <jvanek@redhat.com> - 1.7.0.65-2.5.1.7
- added and applied patch666 stackoverflow-ppc32_64-20140828.patch
- returned ppc (rebuild in brew must be done by 2.4.x)
- Resolves: rhbz#1125557

* Tue Aug 19 2014 Jiri Vanek  <jvanek@redhat.com> - 1.7.0.65-2.5.1.6
- added ExcludeArch: ppc
- Resolves: rhbz#1125557

* Mon Aug 04 2014 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.65-2.5.1.5
- Add workaround to build on ppc64le where arch directory is still ppc64le, not ppc64
- Resolves: rhbz#1125557

* Wed Jul 30 2014 Omair Majid <omajid@redhat.com> - 1.7.0.65-2.5.1.4
- Bump release to build package on aarch64
- Resolves: rhbz#1082779

* Wed Jul 30 2014 Jiri Vanek  <jvanek@redhat.com> - 1.7.0.65-2.5.1.3
- Update aarch64 to latest version
- Resolves: rhbz#1082779

* Thu Jul 17 2014 Andrew Hughes <ahughes@redhat.com> - 1:1.7.0.65-2.5.1.3
- NSS_LIBS should be set from nss pkgconfig, not nss-softokn
- Resolves: rhbz#1121210

* Mon Jul 14 2014 Jiri Vanek  <jvanek@redhat.com> - 1.7.0.65-2.5.1.2
- added and applied fix for samrtcard io patch405, pr1864_smartcardIO.patch
- Resolves: rhbz#1115877

* Mon Jul 07 2014 Jiri Vanek  <jvanek@redhat.com> - 1.7.0.65-2.5.1.1
- updated to security patched icedtea7-forest-2.5.1
- Resolves: rhbz#1115877

* Wed Jul 02 2014 Jiri Vanek  <jvanek@redhat.com> - 1.7.0.60-2.5.0.3
- updated to icedtea7-forest-2.5.0 (rh1114934)
- Resolves: rhbz#1099566

* Tue Jul 01 2014 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.60-2.5.0.2
- Add nss-softokn dependency for SunEC provider
- Resolves: rhbz#1121210

* Mon Jun 30 2014 Andrew Hughes <gnu.andrew@redhat.com> - 1:1.7.0.60-2.5.0.1
- Enable SunEC provider with system NSS support.
- Resolves: rhbz#1121210

* Fri May 30 2014 Andrew John Hughes <gnu.andrew@redhat.com> - 1.7.0.55-2.4.7.2
- Remove NSS patches. Issues with PKCS11 provider mean it shouldn't be enabled.
- Always setup nss.cfg and depend on nss-devel at build-time to do so.
- This allows users who wish to use PKCS11+NSS to just add it to java.security.
- Patches to PKCS11 provider will be included upstream in 2.4.8 (ETA July 2014)
- Resolves: rhbz#1099565

* Tue May 20 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.55-2.4.7.0.el7
- bumped to future icedtea-forest 2.4.7
- updatever set to 55, buildver se to 13, release reset to 0
- removed upstreamed patch402 gstackbounds.patch
- removed Requires: rhino, BuildRequires is enough
- ppc64 repalced by power64 macro
- patch111 applied as dry-run (6.6 forward port)
- nss enabled, but notused as default (6.6 forward port)
- Resolves: rhbz#1099565

* Fri Apr 04 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.4.5.5.el7
- added OrderWithRequires on headless where possible
- Resolves: rhbz#1038092

* Thu Mar 27 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.4.5.3.el7
- synced lua script from fedora.
- Resolves: rhbz#1038092

* Fri Mar 14 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.4.5.2.el7
- added fstack-protector-strong to CFLAGS
- Resolves: rhbz#1070816

* Thu Mar 06 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.4.5.1.el7
- diabled NSS. Missuisng 1038092 for it as it is in hurry.
- Related: rhbz#1038092

* Thu Jan 30 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.4.5.0.el7
- updated to icedtea 2.4.5 + sync with f21
 - http://blog.fuseyism.com/index.php/2014/01/29/icedtea-2-4-5-released/
- removed buildRequires: pulseaudio >= 0.9.11, as not neccessary
 -  but kept libs-devel)
- removed upstreamed or unwonted patches (thanx to gnu_andrew to pointing them out)
 - patch410 1015432.patch (upstreamed)
 - patch411 1029588.patch
 - patch412 zero-x32.diff
 - patch104 java-1.7.0-ppc-zero-jdk.patch
 - patch105 java-1.7.0-ppc-zero-hotspot.patch
- patch402 gstackbounds.patch and patch403 PStack-808293.patch applied always
 (again thanx to gnu_andrew)
- merged other gnu_andrew's changes
 - FT2_CFLAGS and FT2_LIBS hardoced values replaced by correct pkg-config calls 
 - buildver bumbed to 31
- added build requires  nss-devel
- removed build requires mercurial
- added JRE_RELEASE_VERSION and ALT_PARALLEL_COMPILE_JOBS into make call
- Related: rhbz1038092

* Tue Jan 28 2014 Daniel Mach <dmach@redhat.com> - 1.7.0.51-2.4.4.1
- Mass rebuild 2014-01-24

* Fri Jan 10 2014 Jiri Vanek <jvanek@redhat.com> - 1.7.0.51-2.4.4.0.el7
- updated to security icedtea 2.4.4
 - icedtea_version set to 2.4.4
 - updatever bumped to       51
 - release reset to 0
- sync with fedora
 - added and applied patch411 1029588.patch (rh 1029588)
 - added aand applied patch410, 1015432 (rh 1015432)
 - and so removed patch121 FixPPC64StackOverflow.patch
- added patch412 zero-x32.diff to try to fix zero builds build
- Resolves: rhbz#1053280

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.7.0.45-2.4.3.5.el7 
- Mass rebuild 2013-12-27

* Thu Oct 31 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.3.4.fel7
- Removed obsoletes for java-1.6.0-openjdk* ,  until decided its presence in el7
- Resolves:rhbz#1018680

* Thu Oct 31 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.3.3.fel7
- just bumped release, need to confirm, that   patch121, FixPPC64StackOverflow.patch
  really works
- Resolves:rhbz#1018680

* Wed Oct 16 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.3.2.fel7
- added and applied patch121, FixPPC64StackOverflow.patch
- all redundant ppc64 strings replaced by power64 macro
- Resolves:rhbz#1018680

* Wed Oct 16 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.3.1.fel7
- updated to new  CPU sources 2.4.3
- Resolves:rhbz#1018680

* Mon Oct 14 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.3.0.fel7
- updated to latest CPU sources 2.4.3
- Resolves:rhbz#1018680

* Mon Oct 14 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.12.fel7
- jdk splitted to headless and rest
- Resolves:rhbz#875408

* Fri Oct 04 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.11.fel7
- another tapset fix 
- Resolves:rhbz#875408

* Fri Oct 04 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.10.fel7
- abrt changed to soft dependece
- Resolves:rhbz#875408

* Thu Oct 03 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.9.el7
- renamed tapset source to be "versioned"
- improved agent placement
- Resolves:rhbz#875408

* Wed Oct 02 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.8.el7
- updated tapset to current head (825824)
- Resolves:rhbz#875408

* Tue Oct 01 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.7.el7
- fixed incorrect  _jvmdir/jre-javaver_origin to  _jvmdir/jre-javaver-origin link
- Resolves:rhbz#875408

* Tue Oct 01 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.6.el7
- syncing with f20 - abrt connector
- Resolves:rhbz#875408

* Tue Oct 01 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.40-2.4.2.3.el7
- syncing with f19/rhel-6.5
- Resolves:rhbz#875408


* Wed Aug 07 2013 Deepak Bhole <dbhole@redhat.com> - 1.7.0.25-2.3.12.3.el7
- Removed obsoletes for java-1.6.0-openjdk*

* Fri Jul 26 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.12.2.el7
- refreshed icedtea7-forest 2.3.12
- fix broken jre_exports alternatives links (thanx to orion bug #979128)

* Thu Jul 25 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.11.0.el7
- added new alternatives jre-1.7.0-openjdk and java-1.7.0-openjdk 
- finally merged arm and main source tarballs
- updated to icedtea 2.3.11
 - http://blog.fuseyism.com/index.php/2013/07/25/icedtea-2-3-11-released/
- added removal of new jre-1.7.0-openjdk and java-1.7.0-openjdk alternatives
- removed patch 400, rhino for 2.1 and other 2.1 conditional stuff
- removed patch 103 arm-fixes.patch
- removed "dir" from files which was duplicating jre in sdk

* Fri Jul 19 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.6.el7
- jrelnk is now just lnk, everything is pointing through jredir

* Thu Jul 18 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.6.el7
- minor cleaning
- sdklnk removed, and substitued by  sdkdir

* Wed Jul 03 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.5.fel7
- moved to xz compression of sources
- updated 2.1 tarball

* Thu Jun 27 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.4.el7
- Sync with upstream IcedTea7-forest 2.3.10 tag
- Fixes regressions as introduced with 1.7.0.25-2.3.10.3.el6:
  rhbz#978005, rhbz#977979, rhbz#976693, IcedTeaBZ#1487.
- all patch commands repalced by patch macro
  - updated java-1.7.0-openjdk-ppc-zero-hotspot.patch to pass without loose patching

* Wed Jun 19 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.3.el7
- update of IcedTea7-forest 2.3.10 tarball
- removed patch1000 MBeanFix.patch to fix regressions caused by security patches


* Thu Jun 13 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.2.el7
- added patch1000 MBeanFix.patch to fix regressions caused by security patches

* Thu Jun 13 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.25-2.3.10.1.el7
- arm tarball updated to 2.1.9
- build bumped to 25

* Wed Jun 12 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.10.0.el7
- fixed RH972717 by enabling patch110 java-1.7.0-openjdk-nss-icedtea-e9c857dcb964.patch
- temporarly swithced to intree lcms as it have security fixes (patch 500)
 - added  GENSRCDIR="$PWD/generated.build" to be able to
 - removed (build)requires  lcms2(-devel)
- Updated to latest IcedTea7-forest 2.3.10

* Wed Jun 05 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.9.14.fc19
- Added client/server directories so they can be owned
- Renamed patch 107 to 200
- Added nss support from 6.5
- Added fix for RH857717, owned /etc/.java/ and /etc/.java/.systemPrefs
- Removed ant-nodeps, should not be needed

* Tue May 28 2013 Jiri Vanek <jvanek@redhat.com> - 1.7.0.19-2.3.9.13.el7
- javadoc put into fully versioned directory, but without arch (to be kept noarch)
 - uniquejavadocdir
- updated to latest 2.3.9 tarball - fixing the rhbz#967436

* Mon May 27 2013 Omair Majid <omajid@redhat.com> - 1.7.0.19-2.3.9.12.el7
- Allowed multiple OpenJDKs to be installed in parallel
- Removed archname
- Added arch to all, not only multilib arches
- uniquesuffix is now holding fully versioned name
- Intorduced source11 remove-buildids.sh

* Fri May 17 2013 Omair Majid <omajid@redhat.com> - 1.7.0.19-2.3.9.12.el7
- Replace %%{name} with %%{uniquesuffix} where it's used as a unique suffix.

* Thu May 16 2013 Jiri Vanek <jvanek@redhat.com>
- added variable arm_arches as restriction to some cases of not jit_arches

* Tue May 14 2013 Jiri Vanek <jvanek@redhat.com>
- patch402 gstackbounds.patch applied only to jit arches
- patch403 PStack-808293.patch likewise

* Mon May 13 2013 Jiri Vanek <jvanek@redhat.com>
- initial, not buildable, sync with f19
