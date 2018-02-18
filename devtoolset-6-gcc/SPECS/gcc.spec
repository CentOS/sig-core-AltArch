%{?scl:%global __strip %%{_scl_root}/usr/bin/strip}
%{?scl:%global __objdump %%{_scl_root}/usr/bin/objdump}
%{?scl:%scl_package gcc}
%global DATE 20170216
%global SVNREV 245503
%global gcc_version 6.3.1
# Note, gcc_release must be integer, if you want to add suffixes to
# %{release}, append them after %{gcc_release} on Release: line.
%global gcc_release 3
%global mpc_version 0.8.1
%global isl_version 0.14
%global graphviz_version 2.26.0
%global doxygen_version 1.8.0
%global _unpackaged_files_terminate_build 0
%global multilib_64_archs sparc64 ppc64 s390x x86_64
%ifarch %{ix86} x86_64 ia64
%global build_libquadmath 1
%else
%global build_libquadmath 0
%endif
%global build_fortran 1
%ifarch %{ix86} x86_64 %{arm} alpha ppc ppc64 ppc64le ppc64p7 s390 s390x aarch64
%global build_libitm 1
%else
%global build_libitm 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le %{arm} aarch64
%global build_libasan 1
%else
%global build_libasan 0
%endif
%ifarch x86_64 aarch64
%global build_libtsan 1
%else
%global build_libtsan 0
%endif
%ifarch x86_64 aarch64
%global build_liblsan 1
%else
%global build_liblsan 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 %{arm} aarch64
%global build_libubsan 1
%else
%global build_libubsan 0
%endif
%ifarch %{ix86} x86_64
%global build_libcilkrts 1
%else
%global build_libcilkrts 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64p7 ppc64le s390 s390x %{arm} aarch64
%global build_libatomic 1
%else
%global build_libatomic 0
%endif
%ifarch %{ix86} x86_64 ppc ppc64 ppc64le ppc64p7 s390 s390x %{arm} aarch64
%global attr_ifunc 1
%else
%global attr_ifunc 0
%endif
%ifarch %{ix86} x86_64
%global build_libmpx 1
%else
%global build_libmpx 0
%endif
%global build_isl 1
%global build_libstdcxx_docs 1
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
Summary: GCC version 6
Name: %{?scl_prefix}gcc
#Name: %{?scl_prefix}gcc%{!?scl:5}
Version: %{gcc_version}
Release: %{gcc_release}.1%{?dist}
# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
Group: Development/Languages
# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# svn export svn://gcc.gnu.org/svn/gcc/branches/redhat/gcc-6-branch@%{SVNREV} gcc-%{version}-%{DATE}
# tar cf - gcc-%{version}-%{DATE} | bzip2 -9 > gcc-%{version}-%{DATE}.tar.bz2
Source0: gcc-%{version}-%{DATE}.tar.bz2
Source1: ftp://gcc.gnu.org/pub/gcc/infrastructure/isl-%{isl_version}.tar.bz2
Source2: http://www.multiprecision.org/mpc/download/mpc-%{mpc_version}.tar.gz
Source3: ftp://ftp.stack.nl/pub/users/dimitri/doxygen-%{doxygen_version}.src.tar.gz
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
BuildRequires: binutils >= 2.19.51.0.14-33
# While gcc doesn't include statically linked binaries, during testing
# -static is used several times.
BuildRequires: glibc-static
%if 0%{?scl:1}
BuildRequires: %{?scl_prefix}binutils >= 2.22.52.0.1
# For testing
BuildRequires: %{?scl_prefix}gdb >= 7.4.50
%endif
BuildRequires: zlib-devel, gettext, dejagnu, bison, flex, texinfo, sharutils, gcc-gfortran
BuildRequires: /usr/bin/pod2man
%if 0%{?rhel} >= 7
BuildRequires: texinfo-tex
%endif
#BuildRequires: systemtap-sdt-devel >= 1.3
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
# Need binutils which support --build-id >= 2.17.50.0.17-3
# Need binutils which support %gnu_unique_object >= 2.19.51.0.14
# Need binutils which support .cfi_sections >= 2.19.51.0.14-33
%if 0%{?scl:1}
Requires: %{?scl_prefix}binutils >= 2.22.52.0.1
%else
Requires: binutils >= 2.19.51.0.14-33
%endif
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
%if %{build_libstdcxx_docs}
BuildRequires: libxml2
BuildRequires: graphviz
%if 0%{?rhel} < 7
# doxygen BRs
BuildRequires: perl
BuildRequires: texlive-dvips, texlive-utils, texlive-latex
BuildRequires: ghostscript
%endif
%if 0%{?rhel} >= 7
BuildRequires: doxygen >= 1.7.1
BuildRequires: dblatex, texlive-collection-latex, docbook5-style-xsl
%endif
%endif
%{?scl:Requires:%scl_runtime}
%{?scl:Provides:gcc = %{version}-%{release}}
AutoReq: true
AutoProv: false
%ifarch sparc64 ppc64 ppc64le s390x x86_64 ia64
Provides: liblto_plugin.so.0()(64bit)
%else
Provides: liblto_plugin.so.0
%endif
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
%ifarch aarch64
%global oformat OUTPUT_FORMAT(elf64-littleaarch64)
%endif

Patch0: gcc6-hack.patch
Patch1: gcc6-java-nomulti.patch
Patch2: gcc6-ppc32-retaddr.patch
Patch3: gcc6-rh330771.patch
Patch4: gcc6-i386-libgomp.patch
Patch5: gcc6-sparc-config-detection.patch
Patch6: gcc6-libgomp-omp_h-multilib.patch
Patch7: gcc6-libtool-no-rpath.patch
Patch8: gcc6-isl-dl.patch
Patch9: gcc6-libstdc++-docs.patch
Patch10: gcc6-no-add-needed.patch
Patch11: gcc6-libgo-p224.patch
Patch12: gcc6-aarch64-async-unw-tables.patch
Patch13: gcc6-libsanitize-aarch64-va42.patch

Patch1000: gcc6-libstdc++-compat.patch
Patch1001: gcc6-libgfortran-compat.patch
Patch1002: gcc6-alt-compat-test.patch
Patch1003: gcc6-libquadmath-compat.patch
Patch1004: gcc6-libstdc++44-xfail.patch
Patch1005: gcc6-rh1118870.patch
Patch1006: gcc6-isl-dl2.patch

Patch2001: doxygen-1.7.1-config.patch
Patch2002: doxygen-1.7.5-timestamp.patch
Patch2003: doxygen-1.8.0-rh856725.patch

%if 0%{?rhel} >= 7
%global nonsharedver 48
%else
%global nonsharedver 44
%endif

%if 0%{?scl:1}
%global _gnu %{nil}
%else
%global _gnu 7E
%endif
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
The %{?scl_prefix}gcc%{!?scl:5} package contains the GNU Compiler Collection version 6.

%package c++
Summary: C++ support for GCC version 6
Group: Development/Languages
Requires: %{?scl_prefix}gcc%{!?scl:5} = %{version}-%{release}
%if 0%{?rhel} >= 7
Requires: libstdc++
%else
Requires: libstdc++ >= 4.4.4-13
%endif
Requires: %{?scl_prefix}libstdc++%{!?scl:5}-devel = %{version}-%{release}
Autoreq: true
Autoprov: true

%description c++
This package adds C++ support to the GNU Compiler Collection
version 6.  It includes support for most of the current C++ specification
and a lot of support for the upcoming C++ specification.

%package -n %{?scl_prefix}libstdc++%{!?scl:5}-devel
Summary: Header files and libraries for C++ development
Group: Development/Libraries
%if 0%{?rhel} >= 7
Requires: libstdc++
%else
Requires: libstdc++ >= 4.4.4-13
%endif
Requires: libstdc++%{?_isa}
Autoreq: true
Autoprov: true

%description -n %{?scl_prefix}libstdc++%{!?scl:5}-devel
This is the GNU implementation of the standard C++ libraries.  This
package includes the header files and libraries needed for C++
development. This includes rewritten implementation of STL.

%package -n %{?scl_prefix}libstdc++%{!?scl:5}-docs
Summary: Documentation for the GNU standard C++ library
Group: Development/Libraries
Autoreq: true

%description -n %{?scl_prefix}libstdc++%{!?scl:5}-docs
Manual, doxygen generated API information and Frequently Asked Questions
for the GNU standard C++ library.

%package gfortran
Summary: Fortran support for GCC 6
Group: Development/Languages
Requires: %{?scl_prefix}gcc%{!?scl:5} = %{version}-%{release}
%if 0%{?rhel} >= 7
Requires: libgfortran
%else
Requires: libgfortran >= 4.4.4-13
%endif
%if %{build_libquadmath}
%if 0%{!?scl:1}
%if 0%{?rhel} >= 7
Requires: libquadmath
%else
Requires: %{?scl_prefix}libquadmath = %{version}-%{release}
%endif
%else
%if 0%{?rhel} >= 7
Requires: libquadmath
%endif
%endif
Requires: %{?scl_prefix}libquadmath-devel = %{version}-%{release}
%endif
Autoreq: true
Autoprov: true

%description gfortran
The %{?scl_prefix}gcc%{!?scl:5}-gfortran package provides support for compiling Fortran
programs with the GNU Compiler Collection.

%package gdb-plugin
Summary: GCC 6 plugin for GDB
Group: Development/Debuggers
Requires: %{?scl_prefix}gcc%{!?scl:5} = %{version}-%{release}

%description gdb-plugin
This package contains GCC 6 plugin for GDB C expression evaluation.

%package -n %{?scl_prefix}libgccjit
Summary: Library for embedding GCC inside programs and libraries
Group: System Environment/Libraries
Requires: %{?scl_prefix}gcc%{!?scl:5} = %{version}-%{release}

%description -n %{?scl_prefix}libgccjit
This package contains shared library with GCC 6 JIT front end.

