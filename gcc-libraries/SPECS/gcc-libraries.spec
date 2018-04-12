%global DATE 20170829
%global SVNREV 251415
%global gcc_version 7.2.1
%global gcc_major 7
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 1
%global mpc_version 0.8.1
%global _unpackaged_files_terminate_build 0
%global multilib_64_archs sparc64 ppc64 s390x x86_64
%ifarch s390x
%global multilib_32_arch s390
%endif
%ifarch sparc64
%global multilib_32_arch sparcv9
%endif
%ifarch ppc64
%global multilib_32_arch ppc
%endif
%ifarch x86_64
%global multilib_32_arch i686
%endif
%ifarch %{ix86} x86_64 ia64
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%ifarch %{ix86} x86_64
%global build_libcilkrts 1
%else
%global build_libcilkrts 0
%endif
%ifarch aarch64
%if 0%{?rhel} >= 7
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%endif
%ifnarch aarch64
%if 0%{?rhel} >= 7
%global build_libatomic 0
%else
%global build_libatomic 1
%endif
%endif
%if 0%{?rhel} >= 7
%global build_libitm 0
%else
%global build_libitm 1
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64 %{mips}
%global attr_ifunc 1
%else
%global attr_ifunc 0
%endif
Summary: GCC runtime libraries
Name: gcc-libraries
Provides: libatomic libitm libcilkrts libgfortran4
Obsoletes: libitm

Version: %{gcc_version}
Release: %{gcc_release}.1.1%{?dist}
# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: System Environment/Libraries
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-7-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
Source1: http://www.multiprecision.org/mpc/download/mpc-%{mpc_version}.tar.gz
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# Need binutils with -pie support >= 2.14.90.0.4-4
# Need binutils which can omit dot symbols and overlap .opd on ppc64 >= 2.15.91.0.2-4
# Need binutils which handle -msecure-plt on ppc >= 2.16.91.0.2-2
# Need binutils which support .weakref >= 2.16.91.0.3-1
# Need binutils which support --hash-style=gnu >= 2.17.50.0.2-7
# Need binutils which support mffgpr and mftgpr >= 2.17.50.0.2-8
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
# Need binutils which support --no-add-needed >= 2.20.51.0.2-12
# Need binutils which support -plugin
BuildRequires: binutils >= 2.24
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo, sharutils
BuildRequires: /usr/bin/pod2man
%if 0%{?rhel} >= 7
BuildRequires: texinfo-tex
%endif
# For VTA guality testing
BuildRequires: gdb
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires: glibc-devel >= 2.4.90-13
BuildRequires: elfutils-devel >= 0.147
BuildRequires: elfutils-libelf-devel >= 0.147
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
BuildRequires: glibc >= 2.3.90-35
%endif
%ifarch %{multilib_64_archs} sparcv9 ppc
# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif
%ifarch ia64
BuildRequires: libunwind >= 0.98
%endif
# Need .eh_frame ld optimizations
# Need proper visibility support
# Need -pie support
# Need --as-needed/--no-as-needed support
# On ppc64, need omit dot symbols support and --non-overlapping-opd
# Need binutils that owns /usr/bin/c++filt
# Need binutils that support .weakref
# Need binutils that supports --hash-style=gnu
# Need binutils that support mffgpr/mftgpr
# Need binutils that support --build-id
# Need binutils that support %gnu_unique_object
# Need binutils that support .cfi_sections
# Need binutils that support --no-add-needed
# Need binutils that support -plugin
Requires: binutils >= 2.24
# Make sure gdb will understand DW_FORM_strp
Conflicts: gdb < 5.1-2
Requires: glibc-devel >= 2.2.90-12
%ifarch ppc ppc64 ppc64le ppc64p7 s390 s390x sparc sparcv9 alpha
# Make sure glibc supports TFmode long double
Requires: glibc >= 2.3.90-35
%endif
Requires: libgcc >= 4.1.2-43
Requires: libgomp >= 4.4.4-13
BuildRequires: gmp-devel >= 4.1.2-8
BuildRequires: mpfr-devel >= 2.2.1
%if 0%{?rhel} >= 7
BuildRequires: libmpc-devel >= 0.8.1
%endif
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
ExclusiveArch: %{ix86} x86_64 ppc ppc64 ppc64le s390 s390x aarch64

