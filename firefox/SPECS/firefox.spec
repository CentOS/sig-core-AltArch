# Use system nspr/nss? FIXME
%global system_nss        1
%define use_bundled_ffi   0

# Don't use system hunspell for now
%global system_hunspell   0
%global system_sqlite     0

%if 0%{?rhel} > 6
%global system_ffi        1
%else
%global system_ffi        0
%endif
%if 0%{?rhel} < 8
%global use_dts           1
%endif

%global use_rustts        1
%global dts_version       7
%global rst_version       7

# Use system cairo?
%global system_cairo      0

# Use system libvpx?
%global system_libvpx     0

# Use system libicu?
%if 0%{?fedora} > 27
%global system_libicu     0
%else
%global system_libicu     0
%endif

# Big endian platforms
%ifarch ppc64 s390x
# Javascript Intl API is not supported on big endian platforms right now:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1322212
%global big_endian        1
%endif

# Hardened build?
%global hardened_build    1

%global system_jpeg       1

%ifarch %{ix86} x86_64
%global run_tests         0
%else
%global run_tests         0
%endif

# Build as a debug package?
%global debug_build       0

%global default_bookmarks_file  %{_datadir}/bookmarks/default-bookmarks.html
%global firefox_app_id  \{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}
# Minimal required versions
%global cairo_version 1.13.1
%global freetype_version 2.1.9
%if %{?system_libvpx}
%global libvpx_version 1.4.0
%endif

%if %{?system_nss}
%global nspr_version 4.19.0
# NSS/NSPR quite often ends in build override, so as requirement the version
# we're building against could bring us some broken dependencies from time to time.
#%global nspr_build_version %(pkg-config --silence-errors --modversion nspr 2>/dev/null || echo 65536)
%global nspr_build_version %{nspr_version}
%global nss_version 3.36.0
#%global nss_build_version %(pkg-config --silence-errors --modversion nss 2>/dev/null || echo 65536)
%global nss_build_version %{nss_version}
%endif

%if %{?system_sqlite}
%global sqlite_version 3.8.4.2
# The actual sqlite version (see #480989):
%global sqlite_build_version %(pkg-config --silence-errors --modversion sqlite3 2>/dev/null || echo 65536)
%endif

%define bundled_python_version 2.7.13
%define use_bundled_yasm        1

# GTK3 bundling
%define avoid_bundled_rebuild 0
%if 0%{?rhel} == 6
%define bundle_gtk3             1
# In-tree libffi is able to build on following platforms, we have to bundle it for the rest
%ifnarch x86_64 i686 aarch64
%define use_bundled_ffi         1
%endif
%endif

%define gtk3_nvr 3.22.26-1
%define gtk3_install_path %{mozappdir}/bundled

%if 0%{?bundle_gtk3}
# We could use %%include, but in %%files, %%post and other sections, but in these
# sections it could lead to syntax errors about unclosed %%if. Work around it by
# using the following macro
%define include_file() %{expand:%(cat '%1')}
%endif


%global mozappdir     %{_libdir}/%{name}
%global mozappdirdev  %{_libdir}/%{name}-devel-%{version}
%global langpackdir   %{mozappdir}/distribution/extensions
%global tarballdir    %{name}-%{version}
%global pre_version   esr

%global official_branding       1
%global build_langpacks         1

%global enable_mozilla_crashreporter       0
%if !%{debug_build}
%ifarch %{ix86} x86_64
%global enable_mozilla_crashreporter       0
%endif
%endif

Summary:        Mozilla Firefox Web browser
Name:           firefox
Version:        60.1.0
Release:        4%{?pre_tag}%{?dist}
URL:            https://www.mozilla.org/firefox/
License:        MPLv1.1 or GPLv2+ or LGPLv2+
%if 0%{?rhel} == 7
ExcludeArch:    s390 ppc
%endif
%if 0%{?rhel} == 6
ExclusiveArch:  i686 x86_64 ppc64 s390x
%endif

Source0:        https://hg.mozilla.org/releases/mozilla-release/archive/firefox-%{version}%{?pre_version}.source.tar.xz
%if %{build_langpacks}
Source1:        firefox-langpacks-%{version}%{?pre_version}-20180622.tar.xz
%endif
Source10:       firefox-mozconfig
Source12:       firefox-centos-default-prefs.js
Source20:       firefox.desktop
Source21:       firefox.sh.in
Source23:       firefox.1
Source24:       mozilla-api-key
Source25:       firefox-symbolic.svg
Source26:       distribution.ini
Source27:       google-api-key

Source200:      gtk3-private-%{gtk3_nvr}.el6.src.rpm
Source201:      gtk3-private-%{gtk3_nvr}-post.inc
Source202:      gtk3-private-%{gtk3_nvr}-postun.inc
Source203:      gtk3-private-%{gtk3_nvr}-posttrans.inc
Source204:      gtk3-private-%{gtk3_nvr}-files.inc
Source205:      gtk3-private-%{gtk3_nvr}-setup-flags-env.inc
Source206:      gtk3-private-%{gtk3_nvr}-requires-provides-filter.inc
Source301:      yasm-1.2.0-3.el5.src.rpm
Source303:      libffi-3.0.13-18.el7_3.src.rpm

#Python 2.7
Source100:      https://www.python.org/ftp/python/%{bundled_python_version}/Python-%{bundled_python_version}.tar.xz
# Build patches
Patch3:         mozilla-build-arm.patch
Patch4:         build-mozconfig-fix.patch
Patch5:         build-gdk-version.patch
Patch6:         build-nss-version.patch
Patch26:        build-icu-big-endian.patch
# Also fixes s390x: https://bugzilla.mozilla.org/show_bug.cgi?id=1376268
Patch29:        build-big-endian.patch
# Always feel lucky for unsupported platforms:
# https://bugzilla.mozilla.org/show_bug.cgi?id=1347128
Patch37:        build-jit-atomic-always-lucky.patch
Patch40:        build-aarch64-skia.patch
Patch41:        build-debug-qcms.patch
Patch43:        xulrunner-24.0-jemalloc-ppc.patch
Patch44:        firefox-disable-dbus-remote.patch

