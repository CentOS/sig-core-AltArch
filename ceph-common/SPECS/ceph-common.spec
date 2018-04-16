%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

#################################################################################
# common
#################################################################################
Name:		ceph-common
Version:	0.94.5
Release:	2%{?dist}
Epoch:		1
Summary:	Ceph Common
License:	GPLv2
Group:		System Environment/Base
URL:		http://ceph.com/
Source0:	http://ceph.com/download/ceph-%{version}.tar.bz2
Patch1:         0001-Disable-erasure_codelib-neon-build.patch
Requires:	librbd1 = %{epoch}:%{version}-%{release}
Requires:	librados2 = %{epoch}:%{version}-%{release}
Requires:	python-rbd = %{epoch}:%{version}-%{release}
Requires:	python-rados = %{epoch}:%{version}-%{release}
Requires:	python
Requires:	python-argparse
Requires:	python-requests
%if ! ( 0%{?rhel} && 0%{?rhel} <= 6 )
Requires:	xfsprogs
%endif
Requires:	cryptsetup
Requires:	parted
Requires:	util-linux
%ifnarch s390 s390x
Requires:	hdparm
%endif
# For initscript
Requires:	redhat-lsb-core
Requires(post):	binutils
BuildRequires:	make
BuildRequires:	gcc-c++
BuildRequires:	libtool
BuildRequires:	boost-devel
BuildRequires:	bzip2-devel
BuildRequires:	libedit-devel
BuildRequires:	perl
BuildRequires:	gdbm
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	python-nose
BuildRequires:	python-argparse
BuildRequires:	libaio-devel
BuildRequires:	libcurl-devel
BuildRequires:	libxml2-devel
BuildRequires:	libuuid-devel
BuildRequires:	libblkid-devel >= 2.17
BuildRequires:	libudev-devel
BuildRequires:	expat-devel
%if ! ( 0%{?rhel} && 0%{?rhel} <= 6 )
BuildRequires:	xfsprogs-devel
%endif
# No yasm dependency for now, it causes selinux issues
#BuildRequires:	yasm

#################################################################################
# specific
#################################################################################
%if ! 0%{?rhel}
BuildRequires:	sharutils
%endif

Requires:	gdisk
BuildRequires:	nss-devel
BuildRequires:	keyutils-libs-devel
Requires:	gdisk
Requires(post):	chkconfig
Requires(preun):chkconfig
Requires(preun):initscripts

#################################################################################
# obsoletes
#################################################################################
# We need to obsolete and provide python-ceph with this package
# We moved ceph_argparse.py from python-ceph to ceph-common when
# we split python-ceph, ceph-common needs to obsolete python-ceph
# as well, it also provides python-ceph via dependencies
Obsoletes:	python-ceph
Provides:	python-ceph

%description
Common utilities to mount and interact with a ceph storage cluster.


#################################################################################
# packages
#################################################################################
%package -n librados2
Summary:	RADOS distributed object store client library
Group:		System Environment/Libraries
License:	LGPL-2.0
Obsoletes:	ceph-libs
%description -n librados2
RADOS is a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to access the distributed object
store using a simple file-like interface.

%package -n librados2-devel
Summary:	RADOS headers
Group:		Development/Libraries
License:	LGPL-2.0
Requires:	librados2 = %{epoch}:%{version}-%{release}
Obsoletes:	ceph-devel
%description -n librados2-devel
This package contains libraries and headers needed to develop programs
that use RADOS object store.

%package -n python-rados
Summary:	Python libraries for the RADOS object store
Group:		System Environment/Libraries
License:	LGPL-2.0
Requires:	librados2 = %{epoch}:%{version}-%{release}
Obsoletes:	python-ceph
%description -n python-rados
This package contains Python libraries for interacting with Cephs RADOS
object store.

%package -n librbd1
Summary:	RADOS block device client library
Group:		System Environment/Libraries
License:	LGPL-2.0
Requires:	librados2 = %{epoch}:%{version}-%{release}
Obsoletes:	ceph-libs
%description -n librbd1
RBD is a block device striped across multiple distributed objects in
RADOS, a reliable, autonomic distributed object storage cluster
developed as part of the Ceph distributed storage system. This is a
shared library allowing applications to manage these block devices.