%global oformat %{nil}
%global oformat2 %{nil}
%ifarch %{ix86}
%global oformat OUTPUT_FORMAT(elf32-i386)
%endif
%ifarch x86_64
%global oformat OUTPUT_FORMAT(elf64-x86-64)
%global oformat2 OUTPUT_FORMAT(elf32-i386)
%endif
%ifarch ppc
%global oformat OUTPUT_FORMAT(elf32-powerpc)
%global oformat2 OUTPUT_FORMAT(elf64-powerpc)
%endif
%ifarch ppc64
%global oformat OUTPUT_FORMAT(elf64-powerpc)
%global oformat2 OUTPUT_FORMAT(elf32-powerpc)
%endif
%ifarch s390
%global oformat OUTPUT_FORMAT(elf32-s390)
%endif
%ifarch s390x
%global oformat OUTPUT_FORMAT(elf64-s390)
%global oformat2 OUTPUT_FORMAT(elf32-s390)
%endif
%ifarch ia64
%global oformat OUTPUT_FORMAT(elf64-ia64-little)
%endif
%ifarch ppc64le
%global oformat OUTPUT_FORMAT(elf64-powerpcle)
%endif

Patch0: gcc7-hack.patch
Patch1: gcc7-ppc32-retaddr.patch
Patch2: gcc7-i386-libgomp.patch
Patch3: gcc7-sparc-config-detection.patch
Patch4: gcc7-libgomp-omp_h-multilib.patch
Patch5: gcc7-libtool-no-rpath.patch
Patch6: gcc7-isl-dl.patch
Patch7: gcc7-libstdc++-docs.patch
Patch8: gcc7-no-add-needed.patch
Patch9: gcc7-aarch64-async-unw-tables.patch
Patch10: gcc7-foffload-default.patch
Patch11: gcc7-Wno-format-security.patch

Patch1002: gcc7-alt-compat-test.patch
Patch1005: gcc7-rh1118870.patch
Patch1100: gcc7-htm-in-asm.patch

%if 0%{?rhel} >= 7
%global nonsharedver 48
%else
%global nonsharedver 44
%endif

%global _gnu %{nil}
%ifarch sparcv9
%global gcc_target_platform sparc64-%{_vendor}-%{_target_os}%{?_gnu}
%endif
%ifarch ppc
%global gcc_target_platform ppc64-%{_vendor}-%{_target_os}%{?_gnu}
%endif
%ifnarch sparcv9 ppc
%global gcc_target_platform %{_target_platform}
%endif

%description
This package contains various GCC runtime libraries, such as libatomic,
or libitm.

%package -n libitm
Summary: The GNU Transactional Memory library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n libatomic
Summary: The GNU Atomic library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libatomic
This package contains the GNU Atomic library
which is a GCC support runtime library for atomic operations not supported
by hardware.

%package -n libcilkrts
Summary: The Cilk+ runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libcilkrts
This package contains the Cilk+ runtime library.

%package -n libmpx
Summary: The Memory Protection Extensions runtime libraries
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libmpx
This package contains the Memory Protection Extensions runtime libraries
which is used for -fcheck-pointer-bounds -mmpx instrumented programs.

%package -n libgfortran4
Summary: Fortran runtime
Group: System Environment/Libraries
Autoreq: true
%if %{build_libquadmath}
Requires: libquadmath
%endif
%if "%{version}" != "%{gcc_version}"
Provides: libgfortran = %{gcc_provides}
%endif

%description -n libgfortran4
This package contains Fortran shared library which is needed to run
Fortran dynamically linked programs.

%prep
%if 0%{?rhel} >= 7
%setup -q -n gcc-%{version}-%{DATE}
%else
%setup -q -n gcc-%{version}-%{DATE} -a 1
%endif
%patch0 -p0 -b .hack~
%patch1 -p0 -b .ppc32-retaddr~
%patch2 -p0 -b .i386-libgomp~
%patch3 -p0 -b .sparc-config-detection~
%patch4 -p0 -b .libgomp-omp_h-multilib~
%patch5 -p0 -b .libtool-no-rpath~
%patch8 -p0 -b .no-add-needed~
%patch9 -p0 -b .aarch64-async-unw-tables~
%patch10 -p0 -b .foffload-default~
%patch11 -p0 -b .Wno-format-security~

sed -i -e 's/ -Wl,-z,nodlopen//g' gcc/ada/gcc-interface/Makefile.in

%ifarch %{ix86} x86_64
%if 0%{?rhel} < 7
# On i?86/x86_64 there are some incompatibilities in _Decimal* as well as
# aggregates containing larger vector passing.
%patch1002 -p0 -b .alt-compat-test~
%endif
%endif

