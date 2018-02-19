%define enable_native_atlas 0

Name:           atlas
Version:        3.10.1
%if "%{?enable_native_atlas}" != "0"
%define dist .native
%endif
Release:        12%{?dist}
Summary:        Automatically Tuned Linear Algebra Software

Group:          System Environment/Libraries
License:        BSD
URL:            http://math-atlas.sourceforge.net/
Source0:        http://downloads.sourceforge.net/math-atlas/%{name}%{version}.tar.bz2
Source1:        PPRO32.tgz
#Source2:        K7323DNow.tgz
Source3:        README.dist
#Source4:        USII64.tgz                                              
#Source5:        USII32.tgz                                              
#Source6:        IBMz1032.tgz
#Source7:        IBMz1064.tgz
#Source8:        IBMz19632.tgz
#Source9:        IBMz19664.tgz
Source10: 	lapack-3.4.2-clean.tgz
#archdefs taken from debian:
Source11: 	POWER332.tar.bz2
Source12: 	IBMz932.tar.bz2
#Source13: 	IBMz964.tar.bz2
#upstream arm uses softfp abi, fedora arm uses hard
Source14: 	ARMv732NEON.tar.bz2

Patch1:         atlas-s390port.patch
Patch2:		atlas-fedora-arm.patch
# Properly pass -melf_* to the linker with -Wl, fixes FTBFS bug 817552
# https://sourceforge.net/tracker/?func=detail&atid=379484&aid=3555789&group_id=23725
Patch3:		atlas-melf.patch
Patch4:		atlas-throttling.patch

#credits Lukas Slebodnik
Patch5:		atlas-shared_libraries.patch

Patch6:		atlas-affinity.patch

Patch7:		atlas-aarch64port.patch
Patch8:		atlas-genparse.patch

Patch9:		atlas-memleak.patch
# ppc64le patches
Patch95:	initialize_malloc_memory.invtrsm.wms.oct23.patch
Patch96:	xlf.command.not.found.patch
Patch98:	getdoublearr.stripwhite.patch
Patch99:	ppc64le-remove-vsx.patch
Patch100:	ppc64le-abiv2.patch
Patch110:	p8-mem-barrier.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc-gfortran

%ifarch x86_64
Obsoletes:      atlas-sse3 < 3.10
%endif

%ifarch %{ix86}
Obsoletes:      atlas-3dnow < 3.10
Obsoletes:      atlas-sse < 3.10
%endif

%ifarch s390 s390x
Obsoletes:      atlas-z10 < 3.10
Obsoletes:      atlas-z196 < 3.10
%endif


%description
The ATLAS (Automatically Tuned Linear Algebra Software) project is an
ongoing research effort focusing on applying empirical techniques in
order to provide portable performance. At present, it provides C and
Fortran77 interfaces to a portably efficient BLAS implementation, as
well as a few routines from LAPACK.

The performance improvements in ATLAS are obtained largely via
compile-time optimizations and tend to be specific to a given hardware
configuration. In order to package ATLAS some compromises
are necessary so that good performance can be obtained on a variety
of hardware. This set of ATLAS binary packages is therefore not
necessarily optimal for any specific hardware configuration.  However,
the source package can be used to compile customized ATLAS packages;
see the documentation for information.

%package devel
Summary:        Development libraries for ATLAS
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Obsoletes:	%name-header <= %version-%release
Requires(posttrans):	chkconfig
Requires(preun):	chkconfig

%description devel
This package contains the libraries and headers for development
with ATLAS (Automatically Tuned Linear Algebra Software).

%package static
Summary:        Static libraries for ATLAS
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}
Requires(posttrans):	chkconfig
Requires(preun):	chkconfig

%description static
This package contains static version of ATLAS (Automatically Tuned
Linear Algebra Software).


%define types base

%if "%{?enable_native_atlas}" == "0"
############## Subpackages for architecture extensions #################
#
%ifarch x86_64
%define types base
# sse3

#package sse3
#Summary:        ATLAS libraries for SSE3 extensions
#Group:          System Environment/Libraries

#description sse3
#This package contains the ATLAS (Automatically Tuned Linear Algebra
#Software) libraries compiled with optimizations for the SSE3
#extensions to the x86_64 architecture. The base ATLAS builds for the
#x86_64 architecture are made for the SSE2 extensions.

#package sse3-devel
#Summary:        Development libraries for ATLAS with SSE3 extensions
#Group:          Development/Libraries
#Requires:       %{name}-sse3 = %{version}-%{release}
#Obsoletes:	%name-header <= %version-%release
#Requires(posttrans):	chkconfig
#Requires(preun):	chkconfig