%package -n librbd1-devel
Summary:	RADOS block device headers
Group:		Development/Libraries
License:	LGPL-2.0
Requires:	librbd1 = %{epoch}:%{version}-%{release}
Requires:	librados2-devel = %{epoch}:%{version}-%{release}
Obsoletes:	ceph-devel
%description -n librbd1-devel
This package contains libraries and headers needed to develop programs
that use RADOS block device.

%package -n python-rbd
Summary:	Python libraries for the RADOS block device
Group:		System Environment/Libraries
License:	LGPL-2.0
Requires:	librbd1 = %{epoch}:%{version}-%{release}
Requires:	python-rados = %{epoch}:%{version}-%{release}
Obsoletes:	python-ceph
%description -n python-rbd
This package contains Python libraries for interacting with Cephs RADOS
block device.

#################################################################################
# common
#################################################################################
%prep
%setup -q -n ceph-%{version}
%patch1 -p1

%build
./autogen.sh

%if ( 0%{?rhel} && 0%{?rhel} <= 6)
MY_CONF_OPT="--without-libxfs"
%else
MY_CONF_OPT=""
%endif

# Do not build server part of the project
# Do not use gperftools (tcmalloc) on rhel
# No need to build fuse, rest-bench radosgw and ocf pkgs so far
# Use nss instead of cryptopp library
MY_CONF_OPT="$MY_CONF_OPT --disable-server --without-libatomic-ops --without-tcmalloc --without-radosgw --without-rest-bench --without-fuse --without-ocf --without-cryptopp --with-nss --without-radosstriper --without-cephfs"