%patch1005 -p0 -b .rh1118870~
%patch1100 -p0 -b .gcc6-htm-in-asm~

%if 0%{?rhel} == 6
# Default to -gdwarf-3 rather than -gdwarf-4
sed -i '/UInteger Var(dwarf_version)/s/Init(4)/Init(3)/' gcc/common.opt
sed -i 's/\(may be either 2, 3 or 4; the default version is \)4\./\13./' gcc/doc/invoke.texi
%endif

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h
cp -a libstdc++-v3/config/cpu/i{4,3}86/opt

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

sed -i -e 's/Common Driver Var(flag_report_bug)/& Init(1)/' gcc/common.opt

%ifarch ppc
if [ -d libstdc++-v3/config/abi/post/powerpc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/powerpc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/powerpc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/powerpc64-linux-gnu/32
fi
%endif
%build

# Undo the broken autoconf change in recent Fedora versions
export CONFIG_SITE=NONE

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}


%if 0%{?rhel} < 7
mkdir mpc mpc-install
cd mpc
../../mpc-%{mpc_version}/configure --disable-shared \
  CFLAGS="${CFLAGS:-%optflags} -fPIC" CXXFLAGS="${CXXFLAGS:-%optflags} -fPIC" \
  --prefix=`cd ..; pwd`/mpc-install
make %{?_smp_mflags}
make install
cd ..
%endif

CC=gcc
CXX=g++
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
%ifarch sparc
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mcpu=ultrasparc/-mtune=ultrasparc/g;s/-mcpu=v[78]//g'`
%endif
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
%ifarch sparc64
cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
chmod +x gcc64
CC=`pwd`/gcc64
cat > g++64 <<"EOF"
#!/bin/sh
exec /usr/bin/g++ -m64 "$@"
EOF
chmod +x g++64
CXX=`pwd`/g++64
%endif
%ifarch ppc64 ppc64le ppc64p7
if gcc -m64 -xc -S /dev/null -o - > /dev/null 2>&1; then
  cat > gcc64 <<"EOF"
#!/bin/sh
exec /usr/bin/gcc -m64 "$@"
EOF
  chmod +x gcc64
  CC=`pwd`/gcc64
  cat > g++64 <<"EOF"
#!/bin/sh
exec /usr/bin/g++ -m64 "$@"
EOF
  chmod +x g++64
  CXX=`pwd`/g++64
fi
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	GCJFLAGS="$OPT_FLAGS" \
	../configure --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla --enable-bootstrap \
	--enable-shared --enable-threads=posix --enable-checking=release \
	--enable-multilib --disable-libsanitizer \
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object \
	--enable-linker-build-id \
	--enable-languages=c,c++,lto,fortran \
	--enable-plugin --with-linker-hash-style=gnu \
%if 0%{?rhel} >= 7
	--enable-initfini-array \
%else
	--disable-initfini-array \
%endif
	--disable-libgcj \
	--without-ppl --without-cloog \
%if 0%{?rhel} < 7
	--with-mpc=`pwd`/mpc-install \
%endif
%if 0%{?rhel} >= 7
%if %{attr_ifunc}
        --enable-gnu-indirect-function \
%endif
%endif
%ifarch %{arm}
	--disable-sjlj-exceptions \
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
	--enable-secureplt \
%endif
%ifarch sparc sparcv9 sparc64 ppc ppc64 ppc64le ppc64p7 s390 s390x alpha
	--with-long-double-128 \
%endif
%ifarch sparc
	--disable-linux-futex \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
%ifarch sparc sparcv9
	--host=%{gcc_target_platform} --build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=v7
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
%if 0%{?rhel} >= 7
	--with-cpu-32=power7 --with-tune-32=power7 --with-cpu-64=power7 --with-tune-64=power7 \
%else
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc
	--build=%{gcc_target_platform} --target=%{gcc_target_platform} --with-cpu=default32
%endif
%ifarch %{ix86} x86_64
	--with-tune=generic \
%endif
%ifarch %{ix86}
	--with-arch=i686 \
%endif
%ifarch x86_64
	--with-arch_32=i686 \
%endif
%ifarch s390 s390x
	--with-arch=z9-109 --with-tune=z10 --enable-decimal-float \
%endif
%ifnarch sparc sparcv9 ppc
	--build=%{gcc_target_platform}
%endif

GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS"

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/libatomic rpm.doc/libitm rpm.doc/libcilkrts rpm.doc/libmpx

(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)

%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif

%if %{build_libatomic}
(cd libatomic; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libatomic/$i.libatomic
done)
%endif

