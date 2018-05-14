# Globals and defines to control package behavior (configure these as desired)

## User and group to use for nonprivileged services
%global uname hacluster
%global gname haclient

## Where to install Pacemaker documentation
%global pcmk_docdir %{_docdir}/%{name}

## GitHub entity that distributes source (for ease of using a fork)
%global github_owner ClusterLabs

## Upstream pacemaker version, and its package version (specversion
## can be incremented to build packages reliably considered "newer"
## than previously built packages with the same pcmkversion)
%global pcmkversion 1.1.18
%global specversion 11

## Upstream commit (or git tag, such as "Pacemaker-" plus the
## {pcmkversion} macro for an official release) to use for this package
%global commit 2b07d5c5a908998891c3317faa30328c108d3a91
## Since git v2.11, the extent of abbreviation is autoscaled by default
## (used to be constant of 7), so we need to convey it for non-tags, too.
%global commit_abbrev 7


# Define globals for convenient use later

## Workaround to use parentheses in other globals
%global lparen (
%global rparen )

## Short version of git commit
%define shortcommit %(c=%{commit}; case ${c} in
                      Pacemaker-*%{rparen} echo ${c:10};;
                      *%{rparen} echo ${c:0:%{commit_abbrev}};; esac)

## Whether this is a tagged release
%define tag_release %([ %{commit} != Pacemaker-%{shortcommit} ]; echo $?)

## Whether this is a release candidate (in case of a tagged release)
%define pre_release %([ "%{tag_release}" -eq 0 ] || {
                      case "%{shortcommit}" in *-rc[[:digit:]]*%{rparen} false;;
                      esac; }; echo $?)

## Whether this is a development branch
%define post_release %([ %{commit} = Pacemaker-%{shortcommit} ]; echo $?)