# Fedora/RHEL specific patches
Patch215:        firefox-enable-addons.patch
Patch219:        rhbz-1173156.patch
Patch221:        firefox-fedora-ua.patch
Patch224:        mozilla-1170092.patch
Patch225:        mozilla-1005640-accept-lang.patch
#ARM run-time patch
Patch226:        rhbz-1354671.patch
Patch230:        rhbz-1503632-nss.patch

# Upstream patches
Patch402:        mozilla-1196777.patch
Patch406:        mozilla-256180.patch
Patch413:        mozilla-1353817.patch
Patch415:        mozilla-1436242.patch

# Debian patches

%if %{?system_nss}
BuildRequires:  pkgconfig(nspr) >= %{nspr_version}
BuildRequires:  pkgconfig(nss) >= %{nss_version}
BuildRequires:  nss-static >= %{nss_version}
%endif
%if %{?system_cairo}
BuildRequires:  pkgconfig(cairo) >= %{cairo_version}
%endif
BuildRequires:  pkgconfig(libpng)
BuildRequires:  xz
BuildRequires:  libXt-devel
BuildRequires:  mesa-libGL-devel
Requires:       liberation-fonts-common
Requires:       liberation-sans-fonts
%if %{?system_jpeg}
BuildRequires:  libjpeg-devel
%endif
BuildRequires:  zip
BuildRequires:  bzip2-devel
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(libIDL-2.0)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  krb5-devel
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(freetype2) >= %{freetype_version}
BuildRequires:  pkgconfig(xt)
BuildRequires:  pkgconfig(xrender)
%if %{?system_hunspell}
BuildRequires:  hunspell-devel
%endif
BuildRequires:  pkgconfig(libstartup-notification-1.0)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(dri)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  dbus-glib-devel
%if %{?system_libvpx}
BuildRequires:  libvpx-devel >= %{libvpx_version}
%endif
BuildRequires:  autoconf213
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(gconf-2.0)

%if 0%{?use_dts}
BuildRequires:  devtoolset-%{dts_version}-gcc-c++
BuildRequires:  devtoolset-%{dts_version}-gcc
BuildRequires:  devtoolset-%{dts_version}-binutils
BuildRequires:  devtoolset-%{dts_version}-libatomic-devel
%if 0%{?rhel} > 6
BuildRequires:  llvm-toolset-%{dts_version}
BuildRequires:  llvm-toolset-%{dts_version}-llvm-devel
%endif
%endif
%if 0%{?use_rustts}
BuildRequires:  rust-toolset-%{rst_version}-cargo
BuildRequires:  rust-toolset-%{rst_version}-rust
%endif
%if 0%{?rhel} == 8
BuildRequires:  llvm-toolset-%{dts_version}
BuildRequires:  llvm-toolset-%{dts_version}-llvm-devel
%endif
%if 0%{?rhel} == 6
# Needed for Python in RHEL6
BuildRequires:  openssl-devel
%endif

%if 0%{?bundle_gtk3}
BuildRequires:        automake
BuildRequires:        autoconf
BuildRequires:        cups-devel
BuildRequires:        dbus-devel
BuildRequires:        desktop-file-utils
BuildRequires:        expat-devel
BuildRequires:        fontpackages-devel
BuildRequires:        gamin-devel
BuildRequires:        gettext-devel
BuildRequires:        git
BuildRequires:        intltool
BuildRequires:        jasper-devel
BuildRequires:        libepoxy-devel
BuildRequires:        libcroco-devel
BuildRequires:        libffi-devel
BuildRequires:        libpng-devel
BuildRequires:        libtiff-devel
BuildRequires:        libtool
BuildRequires:        libxml2-devel
BuildRequires:        libX11-devel
BuildRequires:        libXcomposite-devel
BuildRequires:        libXcursor-devel
BuildRequires:        libXinerama-devel
BuildRequires:        libXevie-devel
BuildRequires:        libXrandr-devel
BuildRequires:        libXrender-devel
BuildRequires:        libXtst-devel
BuildRequires:        mesa-libGL-devel
BuildRequires:        mesa-libEGL-devel
BuildRequires:        pixman-devel
BuildRequires:        rest-devel
BuildRequires:        readline-devel
%else
BuildRequires:        gtk3-devel
BuildRequires:        glib2-devel
%endif

Requires:       mozilla-filesystem
Requires:       p11-kit-trust
%if %{?system_nss}
Requires:       nspr >= %{nspr_build_version}
Requires:       nss >= %{nss_build_version}
%endif
BuildRequires:  python2-devel

%if 0%{?fedora} > 25
# For early testing of rhbz#1400293 mozbz#1324096 on F26 and Rawhide,
# temporarily require the specific NSS build with the backports.
# Can be removed after firefox is changed to require NSS 3.30.
BuildRequires:  nss-devel >= 3.29.1-2.1
Requires:       nss >= 3.29.1-2.1
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  system-bookmarks
Requires:       redhat-indexhtml
%if %{?system_sqlite}
BuildRequires:  pkgconfig(sqlite3) >= %{sqlite_version}
Requires:       sqlite >= %{sqlite_build_version}
%endif


%if %{?run_tests}
BuildRequires:  xorg-x11-server-Xvfb
%endif

%if %{?system_ffi}
  %if !%{use_bundled_ffi}0
BuildRequires:  pkgconfig(libffi)
  %endif
%endif

Obsoletes:      mozilla <= 37:1.7.13
Provides:       webclient

%description
Mozilla Firefox is an open-source web browser, designed for standards
compliance, performance and portability.