%if %{build_libcilkrts}
(cd libcilkrts; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libcilkrts/$i.libcilkrts
done)
%endif

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9

%install
rm -fr %{buildroot}

cd obj-%{gcc_target_platform}

# Make sure libcilkrts can use system libgcc_s.so.1.
rm -f gcc/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
GROUP ( /%{_lib}/libgcc_s.so.1 libgcc.a )' > gcc/libgcc_s.so

mkdir -p %{buildroot}%{_prefix}/%{_lib}
mkdir -p %{buildroot}%{_infodir}

# Use make install DESTDIR trick to avoid bogus RPATHs.
%if %{build_libitm}
cd %{gcc_target_platform}/libitm/
mkdir temp
make install DESTDIR=`pwd`/temp
cp -a temp/usr/%{_lib}/libitm.so.1* %{buildroot}%{_prefix}/%{_lib}/
cp -a libitm.info %{buildroot}%{_infodir}/
cd ../..
%endif

%if %{build_libatomic}
cd %{gcc_target_platform}/libatomic/
mkdir temp
make install DESTDIR=`pwd`/temp
cp -a temp/usr/%{_lib}/libatomic.so.1* %{buildroot}%{_prefix}/%{_lib}/
cd ../..
%endif

%if %{build_libcilkrts}
cd %{gcc_target_platform}/libcilkrts/
mkdir temp
make install DESTDIR=`pwd`/temp
cp -a temp/usr/%{_lib}/libcilkrts.so.5* %{buildroot}%{_prefix}/%{_lib}/
cd ../..
%endif

%if %{build_libquadmath}
cd %{gcc_target_platform}/libquadmath/
mkdir temp
make install DESTDIR=`pwd`/temp
cp -a temp/usr/%{_lib}/libquadmath.so.0* %{buildroot}%{_prefix}/%{_lib}/
cd ../..
%endif

cd %{gcc_target_platform}/libgfortran/
mkdir temp
%if %{build_libquadmath}
# It needs to find libquadmath.so.
export LIBRARY_PATH=`pwd`/../../%{gcc_target_platform}/libquadmath/temp/usr/%{_lib}
%endif
make install DESTDIR=`pwd`/temp
cp -a temp/usr/%{_lib}/libgfortran.so.4* %{buildroot}%{_prefix}/%{_lib}/
cd ../..


# Remove binaries we will not be including, so that they don't end up in
# gcc-libraries-debuginfo.
%if 0%{?rhel} >= 7
rm -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.so*
%endif

rm -f gcc/libgcc_s.so
ln -sf libgcc_s.so.1 gcc/libgcc_s.so

%check
cd obj-%{gcc_target_platform}

# run the tests.
%ifnarch ppc64le
make %{?_smp_mflags} -k check RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
%else
make %{?_smp_mflags} -k check || :
%endif
( LC_ALL=C ../contrib/test_summary -t || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}' > testresults
echo ====================TESTING=========================
cat testresults
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

%clean
rm -rf %{buildroot}