%package -n %{?scl_prefix}libgccjit-devel
Summary: Support for embedding GCC inside programs and libraries
Group: Development/Libraries
Requires: %{?scl_prefix}libgccjit = %{version}-%{release}
Requires: %{?scl_prefix}libgccjit-docs = %{version}-%{release}

%description -n %{?scl_prefix}libgccjit-devel
This package contains header files for GCC 6 JIT front end.

%package -n %{?scl_prefix}libgccjit-docs
Summary: Documentation for embedding GCC inside programs and libraries
Group: Development/Libraries
BuildRequires: python-sphinx
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n %{?scl_prefix}libgccjit-docs
This package contains documentation for GCC 6 JIT front end.

%package -n %{?scl_prefix}libquadmath
Summary: GCC 6 __float128 shared support library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n %{?scl_prefix}libquadmath
This package contains GCC shared support library which is needed
for __float128 math support and for Fortran REAL*16 support.

%package -n %{?scl_prefix}libquadmath-devel
Summary: GCC 6 __float128 support
Group: Development/Libraries
%if 0%{!?scl:1}
Requires: %{?scl_prefix}libquadmath = %{version}-%{release}
%else
%if 0%{?rhel} >= 7
Requires: libquadmath
%endif
%endif
Requires: %{?scl_prefix}gcc%{!?scl:5} = %{version}-%{release}

%description -n %{?scl_prefix}libquadmath-devel
This package contains headers for building Fortran programs using
REAL*16 and programs using __float128 math.

%package -n libitm
Summary: The GNU Transactional Memory library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libitm
This package contains the GNU Transactional Memory library
which is a GCC transactional memory support runtime library.

%package -n %{?scl_prefix}libitm-devel
Summary: The GNU Transactional Memory support
Group: Development/Libraries
Requires: libitm >= 4.7.0-1
Requires: %{?scl_prefix}gcc%{!?scl:5} = %{version}-%{release}

%description -n %{?scl_prefix}libitm-devel
This package contains headers and support files for the
GNU Transactional Memory library.

%package plugin-devel
Summary: Support for compiling GCC plugins
Group: Development/Languages
Requires: %{?scl_prefix}gcc%{!?scl:5} = %{version}-%{release}
Requires: gmp-devel >= 4.1.2-8
Requires: mpfr-devel >= 2.2.1
%if 0%{?rhel} >= 7
Requires: libmpc-devel >= 0.8.1
%endif

%description plugin-devel
This package contains header files and other support files
for compiling GCC 6 plugins.  The GCC plugin ABI is currently
not stable, so plugins must be rebuilt any time GCC is updated.

%package -n libatomic
Summary: The GNU Atomic library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libatomic
This package contains the GNU Atomic library
which is a GCC support runtime library for atomic operations not supported
by hardware.

%package -n %{?scl_prefix}libatomic-devel
Summary: The GNU Atomic static library
Group: Development/Libraries
Requires: libatomic >= 4.8.0

%description -n %{?scl_prefix}libatomic-devel
This package contains GNU Atomic static libraries.

%package -n libasan3
Summary: The Address Sanitizer runtime library from GCC 6
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libasan3
This package contains the Address Sanitizer library from GCC 6
which is used for -fsanitize=address instrumented programs.

%package -n %{?scl_prefix}libasan-devel
Summary: The Address Sanitizer static library
Group: Development/Libraries
Requires: libasan3 >= 5.1.1

%description -n %{?scl_prefix}libasan-devel
This package contains Address Sanitizer static runtime library.

%package -n libtsan
Summary: The Thread Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libtsan
This package contains the Thread Sanitizer library
which is used for -fsanitize=thread instrumented programs.

%package -n %{?scl_prefix}libtsan-devel
Summary: The Thread Sanitizer static library
Group: Development/Libraries
Requires: libtsan >= 5.1.1

%description -n %{?scl_prefix}libtsan-devel
This package contains Thread Sanitizer static runtime library.

%package -n libubsan
Summary: The Undefined Behavior Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libubsan
This package contains the Undefined Behavior Sanitizer library
which is used for -fsanitize=undefined instrumented programs.

%package -n %{?scl_prefix}libubsan-devel
Summary: The Undefined Behavior Sanitizer static library
Group: Development/Libraries
Requires: libubsan >= 5.1.1

%description -n %{?scl_prefix}libubsan-devel
This package contains Undefined behavior Sanitizer static runtime library.

%package -n liblsan
Summary: The Leak Sanitizer runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n liblsan
This package contains the Leak Sanitizer library
which is used for -fsanitize=leak instrumented programs.

%package -n %{?scl_prefix}liblsan-devel
Summary: The Leak Sanitizer static library
Group: Development/Libraries
Requires: liblsan >= 5.1.1

%description -n %{?scl_prefix}liblsan-devel
This package contains Leak Sanitizer static runtime library.

%package -n libcilkrts
Summary: The Cilk+ runtime library
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libcilkrts
This package contains the Cilk+ runtime library.

%package -n %{?scl_prefix}libcilkrts-devel
Summary: The Cilk+ static runtime library
Group: Development/Libraries
Requires: libcilkrts >= 5.1.1

%description -n %{?scl_prefix}libcilkrts-devel
This package contains the Cilk+ static runtime library.

%package -n libmpx
Summary: The Memory Protection Extensions runtime libraries
Group: System Environment/Libraries
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description -n libmpx
This package contains the Memory Protection Extensions runtime libraries
which is used for -fcheck-pointer-bounds -mmpx instrumented programs.

%package -n %{?scl_prefix}libmpx-devel
Summary: The Memory Protection Extensions static libraries
Group: Development/Libraries
Requires: libmpx >= 5.1.1

%description -n %{?scl_prefix}libmpx-devel
This package contains the Memory Protection Extensions static runtime libraries.

%prep
%if 0%{?rhel} >= 7
%setup -q -n gcc-%{version}-%{DATE} -a 1
%else
%setup -q -n gcc-%{version}-%{DATE} -a 1 -a 2 -a 3
%endif
%patch0 -p0 -b .hack~
%patch1 -p0 -b .java-nomulti~
%patch2 -p0 -b .ppc32-retaddr~
%patch3 -p0 -b .rh330771~
%patch4 -p0 -b .i386-libgomp~
%patch5 -p0 -b .sparc-config-detection~
%patch6 -p0 -b .libgomp-omp_h-multilib~
%patch7 -p0 -b .libtool-no-rpath~
%if %{build_isl}
%patch8 -p0 -b .isl-dl~
%endif
%if %{build_libstdcxx_docs}
%patch9 -p0 -b .libstdc++-docs~
%endif
%patch10 -p0 -b .no-add-needed~
%patch11 -p0 -b .libgo-p224~
rm -f libgo/go/crypto/elliptic/p224{,_test}.go
%patch12 -p0 -b .aarch64-async-unw-tables~
%patch13 -p0 -b .libsanitize-aarch64-va42~
sed -i -e 's/ -Wl,-z,nodlopen//g' gcc/ada/gcc-interface/Makefile.in

%patch1000 -p0 -b .libstdc++-compat~
%patch1001 -p0 -b .libgfortran-compat~
%ifarch %{ix86} x86_64
%if 0%{?rhel} < 7
# On i?86/x86_64 there are some incompatibilities in _Decimal* as well as
# aggregates containing larger vector passing.
%patch1002 -p0 -b .alt-compat-test~
%endif
%endif
%if 0%{?rhel} < 7
%patch1003 -p0 -b .libquadmath-compat~
%endif
%if 0%{?rhel} == 6
# Fix this up
#%patch1004 -p0 -b .libstdc++44-xfail~
%endif
%patch1005 -p0 -b .rh1118870~
%patch1006 -p0 -b .isl-dl2~

%if %{build_libstdcxx_docs}
%if 0%{?rhel} < 7
cd doxygen-%{doxygen_version}
%patch2001 -p1 -b .config~
%patch2002 -p1 -b .timestamp~
%patch2003 -p1 -b .rh856725~
cd ..
%endif
%endif

echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

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
%ifarch sparc
if [ -d libstdc++-v3/config/abi/post/sparc64-linux-gnu ]; then
  mkdir -p libstdc++-v3/config/abi/post/sparc64-linux-gnu/64
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{,64/}baseline_symbols.txt
  mv libstdc++-v3/config/abi/post/sparc64-linux-gnu/{32/,}baseline_symbols.txt
  rm -rf libstdc++-v3/config/abi/post/sparc64-linux-gnu/32
fi
%endif

%build

# Undo the broken autoconf change in recent Fedora versions
export CONFIG_SITE=NONE

rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

%if %{build_libstdcxx_docs}

%if 0%{?rhel} < 7
mkdir doxygen-install
pushd ../doxygen-%{doxygen_version}
./configure --prefix `cd ..; pwd`/obj-%{gcc_target_platform}/doxygen-install \
  --shared --release --english-only

make %{?_smp_mflags} all
make install
popd
export PATH=`pwd`/doxygen-install/bin/${PATH:+:${PATH}}
%endif
%endif

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

%if %{build_isl}
mkdir isl-build isl-install
%ifarch s390 s390x
ISL_FLAG_PIC=-fPIC
%else
ISL_FLAG_PIC=-fpic
%endif
cd isl-build
sed -i 's|libisl|libgcc6privateisl|g' \
  ../../isl-%{isl_version}/Makefile.{am,in}
../../isl-%{isl_version}/configure \
  CC=/usr/bin/gcc CXX=/usr/bin/g++ \
  CFLAGS="${CFLAGS:-%optflags} $ISL_FLAG_PIC" --prefix=`cd ..; pwd`/isl-install
make %{?_smp_mflags}
make install
cd ../isl-install/lib
rm libgcc6privateisl.so{,.13}
mv libgcc6privateisl.so.13.1.0 libisl.so.13
ln -sf libisl.so.13 libisl.so
cd ../..
%endif

%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}

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
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
CONFIGURE_OPTS="\
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--with-bugurl=http://bugzilla.redhat.com/bugzilla \
	--enable-shared --enable-threads=posix --enable-checking=release \
%ifarch ppc64le
	--enable-targets=powerpcle-linux --disable-multilib \