#description sse3-devel
#This package contains shared and static versions of the ATLAS
#(Automatically Tuned Linear Algebra Software) libraries compiled with
#optimizations for the SSE3 extensions to the x86_64 architecture.

%endif

%ifarch %{ix86}
%define types base sse2 sse3

%package sse2
Summary:        ATLAS libraries for SSE2 extensions
Group:          System Environment/Libraries

%description sse2
This package contains ATLAS (Automatically Tuned Linear Algebra Software)
shared libraries compiled with optimizations for the SSE2
extensions to the ix86 architecture. ATLAS builds with
SSE(1) and SSE3 extensions also exist.

%package sse2-devel
Summary:        Development libraries for ATLAS with SSE2 extensions
Group:          Development/Libraries
Requires:       %{name}-sse2 = %{version}-%{release}
Obsoletes:	%name-header <= %version-%release
Requires(posttrans):	chkconfig
Requires(preun):	chkconfig

%description sse2-devel
This package contains ATLAS (Automatically Tuned Linear Algebra Software)
shared libraries compiled with optimizations for the SSE2 extensions to the 
ix86 architecture.

%package sse2-static
Summary:        Static libraries for ATLAS with SSE2 extensions
Group:          Development/Libraries
Requires:       %{name}-sse2-devel = %{version}-%{release}
Requires(posttrans):	chkconfig
Requires(preun):	chkconfig

%description sse2-static
This package contains ATLAS (Automatically Tuned Linear Algebra Software)
static libraries compiled with optimizations for the SSE2 extensions to the 
ix86 architecture.


%package sse3
Summary:        ATLAS libraries for SSE3 extensions
Group:          System Environment/Libraries

%description sse3
This package contains the ATLAS (Automatically Tuned Linear Algebra
Software) libraries compiled with optimizations for the SSE3.
ATLAS builds with SSE(1) and SSE2 extensions also exist.

%package sse3-devel
Summary:        Development libraries for ATLAS with SSE3 extensions
Group:          Development/Libraries
Requires:       %{name}-sse3 = %{version}-%{release}
Obsoletes:	%name-header <= %version-%release
Requires(posttrans):	chkconfig
Requires(preun):	chkconfig

%description sse3-devel
This package contains ATLAS (Automatically Tuned Linear Algebra Software)
shared libraries compiled with optimizations for the SSE3 extensions to the ix86 architecture.

%package sse3-static
Summary:        Static libraries for ATLAS with SSE2 extensions
Group:          Development/Libraries
Requires:       %{name}-sse2-devel = %{version}-%{release}
Requires(posttrans):	chkconfig
Requires(preun):	chkconfig

%description sse3-static
This package contains ATLAS (Automatically Tuned Linear Algebra Software)
static libraries compiled with optimizations for the SSE3 extensions to the 
ix86 architecture.

%endif

%ifarch s390 s390x
%define types base 
#z196
#z10

#%package z196
#Summary:        ATLAS libraries for z196
#Group:          System Environment/Libraries
#
#%description z196
#This package contains the ATLAS (Automatically Tuned Linear Algebra
#Software) libraries compiled with optimizations for the z196.
#
#%package z196-devel
#Summary:        Development libraries for ATLAS for z196
#Group:          Development/Libraries
#Requires:       %{name}-z196 = %{version}-%{release}
#Obsoletes:	%name-header <= %version-%release
#Requires(posttrans):	chkconfig
#Requires(preun):	chkconfig
#
#%description z196-devel
#This package contains headers and shared versions of the ATLAS
#(Automatically Tuned Linear Algebra Software) libraries compiled with
#optimizations for the z196 architecture.

#%package z196-static
#Summary:        Static libraries for ATLAS
#Group:          Development/Libraries
#Requires:       %{name}-devel = %{version}-%{release}
#Requires(posttrans):	chkconfig
#Requires(preun):	chkconfig

#%description z196-static
#This package contains static version of ATLAS (Automatically Tuned
#Linear Algebra Software) for the z196 architecture.