%post -n libitm
/sbin/ldconfig
if [ -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%post -n libatomic
/sbin/ldconfig
if [ -f %{_infodir}/libatomic.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libatomic.info.gz || :
fi

%post -n libcilkrts
/sbin/ldconfig
if [ -f %{_infodir}/libcilkrts.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libcilkrts.info.gz || :
fi

%post -n libgfortran4
/sbin/ldconfig
if [ -f %{_infodir}/libgfortran.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libgfortran.info.gz || :
fi

%post -n libmpx -p /sbin/ldconfig

%preun -n libitm
if [ $1 = 0 -a -f %{_infodir}/libitm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libitm.info.gz || :
fi

%preun -n libatomic
if [ $1 = 0 -a -f %{_infodir}/libatomic.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libatomic.info.gz || :
fi

%preun -n libgfortran4
if [ $1 = 0 -a -f %{_infodir}/libgfortran.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgfortran.info.gz || :
fi

%preun -n libcilkrts
if [ $1 = 0 -a -f %{_infodir}/libcilkrts.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libcilkrts.info.gz || :
fi

%postun -n libitm -p /sbin/ldconfig

%postun -n libatomic -p /sbin/ldconfig

%postun -n libcilkrts -p /sbin/ldconfig

%postun -n libgfortran4 -p /sbin/ldconfig

%postun -n libmpx -p /sbin/ldconfig

%if %{build_libitm}
%files -n libitm
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libitm.so.1*
%{_infodir}/libitm.info*

%doc gcc/COPYING3 COPYING.RUNTIME rpm.doc/libitm/*
%endif

%if %{build_libatomic}
%files -n libatomic
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libatomic.so.1*

%doc gcc/COPYING3 COPYING.RUNTIME rpm.doc/libatomic/*
%endif

%if %{build_libcilkrts}
%files -n libcilkrts
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libcilkrts.so.5*

%doc gcc/COPYING3 COPYING.RUNTIME rpm.doc/libcilkrts/*
%endif

%files -n libgfortran4
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgfortran.so.4*

%doc gcc/COPYING3 COPYING.RUNTIME rpm.doc/gfortran/*

%changelog
* Thu Oct 19 2017 Marek Polacek <polacek@redhat.com> 7.2.1-1.1.1
- update from gcc-7.2.1-1 (#1477224)

* Tue Jun 20 2017 Marek Polacek <polacek@redhat.com> 7.1.1-2.2.1
- don't run make check with -fstack-protector on ppc64le

* Thu Jun 15 2017 Marek Polacek <polacek@redhat.com> 7.1.1-2.1.1
- bump gcc_release (DTS7 gcc-gfortran requires libgfortran4 >= 7.1.1-2)

* Mon Jun 12 2017 Marek Polacek <polacek@redhat.com> 7.1.1-1.2.1
- remove libquadmath.so.* so that it doesn't end up in debuginfo

* Mon Jun  5 2017 Marek Polacek <polacek@redhat.com> 7.1.1-1.1.1
- rename libgfortran2 to libgfortran4
- update from Fedora gcc-7.1.1-2.fc27
 
* Wed May 24 2017 Marek Polacek <polacek@redhat.com> 7.0.1-4.2.1
- also build on ppc64le

* Mon Mar 20 2017 Marek Polacek <polacek@redhat.com> 7.0.1-4.1.1
- also build on aarch64
- drop libitm
- only enable libatomic for aarch64

* Fri Mar 17 2017 Marek Polacek <polacek@redhat.com> 7.0.1-3.1.1
- drop libquadmath and rename libgfortran to libgfortran2

* Wed Mar 15 2017 Marek Polacek <polacek@redhat.com> 7.0.1-2.1.1
- also include the libquadmath subpackage

* Tue Mar 14 2017 Marek Polacek <polacek@redhat.com> 7.0.1-1.1.1
- update from Fedora 7.0.1-0.12.fc26 (#1412815)
- add the libgfortran subpackage

* Wed Oct 19 2016 Marek Polacek <polacek@redhat.com> 6.2.1-1.1.1
- update from DTS 6.2.1 (#1265255)

* Tue Oct 18 2016 Marek Polacek <polacek@redhat.com> 5.3.1-1.1.1
- update from DTS 5.3.1 (#1265255)
- run the whole testsuite (because of Cilk+)

* Tue Dec 15 2015 Marek Polacek <polacek@redhat.com> 5.2.1-2.1.1
- update from DTS 5.2.1-2 (#1265253)
- drop libmpx (#1275357)

* Fri Apr 10 2015 Marek Polacek <polacek@redhat.com> 5.0.0-1.1.1
- update from Fedora gcc-5.0.0-0.21.fc22
- add libmpx subpackage on x86

* Mon Jun 02 2014 Marek Polacek <polacek@redhat.com> 4.9.0-6.1.1
- make sure libcilkrts can use system libgcc_s.so.1 (#1101277)
- update from DTS gcc-4.9.0-6

* Fri May 23 2014 Marek Polacek <polacek@redhat.com> 4.9.0-5.2.1
- prevent bogus RPATHs

* Wed May 14 2014 Marek Polacek <polacek@redhat.com> 4.9.0-5.1.1
- update from DTS gcc-4.9.0-5
- add libcilkrts

* Mon Apr 28 2014 Marek Polacek <polacek@redhat.com> 4.8.2-12.1.1
- update from DTS gcc-4.8.2-12

* Wed Aug 14 2013 Marek Polacek <polacek@redhat.com> 4.8.1-4.2.1
- always build HTM bits in libitm (#996683, #996682)

* Fri Jul 19 2013 Marek Polacek <polacek@redhat.com> 4.8.1-4.1.1
- update from DTS gcc-4.8.1-4

* Wed May 29 2013 Marek Polacek <polacek@redhat.com> 4.8.0-5.1.1
- update from DTS gcc-4.8.0-5
- build libitm even for s390{,x}

* Thu May 02 2013 Marek Polacek <polacek@redhat.com> 4.8.0-3.1.1
- new package