export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed -e 's/i386/i486/'`

%{configure}	--prefix=/usr \
		--localstatedir=/var \
		--sysconfdir=/etc \
		--docdir=%{_docdir}/ceph \
		$MY_CONF_OPT \
		CFLAGS="$RPM_OPT_FLAGS $EXTRA_CFLAGS" \
		CXXFLAGS="$RPM_OPT_FLAGS $EXTRA_CFLAGS" \
		LDFLAGS="$EXTRA_LDFLAGS"

make %{_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
install -D src/init-rbdmap $RPM_BUILD_ROOT%{_initrddir}/rbdmap
install -D src/rbdmap $RPM_BUILD_ROOT%{_sysconfdir}/ceph/rbdmap
rm -f $RPM_BUILD_ROOT%{_docdir}/ceph/sample.ceph.conf
rm -f $RPM_BUILD_ROOT%{_docdir}/ceph/sample.fetch_config
rm -f $RPM_BUILD_ROOT%{_libdir}/ceph/erasure-code/libec_*.so*
rm -f $RPM_BUILD_ROOT%{_libexecdir}/ceph/ceph-osd-prestart.sh
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/radosgw-admin
rm -f $RPM_BUILD_ROOT%{_bindir}/crushtool
rm -f $RPM_BUILD_ROOT%{_bindir}/monmaptool
rm -f $RPM_BUILD_ROOT%{_bindir}/osdmaptool
rm -f $RPM_BUILD_ROOT%{_bindir}/rbd-replay
rm -f $RPM_BUILD_ROOT%{_bindir}/rbd-replay-many
rm -f $RPM_BUILD_ROOT%{_libdir}/ceph/ceph_common.sh
rm -f $RPM_BUILD_ROOT%{_libexecdir}/ceph/ceph-osd-prestart.sh
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/rbd-replay.8*
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/rbd-replay-many.8*
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/rbd-replay-prep.8*

# udev rules
%if 0%{?rhel} >= 7 || 0%{?fedora}
install -m 0644 -D udev/50-rbd.rules $RPM_BUILD_ROOT/usr/lib/udev/rules.d/50-rbd.rules
%else
install -m 0644 -D udev/50-rbd.rules $RPM_BUILD_ROOT/lib/udev/rules.d/50-rbd.rules
%endif

%clean
rm -rf $RPM_BUILD_ROOT


#################################################################################
# files
#################################################################################
%files
%defattr(-,root,root,-)
%{_bindir}/ceph
%{_bindir}/ceph-authtool
%{_bindir}/ceph-conf
%{_bindir}/ceph-dencoder
%{_bindir}/ceph-rbdnamer
%{_bindir}/ceph-syn
%{_bindir}/rados
%{_bindir}/rbd
%{_bindir}/ceph-post-file
%{_bindir}/ceph-brag
%{_mandir}/man8/ceph-authtool.8*
%{_mandir}/man8/ceph-conf.8*
%{_mandir}/man8/ceph-dencoder.8*
%{_mandir}/man8/ceph-rbdnamer.8*
%{_mandir}/man8/ceph-syn.8*
%{_mandir}/man8/ceph-post-file.8*
%{_mandir}/man8/ceph.8*
%{_mandir}/man8/rados.8*
%{_mandir}/man8/rbd.8*
%{_datadir}/ceph/known_hosts_drop.ceph.com
%{_datadir}/ceph/id_dsa_drop.ceph.com
%{_datadir}/ceph/id_dsa_drop.ceph.com.pub
%dir %{_sysconfdir}/ceph/
%dir %{_localstatedir}/log/ceph/
%config %{_sysconfdir}/bash_completion.d/ceph
%config %{_sysconfdir}/bash_completion.d/rados
%config %{_sysconfdir}/bash_completion.d/rbd
%config(noreplace) %{_sysconfdir}/ceph/rbdmap
%{_initrddir}/rbdmap
%{python_sitelib}/ceph_argparse.py*
%{_udevrulesdir}/50-rbd.rules

%postun
# Package removal cleanup
if [ "$1" -eq "0" ] ; then
    rm -rf /var/log/ceph
    rm -rf /etc/ceph
fi

#################################################################################
%files -n librados2
%defattr(-,root,root,-)
%{_libdir}/librados.so.*

%post -n librados2
/sbin/ldconfig

%postun -n librados2
/sbin/ldconfig

#################################################################################
%files -n librados2-devel
%defattr(-,root,root,-)
%dir %{_includedir}/rados
%{_includedir}/rados/librados.h
%{_includedir}/rados/librados.hpp
%{_includedir}/rados/buffer.h
%{_includedir}/rados/page.h
%{_includedir}/rados/crc32c.h
%{_includedir}/rados/rados_types.h
%{_includedir}/rados/rados_types.hpp
%{_includedir}/rados/memory.h
%{_libdir}/librados.so
%{_bindir}/librados-config
%{_mandir}/man8/librados-config.8*

#################################################################################
%files -n librbd1
%defattr(-,root,root,-)
%{_libdir}/librbd.so.*
%if 0%{?rhel} >= 7 || 0%{?fedora}
/usr/lib/udev/rules.d/50-rbd.rules
%else
/lib/udev/rules.d/50-rbd.rules
%endif

%post -n librbd1
/sbin/ldconfig

%postun -n librbd1
/sbin/ldconfig

#################################################################################
%files -n librbd1-devel
%defattr(-,root,root,-)
%dir %{_includedir}/rbd
%{_includedir}/rbd/librbd.h
%{_includedir}/rbd/librbd.hpp
%{_includedir}/rbd/features.h
%{_libdir}/librbd.so

#################################################################################
%files -n python-rados
%defattr(-,root,root,-)
%{python_sitelib}/rados.py*

#################################################################################
%files -n python-rbd
%defattr(-,root,root,-)
%{python_sitelib}/rbd.py*

%changelog
* Sun Apr 15 2018 Pablo Greco <pablo@fliagreco.com.ar> - 1:0.94.5-2
- backport Fedora patch to fix fuild on armhfp

* Tue Jun 20 2017 Boris Ranto <branto@redhat.com> - 1:0.94.5-2
- drop the rebase

* Thu Jun 01 2017 Boris Ranto <branto@redhat.com> - 1:10.2.5-3
- Strip away ceph user (errata complains after rebase)

* Mon Apr 24 2017 Boris Ranto <branto@redhat.com> - 1:10.2.5-2
- New release (1:10.2.5-2)
- A compile patch for s390
- Build on all the platforms

* Wed Feb 22 2017 Boris Ranto <branto@redhat.com> - 1:10.2.5-1
- New version (1:10.2.5-1)
- Makefile: Fix dencoder build
- Add fake fcgiapp.h for rgw
- common: Build more files of libcommon in client
- libradosstripper: Build libradostripper for rados as noinst

* Wed Jun 22 2016 Boris Ranto <branto@redhat.com> - 1:0.94.5-1
- New version (1:0.94.5-1)

* Wed Jun 17 2015 Boris Ranto <branto@redhat.com> - 1:0.80.7-3
- Fix librbd: aio calls may block (1225188)

* Fri Nov 21 2014 Boris Ranto <branto@redhat.com> - 1:0.80.7-2
- We need to obsolete and provide python-ceph by ceph-common

* Thu Oct 16 2014 Boris Ranto <branto@redhat.com> - 1:0.80.7-1
- Rebase to latest upstream version

* Mon Oct 13 2014 Boris Ranto <branto@redhat.com> - 1:0.80.6-4
- fix the typo in librados-devel vs librados2-devel dependency

* Thu Oct 9 2014 Boris Ranto <branto@redhat.com> - 1:0.80.6-3
- split the python-ceph and ceph-devel packages to properly fix the
  'disable cephfs' issue

* Wed Oct 8 2014 Boris Ranto <branto@redhat.com> - 1:0.80.6-2
- Do not package cephfs files

* Tue Oct 7 2014 Boris Ranto <branto@redhat.com> - 1:0.80.6-1
- Rebase to latest stable upstream version
- Remove libatomic_ops dependency

* Wed Oct 1 2014 Boris Ranto <branto@redhat.com> - 1:0.80.5-13
- Remove python-flask dependency

* Wed Sep 24 2014 Boris Ranto <branto@redhat.com> - 1:0.80.5-12
- Fix the license field

* Wed Sep 24 2014 Boris Ranto <branto@redhat.com> - 1:0.80.5-11
- First attempt to build rhel 7 ceph packages

* Tue Sep 9 2014 Dan Horák <dan[at]danny.cz> - 1:0.80.5-10
- update Requires for s390(x)

* Wed Sep 3 2014 Boris Ranto <branto@redhat.com> - 1:0.80.5-9
- Symlink librd.so.1 to /usr/lib64/qemu only on rhel6+ x86_64 (1136811)

* Thu Aug 21 2014 Boris Ranto <branto@redhat.com> - 1:0.80.5-8
- Revert the previous change
- Fix bz 1118504, second attempt (yasm appears to be the package that caused this

* Wed Aug 20 2014 Boris Ranto <branto@redhat.com> - 1:0.80.5-7
- Several more merges from file to try to fix the selinux issue (1118504)

* Sun Aug 17 2014 Kalev Lember <kalevlember@gmail.com> - 1:0.80.5-6
- Obsolete ceph-libcephfs

* Sat Aug 16 2014 Boris Ranto <branto@redhat.com> - 1:0.80.5-5
- Do not require xfsprogs/xfsprogs-devel for el6
- Require gperftools-devel for non-ppc*/s390* architectures only
- Do not require junit -- no need to build libcephfs-test.jar
- Build without libxfs for el6
- Build without tcmalloc for ppc*/s390* architectures
- Location of mkcephfs must depend on a rhel release
- Use epoch in the Requires fields [1130700]

* Sat Aug 16 2014 Boris Ranto <branto@redhat.com> - 1:0.80.5-4
- Use the proper version name in Obsoletes

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.80.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Boris Ranto <branto@redhat.com> - 1:0.80.5-2
- Add the arm pthread hack

* Fri Aug 15 2014 Boris Ranto <branto@redhat.com> - 1:0.80.5-1
- Bump the Epoch, we need to keep the latest stable, not development,
  ceph version in fedora
- Use the upstream spec file with the ceph-libs split
- Add libs-compat subpackage [1116546]
- use fedora in rhel 7 checks
- obsolete libcephfs [1116614]
- depend on redhat-lsb-core for the initscript [1108696]

* Wed Aug 13 2014 Kalev Lember <kalevlember@gmail.com> - 0.81.0-6
- Add obsoletes to keep the upgrade path working (#1118510)

* Mon Jul 7 2014 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 0.81.0-5
- revert to old spec until after f21 branch

* Fri Jul 4 2014 Kaleb S. KEITHLEY <kkeithle[at]redhat.com>
- temporary exclude f21/armv7hl. N.B. it builds fine on f20/armv7hl.

* Fri Jul 4 2014 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 0.81.0-4
- upstream ceph.spec file

* Tue Jul 1 2014 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 0.81.0-3
- upstream ceph.spec file

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.81.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 5 2014 Kaleb S. KEITHLEY <kkeithle[at]redhat.com>
- el6 ppc64 likewise for tcmalloc, merge from origin/el6

* Thu Jun 5 2014 Kaleb S. KEITHLEY <kkeithle[at]redhat.com>
- el6 ppc64 does not have gperftools, merge from origin/el6

* Thu Jun 5 2014 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 0.81.0-1
- ceph-0.81.0

* Wed Jun  4 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.80.1-5
- gperftools now available on aarch64/ppc64

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 0.80.1-4
- Rebuild for boost 1.55.0

* Fri May 23 2014 David Tardon <dtardon@redhat.com> - 0.80.1-3
- rebuild for boost 1.55.0

* Wed May 14 2014 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 0.80.1-2
- build epel-6
- exclude %%{_libdir}/ceph/erasure-code in base package

* Tue May 13 2014 Kaleb S. KEITHLEY <kkeithle[at]redhat.com> - 0.80.1-1
- Update to latest stable upstream release, BZ 1095201
- PIE, _hardened_build, BZ 955174

* Thu Feb 06 2014 Ken Dreyer <ken.dreyer@inktank.com> - 0.72.2-2
- Move plugins from -devel into -libs package (#891993). Thanks Michael
  Schwendt.

* Mon Jan 06 2014 Ken Dreyer <ken.dreyer@inktank.com> 0.72.2-1
- Update to latest stable upstream release
- Use HTTPS for URLs
- Submit Automake 1.12 patch upstream
- Move unversioned shared libs from ceph-libs into ceph-devel

* Wed Dec 18 2013 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> 0.67.3-4
- build without tcmalloc on aarch64 (no gperftools)

* Sat Nov 30 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.67.3-3
- gperftools not currently available on aarch64

* Mon Oct 07 2013 Dan Horák <dan[at]danny.cz> - 0.67.3-2
- fix build on non-x86_64 64-bit arches

* Wed Sep 11 2013 Josef Bacik <josef@toxicpanda.com> - 0.67.3-1
- update to 0.67.3

* Wed Sep 11 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 0.61.7-3
- let base package include all its documentation files via %%doc magic,
  so for Fedora 20 Unversioned Docdirs no files are included accidentally
- include the sample config files again (instead of just an empty docdir
  that has been added for #846735)
- don't include librbd.so.1 also in -devel package (#1003202)
- move one misplaced rados plugin from -devel into -libs package (#891993)
- include missing directories in -devel and -libs packages
- move librados-config into the -devel pkg where its manual page is, too
- add %%_isa to subpackage dependencies
- don't use %%defattr anymore
- add V=1 to make invocation for verbose build output

* Wed Jul 31 2013 Peter Robinson <pbrobinson@fedoraproject.org> 0.61.7-2
- re-enable tmalloc on arm now gperftools is fixed

* Mon Jul 29 2013 Josef Bacik <josef@toxicpanda.com> - 0.61.7-1
- Update to 0.61.7

* Sat Jul 27 2013 pmachata@redhat.com - 0.56.4-2
- Rebuild for boost 1.54.0

* Fri Mar 29 2013 Josef Bacik <josef@toxicpanda.com> - 0.56.4-1
- Update to 0.56.4
- Add upstream d02340d90c9d30d44c962bea7171db3fe3bfba8e to fix logrotate

* Wed Feb 20 2013 Josef Bacik <josef@toxicpanda.com> - 0.56.3-1
- Update to 0.56.3

* Mon Feb 11 2013 Richard W.M. Jones <rjones@redhat.com> - 0.53-2
- Rebuilt to try to fix boost dependency problem in Rawhide.

* Thu Nov  1 2012 Josef Bacik <josef@toxicpanda.com> - 0.53-1
- Update to 0.53

* Mon Sep 24 2012 Jonathan Dieter <jdieter@lesbg.com> - 0.51-3
- Fix automake 1.12 error
- Rebuild after buildroot was messed up

* Tue Sep 18 2012 Jonathan Dieter <jdieter@lesbg.com> - 0.51-2
- Use system leveldb

* Fri Sep 07 2012 David Nalley <david@gnsa.us> - 0.51-1
- Updating to 0.51
- Updated url and source url. 

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  9 2012 Josef Bacik <josef@toxicpanda.com> - 0.46-1
- updated to upstream 0.46
- broke out libcephfs (rhbz# 812975)

* Mon Apr 23 2012 Dan Horák <dan[at]danny.cz> - 0.45-2
- fix detection of C++11 atomic header

* Thu Apr 12 2012 Josef Bacik <josef@toxicpanda.com> - 0.45-1
- updating to upstream 0.45

* Wed Apr  4 2012 Niels de Vos <devos@fedoraproject.org> - 0.44-5
- Add LDFLAGS=-lpthread on any ARM architecture
- Add CFLAGS=-DAO_USE_PTHREAD_DEFS on ARMv5tel

* Mon Mar 26 2012 Dan Horák <dan[at]danny.cz> 0.44-4
- gperftools not available also on ppc

* Mon Mar 26 2012 Jonathan Dieter <jdieter@lesbg.com> - 0.44-3
- Remove unneeded patch

* Sun Mar 25 2012 Jonathan Dieter <jdieter@lesbg.com> - 0.44-2
- Update to 0.44
- Fix build problems

* Mon Mar  5 2012 Jonathan Dieter <jdieter@lesbg.com> - 0.43-1
- Update to 0.43
- Remove upstreamed compile fixes patch
- Remove obsoleted dump_pop patch

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.41-2
- Rebuilt for c++ ABI breakage

* Thu Feb 16 2012 Tom Callaway <spot@fedoraproject.org> 0.41-1
- update to 0.41
- fix issues preventing build
- rebuild against gperftools

* Sat Dec 03 2011 David Nalley <david@gnsa.us> 0.38-1
- updating to upstream 0.39

* Sat Nov 05 2011 David Nalley <david@gnsa.us> 0.37-1
- create /etc/ceph - bug 745462
- upgrading to 0.37, fixing 745460, 691033
- fixing various logrotate bugs 748930, 747101

* Fri Aug 19 2011 Dan Horák <dan[at]danny.cz> 0.31-4
- google-perftools not available also on s390(x)

* Mon Jul 25 2011 Karsten Hopp <karsten@redhat.com> 0.31-3
- build without tcmalloc on ppc64, BR google-perftools is not available there

* Tue Jul 12 2011 Josef Bacik <josef@toxicpanda.com> 0.31-2
- Remove curl/types.h include since we don't use it anymore

* Tue Jul 12 2011 Josef Bacik <josef@toxicpanda.com> 0.31-1
- Update to 0.31

* Tue Apr  5 2011 Josef Bacik <josef@toxicpanda.com> 0.26-2
- Add the compile fix patch

* Tue Apr  5 2011 Josef Bacik <josef@toxicpanda.com> 0.26
- Update to 0.26

* Tue Mar 22 2011 Josef Bacik <josef@toxicpanda.com> 0.25.1-1
- Update to 0.25.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.21.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 Steven Pritchard <steve@kspei.com> 0.21.3-1
- Update to 0.21.3.

* Mon Aug 30 2010 Steven Pritchard <steve@kspei.com> 0.21.2-1
- Update to 0.21.2.

* Thu Aug 26 2010 Steven Pritchard <steve@kspei.com> 0.21.1-1
- Update to 0.21.1.
- Sample configs moved to /usr/share/doc/ceph/.
- Added cclass, rbd, and cclsinfo.
- Dropped mkmonfs and rbdtool.
- mkcephfs moved to /sbin.
- Add libcls_rbd.so.

* Tue Jul  6 2010 Josef Bacik <josef@toxicpanda.com> 0.20.2-1
- update to 0.20.2

* Wed May  5 2010 Josef Bacik <josef@toxicpanda.com> 0.20-1
- update to 0.20
- disable hadoop building
- remove all the test binaries properly

* Fri Apr 30 2010 Sage Weil <sage@newdream.net> 0.19.1-5
- Remove java deps (no need to build hadoop by default)
- Include all required librados helpers
- Include fetch_config sample
- Include rbdtool
- Remove misc debugging, test binaries

* Fri Apr 30 2010 Josef Bacik <josef@toxicpanda.com> 0.19.1-4
- Add java-devel and java tricks to get hadoop to build

* Mon Apr 26 2010 Josef Bacik <josef@toxicpanda.com> 0.19.1-3
- Move the rados and cauthtool man pages into the base package

* Sun Apr 25 2010 Jonathan Dieter <jdieter@lesbg.com> 0.19.1-2
- Add missing libhadoopcephfs.so* to file list
- Add COPYING to all subpackages
- Fix ownership of /usr/lib[64]/ceph
- Enhance description of fuse client

* Tue Apr 20 2010 Josef Bacik <josef@toxicpanda.com> 0.19.1-1
- Update to 0.19.1

* Mon Feb  8 2010 Josef Bacik <josef@toxicpanda.com> 0.18-1
- Initial spec file creation, based on the template provided in the ceph src