#%package z10
#Summary:        ATLAS libraries for z10
#Group:          System Environment/Libraries
#
#%description z10
#This package contains the ATLAS (Automatically Tuned Linear Algebra
#Software) libraries compiled with optimizations for the z10.
#
#%package z10-devel
#Summary:        Development libraries for ATLAS for z10
#Group:          Development/Libraries
#Requires:       %{name}-z10 = %{version}-%{release}
#Obsoletes:	%name-header <= %version-%release
#Requires(posttrans):	chkconfig
#Requires(preun):	chkconfig
#
#%description z10-devel
#This package contains headers and shared versions of the ATLAS
#(Automatically Tuned Linear Algebra Software) libraries compiled with
#optimizations for the z10 architecture.
#
#%package z10-static
#Summary:        Static libraries for ATLAS
#Group:          Development/Libraries
#Requires:       %{name}-devel = %{version}-%{release}
#Requires(posttrans):	chkconfig
#Requires(preun):	chkconfig
#
#%description z10-static
#This package contains static version of ATLAS (Automatically Tuned
#Linear Algebra Software) for the z10 architecture.


%endif
%endif

%ifarch %{arm}
#beware - arch constant can change between releases
%define arch_option -A 46 
%define threads_option -t 2
%global armflags -mfpu=neon -mfloat-abi=hard
%global mode %{nil}
%else
%global mode -b %{__isa_bits}
%global armflags %{nil}
%if "%{?enable_native_atlas}" == "0"
%define threads_option -t 4
%endif
%endif

%prep
%setup -q -n ATLAS
#patch0 -p0 -b .shared
%ifarch s390 s390x
%patch1 -p1 -b .s390
%endif
#arm patch not applicable, probably not needed
#%ifarch %{arm}
#%patch2 -p0 -b .arm
#%endif
%patch3 -p1 -b .melf
%patch4 -p1 -b .thrott
%patch5 -p2 -b .sharedlib
#affinity crashes with fewer processors than the builder but increases performance of locally builded library
%if "%{?enable_native_atlas}" == "0"
%patch6 -p1 -b .affinity
%endif
#%patch6 -p1 -b .m32
%ifarch aarch64
%patch7 -p1 -b .aarch64
%endif
%patch8 -p1 -b .genparse
%patch9 -p1 -b .memleak
cp %{SOURCE1} CONFIG/ARCHS/
#cp %{SOURCE2} CONFIG/ARCHS/
cp %{SOURCE3} doc
cp %{SOURCE11} CONFIG/ARCHS/
cp %{SOURCE12} CONFIG/ARCHS/
#cp %{SOURCE13} CONFIG/ARCHS/

cp %{SOURCE14} CONFIG/ARCHS/
#cp %{SOURCE8} CONFIG/ARCHS/
#cp %{SOURCE9} CONFIG/ARCHS/

%ifarch ppc ppc64
%patch99 -p2
#%patch98 -p2
#%patch95 -p2
#%patch100 -p2
%patch110 -p1
%endif

%ifarch ppc64le
%patch99 -p2
%patch98 -p2
%patch96 -p2
%patch95 -p2
%patch100 -p2
%patch110 -p1
%endif

%build

for type in %{types}; do
	if [ "$type" = "base" ]; then
		libname=atlas
		%define pr_base %(echo $((%{__isa_bits}+0)))
	else
		libname=atlas-${type}
	fi

	mkdir -p %{_arch}_${type}
	pushd %{_arch}_${type}
	../configure  %{mode} %{?threads_option} %{?arch_option} -D c -DWALL -Fa alg '%{armflags} -g -fstack-protector-strong -Wa,--noexecstack -fPIC'\
	--prefix=%{buildroot}%{_prefix}			\
	--incdir=%{buildroot}%{_includedir}		\
	--libdir=%{buildroot}%{_libdir}/${libname}	\
	--with-netlib-lapack-tarfile=%{SOURCE10}

sed -i 's#F77FLAGS =\(.*\)#F77FLAGS=\1 -frecursive#' Make.inc

%if "%{?enable_native_atlas}" == "0"
%ifarch x86_64
	if [ "$type" = "base" ]; then
#		sed -i 's#ARCH =.*#ARCH = HAMMER64SSE2#' Make.inc
#		sed -i 's#ARCH =.*#ARCH = HAMMER64SSE3#' Make.inc
		sed -i 's#ARCH =.*#ARCH = P4E64SSE3#' Make.inc
#		sed -i 's#-DATL_SSE3##' Make.inc
		sed -i 's#-DATL_AVX\b##' Make.inc
#		sed -i 's#-msse3#-msse2#' Make.inc
		sed -i 's#-mavx\b#-msse3#' Make.inc
		echo 'base makefile edited'
#		sed -i 's#PMAKE = $(MAKE) .*#PMAKE = $(MAKE) -j 1#' Make.inc
	elif [ "$type" = "sse3" ]; then