## Turn off auto-compilation of python files outside site-packages directory,
## so that the -libs-devel package is multilib-compliant (no *.py[co] files)
%global __os_install_post %(echo '%{__os_install_post}' | {
                            sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g'; })

## Heuristic used to infer bleeding-edge deployments that are
## less likely to have working versions of the documentation tools
%define bleeding %(test ! -e /etc/yum.repos.d/fedora-rawhide.repo; echo $?)

## Corosync version
%define cs_version %(pkg-config corosync --modversion 2>/dev/null | awk -F . '{print $1}')

## Where to install python site libraries (currently, this uses the unversioned
## python_sitearch macro to get the default system python, but at some point,
## we should explicitly choose python2_sitearch or python3_sitearch -- or both)
%define py_site %{?python_sitearch}%{!?python_sitearch:%(
  python -c 'from distutils.sysconfig import get_python_lib as gpl; print(gpl(1))' 2>/dev/null)}

## Whether this platform defaults to using CMAN
%define cman_native (0%{?el6} || (0%{?fedora} > 0 && 0%{?fedora} < 17))

## Whether this platform defaults to using systemd as an init system
## (needs to be evaluated prior to BuildRequires being enumerated and
## installed as it's intended to conditionally select some of these, and
## for that there are only few indicators with varying reliability:
## - presence of systemd-defined macros (when building in a full-fledged
##   environment, which is not the case with ordinary mock-based builds)
## - systemd-aware rpm as manifested with the presence of particular
##   macro (rpm itself will trivially always be present when building)
## - existence of /usr/lib/os-release file, which is something heavily
##   propagated by systemd project
## - when not good enough, there's always a possibility to check
##   particular distro-specific macros (incl. version comparison)
%define systemd_native (%{?_unitdir:1}%{!?_unitdir:0}%{nil \
  } || %{?__transaction_systemd_inhibit:1}%{!?__transaction_systemd_inhibit:0}%{nil \
  } || %(test -f /usr/lib/os-release; test $? -ne 0; echo $?))

## Upstream commit to use for nagios-agents-metadata package
%global nagios_hash 105ab8a


# Definitions for backward compatibility with older RPM versions

## Ensure the license macro behaves consistently (older RPM will otherwise
## overwrite it once it encounters "License:"). Courtesy Jason Tibbitts:
## https://pkgs.fedoraproject.org/cgit/rpms/epel-rpm-macros.git/tree/macros.zzz-epel?h=el6&id=e1adcb77
%if !%{defined _licensedir}
%define description %{lua:
    rpm.define("license %doc")
    print("%description")
}
%endif


# Define conditionals so that "rpmbuild --with <feature>" and
# "rpmbuild --without <feature>" can enable and disable specific features

## Add option to enable support for stonith/external fencing agents
%bcond_with stonithd

## Add option to create binaries suitable for use with profiling tools
%bcond_with profiling

## Add option to create binaries with coverage analysis
%bcond_with coverage

## Add option to generate documentation (requires Publican, Asciidoc and Inkscape)
%bcond_with doc

## Add option to prefix package version with "0."
## (so later "official" packages will be considered updates)
%bcond_with pre_release

## Add option to ship Upstart job files
%bcond_with upstart_job

## Add option to enable CMAN support
%bcond_with cman

## Add option to turn on SNMP / ESMTP support
%bcond_with snmp
%bcond_with esmtp

## Add option to turn off hardening of libraries and daemon executables
%bcond_without hardening


# Keep sane profiling data if requested
%if %{with profiling}

## Disable -debuginfo package and stripping binaries/libraries
%define debug_package %{nil}

%endif


# Define the release version
# (do not look at externally enforced pre-release flag for tagged releases
# as only -rc tags, captured with the second condition, implies that then)
%if (!%{tag_release} && %{with pre_release}) || 0%{pre_release}
%if 0%{pre_release}
%define pcmk_release 0.%{specversion}.%(s=%{shortcommit}; echo ${s: -3})
%else
%define pcmk_release 0.%{specversion}.%{shortcommit}.git
%endif
%else
%if 0%{tag_release}
%define pcmk_release %{specversion}
%else
# Never use the short commit in a RHEL release number
%define pcmk_release %{specversion}
%endif
%endif

Name:          pacemaker
Summary:       Scalable High-Availability cluster resource manager
Version:       %{pcmkversion}
Release:       %{pcmk_release}%{?dist}.2
%if %{defined _unitdir}
License:       GPLv2+ and LGPLv2+
%else
# initscript is Revised BSD
License:       GPLv2+ and LGPLv2+ and BSD
%endif
Url:           http://www.clusterlabs.org
Group:         System Environment/Daemons

# Hint: use "spectool -s 0 pacemaker.spec" (rpmdevtools) to check the final URL:
# https://github.com/ClusterLabs/pacemaker/archive/e91769e5a39f5cb2f7b097d3c612368f0530535e/pacemaker-e91769e.tar.gz
Source0:       https://github.com/%{github_owner}/%{name}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:       nagios-agents-metadata-%{nagios_hash}.tar.gz

# upstream commits
Patch1:        001-new-behavior.patch
Patch2:        002-fixes.patch
Patch3:        003-cleanup.patch
Patch4:        004-cleanup.patch
Patch5:        005-cleanup.patch
Patch6:        006-leaks.patch
Patch7:        007-bundles.patch
Patch8:        008-quorum.patch
Patch9:        009-crm_resource.patch
Patch10:       010-crm_master.patch
Patch11:       011-regression-tests.patch
Patch12:       012-notifs.patch
Patch13:       013-notifs-tests.patch
Patch14:       014-segfault.patch
Patch15:       015-fail-timeout.patch
Patch16:       016-crm_diff.patch
Patch17:       017-pending-notify.patch

# patches that aren't from upstream
Patch100:      lrmd-protocol-version.patch
Patch101:      rhbz-url.patch

BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
AutoReqProv:   on
Requires:      resource-agents
Requires:      %{name}-libs = %{version}-%{release}
Requires:      %{name}-cluster-libs = %{version}-%{release}
Requires:      %{name}-cli = %{version}-%{release}
Obsoletes:     rgmanager < 3.2.0
Provides:      rgmanager >= 3.2.0
Provides:      pcmk-cluster-manager

%{?systemd_requires}

ExclusiveArch: i686 x86_64 ppc64le s390x

# Pacemaker targets compatibility with python 2.6+ and 3.2+
Requires:      python >= 2.6
BuildRequires: python-devel >= 2.6

# Pacemaker requires a minimum libqb functionality
Requires:      libqb > 0.17.0
BuildRequires: libqb-devel > 0.17.0

# Basics required for the build (even if usually satisfied through other BRs)
BuildRequires: coreutils findutils grep sed

# Required for core functionality
BuildRequires: automake autoconf libtool pkgconfig libtool-ltdl-devel
## version lower bound for: G_GNUC_INTERNAL
BuildRequires: pkgconfig(glib-2.0) >= 2.6
BuildRequires: libxml2-devel libxslt-devel libuuid-devel
BuildRequires: bzip2-devel pam-devel

# Required for agent_config.h which specifies the correct scratch directory
BuildRequires: resource-agents

# RH patches are created by git, so we need git to apply them
BuildRequires: git

# Enables optional functionality
BuildRequires: ncurses-devel docbook-style-xsl
BuildRequires: bison byacc flex help2man gnutls-devel pkgconfig(dbus-1)

%if %{systemd_native}
BuildRequires: pkgconfig(systemd)
%endif

%if %{with cman} && %{cman_native}
BuildRequires: clusterlib-devel
# pacemaker initscript: cman initscript, fence_tool (+ some soft-dependencies)
# "post" scriptlet: ccs_update_schema
Requires:      cman
%endif

Requires:      corosync
BuildRequires: corosynclib-devel

%if %{with stonithd}
BuildRequires: cluster-glue-libs-devel
%endif

## (note no avoiding effect when building through non-customized mock)
%if !%{bleeding}
%if %{with doc}
BuildRequires: publican inkscape asciidoc
%endif
%endif

%description
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Corosync, CMAN and/or Linux-HA.

It supports more than 16 node clusters with significant capabilities
for managing resources and dependencies.

It will run scripts at initialization, when machines go up or down,
when related resources fail and can be configured to periodically check
resource health.

Available rpmbuild rebuild options:
  --with(out) : cman coverage doc stonithd hardening pre_release profiling

%package cli
License:       GPLv2+ and LGPLv2+
Summary:       Command line tools for controlling Pacemaker clusters
Group:         System Environment/Daemons
Requires:      %{name}-libs = %{version}-%{release}
Requires:      perl-TimeDate

%description cli
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Corosync, CMAN and/or Linux-HA.

The %{name}-cli package contains command line tools that can be used
to query and control the cluster from machines that may, or may not,
be part of the cluster.

%package -n %{name}-libs
License:       GPLv2+ and LGPLv2+
Summary:       Core Pacemaker libraries
Group:         System Environment/Daemons
Requires(pre): shadow-utils

%description -n %{name}-libs
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Corosync, CMAN and/or Linux-HA.

The %{name}-libs package contains shared libraries needed for cluster
nodes and those just running the CLI tools.

%package -n %{name}-cluster-libs
License:       GPLv2+ and LGPLv2+
Summary:       Cluster Libraries used by Pacemaker
Group:         System Environment/Daemons
Requires:      %{name}-libs = %{version}-%{release}

%description -n %{name}-cluster-libs
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Corosync, CMAN and/or Linux-HA.

The %{name}-cluster-libs package contains cluster-aware shared
libraries needed for nodes that will form part of the cluster nodes.

%package remote
%if %{defined _unitdir}
License:       GPLv2+ and LGPLv2+
%else
# initscript is Revised BSD
License:       GPLv2+ and LGPLv2+ and BSD
%endif
Summary:       Pacemaker remote daemon for non-cluster nodes
Group:         System Environment/Daemons
Requires:      %{name}-libs = %{version}-%{release}
Requires:      %{name}-cli = %{version}-%{release}
Requires:      resource-agents
Provides:      pcmk-cluster-manager
# -remote can be fully independent of systemd
%{?systemd_ordering}%{!?systemd_ordering:%{?systemd_requires}}

%description remote
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Corosync, CMAN and/or Linux-HA.

The %{name}-remote package contains the Pacemaker Remote daemon
which is capable of extending pacemaker functionality to remote
nodes not running the full corosync/cluster stack.

%package -n %{name}-libs-devel
License:       GPLv2+ and LGPLv2+
Summary:       Pacemaker development package
Group:         Development/Libraries
Requires:      %{name}-cts = %{version}-%{release}
Requires:      %{name}-libs = %{version}-%{release}
Requires:      %{name}-cluster-libs = %{version}-%{release}
Requires:      libtool-ltdl-devel libqb-devel libuuid-devel
Requires:      libxml2-devel libxslt-devel bzip2-devel glib2-devel
Requires:      corosynclib-devel

%description -n %{name}-libs-devel
Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Corosync, CMAN and/or Linux-HA.

The %{name}-libs-devel package contains headers and shared libraries
for developing tools for Pacemaker.

# NOTE: can be noarch if lrmd_test is moved to another subpackage
%package       cts
License:       GPLv2+ and LGPLv2+
Summary:       Test framework for cluster-related technologies like Pacemaker
Group:         System Environment/Daemons
Requires:      python >= 2.6
Requires:      %{name}-libs = %{version}-%{release}

# systemd python bindings are separate package in some distros
%if %{defined systemd_requires}

%if 0%{?fedora} > 22
Requires:      python2-systemd
%else
%if 0%{?fedora} > 20 || 0%{?rhel} > 6
Requires:      systemd-python
%endif
%endif

%endif

%description   cts
Test framework for cluster-related technologies like Pacemaker

%package       doc
License:       CC-BY-SA-4.0
Summary:       Documentation for Pacemaker
Group:         Documentation

%description   doc
Documentation for Pacemaker.

Pacemaker is an advanced, scalable High-Availability cluster resource
manager for Corosync, CMAN and/or Linux-HA.

%package       nagios-plugins-metadata
License:       GPLv3
Summary:       Pacemaker Nagios Metadata
Group:         System Environment/Daemons
# NOTE below are the plugins this metadata uses.
# These plugin packages are currently not requirements
# for the nagios metadata because rhel does not ship these
# plugins. This metadata is providing 3rd party support
# for nagios. Users may install the plugins via 3rd party
# rpm packages, or source. If rhel ships the nagios plugins
# in the future, we should consider enabling the following
# required fields.
#Requires:      nagios-plugins-http
#Requires:      nagios-plugins-ldap
#Requires:      nagios-plugins-mysql
#Requires:      nagios-plugins-pgsql
#Requires:      nagios-plugins-tcp
Requires:      pcmk-cluster-manager

%description   nagios-plugins-metadata
The metadata files required for Pacemaker to execute the nagios plugin
monitor resources.

%prep
%autosetup -a 1 -n %{name}-%{commit} -S git_am -p 1

# Force the local time
#
# 'git' sets the file date to the date of the last commit.
# This can result in files having been created in the future
# when building on machines in timezones 'behind' the one the
# commit occurred in - which seriously confuses 'make'
find . -exec touch \{\} \;

%build

export CPPFLAGS="-DRHEL7_COMPAT"

# Early versions of autotools (e.g. RHEL <= 5) do not support --docdir
export docdir=%{pcmk_docdir}

export systemdunitdir=%{?_unitdir}%{!?_unitdir:no}

%if %{with hardening}
# prefer distro-provided hardening flags in case they are defined
# through _hardening_{c,ld}flags macros, configure script will
# use its own defaults otherwise; if such hardenings are completely
# undesired, rpmbuild using "--without hardening"
# (or "--define '_without_hardening 1'")
export CFLAGS_HARDENED_EXE="%{?_hardening_cflags}"
export CFLAGS_HARDENED_LIB="%{?_hardening_cflags}"
export LDFLAGS_HARDENED_EXE="%{?_hardening_ldflags}"
export LDFLAGS_HARDENED_LIB="%{?_hardening_ldflags}"
%endif

./autogen.sh

%{configure}                                       \
        %{?with_profiling:   --with-profiling}     \
        %{?with_coverage:    --with-coverage}      \
        %{!?with_cman:       --without-cman}       \
        %{!?with_snmp:       --without-snmp}       \
        %{!?with_esmtp:      --without-esmtp}      \
        --without-heartbeat                        \
        %{!?with_doc:        --with-brand=}        \
        %{!?with_hardening:  --disable-hardening}  \
        --with-initdir=%{_initrddir}               \
        --localstatedir=%{_var}                    \
        --with-nagios                              \
        --with-nagios-metadata-dir=%{_datadir}/pacemaker/nagios/plugins-metadata/   \
        --with-nagios-plugin-dir=%{_libdir}/nagios/plugins/   \
        --with-version=%{version}-%{release}

%if 0%{?suse_version} >= 1200
# Fedora handles rpath removal automagically
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%endif

make %{_smp_mflags} V=1 all

%check
# Prevent false positives in rpmlint
./BasicSanity.sh -V pengine cli 2>&1 | sed s/[fF]ail/faiil/g

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} docdir=%{pcmk_docdir} V=1 install

mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig
install -m 644 mcp/pacemaker.sysconfig ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/pacemaker
install -m 644 tools/crm_mon.sysconfig ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/crm_mon

%if %{with upstart_job}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/init
install -m 644 mcp/pacemaker.upstart ${RPM_BUILD_ROOT}%{_sysconfdir}/init/pacemaker.conf
install -m 644 mcp/pacemaker.combined.upstart ${RPM_BUILD_ROOT}%{_sysconfdir}/init/pacemaker.combined.conf
install -m 644 tools/crm_mon.upstart ${RPM_BUILD_ROOT}%{_sysconfdir}/init/crm_mon.conf
%endif

mkdir -p %{buildroot}%{_datadir}/pacemaker/nagios/plugins-metadata
for file in $(find nagios-agents-metadata-%{nagios_hash}/metadata -type f); do
        install -m 644 $file %{buildroot}%{_datadir}/pacemaker/nagios/plugins-metadata
done

%if %{defined _unitdir}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/lib/rpm-state/%{name}
%endif

# Scripts that should be executable
chmod a+x %{buildroot}/%{_datadir}/pacemaker/tests/cts/CTSlab.py

# These are not actually scripts
find %{buildroot} -name '*.xml' -type f -print0 | xargs -0 chmod a-x

# Don't package static libs
find %{buildroot} -name '*.a' -type f -print0 | xargs -0 rm -f
find %{buildroot} -name '*.la' -type f -print0 | xargs -0 rm -f

# Do not package these either
rm -f %{buildroot}/%{_libdir}/service_crm.so
rm -f %{buildroot}/%{_sbindir}/fence_legacy
rm -f %{buildroot}/%{_mandir}/man8/fence_legacy.*
find %{buildroot} -name '*o2cb*' -type f -print0 | xargs -0 rm -f

# Don't ship init scripts for systemd based platforms
%if %{defined _unitdir}
rm -f %{buildroot}/%{_initrddir}/pacemaker
rm -f %{buildroot}/%{_initrddir}/pacemaker_remote
%endif

# Don't ship fence_pcmk where it has no use
%if %{without cman}
rm -f %{buildroot}/%{_sbindir}/fence_pcmk
%endif

%if %{with coverage}
GCOV_BASE=%{buildroot}/%{_var}/lib/pacemaker/gcov
mkdir -p $GCOV_BASE
find . -name '*.gcno' -type f | while read F ; do
        D=`dirname $F`
        mkdir -p ${GCOV_BASE}/$D
        cp $F ${GCOV_BASE}/$D
done
%endif

%clean
rm -rf %{buildroot}

%post
%if %{defined _unitdir}
%systemd_post pacemaker.service
%else
/sbin/chkconfig --add pacemaker || :
%if %{with cman} && %{cman_native}
# make fence_pcmk in cluster.conf valid instantly otherwise tools like ccs may
# choke (until schema gets auto-regenerated on the next start of cluster),
# per the protocol shared with other packages contributing to cluster.rng
/usr/sbin/ccs_update_schema >/dev/null 2>&1 || :
%endif
%endif

%preun
%if %{defined _unitdir}
%systemd_preun pacemaker.service
%else
/sbin/service pacemaker stop >/dev/null 2>&1 || :
if [ $1 -eq 0 ]; then
    # Package removal, not upgrade
    /sbin/chkconfig --del pacemaker || :
fi
%endif

%postun
%if %{defined _unitdir}
%systemd_postun_with_restart pacemaker.service
%endif

%pre remote
%if %{defined _unitdir}
# Stop the service before anything is touched, and remember to restart
# it as one of the last actions (compared to using systemd_postun_with_restart,
# this avoids suicide when sbd is in use)
systemctl --quiet is-active pacemaker_remote
if [ $? -eq 0 ] ; then
    mkdir -p %{_localstatedir}/lib/rpm-state/%{name}
    touch %{_localstatedir}/lib/rpm-state/%{name}/restart_pacemaker_remote
    systemctl stop pacemaker_remote >/dev/null 2>&1
else
    rm -f %{_localstatedir}/lib/rpm-state/%{name}/restart_pacemaker_remote
fi
%endif

%post remote
%if %{defined _unitdir}
%systemd_post pacemaker_remote.service
%else
/sbin/chkconfig --add pacemaker_remote || :
%endif

%preun remote
%if %{defined _unitdir}
%systemd_preun pacemaker_remote.service
%else
/sbin/service pacemaker_remote stop >/dev/null 2>&1 || :
if [ $1 -eq 0 ]; then
    # Package removal, not upgrade
    /sbin/chkconfig --del pacemaker_remote || :
fi
%endif

%postun remote
%if %{defined _unitdir}
# This next line is a no-op, because we stopped the service earlier, but
# we leave it here because it allows us to revert to the standard behavior
# in the future if desired
%systemd_postun_with_restart pacemaker_remote.service
# Explicitly take care of removing the flag-file(s) upon final removal
if [ $1 -eq 0 ] ; then
    rm -f %{_localstatedir}/lib/rpm-state/%{name}/restart_pacemaker_remote
fi
%endif

%posttrans remote
%if %{defined _unitdir}
if [ -e %{_localstatedir}/lib/rpm-state/%{name}/restart_pacemaker_remote ] ; then
    systemctl start pacemaker_remote >/dev/null 2>&1
    rm -f %{_localstatedir}/lib/rpm-state/%{name}/restart_pacemaker_remote
fi
%endif

%post cli
%if %{defined _unitdir}
%systemd_post crm_mon.service
%endif

%preun cli
%if %{defined _unitdir}
%systemd_preun crm_mon.service
%endif

%postun cli
%if %{defined _unitdir}
%systemd_postun_with_restart crm_mon.service
%endif

%pre -n %{name}-libs

getent group %{gname} >/dev/null || groupadd -r %{gname} -g 189
getent passwd %{uname} >/dev/null || useradd -r -g %{gname} -u 189 -s /sbin/nologin -c "cluster user" %{uname}
exit 0

%post -n %{name}-libs -p /sbin/ldconfig

%postun -n %{name}-libs -p /sbin/ldconfig

%post -n %{name}-cluster-libs -p /sbin/ldconfig

%postun -n %{name}-cluster-libs -p /sbin/ldconfig

%files
###########################################################
%defattr(-,root,root)

%config(noreplace) %{_sysconfdir}/sysconfig/pacemaker
%{_sbindir}/pacemakerd

%if %{defined _unitdir}
%{_unitdir}/pacemaker.service
%else
%{_initrddir}/pacemaker
%endif

%exclude %{_libexecdir}/pacemaker/lrmd_test
%exclude %{_sbindir}/pacemaker_remoted
%{_libexecdir}/pacemaker/*

%{_sbindir}/crm_attribute
%{_sbindir}/crm_master
%{_sbindir}/crm_node
%if %{with cman}
%{_sbindir}/fence_pcmk
%endif
%{_sbindir}/stonith_admin

%doc %{_mandir}/man7/crmd.*
%doc %{_mandir}/man7/pengine.*
%doc %{_mandir}/man7/stonithd.*
%if %{without cman} || !%{cman_native}
%doc %{_mandir}/man7/ocf_pacemaker_controld.*
%endif
%doc %{_mandir}/man7/ocf_pacemaker_remote.*
%doc %{_mandir}/man8/crm_attribute.*
%doc %{_mandir}/man8/crm_node.*
%doc %{_mandir}/man8/crm_master.*
%if %{with cman}
%doc %{_mandir}/man8/fence_pcmk.*
%endif
%doc %{_mandir}/man8/pacemakerd.*
%doc %{_mandir}/man8/stonith_admin.*

%doc %{_datadir}/pacemaker/alerts

%license licenses/GPLv2
%doc COPYING
%doc ChangeLog

%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/cib
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/pengine
%if %{without cman} || !%{cman_native}
/usr/lib/ocf/resource.d/pacemaker/controld
%endif
/usr/lib/ocf/resource.d/pacemaker/remote
/usr/lib/ocf/resource.d/.isolation

%if "%{?cs_version}" != "UNKNOWN"
%if 0%{?cs_version} < 2
%{_libexecdir}/lcrso/pacemaker.lcrso
%endif
%endif

%if %{with upstart_job}
%config(noreplace) %{_sysconfdir}/init/pacemaker.conf
%config(noreplace) %{_sysconfdir}/init/pacemaker.combined.conf
%endif

%files cli
%defattr(-,root,root)

%config(noreplace) %{_sysconfdir}/logrotate.d/pacemaker
%config(noreplace) %{_sysconfdir}/sysconfig/crm_mon

%if %{defined _unitdir}
%{_unitdir}/crm_mon.service
%endif

%if %{with upstart_job}
%config(noreplace) %{_sysconfdir}/init/crm_mon.conf
%endif

%{_sbindir}/attrd_updater
%{_sbindir}/cibadmin
%{_sbindir}/crm_diff
%{_sbindir}/crm_error
%{_sbindir}/crm_failcount
%{_sbindir}/crm_mon
%{_sbindir}/crm_resource
%{_sbindir}/crm_standby
%{_sbindir}/crm_verify
%{_sbindir}/crmadmin
%{_sbindir}/iso8601
%{_sbindir}/crm_shadow
%{_sbindir}/crm_simulate
%{_sbindir}/crm_report
%{_sbindir}/crm_ticket
%exclude %{_datadir}/pacemaker/alerts
%exclude %{_datadir}/pacemaker/tests
%exclude %{_datadir}/pacemaker/nagios
%{_datadir}/pacemaker
%{_datadir}/snmp/mibs/PCMK-MIB.txt

%exclude /usr/lib/ocf/resource.d/pacemaker/controld
%exclude /usr/lib/ocf/resource.d/pacemaker/remote

%dir /usr/lib/ocf
%dir /usr/lib/ocf/resource.d
/usr/lib/ocf/resource.d/pacemaker

%doc %{_mandir}/man7/*
%exclude %{_mandir}/man7/crmd.*
%exclude %{_mandir}/man7/pengine.*
%exclude %{_mandir}/man7/stonithd.*
%exclude %{_mandir}/man7/ocf_pacemaker_controld.*
%exclude %{_mandir}/man7/ocf_pacemaker_remote.*
%doc %{_mandir}/man8/*
%exclude %{_mandir}/man8/crm_attribute.*
%exclude %{_mandir}/man8/crm_node.*
%exclude %{_mandir}/man8/crm_master.*
%exclude %{_mandir}/man8/fence_pcmk.*
%exclude %{_mandir}/man8/pacemakerd.*
%exclude %{_mandir}/man8/pacemaker_remoted.*
%exclude %{_mandir}/man8/stonith_admin.*

%license licenses/GPLv2
%doc COPYING
%doc ChangeLog

%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/blackbox
%dir %attr (750, %{uname}, %{gname}) %{_var}/lib/pacemaker/cores

%files -n %{name}-libs
%defattr(-,root,root)

%{_libdir}/libcib.so.*
%{_libdir}/liblrmd.so.*
%{_libdir}/libcrmservice.so.*
%{_libdir}/libcrmcommon.so.*
%{_libdir}/libpe_status.so.*
%{_libdir}/libpe_rules.so.*
%{_libdir}/libpengine.so.*
%{_libdir}/libstonithd.so.*
%{_libdir}/libtransitioner.so.*
%license licenses/LGPLv2.1
%doc COPYING
%doc ChangeLog

%files -n %{name}-cluster-libs
%defattr(-,root,root)
%{_libdir}/libcrmcluster.so.*
%license licenses/LGPLv2.1
%doc COPYING
%doc ChangeLog

%files remote
%defattr(-,root,root)

%config(noreplace) %{_sysconfdir}/sysconfig/pacemaker
%if %{defined _unitdir}
# state directory is shared between the subpackets
# let rpm take care of removing it once it isn't
# referenced anymore and empty
%ghost %dir %{_localstatedir}/lib/rpm-state/%{name}
%{_unitdir}/pacemaker_remote.service
%else
%{_initrddir}/pacemaker_remote
%endif

%{_sbindir}/pacemaker_remoted
%{_mandir}/man8/pacemaker_remoted.*
%license licenses/GPLv2
%doc COPYING
%doc ChangeLog

%files doc
%defattr(-,root,root)
%doc %{pcmk_docdir}
%license licenses/CC-BY-SA-4.0

%files cts
%defattr(-,root,root)
%{py_site}/cts
%{_datadir}/pacemaker/tests/cts
%{_libexecdir}/pacemaker/lrmd_test
%license licenses/GPLv2
%doc COPYING
%doc ChangeLog

%files -n %{name}-libs-devel
%defattr(-,root,root)
%exclude %{_datadir}/pacemaker/tests/cts
%{_datadir}/pacemaker/tests
%{_includedir}/pacemaker
%{_libdir}/*.so
%if %{with coverage}
%{_var}/lib/pacemaker/gcov
%endif
%{_libdir}/pkgconfig/*.pc
%license licenses/LGPLv2.1
%doc COPYING
%doc ChangeLog

%files nagios-plugins-metadata
%defattr(-,root,root)
%dir %{_datadir}/pacemaker/nagios/plugins-metadata
%attr(0644,root,root) %{_datadir}/pacemaker/nagios/plugins-metadata/*

%changelog
* Fri Apr 20 2018 Ken Gaillot <kgaillot@redhat.com> - 1.1.18-11.2
- Do not record pending notify actions as completed
- Resolves: rhbz#1570618

* Wed Apr 18 2018 Ken Gaillot <kgaillot@redhat.com> - 1.1.18-11.1
- Do not schedule notifications for unrunnable actions
- Do not expire remote failures if fencing is pending
- Do not consider attribute order difference as CIB change in crm_diff
- Resolves: rhbz#1563345
- Resolves: rhbz#1566533
- Resolves: rhbz#1568720

* Fri Jan 26 2018 Ken Gaillot <kgaillot@redhat.com> - 1.1.18-11
- Fix regression in crm_master
- Resolves: rhbz#1539113

* Wed Jan 24 2018 Ken Gaillot <kgaillot@redhat.com> - 1.1.18-10
- Always trigger transition when quorum changes
- Match clone names correctly with crm_resource --cleanup
- Fix pcs resource --wait timeout when bundles are used
- Observe colocation constraints correctly with bundles in master role
- Resolves: rhbz#1464068
- Resolves: rhbz#1508350
- Resolves: rhbz#1519812
- Resolves: rhbz#1527072

* Mon Dec 18 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.18-9
- Fix small memory leak introduced by node attribute delay fix
- Resolves: rhbz#1454960

* Tue Dec 12 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.18-8
- Regression fix for "pcs resource cleanup" was incomplete
- Resolves: rhbz#1508350

* Mon Dec 11 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.18-7
- Avoid node attribute write delay when corosync.conf has only IP addresses
- Fix regressions in "pcs resource cleanup" behavior
- Restore ordering of unfencing before fence device starts
- Ensure --wait options work when bundles are in use
- Fix possible invalid transition with bundle ordering constraints
- Resolves: rhbz#1454960
- Resolves: rhbz#1508350
- Resolves: rhbz#1517796
- Resolves: rhbz#1519812
- Resolves: rhbz#1522822

* Wed Nov 15 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.18-6
- Rebase to upstream 2b07d5c5a908998891c3317faa30328c108d3a91 (1.1.18)
- If on-fail=ignore, migration-threshold should also be ignored
- Resolves: rhbz#1474428
- Resolves: rhbz#1507344

* Fri Nov 3 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.18-5
- Properly clean up primitive inside bundle
- Scalability improvements
- Resolves: rhbz#1499217
- Resolves: rhbz#1508373

* Fri Nov 3 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.18-4
- Rebase to upstream 1a4ef7d180e77bcd6423f342d62e05e516c4e852 (1.1.18-rc4)
- Resolves: rhbz#1381754
- Resolves: rhbz#1474428
- Resolves: rhbz#1499217
- Resolves: rhbz#1508373

* Tue Oct 24 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.18-3
- Rebase to upstream 36d2962a8613322fc43d727d95720d61a47d0138 (1.1.18-rc3)
- Resolves: rhbz#1474428

* Mon Oct 16 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.18-2
- Rebase to upstream 5cccc41c95d6288eab27d93901b650b071f976dc (1.1.18-rc2)
- Default record-pending to true
- Resolves: rhbz#1323546
- Resolves: rhbz#1376556
- Resolves: rhbz#1382364
- Resolves: rhbz#1461976
- Resolves: rhbz#1474428
- Resolves: rhbz#1500509
- Resolves: rhbz#1501903
- Resolves: rhbz#1501924

* Mon Oct 9 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.18-1
- Rebase to upstream 1cb712c5369c98f03d42bcf8648cacd86a5f48f7 (1.1.18-rc1)
- Resolves: rhbz#1298581
- Resolves: rhbz#1394418
- Resolves: rhbz#1427648
- Resolves: rhbz#1454933
- Resolves: rhbz#1454957
- Resolves: rhbz#1454960
- Resolves: rhbz#1462253
- Resolves: rhbz#1464068
- Resolves: rhbz#1465519
- Resolves: rhbz#1470262
- Resolves: rhbz#1471506
- Resolves: rhbz#1474428
- Resolves: rhbz#1474463
- Resolves: rhbz#1482278
- Resolves: rhbz#1489728
- Resolves: rhbz#1489735

* Tue Jun 20 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.16-12
- Avoid unnecessary restarts when recovering remote connections
- Resolves: rhbz#1448773

* Fri Jun 9 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.16-11
- Support bundle meta-attributes
- Resolves: rhbz#1447903

* Tue May 23 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.16-10
- Fix issues when running bundles on Pacemaker Remote nodes
- Reap orphaned processes when running Pacemaker Remote as pid 1
- Order remote actions after remote connection recovery
  (fixes regression in RHEL 7.3)
- Avoid local resource manager daemon (lrmd) crash when an
  in-flight systemd operation is cancelled
- Resolves: rhbz#1432722
- Resolves: rhbz#1441603
- Resolves: rhbz#1448772
- Resolves: rhbz#1451170

* Tue May 9 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.16-9
- Allow cleanup of guest nodes when guest is unmanaged
- Allow bundles to run on Pacemaker Remote nodes
- Handle slow IPC clients better
- Update crmd throttle information when CPUs are hot-plugged in
- Order pacemaker systemd unit after resource-agents-deps target
- Resolves: rhbz#1303742
- Resolves: rhbz#1432722
- Resolves: rhbz#1435067
- Resolves: rhbz#1444728
- Resolves: rhbz#1446669

* Tue Apr 18 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.16-8
- Fix shell script syntax error introduced with URL patch
- Resolves: rhbz#1410886

* Tue Apr 18 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.16-7
- Avoid fencing old DC if it is shutting down while another node is joining
- Improve crmd's handling of repeated fencing failures
- Correct behavior when guest created by bundle has a node attribute
- Show Red Hat bugzilla URL rather than upstream when generating cluster report
- Resolves: rhbz#1430112
- Resolves: rhbz#1432722

* Wed Apr 5 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.16-6
- Allow container without IP to use underlying hostname
- Resolves: rhbz#1432722

* Tue Apr 4 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.16-5
- Keep man pages compressed
- Bugfixes for container bundles
- Resolves: rhbz#1410886
- Resolves: rhbz#1432722

* Mon Apr 3 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.16-4
- Add support for container bundles
- Treat systemd reloading state as monitor success
- Resolves: rhbz#1432722
- Resolves: rhbz#1436696

* Mon Mar 20 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.16-3
- Avoid hang when shutting down unmanaged remote node connections
- Get correct node name when crm_node or crm_attribute is run on remote node
- Ignore action when configured as a stonith device parameter
- Include recent upstream bug fixes
- Resolves: rhbz#1388489
- Resolves: rhbz#1410886
- Resolves: rhbz#1417936
- Resolves: rhbz#1421700

* Thu Jan 19 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.16-2
- Avoid grep crashes in crm_report when looking for system logs
- Properly ignore version with crm_diff --no-version
- Process guest node fencing properly
- Ensure filename is valid before using
- Build for ppc64le
- Resolves: rhbz#1288261
- Resolves: rhbz#1289662
- Resolves: rhbz#1383462
- Resolves: rhbz#1405635
- Resolves: rhbz#1412309 

* Thu Jan 12 2017 Ken Gaillot <kgaillot@redhat.com> - 1.1.16-1
- Rebase to upstream 94ff4df51a55cc30d01843ea11b3292bac755432 (1.1.16)
- Resolves: rhbz#1374777
- Resolves: rhbz#1378817
- Resolves: rhbz#1410886

* Wed Oct 26 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.15-12
- Preserve rolling upgrades involving Pacemaker Remote nodes
- Resolves: rhbz#1388827

* Fri Oct 21 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.15-11.1
- Fix CVE-2016-7035
- Resolves: rhbz#1374776

* Thu Sep 22 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.15-11
- Sanitize readable CIB output collected by crm_report
- Document crm_report --sos-mode option
- Speed up crm_report on Pacemaker Remote nodes
- Avoid sbd fencing when upgrading pacemaker_remote package
- Resolves: rhbz#1219188
- Resolves: rhbz#1235434
- Resolves: rhbz#1323544
- Resolves: rhbz#1372009

* Mon Aug 15 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.15-10
- Only clear remote node operation history on startup
- Resend a lost shutdown request
- Correctly detect and report invalid configurations
- Don't include manual page for resource agent that isn't included
- Resolves: rhbz#1288929
- Resolves: rhbz#1310486
- Resolves: rhbz#1352039

* Fri Aug 5 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.15-9
- Make crm_mon XML schema handle multiple-active resources
- Resolves: rhbz#1364500

* Wed Aug 3 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.15-8
- Quote timestamp-format correctly in alert_snmp.sh.sample
- Unregister CIB callbacks correctly
- Print resources section heading consistently in crm_mon output
- Resolves: rhbz#773656
- Resolves: rhbz#1361533

* Tue Jul 26 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.15-7
- Avoid null dereference
- Resolves: rhbz#1290592

* Tue Jul 26 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.15-6
- Fix transition failure with start-then-stop order constraint + unfencing
- Resolves: rhbz#1290592

* Fri Jul 1 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.15-5
- Update spec file for toolchain hardening
- Resolves: rhbz#1242258

* Tue Jun 28 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.15-4
- Take advantage of toolchain hardening
- Resolves: rhbz#1242258

* Wed Jun 22 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.15-3
- Rebase to upstream e174ec84857e087210b9dacee3318f8203176129 (1.1.15)
- Resolves: rhbz#1304771
  Resolves: rhbz#1303765
  Resolves: rhbz#1327469
  Resolves: rhbz#1337688
  Resolves: rhbz#1345876
  Resolves: rhbz#1346726

* Fri Jun 10 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.15-2
- Rebase to upstream 25920dbdbc7594fc944a963036996f724c63a8b8 (1.1.15-rc4)
- Resolves: rhbz#1304771
  Resolves: rhbz#773656
  Resolves: rhbz#1240330
  Resolves: rhbz#1281450
  Resolves: rhbz#1286316
  Resolves: rhbz#1287315
  Resolves: rhbz#1323544

* Tue May 31 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.15-1
- Rebase to upstream 2c148ac30dfcc2cfb91dc367ed469b6f227a8abc (1.1.15-rc3+)
- Resolves: rhbz#1304771
  Resolves: rhbz#1040685
  Resolves: rhbz#1219188
  Resolves: rhbz#1235434
  Resolves: rhbz#1268313
  Resolves: rhbz#1284069
  Resolves: rhbz#1287868
  Resolves: rhbz#1288929
  Resolves: rhbz#1312094
  Resolves: rhbz#1314157
  Resolves: rhbz#1321711
  Resolves: rhbz#1338623

* Thu Feb 18 2016 Ken Gaillot <kgaillot@redhat.com> - 1.1.14-11
- Rebase to upstream 2cccd43d6b7f2525d406251e14ef37626e29c51f (1.1.14+)
- Resolves: rhbz#1304771
  Resolves: rhbz#1207388
  Resolves: rhbz#1240330
  Resolves: rhbz#1281450
  Resolves: rhbz#1284069
  Resolves: rhbz#1286316
  Resolves: rhbz#1287315
  Resolves: rhbz#1287868
  Resolves: rhbz#1288929
  Resolves: rhbz#1303765
- This also updates the packaging to follow upstream more closely,
  most importantly moving some files from the pacemaker package to
  pacemaker-cli (including XML schemas, SNMP MIB, attrd_updater command,
  most ocf:pacemaker resource agents, and related man pages),
  and deploying /etc/sysconfig/crm_mon.

* Thu Oct 08 2015 Andrew Beekhof <abeekhof@redhat.com> - 1.1.13-10
- More improvements when updating and deleting meta attributes
- Resolves: rhbz#1267265

* Mon Oct 05 2015 Andrew Beekhof <abeekhof@redhat.com> - 1.1.13-9
- Fix regression when updating child meta attributes
- Resolves: rhbz#1267265

* Wed Sep 16 2015 Andrew Beekhof <abeekhof@redhat.com> - 1.1.13-8
- Fix regression when setting attributes for remote nodes 
- Resolves: rhbz#1206647

* Thu Sep 10 2015 Andrew Beekhof <abeekhof@redhat.com> - 1.1.13-7
- Additional upstream patches
- Resolves: rhbz#1234680

* Wed Jul 22 2015 Andrew Beekhof <abeekhof@redhat.com> - 1.1.13-6
- Correctly apply and build patches
- Resolves: rhbz#1234680

* Wed Jul 22 2015 Andrew Beekhof <abeekhof@redhat.com> - 1.1.13-5
- Sync with upstream 63f8e9a
- Resolves: rhbz#1234680

* Mon Jul 20 2015 Andrew Beekhof <abeekhof@redhat.com> - 1.1.13-4
- Sync with upstream 63f8e9a
- Resolves: rhbz#1234680

* Fri Jun 26 2015 Andrew Beekhof <abeekhof@redhat.com> - 1.1.13-3
- New upstream tarball 44eb2ddf8d4f8fc05256aae2abc9fbf3ae4d1fbc
- Resolves: rhbz#1234680

* Thu Jun 11 2015 David Vossel <dvossel@redhat.com> - 1.1.13-2
- Adds nagios metadata.

  Resolves: rhbz#1203053

* Tue May 12 2015 Andrew Beekhof <abeekhof@redhat.com> - 1.1.13-0.1
- New upstream tarball 8ae45302394b039fb098e150f156df29fc0cb576

* Wed Mar 18 2015 David Vossel <dvossel@redhat.com> - 1.1.12-25
- Convince systemd to shutdown dbus after pacemaker.

  Resolves: rhbz#1198886

* Wed Mar 18 2015 David Vossel <dvossel@redhat.com> - 1.1.12-23
- Ensure B with A, that B can not run if A can not run.

  Resolves: rhbz#1194475

* Thu Jan 15 2015 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-22
- Fix segfault encountered with orphaned remote node connections

  Resolves: rhbz#1176210

* Thu Jan 15 2015 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-21
- Fix use-after-free in CLI tool when restarting a resource 

* Tue Jan 13 2015 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-20
- Expose the -N/--node option for attrd_updater to allow attributes to
  be set for other nodes

* Sun Jan 11 2015 David Vossel <dvossel@redhat.com> - 1.1.12-19
- Imply stop on actions within containers during host fencing
- acl correctly implement the reference acl direct

  Resolves: rhbz#1117341

* Tue Jan 6 2015 David Vossel <dvossel@redhat.com> - 1.1.12-18
- clone order constraint require-all option.
- fix memory leaks in crmd and pacemakerd

  Resolves: rhbz#1176210

* Tue Dec 16 2014 David Vossel <dvossel@redhat.com> - 1.1.12-15
- Include ipc and pacemaker remote related upstream fixes.

* Wed Nov 26 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-13
- Update patch level to upstream a433de6
- Ensure we wait for long running systemd stop operations to complete
  Resolves: rhbz#1165423

* Tue Nov 18 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-11
- Update patch level to upstream 7dd9022
- Ensure all internal caches are updated when nodes are removed from the cluster
  Resolves: rhbz#1162727
 
* Wed Nov 05 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-10
- Update patch level to upstream 98b6688
- Support an intelligent resource restart operation
- Exclusive discovery implies running the resource is only possible on the listed nodes

* Wed Nov 05 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-9
- Update patch level to upstream fb94901
- Prevent blocking by performing systemd reloads asynchronously

* Tue Oct 28 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-8
- Repair the ability to start when sbd is not enabled

* Mon Oct 27 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-7
- Update patch level to upstream afa0f33
  - Resolve coverity defects

* Fri Oct 24 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-5
- Update patch level to upstream 031e46c
  - Prevent glib assert triggered by timers being removed from mainloop more than once 
  - Allow rsc discovery to be disabled in certain situations
  - Allow remote-nodes to be placed in maintenance mode
  - Improved sbd integration

* Thu Oct 16 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-4
- Add install dependancy on sbd

* Wed Oct 01 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-3
- Update patch level to upstream be1e835
    Resolves: rhbz#1147989

* Fri Sep 19 2014 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.1.12-2
- Enable build on s390x
    Resolves: rhbz#1140917

* Mon Sep 08 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.12-1
- Rebase to upstream a14efad51ca8f1e3742fd8520e051cd7a0864f04 (1.1.12+)
    Resolves: rhbz#1059626

* Fri Jul 04 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-32

- Fix: lrmd: Handle systemd reporting 'done' before a resource is actually stopped
    Resolves: rhbz#1111747

* Thu Apr 17 2014 David Vossel <dvossel@redhat.com> - 1.1.10-31

- fencing: Fence using all required devices
- fencing: Execute all required fencing devices regardless of what topology level they are at
- fencing: default to 'off' when agent does not advertise 'reboot' in metadata
    Resolves: rhbz#1078078

* Mon Apr 14 2014 Andrew Beekhof <abeekhof@redhat.com> 1.1.10-30

- crmd: Do not erase the status section for unfenced nodes
- crmd: Correctly react to successful unfencing operations
- crmd: Report unsuccessful unfencing operations
- crmd: Do not overwrite existing node state when fencing completes
- fencing: Correctly record which peer performed the fencing operation
- fencing: Automatically switch from 'list' to 'status' to 'static-list' if those actions are not advertised in the metadata
- fencing: Filter self-fencing at the peers to allow unfencing to work correctly
- pengine: Automatically re-unfence a node if the fencing device definition changes
- pengine: Fencing devices default to only requiring quorum in order to start
- pengine: Delay unfencing until after we know the state of all resources that require unfencing
- pengine: Ensure unfencing occurs before fencing devices are (re-)probed
- pengine: Ensure unfencing only happens once, even if the transition is interrupted
- pengine: Do not unfence nodes that are offline, unclean or shutting down
- pengine: Unfencing is based on device probes, there is no need to unfence when normal resources are found active
- logging: daemons always get a log file, unless explicitly set to configured 'none'
- lrmd: Expose logging variables expected by OCF agents
- crm_report: Suppress logging errors after the target directory has been compressed
- crm_resource: Wait for the correct number of replies when cleaning up resources
    Resolves: rhbz#1078078

* Tue Mar 25 2014 David Vossel <dvossel@redhat.com> - 1.1.10-29

- Low: controld: Remove '-q 0' from default dlm_controld arguments
    Resolves: rhbz#1064519

* Tue Mar 25 2014 David Vossel <dvossel@redhat.com> - 1.1.10-28

- pengine: fixes invalid transition caused by clones with more than 10 instances
    Resolves: rhbz#1078504

* Fri Feb 28 2014 Andrew Beekhof <beekhof@redhat.com> - 1.1.10-27

- crm_resource: Prevent use-of-NULL
- systemd: Prevent use-of-NULL when determining if an agent exists
- Fencing: Remove shadow definition and use of variable 'progress'
    Resolves: rhbz#1070916

* Thu Feb 27 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-26

- Run automated regression tests after every build
- Fencing: Send details of stonith_api_time() and stonith_api_kick() to syslog
- Fencing: Pass the correct options when looking up the history by node name
- Fencing: stonith_api_time_helper now returns when the most recent fencing operation completed
- crm_report: Additional dlm detail if dlm_controld is running
- crmd: Gracefully handle actions that cannot be initiated
- pengine: Gracefully handle bad values for XML_ATTR_TRANSITION_MAGIC
    Resolves: rhbz#1070916

* Tue Feb 25 2014 David Vossel <dvossel@redhat.com> - 1.1.10-25

- pengine: cl#5187 - Prevent resources in an anti-colocation from even temporarily running on a same node
    Resolves: rhbz#1069284

* Thu Feb 20 2014 David Vossel <dvossel@redhat.com> - 1.1.10-24

- controld: handling startup fencing within the controld agent, not the dlm
    Resolves: rhbz#1064519
- controld: Do not consider the dlm up until the address list is present
    Resolves: rhbz#1067536

* Wed Feb 12 2014 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-23

- mcp: Tell systemd not to respawn us if we return 100
- services: Detect missing agents and permission errors before forking
- Use native DBus library for systemd support to avoid problematic use of threads
    Resolves: rhbz#720543 (aka. 1057697)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1.10-22
- Mass rebuild 2013-12-27

* Wed Dec 04 2013 David Vossel <dvossel@redhat.com> - 1.1.10-21

- Fix: Removes unnecessary newlines in crm_resource -O output
    Resolves: rhbz#720543

* Thu Nov 14 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-20

- Fix: tools: Fixes formatting of remote-nodes in crm_mon and crm_simulate
- Fix: Corosync: Attempt to retrieve a peers node name if it is not already known
    Resolves: rhbz#720543

* Thu Nov 14 2013 David Vossel <dvossel@redhat.com> - 1.1.10-19
- Fix: controld: Use the correct variant of dlm_controld for
  corosync-2 clusters

    Resolves: rhbz#1028627

* Thu Nov 07 2013 David Vossel <dvossel@redhat.com> - 1.1.10-18

- High: remote: Add support for ipv6 into pacemaker_remote daemon
    Resolves: rhbz#720543

* Wed Nov 06 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-17

    Resolves: rhbz#720543

- Fix: core: Do not enabled blackbox for cli tools
- Fix: Command-line tools should stop after an assertion failure
- Fix: crmd: Dont add node_state to cib, if we have not seen or fenced this node yet
- Fix: crmd: Correctly update expected state when the previous DC shuts down
- Fix: crmd: Cache rsc_info retrieved from lrmd and pacemaker_remoted
- Fix: crmd: Pad internal lrmd rsc_info and metadata retrieval timeout
- Fix: crm_attribute: Detect orphaned remote-nodes when setting attributes
- Fix: crm_mon: Prevent use-of-NULL when ping resources do not define a host list
- Fix: crm_report: Record the output of the collector
- Fix: crm_report: Do not print garbage when collecting from the local node
- Fix: crm_resource: Wait for all replies when cleaning up resources
- Fix: fencing: Do not broadcast suicide if the on action is being executed
- Fix: fencing: Allow fencing for node after topology entries are deleted
- Fix: fencing: Deep copy current topology level list on remote op
- Fix: lrmd: Correctly cancel monitor actions for lsb/systemd/service resources on cleaning up
- Fix: pengine: Dont prevent clones from running due to dependant resources
- Fix: pengine: Probe containers not expected to be up
- Fix: ipc: Raise the default buffer size to 128k
- Fix: ipc: Use the higher of the configured buffer size or the default
- Fix: iso8601: Prevent dates from jumping backwards a day in some timezones
- Fix: remote: Properly version the remote connection protocol
- Fix: remote: Handle endian changes between client and server and improve forward compatibility
    Resolves: rhbz#720543

* Mon Oct 07 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-16

- Remove unsupported resource agent
- Log: crmd: Supply arguments in the correct order
- Fix: crm_report: Correctly redirect error message to /dev/null
- Fix: Bug rhbz#1011618 - Consistently use 'Slave' as the role for unpromoted master/slave resources
- Fix: pengine: Location constraints with role=Started should prevent masters from running at all
- Fix: crm_resource: Observe --master modifier for --move
- Provide a meaningful error if --master is used for primitives and groups
- Fix: Fencing: Observe pcmk_host_list during automatic unfencing
    Resolves: rhbz#996576

* Fri Sep 27 2013 David Vossel  <dvossel@redhat.com> - 1.1.10-15
  + Fix: crmd: Allow transient attributes to be set on remote-nodes.
  + Fix: pengine: Handle orphaned remote-nodes properly
  + Low: cts: Add RemoteLXC regression test.

  Resolves: rhbz#1006465
  Resolves: rhbz#1006471

* Fri Aug 23 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-14
  + Fix: xml: Location constraints are allowed to specify a role
  + Bug rhbz#902407 - crm_resource: Handle --ban for master/slave resources as advertised
    Resolves: rhbz#902407

* Wed Aug 14 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-13
  + Fencing: Support agents that need the host to be unfenced at startup
    Resolves: rhbz#996576
  + crm_report: Collect corosync quorum data
    Resolves: rhbz#839342

* Thu Aug 08 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-12
- Regenerate patches to have meaningful names

* Thu Aug 08 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-11
  + Fix: systemd: Prevent glib assertion - only call g_error_free() with non-NULL arguments
  + Fix: systemd: Prevent additional assertions in g_error_free
  + Fix: logging: glib CRIT messages should not produce core files by default
  + Doc: controld: Update the description
  + Fix: pengine: Correctly account for the location preferences of things colocated with a group
  + Fix: cib: Correctly log short-form xml diffs
  + Fix: crmd: Correcty update the history cache when recurring ops change their return code
  + Log: pengine: Better indicate when a resource has failed
  + Log: crm_mon: Unmunge the output for failed operations

* Fri Aug 02 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-10
  + Fix: pengine: Do not re-allocate clone instances that are blocked in the Stopped state
  + Fix: pengine: Do not allow colocation with blocked clone instances

* Thu Aug 01 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-9
  + Fix: crmd: Prevent crash by passing log arguments in the correct order

* Thu Aug 01 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-8
  + Fix: pengine: Do not restart resources that depend on unmanaged resources

* Thu Aug 01 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-7
  + Fix: crmd: Prevent recurring monitors being cancelled due to notify operations

* Fri Jul 26 2013 Andrew Beekhof <andrew@beekhof.net> Pacemaker-1.1.10-6
- Update source tarball to revision: 368c726 (Pacemaker-1.1.10-rc7)
- Changesets: 18
- Diff:       9 files changed, 245 insertions(+), 170 deletions(-)

- Features added since Pacemaker-1.1.10-rc7
  + crm_resource: Allow options to be set recursively

- Changes since Pacemaker-1.1.10-rc7
  + Bug cl#5161 - crmd: Prevent memory leak in operation cache
  + cib: Correctly read back archived configurations if the primary is corrupted

* Mon Jul 22 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-5
- Streamline spec file

- Upstream patch for:
  + cman: Only build migration tools for targets that may use them
  + cib: Ensure we set up hacluster's groups in stand-alone mode

- Update for new upstream tarball: Pacemaker-1.1.10-rc7

  + Bug cl#5157 - Allow migration in the absence of some colocation constraints
  + Bug cl#5168 - Prevent clones from being bounced around the cluster due to location constraints
  + Bug cl#5170 - Correctly support on-fail=block for clones
  + crmd: CID#1036761 Dereference null return value
  + crmd: cl#5164 - Fixes crmd crash when using pacemaker-remote
  + crmd: Ensure operations for cleaned up resources don't block recovery
  + crmd: Prevent messages for remote crmd clients from being relayed to wrong daemons
  + crmd: Properly handle recurring monitor operations for remote-node agent
  + fencing: Correctly detect existing device entries when registering a new one
  + logging: If SIGTRAP is sent before tracing is turned on, turn it on
  + lrmd: Prevent use-of-NULL in client library
  + pengine: cl#5128 - Support maintenance mode for a single node
  + pengine: cl#5164 - Pengine segfault when calculating transition with remote-nodes.
  + pengine: Do the right thing when admins specify the internal resource instead of the clone
  + systemd: Turn off auto-respawning of systemd services when the cluster starts them

* Wed Jul 10 2013 David Vossel <dvossel@redhat.com> - 1.1.10-4
- Fixes crmd crash when using pacemaker_remote.

* Mon Jun 17 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-3
- Update to upstream 838e41e

  + Feature: pengine: Allow active nodes in our current membership to be fenced without quorum
  + Fix: attrd: Fixes deleted attributes during dc election
  + Fix: corosync: Fall back to uname for local nodes
  + Fix: crm_report: Find logs in compressed files
  + Fix: pengine: If fencing is unavailable or disabled, block further recovery for resources that fail to stop
  + Fix: systemd: Ensure we get shut down correctly by systemd

* Sun Jun 09 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-2
- Update for new upstream tarball: Pacemaker-1.1.10-rc4

- Features in Pacemaker-1.1.10-rc4:
  + PE: Display a list of nodes on which stopped anonymous clones are not active instead of meaningless clone IDs
  + crm_error: Add the ability to list and print error symbols
  + crm_resource: Implement --ban for moving resources away from nodes and --clear (replaces --unmove)
  + crm_resource: Support OCF tracing when using --force-(check|start|stop)

- Changes since Pacemaker-1.1.10-rc1

  + Bug cl#5133 - pengine: Correctly observe on-fail=block for failed demote operation
  + Bug cl#5152 - Correctly clean up fenced nodes during membership changes
  + Bug cl#5153 - Correctly display clone failcounts in crm_mon
  + Bug cl#5154 - Do not expire failures when on-fail=block is present
  + Bug pengine: cl#5155 - Block the stop of resources if any depending resource is unmanaged
  + crm_report: Correctly collect logs when 'uname -n' reports fully qualified names
  + Check for and replace non-printing characters with their octal equivalent while exporting xml text
  + Convert all exit codes to positive errno values
  + Core: Ensure the blackbox is saved on abnormal program termination
  + corosync: Detect the loss of members for which we only know the nodeid
  + corosync: Nodes that can persist in sending CPG messages must be alive afterall
  + crmd: Do not get stuck in S_POLICY_ENGINE if a node we couldn't fence returns
  + crmd: Ensure all membership operations can complete while trying to cancel a transition
  + crmd: Everyone who gets a fencing notification should mark the node as down
  + crmd: Initiate node shutdown if another node claims to have successfully fenced us
  + crm_resource: Gracefully fail when --force-* is attempted for stonith resources
  + fencing: Restore the ability to manually confirm that fencing completed
  + pengine: Correctly handle resources that recover before we operate on them
  + pengine: Ensure per-node resource parameters are used during probes
  + pengine: Implement the rest of get_timet_now() and rename to get_effective_time
  + pengine: Mark unrunnable stop actions as "blocked"
  + pengine: Re-initiate active recurring monitors that previously failed but have timed out
  + xml: Restore the ability to embed comments in the cib

* Wed Apr 17 2013 Andrew Beekhof <abeekhof@redhat.com> - 1.1.10-1
- Update for new upstream tarball: Pacemaker-1.1.10-rc1
- Features added since Pacemaker-1.1.8
  + Performance enhancements for supporting 16 node clusters
  + corosync: Use queues to avoid blocking when sending CPG messages
  + ipc: Compress messages that exceed the configured IPC message limit
  + ipc: Use queues to prevent slow clients from blocking the server
  + ipc: Use shared memory by default
  + lrmd: Support nagios remote monitoring
  + lrmd: Pacemaker Remote Daemon for extending pacemaker functionality outside corosync cluster.
  + pengine: Check for master/slave resources that are not OCF agents
  + pengine: Support a 'requires' resource meta-attribute for controlling whether it needs quorum, fencing or nothing
  + pengine: Support for resource containers
  + pengine: Support resources that require unfencing before start

- Changes since Pacemaker-1.1.8
  + attrd: Correctly handle deletion of non-existant attributes
  + Bug cl#5135 - Improved detection of the active cluster type
  + Bug rhbz#913093 - Use crm_node instead of uname
  + cib: Prevent ordering changes when applying xml diffs
  + cib: Remove text nodes from cib replace operations
  + crmd: Prevent election storms caused by getrusage() values being too close
  + date/time: Bug cl#5118 - Correctly convert seconds-since-epoch to the current time
  + fencing: Attempt to provide more information that just 'generic error' for failed actions
  + fencing: Correctly record completed but previously unknown fencing operations
  + fencing: Correctly terminate when all device options have been exhausted
  + fencing: cov#739453 - String not null terminated
  + fencing: Do not merge new fencing requests with stale ones from dead nodes
  + fencing: Do not start fencing until entire device topology is found or query results timeout.
  + fencing: Do not wait for the query timeout if all replies have arrived
  + fencing: Fix passing of parameters from CMAN containing '='
  + fencing: Fix non-comparison when sorting devices by priority
  + fencing: On failure, only try a topology device once from the remote level.
  + fencing: Only try peers for non-topology based operations once
  + fencing: Retry stonith device for duration of action's timeout period.
  + ipc: Bug cl#5110 - Prevent 100% CPU usage when looking for synchronous replies
  + mcp: Re-attach to existing pacemaker components when mcp fails
  + pengine: Any location constraint for the slave role applies to all roles
  + pengine: Bug cl#5101 - Ensure stop order is preserved for partially active groups
  + pengine: Bug cl#5140 - Allow set members to be stopped when the subseqent set has require-all=false
  + pengine: Bug cl#5143 - Prevent shuffling of anonymous master/slave instances
  + pengine: Bug rhbz#880249 - Ensure orphan masters are demoted before being stopped
  + pengine: Bug rhbz#880249 - Teach the PE how to recover masters into primitives
  + pengine: cl#5025 - Automatically clear failcount for start/monitor failures after resource parameters change
  + pengine: cl#5099 - Probe operation uses the timeout value from the minimum interval monitor by default (#bnc776386)
  + pengine: cl#5111 - When clone/master child rsc has on-fail=stop, insure all children stop on failure.
  + pengine: cl#5142 - Do not delete orphaned children of an anonymous clone
  + pengine: Correctly unpack active anonymous clones
  + pengine: Ensure previous migrations are closed out before attempting another one
  + pengine: rhbz#902459 - Remove rsc node status for orphan resources
  + Replace the use of the insecure mktemp(3) with mkstemp(3)

* Thu Apr 04 2013 David Vossel <dvossel@redhat.com> - 1.1.8-6
  Fixes depreciated use of gnutls 3.1

* Thu Apr 04 2013 David Vossel <dvossel@redhat.com> - 1.1.8-5
  Rebuilt for gnutls 3.1

* Thu Oct 25 2012 Andrew Beekhof <abeekhof@redhat.com> - 1.1.8-4
- Update for new upstream tarball: 5db5f53

  + High: mcp: Re-attach to existing pacemaker components when pacemakerd fails
  + High: pengine: cl#5111 - When clone/master child rsc has on-fail=stop, insure all children stop on failure.
  + High: Replace the use of the insecure mktemp(3) with mkstemp(3)
  + High: Core: Correctly process XML diff's involving element removal
  + High: PE: Correctly unpack active anonymous clones
  + High: PE: Fix clone_zero() and clone_strip() for single character resource names
  + High: IPC: Bug cl#5110 - Prevent 100% CPU usage when looking for synchronous replies
  + High: PE: Bug cl#5101 - Ensure stop order is preserved for partially active groups
  + High: fencing: On failure, only try a topology device once from the remote level.
  + High: fencing: Retry stonith device for duration of action's timeout period.
  + High: PE: Fix memory leak on processing message (bnc#780224)
  + High: fencing: Support 'on_target' option in fencing device metadata for forcing unfence on target node
  + High: PE: Support resources that require unfencing before start
  + High: PE: Support a 'requires' resource meta-attribute for controlling whether it needs quorum, fencing or nothing
  + High: mcp: Only define HA_DEBUGLOG to avoid agent calls to ocf_log printing everything twice
  + High: fencing: Do not start fencing until entire device topology is found or query results timeout.
  + High: Cluster: Allow cman and corosync 2.0 nodes to use a name other than uname()

* Fri Sep 21 2012 Andrew Beekhof <andrew@beekhof.net> 1.1.8-3
- Only build for i386 and x86_64 as directed

* Fri Sep 21 2012 Andrew Beekhof <andrew@beekhof.net> 1.1.8-1
- Rebuild for upstream 1.1.8 release
- Documentation disabled pending a functional publican/ImageMagick combination

- Statistics:
  Changesets: 1019
  Diff:       2107 files changed, 117258 insertions(+), 73606 deletions(-)

- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for full details

  + New IPC implementation from libqb
  + New logging implementation from libqb
  + Quieter - info, debug and trace logs are no longer sent to syslog
  + Dropped dependancy on cluster-glue
  + Config and core directories no longer located in heartbeat directories
  + Support for managing systemd services
  + Rewritten local resource management daemon
  + Version bumps for every shared library due to API cleanups
  + Removes crm shell, install/use pcs shell and GUI instead

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 28 2012 Andrew Beekhof <andrew@beekhof.net> Pacemaker-1.1.7-2
- Reinstate the ghost directive for /var/run/crm

* Wed Mar 28 2012 Andrew Beekhof <andrew@beekhof.net> Pacemaker-1.1.7-1
- Update source tarball to upstream release: Pacemaker-1.1.7
- See included ChangeLog file or https://raw.github.com/ClusterLabs/pacemaker/master/ChangeLog for details

* Thu Feb 16 2012 Andrew Beekhof <andrew@beekhof.net> 1.1.7-0.3-7742926.git
- New upstream tarball: 7742926
- Additional Provides and Obsoletes directives to enable upgrading from heartbeat
- Rebuild now that the Corosync CFG API has been removed

* Thu Feb 02 2012 Andrew Beekhof <andrew@beekhof.net> 1.1.7-0.2-bc7c125.git
- Additional Provides and Obsoletes directives to enable upgrading from rgmanager

* Thu Feb 02 2012 Andrew Beekhof <andrew@beekhof.net> 1.1.7-0.1-bc7c125.git
- New upstream tarball: bc7c125
- Pre-release 1.1.7 build to deal with the removal of cman and support for corosync plugins
- Add libqb as a dependancy

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 26 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.6-3
- New upstream tarball: 89678d4
- Move man pages to the correct subpackages

* Mon Sep 26 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.6-2
- Do not build in support for heartbeat, snmp, esmtp by default
- Create a package for cluster unaware libraries to minimze our
  footprint on non-cluster nodes
- Better package descriptions

* Wed Sep 07 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.6-1
- Upstream release of 1.1.6
- See included ChangeLog file or http://hg.clusterlabs.org/pacemaker/1.1/file/tip/ChangeLog for details

- Disabled eSMTP and SNMP support.  Painful to configure and rarely used.
- Created cli sub-package for non-cluster usage

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.1.5-3.2
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.1.5-3.1
- Perl mass rebuild

* Mon Jul 11 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.5-3
- Rebuild for new snmp .so

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1.5-2.2
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.1.5-2.1
- Perl 5.14 mass rebuild

* Wed Apr 27 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.5-2
- Mark /var/run directories with ghost directive
  Resolves: rhbz#656654

* Wed Apr 27 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.5-1
- New upstream release plus patches for CMAN integration

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 11 2011 Andrew Beekhof <andrew@beekhof.net> 1.1.4-5
- Re-enable corosync and heartbeat support with correct bcond variable
  usage

* Wed Dec  8 2010 Fabio M. Di Nitto <fdinitto@redhat.com> 1.1.4-4
- Temporary drop publican doc build

* Wed Dec  8 2010 Fabio M. Di Nitto <fdinitto@redhat.com> 1.1.4-3
- Fix publican build on x86

* Wed Dec  8 2010 Fabio M. Di Nitto <fdinitto@redhat.com> 1.1.4-2
- Drop double source entry and 22Mb from the srpm

* Mon Nov 15 2010 Andrew Beekhof <andrew@beekhof.net> 1.1.4-1
- Upstream release of 1.1.4
- See included ChangeLog file or http://hg.clusterlabs.org/pacemaker/1.1/file/tip/ChangeLog for details

* Wed Sep 29 2010 jkeating - 1.1.3-1.1
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.3-1
- Upstream release of 1.1.3
  + High: crmd: Use the correct define/size for lrm resource IDs
  + High: crmd: Bug lf#2458 - Ensure stop actions always have the relevant resource attributes
  + High: crmd: Ensure we activate the DC timer if we detect an alternate DC
  + High: mcp: Correctly initialize the string containing the list of active daemons
  + High: mcp: Fix the expansion of the pid file in the init script
  + High: mcp: Tell chkconfig we need to shut down early on
  + High: PE: Bug lf#2476 - Repair on-fail=block for groups and primitive resources
  + High: PE: Do not demote resources because something that requires it can't run
  + High: PE: Rewrite the ordering constraint logic to be simplicity, clarity and maintainability
  + High: PE: Wait until stonith is available, don't fall back to shutdown for nodes requesting termination
  + High: PE: Prevent segfault by ensuring the arguments to do_calculations() are initialized
  + High: stonith: Bug lf#2461 - Prevent segfault by not looking up operations if the hashtable hasn't been initialized yet
  + High: Stonith: Bug lf#2473 - Ensure stonith operations complete within the timeout and are terminated if they run too long
  + High: stonith: Bug lf#2473 - Gracefully handle remote operations that arrive late (after we've done notifications)
  + High: stonith: Bug lf#2473 - Add the timeout at the top level where the daemon is looking for it
  + High: stonith: Bug lf#2473 - Ensure timeouts are included for fencing operations
  + High: Stonith: Use the timeout specified by the user
  + High: Tools: Bug lf#2456 - Fix assertion failure in crm_resource

* Mon Jul 26 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.3-0.1-b3cb4f4a30ae.hg
- Pre-release version of 1.1.3
  + High: ais: Bug lf2401 - Improved processing when the peer crmd processes join/leave
  + High: ais: fix list of active processes sent to clients (bnc#603685)
  + High: ais: Move the code for finding uid before the fork so that the child does no logging
  + High: ais: Resolve coverity CONSTANT_EXPRESSION_RESULT defects
  + High: cib: Also free query result for xpath operations that return more than one hit
  + High: cib: Attempt to resolve memory corruption when forking a child to write the cib to disk
  + High: cib: Correctly free memory when writing out the cib to disk
  + High: cib: Fix the application of unversioned diffs
  + High: cib: Remove old developmental error logging
  + High: cib: Restructure the 'valid peer' check for deciding which instructions to ignore
  + High: Core: Bug lf#2401 - Backed out changeset 6e6980376f01
  + High: Core: Correctly unpack HA_Messages containing multiple entries with the same name
  + High: Core: crm_count_member() should only track nodes that have the full stack up
  + High: Core: New developmental logging system inspired by the kernel and a PoC from Lars Ellenberg
  + High: crmd: All nodes should see status updates, not just he DC
  + High: crmd: Allow non-DC nodes to clear failcounts too
  + High: crmd: Base DC election on process relative uptime
  + High: crmd: Bug lf#2439 - cancel_op() can also return HA_RSCBUSY
  + High: crmd: Bug lf#2439 - Handle asynchronous notification of resource deletion events
  + High: crmd: Fix assertion failure when performing async resource failures
  + High: crmd: Fix handling of async resource deletion results
  + High: crmd: Include the action for crm graph operations
  + High: crmd: Make sure the membership cache is accurate after a sucessful fencing operation
  + High: crmd: Make sure we always poke the FSA after a transition to clear any TE_HALT actions
  + High: crmd: Offer crm-level membership once the peer starts the crmd process
  + High: crmd: Only need to request quorum update for plugin based clusters
  + High: crmd: Prevent everyone from loosing DC elections by correctly initializing all relevant variables
  + High: crmd: Prevent segmentation fault
  + High: crmd: several fixes for async resource delete
  + High: mcp: Add missing headers when built without heartbeat support
  + High: mcp: New master control process for (re)spawning pacemaker daemons
  + High: PE: Avoid creating invalid ordering constraints for probes that are not needed
  + High: PE: Bug lf#1959 - Fail unmanaged resources should not prevent other services from shutting down
  + High: PE: Bug lf#2422 - Ordering dependencies on partially active groups not observed properly
  + High: PE: Bug lf#2424 - Use notify oepration definition if it exists in the configuration
  + High: PE: Bug lf#2433 - No services should be stopped until probes finish
  + High: PE: Bug lf#2453 - Enforce clone ordering in the absense of colocation constraints
  + High: PE: Correctly detect when there is a real failcount that expired and needs to be cleared
  + High: PE: Correctly handle pseudo action creation
  + High: PE: Correctly order clone startup after group/clone start
  + High: PE: Fix colocation for interleaved clones
  + High: PE: Fix colocation with partially active groups
  + High: PE: Fix potential use-after-free defect from coverity
  + High: PE: Fix previous merge
  + High: PE: Fix use-after-free in order_actions() reported by valgrind
  + High: PE: Prevent endless loop when looking for operation definitions in the configuration
  + High: Resolve coverity RESOURCE_LEAK defects
  + High: Shell: Complete the transition to using crm_attribute instead of crm_failcount and crm_standby
  + High: stonith: Advertise stonith-ng options in the metadata
  + High: stonith: Correctly parse pcmk_host_list parameters that appear on a single line
  + High: stonith: Map poweron/poweroff back to on/off expected by the stonith tool from cluster-glue
  + High: stonith: pass the configuration to the stonith program via environment variables (bnc#620781)
  + High: Support starting plugin-based Pacemaker clusters with the MCP as well
  + High: tools: crm_report - corosync.conf wont necessarily contain the text 'pacemaker' anymore
  + High: tools: crm_simulate - Resolve coverity USE_AFTER_FREE defect
  + High: Tools: Drop the 'pingd' daemon and resource agent in favor of ocf:pacemaker:ping
  + High: Tools: Fix recently introduced use-of-NULL
  + High: Tools: Fix use-after-free defect from coverity

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.1.2-5.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul  9 2010 Dan Horák <dan[at]danny.cz> - 1.1.2-5
- re-enable AIS cluster on s390(x)

* Fri Jul  9 2010 Dan Horák <dan[at]danny.cz> - 1.1.2-4
- AIS cluster not available on s390(x)

* Mon Jun 21 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.2-3
- publican is only available as a dependancy on i386/x86_64 machines

* Fri Jun 11 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.2-2
- Resolves rhbz#602239 - Added patch to documentation so that it passes validation
- High: Core: Bug lf#2401 - Backed out changeset 6e6980376f01

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.1.2-1.1
- Mass rebuild with perl-5.12.0

* Wed May 12 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.2-1
- Update the tarball from the upstream 1.1.2 release
  + High: ais: Bug lf#2340 - Force rogue child processes to terminate after waiting 2.5 minutes
  + High: ais: Bug lf#2359 - Default expected votes to 2 inside Corosync/OpenAIS plugin
  + High: ais: Bug lf#2359 - expected-quorum-votes not correctly updated after membership change
  + High: ais: Bug rhbz#525552 - Move non-threadsafe calls to setenv() to after the fork()
  + High: ais: Do not count votes from offline nodes and calculate current votes before sending quorum data
  + High: ais: Ensure the list of active processes sent to clients is always up-to-date
  + High: ais: Fix previous commit, actually return a result in get_process_list()
  + High: ais: Fix two more uses of getpwnam() in non-thread-safe locations
  + High: ais: Look for the correct conf variable for turning on file logging
  + High: ais: Need to find a better and thread-safe way to set core_uses_pid. Disable for now.
  + High: ais: Use the threadsafe version of getpwnam
  + High: Core: Bug lf#2414 - Prevent use-after-free reported by valgrind when doing xpath based deletions
  + High: Core: Bump the feature set due to the new failcount expiry feature
  + High: Core: Fix memory leak in replace_xml_child() reported by valgrind
  + High: Core: fix memory leaks exposed by valgrind
  + High: crmd: Bug 2401 - Improved detection of partially active peers
  + High: crmd: Bug bnc#578644 - Improve handling of cancelled operations caused by resource cleanup
  + High: crmd: Bug lf#2379 - Ensure the cluster terminates when the PE is not available
  + High: crmd: Bug lf#2414 - Prevent use-after-free of the PE connection after it dies
  + High: crmd: Bug lf#2414 - Prevent use-after-free of the stonith-ng connection
  + High: crmd: Do not allow the target_rc to be misused by resource agents
  + High: crmd: Do not ignore action timeouts based on FSA state
  + High: crmd: Ensure we dont get stuck in S_PENDING if we loose an election to someone that never talks to us again
  + High: crmd: Fix memory leaks exposed by valgrind
  + High: crmd: Remove race condition that could lead to multiple instances of a clone being active on a machine
  + High: crmd: Send erase_status_tag() calls to the local CIB when the DC is fenced, since there is no DC to accept them
  + High: crmd: Use global fencing notifications to prevent secondary fencing operations of the DC
  + High: fencing: Account for stonith_get_info() always returning a pointer to the same static buffer
  + High: PE: Allow startup probes to be disabled - their calculation is a major bottleneck for very large clusters
  + High: PE: Bug lf#2317 - Avoid needless restart of primitive depending on a clone
  + High: PE: Bug lf#2358 - Fix master-master anti-colocation
  + High: PE: Bug lf#2361 - Ensure clones observe mandatory ordering constraints if the LHS is unrunnable
  + High: PE: Bug lf#2383 - Combine failcounts for all instances of an anonymous clone on a host
  + High: PE: Bug lf#2384 - Fix intra-set colocation and ordering
  + High: PE: Bug lf#2403 - Enforce mandatory promotion (colocation) constraints
  + High: PE: Bug lf#2412 - Correctly locate clone instances by their prefix
  + High: PE: Correctly implement optional colocation between primitives and clone resources
  + High: PE: Do not be so quick to pull the trigger on nodes that are coming up
  + High: PE: Fix memory leaks exposed by valgrind
  + High: PE: Fix memory leaks reported by valgrind
  + High: PE: Repair handling of unordered groups in RHS ordering constraints
  + High: PE: Rewrite native_merge_weights() to avoid Fix use-after-free
  + High: PE: Suppress duplicate ordering constraints to achieve orders of magnitude speed increases for large clusters
  + High: Shell: add support for xml in cli
  + High: Shell: always reload status if working with the cluster (bnc#590035)
  + High: Shell: check timeouts also against the default-action-timeout property
  + High: Shell: Default to using the status section from the live CIB (bnc#592762)
  + High: Shell: edit multiple meta_attributes sets in resource management (lf#2315)
  + High: Shell: enable comments (lf#2221)
  + High: Shell: implement new cibstatus interface and commands (bnc#580492)
  + High: Shell: improve configure commit (lf#2336)
  + High: Shell: new cibstatus import command (bnc#585471)
  + High: Shell: new configure filter command
  + High: Shell: restore error reporting in options
  + High: Shell: split shell into modules
  + High: Shell: support for the utilization element (old patch for the new structure)
  + High: Shell: update previous node lookup procedure to include the id where necessary
  + High: Tools: crm_mon - fix memory leaks exposed by valgrind

* Thu Feb 11 2010 Andrew Beekhof <andrew@beekhof.net> - 1.1.1-0.1-60b7753f7310.hg
- Update the tarball from upstream to version 60b7753f7310
  + First public release of the 1.1 series

* Wed Dec 9 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-5
- Include patch of changeset 66b7bfd467f3:
  Some clients such as gfs_controld want a cluster name, allow one to be specified in corosync.conf

* Thu Oct 29 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-4
- Include the fixes from CoroSync integration testing
- Move the resource templates - they are not documentation
- Ensure documentation is placed in a standard location
- Exclude documentation that is included elsewhere in the package

- Update the tarball from upstream to version ee19d8e83c2a
  + High: cib: Correctly clean up when both plaintext and tls remote ports are requested
  + High: PE: Bug bnc#515172 - Provide better defaults for lt(e) and gt(e) comparisions
  + High: PE: Bug lf#2197 - Allow master instances placemaker to be influenced by colocation constraints
  + High: PE: Make sure promote/demote pseudo actions are created correctly
  + High: PE: Prevent target-role from promoting more than master-max instances
  + High: ais: Bug lf#2199 - Prevent expected-quorum-votes from being populated with garbage
  + High: ais: Prevent deadlock - dont try to release IPC message if the connection failed
  + High: cib: For validation errors, send back the full CIB so the client can display the errors
  + High: cib: Prevent use-after-free for remote plaintext connections
  + High: crmd: Bug lf#2201 - Prevent use-of-NULL when running heartbeat
  + High: Core: Bug lf#2169 - Allow dtd/schema validation to be disabled
  + High: PE: Bug lf#2106 - Not all anonymous clone children are restarted after configuration change
  + High: PE: Bug lf#2170 - stop-all-resources option had no effect
  + High: PE: Bug lf#2171 - Prevent groups from starting if they depend on a complex resource which cannot
  + High: PE: Disable resource management if stonith-enabled=true and no stonith resources are defined
  + High: PE: Do not include master score if it would prevent allocation
  + High: ais: Avoid excessive load by checking for dead children every 1s (instead of 100ms)
  + High: ais: Bug rh#525589 - Prevent shutdown deadlocks when running on CoroSync
  + High: ais: Gracefully handle changes to the AIS nodeid
  + High: crmd: Bug bnc#527530 - Wait for the transition to complete before leaving S_TRANSITION_ENGINE
  + High: crmd: Prevent use-after-free with LOG_DEBUG_3
  + Medium: xml: Mask the "symmetrical" attribute on rsc_colocation constraints (bnc#540672)
  + Medium (bnc#520707): Tools: crm: new templates ocfs2 and clvm
  + Medium: Build: Invert the disable ais/heartbeat logic so that --without (ais|heartbeat) is available to rpmbuild
  + Medium: PE: Bug lf#2178 - Indicate unmanaged clones
  + Medium: PE: Bug lf#2180 - Include node information for all failed ops
  + Medium: PE: Bug lf#2189 - Incorrect error message when unpacking simple ordering constraint
  + Medium: PE: Correctly log resources that would like to start but cannot
  + Medium: PE: Stop ptest from logging to syslog
  + Medium: ais: Include version details in plugin name
  + Medium: crmd: Requery the resource metadata after every start operation

* Fri Oct  9 2009 Fabio M. Di Nitto <fdinitto@redhat.com> - 1.0.5-3
- rebuilt with new net-snmp

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.0.5-2.1
- rebuilt with new openssl

* Wed Aug 19 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-2
- Add versioned perl dependancy as specified by
    https://fedoraproject.org/wiki/Packaging/Perl#Packages_that_link_to_libperl
- No longer remove RPATH data, it prevents us finding libperl.so and no other
  libraries were being hardcoded
- Compile in support for heartbeat
- Conditionally add heartbeat-devel and corosynclib-devel to the -devel requirements
  depending on which stacks are supported

* Mon Aug 17 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-1
- Add dependancy on resource-agents
- Use the version of the configure macro that supplies --prefix, --libdir, etc
- Update the tarball from upstream to version 462f1569a437 (Pacemaker 1.0.5 final)
  + High: Tools: crm_resource - Advertise --move instead of --migrate
  + Medium: Extra: New node connectivity RA that uses system ping and attrd_updater
  + Medium: crmd: Note that dc-deadtime can be used to mask the brokeness of some switches

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.0.5-0.7.c9120a53a6ae.hg
- Use bzipped upstream tarball.

* Wed Jul  29 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-0.6.c9120a53a6ae.hg
- Add back missing build auto* dependancies
- Minor cleanups to the install directive

* Tue Jul  28 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-0.5.c9120a53a6ae.hg
- Add a leading zero to the revision when alphatag is used

* Tue Jul  28 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.5-0.4.c9120a53a6ae.hg
- Incorporate the feedback from the cluster-glue review
- Realistically, the version is a 1.0.5 pre-release
- Use the global directive instead of define for variables
- Use the haclient/hacluster group/user instead of daemon
- Use the _configure macro
- Fix install dependancies

* Fri Jul  24 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.4-3
- Include an AUTHORS and license file in each package
- Change the library package name to pacemaker-libs to be more
  Fedora compliant
- Remove execute permissions from xml related files
- Reference the new cluster-glue devel package name
- Update the tarball from upstream to version c9120a53a6ae
  + High: PE: Only prevent migration if the clone dependancy is stopping/starting on the target node
  + High: PE: Bug 2160 - Dont shuffle clones due to colocation
  + High: PE: New implementation of the resource migration (not stop/start) logic
  + Medium: Tools: crm_resource - Prevent use-of-NULL by requiring a resource name for the -A and -a options
  + Medium: PE: Prevent use-of-NULL in find_first_action()
  + Low: Build: Include licensing files

* Tue Jul 14 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.4-2
- Reference authors from the project AUTHORS file instead of listing in description
- Change Source0 to reference the project's Mercurial repo
- Cleaned up the summaries and descriptions
- Incorporate the results of Fedora package self-review

* Tue Jul 14 2009 Andrew Beekhof <andrew@beekhof.net> - 1.0.4-1
- Initial checkin
