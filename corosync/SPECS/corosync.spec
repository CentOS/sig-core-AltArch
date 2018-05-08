# Conditionals
# Invoke "rpmbuild --without <feature>" or "rpmbuild --with <feature>"
# to disable or enable specific features
%bcond_with testagents
%bcond_with watchdog
%bcond_with monitoring
%bcond_without snmp
%bcond_without dbus
# no InfiniBand stack on s390(x)
%ifnarch s390 s390x
%bcond_with rdma
%endif
%bcond_without systemd
%bcond_with upstart
%bcond_without xmlconf
%bcond_without runautogen
%bcond_without qdevices
%bcond_without qnetd
%bcond_without libcgroup

%global gitver %{?numcomm:.%{numcomm}}%{?alphatag:.%{alphatag}}%{?dirty:.%{dirty}}
%global gittarver %{?numcomm:.%{numcomm}}%{?alphatag:-%{alphatag}}%{?dirty:-%{dirty}}

Name: corosync
Summary: The Corosync Cluster Engine and Application Programming Interfaces
Version: 2.4.3
Release: 2%{?gitver}%{?dist}.1
License: BSD
Group: System Environment/Base
URL: http://corosync.github.io/corosync/
Source0: http://build.clusterlabs.org/corosync/releases/%{name}-%{version}%{?gittarver}.tar.gz

Patch0: bz1536219-1-logging-Make-blackbox-configurable.patch
Patch1: bz1536219-2-logging-Close-before-and-open-blackbox-after-fork.patch
Patch2: bz1560467-1-totemcrypto-Check-length-of-the-packet.patch

%if 0%{?rhel}
ExclusiveArch: i686 x86_64 s390x ppc64le
%endif

# Runtime bits
Requires: corosynclib = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/chkconfig
Obsoletes: openais, openais-devel, openaislib, openaislib-devel
Obsoletes: cman, clusterlib, clusterlib-devel

# Build bits

BuildRequires: groff
BuildRequires: libqb-devel >= 0.14.2
BuildRequires: nss-devel
BuildRequires: zlib-devel
%if %{with runautogen}
BuildRequires: autoconf automake libtool
%endif
%if %{with monitoring}
BuildRequires: libstatgrab-devel
%endif
%if %{with rdma}
BuildRequires: libibverbs-devel librdmacm-devel
%endif
%if %{with snmp}
BuildRequires: net-snmp-devel
%endif
%if %{with dbus}
BuildRequires: dbus-devel
%endif
%if %{with systemd}
BuildRequires: systemd-units
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif
%if %{with xmlconf}
Requires: libxslt
%endif
%if %{with qdevices} || %{with qnetd}
Requires: nss-tools
%endif
%if %{with qnetd}
BuildRequires: sed
%endif
%if %{with libcgroup}
BuildRequires: libcgroup-devel
%endif

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

%prep
%setup -q -n %{name}-%{version}%{?gittarver}
%patch0 -p1 -b .bz1536219-1
%patch1 -p1 -b .bz1536219-2
%patch2 -p1 -b .bz1560467-1

%build
%if %{with runautogen}
./autogen.sh
%endif

%if %{with rdma}
export ibverbs_CFLAGS=-I/usr/include/infiniband \
export ibverbs_LIBS=-libverbs \
export rdmacm_CFLAGS=-I/usr/include/rdma \
export rdmacm_LIBS=-lrdmacm \
%endif
%{configure} \
%if %{with testagents}
	--enable-testagents \
%endif
%if %{with watchdog}
	--enable-watchdog \
%endif
%if %{with monitoring}
	--enable-monitoring \
%endif
%if %{with snmp}
	--enable-snmp \
%endif
%if %{with dbus}
	--enable-dbus \
%endif
%if %{with rdma}
	--enable-rdma \
%endif
%if %{with systemd}
	--enable-systemd \
%endif
%if %{with upstart}
	--enable-upstart \
%endif
%if %{with xmlconf}
	--enable-xmlconf \
%endif
%if %{with qdevices}
	--enable-qdevices \
%endif
%if %{with qnetd}
	--enable-qnetd \
%endif
%if %{with libcgroup}
	--enable-libcgroup \
%endif
	--with-initddir=%{_initrddir} \
	--with-systemddir=%{_unitdir} \
	--with-upstartdir=%{_sysconfdir}/init \
	--with-tmpfilesdir=%{_tmpfilesdir}

make %{_smp_mflags}

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot}

%if %{with dbus}
mkdir -p -m 0700 %{buildroot}/%{_sysconfdir}/dbus-1/system.d
install -m 644 %{_builddir}/%{name}-%{version}%{?gittarver}/conf/corosync-signals.conf %{buildroot}/%{_sysconfdir}/dbus-1/system.d/corosync-signals.conf
%endif