%else
	--enable-multilib \
%endif
	--with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
	--enable-gnu-unique-object \
	--enable-linker-build-id \
	--enable-plugin --with-linker-hash-style=gnu \
%if 0%{?scl:1}
	--enable-initfini-array \
%else
%ifnarch ia64
%if 0%{?rhel} >= 7
	--enable-initfini-array \
%else
	--disable-initfini-array \
%endif
%endif
%endif
	--disable-libgcj \
%if 0%{rhel} < 8
	--with-default-libstdcxx-abi=gcc4-compatible \
%endif
%if %{build_isl}
	--with-isl=`pwd`/isl-install \
%else
	--without-isl \
%endif
%if %{build_libmpx}
	--enable-libmpx \
%else
	--disable-libmpx \
%endif
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
%ifarch ppc ppc64 ppc64p7
%if 0%{?rhel} >= 7
	--with-cpu-32=power7 --with-tune-32=power7 --with-cpu-64=power7 --with-tune-64=power7 \
%else
	--with-cpu-32=power4 --with-tune-32=power6 --with-cpu-64=power4 --with-tune-64=power6 \
%endif
%endif
%ifarch ppc64le
%if 0%{?rhel} >= 7
	--with-cpu-32=power8 --with-tune-32=power8 --with-cpu-64=power8 --with-tune-64=power8 \
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
	--build=%{gcc_target_platform} \
%endif
	"

CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	GCJFLAGS="$OPT_FLAGS" \
	../configure --enable-bootstrap \
%if %{build_fortran}
	--enable-languages=c,c++,fortran,lto \
%else
	--enable-languages=c,c++,lto \
%endif
	$CONFIGURE_OPTS

%ifarch ia64
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" bootstrap
%else
GCJFLAGS="$OPT_FLAGS" make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" profiledbootstrap
%endif

echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 -lstdc++_nonshared%{nonsharedver} )' \
  > %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_system.so

# Relink libcc1 against -lstdc++_nonshared:
sed -i -e '/^postdeps/s/-lstdc++/-lstdc++_system/' libcc1/libtool
rm -f libcc1/libcc1.la
make -C libcc1 libcc1.la

CC="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cc`"
CXX="`%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-cxx` `%{gcc_target_platform}/libstdc++-v3/scripts/testsuite_flags --build-includes`"

# Build libgccjit separately, so that normal compiler binaries aren't -fpic
# unnecessarily.
mkdir objlibgccjit
cd objlibgccjit
CC="$CC" CXX="$CXX" CFLAGS="$OPT_FLAGS" \
	CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g'`" \
	XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../../configure --disable-bootstrap --enable-host-shared \
	--enable-languages=jit $CONFIGURE_OPTS
make %{?_smp_mflags} BOOT_CFLAGS="$OPT_FLAGS" all-gcc
cp -a gcc/libgccjit.so* ../gcc/
cd ../gcc/
ln -sf xgcc %{gcc_target_platform}-gcc-%{version}
cp -a Makefile{,.orig}
sed -i -e '/^CHECK_TARGETS/s/$/ check-jit/' Makefile
touch -r Makefile.orig Makefile
rm Makefile.orig
make jit.sphinx.html
make jit.sphinx.install-html jit_htmldir=`pwd`/../../rpm.doc/libgccjit-devel/html
cd ..

%if %{build_isl}
cp -a isl-install/lib/libisl.so.13 gcc/
%endif

# Make generated man pages even if Pod::Man is not new enough
perl -pi -e 's/head3/head2/' ../contrib/texi2pod.pl
for i in ../gcc/doc/*.texi; do
  cp -a $i $i.orig; sed 's/ftable/table/' $i.orig > $i
done
make -C gcc generated-manpages
for i in ../gcc/doc/*.texi; do mv -f $i.orig $i; done

# Make generated doxygen pages.
%if %{build_libstdcxx_docs}
cd %{gcc_target_platform}/libstdc++-v3
make doc-html-doxygen
make doc-man-doxygen
cd ../..
%endif

# Copy various doc files here and there
cd ..
mkdir -p rpm.doc/gfortran rpm.doc/libquadmath rpm.doc/libitm
mkdir -p rpm.doc/changelogs/{gcc/cp,gcc/jit,libstdc++-v3,libgomp,libcc1,libatomic,libsanitizer,libcilkrts,libmpx}

for i in {gcc,gcc/cp,gcc/jit,libstdc++-v3,libgomp,libcc1,libatomic,libsanitizer,libcilkrts,libmpx}/ChangeLog*; do
	cp -p $i rpm.doc/changelogs/$i
done

%if %{build_fortran}
(cd gcc/fortran; for i in ChangeLog*; do
	cp -p $i ../../rpm.doc/gfortran/$i
done)
(cd libgfortran; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/gfortran/$i.libgfortran
done)
%endif

%if %{build_libquadmath}
(cd libquadmath; for i in ChangeLog* COPYING.LIB; do
	cp -p $i ../rpm.doc/libquadmath/$i.libquadmath
done)
%endif

%if %{build_libitm}
(cd libitm; for i in ChangeLog*; do
	cp -p $i ../rpm.doc/libitm/$i.libitm
done)
%endif

rm -f rpm.doc/changelogs/gcc/ChangeLog.[1-9]
find rpm.doc -name \*ChangeLog\* | xargs bzip2 -9
mkdir libstdc++_compat_test
cd libstdc++_compat_test
readelf -Ws %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 | sed -n '/\.symtab/,$d;/ UND /d;/@GLIBC_PRIVATE/d;/\(GLOBAL\|WEAK\|UNIQUE\)/p' | awk '{ if ($4 == "OBJECT") { printf "%s %s %s %s %s\n", $8, $4, $5, $6, $3 } else { printf "%s %s %s %s\n", $8, $4, $5, $6 }}' | sed 's/ UNIQUE / GLOBAL /;s/ WEAK / GLOBAL /;s/@@GLIBCXX_[0-9.]*//;s/@@CXXABI_TM_[0-9.]*//;s/@@CXXABI_FLOAT128//;s/@@CXXABI_[0-9.]*//' | LC_ALL=C sort -u > system.abilist
readelf -Ws ../obj-%{gcc_target_platform}/%{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so.6 | sed -n '/\.symtab/,$d;/ UND /d;/@GLIBC_PRIVATE/d;/\(GLOBAL\|WEAK\|UNIQUE\)/p' | awk '{ if ($4 == "OBJECT") { printf "%s %s %s %s %s\n", $8, $4, $5, $6, $3 } else { printf "%s %s %s %s\n", $8, $4, $5, $6 }}' | sed 's/ UNIQUE / GLOBAL /;s/ WEAK / GLOBAL /;s/@@GLIBCXX_[0-9.]*//;s/@@CXXABI_TM_[0-9.]*//;s/@@CXXABI_FLOAT128//;s/@@CXXABI_[0-9.]*//' | LC_ALL=C sort -u > vanilla.abilist
diff -up system.abilist vanilla.abilist | awk '/^\+\+\+/{next}/^\+/{print gensub(/^+(.*)$/,"\\1","1",$0)}' > system2vanilla.abilist.diff
../obj-%{gcc_target_platform}/gcc/xgcc -B ../obj-%{gcc_target_platform}/gcc/ -shared -o libstdc++_nonshared.so -Wl,--whole-archive ../obj-%{gcc_target_platform}/%{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared%{nonsharedver}.a -Wl,--no-whole-archive %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6
readelf -Ws libstdc++_nonshared.so | sed -n '/\.symtab/,$d;/ UND /d;/@GLIBC_PRIVATE/d;/\(GLOBAL\|WEAK\|UNIQUE\)/p' | awk '{ if ($4 == "OBJECT") { printf "%s %s %s %s %s\n", $8, $4, $5, $6, $3 } else { printf "%s %s %s %s\n", $8, $4, $5, $6 }}' | sed 's/ UNIQUE / GLOBAL /;s/ WEAK / GLOBAL /;s/@@GLIBCXX_[0-9.]*//;s/@@CXXABI_TM_[0-9.]*//;s/@@CXXABI_FLOAT128//;s/@@CXXABI_[0-9.]*//' | LC_ALL=C sort -u > nonshared.abilist
echo ====================NONSHARED=========================
ldd -d -r ./libstdc++_nonshared.so || :
ldd -u ./libstdc++_nonshared.so || :
diff -up system2vanilla.abilist.diff nonshared.abilist || :
echo ====================NONSHARED END=====================
rm -f libstdc++_nonshared.so
cd ..
mkdir libgfortran_compat_test
cd libgfortran_compat_test
TEST_LIBQUADMATH=
%if %{build_libquadmath}
TEST_LIBQUADMATH=`pwd`/../obj-%{gcc_target_platform}/%{gcc_target_platform}/libquadmath/.libs/libquadmath.so.0
%endif
readelf -Ws %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libgfortran.so.3 | sed -n '/\.symtab/,$d;/ UND /d;/@GLIBC_PRIVATE/d;/\(GLOBAL\|WEAK\|UNIQUE\)/p' | awk '{ if ($4 == "OBJECT") { printf "%s %s %s %s %s\n", $8, $4, $5, $6, $3 } else { printf "%s %s %s %s\n", $8, $4, $5, $6 }}' | sed 's/ UNIQUE / GLOBAL /;s/ WEAK / GLOBAL /;s/@@GFORTRAN_[0-9.]*//;s/@@GFORTRAN_C99_TM_[0-9.]*//;s/@@GFORTRAN_C99_FLOAT128//;s/@@GFORTRAN_C99_[0-9.]*//' | LC_ALL=C sort -u > system.abilist
readelf -Ws ../obj-%{gcc_target_platform}/%{gcc_target_platform}/libgfortran/.libs/libgfortran.so.3 | sed -n '/\.symtab/,$d;/ UND /d;/@GLIBC_PRIVATE/d;/\(GLOBAL\|WEAK\|UNIQUE\)/p' | awk '{ if ($4 == "OBJECT") { printf "%s %s %s %s %s\n", $8, $4, $5, $6, $3 } else { printf "%s %s %s %s\n", $8, $4, $5, $6 }}' | sed 's/ UNIQUE / GLOBAL /;s/ WEAK / GLOBAL /;s/@@GFORTRAN_[0-9.]*//;s/@@GFORTRAN_C99_TM_[0-9.]*//;s/@@GFORTRAN_C99_FLOAT128//;s/@@GFORTRAN_C99_[0-9.]*//' | LC_ALL=C sort -u > vanilla.abilist
diff -up system.abilist vanilla.abilist | awk '/^\+\+\+/{next}/^\+/{print gensub(/^+(.*)$/,"\\1","1",$0)}' > system2vanilla.abilist.diff
../obj-%{gcc_target_platform}/gcc/xgcc -B ../obj-%{gcc_target_platform}/gcc/ -shared -o libgfortran_nonshared.so -Wl,--whole-archive ../obj-%{gcc_target_platform}/%{gcc_target_platform}/libgfortran/.libs/libgfortran_nonshared%{nonsharedver}.a -Wl,--no-whole-archive %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libgfortran.so.3 $TEST_LIBQUADMATH
readelf -Ws libgfortran_nonshared.so | sed -n '/\.symtab/,$d;/ UND /d;/@GLIBC_PRIVATE/d;/\(GLOBAL\|WEAK\|UNIQUE\)/p' | awk '{ if ($4 == "OBJECT") { printf "%s %s %s %s %s\n", $8, $4, $5, $6, $3 } else { printf "%s %s %s %s\n", $8, $4, $5, $6 }}' | sed 's/ UNIQUE / GLOBAL /;s/ WEAK / GLOBAL /;s/@@GFORTRAN_[0-9.]*//;s/@@GFORTRAN_C99_TM_[0-9.]*//;s/@@GFORTRAN_C99_FLOAT128//;s/@@GFORTRAN_C99_[0-9.]*//' | LC_ALL=C sort -u > nonshared.abilist
echo ====================NONSHARED ========================
ldd -d -r ./libgfortran_nonshared.so || :
ldd -u ./libgfortran_nonshared.so || :
diff -up system2vanilla.abilist.diff nonshared.abilist || :
echo ====================NONSHARED END=====================
rm -f libgfortran_nonshared.so
cd ..

%install
rm -fr %{buildroot}

%if %{build_libstdcxx_docs}
%if 0%{?rhel} < 7
export PATH=`pwd`/obj-%{gcc_target_platform}/doxygen-install/bin/${PATH:+:${PATH}}
%endif
%endif

%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}
# Also set LD_LIBRARY_PATH so that DTS eu-strip (called from find-debuginfo.sh)
# can find the libraries it needs.
%{?scl:export LD_LIBRARY_PATH=%{_libdir}${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}}

perl -pi -e \
  's~href="l(ibstdc|atest)~href="http://gcc.gnu.org/onlinedocs/libstdc++/l\1~' \
  libstdc++-v3/doc/html/api.html

cd obj-%{gcc_target_platform}

TARGET_PLATFORM=%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
make -C %{gcc_target_platform}/libstdc++-v3

%if 0%{?scl:1}
rm -f gcc/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
GROUP ( /%{_lib}/libgcc_s.so.1 libgcc.a )' > gcc/libgcc_s.so
%endif

make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
  infodir=%{buildroot}%{_infodir} install

%if 0%{?scl:1}
rm -f gcc/libgcc_s.so
ln -sf libgcc_s.so.1 gcc/libgcc_s.so
%endif

FULLPATH=%{buildroot}%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
FULLEPATH=%{buildroot}%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}