%if %{enable_mozilla_crashreporter}
%global moz_debug_prefix %{_prefix}/lib/debug
%global moz_debug_dir %{moz_debug_prefix}%{mozappdir}
%global uname_m %(uname -m)
%global symbols_file_name %{name}-%{version}.en-US.%{_os}-%{uname_m}.crashreporter-symbols.zip
%global symbols_file_path %{moz_debug_dir}/%{symbols_file_name}
%global _find_debuginfo_opts -p %{symbols_file_path} -o debugcrashreporter.list
%global crashreporter_pkg_name mozilla-crashreporter-%{name}-debuginfo
%package -n %{crashreporter_pkg_name}
Summary: Debugging symbols used by Mozilla's crash reporter servers
%description -n %{crashreporter_pkg_name}
This package provides debug information for Firefox, for use by
Mozilla's crash reporter servers.  If you are trying to locally
debug %{name}, you want to install %{name}-debuginfo instead.
%files -n %{crashreporter_pkg_name} -f debugcrashreporter.list
%endif

%if %{run_tests}
%global testsuite_pkg_name mozilla-%{name}-testresults
%package -n %{testsuite_pkg_name}
Summary: Results of testsuite
%description -n %{testsuite_pkg_name}
This package contains results of tests executed during build.
%files -n %{testsuite_pkg_name}
/test_results
%endif

#---------------------------------------------------------------------

%prep
%setup -q -T -c -n python -a 100
%setup -q -n %{tarballdir}
# Build patches, can't change backup suffix from default because during build
# there is a compare of config and js/config directories and .orig suffix is
# ignored during this compare.

%patch29 -p1 -b .big-endian
%patch37 -p1 -b .jit-atomic-lucky
%patch40 -p1 -b .aarch64-skia
%if %{?debug_build}
%patch41 -p1 -b .build-debug-qcms
%endif
%patch43 -p1 -b .jemalloc-ppc
# Disable DBus remote on RHEL6 as it does not build here.
%if 0%{?rhel} == 6
%patch44 -p1 -b .disable-dbus-remote
%endif

%patch3  -p1 -b .arm
%patch4  -p1 -b .build-mozconfig-fix
%patch5  -p1 -b .gdk-version
%patch6  -p1 -b .nss-version

# Fedora patches
%patch215 -p1 -b .addons
%patch219 -p2 -b .rhbz-1173156
%patch221 -p2 -b .fedora-ua
%patch224 -p1 -b .1170092
%patch225 -p1 -b .1005640-accept-lang

# This ensures no migration of certdb to sqlite on the RHEL6 and RHEL7.
# This needs to stay for the future releases
%if 0%{?rhel} < 8
%patch230 -p1 -b .1503632-nss
%endif

#ARM run-time patch
%ifarch aarch64
%patch226 -p1 -b .1354671
%endif

%patch402 -p1 -b .1196777
%patch406 -p1 -b .256180
%patch413 -p1 -b .1353817
%patch415 -p1 -b .1436242

# Patch for big endian platforms only
%if 0%{?big_endian}
%patch26 -p1 -b .icu
%endif

%{__rm} -f .mozconfig
%{__cp} %{SOURCE10} .mozconfig
%if %{official_branding}
echo "ac_add_options --enable-official-branding" >> .mozconfig
%endif
%{__cp} %{SOURCE24} mozilla-api-key
%{__cp} %{SOURCE27} google-api-key

%if %{?system_nss}
echo "ac_add_options --with-system-nspr" >> .mozconfig
echo "ac_add_options --with-system-nss" >> .mozconfig
%else
echo "ac_add_options --without-system-nspr" >> .mozconfig
echo "ac_add_options --without-system-nss" >> .mozconfig
%endif

%if %{?system_sqlite}
echo "ac_add_options --enable-system-sqlite" >> .mozconfig
%else
echo "ac_add_options --disable-system-sqlite" >> .mozconfig
%endif

%if %{?system_cairo}
echo "ac_add_options --enable-system-cairo" >> .mozconfig
%else
echo "ac_add_options --disable-system-cairo" >> .mozconfig
%endif

%if 0%{?use_bundled_ffi}
echo "ac_add_options --enable-system-ffi" >> .mozconfig
%endif
%if 0%{?system_ffi}
echo "ac_add_options --enable-system-ffi" >> .mozconfig
%endif

%ifarch %{arm}
echo "ac_add_options --disable-elf-hack" >> .mozconfig
%endif

%if %{?system_hunspell}
echo "ac_add_options --enable-system-hunspell" >> .mozconfig
%else
echo "ac_add_options --disable-system-hunspell" >> .mozconfig
%endif

%if %{?debug_build}
echo "ac_add_options --enable-debug" >> .mozconfig
echo "ac_add_options --disable-optimize" >> .mozconfig
%else
%global optimize_flags "none"
# Fedora 26 (gcc7) needs to disable default build flags (mozbz#1342344)
%if 0%{?fedora} > 25
%ifnarch s390 s390x
%global optimize_flags "-g -O2"
%endif
%endif
%ifarch armv7hl
# ARMv7 need that (rhbz#1426850)
%global optimize_flags "-g -O2 -fno-schedule-insns"
%endif
%ifarch ppc64le aarch64
%global optimize_flags "-g -O2"
%endif
%if %{optimize_flags} != "none"
echo 'ac_add_options --enable-optimize=%{?optimize_flags}' >> .mozconfig
%else
echo 'ac_add_options --enable-optimize' >> .mozconfig
%endif
echo "ac_add_options --disable-debug" >> .mozconfig
%endif

# Second arches fail to start with jemalloc enabled
%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-jemalloc" >> .mozconfig
%endif

%ifnarch %{ix86} x86_64
echo "ac_add_options --disable-webrtc" >> .mozconfig
%endif

%if !%{enable_mozilla_crashreporter}
echo "ac_add_options --disable-crashreporter" >> .mozconfig
%endif

%if %{?run_tests}
echo "ac_add_options --enable-tests" >> .mozconfig
%endif

%if !%{?system_jpeg}
echo "ac_add_options --without-system-jpeg" >> .mozconfig
%else
echo "ac_add_options --with-system-jpeg" >> .mozconfig
%endif

%if %{?system_libvpx}
echo "ac_add_options --with-system-libvpx" >> .mozconfig
%else
echo "ac_add_options --without-system-libvpx" >> .mozconfig
%endif