#		sed -i 's#ARCH =.*#ARCH = Corei264AVX#' Make.inc
#		sed -i 's#PMAKE = $(MAKE) .*#PMAKE = $(MAKE) -j 1#' Make.inc
		sed -i 's#-DATL_AVX\b##' Make.inc
		sed -i 's#-DATL_SSE2##' Make.inc
		sed -i 's#-mavx\b#-msse2#' Make.inc
		sed -i 's#-msse3#-msse2#' Make.inc
		echo 'sse makefile edited'
		%define pr_sse3 %(echo $((%{__isa_bits}+4)))
	fi
%endif

%ifarch %{ix86}
	if [ "$type" = "base" ]; then
		sed -i 's#ARCH =.*#ARCH = PPRO32#' Make.inc
		#sed -i 's#-DATL_SSE3 -DATL_SSE2 -DATL_SSE1##' Make.inc
		sed -i 's#-DATL_SSE3##' Make.inc
		sed -i 's#-DATL_SSE2##' Make.inc
		sed -i 's#-DATL_SSE1##' Make.inc  
		sed -i 's#-mfpmath=sse -msse3#-mfpmath=387#' Make.inc 
	elif [ "$type" = "sse" ]; then
		sed -i 's#ARCH =.*#ARCH = PIII32SSE1#' Make.inc
		sed -i 's#-DATL_SSE3#-DATL_SSE1#' Make.inc 
		sed -i 's#-msse3#-msse#' Make.inc 
		%define pr_sse %(echo $((%{__isa_bits}+2)))
	elif [ "$type" = "sse2" ]; then
#		sed -i 's#ARCH =.*#ARCH = P432SSE2#' Make.inc
		sed -i 's#ARCH =.*#ARCH = x86SSE232SSE2#' Make.inc
		sed -i 's#-DATL_SSE3#-DATL_SSE2#' Make.inc 
		sed -i 's#-msse3#-msse2#' Make.inc 
		%define pr_sse2 %(echo $((%{__isa_bits}+3)))
	elif [ "$type" = "sse3" ]; then
		sed -i 's#ARCH =.*#ARCH = P4E32SSE3#' Make.inc
		%define pr_sse3 %(echo $((%{__isa_bits}+4)))
	fi
%endif

%ifarch s390 s390x
	if [ "$type" = "base" ]; then
		%ifarch s390x 
			sed -i 's#ARCH =.*#ARCH = IBMz19664#' Make.inc
                %endif
		%ifarch s390 
			sed -i 's#ARCH =.*#ARCH = IBMz932#' Make.inc
                %endif
		#sed -i 's#-march=z196#-march=z10 -mtune=z196#' Make.inc
		sed -i 's#-march=z10#-march=z196#' Make.inc
		sed -i 's#-march=z9-109#-march=z196#' Make.inc
		sed -i 's#-DATL_ARCH_IBMz10#-DATL_ARCH_IBMz196#' Make.inc
		sed -i 's#-DATL_ARCH_IBMz9#-DATL_ARCH_IBMz196#' Make.inc
		%define pr_z196 %(echo $((%{__isa_bits}+2)))
	fi
%endif

%ifarch ppc
	sed -i 's#ARCH =.*#ARCH = POWER332#' Make.inc
	sed -i 's#-DATL_ARCH_POWER7#-DATL_ARCH_POWER3#g' Make.inc
	sed -i 's#power7#power3#g' Make.inc
	sed -i 's#-DATL_VSX\b##g' Make.inc
	sed -i 's#-mvsx\b##g' Make.inc
	sed -i 's#-DATL_AltiVec##g' Make.inc
	sed -i 's#-m64#-m32#g' Make.inc
%endif

%ifarch ppc64le
	sed -i 's#-mvsx##g' Make.inc
	sed -i 's#-DATL_VSX\b##g' Make.inc
	sed -i 's#-DATL_AltiVec\b##g' Make.inc
	sed -i 's#-maltivec##g' Make.inc
	sed -i 's#ARCH =.*#ARCH = POWER464#' Make.inc
%endif

%endif
	make build
	cd lib
	make shared
	make ptshared
	popd
done