%if 0%{?scl:1}
ln -sf ../../../../bin/ar $FULLEPATH/ar
ln -sf ../../../../bin/as $FULLEPATH/as
ln -sf ../../../../bin/ld $FULLEPATH/ld
ln -sf ../../../../bin/ld.bfd $FULLEPATH/ld.bfd
ln -sf ../../../../bin/ld.gold $FULLEPATH/ld.gold
ln -sf ../../../../bin/nm $FULLEPATH/nm
ln -sf ../../../../bin/ranlib $FULLEPATH/ranlib
ln -sf ../../../../bin/strip $FULLEPATH/strip
%endif

%if %{build_isl}
cp -a isl-install/lib/libisl.so.13 $FULLPATH/
%endif

# fix some things
ln -sf gcc %{buildroot}%{_prefix}/bin/cc
mkdir -p %{buildroot}/lib
ln -sf ..%{_prefix}/bin/cpp %{buildroot}/lib/cpp
%if %{build_fortran}
ln -sf gfortran %{buildroot}%{_prefix}/bin/f95
%endif
rm -f %{buildroot}%{_infodir}/dir
gzip -9 %{buildroot}%{_infodir}/*.info*
ln -sf gcc %{buildroot}%{_prefix}/bin/gnatgcc

cxxconfig="`find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h`"
for i in `find %{gcc_target_platform}/[36]*/libstdc++-v3/include -name c++config.h 2>/dev/null`; do
  if ! diff -up $cxxconfig $i; then
    cat > %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/c++config.h <<EOF
#ifndef _CPP_CPPCONFIG_WRAPPER
#define _CPP_CPPCONFIG_WRAPPER 1
#include <bits/wordsize.h>
#if __WORDSIZE == 32
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/32/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%endif
#else
%ifarch %{multilib_64_archs}
`cat $(find %{gcc_target_platform}/libstdc++-v3/include -name c++config.h)`
%else
`cat $(find %{gcc_target_platform}/64/libstdc++-v3/include -name c++config.h)`
%endif
#endif
#endif
EOF
    break
  fi
done

for f in `find %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/ -name c++config.h`; do
  for i in 1 2 4 8; do
    sed -i -e 's/#define _GLIBCXX_ATOMIC_BUILTINS_'$i' 1/#ifdef __GCC_HAVE_SYNC_COMPARE_AND_SWAP_'$i'\
&\
#endif/' $f
  done
  # Force the old ABI unconditionally, the new one does not work in the
  # libstdc++_nonshared.a model against RHEL 6/7 libstdc++.so.6.
  sed -i -e 's/\(define[[:blank:]]*_GLIBCXX_USE_DUAL_ABI[[:blank:]]*\)1/\10/' $f
done

# Nuke bits/*.h.gch dirs
# 1) there is no bits/*.h header installed, so when gch file can't be
#    used, compilation fails
# 2) sometimes it is hard to match the exact options used for building
#    libstdc++-v3 or they aren't desirable
# 3) there are multilib issues, conflicts etc. with this
# 4) it is huge
# People can always precompile on their own whatever they want, but
# shipping this for everybody is unnecessary.
rm -rf %{buildroot}%{_prefix}/include/c++/%{gcc_version}/%{gcc_target_platform}/bits/*.h.gch

%if %{build_libstdcxx_docs}
libstdcxx_doc_builddir=%{gcc_target_platform}/libstdc++-v3/doc/doxygen
mkdir -p ../rpm.doc/libstdc++-v3
cp -r -p ../libstdc++-v3/doc/html ../rpm.doc/libstdc++-v3/html
cp -r -p $libstdcxx_doc_builddir/html ../rpm.doc/libstdc++-v3/html/api
mkdir -p %{buildroot}%{_mandir}/man3
cp -r -p $libstdcxx_doc_builddir/man/man3/* %{buildroot}%{_mandir}/man3/
find ../rpm.doc/libstdc++-v3 -name \*~ | xargs rm
%endif

%ifarch sparcv9 sparc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}%{?_gnu}-gcc
%endif
%ifarch ppc ppc64
ln -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gcc \
  %{buildroot}%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}%{?_gnu}-gcc
%endif

%ifarch sparcv9 ppc
FULLLPATH=$FULLPATH/lib32
%endif
%ifarch sparc64 ppc64
FULLLPATH=$FULLPATH/lib64
%endif
if [ -n "$FULLLPATH" ]; then
  mkdir -p $FULLLPATH
else
  FULLLPATH=$FULLPATH
fi

find %{buildroot} -name \*.la | xargs rm -f

%if %{build_fortran}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.spec $FULLPATH/libgfortran.spec
%endif
%if %{build_libitm}
mv %{buildroot}%{_prefix}/%{_lib}/libitm.spec $FULLPATH/
%endif
%if %{build_libasan}
mv %{buildroot}%{_prefix}/%{_lib}/libsanitizer.spec $FULLPATH/
%endif
%if %{build_libcilkrts}
mv %{buildroot}%{_prefix}/%{_lib}/libcilkrts.spec $FULLPATH/
%endif
%if %{build_libmpx}
mv %{buildroot}%{_prefix}/%{_lib}/libmpx.spec $FULLPATH/
%endif

mkdir -p %{buildroot}/%{_lib}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgcc_s.so.1 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
chmod 755 %{buildroot}/%{_lib}/libgcc_s-%{gcc_version}-%{DATE}.so.1
ln -sf libgcc_s-%{gcc_version}-%{DATE}.so.1 %{buildroot}/%{_lib}/libgcc_s.so.1
ln -sf /%{_lib}/libgcc_s.so.1 $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
ln -sf /lib64/libgcc_s.so.1 $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
ln -sf /lib/libgcc_s.so.1 $FULLPATH/32/libgcc_s.so
%endif

rm -f $FULLPATH/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
GROUP ( /%{_lib}/libgcc_s.so.1 libgcc.a )' > $FULLPATH/libgcc_s.so
%ifarch sparcv9 ppc
rm -f $FULLPATH/64/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
GROUP ( /lib64/libgcc_s.so.1 libgcc.a )' > $FULLPATH/64/libgcc_s.so
%endif
%ifarch %{multilib_64_archs}
rm -f $FULLPATH/32/libgcc_s.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
GROUP ( /lib/libgcc_s.so.1 libgcc.a )' > $FULLPATH/32/libgcc_s.so
%endif

%if %{build_libquadmath}
%if 0%{?scl:1}
%if 0%{?rhel} < 7
cp -a %{gcc_target_platform}/libquadmath/.libs/libquadmathconvenience.a \
  %{buildroot}%{_prefix}/%{_lib}/libquadmath.a
%endif
%endif
%endif

mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.spec $FULLPATH/
cp -a %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared%{nonsharedver}.a \
  $FULLLPATH/libstdc++_nonshared.a
%if %{build_fortran}
cp -a %{gcc_target_platform}/libgfortran/.libs/libgfortran_nonshared%{nonsharedver}.a \
  $FULLPATH/libgfortran_nonshared.a
%ifarch sparcv9 ppc
cp -a %{gcc_target_platform}/64/libgfortran/.libs/libgfortran_nonshared%{nonsharedver}.a \
  $FULLPATH/64/libgfortran_nonshared.a
%endif
%ifarch %{multilib_64_archs}
cp -a %{gcc_target_platform}/32/libgfortran/.libs/libgfortran_nonshared%{nonsharedver}.a \
  $FULLPATH/32/libgfortran_nonshared.a
%endif
%endif

rm -f $FULLEPATH/libgccjit.so
mkdir -p %{buildroot}%{_prefix}/%{_lib}/
cp -a objlibgccjit/gcc/libgccjit.so.* %{buildroot}%{_prefix}/%{_lib}/
rm -f $FULLPATH/libgccjit.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{_prefix}/%{_lib}/libgccjit.so.0 )' > $FULLPATH/libgccjit.so
cp -a ../gcc/jit/libgccjit*.h $FULLPATH/include/
/usr/bin/install -c -m 644 objlibgccjit/gcc/doc/libgccjit.info %{buildroot}/%{_infodir}/
gzip -9 %{buildroot}/%{_infodir}/libgccjit.info

pushd $FULLPATH
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libgomp.so.1 )' > libgomp.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 -lstdc++_nonshared )' > libstdc++.so
%if %{build_fortran}
rm -f libgfortran.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
INPUT ( -lgfortran_nonshared %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libgfortran.so.3 AS_NEEDED ( -ldl ) )' > libgfortran.so
%endif
%if %{build_libquadmath}
rm -f libquadmath.so
echo '/* GNU ld script */
%{oformat}
%if 0%{!?scl:1}
INPUT ( %{_prefix}/%{_lib}/libquadmath.so.0 )' > libquadmath.so
%else
%if 0%{?rhel} >= 7
INPUT ( %{_root_prefix}/%{_lib}/libquadmath.so.0 )' > libquadmath.so
%else
INPUT ( libquadmath.a )' > libquadmath.so
%endif
%endif
%endif
%if %{build_libitm}
rm -f libitm.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libitm.so.1 )' > libitm.so
%endif
%if %{build_libatomic}
rm -f libatomic.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libatomic.so.1 )' > libatomic.so
%endif
%if %{build_libasan}
rm -f libasan.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libasan.so.3 )' > libasan.so
%endif
%if %{build_libtsan}
rm -f libtsan.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libtsan.so.0 )' > libtsan.so
%endif
%if %{build_libubsan}
rm -f libubsan.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libubsan.so.0 )' > libubsan.so
%endif
%if %{build_liblsan}
rm -f liblsan.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/liblsan.so.0 )' > liblsan.so
%endif
%if %{build_libcilkrts}
rm -f libcilkrts.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libcilkrts.so.5 )' > libcilkrts.so
%endif
%if %{build_libmpx}
rm -f libmpx.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libmpx.so.2 )' > libmpx.so
rm -f libmpxwrappers.so
echo '/* GNU ld script */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libmpxwrappers.so.2 )' > libmpxwrappers.so
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libstdc++fs.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libsupc++.*a .
%if %{build_fortran}
mv -f %{buildroot}%{_prefix}/%{_lib}/libgfortran.*a .
%endif
mv -f %{buildroot}%{_prefix}/%{_lib}/libgomp.*a .
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/%{_lib}/libquadmath.*a $FULLLPATH/
%endif
%if %{build_libitm}
mv -f %{buildroot}%{_prefix}/%{_lib}/libitm.*a $FULLLPATH/
%endif
%if %{build_libatomic}
mv -f %{buildroot}%{_prefix}/%{_lib}/libatomic.*a $FULLLPATH/
%endif
%if %{build_libasan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libasan.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libasan_preinit.o $FULLLPATH/
%endif
%if %{build_libtsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libtsan.*a $FULLLPATH/
%endif
%if %{build_libubsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/libubsan.*a $FULLLPATH/
%endif
%if %{build_liblsan}
mv -f %{buildroot}%{_prefix}/%{_lib}/liblsan.*a $FULLLPATH/
%endif
%if %{build_libcilkrts}
mv -f %{buildroot}%{_prefix}/%{_lib}/libcilkrts.*a $FULLLPATH/
%endif
%if %{build_libmpx}
mv -f %{buildroot}%{_prefix}/%{_lib}/libmpx.*a $FULLLPATH/
mv -f %{buildroot}%{_prefix}/%{_lib}/libmpxwrappers.*a $FULLLPATH/
%endif

%ifarch sparcv9 ppc
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libstdc++.so.6 -lstdc++_nonshared )' > 64/libstdc++.so
%if %{build_fortran}
rm -f 64/libgfortran.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( -lgfortran_nonshared %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libgfortran.so.3 AS_NEEDED ( -ldl ) )' > 64/libgfortran.so
%endif
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libgomp.so.1 )' > 64/libgomp.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{_prefix}/lib64/libgccjit.so.0 )' > 64/libgccjit.so
%if %{build_libquadmath}
rm -f 64/libquadmath.so
echo '/* GNU ld script */
%{oformat2}
%if 0%{!?scl:1}
INPUT ( %{_prefix}/lib64/libquadmath.so.0 )' > 64/libquadmath.so
%else
%if 0%{?rhel} >= 7
INPUT ( %{_root_prefix}/lib64/libquadmath.so.0 )' > 64/libquadmath.so
%else
INPUT ( libquadmath.a )' > 64/libquadmath.so
%endif
%endif
%endif
%if %{build_libitm}
rm -f 64/libitm.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libitm.so.1 )' > 64/libitm.so
%endif
%if %{build_libatomic}
rm -f 64/libatomic.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libatomic.so.1 )' > 64/libatomic.so
%endif
%if %{build_libasan}
rm -f 64/libasan.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libasan.so.3 )' > 64/libasan.so
%endif
%if %{build_libubsan}
rm -f 64/libubsan.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libubsan.so.0 )' > 64/libubsan.so
%endif
%if %{build_libcilkrts}
rm -f 64/libcilkrts.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libcilkrts.so.5 )' > 64/libcilkrts.so
%endif
%if %{build_libmpx}
rm -f 64/libmpx.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libmpx.so.2 )' > 64/libmpx.so
rm -f 64/libmpxwrappers.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib64/libmpxwrappers.so.2 )' > 64/libmpxwrappers.so
%endif
mv -f %{buildroot}%{_prefix}/lib64/libsupc++.*a 64/
%if %{build_fortran}
mv -f %{buildroot}%{_prefix}/lib64/libgfortran.*a 64/
%endif
mv -f %{buildroot}%{_prefix}/lib64/libgomp.*a 64/
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/lib64/libquadmath.*a 64/
%endif
ln -sf lib32/libstdc++.a libstdc++.a
ln -sf ../lib64/libstdc++.a 64/libstdc++.a
ln -sf lib32/libstdc++fs.a libstdc++fs.a
ln -sf ../lib64/libstdc++fs.a 64/libstdc++fs.a
ln -sf lib32/libstdc++_nonshared.a libstdc++_nonshared.a
ln -sf ../lib64/libstdc++_nonshared.a 64/libstdc++_nonshared.a
%if %{build_libquadmath}
ln -sf lib32/libquadmath.a libquadmath.a
ln -sf ../lib64/libquadmath.a 64/libquadmath.a
%endif
%if %{build_libitm}
ln -sf lib32/libitm.a libitm.a
ln -sf ../lib64/libitm.a 64/libitm.a
%endif
%if %{build_libatomic}
ln -sf lib32/libatomic.a libatomic.a
ln -sf ../lib64/libatomic.a 64/libatomic.a
%endif
%if %{build_libasan}
ln -sf lib32/libasan.a libasan.a
ln -sf ../lib64/libasan.a 64/libasan.a
ln -sf lib32/libasan_preinit.o libasan_preinit.o
ln -sf ../lib64/libasan_preinit.o 64/libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf lib32/libubsan.a libubsan.a
ln -sf ../lib64/libubsan.a 64/libubsan.a
%endif
%if %{build_libcilkrts}
ln -sf lib32/libcilkrts.a libcilkrts.a
ln -sf ../lib64/libcilkrts.a 64/libcilkrts.a
%endif
%if %{build_libmpx}
ln -sf lib32/libmpx.a libmpx.a
ln -sf ../lib64/libmpx.a 64/libmpx.a
ln -sf lib32/libmpxwrappers.a libmpxwrappers.a
ln -sf ../lib64/libmpxwrappers.a 64/libmpxwrappers.a
%endif
%endif
%ifarch %{multilib_64_archs}
mkdir -p 32
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libstdc++.so.6 -lstdc++_nonshared )' > 32/libstdc++.so
%if %{build_fortran}
rm -f 32/libgfortran.so
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat2}
INPUT ( -lgfortran_nonshared %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libgfortran.so.3 AS_NEEDED ( -ldl ) )' > 32/libgfortran.so
%endif
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libgomp.so.1 )' > 32/libgomp.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{_prefix}/lib/libgccjit.so.0 )' > 32/libgccjit.so
%if %{build_libquadmath}
rm -f 32/libquadmath.so
echo '/* GNU ld script */
%{oformat2}
%if 0%{!?scl:1}
INPUT ( %{_prefix}/lib/libquadmath.so.0 )' > 32/libquadmath.so
%else
%if 0%{?rhel} >= 7
INPUT ( %{_root_prefix}/lib/libquadmath.so.0 )' > 32/libquadmath.so
%else
INPUT ( libquadmath.a )' > 32/libquadmath.so
%endif
%endif
%endif
%if %{build_libitm}
rm -f 32/libitm.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libitm.so.1 )' > 32/libitm.so
%endif
%if %{build_libatomic}
rm -f 32/libatomic.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libatomic.so.1 )' > 32/libatomic.so
%endif
%if %{build_libasan}
rm -f 32/libasan.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libasan.so.3 )' > 32/libasan.so
%endif
%if %{build_libubsan}
rm -f 32/libubsan.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libubsan.so.0 )' > 32/libubsan.so
%endif
%if %{build_libcilkrts}
rm -f 32/libcilkrts.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libcilkrts.so.5 )' > 32/libcilkrts.so
%endif
%if %{build_libmpx}
rm -f 32/libmpx.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libmpx.so.2 )' > 32/libmpx.so
rm -f 32/libmpxwrappers.so
echo '/* GNU ld script */
%{oformat2}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/libmpxwrappers.so.2 )' > 32/libmpxwrappers.so
%endif
mv -f %{buildroot}%{_prefix}/lib/libsupc++.*a 32/
%if %{build_fortran}
mv -f %{buildroot}%{_prefix}/lib/libgfortran.*a 32/
%endif
mv -f %{buildroot}%{_prefix}/lib/libgomp.*a 32/
%if %{build_libquadmath}
mv -f %{buildroot}%{_prefix}/lib/libquadmath.*a 32/
%endif
%endif
%ifarch sparc64 ppc64
ln -sf ../lib32/libstdc++.a 32/libstdc++.a
ln -sf lib64/libstdc++.a libstdc++.a
ln -sf ../lib32/libstdc++fs.a 32/libstdc++fs.a
ln -sf lib64/libstdc++fs.a libstdc++fs.a
ln -sf ../lib32/libstdc++_nonshared.a 32/libstdc++_nonshared.a
ln -sf lib64/libstdc++_nonshared.a libstdc++_nonshared.a
%if %{build_libquadmath}
ln -sf ../lib32/libquadmath.a 32/libquadmath.a
ln -sf lib64/libquadmath.a libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../lib32/libitm.a 32/libitm.a
ln -sf lib64/libitm.a libitm.a
%endif
%if %{build_libatomic}
ln -sf ../lib32/libatomic.a 32/libatomic.a
ln -sf lib64/libatomic.a libatomic.a
%endif
%if %{build_libasan}
ln -sf ../lib32/libasan.a 32/libasan.a
ln -sf lib64/libasan.a libasan.a
ln -sf ../lib32/libasan_preinit.o 32/libasan_preinit.o
ln -sf lib64/libasan_preinit.o libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../lib32/libubsan.a 32/libubsan.a
ln -sf lib64/libubsan.a libubsan.a
%endif
%if %{build_libcilkrts}
ln -sf ../lib32/libcilkrts.a 32/libcilkrts.a
ln -sf lib64/libcilkrts.a libcilkrts.a
%endif
%if %{build_libmpx}
ln -sf ../lib32/libmpx.a 32/libmpx.a
ln -sf lib64/libmpx.a libmpx.a
ln -sf ../lib32/libmpxwrappers.a 32/libmpxwrappers.a
ln -sf lib64/libmpxwrappers.a libmpxwrappers.a
%endif
%else
%ifarch %{multilib_64_archs}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libstdc++.a 32/libstdc++.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libstdc++fs.a 32/libstdc++fs.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libstdc++_nonshared.a 32/libstdc++_nonshared.a
%if %{build_libquadmath}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libquadmath.a 32/libquadmath.a
%endif
%if %{build_libitm}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libitm.a 32/libitm.a
%endif
%if %{build_libatomic}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libatomic.a 32/libatomic.a
%endif
%if %{build_libasan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libasan.a 32/libasan.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libasan_preinit.o 32/libasan_preinit.o
%endif
%if %{build_libubsan}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libubsan.a 32/libubsan.a
%endif
%if %{build_libcilkrts}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libcilkrts.a 32/libcilkrts.a
%endif
%if %{build_libmpx}
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libmpx.a 32/libmpx.a
ln -sf ../../../%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}/%{gcc_version}/libmpxwrappers.a 32/libmpxwrappers.a
%endif
%endif
%endif

# If we are building a debug package then copy all of the static archives
# into the debug directory to keep them as unstripped copies.
%if 0%{?_enable_debug_packages}
mkdir -p $RPM_BUILD_ROOT%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
adirs="$FULLPATH"
if [ $FULLLPATH -ne $FULLPATH ]; then
  adirs="$adirs $FULLLPATH"
fi
for f in `find $adirs -maxdepth 1 -a \
		 \( -name libgfortran.a -o -name libgomp.a \
		    -o -name libgcc.a -o -name libgcc_eh.a -o -name libgcov.a \
		    -o -name libquadmath.a -o -name libitm.a \
		    -o -name libatomic.a -o -name libasan.a \
		    -o -name libtsan.a -o -name libubsan.a \
		    -o -name liblsan.a -o -name libcilkrts.a \
		    -o -name libmpx.a -o -name libmpxwrappers.a \
		    -o -name libcc1.a -o -name libstdc++_nonshared.a \
		    -o -name libgfortran_nonshared.a -o -name libsupc++.a \
		    -o -name libstdc++.a -o -name libcaf_single.a \
		    -o -name libstdc++fs.a \) -a -type f`; do
  cp -a $f $RPM_BUILD_ROOT%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/lib/debug%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/
done
%endif

# Strip debug info from Fortran/ObjC/Java static libraries
strip -g `find . \( -name libgfortran.a  -o -name libgomp.a \
		    -o -name libgcc.a -o -name libgcov.a \
		    -o -name libquadmath.a -o -name libitm.a \
		    -o -name libatomic.a -o -name libasan.a \
		    -o -name libtsan.a -o -name libubsan.a \
		    -o -name liblsan.a -o -name libcilkrts.a \
		    -o -name libmpx.a -o -name libmpxwrappers.a \
		    -o -name libcc1.a \) -a -type f`
popd
%if %{build_fortran}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgfortran.so.3.*
%endif
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libgomp.so.1.*
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcc1.so.0.*
%if %{build_libquadmath}
%if 0%{!?scl:1}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libquadmath.so.0.*
%endif
%endif
%if %{build_libitm}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libitm.so.1.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libitm.so.1* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
mv %{buildroot}%{_infodir}/libitm.info* %{buildroot}%{_root_infodir}/
%endif
%endif
%if %{build_libatomic}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libatomic.so.1* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%endif
%endif
%if %{build_libasan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libasan.so.3.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libasan.so.3* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%endif
%endif
%if %{build_libtsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libtsan.so.0.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libtsan.so.0* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%endif
%endif
%if %{build_libubsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libubsan.so.0.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libubsan.so.0* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%endif
%endif
%if %{build_liblsan}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/liblsan.so.0.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/liblsan.so.0* %{buildroot}%{_root_prefix}/%{_lib}/
mkdir -p %{buildroot}%{_root_infodir}
%endif
%endif
%if %{build_libcilkrts}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libcilkrts.so.5.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libcilkrts.so.5* %{buildroot}%{_root_prefix}/%{_lib}/
%endif
%endif
%if %{build_libmpx}
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libmpx.so.2.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libmpx.so.2* %{buildroot}%{_root_prefix}/%{_lib}/
%endif
chmod 755 %{buildroot}%{_prefix}/%{_lib}/libmpxwrappers.so.2.*
%if 0%{?scl:1}
mkdir -p %{buildroot}%{_root_prefix}/%{_lib}/
mv %{buildroot}%{_prefix}/%{_lib}/libmpxwrappers.so.2* %{buildroot}%{_root_prefix}/%{_lib}/
%endif
%endif

mv $FULLPATH/include-fixed/syslimits.h $FULLPATH/include/syslimits.h
mv $FULLPATH/include-fixed/limits.h $FULLPATH/include/limits.h
for h in `find $FULLPATH/include -name \*.h`; do
  if grep -q 'It has been auto-edited by fixincludes from' $h; then
    rh=`grep -A2 'It has been auto-edited by fixincludes from' $h | tail -1 | sed 's|^.*"\(.*\)".*$|\1|'`
    diff -up $rh $h || :
    rm -f $h
  fi
done

cd ..

%if 0%{!?scl:1}
for i in %{buildroot}%{_prefix}/bin/{*gcc,*++,gcov,gfortran,gcc-ar,gcc-nm,gcc-ranlib}; do
  mv -f $i ${i}5
done
%endif

# Remove binaries we will not be including, so that they don't end up in
# gcc6-debuginfo
rm -f %{buildroot}%{_prefix}/%{_lib}/{libffi*,libiberty.a,libmudflap*,libstdc++*,libgfortran*}
%if 0%{?scl:1}
rm -f %{buildroot}%{_prefix}/%{_lib}/{libquadmath*,libitm*,libatomic*,libasan*,libtsan*,libubsan*,liblsan*}
%else
%if 0%{rhel} >= 7
rm -f %{buildroot}%{_prefix}/%{_lib}/{libitm*,libatomic*}
%endif
%endif
rm -f %{buildroot}%{_prefix}/%{_lib}/libgomp*
rm -f $FULLEPATH/install-tools/{mkheaders,fixincl}
rm -f %{buildroot}%{_prefix}/lib/{32,64}/libiberty.a
rm -f %{buildroot}%{_prefix}/%{_lib}/libssp*
rm -f %{buildroot}%{_prefix}/%{_lib}/libvtv* || :
rm -f %{buildroot}/lib/cpp
rm -f %{buildroot}/%{_lib}/libgcc_s*
rm -f %{buildroot}%{_prefix}/bin/{f95,gccbug,gnatgcc*}
rm -f %{buildroot}%{_prefix}/bin/%{gcc_target_platform}-gfortran
%if 0%{!?scl:1}
rm -f %{buildroot}%{_prefix}/bin/{*c++*,cc,cpp}
%endif
rm -f %{buildroot}%{_prefix}/bin/%{_target_platform}-gfortran || :

%ifarch %{multilib_64_archs}
# Remove libraries for the other arch on multilib arches
rm -f %{buildroot}%{_prefix}/lib/lib*.so*
rm -f %{buildroot}%{_prefix}/lib/lib*.a
rm -f %{buildroot}/lib/libgcc_s*.so*
%else
%ifarch sparcv9 ppc
rm -f %{buildroot}%{_prefix}/lib64/lib*.so*
rm -f %{buildroot}%{_prefix}/lib64/lib*.a
rm -f %{buildroot}/lib64/libgcc_s*.so*
%endif
%endif

%ifnarch sparc64 ppc64
%ifarch %{multilib_64_archs}
cat <<\EOF > %{buildroot}%{_prefix}/bin/%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}-gcc-%{version}
#!/bin/sh
%ifarch s390x
exec %{gcc_target_platform}-gcc-%{version} -m31 "$@"
%else
exec %{gcc_target_platform}-gcc-%{version} -m32 "$@"
%endif
EOF
chmod 755 %{buildroot}%{_prefix}/bin/%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}-gcc-%{version}
%endif
%endif

# Help plugins find out nvra.
echo gcc-%{version}-%{release}.%{arch} > $FULLPATH/rpmver

%check
cd obj-%{gcc_target_platform}

%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}

# Test against the system libstdc++.so.6 + libstdc++_nonshared.a combo
mv %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so.6{,.not_here}
mv %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so{,.not_here}
ln -sf %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 \
  %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so.6
echo '/* GNU ld script
   Use the shared library, but some functions are only in
   the static library, so try that secondarily.  */
%{oformat}
INPUT ( %{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libstdc++.so.6 -lstdc++_nonshared )' \
  > %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++.so
cp -a %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared%{nonsharedver}.a \
  %{gcc_target_platform}/libstdc++-v3/src/.libs/libstdc++_nonshared.a

# run the tests.
make %{?_smp_mflags} -k check RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}'" || :
( LC_ALL=C ../contrib/test_summary -t || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}' > testresults
rm -rf gcc/testsuite.prev
mv gcc/testsuite{,.prev}
rm -f gcc/site.exp
make %{?_smp_mflags} -C gcc -k check-gcc check-g++ ALT_CC_UNDER_TEST=gcc ALT_CXX_UNDER_TEST=g++ RUNTESTFLAGS="--target_board=unix/'{,-fstack-protector}' compat.exp struct-layout-1.exp" || :
mv gcc/testsuite/gcc/gcc.sum{,.sent}
mv gcc/testsuite/g++/g++.sum{,.sent}
( LC_ALL=C ../contrib/test_summary -o -t || : ) 2>&1 | sed -n '/^cat.*EOF/,/^EOF/{/^cat.*EOF/d;/^EOF/d;/^LAST_UPDATED:/d;p;}' > testresults2
rm -rf gcc/testsuite.compat
mv gcc/testsuite{,.compat}
mv gcc/testsuite{.prev,}
echo ====================TESTING=========================
cat testresults
echo ===`gcc --version | head -1` compatibility tests====
cat testresults2
echo ====================TESTING END=====================
mkdir testlogs-%{_target_platform}-%{version}-%{release}
for i in `find . -name \*.log | grep -F testsuite/ | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/ || :
done
for i in `find gcc/testsuite.compat -name \*.log | grep -v 'config.log\|acats.*/tests/'`; do
  ln $i testlogs-%{_target_platform}-%{version}-%{release}/`basename $i`.compat || :