%if %{?system_libicu}
echo "ac_add_options --with-system-icu" >> .mozconfig
%else
echo "ac_add_options --without-system-icu" >> .mozconfig
%endif
%ifarch s390 s390x
echo "ac_add_options --disable-ion" >> .mozconfig
%endif

%ifarch %{ix86}
echo "ac_add_options --disable-stylo" >> .mozconfig
%endif
%if 0%{?rhel} == 6
echo "ac_add_options --disable-stylo" >> .mozconfig
%endif

# Remove executable bit to make brp-mangle-shebangs happy.
chmod -x third_party/rust/itertools/src/lib.rs

#---------------------------------------------------------------------

%build

#GTK3 >>
%if ! 0%{?avoid_bundled_rebuild}
    rm -rf %{_buildrootdir}/*
%endif
export PATH="%{_buildrootdir}/bin:$PATH"

function install_rpms_to_current_dir() {
    PACKAGE_RPM=$(eval echo $1)
    PACKAGE_DIR=%{_rpmdir}

    if [ ! -f $PACKAGE_DIR/$PACKAGE_RPM ]; then
        # Hack for tps tests
        ARCH_STR=%{_arch}
        %ifarch i386 i686
            ARCH_STR="i?86"
        %endif
        PACKAGE_DIR="$PACKAGE_DIR/$ARCH_STR"
     fi

     for package in $(ls $PACKAGE_DIR/$PACKAGE_RPM)
     do
         echo "$package"
         rpm2cpio "$package" | cpio -idu
     done
}

function build_bundled_package() {
  PACKAGE_RPM=$1
  PACKAGE_FILES=$2
  PACKAGE_SOURCE=$3
  PACKAGE_DIR="%{_topdir}/RPMS"

  PACKAGE_ALREADY_BUILD=0
  %if %{?avoid_bundled_rebuild}
    if ls $PACKAGE_DIR/$PACKAGE_RPM; then
      PACKAGE_ALREADY_BUILD=1
    fi
    if ls $PACKAGE_DIR/%{_arch}/$PACKAGE_RPM; then
      PACKAGE_ALREADY_BUILD=1
    fi
  %endif
  if [ $PACKAGE_ALREADY_BUILD == 0 ]; then
    echo "Rebuilding $PACKAGE_RPM from $PACKAGE_SOURCE"; echo "==============================="
    rpmbuild --nodeps --rebuild $PACKAGE_SOURCE
  fi

  if [ ! -f $PACKAGE_DIR/$PACKAGE_RPM ]; then
    # Hack for tps tests
    ARCH_STR=%{_arch}
    %ifarch i386 i686
    ARCH_STR="i?86"
    %endif
    PACKAGE_DIR="$PACKAGE_DIR/$ARCH_STR"
  fi
  pushd $PACKAGE_DIR
  echo "Installing $PACKAGE_DIR/$PACKAGE_RPM"; echo "==============================="
  rpm2cpio $PACKAGE_DIR/$PACKAGE_RPM | cpio -iduv
  # Clean rpms to avoid including them to package
  %if ! 0%{?avoid_bundled_rebuild}
    rm -f $PACKAGE_FILES
  %endif

  PATH=$PACKAGE_DIR/usr/bin:$PATH
  export PATH
  LD_LIBRARY_PATH=$PACKAGE_DIR/usr/%{_lib}
  export LD_LIBRARY_PATH
  popd
}

# Build and install local yasm if needed
# ======================================
%if %{use_bundled_yasm}
  build_bundled_package 'yasm-1*.rpm' 'yasm-*.rpm' '%{SOURCE301}'
%endif


%if 0%{?bundle_gtk3}
   %if ! 0%{?avoid_bundled_rebuild}
    rpm -ivh %{SOURCE200}
    rpmbuild --nodeps --define '_prefix %{gtk3_install_path}' -ba %{_specdir}/gtk3-private.spec
   %endif
   rm -rf %{_buildrootdir}/*
   pushd %{_buildrootdir}
   install_rpms_to_current_dir gtk3-private-%{gtk3_nvr}*.rpm
   install_rpms_to_current_dir gtk3-private-devel-%{gtk3_nvr}*.rpm
   install_rpms_to_current_dir gtk3-private-rpm-scripts-%{gtk3_nvr}*.rpm
   popd
%endif

# If needed build the bundled python 2.7 and put it in the PATH
if [ $(python --version 2>&1 | awk '{ print substr ($2, 0, 3) }') = "2.6" ]; then
    pushd %{_builddir}/python/Python-%{bundled_python_version}
    #if ! 0%{?avoid_bundled_rebuild}
        # Build Python 2.7 and set environment
        ./configure --prefix="%{_buildrootdir}" --exec-prefix="%{_buildrootdir}" --libdir="%{_buildrootdir}/lib"
    #endif
    make %{?_smp_mflags} install V=1
    popd
fi

%if 0%{?bundle_gtk3}
# gtk3-private-3.22.26.el6-1-requires-provides-filter.inc
%include_file %{SOURCE206}
%endif
%if 0%{use_bundled_ffi}
  # Install libraries to the predefined location to later add them to the Firefox libraries
  rpm -ivh %{SOURCE303}
  rpmbuild --nodeps --define '_prefix %{gtk3_install_path}' -ba %{_specdir}/libffi.spec
  pushd %{_buildrootdir}
  install_rpms_to_current_dir 'libffi*.rpm'
  popd
  %filter_from_requires /libffi.so.6/d
%endif
%filter_setup

# GTK3 <<

%if %{?system_sqlite}
# Do not proceed with build if the sqlite require would be broken:
# make sure the minimum requirement is non-empty, ...
sqlite_version=$(expr "%{sqlite_version}" : '\([0-9]*\.\)[0-9]*\.') || exit 1
# ... and that major number of the computed build-time version matches:
case "%{sqlite_build_version}" in
  "$sqlite_version"*) ;;
  *) exit 1 ;;
esac
%endif

# We need to disable exit on error temporarily for the following scripts:
set +e
%if 0%{?use_dts}
source scl_source enable devtoolset-%{dts_version}
%endif
%if 0%{?use_rustts}
source scl_source enable rust-toolset-%{rst_version}
%endif

set -e
# Hack for missing shell when building in brew on RHEL6
%if 0%{?rhel} == 6
export SHELL=/bin/sh
%endif

echo "Generate big endian version of config/external/icu/data/icud58l.dat"
%if 0%{?big_endian}
  ./mach python intl/icu_sources_data.py .
  ls -l config/external/icu/data
  rm -f config/external/icu/data/icudt*l.dat
%endif

# Update the various config.guess to upstream release for aarch64 support
find ./ -name config.guess -exec cp /usr/lib/rpm/config.guess {} ';'

# -fpermissive is needed to build with gcc 4.6+ which has become stricter
#
# Mozilla builds with -Wall with exception of a few warnings which show up
# everywhere in the code; so, don't override that.
#
# Disable C++ exceptions since Mozilla code is not exception-safe
#
MOZ_OPT_FLAGS=$(echo "%{optflags}" | %{__sed} -e 's/-Wall//')
#rhbz#1037063
# -Werror=format-security causes build failures when -Wno-format is explicitly given
# for some sources
# Explicitly force the hardening flags for Firefox so it passes the checksec test;
# See also https://fedoraproject.org/wiki/Changes/Harden_All_Packages
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -Wformat-security -Wformat -Werror=format-security"
%if 0%{?fedora} > 23
# Disable null pointer gcc6 optimization in gcc6 (rhbz#1328045)
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fno-delete-null-pointer-checks"
%endif
# Use hardened build?
%if %{?hardened_build}
MOZ_OPT_FLAGS="$MOZ_OPT_FLAGS -fPIC -Wl,-z,relro -Wl,-z,now"
%endif
%if %{?debug_build}
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-O2//')
%endif
%ifarch s390
MOZ_OPT_FLAGS=$(echo "$MOZ_OPT_FLAGS" | %{__sed} -e 's/-g/-g1/')
# If MOZ_DEBUG_FLAGS is empty, firefox's build will default it to "-g" which
# overrides the -g1 from line above and breaks building on s390
# (OOM when linking, rhbz#1238225)
export MOZ_DEBUG_FLAGS=" "
%endif
%ifarch s390 %{arm} ppc aarch64 i686
MOZ_LINK_FLAGS="-Wl,--no-keep-memory -Wl,--reduce-memory-overheads"
%endif
%ifarch %{arm}
export RUSTFLAGS="-Cdebuginfo=0"
%endif
export CFLAGS=$MOZ_OPT_FLAGS
export CXXFLAGS=$MOZ_OPT_FLAGS
export LDFLAGS=$MOZ_LINK_FLAGS

export PREFIX='%{_prefix}'
export LIBDIR='%{_libdir}'

MOZ_SMP_FLAGS=-j1
# On x86 architectures, Mozilla can build up to 4 jobs at once in parallel,
# however builds tend to fail on other arches when building in parallel.
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le aarch64
[ -z "$RPM_BUILD_NCPUS" ] && \
     RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"
[ "$RPM_BUILD_NCPUS" -ge 2 ] && MOZ_SMP_FLAGS=-j2
[ "$RPM_BUILD_NCPUS" -ge 4 ] && MOZ_SMP_FLAGS=-j4
[ "$RPM_BUILD_NCPUS" -ge 8 ] && MOZ_SMP_FLAGS=-j8
%endif

%if 0%{?bundle_gtk3}
# gtk3-private-setup-flags-env.inc
%include_file %{SOURCE205}
%endif

#make -f client.mk build STRIP="/bin/true" MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS" MOZ_SERVICES_SYNC="1"
export MOZ_MAKE_FLAGS="$MOZ_SMP_FLAGS"
export MOZ_SERVICES_SYNC="1"
export STRIP=/bin/true
./mach build -v

# create debuginfo for crash-stats.mozilla.com
%if %{enable_mozilla_crashreporter}
#cd %{moz_objdir}
make -C objdir buildsymbols
%endif

%if %{?run_tests}
%if %{?system_nss}
ln -s /usr/bin/certutil objdir/dist/bin/certutil
ln -s /usr/bin/pk12util objdir/dist/bin/pk12util

%endif
mkdir test_results
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey || true
./mach --log-no-times check-spidermonkey &> test_results/check-spidermonkey-2nd-run || true
./mach --log-no-times cppunittest &> test_results/cppunittest || true
xvfb-run ./mach --log-no-times crashtest &> test_results/crashtest || true
./mach --log-no-times gtest &> test_results/gtest || true
xvfb-run ./mach --log-no-times jetpack-test &> test_results/jetpack-test || true
# not working right now ./mach marionette-test &> test_results/marionette-test || true
xvfb-run ./mach --log-no-times mochitest-a11y &> test_results/mochitest-a11y || true
xvfb-run ./mach --log-no-times mochitest-browser &> test_results/mochitest-browser || true
xvfb-run ./mach --log-no-times mochitest-chrome &> test_results/mochitest-chrome || true
xvfb-run ./mach --log-no-times mochitest-devtools &> test_results/mochitest-devtools || true
xvfb-run ./mach --log-no-times mochitest-plain &> test_results/mochitest-plain || true
xvfb-run ./mach --log-no-times reftest &> test_results/reftest || true
xvfb-run ./mach --log-no-times webapprt-test-chrome &> test_results/webapprt-test-chrome || true
xvfb-run ./mach --log-no-times webapprt-test-content &> test_results/webapprt-test-content || true
./mach --log-no-times webidl-parser-test &> test_results/webidl-parser-test || true
xvfb-run ./mach --log-no-times xpcshell-test &> test_results/xpcshell-test || true
%if %{?system_nss}
rm -f  objdir/dist/bin/certutil
rm -f  objdir/dist/bin/pk12util
%endif

%endif
#---------------------------------------------------------------------

%install
%if 0%{?rhel} == 6
export SHELL=/bin/sh
%endif

%if 0%{?bundle_gtk3}
function install_rpms_to_current_dir() {
    PACKAGE_RPM=$(eval echo $1)
    PACKAGE_DIR=%{_rpmdir}

    if [ ! -f $PACKAGE_DIR/$PACKAGE_RPM ]; then
        # Hack for tps tests
        ARCH_STR=%{_arch}
        %ifarch i386 i686
            ARCH_STR="i?86"
        %endif
        PACKAGE_DIR="$PACKAGE_DIR/$ARCH_STR"
     fi

     for package in $(ls $PACKAGE_DIR/$PACKAGE_RPM)
     do
         echo "$package"
         rpm2cpio "$package" | cpio -idu
     done
}

pushd %{buildroot}
# Install gtk3-private again to the buildroot, but without devel subpackage
install_rpms_to_current_dir gtk3-private-%{gtk3_nvr}*.rpm
install_rpms_to_current_dir gtk3-private-rpm-scripts-%{gtk3_nvr}*.rpm
popd
%endif

# Install bundled libffi
%if %{use_bundled_ffi}
  pushd %{buildroot}
  install_rpms_to_current_dir libffi-3*.rpm
  popd
%endif

# set up our default bookmarks
%{__cp} -p %{default_bookmarks_file} objdir/dist/bin/browser/chrome/en-US/locale/browser/bookmarks.html

# Make sure locale works for langpacks
%{__cat} > objdir/dist/bin/browser/defaults/preferences/firefox-l10n.js << EOF
pref("general.useragent.locale", "chrome://global/locale/intl.properties");
EOF

DESTDIR=%{buildroot} make -C objdir install

%{__mkdir_p} %{buildroot}{%{_libdir},%{_bindir},%{_datadir}/applications}

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE20}

# set up the firefox start script
%{__rm} -rf %{buildroot}%{_bindir}/firefox
%{__cat} %{SOURCE21} > %{buildroot}%{_bindir}/firefox
%{__chmod} 755 %{buildroot}%{_bindir}/firefox

%{__install} -p -D -m 644 %{SOURCE23} %{buildroot}%{_mandir}/man1/firefox.1

%{__rm} -f %{buildroot}/%{mozappdir}/firefox-config
%{__rm} -f %{buildroot}/%{mozappdir}/update-settings.ini

for s in 16 22 24 32 48 256; do
    %{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
    %{__cp} -p browser/branding/official/default${s}.png \
               %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/firefox.png
done

# Install hight contrast icon
%{__mkdir_p} %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps
%{__cp} -p %{SOURCE25} \
           %{buildroot}%{_datadir}/icons/hicolor/symbolic/apps

# Register as an application to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
%{__mkdir_p} %{buildroot}%{_datadir}/appdata
cat > %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2014 Richard Hughes <richard@hughsie.com> -->
<!--
BugReportURL: https://bugzilla.mozilla.org/show_bug.cgi?id=1071061
SentUpstream: 2014-09-22
-->
<application>
  <id type="desktop">firefox.desktop</id>
  <metadata_license>CC0-1.0</metadata_license>
  <description>
    <p>
      Bringing together all kinds of awesomeness to make browsing better for you.
      Get to your favorite sites quickly – even if you don’t remember the URLs.
      Type your term into the location bar (aka the Awesome Bar) and the autocomplete
      function will include possible matches from your browsing history, bookmarked
      sites and open tabs.
    </p>
    <!-- FIXME: Needs another couple of paragraphs -->
  </description>
  <url type="homepage">http://www.mozilla.org/</url>
  <screenshots>
    <screenshot type="default">https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/a.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/b.png</screenshot>
    <screenshot>https://raw.githubusercontent.com/hughsie/fedora-appstream/master/screenshots-extra/firefox/c.png</screenshot>
  </screenshots>
  <!-- FIXME: change this to an upstream email address for spec updates
  <updatecontact>someone_who_cares@upstream_project.org</updatecontact>
   -->
</application>
EOF

echo > %{name}.lang
%if %{build_langpacks}
# Extract langpacks, make any mods needed, repack the langpack, and install it.
%{__mkdir_p} %{buildroot}%{langpackdir}
%{__tar} xf %{SOURCE1}
for langpack in `ls firefox-langpacks/*.xpi`; do
  language=`basename $langpack .xpi`
  extensionID=langpack-$language@firefox.mozilla.org
  %{__mkdir_p} $extensionID
  unzip -qq $langpack -d $extensionID
  find $extensionID -type f | xargs chmod 644

  cd $extensionID
  zip -qq -r9mX ../${extensionID}.xpi *
  cd -

  %{__install} -m 644 ${extensionID}.xpi %{buildroot}%{langpackdir}
  language=`echo $language | sed -e 's/-/_/g'`
  echo "%%lang($language) %{langpackdir}/${extensionID}.xpi" >> %{name}.lang
done
%{__rm} -rf firefox-langpacks

# Install langpack workaround (see #707100, #821169)
function create_default_langpack() {
language_long=$1
language_short=$2
cd %{buildroot}%{langpackdir}
ln -s langpack-$language_long@firefox.mozilla.org.xpi langpack-$language_short@firefox.mozilla.org.xpi
cd -
echo "%%lang($language_short) %{langpackdir}/langpack-$language_short@firefox.mozilla.org.xpi" >> %{name}.lang
}

# Table of fallbacks for each language
# please file a bug at bugzilla.redhat.com if the assignment is incorrect
create_default_langpack "bn-IN" "bn"
create_default_langpack "es-AR" "es"
create_default_langpack "fy-NL" "fy"
create_default_langpack "ga-IE" "ga"
create_default_langpack "gu-IN" "gu"
create_default_langpack "hi-IN" "hi"
create_default_langpack "hy-AM" "hy"
create_default_langpack "nb-NO" "nb"
create_default_langpack "nn-NO" "nn"
create_default_langpack "pa-IN" "pa"
create_default_langpack "pt-PT" "pt"
create_default_langpack "sv-SE" "sv"
create_default_langpack "zh-TW" "zh"
%endif # build_langpacks

# Keep compatibility with the old preference location.
%{__mkdir_p} %{buildroot}%{mozappdir}/defaults/preferences
%{__mkdir_p} %{buildroot}%{mozappdir}/browser/defaults
ln -s %{mozappdir}/defaults/preferences $RPM_BUILD_ROOT/%{mozappdir}/browser/defaults/preferences
# Default preferences
%{__cp} %{SOURCE12} %{buildroot}%{mozappdir}/defaults/preferences/all-redhat.js

# System config dir
%{__mkdir_p} %{buildroot}/%{_sysconfdir}/%{name}/pref

# System extensions
%{__mkdir_p} %{buildroot}%{_datadir}/mozilla/extensions/%{firefox_app_id}
%{__mkdir_p} %{buildroot}%{_libdir}/mozilla/extensions/%{firefox_app_id}

# Copy over the LICENSE
%{__install} -p -c -m 644 LICENSE %{buildroot}/%{mozappdir}

# Use the system hunspell dictionaries
%{__rm} -rf %{buildroot}%{mozappdir}/dictionaries
ln -s %{_datadir}/myspell %{buildroot}%{mozappdir}/dictionaries

# Enable crash reporter for Firefox application
%if %{enable_mozilla_crashreporter}
sed -i -e "s/\[Crash Reporter\]/[Crash Reporter]\nEnabled=1/" %{buildroot}/%{mozappdir}/application.ini
# Add debuginfo for crash-stats.mozilla.com
%{__mkdir_p} %{buildroot}/%{moz_debug_dir}
%{__cp} objdir/dist/%{symbols_file_name} %{buildroot}/%{moz_debug_dir}
%endif

%if %{run_tests}
# Add debuginfo for crash-stats.mozilla.com
%{__mkdir_p} %{buildroot}/test_results
%{__cp} test_results/* %{buildroot}/test_results
%endif


# Copy over run-mozilla.sh
%{__cp} build/unix/run-mozilla.sh %{buildroot}%{mozappdir}

# Add distribution.ini
%{__mkdir_p} %{buildroot}%{mozappdir}/distribution
%{__cp} %{SOURCE26} %{buildroot}%{mozappdir}/distribution

# Remove copied libraries to speed up build
rm -f %{buildroot}%{mozappdirdev}/sdk/lib/libmozjs.so
rm -f %{buildroot}%{mozappdirdev}/sdk/lib/libmozalloc.so
rm -f %{buildroot}%{mozappdirdev}/sdk/lib/libxul.so
#---------------------------------------------------------------------



%preun
# is it a final removal?
if [ $1 -eq 0 ]; then
  %{__rm} -rf %{mozappdir}/components
  %{__rm} -rf %{mozappdir}/extensions
  %{__rm} -rf %{mozappdir}/plugins
  %{__rm} -rf %{langpackdir}
fi

%clean
rm -rf %{_srcrpmdir}/gtk3-private-%{gtk3_nvr}*.src.rpm
find %{_rpmdir} -name "gtk3-private-*%{gtk3_nvr}*.rpm" -delete
rm -rf %{_srcrpmdir}/libffi*.src.rpm
find %{_rpmdir} -name "libffi*.rpm" -delete

%post
update-desktop-database &> /dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
%if 0%{?bundle_gtk3}
# gtk3-private-post.inc
%include_file %{SOURCE201}
%endif

%postun
update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
%if 0%{?bundle_gtk3}
# gtk3-private-postun.inc
%include_file %{SOURCE202}
%endif

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
%if 0%{?bundle_gtk3}
# gtk3-private-posttrans.inc
%include_file %{SOURCE203}
%endif

%files -f %{name}.lang
%{_bindir}/firefox
%{mozappdir}/firefox
%{mozappdir}/firefox-bin
%doc %{_mandir}/man1/*
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/*
%dir %{_datadir}/mozilla/extensions/*
%dir %{_libdir}/mozilla/extensions/*
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/*.desktop
%dir %{mozappdir}
%doc %{mozappdir}/LICENSE
%{mozappdir}/browser/chrome
%{mozappdir}/browser/chrome.manifest
%{mozappdir}/defaults/preferences/*
%{mozappdir}/browser/defaults/preferences
%{mozappdir}/browser/features/*.xpi
%{mozappdir}/distribution/distribution.ini
# That's Windows only
%ghost %{mozappdir}/browser/features/aushelper@mozilla.org.xpi
%attr(644, root, root) %{mozappdir}/browser/blocklist.xml
%dir %{mozappdir}/browser/extensions
%{mozappdir}/browser/extensions/*
%if %{build_langpacks}
%dir %{langpackdir}
%endif
%{mozappdir}/browser/omni.ja
%{mozappdir}/chrome.manifest
%{mozappdir}/run-mozilla.sh
%{mozappdir}/application.ini
%{mozappdir}/pingsender
%exclude %{mozappdir}/removed-files
%{_datadir}/icons/hicolor/16x16/apps/firefox.png
%{_datadir}/icons/hicolor/22x22/apps/firefox.png
%{_datadir}/icons/hicolor/24x24/apps/firefox.png
%{_datadir}/icons/hicolor/256x256/apps/firefox.png
%{_datadir}/icons/hicolor/32x32/apps/firefox.png
%{_datadir}/icons/hicolor/48x48/apps/firefox.png
%{_datadir}/icons/hicolor/symbolic/apps/firefox-symbolic.svg
%if %{enable_mozilla_crashreporter}
%{mozappdir}/crashreporter
%{mozappdir}/crashreporter.ini
%{mozappdir}/minidump-analyzer
%{mozappdir}/Throbber-small.gif
%{mozappdir}/browser/crashreporter-override.ini
%endif
%{mozappdir}/*.so
%{mozappdir}/gtk2/*.so
%{mozappdir}/defaults/pref/channel-prefs.js
%{mozappdir}/dependentlibs.list
%{mozappdir}/dictionaries
%{mozappdir}/omni.ja
%{mozappdir}/platform.ini
%{mozappdir}/plugin-container
%{mozappdir}/gmp-clearkey
%{mozappdir}/fonts/EmojiOneMozilla.ttf
%if !%{?system_libicu}
#%{mozappdir}/icudt*.dat
%endif
%if !%{?system_nss}
%{mozappdir}/libfreeblpriv3.chk
%{mozappdir}/libnssdbm3.chk
%{mozappdir}/libsoftokn3.chk
%exclude %{mozappdir}/libnssckbi.so
%endif
%if 0%{use_bundled_ffi}
%{mozappdir}/bundled/%{_lib}/libffi.so*
%exclude %{_datadir}/doc/libffi*
%endif

%if 0%{?bundle_gtk3}
# gtk3-private-files.inc
%include_file %{SOURCE204}
%endif


#---------------------------------------------------------------------

%changelog
* Tue Jul 10 2018 Johnny Hughes <johnny@centos.org> - 60.1.0-4
- Manual CentOS Branding

* Sun Jun 24 2018 Martin Stransky <stransky@redhat.com> - 60.1.0-4
- Disabled jemalloc on all second arches

* Fri Jun 22 2018 Martin Stransky <stransky@redhat.com> - 60.1.0-3
- Updated to 60.1.0 ESR build2

* Thu Jun 21 2018 Martin Stransky <stransky@redhat.com> - 60.1.0-2
- Disabled jemalloc on second arches

* Wed Jun 20 2018 Martin Stransky <stransky@redhat.com> - 60.1.0-1
- Updated to 60.1.0 ESR

* Wed Jun 13 2018 Jan Horak <jhorak@redhat.com> - 60.0-12
- Fixing bundled libffi issues
- Readded some requirements

* Mon Jun 11 2018 Martin Stransky <stransky@redhat.com> - 60.0-10
- Added fix for mozilla BZ#1436242 - IPC crashes.

* Mon Jun 11 2018 Jan Horak <jhorak@redhat.com> - 60.0-9
- Bundling libffi for the sec-arches
- Added openssl-devel for the Python
- Fixing bundled gtk3

* Fri May 18 2018 Martin Stransky <stransky@redhat.com> - 60.0-8
- Added fix for mozilla BZ#1458492

* Wed May 16 2018 Martin Stransky <stransky@redhat.com> - 60.0-7
- Added patch from rhbz#1498561 to fix ppc64(le) crashes.

* Wed May 16 2018 Martin Stransky <stransky@redhat.com> - 60.0-6
- Disabled jemalloc on second arches

* Sun May  6 2018 Jan Horak <jhorak@redhat.com> - 60.0-4
- Update to 60.0 ESR

* Thu Mar  8 2018 Jan Horak <jhorak@redhat.com> - 52.7.0-1
- Update to 52.7.0 ESR

* Mon Jan 29 2018 Martin Stransky <stransky@redhat.com> - 52.6.0-2
- Build Firefox for desktop arches only (x86_64 and ppc64le)

* Thu Jan 18 2018 Martin Stransky <stransky@redhat.com> - 52.6.0-1
- Update to 52.6.0 ESR

* Thu Nov  9 2017 Jan Horak <jhorak@redhat.com> - 52.5.0-1
- Update to 52.5.0 ESR

* Mon Sep 25 2017 Jan Horak <jhorak@redhat.com> - 52.4.0-1
- Update to 52.4.0 ESR

* Thu Aug  3 2017 Jan Horak <jhorak@redhat.com> - 52.3.0-3
- Update to 52.3.0 ESR (b2)
- Require correct nss version

* Tue Jun 13 2017 Jan Horak <jhorak@redhat.com> - 52.2.0-1
- Update to 52.2.0 ESR

* Wed May 24 2017 Jan Horak <jhorak@redhat.com> - 52.1.2-1
- Update to 52.1.2 ESR

* Wed May 24 2017 Jan Horak <jhorak@redhat.com> - 52.0-7
- Added fix for accept language (rhbz#1454322)

* Wed Mar 22 2017 Jan Horak <jhorak@redhat.com> - 52.0-6
- Removing patch required for older NSS from RHEL 7.3
- Added patch for rhbz#1414564

* Fri Mar 17 2017 Martin Stransky <stransky@redhat.com> - 52.0-5
- Added fix for mozbz#1348168/CVE-2017-5428

* Mon Mar  6 2017 Jan Horak <jhorak@redhat.com> - 52.0-4
- Update to 52.0 ESR (b4)

* Thu Mar 2 2017 Martin Stransky <stransky@redhat.com> - 52.0-3
- Added fix for rhbz#1423012 - ppc64 gfx crashes

* Wed Mar  1 2017 Jan Horak <jhorak@redhat.com> - 52.0-2
- Enable system nss

* Tue Feb 28 2017 Martin Stransky <stransky@redhat.com> - 52.0-1
- Update to 52.0ESR (B1)
- Build RHEL7 package for Gtk3

* Mon Feb 27 2017 Martin Stransky <stransky@redhat.com> - 52.0-0.13
- Added fix for rhbz#1414535

* Tue Feb 21 2017 Jan Horak <jhorak@redhat.com> - 52.0-0.12
- Update to 52.0b8

* Tue Feb  7 2017 Jan Horak <jhorak@redhat.com> - 52.0-0.11
- Readded addons patch

* Mon Feb  6 2017 Jan Horak <jhorak@redhat.com> - 52.0-0.10
- Update to 52.0b3

* Tue Jan 31 2017 Jan Horak <jhorak@redhat.com> - 52.0-0.9
- Update to 52.0b2

* Fri Jan 27 2017 Jan Horak <jhorak@redhat.com> - 52.0-0.8
- Update to 52.0b1

* Thu Dec  8 2016 Jan Horak <jhorak@redhat.com> - 52.0-0.5
- Firefox Aurora 52 testing build