## tree fixup
# drop static libs
rm -f %{buildroot}%{_libdir}/*.a
rm -f %{buildroot}%{_libdir}/*.la
# drop docs and html docs for now
rm -rf %{buildroot}%{_docdir}/*
# /etc/sysconfig/corosync-notifyd
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 tools/corosync-notifyd.sysconfig.example \
   %{buildroot}%{_sysconfdir}/sysconfig/corosync-notifyd
# /etc/sysconfig/corosync
install -m 644 init/corosync.sysconfig.example \
   %{buildroot}%{_sysconfdir}/sysconfig/corosync

%if %{with qdevices}
# /etc/sysconfig/corosync-qdevice
install -m 644 init/corosync-qdevice.sysconfig.example \
   %{buildroot}%{_sysconfdir}/sysconfig/corosync-qdevice
%endif

%if %{with qnetd}
# /etc/sysconfig/corosync-qnetd
install -m 644 init/corosync-qnetd.sysconfig.example \
   %{buildroot}%{_sysconfdir}/sysconfig/corosync-qnetd
%if %{with systemd}
sed -i -e 's/^#User=/User=/' \
   %{buildroot}%{_unitdir}/corosync-qnetd.service
sed -i -e 's/root/coroqnetd/g' \
   %{buildroot}%{_tmpfilesdir}/corosync-qnetd.conf
%else
sed -i -e 's/^COROSYNC_QNETD_RUNAS=""$/COROSYNC_QNETD_RUNAS="coroqnetd"/' \
   %{buildroot}%{_sysconfdir}/sysconfig/corosync-qnetd
%endif
%endif

%clean
rm -rf %{buildroot}

%description
This package contains the Corosync Cluster Engine Executive, several default
APIs and libraries, default configuration files, and an init script.

%post
%if %{with systemd} && 0%{?systemd_post:1}
%systemd_post corosync.service
%else
if [ $1 -eq 1 ]; then
	/sbin/chkconfig --add corosync || :
fi
%endif

%preun
%if %{with systemd} && 0%{?systemd_preun:1}
%systemd_preun corosync.service
%else
if [ $1 -eq 0 ]; then
	/sbin/service corosync stop &>/dev/null || :
	/sbin/chkconfig --del corosync || :
fi
%endif

%postun
%if %{with systemd} && 0%{?systemd_postun:1}
%systemd_postun
%endif

%files
%defattr(-,root,root,-)
%doc LICENSE SECURITY
%{_sbindir}/corosync
%{_sbindir}/corosync-keygen
%{_sbindir}/corosync-cmapctl
%{_sbindir}/corosync-cfgtool
%{_sbindir}/corosync-cpgtool
%{_sbindir}/corosync-quorumtool
%{_sbindir}/corosync-notifyd
%{_bindir}/corosync-blackbox
%if %{with xmlconf}
%{_bindir}/corosync-xmlproc
%config(noreplace) %{_sysconfdir}/corosync/corosync.xml.example
%dir %{_datadir}/corosync
%{_datadir}/corosync/xml2conf.xsl
%{_mandir}/man8/corosync-xmlproc.8*
%{_mandir}/man5/corosync.xml.5*
%endif
%dir %{_sysconfdir}/corosync
%dir %{_sysconfdir}/corosync/uidgid.d
%config(noreplace) %{_sysconfdir}/corosync/corosync.conf.example
%config(noreplace) %{_sysconfdir}/corosync/corosync.conf.example.udpu
%config(noreplace) %{_sysconfdir}/sysconfig/corosync-notifyd
%config(noreplace) %{_sysconfdir}/sysconfig/corosync
%config(noreplace) %{_sysconfdir}/logrotate.d/corosync
%if %{with dbus}
%{_sysconfdir}/dbus-1/system.d/corosync-signals.conf
%endif
%if %{with snmp}
%{_datadir}/snmp/mibs/COROSYNC-MIB.txt
%endif
%if %{with systemd}
%{_unitdir}/corosync.service
%{_unitdir}/corosync-notifyd.service
%dir %{_datadir}/corosync
%{_datadir}/corosync/corosync
%{_datadir}/corosync/corosync-notifyd
%else
%{_initrddir}/corosync
%{_initrddir}/corosync-notifyd
%endif
%if %{with upstart}
%{_sysconfdir}/init/corosync.conf
%{_sysconfdir}/init/corosync-notifyd.conf
%endif
%dir %{_localstatedir}/lib/corosync
%dir %{_localstatedir}/log/cluster
%{_mandir}/man8/corosync_overview.8*
%{_mandir}/man8/corosync.8*
%{_mandir}/man8/corosync-blackbox.8*
%{_mandir}/man8/corosync-cmapctl.8*
%{_mandir}/man8/corosync-keygen.8*
%{_mandir}/man8/corosync-cfgtool.8*
%{_mandir}/man8/corosync-cpgtool.8*
%{_mandir}/man8/corosync-notifyd.8*
%{_mandir}/man8/corosync-quorumtool.8*
%{_mandir}/man5/corosync.conf.5*
%{_mandir}/man5/votequorum.5*
%{_mandir}/man8/cmap_keys.8*

# optional testagent rpm
#
%if %{with testagents}

%package -n corosync-testagents
Summary: The Corosync Cluster Engine Test Agents
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libqb >= 0.14.2

%description -n corosync-testagents
This package contains corosync test agents.

%files -n corosync-testagents
%defattr(755,root,root,-)
%{_datadir}/corosync/tests/mem_leak_test.sh
%{_datadir}/corosync/tests/net_breaker.sh
%{_datadir}/corosync/tests/cmap-dispatch-deadlock.sh
%{_datadir}/corosync/tests/shm_leak_audit.sh
%{_bindir}/cpg_test_agent
%{_bindir}/sam_test_agent
%{_bindir}/votequorum_test_agent

%endif

# library
#
%package -n corosynclib
Summary: The Corosync Cluster Engine Libraries
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description -n corosynclib
This package contains corosync libraries.

%files -n corosynclib
%defattr(-,root,root,-)
%doc LICENSE
%{_libdir}/libcfg.so.*
%{_libdir}/libcpg.so.*
%{_libdir}/libcmap.so.*
%{_libdir}/libtotem_pg.so.*
%{_libdir}/libquorum.so.*
%{_libdir}/libvotequorum.so.*
%{_libdir}/libsam.so.*
%{_libdir}/libcorosync_common.so.*

%post -n corosynclib -p /sbin/ldconfig

%postun -n corosynclib -p /sbin/ldconfig

%package -n corosynclib-devel
Summary: The Corosync Cluster Engine Development Kit
Group: Development/Libraries
Requires: corosynclib = %{version}-%{release}
Requires: pkgconfig
Provides: corosync-devel = %{version}
Obsoletes: corosync-devel < 0.92-7

%description -n corosynclib-devel
This package contains include files and man pages used to develop using
The Corosync Cluster Engine APIs.

%files -n corosynclib-devel
%defattr(-,root,root,-)
%doc LICENSE
%dir %{_includedir}/corosync/
%{_includedir}/corosync/corodefs.h
%{_includedir}/corosync/cfg.h
%{_includedir}/corosync/cmap.h
%{_includedir}/corosync/corotypes.h
%{_includedir}/corosync/cpg.h
%{_includedir}/corosync/hdb.h
%{_includedir}/corosync/sam.h
%{_includedir}/corosync/quorum.h
%{_includedir}/corosync/votequorum.h
%dir %{_includedir}/corosync/totem/
%{_includedir}/corosync/totem/totem.h
%{_includedir}/corosync/totem/totemip.h
%{_includedir}/corosync/totem/totempg.h
%{_libdir}/libcfg.so
%{_libdir}/libcpg.so
%{_libdir}/libcmap.so
%{_libdir}/libtotem_pg.so
%{_libdir}/libquorum.so
%{_libdir}/libvotequorum.so
%{_libdir}/libsam.so
%{_libdir}/libcorosync_common.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/cpg_*3*
%{_mandir}/man3/quorum_*3*
%{_mandir}/man3/votequorum_*3*
%{_mandir}/man3/sam_*3*
%{_mandir}/man8/cpg_overview.8*
%{_mandir}/man8/votequorum_overview.8*
%{_mandir}/man8/sam_overview.8*
%{_mandir}/man3/cmap_*3*
%{_mandir}/man8/cmap_overview.8*
%{_mandir}/man8/quorum_overview.8*

# optional qdevices
#
%if %{with qdevices}

%package -n corosync-qdevice
Summary: The Corosync Cluster Engine Qdevice
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}
Requires: corosynclib = %{version}-%{release}
Requires: nss-tools

%if %{with systemd}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

%description -n corosync-qdevice
This package contains the Corosync Cluster Engine Qdevice, script for creating
NSS certificates and an init script.

%post -n corosync-qdevice
%if %{with systemd} && 0%{?systemd_post:1}
%systemd_post corosync-qdevice.service
%else
if [ $1 -eq 1 ]; then
	/sbin/chkconfig --add corosync-qdevice || :
fi
%endif

%preun -n corosync-qdevice
%if %{with systemd} && 0%{?systemd_preun:1}
%systemd_preun corosync-qdevice.service
%else
if [ $1 -eq 0 ]; then
	/sbin/service corosync-qdevice stop &>/dev/null || :
	/sbin/chkconfig --del corosync-qdevice || :
fi
%endif

%postun -n corosync-qdevice
%if %{with systemd} && 0%{?systemd_postun:1}
%systemd_postun
%endif

%files -n corosync-qdevice
%defattr(-,root,root,-)
%dir %{_sysconfdir}/corosync/qdevice
%dir %config(noreplace) %{_sysconfdir}/corosync/qdevice/net
%dir %{_localstatedir}/run/corosync-qdevice
%{_sbindir}/corosync-qdevice
%{_sbindir}/corosync-qdevice-net-certutil
%{_sbindir}/corosync-qdevice-tool
%config(noreplace) %{_sysconfdir}/sysconfig/corosync-qdevice
%if %{with systemd}
%{_unitdir}/corosync-qdevice.service
%dir %{_datadir}/corosync
%{_datadir}/corosync/corosync-qdevice
%else
%{_initrddir}/corosync-qdevice
%endif
%{_mandir}/man8/corosync-qdevice-tool.8*
%{_mandir}/man8/corosync-qdevice-net-certutil.8*
%{_mandir}/man8/corosync-qdevice.8*
%endif

# optional qnetd
#
%if %{with qnetd}

%package -n corosync-qnetd
Summary: The Corosync Cluster Engine Qdevice Network Daemon
Group: System Environment/Base
Requires: nss-tools
Requires(pre): shadow-utils

%if %{with systemd}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

%description -n corosync-qnetd
This package contains the Corosync Cluster Engine Qdevice Network Daemon, script for creating
NSS certificates and an init script.

%pre -n corosync-qnetd
getent group coroqnetd >/dev/null || groupadd -r coroqnetd
getent passwd coroqnetd >/dev/null || \
    useradd -r -g coroqnetd -d / -s /sbin/nologin -c "User for corosync-qnetd" coroqnetd
exit 0

%post -n corosync-qnetd
%if %{with systemd} && 0%{?systemd_post:1}
%systemd_post corosync-qnetd.service
%else
if [ $1 -eq 1 ]; then
	/sbin/chkconfig --add corosync-qnetd || :
fi
%endif

%preun -n corosync-qnetd
%if %{with systemd} && 0%{?systemd_preun:1}
%systemd_preun corosync-qnetd.service
%else
if [ $1 -eq 0 ]; then
	/sbin/service corosync-qnetd stop &>/dev/null || :
	/sbin/chkconfig --del corosync-qnetd || :
fi
%endif

%postun -n corosync-qnetd
%if %{with systemd} && 0%{?systemd_postun:1}
%systemd_postun
%endif

%files -n corosync-qnetd
%defattr(-,root,root,-)
%dir %config(noreplace) %attr(770, coroqnetd, coroqnetd) %{_sysconfdir}/corosync/qnetd
%dir %attr(770, coroqnetd, coroqnetd) %{_localstatedir}/run/corosync-qnetd
%{_bindir}/corosync-qnetd
%{_bindir}/corosync-qnetd-certutil
%{_bindir}/corosync-qnetd-tool
%config(noreplace) %{_sysconfdir}/sysconfig/corosync-qnetd
%if %{with systemd}
%{_unitdir}/corosync-qnetd.service
%dir %{_datadir}/corosync
%{_datadir}/corosync/corosync-qnetd
%{_tmpfilesdir}/corosync-qnetd.conf
%else
%{_initrddir}/corosync-qnetd
%endif
%{_mandir}/man8/corosync-qnetd-tool.8*
%{_mandir}/man8/corosync-qnetd-certutil.8*
%{_mandir}/man8/corosync-qnetd.8*
%endif

%changelog
* Fri Apr 06 2018 Jan Friesse <jfriesse@redhat.com> 2.4.3-2.1
- Resolves: rhbz#1560467

- totemcrypto: Check length of the packet

* Mon Feb 05 2018 Jan Friesse <jfriesse@redhat.com> 2.4.3-2
- Resolves: rhbz#1536219

- logging: Make blackbox configurable (rhbz#1536219)
- merge upstream commit 8af39f66e56e319b6b93804c0400e6e29737a90f (rhbz#1536219)
- logging: Close before and open blackbox after fork (rhbz#1536219)
- merge upstream commit 995ed0bd814ff3eacf6c09534841e6ce39ab6614 (rhbz#1536219)

* Fri Oct 20 2017 Jan Friesse <jfriesse@redhat.com> 2.4.3-1
- Resolves: rhbz#1413573
- Resolves: rhbz#1503008

* Tue Oct 17 2017 Jan Friesse <jfriesse@redhat.com> 2.4.0-10
- Resolves: rhbz#1439205
- Resolves: rhbz#1461450
- Resolves: rhbz#1469170
- Resolves: rhbz#1476214

- main: Don't ask libqb to handle segv, it doesn't work (rhbz#1439205)
- merge upstream commit c0da36a6c0ecf7bc7def252a06336a7088e68086 (rhbz#1439205)
- totem: Propagate totem initialization failure (rhbz#1461450)
- merge upstream commit 0413a8f4672352171f0df731b7d9c1fe20acbc4c (rhbz#1461450)
- totemcrypto: Refactor symmetric key importing (rhbz#1461450)
- merge upstream commit a885868181c07ba9ab5cdfdad1d66d387b2a4428 (rhbz#1461450)
- totemcrypto: Use different method to import key (rhbz#1461450)
- merge upstream commit 5dadebd21862074deaeb9a337fc9e49f5e9f692a (rhbz#1461450)
- main: Add option to set priority (rhbz#1469170)
- merge upstream commit a008448efb2b1d45c432867caf08f0bcf2b4b9b0 (rhbz#1469170)
- main: Add support for libcgroup (rhbz#1476214)
- merge upstream commit c56086c701d08fc17cf6d8ef603caf505a4021b7 (rhbz#1476214)
- totemcrypto: Fix compiler warning (rhbz#1461450)
- merge upstream commit fdeed33f514e0056e322a45d9a0a04ca4b9a2709 (rhbz#1461450)

* Wed Apr 26 2017 Jan Friesse <jfriesse@redhat.com> 2.4.0-9
- Resolves: rhbz#1445001

- Main: Call mlockall after fork (rhbz#1445001)
- merge upstream commit 238e2e62d8b960e7c10bfa0a8281d78ec99f3a26 (rhbz#1445001)
- Disable aarch64 build (bz#1422598)

* Wed Mar 22 2017 Jan Friesse <jfriesse@redhat.com> 2.4.0-8
- Resolves: rhbz#1434528
- Resolves: rhbz#1434529
- Resolves: rhbz#1434534

- cfg: Prevents use of uninitialized buffer (rhbz#1434528)
- merge upstream commit 52e6ae57ea06d0bef61c5c9250881bef1372ead2 (rhbz#1434528)
- man: Fix typos in man page (rhbz#1434529)
- merge upstream commit b642904ea9640bd7a1573a8c0d2c5bcb43a10dfc (rhbz#1434529)
- Fix typo: Destorying -> Destroying (rhbz#1434529)
- merge upstream commit 117d9e4eb77ef9941fdeaf17ddfd892514da8143 (rhbz#1434529)
- init: Add doc URIs to the systemd service files (rhbz#1434529)
- merge upstream commit 21a728785027483786e41c19f6aff57a95b80aa5 (rhbz#1434529)
- man: Modify man-page according to command usage (rhbz#1434529)
- merge upstream commit 79898e8cb1715e79b7467b91661b7341e2664550 (rhbz#1434529)
- Totempg: remove duplicate memcpy in mcast_msg func (rhbz#1434528)
- merge upstream commit 4a8e9d80409590cb42732ae3105b5ae71fda52c1 (rhbz#1434528)
- upstart: Add softdog module loading example (rhbz#1434529)
- merge upstream commit 75474d69bebea6c9c4ef2252476ce738cf92f0f4 (rhbz#1434529)
- Remove deprecated doxygen flags (rhbz#1434529)
- merge upstream commit b252013e42007ea7284ae54d035a30ca40f20fc0 (rhbz#1434529)
- Remove redundant header file inclusion (rhbz#1434528)
- merge upstream commit d6c7ade277a4a23d84c56d7fde6b60b377a1023b (rhbz#1434528)
- Qdevice: fix spell errors in qdevice (rhbz#1434529)
- merge upstream commit d9caa09c45d4560c89a1ad873087c0476cabab46 (rhbz#1434529)
- doc: document watchdog_device parameter (rhbz#1434529)
- merge upstream commit a5f97ae1b99063383d8f45168125b34232b91faf (rhbz#1434529)
- Logsys: Change logsys syslog_priority priority (rhbz#1434534)
- merge upstream commit 609cc0cc100aa1070d97b405273373682da0e270 (rhbz#1434534)
- logconfig: Do not overwrite logger_subsys priority (rhbz#1434534)
- merge upstream commit c866a2f8603b44e89eb21a6cf7d88134af2e8b66 (rhbz#1434534)

* Tue Mar 21 2017 Jan Friesse <jfriesse@redhat.com> 2.4.0-7
- Related: rhbz#1371880

- Fix build on RHEL7.3 latest (rhbz#1371880)
- merge upstream commit 19e48a6eee20d5f34f79a3b8d4e1c694169c1d7b (rhbz#1371880)
- Enable aarch64 build (bz#1422598)

* Tue Mar 21 2017 Jan Friesse <jfriesse@redhat.com> 2.4.0-6
- Resolves: rhbz#1371880

- libvotequorum: Bump version (rhbz#1371880)
- merge upstream commit 96f91f23a6a413535cc2f0e8492e2300373fed40 (rhbz#1371880)
- votequorum: Don't update expected_votes display if value is too high (rhbz#1371880)
- merge upstream commit 596433066805af029be1292a37a35ce31307f0bf (rhbz#1371880)
- votequorum: simplify reconfigure message handling (rhbz#1371880)
- merge upstream commit 4a385f2e94c7168dbd92168c54a80ee97a3c2140 (rhbz#1371880)

* Thu Jan 19 2017 Jan Friesse <jfriesse@redhat.com> 2.4.0-5
- Resolves: rhbz#1289661

- Enable ppc64le build

* Wed Aug 31 2016 Jan Friesse <jfriesse@redhat.com> 2.4.0-4
- Resolves: rhbz#1367813

- Man: Fix corosync-qdevice-net-certutil link (rhbz#1367813)
- merge upstream commit 49a9f722bba13e4b2762151b7b96b1d4196fd5e0 (rhbz#1367813)
- man: mention qdevice incompatibilites in votequorum.5 (rhbz#1367813)
- merge upstream commit 0da1b7446239424b76b1d5eb7c3640afce9b054e (rhbz#1367813)
- Qnetd LMS: Fix two partition use case (rhbz#1367813)
- merge upstream commit b0c850f308d44ddcdf1a1f881c1e1142ad489385 (rhbz#1367813)

* Thu Aug 04 2016 Jan Friesse <jfriesse@redhat.com> 2.4.0-3
- Related: rhbz#1363654

- Enhance spec so corosync-qdevice subpackage depends on same version of
  the corosync and corosynclib packages.

* Thu Aug 04 2016 Jan Friesse <jfriesse@redhat.com> 2.4.0-2
- Resolves: rhbz#1363654

- Config: Flag config uidgid entries (rhbz#1363654)
- merge upstream commit f837f95dfe96d60f2367e900efd4def7a07b2a89 (rhbz#1363654)

* Thu Jun 30 2016 Jan Friesse <jfriesse@redhat.com> 2.4.0-1
- Resolves: rhbz#614122
- Resolves: rhbz#1185000
- Resolves: rhbz#1306680

* Thu Jun 16 2016 Jan Friesse <jfriesse@redhat.com> 2.3.6-1
- Related: rhbz#1306680
- Resolves: rhbz#1289169
- Resolves: rhbz#1306349
- Resolves: rhbz#1282372
- Resolves: rhbz#1317573
- Resolves: rhbz#1336462

- Rebase to Corosync 2.3.6

* Mon Jun 22 2015 Jan Friesse <jfriesse@redhat.com> 2.3.4-7
- Related: rhbz#682771

- Don't link with libz when not needed (rhbz#682771)
- merge upstream commit 145f9279d12cf0b981494bbd4dabbc9c3641378e (rhbz#682771)

* Mon Jun 22 2015 Jan Friesse <jfriesse@redhat.com> 2.3.4-6
- Resolves: rhbz#1170347
- Resolves: rhbz#1225441
- Resolves: rhbz#1226842
- Resolves: rhbz#1229194
- Resolves: rhbz#1234261
- Resolves: rhbz#1234266
- Resolves: rhbz#682771
- Resolves: rhbz#773464

- config: Make sure user doesn't mix IPv6 and IPv4 (rhbz#773464)
- merge upstream commit 6c028d4d9c53decaa9469c792ac68fd2a886e7d9 (rhbz#773464)
- config: Process broadcast option consistently (rhbz#773464)
- merge upstream commit 70bd35fc06e68a010d780dfa39bd68d4bd2f7da7 (rhbz#773464)
- config: Ensure mcast address/port differs for rrp (rhbz#773464)
- merge upstream commit 6449bea835c90045baa23e3e041fed1df2abf070 (rhbz#773464)
- Reset timer_problem_decrementer on fault (rhbz#1234261)
- merge upstream commit 8f284b26b3331e1ab252969ba65543e6d9217ab1 (rhbz#1234261)
- automake: Check minimum automake version (rhbz#773464)
- merge upstream commit 114b826c67126fe1f690ad976b5217a8487994a4 (rhbz#773464)
- Set RR priority by default (rhbz#1170347)
- merge upstream commit 177ef0e5240b4060ff5b14eab6f2eefee3aa777d (rhbz#1170347)
- Log auto-recovery of ring only once (rhbz#773464)
- merge upstream commit e0ac861efdc32831366a2b5f5cc1d61e2ffa5504 (rhbz#773464)
- totem: Ignore duplicated commit tokens in recovery (rhbz#1234261)
- merge upstream commit 4ee84c51fa73c4ec7cbee922111a140a3aaf75df (rhbz#1234261)
- corosync_ring_id_store: Use safer permissions (rhbz#1234266)
- merge upstream commit 252b38ab8a62ff083e83b1d6f514109f7b7cbb42 (rhbz#1234266)
- totemsrp: Format member list log as unsigned int (rhbz#773464)
- merge upstream commit 5d9acc5604eb4e8a739cb37a4ad46bcc5ad8deb6 (rhbz#773464)
- cpg: Add support for messages larger than 1Mb (rhbz#682771)
- merge upstream commit 8cc8e513633a1a8b12c416e32fb5362fcf4d65dd (rhbz#682771)
- Really add cpghum (rhbz#682771)
- merge upstream commit 3842ba6080e00fd9484a2a875d982e149f67bc44 (rhbz#682771)
- quorum: don't allow quorum_trackstart to be called twice (rhbz#1229194)
- merge upstream commit 82526d2fe9137e8b604f1bbae6d6e39ba41377f9 (rhbz#1229194)
- totemconfig: Check for duplicate nodeids (rhbz#773464)
- merge upstream commit 997074cc3e1ea425ca63e453b7e2181741bdcef0 (rhbz#773464)
- totem: Log a message if JOIN or LEAVE message is ignored (rhbz#773464)
- merge upstream commit 53f67a2a7914228f1a406aad61ea6768525e11b0 (rhbz#773464)
- totemsrp: Improve logging of left/down nodes (rhbz#773464)
- merge upstream commit ab8942f6260fde93824ed2a18e09e572b59ceb25 (rhbz#773464)
- votequorum: Fix auto_tie_breaker behaviour in odd-sized clusters (rhbz#1229194)
- merge upstream commit b9f5c290b7dedd0a677cdfc25db7dd111245a745 (rhbz#1229194)
- Add note about rrp active beeing unsupported (rhbz#1226842)
- merge upstream commit 219965f4fe694eaaf2eb4ea05cdc7e35f5146114 (rhbz#1226842)
- Log: Add logrotate configuration file (rhbz#1225441)
- merge upstream commit aabbace625b3c68332b4356887378fca81f8f387 (rhbz#1225441)

* Wed Mar 25 2015 Jan Friesse <jfriesse@redhat.com> 2.3.4-5
- Resolves: rhbz#1197091
- Resolves: rhbz#1197671

- Votequorum: Fix auto_tie_breaker default (rhbz#1197091)
- merge upstream commit 314a01c98e5f98ff686333966dbe675935b7b6a8 (rhbz#1197091)
- Don't allow both two_node and auto_tie_breaker in corosync.conf (rhbz#1197671)
- merge upstream commit c832ade034fa737561ccabefbe417c9d7855d970 (rhbz#1197671)

* Wed Jan 21 2015 Jan Friesse <jfriesse@redhat.com> 2.3.4-4
- Resolves: rhbz#1184154

- Handle adding and removing UDPU members atomically (rhbz#1184154)
- merge upstream commit d77cec24d0025d353681762fe707794c621665c7 (rhbz#1184154)

* Mon Oct 13 2014 Jan Friesse <jfriesse@redhat.com> 2.3.4-3
- Resolves: rhbz#1078361
- Resolves: rhbz#1136429
- Resolves: rhbz#1149916

- [crypto] fix crypto block rounding/padding calculation (rhbz#1136429)
- merge upstream commit 239e2397820f9fa7ef430ebef0947ec1246eb50f (rhbz#1136429)
- Adjust MTU for IPv6 correctly (rhbz#1136429)
- merge upstream commit 03f95ddaa1d223e1e93788a307dc1b36d86b22b5 (rhbz#1136429)
- init: Don't wait for ipc if corosync doesn't start (rhbz#1149916)
- merge upstream commit b627844f3d5c5788bd8bb140d8852ba666da16aa (rhbz#1149916)
- manpage: Fix English (rhbz#1078361)
- merge upstream commit f77a61ac1795e794244440e1bfe804f02cc5d2b6 (rhbz#1078361)
- Store configuration values used by totem to cmap (rhbz#1078361)
- merge upstream commit bb52fc2774ef690d6bb951fe9cc34e5b373caffe (rhbz#1078361)
- man page: Improve description of token timeout (rhbz#1078361)
- merge upstream commit 57539d1abc09e5aef322cb9cca5b3e6c496cfae9 (rhbz#1078361)

* Fri Sep 12 2014 Fabio M. Di Nitto <fdinitto@redhat.com> 2.3.4-2
- Resolves: rhbz#1140915

* Tue Aug 26 2014 Jan Friesse <jfriesse@redhat.com> 2.3.4-1
- Resolves: rhbz#1108522

* Tue Aug 26 2014 Jan Friesse <jfriesse@redhat.com> 2.3.3-3
- Resolves: rhbz#1059607
- Resolves: rhbz#1069254
- Resolves: rhbz#1074673
- Resolves: rhbz#1078361
- Resolves: rhbz#1078363
- Resolves: rhbz#1085468
- Resolves: rhbz#1086233
- Resolves: rhbz#1108508
- Resolves: rhbz#1108511
- Resolves: rhbz#1108522
- Resolves: rhbz#1108525
- Resolves: rhbz#1108708
- Resolves: rhbz#1117911

- Free object allocated at quorum_register_callback (rhbz#1059607)
- merge upstream commit fa71067a93ea99d8dc4812e3a028ae154216a91a (rhbz#1059607)
- votequorum: Add extended options to auto_tie_breaker (rhbz#1059607)
- merge upstream commit 90d448af3b4b4508ca890cce67113cb226475d3b (rhbz#1059607)
- totemsrp: Fix typo with cont gather (rhbz#1108508)
- merge upstream commit 38c04d9a66ba41dae14a57eba119dabb31cbb18f (rhbz#1108508)
- mon: Make mon compilable with libstatgrab ver 0.9 (rhbz#1108511)
- merge upstream commit e1e2390b61fb5d47a8639f2538721675dd411b08 (rhbz#1108511)
- mon: Fix comparsion typo (rhbz#1108511)
- merge upstream commit 57ff693b70cb7aaa81e52e9d24f38aa0399a8c46 (rhbz#1108511)
- mon: Pass correct pointer to inst (rhbz#1108511)
- merge upstream commit 099f704cdddfb3b72fe93fb1f4fc777672eb9fdf (rhbz#1108511)
- mon: Make monitoring work (rhbz#1108511)
- merge upstream commit ff67daa55f6cfcb48357a8fddaa312b9fb49602b (rhbz#1108511)
- votequorum: Properly initialize atb and atb_string (rhbz#1059607)
- merge upstream commit e1801ba49738a3ae2ba3ca08c2b74dda5ff9056c (rhbz#1059607)
- config: Handle totem_set_volatile_defaults errors (rhbz#1078361)
- merge upstream commit 2f0cad20a9a368683fd59a869b2cb360bd31f95b (rhbz#1078361)
- Log: Make reload of logging work (rhbz#1078361)
- merge upstream commit 1b6abcc7d5afd4651efcdba1a65effb259f6ee3e (rhbz#1078361)
- Really clear totemconfig nodes on reload (rhbz#1078361)
- merge upstream commit eeb2384157351ff460be0648d954e5e97213d532 (rhbz#1078361)
- totemconfig: Key change process dependencies (rhbz#1078361)
- merge upstream commit b95ebd640eb45267d69822c8292a0098a8e4180e (rhbz#1078361)
- totemconfig: Log errors on key change and reload (rhbz#1078361)
- merge upstream commit 9a8de87c34071f54a9e3b545a1a7460d64568579 (rhbz#1078361)
- Add token_coefficient option (rhbz#1078361)
- merge upstream commit 58176d6779a0f5ff23dabf61dff7544db29af25a (rhbz#1078361)
- init: Make init script configurable (rhbz#1078363)
- merge upstream commit 1f7e78ab9cc686a7528ac4601651ded9d204b01f (rhbz#1078363)
- config: Allow dynamic change of token_coefficient (rhbz#1078361)
- merge upstream commit 7557fdec487cb5fad7c449949ba58496bd396458 (rhbz#1078361)
- upstart: Make job conf file configurable (rhbz#1108522)
- merge upstream commit d23ee6a3e0d5299f488bf9abed98f1853fd0e8b0 (rhbz#1108522)
- Indent: Remove space in negation of expression (rhbz#1108522)
- merge upstream commit b6e2c8024dd314ce17eac4f3f83a2320ebb7017d (rhbz#1108522)
- Indent: Remove newline before else branch start (rhbz#1108522)
- merge upstream commit d0dc9ae93c6f41ab9139242d754428fcf9bcc653 (rhbz#1108522)
- totemiba: Add multicast recovery (rhbz#1108522)
- merge upstream commit 4d6a18d8a5c0001f2eaeebb79d75f999c671cb74 (rhbz#1108522)
- totemiba: Fix incorrect failed log message (rhbz#1108522)
- merge upstream commit e905f92bf532c291d9be23b6a16d972f36d5d464 (rhbz#1108522)
- logsys: Log error if blackbox cannot be created (rhbz#1108525)
- merge upstream commit 19c5b63ff5fae43c2acf28ce95cca6460f500176 (rhbz#1108525)
- logsys: Log warning if flightrecorder init fails (rhbz#1108525)
- merge upstream commit 8f13a983204c2bc16c7490cee6db90138ecc43f1 (rhbz#1108525)
- Introduce get_run_dir function (rhbz#1108525)
- merge upstream commit d310b251c3ba5e92c7ca1b8f6f8197d71141a8d6 (rhbz#1108525)
- Move ringid store and load from totem library (rhbz#1108525)
- merge upstream commit da46ecfc3087de97ad9a76fe6a156f10170503a2 (rhbz#1108525)
- init: change return value when starting corosync (rhbz#1078363)
- merge upstream commit 7a6cc6b5a2f6ec5d88e52e34e62f18db1915afd7 (rhbz#1078363)
- Install doc: Correct a typo (rhbz#1108522)
- merge upstream commit a64696698718071e4e531a5a3332c363742c550b (rhbz#1108522)
- coroparse: More strict numbers parsing (rhbz#1108708)
- merge upstream commit 4e9716ed30ffe6a5750f5c6c2565815e88413c23 (rhbz#1108708)
- Doc: Enhance INSTALL file a bit (rhbz#1108522)
- merge upstream commit e8a5c56ab27fff4beef910804841d73aaa17a6a1 (rhbz#1108522)
- Make config.reload_in_progress key read only (rhbz#1085468)
- merge upstream commit c8e3f14fdb284aadf023d7e62c0f951181f21736 (rhbz#1085468)
- votequorum: Do not process events during reload (rhbz#1085468)
- merge upstream commit 72cf15af27ea9dbf918839ac44929ed9c65eea5e (rhbz#1085468)
- systemd: Config example for corosync wd service (rhbz#1108522)
- merge upstream commit f6d6a9b0a0ca99a201bb9e9353a05075b700bcbd (rhbz#1108522)
- fix memory leak produced by 'corosync -v' (rhbz#1117911)
- merge upstream commit cc80c8567d6eec1d136f9e85d2f8dfb957337eef (rhbz#1117911)
- Handle SIGSEGV and SIGABRT signals (rhbz#1117911)
- merge upstream commit 384760cb670836dc37e243f594612c6e68f44351 (rhbz#1117911)
- Fix compiler warning introduced by previous patch (rhbz#1117911)
- merge upstream commit dfaca4b10a005681230a81e229384b6cd239b4f6 (rhbz#1117911)
- corosync-cmapctl: Allow -p option to delete keys (rhbz#1108522)
- merge upstream commit 7a4bb37723777bf6bcd08035696d8d7317c0ce1d (rhbz#1108522)
- Implement config file testing mode (rhbz#1108522)
- merge upstream commit e3ffd4fedc8158cdb5057f9fe40b6459e3d85846 (rhbz#1108522)
- cleanup after test-driver (rhbz#1108522)
- merge upstream commit c7ebb09530349b7b1bbec7b1d9ef4b05ad186a63 (rhbz#1108522)
- be consistent in using CPPFLAGS vs CFLAGS (rhbz#1108522)
- merge upstream commit 84b9e5989aa4a7090aeccbeb6cb8910735274a65 (rhbz#1108522)
- Slightly rework corosync-keygen. (rhbz#1108522)
- merge upstream commit 520fe686c5e45f0f7143e749a3f6c2001a2ea0d7 (rhbz#1108522)
- totemconfig: Free ifaddrs list (rhbz#1108522)
- merge upstream commit dc35bfae6213256fd7f0d5bf4dd9d5fa0f77a6f6 (rhbz#1108522)
- totemconfig: totem_config_get_ip_version (rhbz#1108522)
- merge upstream commit 10c80f454e70b42fc394d3326af1eb81c4be0d75 (rhbz#1108522)
- totemconfig: refactor nodelist_to_interface func (rhbz#1108522)
- merge upstream commit 63bf09776fb84e939cd56ec2c2d1bbea97c2e0e1 (rhbz#1108522)
- corosync-keygen: Replace printf/exit call with err (rhbz#1108522)
- merge upstream commit 0ce8d51c6d989c4e62d8c1f3fc42785c4f3d250c (rhbz#1108522)
- config: Fix typos (rhbz#1108522)
- merge upstream commit 3b8365e80668eea55bdd3f7178693c82884331ae (rhbz#1108522)
- totemconfig: Make sure join timeout is less than consensus (rhbz#1074673)
- merge upstream commit 88dbb9f722122f04dc7c95681375a53a3a1301a5 (rhbz#1074673)
- votequorum: Return current ring id in callback (rhbz#1108522)
- merge upstream commit 5f6f68805c48f8f72f66f7fff9abc44b4c65df1e (rhbz#1108522)
- votequorum: Add ring id to poll call (rhbz#1108522)
- merge upstream commit b8902464d1b040326108ce7ec0934c1de5fe04ee (rhbz#1108522)
- ipc: Process votequorum messages during sync (rhbz#1108522)
- merge upstream commit 7cad804629fe7d936d098569122f84979959b554 (rhbz#1108522)
- votequorum: Block sync until qdevice poll (rhbz#1108522)
- merge upstream commit b4c99346352ce39cf96f7b12943811c896b89caa (rhbz#1108522)
- testvotequorum2: Opt for polling with old ringid (rhbz#1108522)
- merge upstream commit f8413350b2df4e37822e6d34e9337da87993d271 (rhbz#1108522)
- votequorum: Make qdev timeout in sync configurable (rhbz#1108522)
- merge upstream commit 17488909d4ae0dc948eb9a4a15133570faaf9c0b (rhbz#1108522)
- Cancel token holding while in retransmition (rhbz#1108522)
- merge upstream commit f135b680967aaef1d466f40170c75ae3e470e147 (rhbz#1108522)
- votequorum: Add cmap key to reset wait_for_all (rhbz#1086233)
- merge upstream commit cbf753405b7924e48aa1838cc1d14044229449b3 (rhbz#1086233)
- quorumtool: Sort output by nodeid (rhbz#1108522)
- merge upstream commit ddb017fa0e2026ee4f0d05e9bf780898c32c129a (rhbz#1108522)
- YKD: Fix loading of YKD quorum module (rhbz#1108522)
- merge upstream commit 02f58aec9cd53887aa1dfe1616fcbb32671987d4 (rhbz#1108522)
- corosync-quorumtool: add sort options (rhbz#1108522)
- merge upstream commit f53580c2c1c8fa621cbc18de81974811799bafd8 (rhbz#1108522)
- TODO: Remove TODO file (rhbz#1108522)
- merge upstream commit c9232d5d6cbfb1e4de9eb09afadda630ad4fee83 (rhbz#1108522)
- Makefile: Do not install TODO file (rhbz#1108522)
- merge upstream commit 4b7293da7a03253a7f96401642e1afb006e7750c (rhbz#1108522)
- totem: Inform RRP about membership changes (rhbz#1069254)
- merge upstream commit acb55cdb03808a4cea745b1b6a80c7ef1769880f (rhbz#1069254)
- totemnet: Add totemnet_member_set_active (rhbz#1069254)
- merge upstream commit 4c717942cf5f35902be630f393b81a03a81bb194 (rhbz#1069254)
- totemrrp: Implement *_membership_changed (rhbz#1069254)
- merge upstream commit 371a99e96147f600510bd9d819b92a4de94fcc30 (rhbz#1069254)
- totemudpu: Implement member_set_active (rhbz#1069254)
- merge upstream commit 71f1b99649329ab06309791d0a621d3cfbb74bdb (rhbz#1069254)
- totemudpu: Send msgs to all members occasionally (rhbz#1069254)
- merge upstream commit 2429481b96d895c366ca27c82a2bd7cfee55af15 (rhbz#1069254)

* Thu Feb 20 2014 Jan Friesse <jfriesse@redhat.com> 2.3.3-2
- Resolves: rhbz#1067028

- cpg: Refactor mh_req_exec_cpg_procleave (rhbz#1067028)
- merge upstream commit fcf26e03036b6ae5a8ef762ea0b5691a4f790c92 (rhbz#1067028)
- cpg: Make sure nodid is always logged as hex num (rhbz#1067028)
- merge upstream commit 83c63b247f4030fe8123df7c9f96d7a1c8e245b1 (rhbz#1067028)
- cpg: Make sure left nodes are really removed (rhbz#1067028)
- merge upstream commit fbe8768f1bbab6d546023d70e7f7b91a9dc213b0 (rhbz#1067028)

* Tue Jan 14 2014 Jan Friesse <jfriesse@redhat.com> - 2.3.3-1
- Resolves: rhbz#1030559
- Resolves: rhbz#1038652
- Resolves: rhbz#1052049

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.3.2-4
- Mass rebuild 2013-12-27

* Wed Dec 04 2013 Jan Friesse <jfriesse@redhat.com> 2.3.2-3
- Resolves: rhbz#1031832

- cfgtool: return error on reload failure (rhbz#1031832)
- merge upstream commit 7014f10123a634cf026491edc9a09d6044106116 (rhbz#1031832)

* Thu Nov 7 2013 Jan Friesse <jfriesse@redhat.com> 2.3.2-2
- Resolves: rhbz#1008561

- Drop support for IBA (rhbz#1008561)

* Mon Sep 16 2013 Jan Friesse <jfriesse@redhat.com> - 2.3.2-1
- Resolves: rhbz#998882

- New upstream release

* Mon Aug 19 2013 Jan Friesse <jfriesse@redhat.com> 2.3.1-3
- Resolves: rhbz#998362

- Fix scheduler pause-detection timeout (rhbz#998362)
- merge upstream commit 2740cfd1eac60714601c74df2137fe588b607866 (rhbz#998362)

* Wed Jul 17 2013 Andrew Beekhof <abeekhof@redhat.com> - 2.3.1-2
- Rebuild for snmp library bump

* Wed Jul 10 2013 Jan Friesse <jfriesse@redhat.com> - 2.3.1-1
- New upstream release
- Fix incorrect dates in specfile changelog section

* Mon Mar 25 2013 Jan Friesse <jfriesse@redhat.com> - 2.3.0-3
- Resolves: rhbz#925185

- Run autogen by default

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Jan Friesse <jfriesse@redhat.com> - 2.3.0-1
- New upstream release

* Wed Dec 12 2012 Jan Friesse <jfriesse@redhat.com> - 2.2.0-1
- New upstream release

* Thu Oct 11 2012 Jan Friesse <jfriesse@redhat.com> - 2.1.0-1
- New upstream release

* Fri Aug 3 2012 Steven Dake <sdake@redhat.com> - 2.0.1-3
- add groff as a BuildRequires as it is no longer installed in the buildroot

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012 Jan Friesse <jfriesse@redhat.com> - 2.0.1-1
- New upstream release

* Tue Apr 17 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 2.0.0-2
- Backport IPCS fix from master (ack by Steven)

* Tue Apr 10 2012 Jan Friesse <jfriesse@redhat.com> - 2.0.0-1
- New upstream release

* Thu Apr 05 2012 Karsten Hopp <karsten@redhat.com> 1.99.9-1.1
- bump release and rebuild on PPC

* Tue Mar 27 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.9-1
- New upstream release

* Fri Mar 16 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.8-1
- New upstream release

* Tue Mar  6 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.7-1
- New upstream release

* Tue Feb 28 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.6-1
- New upstream release

* Wed Feb 22 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.5-1
- New upstream release

* Tue Feb 14 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.4-1
- New upstream release

* Tue Feb 14 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.3-1
- New upstream release

* Tue Feb  7 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.99.2-1
- New upstream release
- Re-enable xmlconfig bits
- Ship cmap man pages
- Add workaround to usrmove breakage!!

* Thu Feb  2 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.99.1-2
- Add proper Obsoltes on openais/cman/clusterlib

* Wed Feb  1 2012 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.99.1-1
- New upstream release
- Temporary disable xml config (broken upstream tarball)

* Tue Jan 24 2012 Jan Friesse <jfriesse@redhat.com> - 1.99.0-1
- New upstream release

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 06 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.2-1
- New upstream release

* Thu Sep 08 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.1-2
- Add upstream fixes

* Tue Jul 26 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.1-1
- New upstream release

* Wed Jul 20 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.0-2
- Change attributes of cluster log directory

* Tue Jul 19 2011 Jan Friesse <jfriesse@redhat.com> - 1.4.0-1
- New upstream release
- Resync spec file with upstream changes

* Fri Jul 08 2011 Jan Friesse <jfriesse@redhat.com> - 1.3.2-1
- New upstream release

* Tue May 10 2011 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.3.1-1
- New upstream release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.3.0-1
- New upstream release
- drop upstream patch revision-2770.patch now included in release
- update spec file to ship corosync-blackbox

* Thu Sep  2 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.8-1
- New upstream release

* Thu Jul 29 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.7-1
- New upstream release

* Fri Jul  9 2010 Dan Horák <dan[at]danny.cz> - 1.2.6-2
- no InfiniBand stack on s390(x)

* Mon Jul  5 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.6-1
- New upstream release
- Resync spec file with upstream changes

* Tue May 25 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.3-1
- New upstream release
- Rediff revision 2770 patch

* Mon May 17 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.2-1
- New upstream release
- Add upstream trunk revision 2770 to add cpg_model_initialize api.
- Fix URL and Source0 entries.
- Add workaround to broken 1.2.2 Makefile with make -j.

* Wed Mar 24 2010 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.1-1
- New upstream release

* Tue Dec  8 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.2.0-1
- New upstream release
- Use global instead of define
- Update Source0 url
- Use more name macro around
- Cleanup install section. Init script is now installed by upstream
- Cleanup whitespace
- Don't deadlock between package upgrade and corosync condrestart
- Ship service.d config directory
- Fix Conflicts vs Requires
- Ship new sam library and man pages

* Fri Oct 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.2-1
- New upstream release fixes major regression on specific loads

* Wed Oct 21 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.1-1
- New upstream release

* Fri Sep 25 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.0-1
- New upstream release
- spec file updates:
  * enable IB support
  * explicitly define built-in features at configure time

* Tue Sep 22 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.1-1
- New upstream release
- spec file updates:
  * use proper configure macro

* Tue Jul 28 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.0-3
- spec file updates:
  * more consistent use of macros across the board
  * fix directory ownership

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul  8 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.0-1
- New upstream release

* Thu Jul  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.100-1
- New upstream release

* Sat Jun 20 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.98-1
- New upstream release
- spec file updates:
  * Drop corosync-trunk patch and alpha tag.
  * Fix alphatag vs buildtrunk handling.
  * Drop requirement on ais user/group and stop creating them.
  * New config file locations from upstream: /etc/corosync/corosync.conf.

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.97-1.svn2233
- spec file updates:
  * Update to svn version 2233 to include library linking fixes

* Wed Jun 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.97-1.svn2232
- New upstream release
- spec file updates:
  * Drop pkgconfig fix that's now upstream
  * Update to svn version 2232
  * Define buildtrunk if we are using svn snapshots
  * BuildRequires: nss-devel to enable nss crypto for network communication
  * Force autogen invokation if buildtrunk is defined
  * Whitespace cleanup
  * Stop shipping corosync.conf in favour of a generic example
  * Update file list

* Mon Mar 30 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.95-2
- Backport svn commit 1913 to fix pkgconfig files generation
  and unbreak lvm2 build.

* Tue Mar 24 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.95-1
- New upstream release
- spec file updates:
  * Drop alpha tag
  * Drop local patches (no longer required)
  * Allow to build from svn trunk by supporting rpmbuild --with buildtrunk 
  * BuildRequires autoconf automake if building from trunk
  * Execute autogen.sh if building from trunk and if no configure is available
  * Switch to use rpm configure macro and set standard install paths
  * Build invokation now supports _smp_mflags
  * Remove install section for docs and use proper doc macro instead
  * Add tree fixup bits to drop static libs and html docs (only for now)
  * Add LICENSE file to all subpackages
  * libraries have moved to libdir. Drop ld.so.conf.d corosync file
  * Update BuildRoot usage to preferred versions/names

* Tue Mar 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-5.svn1797
- Update the corosync-trunk patch for real this time.

* Tue Mar 10 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-4.svn1797
- Import fixes from upstream:
  * Cleanup logsys format init around to use default settings (1795)
  * logsys_format_set should use its own internal copy of format_buffer (1796)
  * Add logsys_format_get to logsys API (1797)
- Cherry pick svn1807 to unbreak CPG.

* Mon Mar  9 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-3.svn1794
- Import fixes from upstream:
  * Add reserve/release feature to totem message queue space (1793)
  * Fix CG shutdown (1794)

* Fri Mar  6 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-2.svn1792
- Import fixes from upstream:
  * Fix uninitialized memory. Spotted by valgrind (1788)
  * Fix logsys_set_format by updating the right bits (1789)
  * logsys: re-add support for timestamp  (1790)
  * Fix cpg crash (1791)
  * Allow logsys_format_set to reset to default (1792)

* Tue Mar  3 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.94-1
- New upstream release.
- Drop obsolete patches.
- Add soname bump patch that was missing from upstream.

* Wed Feb 25 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.93-4
- Add Makefile fix to install all corosync tools (commit r1780)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.93-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.93-2
- Rename gcc-4.4 patch to match svn commit (r1767).
- Backport patch from trunk (commit r1774) to fix quorum engine.

* Thu Feb 19 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.93-1
- New upstream release.
- Drop alphatag from spec file.
- Drop trunk patch.
- Update Provides for corosynclib-devel.
- Backport gcc-4.4 build fix from trunk.

* Mon Feb  2 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-7.svn1756
- Update to svn trunk at revision 1756 from upstream.
- Add support pkgconfig to devel package.
- Tidy up spec files by re-organazing sections according to packages.
- Split libraries from corosync to corosynclib.
- Rename corosync-devel to corosynclib-devel.
- Comply with multiarch requirements (libraries).

* Tue Jan 27 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-6.svn1750
- Update to svn trunk at revision 1750 from upstream.
- Include new quorum service in the packaging.

* Mon Dec 15 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-5.svn1709
- Update to svn trunk at revision 1709 from upstream.
- Update spec file to include new include files.

* Wed Dec 10 2008 Fabio M. Di Nitto <fdinitto@redhat.com> - 0.92-4.svn1707
- Update to svn trunk at revision 1707 from upstream.
- Update spec file to include new lcrso services and include file.

* Mon Oct 13 2008 Dennis Gilmore <dennis@ausil.us> - 0.92-3
- remove ExclusiveArch line

* Wed Sep 24 2008 Steven Dake <sdake@redhat.com> - 0.92-2
- Add conflicts for openais and openais-devel packages older then 0.90.

* Wed Sep 24 2008 Steven Dake <sdake@redhat.com> - 0.92-1
- New upstream release corosync-0.92.

* Sun Aug 24 2008 Steven Dake <sdake@redhat.com> - 0.91-3
- move logsys_overview.8.* to devel package.
- move shared libs to main package.

* Wed Aug 20 2008 Steven Dake <sdake@redhat.com> - 0.91-2
- use /sbin/service instead of calling init script directly.
- put corosync-objctl man page in the main package.
- change all initrddir to initddir for fedora 10 guidelines.

* Thu Aug 14 2008 Steven Dake <sdake@redhat.com> - 0.91-1
- First upstream packaged version of corosync for rawhide review.