done
tar cf - testlogs-%{_target_platform}-%{version}-%{release} | bzip2 -9c \
  | uuencode testlogs-%{_target_platform}.tar.bz2 || :
rm -rf testlogs-%{_target_platform}-%{version}-%{release}

%clean
rm -rf %{buildroot}

%if 0%{?scl:1}
%post gfortran
if [ -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi

%preun gfortran
if [ $1 = 0 -a -f %{_infodir}/gfortran.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/gfortran.info.gz || :
fi
%endif

%post gdb-plugin -p /sbin/ldconfig

%postun gdb-plugin -p /sbin/ldconfig

%post -n %{?scl_prefix}libgccjit -p /sbin/ldconfig

%postun -n %{?scl_prefix}libgccjit -p /sbin/ldconfig

%post -n %{?scl_prefix}libgccjit-docs
if [ -f %{_infodir}/libgccjit.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libgccjit.info.gz || :
fi

%preun -n %{?scl_prefix}libgccjit-docs
if [ $1 = 0 -a -f %{_infodir}/libgccjit.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libgccjit.info.gz || :
fi

%post -n %{?scl_prefix}libquadmath
/sbin/ldconfig
if [ -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%preun -n %{?scl_prefix}libquadmath
if [ $1 = 0 -a -f %{_infodir}/libquadmath.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{_infodir} %{_infodir}/libquadmath.info.gz || :
fi

%postun -n %{?scl_prefix}libquadmath -p /sbin/ldconfig

%post -n libitm
/sbin/ldconfig
if [ -f %{?scl:%{_root_infodir}}%{!?scl:%{_infodir}}/libitm.info.gz ]; then
  /sbin/install-info \
    --info-dir=%{?scl:%{_root_infodir}}%{!?scl:%{_infodir}} %{?scl:%{_root_infodir}}%{!?scl:%{_infodir}}/libitm.info.gz || :
fi

%preun -n libitm
if [ $1 = 0 -a -f %{?scl:%{_root_infodir}}%{!?scl:%{_infodir}}/libitm.info.gz ]; then
  /sbin/install-info --delete \
    --info-dir=%{?scl:%{_root_infodir}}%{!?scl:%{_infodir}} %{?scl:%{_root_infodir}}%{!?scl:%{_infodir}}/libitm.info.gz || :
fi

%postun -n libitm -p /sbin/ldconfig

%post -n libatomic -p /sbin/ldconfig

%postun -n libatomic -p /sbin/ldconfig

%post -n libasan3 -p /sbin/ldconfig

%postun -n libasan3 -p /sbin/ldconfig

%post -n libtsan -p /sbin/ldconfig

%postun -n libtsan -p /sbin/ldconfig

%post -n libubsan -p /sbin/ldconfig

%postun -n libubsan -p /sbin/ldconfig

%post -n liblsan -p /sbin/ldconfig

%postun -n liblsan -p /sbin/ldconfig

%post -n libcilkrts -p /sbin/ldconfig

%postun -n libcilkrts -p /sbin/ldconfig

%post -n libmpx -p /sbin/ldconfig

%postun -n libmpx -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_prefix}/bin/gcc%{!?scl:5}
%{_prefix}/bin/gcov%{!?scl:5}
%{_prefix}/bin/gcov-tool%{!?scl:5}
%{_prefix}/bin/gcc-ar%{!?scl:5}
%{_prefix}/bin/gcc-nm%{!?scl:5}
%{_prefix}/bin/gcc-ranlib%{!?scl:5}
%ifarch ppc
%{_prefix}/bin/%{_target_platform}-gcc%{!?scl:5}
%endif
%ifarch sparc64 sparcv9
%{_prefix}/bin/sparc-%{_vendor}-%{_target_os}%{?_gnu}-gcc%{!?scl:5}
%endif
%ifarch ppc64
%{_prefix}/bin/ppc-%{_vendor}-%{_target_os}%{?_gnu}-gcc%{!?scl:5}
%endif
%{_prefix}/bin/%{gcc_target_platform}-gcc%{!?scl:5}
%{_prefix}/bin/%{gcc_target_platform}-gcc-%{version}
%ifnarch sparc64 ppc64
%ifarch %{multilib_64_archs}
%{_prefix}/bin/%{multilib_32_arch}-%{_vendor}-%{_target_os}%{?_gnu}-gcc-%{version}
%endif
%endif
%if 0%{?scl:1}
%{_prefix}/bin/cc
%{_prefix}/bin/cpp
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/cpp.1*
%{_mandir}/man1/gcov.1*
%{_infodir}/gcc*
%{_infodir}/cpp*
%endif
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/rpmver
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stddef.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdfix.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/varargs.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/float.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/limits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdbool.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/iso646.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/syslimits.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/omp.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/openacc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdint-gcc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdalign.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdnoreturn.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/stdatomic.h
%ifarch %{ix86} x86_64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/emmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ammintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/smmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/nmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/wmmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/immintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/x86intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fma4intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xopintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lwpintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/popcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/tbmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia32intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/bmi2intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/f16cintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/lzcntintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rtmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xtestintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/adxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/prfchwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/rdseedintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/fxsrintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsaveoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512cdintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512erintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512fintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512pfintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/shaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm_malloc.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mm3dnow.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cpuid.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cross-stdarg.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512bwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512dqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512ifmaintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512ifmavlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vbmiintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vbmivlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vlbwintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vldqintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/avx512vlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/clflushoptintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/clwbintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mwaitxintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsavecintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/xsavesintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/clzerointrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/pkuintrin.h
%endif
%ifarch ia64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ia64intrin.h
%endif
%ifarch ppc ppc64 ppc64le ppc64p7
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppc-asm.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/altivec.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spe.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/paired.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/ppu_intrinsics.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/si2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/spu2vmx.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/vec_types.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmxlintrin.h
%endif
%ifarch %{arm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/unwind-arm-common.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/mmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_acle.h
%endif
%ifarch aarch64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_neon.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/arm_acle.h
%endif
%ifarch sparc sparcv9 sparc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/visintrin.h
%endif
%ifarch s390 s390x
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/s390intrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/htmxlintrin.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/vecintrin.h
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/cilk
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcilkrts.spec
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpx.spec
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/sanitizer
%endif
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto1
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/lto-wrapper
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/liblto_plugin.so*
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/collect2
%if 0%{?scl:1}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/ar
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/as
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/ld
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/ld.bfd
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/ld.gold
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/nm
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/ranlib
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/strip
%endif
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgomp.so
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.spec
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsanitizer.spec
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%endif
%endif
%if %{build_isl}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libisl.so.*
%endif
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgccjit.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libubsan.so
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libcilkrts.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libcilkrts.so
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmpxwrappers.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libmpxwrappers.so
%endif
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/crt*.o
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcov.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_eh.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgcc_s.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgomp.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgccjit.so
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libasan_preinit.o
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libubsan.so
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libcilkrts.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libcilkrts.so
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmpxwrappers.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libmpxwrappers.so
%endif
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%if %{build_libquadmath}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%endif
%if %{build_libitm}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.so
%endif
%if %{build_libatomic}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.so
%endif
%if %{build_libasan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan_preinit.o
%endif
%if %{build_libtsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.so
%endif
%if %{build_libubsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libubsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libubsan.so
%endif
%if %{build_liblsan}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/liblsan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/liblsan.so
%endif
%if %{build_libcilkrts}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcilkrts.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcilkrts.so
%endif
%if %{build_libmpx}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpx.so
%endif
%endif
%doc gcc/README* rpm.doc/changelogs/gcc/ChangeLog* gcc/COPYING* COPYING.RUNTIME

%files c++
%defattr(-,root,root,-)
%{_prefix}/bin/%{gcc_target_platform}-g++%{!?scl:5}
%{_prefix}/bin/g++%{!?scl:5}
%if 0%{?scl:1}
%{_prefix}/bin/%{gcc_target_platform}-c++
%{_prefix}/bin/c++
%{_mandir}/man1/g++.1*
%endif
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/cc1plus
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libstdc++_nonshared.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libsupc++.a
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libstdc++_nonshared.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libsupc++.a
%endif
%ifarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%ifarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++_nonshared.a
%endif
%doc rpm.doc/changelogs/gcc/cp/ChangeLog*

%files -n %{?scl_prefix}libstdc++%{!?scl:5}-devel
%defattr(-,root,root,-)
%dir %{_prefix}/include/c++
%dir %{_prefix}/include/c++/%{gcc_version}
%{_prefix}/include/c++/%{gcc_version}/[^gjos]*
%{_prefix}/include/c++/%{gcc_version}/os*
%{_prefix}/include/c++/%{gcc_version}/s[^u]*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libstdc++_nonshared.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libstdc++_nonshared.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++fs.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++_nonshared.a
%endif
%ifnarch sparcv9 ppc %{multilib_64_archs}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libstdc++.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libsupc++.a
%endif
%doc rpm.doc/changelogs/libstdc++-v3/ChangeLog* libstdc++-v3/README*

%if %{build_libstdcxx_docs}
%files -n %{?scl_prefix}libstdc++%{!?scl:5}-docs
%defattr(-,root,root)
%{_mandir}/man3/*
%doc rpm.doc/libstdc++-v3/html
%endif

%if %{build_fortran}
%files gfortran
%defattr(-,root,root,-)
%{_prefix}/bin/gfortran%{!?scl:5}
%if 0%{?scl:1}
%{_mandir}/man1/gfortran.1*
%{_infodir}/gfortran*
%endif
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/omp_lib_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/openacc.f90
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/openacc.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/openacc_kinds.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/openacc_lib.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/ieee_arithmetic.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/ieee_exceptions.mod
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/finclude/ieee_features.mod
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/f951
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.spec
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgfortran_nonshared.a
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/libgfortran_nonshared.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/64/finclude
%endif
%ifarch %{multilib_64_archs}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libcaf_single.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/libgfortran_nonshared.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/32/finclude
%endif
%doc rpm.doc/gfortran/*
%endif

%if %{build_libquadmath}
%if 0%{!?scl:1}
%files -n %{?scl_prefix}libquadmath
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libquadmath.so.0*
%{_infodir}/libquadmath.info*
%doc rpm.doc/libquadmath/COPYING*
%endif

%files -n %{?scl_prefix}libquadmath-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath.h
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/quadmath_weak.h
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libquadmath.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libquadmath.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libquadmath.so
%endif
%doc rpm.doc/libquadmath/ChangeLog*
%endif

%if %{build_libitm}
%if 0%{?rhel} < 7
%files -n libitm
%defattr(-,root,root,-)
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libitm.so.1*
%{?scl:%{_root_infodir}}%{!?scl:%{_infodir}}/libitm.info*
%endif

%files -n %{?scl_prefix}libitm-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libitm.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libitm.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libitm.a
%endif
%doc rpm.doc/libitm/ChangeLog*
%endif

%if %{build_libatomic}
%if 0%{?rhel} < 7
%files -n libatomic
%defattr(-,root,root,-)
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libatomic.so.1*
%endif

%files -n %{?scl_prefix}libatomic-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libatomic.a
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libatomic.a
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libatomic.a
%endif
%doc rpm.doc/changelogs/libatomic/ChangeLog*
%endif

%if %{build_libasan}
%files -n libasan3
%defattr(-,root,root,-)
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libasan.so.3*

%files -n %{?scl_prefix}libasan-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%ifarch sparcv9 ppc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib32/libasan_preinit.o
%endif
%ifarch sparc64 ppc64
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/lib64/libasan_preinit.o
%endif
%ifnarch sparcv9 sparc64 ppc ppc64
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libasan_preinit.o
%endif
%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%if %{build_libtsan}
%files -n libtsan
%defattr(-,root,root,-)
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libtsan.so.0*

%files -n %{?scl_prefix}libtsan-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libtsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%if %{build_libubsan}
%files -n libubsan
%defattr(-,root,root,-)
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libubsan.so.0*

%files -n %{?scl_prefix}libubsan-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libubsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libubsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%if %{build_liblsan}
%files -n liblsan
%defattr(-,root,root,-)
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/liblsan.so.0*

%files -n %{?scl_prefix}liblsan-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/liblsan.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/liblsan.a
%doc rpm.doc/changelogs/libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%endif

%if %{build_libcilkrts}
%files -n libcilkrts
%defattr(-,root,root,-)
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libcilkrts.so.5*

%files -n %{?scl_prefix}libcilkrts-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcilkrts.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libcilkrts.a
%doc rpm.doc/changelogs/libcilkrts/ChangeLog* libcilkrts/README
%endif

%if %{build_libmpx}
%files -n libmpx
%defattr(-,root,root,-)
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libmpx.so.2*
%{?scl:%{_root_prefix}}%{!?scl:%{_prefix}}/%{_lib}/libmpxwrappers.so.2*

%files -n %{?scl_prefix}libmpx-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpx.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpx.a
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpxwrappers.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libmpxwrappers.a
%doc rpm.doc/changelogs/libmpx/ChangeLog*
%endif

%files -n %{?scl_prefix}libgccjit
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libgccjit.so*
%doc rpm.doc/changelogs/gcc/jit/ChangeLog*

%files -n %{?scl_prefix}libgccjit-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/libgccjit.so
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/include/libgccjit*.h

%files -n %{?scl_prefix}libgccjit-docs
%defattr(-,root,root,-)
%{_infodir}/libgccjit.info*
%doc rpm.doc/libgccjit-devel/*
%doc gcc/jit/docs/examples

%files plugin-devel
%defattr(-,root,root,-)
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/gtype.state
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/include
%dir %{_prefix}/libexec/gcc
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}
%dir %{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}
%{_prefix}/libexec/gcc/%{gcc_target_platform}/%{gcc_version}/plugin

%files gdb-plugin
%defattr(-,root,root,-)
%{_prefix}/%{_lib}/libcc1.so*
%dir %{_prefix}/lib/gcc
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}
%dir %{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin
%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_version}/plugin/libcc1plugin.so*
%doc rpm.doc/changelogs/libcc1/ChangeLog*

%changelog
* Mon Feb 20 2017 Marek Polacek <polacek@redhat.com> 6.3.1-3.1
- use "export" when setting LD_LIBRARY_PATH (#1421107)

* Thu Feb 16 2017 Jakub Jelinek  <jakub@redhat.com> 6.3.1-3
- update from Fedora 6.3.1-3
  - fix vec_xl and vec_xst altivec.h intrinsics (#1418397, PR target/79268)

* Tue Feb 14 2017 Marek Polacek <polacek@redhat.com> 6.3.1-2.3
- set LD_LIBRARY_PATH (#1421107)

* Thu Jan 19 2017 Jakub Jelinek  <jakub@redhat.com> 6.3.1-2.2
- update from Fedora 6.3.1-2
- some further libstdc++_nonshared.a fixes for ppc, ppc64, ppc64le, s390
  and s390x

* Thu Oct 20 2016 Marek Polacek <polacek@redhat.com> 6.2.1-3.1
- rename libasan2 to libasan3 (#1386146)
- update old references to GCC 5

* Fri Oct  7 2016 Marek Polacek <polacek@redhat.com> 6.2.1-3
- add arm_neon.h and arm_acle.h intrinsic headers on aarch64 (#1382733)

* Fri Sep 16 2016 Jakub Jelinek <jakub@redhat.com> 6.2.1-2
- update from Fedora 6.2.1-2

* Thu Sep  1 2016 Jakub Jelinek <jakub@redhat.com> 6.2.1-1
- update from Fedora 6.2.1-1

* Thu Aug 18 2016 Jakub Jelinek <jakub@redhat.com> 6.1.1-6
- update from Fedora 6.1.1-6
- reenable tsan on aarch64

* Wed Aug 10 2016 Jakub Jelinek <jakub@redhat.com> 6.1.1-5
- update from Fedora 6.1.1-5
- make sure to use DTS strip and objdump during brp scripts (#1365531,
  #1365602)
- use DTS binutils even on RHEL7

* Mon Aug  1 2016 Marek Polacek <polacek@redhat.com> 6.1.1-4.1
- disable tsan on aarch64 (#1361770)

* Thu Jul 21 2016 Jakub Jelinek <jakub@redhat.com> 6.1.1-4
- new package