%install 	
for type in %{types}; do
	pushd %{_arch}_${type}
	make DESTDIR=%{buildroot} install
        mv %{buildroot}%{_includedir}/atlas %{buildroot}%{_includedir}/atlas-%{_arch}-${type}
	if [ "$type" = "base" ]; then
		cp -pr lib/*.so* %{buildroot}%{_libdir}/atlas/
		rm -f %{buildroot}%{_libdir}/atlas/*.a
		cp -pr lib/libatlas.a %{buildroot}%{_libdir}/atlas/
	else
		cp -pr lib/*.so* %{buildroot}%{_libdir}/atlas-${type}/
		rm -f %{buildroot}%{_libdir}/atlas-${type}/*.a
		cp -pr lib/libatlas.a %{buildroot}%{_libdir}/atlas-${type}/
	fi
	popd

	mkdir -p %{buildroot}/etc/ld.so.conf.d
	if [ "$type" = "base" ]; then
		echo "%{_libdir}/atlas"		\
		> %{buildroot}/etc/ld.so.conf.d/atlas-%{_arch}.conf
	else
		echo "%{_libdir}/atlas-${type}"	\
		> %{buildroot}/etc/ld.so.conf.d/atlas-%{_arch}-${type}.conf
	fi
done
mkdir -p %{buildroot}%{_includedir}/atlas


%check
%ifnarch s390 aarch64
for type in %{types}; do
	pushd %{_arch}_${type}
	make check ptcheck
	popd
done
%endif


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%posttrans devel
if [ $1 -eq 0 ] ; then
/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
		%{_includedir}/atlas-%{_arch}-base %{pr_base}
fi

%preun devel
if [ $1 -ge 0 ] ; then
/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-base
fi

%if "%{?enable_native_atlas}" == "0"
#ifarch x86_64

#post -n atlas-sse3 -p /sbin/ldconfig

#postun -n atlas-sse3 -p /sbin/ldconfig

#posttrans sse3-devel
#if [ $1 -eq 0 ] ; then
#/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
#		%{_includedir}/atlas-%{_arch}-sse3  %{pr_sse3}
#fi

#preun sse3-devel
#if [ $1 -ge 0 ] ; then
#/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-sse3
#fi

#endif

%ifarch %{ix86}
#%%post -n atlas-3dnow -p /sbin/ldconfig

#%%postun -n atlas-3dnow -p /sbin/ldconfig

#%%posttrans 3dnow-devel
#if [ $1 -eq 0 ] ; then
#/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
#		%{_includedir}/atlas-%{_arch}-3dnow  %{pr_3dnow}
#fi

#%%preun 3dnow-devel
#if [ $1 -ge 0 ] ; then
#/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-3dnow
#fi

#%%post -n atlas-sse -p /sbin/ldconfig

#%%postun -n atlas-sse -p /sbin/ldconfig

#%%posttrans sse-devel
#if [ $1 -eq 0 ] ; then
#/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
#		%{_includedir}/atlas-%{_arch}-sse  %{pr_sse}
#fi

#%%preun sse-devel
#if [ $1 -ge 0 ] ; then
#/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-sse
#fi

%post -n atlas-sse2 -p /sbin/ldconfig

%postun -n atlas-sse2 -p /sbin/ldconfig

%posttrans sse2-devel
if [ $1 -eq 0 ] ; then
/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
		%{_includedir}/atlas-%{_arch}-sse2  %{pr_sse2}
fi

%preun sse2-devel
if [ $1 -ge 0 ] ; then
/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-sse2
fi

%post -n atlas-sse3 -p /sbin/ldconfig

%postun -n atlas-sse3 -p /sbin/ldconfig

%posttrans sse3-devel
if [ $1 -eq 0 ] ; then
/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
		%{_includedir}/atlas-%{_arch}-sse3  %{pr_sse3}
fi

%preun sse3-devel
if [ $1 -ge 0 ] ; then
/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-sse3
fi

%endif

#%ifarch s390 s390x
#%post -n atlas-z10 -p /sbin/ldconfig

#%postun -n atlas-z10 -p /sbin/ldconfig

#%posttrans z10-devel
#if [ $1 -eq 0 ] ; then
#/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
#		%{_includedir}/atlas-%{_arch}-z10  %{pr_z10}
#fi

#%preun z10-devel
#if [ $1 -ge 0 ] ; then
#/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-z10
#fi

#%post -n atlas-z196 -p /sbin/ldconfig

#%postun -n atlas-z196 -p /sbin/ldconfig

#%posttrans z196-devel
#if [ $1 -eq 0 ] ; then
#/usr/sbin/alternatives	--install %{_includedir}/atlas atlas-inc 	\
#		%{_includedir}/atlas-%{_arch}-z196  %{pr_z196}
#fi

#%preun z196-devel
#if [ $1 -ge 0 ] ; then
#/usr/sbin/alternatives --remove atlas-inc %{_includedir}/atlas-%{_arch}-z196
#fi

#%endif

%endif

%files
%defattr(-,root,root,-)
%doc doc/README.dist
%dir %{_libdir}/atlas
%{_libdir}/atlas/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}.conf

%files devel
%defattr(-,root,root,-)
%doc doc
%{_libdir}/atlas/*.so
%{_includedir}/atlas-%{_arch}-base/
%{_includedir}/*.h
%ghost %{_includedir}/atlas

%files static
%defattr(-,root,root,-)
%{_libdir}/atlas/*.a

%if "%{?enable_native_atlas}" == "0"

#ifarch x86_64

#files sse3
#defattr(-,root,root,-)
#doc doc/README.Fedora
#dir %{_libdir}/atlas-sse3
#{_libdir}/atlas-sse3/*.so
#config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-sse3.conf

#files sse3-devel
#defattr(-,root,root,-)
#doc doc
#{_libdir}/atlas-sse3/*.so
#{_includedir}/atlas-%{_arch}-sse3/
#{_includedir}/*.h
#ghost %{_includedir}/atlas

#endif

%ifarch %{ix86}

#%%files 3dnow
#%%defattr(-,root,root,-)
#%%doc doc/README.Fedora
#%%dir %{_libdir}/atlas-3dnow
#%%{_libdir}/atlas-3dnow/*.so.*
#%%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-3dnow.conf

#%%files 3dnow-devel
#%%defattr(-,root,root,-)
#%%doc doc
#%%{_libdir}/atlas-3dnow/*.so
#%%{_includedir}/atlas-%{_arch}-3dnow/
#%%{_includedir}/*.h
#%%ghost %{_includedir}/atlas

#%%files sse
#%%defattr(-,root,root,-)
#%%doc doc/README.Fedora
#%%dir %{_libdir}/atlas-sse
#%%{_libdir}/atlas-sse/*.so.*
#%%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-sse.conf

#%%files sse-devel
#%%defattr(-,root,root,-)
#%%doc doc
#%%{_libdir}/atlas-sse/*.so
#%%{_includedir}/atlas-%{_arch}-sse/
#%%{_includedir}/*.h
#%%ghost %{_includedir}/atlas

%files sse2
%defattr(-,root,root,-)
%doc doc/README.dist
%dir %{_libdir}/atlas-sse2
%{_libdir}/atlas-sse2/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-sse2.conf

%files sse2-devel
%defattr(-,root,root,-)
%doc doc
%{_libdir}/atlas-sse2/*.so
%{_includedir}/atlas-%{_arch}-sse2/
%{_includedir}/*.h
%ghost %{_includedir}/atlas

%files sse2-static
%defattr(-,root,root,-)
%{_libdir}/atlas-sse2/*.a

%files sse3
%defattr(-,root,root,-)
%doc doc/README.dist
%dir %{_libdir}/atlas-sse3
%{_libdir}/atlas-sse3/*.so.*
%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-sse3.conf

%files sse3-static
%defattr(-,root,root,-)
%{_libdir}/atlas-sse3/*.a

%files sse3-devel
%defattr(-,root,root,-)
%doc doc
%{_libdir}/atlas-sse3/*.so
%{_includedir}/atlas-%{_arch}-sse3/
%{_includedir}/*.h
%ghost %{_includedir}/atlas

%endif

#%ifarch s390 s390x
#%files z10
#%defattr(-,root,root,-)
#%doc doc/README.dist
#%dir %{_libdir}/atlas-z10
#%{_libdir}/atlas-z10/*.so
#%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-z10.conf
#
#%files z10-devel
#%defattr(-,root,root,-)
#%doc doc
#%{_libdir}/atlas-z10/*.so
#%{_includedir}/atlas-%{_arch}-z10/
#%{_includedir}/*.h
#%ghost %{_includedir}/atlas
#
#%files z10-static
#%defattr(-,root,root,-)
#%{_libdir}/atlas-z10/*.a

#%files z196
#%defattr(-,root,root,-)
#%doc doc/README.dist
#%dir %{_libdir}/atlas-z196
#%{_libdir}/atlas-z196/*.so
#%config(noreplace) /etc/ld.so.conf.d/atlas-%{_arch}-z196.conf

#%files z196-devel
#%defattr(-,root,root,-)
#%doc doc
#%{_libdir}/atlas-z196/*.so
#%{_includedir}/atlas-%{_arch}-z196/
#%{_includedir}/*.h
#%ghost %{_includedir}/atlas

#%files z196-static
#%defattr(-,root,root,-)
#%{_libdir}/atlas-z196/*.a

#%endif
%endif

%changelog
* Wed Mar 15 2017 Jakub Martisko <jamartis@redhat.com> - 3.10.1-12
- cleanup: merge the application of ppc patches from previous commit
  into single block
- Related: rhbz#1350536

* Mon Feb 27 2017 Jakub Martisko <jamartis@redhat.com> - 3.10.1-11
- apply patches 99 and 110 to all ppc variants
- build lapack with -frecursive flag (#1176026)
- fix possible memory leak (#1350536)
- fix wrong sed substitutions (#1402627)
- Resolves: rhbz#1350536
- Related: rhbz#1176026

* Thu Oct 23 2014 Jaromir Capik <jcapik@redhat.com> - 3.10.1-10
- patching for Power8 to pass performance tunings and tests on P8 builders
- re-enabling tests on ppc64le
- Resolves: rhbz#1125475

* Sun Sep 07 2014 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-9
- ppcle patches (conflicting patches modified)
- tests on ppcle disabled to shorten build time and fit into 24 hour limit
- resolves bug 1125475
- aarch64 patches
- Resolves: rhbz#1061956

* Fri Feb 28 2014 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-7
- change x86_64 archdef to P4, prefetch instruction from hammer is illegal on some pentium 4
- add -fstack-protector-strong to flags
- Resolves: rhbz#1070783

* Thu Feb 20 2014 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-6
- use upstream archdef for s390x 64-bit
- Resolves: rhbz#804763

* Wed Feb 5 2014 Brendan Conoboy <blc@redhat.com> - 3.10.1-5.2
- Temporarily make %check failures non-fatal.

* Wed Feb 5 2014 Brendan Conoboy <blc@redhat.com> - 3.10.1-5.1
- Add Mark Salter's initial aarch64 port.

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.10.1-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.10.1-4
- Mass rebuild 2013-12-27

* Tue Sep 24 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-3
- disable affinity to prevent crash on systems with fewer cpus

* Mon Sep 23 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-2
- fix atlas-devel dependency
- archdefs for z10 and z196 not yet in use

* Mon Sep 23 2013 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-2
- Add %%check section

* Fri Sep 20 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 3.10.1-1
- Rebase to 3.10.1
- Dropped x86_64-SSE2, ix86-SSE1, ix86-3DNow, z10, z196 (uncompilable).
- Modified incompatible patches.
- Added armv7neon support, modified archdef from softfp abi to hard abi.
- Modified Make.lib to include build-id, soname, versioned library name and symlinks.
- Now builds monolithic libsatlas (serial) and libtatlas (threaded)
  libraries with lapack and blas included.
- Lapack source tarball needed instead of static library.
- Disabled cpu throttling detection again (sorry, could not work on atlas
  otherwise, feel free to enable yet again - atlas-throttling.patch).
- Removed mentions of "Fedora" to promote redistribution.
- Modified parts of atlas.spec sometimes left in place, work still in progress,
  cleanup needed.


* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jan 27 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.8.4-8
- Rebuild for ARM glibc/binutils issues

* Fri Sep 07 2012 Orion Poplawski <orion@nwra.com> - 3.8.4-7
- Rebuild with lapack 3.4.1

* Thu Aug 09 2012 Orion Poplawski <orion@nwra.com> - 3.8.4-6
- Add patch to properly pass -melf_* to the linker with -Wl (bug 817552)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 01 2011 Deji Akingunola <dakingun@gmail.com> - 3.8.4-3
- Apply patch to enable arm build (Patch provided by Jitesh Shah <jiteshs@marvell.com>)
- Stop turning off throttle checking, upstream frown at it (seems O.K. for Koji)

* Mon Jun 20 2011 Dan Horák <dan[at]danny.cz> - 3.8.4-2
- Use -march=z10 for z196 optimised build because the builder is a z10
  (Christian Bornträger)

* Tue Jun 14 2011 Deji Akingunola <dakingun@gmail.com> - 3.8.4-1
- Update to 3.8.4
- Build the default package for SSE2 and add a SSE3 subpackage on x86_64
- Apply patch (and arch defs.) to build on s390 and s390x (Dan Horák)
- Fix-up build on s390 and s390x (Christian Bornträger)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 26 2010 Deji Akingunola <dakingun@gmail.com> - 3.8.3-18
- Create a subpackage for SSE2 on x86_64

* Sat Jul 17 2010 Dan Horák <dan[at]danny.cz> - 3.8.3-17
- rebuild against fixed lapack libraries

* Thu Jul 15 2010 Dan Horák <dan[at]danny.cz> - 3.8.3-16
- fix build on s390 (patch by Karsten Hopp)

* Wed Feb 10 2010 Deji Akingunola <dakingun@gmail.com> - 3.8.3-15
- Disable the problematic sparc patch
- Change lapack-devel BR to lapack-static, where liblapack_pic.a now resides.

* Wed Feb 03 2010 Dennis Gilmore <dennis@ausil.us> - 3.8.3-14
- fix sparc build

* Fri Jan 29 2010 Deji Akingunola <dakingun@gmail.com> - 3.8.3-13
- Remove static libraries.
- Fix typo in SSE3 subpackage's summary.

* Sat Oct 24 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-12
- Use alternatives to workaround multilib conflicts (BZ#508565). 

* Tue Sep 29 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-11
- Obsolete the -header subpackage properly. 

* Sat Sep 26 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-10
- Use the new arch. default for Pentium PRO (Fedora bug #510498)
- (Re-)Introduce 3dNow subpackage

* Sun Sep  6 2009 Alex Lancaster <alexlan[AT]fedoraproject org> - 3.8.3-9
- Rebuild against fixed lapack (see #520518)

* Thu Aug 13 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-8
- Revert the last change, it doesn't solve the problem. 

* Tue Aug 04 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-7
- Create a -header subpackage to avoid multilib conflicts (BZ#508565). 

* Tue Aug 04 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-6
- Add '-g' to build flag to allow proper genration of debuginfo subpackages (Fedora bug #509813)
- Build for F12

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 02 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-4
- Use the right -msse* option for the -sse* subpackages (Fedora bug #498715)

* Tue Apr 21 2009 Karsten Hopp <karsten@redhat.com> 3.8.3-3.1
- add s390x to 64 bit archs

* Fri Feb 27 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-3
- Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Deji Akingunola <dakingun@gmail.com> - 3.8.3-1
- Update to version 3.8.3

* Sun Dec 21 2008 Deji Akingunola <dakingun@gmail.com> - 3.8.2-5
- Link in appropriate libs when creating shared libs, reported by Orcan 'oget' Ogetbil (BZ#475411)

* Tue Dec 16 2008 Deji Akingunola <dakingun@gmail.com> - 3.8.2-4
- Don't symlink the atlas libdir on i386, cause upgrade issue (BZ#476787)
- Fix options passed to gcc when making shared libs

* Tue Dec 16 2008 Deji Akingunola <dakingun@gmail.com> - 3.8.2-3
- Use 'gcc -shared' to build shared libs instead of stock 'ld'

* Sat Dec 13 2008 Deji Akingunola <dakingun@gmail.com> - 3.8.2-2
- Properly obsolete/provide older subpackages that are no longer packaged.

* Mon Sep 01 2008 Deji Akingunola <dakingun@gmail.com> - 3.8.2-1
- Upgrade to ver 3.8.2 with refined build procedures.

* Thu Feb 28 2008 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-15
- Disable altivec package--it is causing illegal instructions during build.

* Thu Feb 28 2008 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-14
- Enable compilation on alpha (bug 426086).
- Patch for compilation on ia64 (bug 432744).

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.6.0-13
- Autorebuild for GCC 4.3

* Mon Jun  4 2007 Orion Poplawski <orion@cora.nwra.com> 3.6.0-12
- Rebuild for ppc64

* Fri Sep  8 2006 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-11
- Rebuild for FC6.
- Remove outdated comments from spec file.

* Mon Feb 13 2006 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-10
- Rebuild for Fedora Extras 5.
- Add --noexecstack to compilation of assembly kernels. These were
  previously marked executable, which caused problems with selinux.

* Mon Dec 19 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-9
- Rebuild for gcc 4.1.

* Mon Oct 10 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-8
- Make all devel subpackages depend on their non-devel counterparts.
- Add /etc/ld.so.conf.d files for -sse and -3dnow, because they don't
  seem to get picked up automatically.

* Wed Oct 05 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-7
- Forgot to add the new patch to sources.

* Tue Oct 04 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-6
- Use new Debian patch, and enable shared libs (they previously failed
  to build on gcc 4).
- Minor updates to description and README.Fedora file.
- Fix buildroot name to match FE preferred form.
- Fixes for custom optimized builds.
- Add dist tag.

* Wed Sep 28 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-5
- fix files lists.

* Mon Sep 26 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-4
- generate library symlinks earlier for the benefit of later linking steps.

* Wed Sep 14 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-3
- Change lapack dependency to lapack-devel, and use lapack_pic.a for
  building liblapack.so.

* Wed Sep 14 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-2
- Add "bit" macro to correctly build on x86_64.

* Tue Aug 16 2005 Quentin Spencer <qspencer@users.sourceforge.net> 3.6.0-1
- Initial version.
