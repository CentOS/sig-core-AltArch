
%global pkgname   dirsrv
# for a pre-release, define the prerel field e.g. .a1 .rc2 - comment out for official release
# also remove the space between % and global - this space is needed because
# fedpkg verrel stupidly ignores comment lines
#% global prerel .rc3
# also need the relprefix field for a pre-release e.g. .0 - also comment out for official release
#% global relprefix 0.

# If perl-Socket-2.000 or newer is available, set 0 to use_Socket6.
%global use_Socket6 0
%global use_nunc_stans 1

%ifnarch s390 s390x %{arm}
%global use_tcmalloc 1
%else
%global use_tcmalloc 0
%endif

# fedora 15 and later uses tmpfiles.d
# otherwise, comment this out
%{!?with_tmpfiles_d: %global with_tmpfiles_d %{_sysconfdir}/tmpfiles.d}

# systemd support
%global groupname %{pkgname}.target

# set PIE flag
%global _hardened_build 1

Summary:          389 Directory Server (base)
Name:             389-ds-base
Version:          1.3.6.1
Release:          %{?relprefix}28%{?prerel}%{?dist}
License:          GPLv3+
URL:              https://www.port389.org/
Group:            System Environment/Daemons
BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Conflicts:        selinux-policy-base < 3.9.8
Requires:         %{name}-libs = %{version}-%{release}
Provides:         ldif2ldbm >= 0

BuildRequires:    nspr-devel
BuildRequires:    nss-devel
BuildRequires:    svrcore-devel >= 4.1.3
BuildRequires:    openldap-devel
BuildRequires:    libdb-devel
BuildRequires:    cyrus-sasl-devel
BuildRequires:    icu
BuildRequires:    libicu-devel
BuildRequires:    pcre-devel
BuildRequires:    gcc-c++
# The following are needed to build the snmp ldap-agent
BuildRequires:    net-snmp-devel
%ifnarch sparc sparc64 ppc ppc64 s390 s390x
BuildRequires:    lm_sensors-devel
%endif
BuildRequires:    bzip2-devel
BuildRequires:    zlib-devel
BuildRequires:    openssl-devel
BuildRequires:    tcp_wrappers
# the following is for the pam passthru auth plug-in
BuildRequires:    pam-devel
BuildRequires:    systemd-units
BuildRequires:    systemd-devel
# Needed to support regeneration of the autotool artifacts.
BuildRequires:    autoconf
BuildRequires:    automake
BuildRequires:    libtool
%if %{use_nunc_stans}
BuildRequires:    libevent-devel
BuildRequires:    libtalloc-devel
BuildRequires:    libtevent-devel
%endif
# For tests!
#BuildRequires:    libcmocka-devel
BuildRequires:    doxygen

# this is needed for using semanage from our setup scripts
Requires:         policycoreutils-python
Requires:         /usr/sbin/semanage
Requires:         libsemanage-python 

Requires:         selinux-policy >= 3.13.1-137

# the following are needed for some of our scripts
Requires:         openldap-clients
# use_openldap assumes perl-Mozilla-LDAP is built with openldap support
Requires:         perl-Mozilla-LDAP

# this is needed to setup SSL if you are not using the
# administration server package
Requires:         nss-tools

# these are not found by the auto-dependency method
# they are required to support the mandatory LDAP SASL mechs
Requires:         cyrus-sasl-gssapi
Requires:         cyrus-sasl-md5
Requires:         cyrus-sasl-plain

# this is needed for verify-db.pl
Requires:         libdb-utils

# This picks up libperl.so as a Requires, so we add this versioned one
Requires:         perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

# for the init script
Requires(post):   systemd-units
Requires(preun):  systemd-units
Requires(postun): systemd-units

# for setup-ds.pl
Requires:         bind-utils

# for setup-ds.pl to support ipv6 
%if %{use_Socket6}
Requires:         perl-Socket6
%else 
Requires:         perl-Socket
%endif
Requires:         perl-NetAddr-IP
Requires:         systemd-libs
Requires:         svrcore >= 4.1.3

# upgrade path from monolithic % {name} (including -libs & -devel) to % {name} + % {name}-snmp
Obsoletes:        %{name} <= 1.3.5.4

%if %{use_tcmalloc}
BuildRequires:    gperftools-devel
Requires:         gperftools-libs
%endif

Source0:          http://www.port389.org/binaries/%{name}-%{version}%{?prerel}.tar.bz2
# 389-ds-git.sh should be used to generate the source tarball from git
Source1:          %{name}-git.sh
Source2:          %{name}-devel.README
Patch0:           0000-Ticket-49164-Change-NS-to-acq-rel-semantics-for-atom.patch
Patch1:           0001-Issue-49170-sync-plugin-thread-count-not-handled-cor.patch
Patch2:           0002-Ticket-49165-pw_verify-did-not-handle-external-auth.patch
Patch3:           0003-Issue-49169-Fix-covscan-errors.patch
Patch4:           0004-Ticket-49171-Nunc-Stans-incorrectly-reports-a-timeou.patch
Patch5:           0005-Issue-49169-Fix-covscan-errors-regression.patch
Patch6:           0006-Issue-49062-Reset-agmt-update-staus-and-total-init
Patch7:           0007-Issue-49065-dbmon.sh-fails-if-you-have-nsslapd-requi.patch
Patch8:           0008-Issue-49095-targetattr-wildcard-evaluation-is-incorr.patch
Patch9:           0009-Issue-49157-ds-logpipe.py-crashes-for-non-existing-u.patch
Patch10:          0010-Fix-double-free-in-_cl5NewDBFile-error-path.patch
Patch11:          0011-Issue-49188-retrocl-can-crash-server-at-shutdown.patch
Patch12:          0012-Ticket-49177-rpm-would-not-create-valid-pkgconfig-fi.patch
Patch13:          0013-Ticket-49076-To-debug-DB_DEADLOCK-condition-allow-to.patch
Patch14:          0014-Issue-49192-Deleting-suffix-can-hang-server.patch
Patch15:          0015-Ticket-49174-nunc-stans-can-not-use-negative-timeout.patch
Patch16:          0016-Issue-48989-Integer-overflow.patch
Patch17:          0017-Issue-49035-dbmon.sh-shows-pages-in-use-that-exceeds.patch
Patch18:          0018-Issue-49177-Fix-pkg-config-file.patch
Patch19:          0019-Issue-49205-Fix-logconv.pl-man-page.patch
Patch20:          0020-Issue-49039-password-min-age-should-be-ignored-if-pa.patch
Patch21:          0021-fix-for-cve-2017-2668-simple-return-text-if-suffix-n.patch
Patch22:          0022-Issue-47662-CLI-args-get-removed.patch
Patch23:          0023-Issue-49210-Fix-regression-when-checking-is-password.patch 
Patch24:          0024-Ticket-49209-Hang-due-to-omitted-replica-lock-releas.patch
Patch25:          0025-Ticket-49184-Overflow-in-memberof.patch
Patch26:          0026-Ticket-49196-Autotune-generates-crit-messages.patch
Patch27:          0027-Issue-49221-During-an-upgrade-the-provided-localhost.patch
Patch28:          0028-Ticket-48864-Add-cgroup-memory-limit-detection-to-38.patch
Patch29:          0029-Ticket-49204-Fix-lower-bounds-on-import-autosize-On-.patch
Patch30:          0030-Ticket-49231-fix-sasl-mech-handling.patch
Patch31:          0031-Ticket-49230-slapi_register_plugin-creates-config-en.patch
Patch32:          0032-49227-ldapsearch-for-nsslapd-errorlog-level-re.patch
Patch33:          0033-Ticket-48989-fix-perf-counters.patch
Patch34:          0034-Ticket-48681-logconv.pl-fix-sasl-bind-stats.patch
Patch35:          0035-Ticket-49241-Update-man-page-and-usage-for-db2bak.pl.patch
Patch36:          0036-Ticket-7662-db2index-not-properly-evalauating-argume.patch
Patch37:          0037-Ticket-49075-Adjust-logging-severity-levels.patch
Patch38:          0038-Ticket-49231-Fix-backport-issue.patch
Patch39:          0039-Ticket-49231-Fix-backport-issue-part2.patch
Patch40:          0040-Ticket-48681-logconv.pl-Fix-SASL-Bind-stats-and-rewo.patch
Patch41:          0041-Ticket-49157-ds-logpipe.py-crashes-for-non-existing-.patch
Patch42:          0042-Ticket-49249-cos_cache-is-erroneously-logging-schema.patch
Patch43:          0043-Ticket-49238-AddressSanitizer-heap-use-after-free-in.patch
Patch44:          0044-Ticket-49246-ns-slapd-crashes-in-role-cache-creation.patch
Patch45:          0045-Ticket-49258-Allow-nsslapd-cache-autosize-to-be-modi.patch
Patch46:          0046-Ticket-49261-Fix-script-usage-and-man-pages.patch
Patch47:          0047-Ticket-48864-Fix-FreeIPA-build.patch
Patch48:          0048-Ticket-49157-fix-error-in-ds-logpipe.py.patch
Patch49:          0049-Ticket-49267-autosize-split-of-0-results-in-dbcache-.patch
Patch50:          0050-Ticket-49231-force-EXTERNAL-always.patch
Patch51:          0051-Ticket-48538-Failed-to-delete-old-semaphore.patch
Patch52:          0052-Ticket-49257-Reject-nsslapd-cachememsize-nsslapd-cac.patch
Patch53:          0053-Ticket-49257-Reject-dbcachesize-updates-while-auto-c.patch
Patch54:          0054-Ticket-49184-adjust-logging-level-in-MO-plugin.patch
Patch55:          0055-Ticket-49241-add-symblic-link-location-to-db2bak.pl-.patch
Patch56:          0056-Ticket-49313-Change-the-retrochangelog-default-cache.patch
Patch57:          0057-Ticket-49287-v3-extend-csnpl-handling-to-multiple-ba.patch
Patch58:          0058-Ticket-49336-SECURITY-Locked-account-provides-differ.patch
Patch59:          0059-Ticket-49298-force-sync-on-shutdown.patch
Patch60:          0060-Ticket-49334-fix-backup-restore-if-changelog-exists.patch
Patch61:          0061-Ticket-49356-mapping-tree-crash-can-occur-during-tot.patch
Patch62:          0062-Ticket-49330-Improve-ndn-cache-performance-1.3.6.patch
Patch63:          0063-Ticket-49330-Add-endian-header-file-check-to-configu.patch
Patch64:          0064-Ticket-49257-only-register-modify-callbacks.patch
Patch65:          0065-Ticket-49291-slapi_search_internal_callback_pb-may-S.patch
Patch66:          0066-Ticket-49370-local-password-policies-should-use-the-.patch
Patch67:          0067-Ticket-49380-Crash-when-adding-invalid-replication.patch
Patch68:          0068-Ticket-49380-Add-CI-test.patch
Patch69:          0069-Ticket-49327-password-expired-control-not-sent-durin.patch
Patch70:          0070-Ticket-49379-Allowed-sasl-mapping-requires-restart.patch
Patch71:          0071-Fix-cherry-pick-error-from-sasl-mech-commit.patch
Patch72:          0072-Ticket-49389-unable-to-retrieve-specific-cosAttribut.patch
Patch73:          0073-Ticket-49180-backport-1.3.6-errors-log-filled-with-a.patch
Patch74:          0074-Ticket-48894-harden-valueset_array_to_sorted_quick-v.patch
Patch75:          0075-Ticket-49401-improve-valueset-sorted-performance-on-.patch
Patch76:          0076-Ticket-49401-Fix-compiler-incompatible-pointer-types.patch
Patch77:          0077-Ticket-48235-Remove-memberOf-global-lock.patch
Patch78:          0078-Ticket-49402-Adding-a-database-entry-with-the-same-d.patch
Patch79:          0079-Ticket-49439-cleanallruv-is-not-logging-information.patch
Patch80:          0080-Ticket-49436-double-free-in-COS-in-some-conditions.patch
Patch81:          0081-Ticket-49441-Import-crashes-with-large-indexed-binar.patch
Patch82:          0082-Ticket-49431-replicated-MODRDN-fails-breaking-replic.patch
Patch83:          0083-Ticket-49410-opened-connection-can-remain-no-longer-.patch
Patch84:          0084-Ticket-48118-backport-changelog-can-be-erronously-re.patch
Patch85:          0085-Ticket-49495-Fix-memory-management-is-vattr.patch
Patch86:          0086-CVE-2017-15134-389-ds-base-Remote-DoS-via-search-fil.patch
Patch87:          0087-Ticket-49509-Indexing-of-internationalized-matching-.patch
Patch88:          0088-Ticket-bz1525628-1.3.6-backport-invalid-password-mig.patch
Patch89:          0089-Ticket-49545-final-substring-extended-filter-search-.patch
Patch90:          0090-Ticket-49471-heap-buffer-overflow-in-ss_unescape.patch

%description
389 Directory Server is an LDAPv3 compliant server.  The base package includes
the LDAP server and command line utilities for server administration.

%package          libs
Summary:          Core libraries for 389 Directory Server
Group:            System Environment/Daemons
BuildRequires:    nspr-devel
BuildRequires:    nss-devel
BuildRequires:    svrcore-devel >= 4.1.3
BuildRequires:    openldap-devel
BuildRequires:    libdb-devel
BuildRequires:    cyrus-sasl-devel
BuildRequires:    libicu-devel
BuildRequires:    pcre-devel
%if %{use_nunc_stans}
BuildRequires:    libtalloc-devel
BuildRequires:    libevent-devel
BuildRequires:    libtevent-devel
%endif
BuildRequires:    systemd-devel

%description      libs
Core libraries for the 389 Directory Server base package.  These libraries
are used by the main package and the -devel package.  This allows the -devel
package to be installed with just the -libs package and without the main package.

%package          devel
Summary:          Development libraries for 389 Directory Server
Group:            Development/Libraries
Requires:         %{name}-libs = %{version}-%{release}
Requires:         pkgconfig
Requires:         nspr-devel
Requires:         nss-devel
Requires:         svrcore-devel >= 4.1.3
Requires:         openldap-devel
%if %{use_nunc_stans}
Requires:         libtalloc
Requires:         libevent
Requires:         libtevent
%endif
Requires:         systemd-libs

%description      devel
Development Libraries and headers for the 389 Directory Server base package.

%package          snmp
Summary:          SNMP Agent for 389 Directory Server
Group:            System Environment/Daemons
Requires:         %{name} = %{version}-%{release}
# upgrade path from monolithic %{name} (including -libs & -devel) to %{name} + %{name}-snmp
Obsoletes:        %{name} <= 1.3.6.0

%description      snmp
SNMP Agent for the 389 Directory Server base package.

%package          tests
Summary:          The lib389 Continuous Integration Tests
Group:            Development/Libraries
Requires:         python-lib389
BuildArch:        noarch

%description      tests
The lib389 CI tests that can be run against the Directory Server.

%prep
%setup -q -n %{name}-%{version}%{?prerel}
cp %{SOURCE2} README.devel
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
%patch27 -p1
%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1
%patch38 -p1
%patch39 -p1
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1
%patch54 -p1
%patch55 -p1
%patch56 -p1
%patch57 -p1
%patch58 -p1
%patch59 -p1
%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1
%patch65 -p1
%patch66 -p1
%patch67 -p1
%patch68 -p1
%patch69 -p1
%patch70 -p1
%patch71 -p1
%patch72 -p1
%patch73 -p1
%patch74 -p1
%patch75 -p1
%patch76 -p1
%patch77 -p1
%patch78 -p1
%patch79 -p1
%patch80 -p1
%patch81 -p1
%patch82 -p1
%patch83 -p1
%patch84 -p1
%patch85 -p1
%patch86 -p1
%patch87 -p1
%patch88 -p1
%patch89 -p1
%patch90 -p1

%build

OPENLDAP_FLAG="--with-openldap"
%{?with_tmpfiles_d: TMPFILES_FLAG="--with-tmpfiles-d=%{with_tmpfiles_d}"}
# hack hack hack https://bugzilla.redhat.com/show_bug.cgi?id=833529
NSSARGS="--with-svrcore-inc=%{_includedir} --with-svrcore-lib=%{_libdir} --with-nss-lib=%{_libdir} --with-nss-inc=%{_includedir}/nss3"
%if %{use_nunc_stans}
NUNC_STANS_FLAGS="--enable-nunc-stans"
%endif
%if %{use_tcmalloc}
TCMALLOC_FLAGS="--enable-tcmalloc"
%endif

# Rebuild the autotool artifacts now.
autoreconf -fiv

%configure --enable-autobind --with-selinux $OPENLDAP_FLAG $TMPFILES_FLAG \
           --with-systemdsystemunitdir=%{_unitdir} \
           --with-systemdsystemconfdir=%{_sysconfdir}/systemd/system \
           --with-perldir=/usr/bin \
           --with-systemdgroupname=%{groupname} $NSSARGS $NUNC_STANS_FLAGS \
           --with-systemd $TCMALLOC_FLAGS

# Generate symbolic info for debuggers
export XCFLAGS=$RPM_OPT_FLAGS

%ifarch x86_64 ppc64 ia64 s390x sparc64
export USE_64=1
%endif

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make DESTDIR="$RPM_BUILD_ROOT" install

# Copy in our docs from doxygen.
cp -r %{_builddir}/%{name}-%{version}%{?prerel}/man/man3 $RPM_BUILD_ROOT/%{_mandir}/man3

mkdir -p $RPM_BUILD_ROOT/var/log/%{pkgname}
mkdir -p $RPM_BUILD_ROOT/var/lib/%{pkgname}
mkdir -p $RPM_BUILD_ROOT/var/lock/%{pkgname}

# for systemd
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system/%{groupname}.wants

#remove libtool archives and static libs
find %{buildroot} -type f -name "*.la" -delete
find %{buildroot} -type f -name "*.a" -delete
#rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/*.a
#rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/*.la
#rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/plugins/*.a
#rm -f $RPM_BUILD_ROOT%{_libdir}/%{pkgname}/plugins/*.la

# Why are we not making this a proper python package?
pushd ../%{name}-%{version}%{?prerel}
cp -r dirsrvtests $RPM_BUILD_ROOT/%{_sysconfdir}/%{pkgname}
find $RPM_BUILD_ROOT/%{_sysconfdir}/%{pkgname}/dirsrvtests -type f -name '*.pyc' -delete
find $RPM_BUILD_ROOT/%{_sysconfdir}/%{pkgname}/dirsrvtests -type f -name '*.pyo' -delete
find $RPM_BUILD_ROOT/%{_sysconfdir}/%{pkgname}/dirsrvtests -type d -name '__pycache__' -delete
popd

# make sure perl scripts have a proper shebang
sed -i -e 's|#{{PERL-EXEC}}|#!/usr/bin/perl|' $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/script-templates/template-*.pl

%clean
rm -rf $RPM_BUILD_ROOT

%post
output=/dev/null
output2=/dev/null
# reload to pick up any changes to systemd files
/bin/systemctl daemon-reload >$output 2>&1 || :
# reload to pick up any shared lib changes
/sbin/ldconfig
# find all instances
instances="" # instances that require a restart after upgrade
ninst=0 # number of instances found in total
if [ -n "$DEBUGPOSTTRANS" ] ; then
   output=$DEBUGPOSTTRANS
   output2=${DEBUGPOSTTRANS}.upgrade
fi

# Soft static allocation for UID and GID
USERNAME="dirsrv"
ALLOCATED_UID=389
GROUPNAME="dirsrv"
ALLOCATED_GID=389
HOMEDIR="/usr/share/dirsrv"

getent group $GROUPNAME >/dev/null || /usr/sbin/groupadd -f -g $ALLOCATED_GID -r $GROUPNAME
if ! getent passwd $USERNAME >/dev/null ; then
    /usr/sbin/useradd -r -u $ALLOCATED_UID -g $GROUPNAME -d $HOMEDIR -s /sbin/nologin -c "user for 389-ds-base" $USERNAME
fi

echo looking for instances in %{_sysconfdir}/%{pkgname} > $output 2>&1 || :
instbase="%{_sysconfdir}/%{pkgname}"
for dir in $instbase/slapd-* ; do
    echo dir = $dir >> $output 2>&1 || :
    if [ ! -d "$dir" ] ; then continue ; fi
    case "$dir" in *.removed) continue ;; esac
    basename=`basename $dir`
    inst="%{pkgname}@`echo $basename | sed -e 's/slapd-//g'`"
    echo found instance $inst - getting status  >> $output 2>&1 || :
    if /bin/systemctl -q is-active $inst ; then
       echo instance $inst is running >> $output 2>&1 || :
       instances="$instances $inst"
    else
       echo instance $inst is not running >> $output 2>&1 || :
    fi
    ninst=`expr $ninst + 1`
done
if [ $ninst -eq 0 ] ; then
    echo no instances to upgrade >> $output 2>&1 || :
    exit 0 # have no instances to upgrade - just skip the rest
fi
# shutdown all instances
echo shutting down all instances . . . >> $output 2>&1 || :
for inst in $instances ; do
    echo stopping instance $inst >> $output 2>&1 || :
    /bin/systemctl stop $inst >> $output 2>&1 || :
done
echo remove pid files . . . >> $output 2>&1 || :
/bin/rm -f /var/run/%{pkgname}*.pid /var/run/%{pkgname}*.startpid
# do the upgrade
echo upgrading instances . . . >> $output 2>&1 || :
DEBUGPOSTSETUPOPT=`/usr/bin/echo $DEBUGPOSTSETUP | /usr/bin/sed -e "s/[^d]//g"`
if [ -n "$DEBUGPOSTSETUPOPT" ] ; then
    %{_sbindir}/setup-ds.pl -$DEBUGPOSTSETUPOPT -u -s General.UpdateMode=offline >> $output 2>&1 || :
else
    %{_sbindir}/setup-ds.pl -u -s General.UpdateMode=offline >> $output 2>&1 || :
fi

# restart instances that require it
for inst in $instances ; do
    echo restarting instance $inst >> $output 2>&1 || :
    /bin/systemctl start $inst >> $output 2>&1 || :
done
exit 0

%preun
if [ $1 -eq 0 ]; then # Final removal
    # remove instance specific service files/links
    rm -rf %{_sysconfdir}/systemd/system/%{groupname}.wants/* > /dev/null 2>&1 || :
fi

%postun
/sbin/ldconfig
if [ $1 = 0 ]; then # Final removal
    rm -rf /var/run/%{pkgname}
fi

%post snmp
%systemd_post %{pkgname}-snmp.service

%preun snmp
%systemd_preun %{pkgname}-snmp.service %{groupname}

%postun snmp
%systemd_postun_with_restart %{pkgname}-snmp.service

%files
%defattr(-,root,root,-)
%doc LICENSE LICENSE.GPLv3+ LICENSE.openssl
%dir %{_sysconfdir}/%{pkgname}
%dir %{_sysconfdir}/%{pkgname}/schema
%config(noreplace)%{_sysconfdir}/%{pkgname}/schema/*.ldif
%dir %{_sysconfdir}/%{pkgname}/config
%dir %{_sysconfdir}/systemd/system/%{groupname}.wants
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/slapd-collations.conf
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/certmap.conf
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/template-initconfig
%config(noreplace)%{_sysconfdir}/sysconfig/%{pkgname}
%config(noreplace)%{_sysconfdir}/sysconfig/%{pkgname}.systemd
%{_datadir}/%{pkgname}
%{_unitdir}
%{_bindir}/*
%{_sbindir}/*
%{_libdir}/%{pkgname}/perl
%{_libdir}/%{pkgname}/python
%dir %{_libdir}/%{pkgname}/plugins
%{_libdir}/%{pkgname}/plugins/*.so
%dir %{_localstatedir}/lib/%{pkgname}
%dir %{_localstatedir}/log/%{pkgname}
%ghost %dir %{_localstatedir}/lock/%{pkgname}
%{_mandir}/man1/*
%{_mandir}/man8/*
%exclude %{_sbindir}/ldap-agent*
%exclude %{_mandir}/man1/ldap-agent.1.gz
%exclude %{_unitdir}/%{pkgname}-snmp.service

%files devel
%defattr(-,root,root,-)
%doc LICENSE LICENSE.GPLv3+ LICENSE.openssl README.devel
%{_includedir}/%{pkgname}
%{_libdir}/%{pkgname}/libslapd.so
%{_libdir}/%{pkgname}/libns-dshttpd.so
%{_mandir}/man3/*
%if %{use_nunc_stans}
%{_libdir}/%{pkgname}/libnunc-stans.so
%{_libdir}/%{pkgname}/libsds.so
%endif
%{_libdir}/pkgconfig/*

%files libs
%defattr(-,root,root,-)
%doc LICENSE LICENSE.GPLv3+ LICENSE.openssl README.devel
%dir %{_libdir}/%{pkgname}
%{_libdir}/%{pkgname}/libslapd.so.*
%{_libdir}/%{pkgname}/libns-dshttpd-*.so
%if %{use_nunc_stans}
%{_libdir}/%{pkgname}/libnunc-stans.so.*
%{_libdir}/%{pkgname}/libsds.so.*
%endif

%files snmp
%defattr(-,root,root,-)
%doc LICENSE LICENSE.GPLv3+ LICENSE.openssl README.devel
%config(noreplace)%{_sysconfdir}/%{pkgname}/config/ldap-agent.conf
%{_sbindir}/ldap-agent*
%{_mandir}/man1/ldap-agent.1.gz
%{_unitdir}/%{pkgname}-snmp.service

%files tests
%defattr(-,root,root,-)
%doc LICENSE LICENSE.GPLv3+
%{_sysconfdir}/%{pkgname}/dirsrvtests

%changelog
* Wed Mar  7 2018 Johnny Hughes <johnnny@centos.org> - 1.3.6.1-28
- Disabled tcmalloc for armhfp (jacco@redsleeve.org)

* Mon Feb 26 2018 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-28
- Bump version to 1.3.6.1-28
- Resolves: Bug 1540105 - CVE-2018-1054 - remote Denial of Service (DoS) via search filters in SetUnicodeStringFromUTF_8

* Tue Feb 13 2018 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-27
- Bump version to 1.3.6.1-27
- Resolves: Bug 1536343 - Indexing of internationalized matching rules is failing
- Resolves: Bug 1535539 - CVE-2017-15135 - Authentication bypass due to lack of size check in slapi_ct_memcmp function
- Resolves: Bug 1540105 - CVE-2018-1054 - remote Denial of Service (DoS) via search filters in SetUnicodeStringFromUTF_8

* Tue Jan 16 2018 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-26
- Bump version to 1.3.6.1-26
- Resolves: Bug 1534430 - crash in slapi_filter_sprintf 

* Mon Dec 18 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-25
- Bump version to 1.3.6.1-25
- Resolves: Bug 1526928 - search with CoS attribute is getting slower after modifying/adding CosTemplate
- Resolves: Bug 1523505 - opened connection are hanging, no longer poll
- Resolves: Bug 1523507 - IPA server replication broken, after DS stop-start, due to changelog reset

* Fri Nov 10 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-24
- Bump version to 1.3.6.1-24
- Resolves: Bug 1508978 - replicated MODRDN fails breaking replication
- Resolves: Bug 1511940 - heap corruption during import
- Resolves: Bug 1510319 - [abrt] 389-ds-base: SLL_Next(): ns-slapd killed by SIGSEGV 
- Resolves: Bug 1509347 - cleanallruv task is not logging any information

* Fri Oct 27 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-23
- Bump version to 1.3.6.1-23
- Resolves: Bug 1504536 - [memberOf Plugin] bulk deleting users causes deadlock when there are multiple backends
- Resolves: Bug 1503001 - Adding a database entry fails if the same database was deleted after an import
- Resolves: Bug 1506912 - Improve valueset sort performance during valueset purging

* Mon Oct 9 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-22
- Bump version to 1.3.6.1-22
- Resolves: Bug 1499668 - Errors log filled with attrlist_replace

* Thu Oct 5 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-21
- Bump verions to 1.3.6.1-21
- Resolves: Bug 1498958 - unable to retrieve specific cosAttribute when subtree password policy is configured

* Mon Sep 18 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-20
- Bump verions to 1.3.6.1-20
- Resolves: Bug 1489693 - PasswordCheckSyntax attribute fails to validate cn, sn, uid
- Resovles: Bug 1492829 - patch should of been applied to 7.4 but got missed
- Resolves: Bug 1486128 - Performance issues with RHDS 10 - NDN cache investigation
- Resolves: Bug 1489694 - crash in send_ldap_result
- Resolves: Bug 1491778 - crash when adding invalid repl agmt
- Resolves: Bug 1492830 - password expired control not sent
- Resolves: Bug 1492833 - sasl-mechanisms removed during upgrade

* Mon Aug 21 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-19
- Bump version to 1.3.6.1-19
- Remove old mozldap and db4 requirements
- Resolves: Bug 1483865 - Crash while binding to a server during replication online init

* Tue Aug 8 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-18
- Bump version to 1.3.6.1-18
- Require srvcore 4.1.3
- Resolves: Bug 1479757 - dse.ldif and fsync
- Resolves: Bug 1479755 - backup fails if changelog is enabled
- Resolves: Bug 1479756 - Locked account provides different return code if password is correct 

* Mon Jul 31 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-17
- Bump version to 1.3.6.1-17
- Resolves: Bug 1476161 - replication halt - pending list first CSN not committed, pending list increasing
- Resolves: Bug 1476162 - Change the retrochangelog default cache size

* Tue Jun 6 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-16
- Bump version to 1.3.6.1-16
- Resolves: Bug 1444938 - nsslapd-allowed-sasl-mechanisms doesn't reset to default values without a restart
- Resolves: Bug 1447015 - Adjust db2bak.pl help and man page to reflect changes introduced to the script
- Resolves: Bug 1450896 - Manual resetting of nsslapd-dbcachesize using ldapmodify
- Resolves: Bug 1454921 - Fixup memberof task throws error "memberof_fix_memberof_callback: Weird
- Resolves: Bug 1456774 - ipa-replica server fails to upgrade

* Tue May 23 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-15
- Bump version to 1.3.6.1-15
- Resolves: Bug 1429770 - ds-logpipe.py crashes for non-existing users
- Resolves: Bug 1444938 - nsslapd-allowed-sasl-mechanisms doesn't reset to default values without a restart
- Resolves: Bug 1450896 - Manual resetting of nsslapd-dbcachesize using ldapmodify 
- Resolves: Bug 1357682 - RHDS fails to start with message: "Failed to delete old semaphore for stats file"
- Resolves: Bug 1452739 - Zero value of nsslapd-cache-autosize-split makes dbcache to be equal 0

* Fri May 19 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-14
- Bump version to 1.3.6.1-14
- Resolves: Bug 1450910 - Modifying "nsslapd-cache-autosize" parameter using ldapmodify command is failing.
- Resolves: Bug 1450893 - When nsslapd-cache-autosize is not set in dse.ldif, ldapsearch does not show the default value
- Resolves: Bug 1449098 - ns-slapd crashes in role cache creation
- Resolves: Bug 1441522 - AddressSanitizer: heap-use-after-free in libreplication-plugin.so
- Resolves: Bug 1437492 - "ERR - cos-plugin - cos_cache_query_attr - cos attribute krbPwdPolicyReference failed schema check" in error log
- Resolves: Bug 1429770 - ds-logpipe.py crashes for non-existing users
- Resolves: Bug 1451657 - -v option is not working for db2ldif.pl

* Fri May 5 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-13
- Bump version to 1.3.6.1-13
- Resolves: Bug 1444938 - Fix backport issue from build 1.3.6.1-10 (part 2)

* Fri May 5 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-12
- Bump version to 1.3.6.1-12
- Resolves: Bug 1444938 - Fix backport issue from build 1.3.6.1-10

* Fri May 5 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-11
- Bump version to 1.3.6.1-11
- Resolves: Bug 1410207 - Utility command had better use INFO log level for the output
- Resolves: Bug 1049190 - Better input argument validation and error messages for db2index and db2index.pl

* Fri May 5 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-10
- Bump version to 1.3.6.1-10
- Resolves: Bug 1444938 - nsslapd-allowed-sasl-mechanisms doesn't reset to default val 
- Resolves: Bug 1111400 - logconv.pl lists sasl binds with no dn as anonymous 
- Resolves: Bug 1377452 - Integer overflow in performance counters
- Resolves: Bug 1441790 - ldapserch for nsslapd-errorlog-level returns incorrect values
- Resolves: Bug 1444431 - ERR - symload_report_error - Netscape Portable Runtime error -5975
- Resolves: Bug 1447015 - Adjust db2bak.pl help and man page to reflect changes introduced to the script

* Wed Apr 19 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-9
- Bump version to 1.3.6.1-9
- Resolves: Bug 1442880 - setup-ds-admin.pl -u with nsslapd-localhost changed
- Resolves: Bug 1443682 - util_info_sys_pages should be able to detect memory restrictions in a cgroup

* Wed Apr 19 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-8
- Bump version to 1.3.6.1-8
- Resolves: Bug 1432016 - Possible deadlock while installing an ipa replica
- Resolves: Bug 1438029 - Overflow in memberof

* Tue Apr 11 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-7
- Bump version to 1.3.6.1-7
- Resolves: bug 1394899 - RHDS should ignore passwordMinAge if "password must reset" is set(fix crash regression)
- Resolves: bug 1381326 - dirsrv-snmp.service is provided by 389-ds-base instead of 389-ds-base-snmp
- Resolves: bug 1049190 - Better input argument validation and error messages for db2index and db2index.pl.

* Mon Apr 3 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-6
- Bump version to 1.3.6.1-6
- Resolves: bug 1437006 - EMBARGOED CVE-2017-2668 389-ds-base: Remote crash via crafted LDAP messages
- Resolves: bug 1341689 - dbmon.sh / cn=monitor] nsslapd-db-pages-in-use is increasing
- Resolves: bug 1394899 - RHDS should ignore passwordMinAge if "password must reset" is set
- Resolves: bug 1397288 - typo in logconv.pl man page
- Resolves: bug 1436994 - incorrect pathes in pkg-config files
- Resolves: bug 1396448 - Add a hard dependency for >=selinux-policy-3.13.1-75

* Tue Mar 28 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-5
- Bump version to 1.3.6.1-5
- Resolves: bug 1377452 - Integer overflow in counters and monitor
- Resolves: bug 1425907 - Harden password storage scheme
- Resolves: bug 1431207 - ns-slapd killed by SIGABRT 

* Mon Mar 27 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-4
- Bump version to 1.3.6.1-4
- Resolves: bug 1379424 - Reset-agmt-update-staus-and-total-init
- Resolves: bug 1394000 - dbmon.sh-fails-if-you-have-nsslapd-requi.patch
- Resolves: bug 1417344 - targetattr-wildcard-evaluation-is-incorr.patch
- Resolves: bug 1429770 - ds-logpipe.py-crashes-for-non-existing-u.patch
- Resolves: bug 1433697 - Fix-double-free-in-_cl5NewDBFile-error-path.patch
- Resolves: bug 1433996 - retrocl-can-crash-server-at-shutdown.patch
- Resolves: bug 1434967 - rpm-would-not-create-valid-pkgconfig-fi.patch
- Resolves: bug 1417338 - To-debug-DB_DEADLOCK-condition-allow-to.patch
- Resolves: bug 1433850 - Deleting-suffix-can-hang-server.patch

* Tue Mar 14 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-3
- Bump version to 1.3.6.1-3
- Fix spec file to include the tests

* Tue Mar 14 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-2
- Bump version to 1.3.6.1-2
- Resolves: bug 1431877 - 389-1.3.6.1-1.el7 covscan errors
- Resolves: bug 1432206 - content sync plugin can hang server shutdown
- Resolves: bug 1432149 - sasl external binds fail in 1.3.6.1

* Wed Mar 8 2017 Mark Reynolds <mreynolds@redhat.com> - 1.3.6.1-1
- Bump version to 1.3.6.1-1
- Resolves: bug 1388567 - Rebase 389-ds-base to 1.3.6 in RHEL-7.4

* Mon Oct 31 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.10-12
- Release 1.3.5.10-12
- Resolves: bug 1384785 - Replica install fails with old IPA master sometimes during replication process (DS 48992)
- Resolves: bug 1388501 - 389-ds-base is missing runtime dependency - bind-utils (DS 48328)
- Resolves: bug 1388581 - Replication stops working only when fips mode is set to true (DS 48909)
- Resolves: bug 1390342 - ns-accountstatus.pl shows wrong status for accounts inactivated by Account policy plugin (DS 49014)
- Resolves: bug 1390343 - trace args debug logging must be more restrictive (DS 49009)

* Tue Sep 13 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.10-11
- Release 1.3.5.10-11
- Resolves: bug 1321124 - Replication changelog can incorrectly skip over updates

* Thu Sep  1 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.10-10
- Release 1.3.5.10-10
- Resolves: bug 1370300 - set proper update status to replication agreement in case of failure (DS 48957)
- Resolves: bug 1209094 - Allow logging of rejected changes (DS 48969)

* Tue Aug 30 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.10-9
- Release 1.3.5.10-9
- Resolves: bug 1364190 - Change example in /etc/sysconfig/dirsrv to use tcmalloc (DS 48950)
- Resolves: bug 1366828 - audit on failure doesn't work if attribute nsslapd-auditlog-logging-enabled is NOT enabled (DS 48958)
- Resolves: bug 1368520 - Crash in import_wait_for_space_in_fifo() (DS 48960)
- Resolves: bug 1368956 - man page of ns-accountstatus.pl shows redundant entries for -p port option
- Resolves: bug 1369537 - passwordMinAge attribute doesn't limit the minimum age of the password (DS 48967)
- Resolves: bug 1369570 - cleanallruv changelog cleaning incorrectly impacts all backends (DS 48964)
- Resolves: bug 1369425 - ACI behaves erratically (DS 48972)
- Resolves: bug 1370300 - set proper update status to replication agreement in case of failure (DS 48957)
- Resolves: bug 1209094 - Allow logging of rejected changes (DS 48969)
- Resolves: bug 1371283 - Server Side Sorting crashes the server. (DS 48970)
- Resolves: bug 1371284 - Disabling CLEAR password storage scheme will crash server when setting a password (DS 48975)

* Thu Aug 18 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.10-8
- Release 1.3.5.10-8
- Resolves: bug 1321124 - Replication changelog can incorrectly skip over updates (DS 48954)
- Resolves: bug 1364190 - Change example in /etc/sysconfig/dirsrv to use tcmalloc (DS 48950)
- Resolves: bug 1366561 - ns-accountstatus.pl giving error even "No such object (32)" (DS 48956)

* Mon Aug  8 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.10-7
- Release 1.3.5.10-7
- Resolves: bug 1316580 - dirsrv service doesn't ask for pin when pin.txt is missing (DS 48450)
- Resolves: bug 1360976 - fixing a compiler warning

* Thu Aug  4 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.10-6
- Release 1.3.5.10-6
- Resolves: bug 1326077 - Page result search should return empty cookie if there is no returned entry (DS 48928)
- Resolves: bug 1360447 - nsslapd-workingdir is empty when ns-slapd is started by systemd (DS 48939)
- Resolves: bug 1360327 - remove-ds.pl deletes an instance even if wrong prefix was specified (DS 48934)
- Resolves: bug 1349815 - DS logs have warning:ancestorid not indexed for all CS subsystems (DS 48940)
- Resolves: bug 1329061 - 389-ds-base-1.3.4.0-29.el7_2 "hang" (DS 48882)
- Resolves: bug 1360976 - EMBARGOED CVE-2016-5405 389-ds-base: Password verification vulnerable to timing attack
- Resolves: bug 1361134 - When fine-grained policy is applied, a sub-tree has a priority over a user while changing password (DS 48943) 
- Resolves: bug 1361321 - Duplicate collation entries (DS 48936)
- Resolves: bug 1316580 - dirsrv service doesn't ask for pin when pin.txt is missing (DS 48450)
- Resolves: bug 1350799 - CVE-2016-4992 389-ds-base: Information disclosure via repeat

* Thu Jul 14 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.10-5
- Release 1.3.5.10-5
- Resolves: bug 1333184 - (389-ds-base-1.3.5) Fixing coverity issues. (DS 48919)

* Thu Jul 14 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.10-4
- Release 1.3.5.10-4
- Resolves: bug 1209128 - [RFE] Add a utility to get the status of Directory Server instances (DS 48144)
- Resolves: bug 1333184 - (389-ds-base-1.3.5) Fixing coverity issues. (DS 48919)
- Resolves: bug 1350799 - CVE-2016-4992 389-ds-base: Information disclosure via repeat
- Resolves: bug 1354660 - flow control in replication also blocks receiving results (DS 48767)
- Resolves: bug 1356261 - Fixup tombstone task needs to set proper flag when updating (DS 48924)
- Resolves: bug 1355760 - ns-slapd crashes during the deletion of backend (DS 48922)
- Resolves: bug 1353629 - DS shuts down automatically if dnaThreshold is set to 0 in a MMR setup (DS 48916)
- Resolves: bug 1355879 - nunc-stans: ns-slapd crashes during startup with SIGILL on AMD Opteron 280 (DS 48925)

* Mon Jul 11 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.10-3
- Release 1.3.5.10-3
- Resolves: bug 1354374 - Fixing the tarball version in the sources file.

* Mon Jul 11 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.10-2
- Release 1.3.5.10-2
- Resolves: bug 1353714 - If a cipher is disabled do not attempt to look it up (DS 48743)
- Resolves: bug 1353592 - Setup-ds.pl --update fails - regression (DS 48755)
- Resolves: bug 1353544 - db2bak.pl task enters infinitive loop when bak fs is almost full (DS 48914)
- Resolves: bug 1354374 - Upgrade to 389-ds-base >= 1.3.5.5 doesn't install 389-ds-base-snmp (DS 48918)

* Wed Jun 29 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.10-1
- Release 1.3.5.10-1
- Resolves: bug 1333184 - (389-ds-base-1.3.5) Fixing coverity issues. (DS 48905)

* Wed Jun 29 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.9-1
- Release 1.3.5.9-1
- Resolves: bug 1349571 - Improve MMR replication convergence (DS 48636)
- Resolves: bug 1304682 - "stale" automember rule (associated to a removed group) causes discrepancies in the database (DS 48637)
- Resolves: bug 1314956 - moving an entry cause next on-line init to skip entry has no parent, ending at line 0 of file "(bulk import)" (DS 48755)
- Resolves: bug 1316731 - syncrepl search returning error 329; plugin sending a bad error code (DS 48904)
- Resolves: bug 1346741 - ns-slapd crashes during the shutdown after adding attribute with a matching rule  (DS 48891)
- Resolves: bug 1349577 - Values of dbcachetries/dbcachehits in cn=monitor could overflow. (DS 48899)
- Resolves: bug 1272682 - nunc-stans: ns-slapd killed by SIGABRT (DS 48898)
- Resolves: bug 1346043 - repl-monitor displays colors incorrectly for the time lag > 60 min (DS 47538)
- Resolves: bug 1350632 - ns-slapd shutdown crashes if pwdstorageschema name is from stack. (DS 48902)

* Tue Jun 21 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.8-1
- Release 1.3.5.8-1
- Resolves: bug 1290101 - proxyauth support does not work when bound as directory  manager (DS 48366)

* Tue Jun 21 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.7-1
- Release 1.3.5.7-1
- Resolves: bug 1196282 - substring index with nssubstrbegin: 1 is not being used with filters like (attr=x*) (DS 48109)
- Resolves: bug 1303794 - Import readNSState.py from RichM's repo (DS 48449)
- Resolves: bug 1290101 - proxyauth support does not work when bound as directory  manager (DS 48366)
- Resolves: bug 1338872 - Wrong result code display in audit-failure log (DS 48892)
- Resolves: bug 1346043 - repl-monitor displays colors incorrectly for the time lag > 60 min (DS 47538)
- Resolves: bug 1346741 - ns-slapd crashes during the shutdown after adding attribute with a matching rule  (DS 48891)
- Resolves: bug 1347407 - By default aci can be read by anonymous (DS 48354)
- Resolves: bug 1347412 - cn=SNMP,cn=config entry can be read by anonymous (DS 48893)

* Tue Jun 14 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.6-1
- Release 1.3.5.6-1
- Resolves: bug 1273549 - [RFE] Improve timestamp resolution in logs (DS 47982)
- Resolves: bug 1321124 - Replication changelog can incorrectly skip over updates (DS 48766, DS 48636)
- Resolves: bug 1233926 - "matching rules" in ACI's "bind rules not fully evaluated (DS 48234)
- Resolves: bug 1346165 - 389-ds-base-1.3.5.5-1.el7.x86_64 requires policycoreutils-py 

* Mon Jun 13 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.5-1
- Release 1.3.5.5-1
- Resolves: bug 1018944 - [RFE] Enhance password change tracking (DS 48833)
- Resolves: bug 1344414 - [RFE] adding pre/post extop ability (DS 48880)
- Resolves: bug 1303794 - Import readNSState.py from RichM's repo (DS 48449)
- Resolves: bug 1257568 - /usr/lib64/dirsrv/libnunc-stans.so is owned by both -libs and -devel (DS 48404)
- Resolves: bug 1314956 - moving an entry cause next on-line init to skip entry has no parent, ending at line 0 of file "(bulk import)" (DS 48755)
- Resolves: bug 1342609 - At startup DES to AES password conversion causes timeout in start script (DS 48862)
- Resolves: bug 1316328 - search returns no entry when OR filter component contains non readable attribute (DS 48275)
- Resolves: bug 1280456 - setup-ds should detect if port is already defined (DS 48336)
- Resolves: bug 1312557 - dirsrv service fails to start when nsslapd-listenhost is configured (DS 48747)
- Resolves: bug 1326077 - Page result search should return empty cookie if there is no returned entry (DS 48752)
- Resolves: bug 1340307 - Running db2index with no options breaks replication (DS 48854)
- Resolves: bug 1337195 - Regression introduced in matching rules by DS 48746 (DS 48844)
- Resolves: bug 1335492 - Modifier's name is not recorded in the audit log with modrdn and moddn operations (DS 48834)
- Resolves: bug 1316741 - ldctl should support -H with ldap uris (DS 48754)

* Wed May 18 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.4-1
- release 1.3.5.4-1
- Resolves: bug 1334455 - db2ldif is not taking into account multiple suffixes or backends (DS 48828)
- Resolves: bug 1241563 - The "repl-monitor" web page does not display "year" in date. (DS 48220)
- Resolves: bug 1335618 - Server ram sanity checks work in isolation (DS 48617)
- Resolves: bug 1333184 - (389-ds-base-1.3.5) Fixing coverity issues. (DS 48837)

* Sat May  7 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.3-1
- release 1.3.5.3-1
- Resolves: bug 1209128 - [RFE] Add a utility to get the status of Directory Server instances (DS 48144)
- Resolves: bug 1332533 - ns-accountstatus.pl gives error message on execution along with results. (DS 48815)
- Resolves: bug 1332709 - password history is not updated when an admin resets the password (DS 48813)
- Resolves: bug 1333184 - (389-ds-base-1.3.5) Fixing coverity issues. (DS 48822)
- Resolves: bug 1333515 - Enable DS to offer weaker DH params in NSS  (DS 48798)

* Tue May  3 2016 Noriko Hosoi <nhosoi@redhat.com> - 1.3.5.2-1
- release 1.3.5.2-1
- Resolves: bug 1270020 - Rebase 389-ds-base to 1.3.5 in RHEL-7.3 
- Resolves: bug 1288229 - many attrlist_replace errors in connection with cleanallruv (DS 48283)
- Resolves: bug 1315893 - License tag does not match actual license of code (DS 48757)
- Resolves: bug 1320715 - DES to AES password conversion fails if a backend is empty (DS 48777)
- Resolves: bug 190862  - [RFE] Default password syntax settings don't work with fine-grained policies (DS 142)
- Resolves: bug 1018944 - [RFE] Enhance password change tracking (DS 548)
- Resolves: bug 1143066 - The dirsrv user/group should be created in rpm %pre, and ideally with fixed uid/gid (DS 48285)
- Resolves: bug 1153758 - [RFE] Support SASL/GSSAPI when ns-slapd is behind a load-balancer (DS 48332)
- Resolves: bug 1160902 - search, matching rules and filter error "unsupported type 0xA9" (DS 48016)
- Resolves: bug 1186512 - High memory fragmentation observed in ns-slapd; OOM-Killer invoked (DS 48377, 48129)
- Resolves: bug 1196282 - substring index with nssubstrbegin: 1 is not being used with filters like (attr=x*) (DS 48109)
- Resolves: bug 1209094 - [RFE] Allow logging of rejected changes (DS 48145, 48280)
- Resolves: bug 1209128 - [RFE] Add a utility to get the status of Directory Server instances (DS 48144)
- Resolves: bug 1210842 - [RFE] Add PIDFile option to systemd service file (DS 47951)
- Resolves: bug 1223510 - [RFE] it could be nice to have nsslapd-maxbersize default to bigger than 2Mb (DS 48326)
- Resolves: bug 1229799 - ldclt-bin killed by SIGSEGV (DS 48289)
- Resolves: bug 1249908 - No validation check for the value for nsslapd-db-locks. (DS 48244)
- Resolves: bug 1254887 - No man page entry for - option '-u' of dbgen.pl for adding group entries with uniquemembers (DS 48290)
- Resolves: bug 1255557 - db2index creates index entry from deleted records (DS 48252)
- Resolves: bug 1258610 - total update request must not be lost (DS 48255)
- Resolves: bug 1258611 - dna plugin needs to handle binddn groups for authorization (DS 48258)
- Resolves: bug 1259624 - [RFE] Provide a utility to detect accounts locked due to inactivity (DS 48269)
- Resolves: bug 1259950 - Add config setting to MemberOf Plugin to add required objectclass got memberOf attribute (DS 48267)
- Resolves: bug 1266510 - Linked Attributes plug-in - wrong behaviour when adding valid and broken links (DS 48295)
- Resolves: bug 1266532 - Linked Attributes plug-in - won't update links after MODRDN operation (DS 48294)
- Resolves: bug 1267750 - pagedresults - when timed out, search results could have been already freed. (DS 48299)
- Resolves: bug 1269378 - ds-logpipe.py with wrong arguments - python exception in the output (DS 48302)
- Resolves: bug 1271330 - nunc-stans: Attempt to release connection that is not acquired (DS 48311)
- Resolves: bug 1272677 - nunc stans: ns-slapd killed by SIGTERM
- Resolves: bug 1272682 - nunc-stans: ns-slapd killed by SIGABRT
- Resolves: bug 1273142 - crash in Managed Entry plugin (DS 48312)
- Resolves: bug 1273549 - [RFE] Improve timestamp resolution in logs (DS 47982)
- Resolves: bug 1273550 - Deadlock between two MODs on the same entry between entry cache and backend lock (DS 47978)
- Resolves: bug 1273555 - deadlock in mep delete post op (DS 47976)
- Resolves: bug 1273584 - lower password history minimum to 1 (DS 48394)
- Resolves: bug 1275763 - [RFE] add setup-ds.pl option to disable instance specific scripts (DS 47840)
- Resolves: bug 1276072 - [RFE] Allow RHDS to be setup using a DNS CNAME alias for General.FullMachineName (DS 48328)
- Resolves: bug 1278567 - SimplePagedResults -- abandon could happen between the abandon check and sending results (DS 48338)
- Resolves: bug 1278584 - Share nsslapd-threadnumber in the case nunc-stans is enabled, as well. (DS 48339)
- Resolves: bug 1278755 - deadlock on connection mutex (DS 48341)
- Resolves: bug 1278987 - Cannot upgrade a consumer to supplier in a multimaster environment (DS 48325)
- Resolves: bug 1280123 - acl - regression - trailing ', (comma)' in macro matched value is not removed. (DS 48344)
- Resolves: bug 1290111 - [RFE] Support for rfc3673 '+' to return operational attributes (DS 48363)
- Resolves: bug 1290141 - With exhausted range, part of DNA shared configuration is deleted after server restart (DS 48362)
- Resolves: bug 1290242 - SimplePagedResults -- in the search error case, simple paged results slot was not released. (DS 48375)
- Resolves: bug 1290600 - The 'eq' index does not get updated properly when deleting and re-adding attributes in the same ldapmodify operation (DS 48370)
- Resolves: bug 1295947 - 389-ds hanging after a few minutes of operation (DS 48406, revert 48338)
- Resolves: bug 1296310 - ldclt - segmentation fault error while binding (DS 48400)
- Resolves: bug 1299758 - CVE-2016-0741 389-ds-base: Worker threads do not detect abnormally closed connections causing DoS [rhel-7.3]
- Resolves: bug 1301097 - logconv.pl displays negative operation speeds (DS 48446)
- Resolves: bug 1302823 - Crash in slapi_get_object_extension (DS 48536)
- Resolves: bug 1303641 - heap corruption at schema replication. (DS 48492)
- Resolves: bug 1307151 - keep alive entries can break replication (DS 48445)
- Resolves: bug 1310848 - Supplier can skip a failing update, although it should retry. (DS 47788)
- Resolves: bug 1314557 - change severity of some messages related to "keep alive" enties (DS 48420)
- Resolves: bug 1316580 - dirsrv service doesn't ask for pin when pin.txt is missing (DS 48450)
- Resolves: bug 1316742 - no plugin calls in tombstone purging (DS 48759)
- Resolves: bug 1319329 - [RFE] add nsslapd-auditlog-logging-enabled: off to template-dse.ldif (DS 48145)
- Resolves: bug 1320295 - If nsSSL3 is on, even if SSL v3 is not really enabled, a confusing message is logged. (DS 48775)
- Resolves: bug 1326520 - db2index uses a buffer size derived from dbcachesize (DS 48383)
- Resolves: bug 1328936 - objectclass values could be dropped on the consumer (DS 48799)
- Resolves: bug 1287475 - [RFE] response control for password age should be sent by default by RHDS (DS 48369)
- Resolves: bug 1331343 - Paged results search returns the blank list of entries (DS 48808)

* Mon Oct  5 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-19
- release 1.3.4.0-19
- Resolves: bug 1228823 - async simple paged results issue (DS 48299, DS 48192)
- Resolves: bug 1266944 - ns-slapd crash during ipa-replica-manage del (DS 48298)

* Tue Sep 22 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-18
- release 1.3.4.0-18
- Resolves: bug 1259949 - Fractional replication evaluates several times the same CSN (DS 48266, DS 48284)

* Fri Sep 18 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-17
- release 1.3.4.0-17
- Resolves: bug 1259949 - A backport error (coverity -- unused variable 'init_retry')

* Fri Sep 18 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-16
- release 1.3.4.0-16
- Resolves: bug 1243970 - In MMR, double free coould occur under some special condition (DS 48276, DS 48226)
- Resolves: bug 1259949 - Fractional replication evaluates several times the same CSN (DS 48266)
- Resolves: bug 1241723 - cleanallruv - fix regression with server shutdown (DS 48217)
- Resolves: bug 1264224 - segfault in ns-slapd due to accessing Slapi_DN freed in pre bind plug-in (DS 48188)

* Fri Sep  4 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-15
- release 1.3.4.0-15
- Resolves: bug 1258996 - Complex filter in a search request doen't work as expected. (regression) (DS 48265)
- Resolves: bug 1179370 - COS cache doesn't properly mark vattr cache as invalid when there are multiple suffixes (DS 47981)

* Tue Aug 25 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-14
- release 1.3.4.0-14
- Resolves: bug 1246389 - wrong password check if passwordInHistory is decreased. (DS 48228)
- Resolves: bug 1255851 - Shell CLI fails with usage errors if an argument containing white spaces is given (DS 48254)
- Resolves: bug 1256938 - Unable to dereference unqiemember attribute because it is dn [#UID] not dn syntax (DS 47757)

* Wed Aug 19 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-13
- release 1.3.4.0-13
- Resolves: bug 1245519 - remove debug logging from retro cl (DS 47831)

* Tue Aug 18 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-12
- release 1.3.4.0-12
- Resolves: bug 1252133 - replica upgrade failed in starting dirsrv service (DS 48243)
- Resolves: bug 1254344 - Server crashes in ACL_LasFindFlush during shutdown if ACIs contain IP addresss restrictions (DS 48233)

* Fri Aug 14 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-11
- release 1.3.4.0-11
- Resolves: bug 1249784 - ipa-dnskeysyncd unhandled exception on named-pkcs11 start (DS 48249)
- Resolves: bug 1252082 - removing chaining database links trigger valgrind read error (DS 47686)
- Resolves: bug 1252207 - bashisms in 389-ds-base admin scripts (DS 47511)
- Resolves: bug 1252533 - Man pages and help for remove-ds.pl doesn't display "-a" option (DS 48245)
- Resolves: bug 1252781 - Slapd crashes reported from latest builds (DS 48250)

* Mon Aug 10 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-10
- release 1.3.4.0-10
- Resolves: bug 1245519 - Fix coverity issues (DS 47931)

* Fri Aug  7 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-9
- release 1.3.4.0-9
- Resolves: bug 1240876 - verify_db.pl doesn't verify DB specified by -a option. (DS 48215)
- Resolves: bug 1245235 - winsync lastlogon attribute not syncing between IPA & Windows 2008. (DS 48232)
- Resolves: bug 1245519 - Deadlock with retrochangelog, memberof plugin (DS 47931)
- Resolves: bug 1246389 - wrong password check if passwordInHistory is decreased. (DS 48228)
- Resolves: bug 1247811 - logconv autobind handling regression caused by 47446 (DS 48231)
- Resolves: bug 1250177 - Investigate betxn plugins to ensure they return the correct error code (DS 47810)

* Thu Jul 23 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-8
- release 1.3.4.0-8
- Resolves: bug 1160243 - [RFE] allow logconv.pl -S/-E switches to work even when exact/same timestamps are not present in access log file (DS 47910)
- Resolves: bug 1172037 - winsync range retrieval gets only 5000 values upon initialization (DS 48010)
- Resolves: bug 1242531 - logconv.pl should handle *.tar.xz, *.txz, *.xz log files (DS 48224)
- Resolves: bug 1243950 - When starting a replica agreement a deadlock can occur with an op updating nsuniqueid index (DS 48179)
- Resolves: bug 1243970 -  In MMR, double free coould occur under some special condition (DS 48226)
- Resolves: bug 1244926 - Crash while triming the retro changelog (DS 48206)

* Thu Jul 16 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-7
- release 1.3.4.0-7
- Resolves: bug 1235060 - Fix coverity issues - 07/14/2015 (DS 48203)
- Resolves: bug 1242531 - redux - logconv.pl should handle *.tar.xz, *.txz, *.xz log files (DS 48224)

* Tue Jul 14 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-6
- release 1.3.4.0-6
- Resolves: bug 1240845 - cleanallruv should completely clean changelog (DS 48208)
- Resolves: bug 1095603 - Any negative LDAP error code number reported as Illegal error by ldclt. (DS 47799)
- Resolves: bug 1168675 - Inconsistent behaviour of DS when LDAP Sync is used with an invalid cookie (DS 48013)
- Resolves: bug 1241723 - cleanAllRUV hangs shutdown if not all of the replicas are online (DS 48217)
- Resolves: bug 1241497 - crash in ns-slapd when deleting winSyncSubtreePair from sync agreement (DS 48216)
- Resolves: bug 1240404 - Silent install needs to properly exit when INF file is missing (DS 48119)
- Resolves: bug 1240406 - Remove warning suppression in 1.3.4 (DS 47878)
- Resolves: bug 1242683 - Winsync fails when AD users have multiple spaces (two)inside the value of the rdn attribute (DS 48223)
- Resolves: bug 1160243 - logconv.pl - validate start and end time args (DS 47910)
- Resolves: bug 1242531 - logconv.pl should handle *.tar.xz, *.txz, *.xz log files (DS 48224)
- Resolves: bug 1230996 - CI test: fixing test cases for ticket 48194 (DS 48194)

* Tue Jul  7 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-5
- release 1.3.4.0-5
- Resolves: bug 1235060 - Fix coverity issues (DS 48203)

* Tue Jul  7 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-4
- release 1.3.4.0-4
- Resolves: bug 1240404 - setup-ds.pl does not log invalid --file path errors the same (DS 48119)
- Resolves: bug 1240406 - setup -u stops after first failure (DS 47878)

* Mon Jul  6 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-3
- release 1.3.4.0-3
- Resolves: bug 1228823 - async simple paged results issue (DS 48192)
- Resolves: bug 1237325 - reindex off-line twice could provoke index corruption (DS 48212)
- Resolves: bug 1238790 - ldapsearch on nsslapd-maxbersize returns 0 instead of current value (DS 48214)

* Wed Jun 24 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-2
- release 1.3.4.0-2
- Resolves: bug 1235060 - Fix coverity issues 
- Resolves: bug 1235387 - Slow replication when deleting large quantities of multi-valued attributes (DS 48195)

* Fri Jun 19 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.4.0-1
- Release 1.3.4.0-1 (rebase)
- Enable nunc-stans for x86_64.
- Resolves: bug 1034325 - Linked attributes betxnpreoperation - transaction not aborted when linked entry does not exit (DS 47640)
- Resolves: bug 1052755 - Retro Changelog Plugin accepts invalid value in nsslapd-changelogmaxage attribute (DS 47669)
- Resolves: bug 1096409 - RHDS keeps on logging write_changelog_and_ruv: failed to update RUV for unknown (DS 47801)
- Resolves: bug 1145378 - Adding an entry with an invalid password as rootDN is incorrectly rejected (DS 47900)
- Resolves: bug 1145382 - Bad manipulation of passwordhistory (DS 47905)
- Resolves: bug 1154147 - Uniqueness plugin: should allow to exclude some subtrees from its scope (DS 47927)
- Resolves: bug 1171358 - Make ReplicaWaitForAsyncResults configurable (DS 47957)
- Resolves: bug 1171663 - MODDN fails when entry doesn't have memberOf attribute and new DN is in the scope of memberOfExcludeSubtree (DS 47526)
- Resolves: bug 1174457 - [RFE] memberOf - add option to skip nested group lookups during delete operations (DS 47963)
- Resolves: bug 1178640 - db2bak.pl man page should be improved. (DS 48008)
- Resolves: bug 1179370 - COS cache doesn't properly mark vattr cache as invalid when there are multiple suffixes (DS 47981)
- Resolves: bug 1180331 - Local Password Policies for Nested OU's not honoured (DS 47980)
- Resolves: bug 1180776 - nsslapd-db-locks modify not taking into account (DS 47934)
- Resolves: bug 1181341 - nsslapd-changelogtrim-interval and nsslapd-changelogcompactdb-interval are not validated (DS 47617)
- Resolves: bug 1185882 - ns-activate.pl fails to activate account if it was disabled on AD (DS 48001)
- Resolves: bug 1186548 - ns-slapd crash in shutdown phase (DS 48005)
- Resolves: bug 1189154 - DNS errors after IPA upgrade due to broken ReplSync (DS 48030)
- Resolves: bug 1206309 - winsync sets AccountUserControl in AD to 544 (DS 47723)
- Resolves: bug 1210845 - slapd crashes during Dogtag clone reinstallation (DS 47966)
- Resolves: bug 1210850 - add an option '-u' to dbgen.pl for adding group entries with (DS 48025)
- Resolves: bug 1210852 - aci with wildcard and macro not correctly evaluated (DS 48141)

* Fri Jun 12 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-19
- release 1.3.3.1-19
- Resolves: bug 1230996 - nsSSL3Ciphers preference not enforced server side (DS 48194)

* Fri Jun  5 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-18
- release 1.3.3.1-18
- Resolves: bug 1228823 - async simple paged results issue (DS 48146, DS 48192)

* Tue Jun  2 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-17
- release 1.3.3.1-17
- Resolves: bug 1226510 - idm/ipa 389-ds-base entry cache converges to 500 KB in dblayer_is_cachesize_sane (DS 48190)

* Tue Apr 21 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-16
- release 1.3.3.1-16
- Resolves: bug 1212894 - CVE-2015-1854 389ds-base: access control bypass with modrdn

* Mon Feb 23 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-15
- release 1.3.3.1-15
- Setting correct build tag 'rhel-7.1-z-candidate'

* Mon Feb 23 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-14
- release 1.3.3.1-14
- Resolves: bug 1189154 - DNS errors after IPA upgrade due to broken ReplSync (DS 48030)
            Fixes spec file to make sure all the server instances are stopped before upgrade
- Resolves: bug 1186548 - ns-slapd crash in shutdown phase (DS 48005)

* Sun Jan 25 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-13
- release 1.3.3.1-13
- Resolves: bug 1183655 - Fixed Covscan FORWARD_NULL defects (DS 47988)

* Sun Jan 25 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-12
- release 1.3.3.1-12
- Resolves: bug 1182477 - Windows Sync accidentally cleared raw_entry (DS 47989)
- Resolves: bug 1180325 - upgrade script fails if /etc and /var are on different file systems (DS 47991 )
- Resolves: bug 1183655 - Schema learning mechanism, in replication, unable to extend an existing definition (DS 47988)

* Mon Jan  5 2015 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-11
- release 1.3.3.1-11
- Resolves: bug 1080186 - During delete operation do not refresh cache entry if it is a tombstone (DS 47750)

* Wed Dec 17 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-10
- release 1.3.3.1-10
- Resolves: bug 1172731 - CVE-2014-8112 password hashing bypassed when "nsslapd-unhashed-pw-switch" is set to off 
- Resolves: bug 1166265 - DS hangs during online total update (DS 47942)
- Resolves: bug 1168151 - CVE-2014-8105 information disclosure through 'cn=changelog' subtree
- Resolves: bug 1044170 - Allow memberOf suffixes to be configurable (DS 47526)
- Resolves: bug 1171356 - Bind DN tracking unable to write to internalModifiersName without special permissions (DS 47950)
- Resolves: bug 1153737 - logconv.pl -- support parsing/showing/reporting different protocol versions (DS 47949)
- Resolves: bug 1171355 - start dirsrv after chrony on RHEL7 and Fedora (DS 47947)
- Resolves: bug 1170707 - cos_cache_build_definition_list does not stop during server shutdown (DS 47967)
- Resolves: bug 1170708 - COS memory leak when rebuilding the cache (DS - Ticket 47969)
- Resolves: bug 1170709 - Account lockout attributes incorrectly updated after failed SASL Bind (DS 47970)
- Resolves: bug 1166260 - cookie_change_info returns random negative number if there was no change in a tree (DS 47960)
- Resolves: bug 1012991 - Error log levels not displayed correctly (DS 47636)
- Resolves: bug 1108881 - rsearch filter error on any search filter (DS 47722)
- Resolves: bug 994690  - Allow dynamically adding/enabling/disabling/removing plugins without requiring a server restart (DS 47451)
- Resolves: bug 1162997 - Running a plugin task can crash the server (DS 47451)
- Resolves: bug 1166252 - RHEL7.1 ns-slapd segfault when ipa-replica-install restarts (DS 47451)
- Resolves: bug 1172597 - Crash if setting invalid plugin config area for MemberOf Plugin (DS 47525)
- Resolves: bug 1139882 - coverity defects found in 1.3.3.x (DS 47965)
		    
* Thu Nov 13 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-9
- release 1.3.3.1-9
- Resolves: bug 1153737 - Disable SSL v3, by default. (DS 47928)
- Resolves: bug 1163461 - Should not check aci syntax when deleting an aci (DS 47953)

* Mon Nov 10 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-8
- release 1.3.3.1-8
- Resolves: bug 1156607 - Crash in entry_add_present_values_wsi_multi_valued (DS 47937)
- Resolves: bug 1153737 - Disable SSL v3, by default (DS 47928, DS 47945, DS 47948)
- Resolves: bug 1158804 - Malformed cookie for LDAP Sync makes DS crash (DS 47939)

* Thu Oct 23 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-7
- release 1.3.3.1-7
- Resolves: bug 1153737 - Disable SSL v3, by default (DS 47928)

* Fri Oct 10 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-6
- release 1.3.3.1-6
- Resolves: bug 1151287 - dynamically added macro aci is not evaluated on the fly (DS 47922)
- Resolves: bug 1080186 - Need to move slapi_pblock_set(pb, SLAPI_MODRDN_EXISTING_ENTRY, original_entry->ep_entry) prior to original_entry overwritten (DS 47897)
- Resolves: bug 1150694 - Encoding of SearchResultEntry is missing tag (DS 47920)
- Resolves: bug 1150695 - ldbm_back_modify SLAPI_PLUGIN_BE_PRE_MODIFY_FN does not return even if one of the preop plugins fails. (DS 47919)
- Resolves: bug 1139882 - Fix remaining compiler warnings (DS 47892)
- Resolves: bug 1150206 - result of dna_dn_is_shared_config is incorrectly used (DS 47918)

* Wed Oct  1 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-5
- release 1.3.3.1-5
- Resolves: bug 1139882 - coverity defects found in 1.3.3.x (DS 47892)

* Wed Oct  1 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-4
- release 1.3.3.1-4
- Resolves: bug 1080186 - Creating a glue fails if one above level is a conflict or missing  (DS 47750)
- Resolves: bug 1145846 - 389-ds 1.3.3.0 does not adjust cipher suite configuration on upgrade, breaks itself and pki-server (DS 47908)
- Resolves: bug 1117979 - harden the list of ciphers available by default (phase 2) (DS 47838)
                        - provide enabled ciphers as search result (DS 47880)

* Fri Sep 12 2014 Rich Megginson <nhosoi@redhat.com> - 1.3.3.1-3
- release 1.3.3.1-3
- Resolves: bug 1139882 - coverity defects found in 1.3.3.1

* Thu Sep 11 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-2
- release 1.3.3.1-2
- Resolves: bug 1079099 - Simultaneous adding a user and binding as the user could fail in the password policy check (DS 47748)
- Resolves: bug 1080186 - Creating a glue fails if one above level is a conflict or missing (DS 47834)
- Resolves: bug 1139882 - coverity defects found in 1.3.3.1 (DS 47890)
- Resolves: bug 1112702 - Broken dereference control with the FreeIPA 4.0 ACIs (DS 47885 - deref plugin should not return references with noc access rights)
- Resolves: bug 1117979 - harden the list of ciphers available by default (DS 47838, DS 47895)
- Resolves: bug 1080186 - Creating a glue fails if one above level is a conflict or missing (DS 47889 - DS crashed during ipa-server-install on test_ava_filter)

* Fri Sep  5 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.3.1-1
- release 1.3.3.1-1
- Resolves: bug 746646 - RFE: easy way to configure which users and groups to sync with winsync
- Resolves: bug 881372 - nsDS5BeginReplicaRefresh attribute accepts any value and it doesn't throw any error when server restarts.
- Resolves: bug 920597 - Possible to add invalid ACI value
- Resolves: bug 921162 - Possible to add nonexistent target to ACI
- Resolves: bug 923799 - if nsslapd-cachememsize set to the number larger than the RAM available, should result in proper error message.
- Resolves: bug 924937 - Attribute "dsOnlyMemberUid" not allowed when syncing nested posix groups from AD with posixWinsync
- Resolves: bug 951754 - Self entry access ACI not working properly
- Resolves: bug 952517 - Dirsrv instance failed to start with Segmentation fault (core dump) after modifying 7-bit check plugin
- Resolves: bug 952682 - nsslapd-db-transaction-batch-val turns to -1
- Resolves: bug 966443 - Plugin library path validation
- Resolves: bug 975176 - Non-directory manager can change the individual userPassword's storage scheme
- Resolves: bug 979465 - IPA replica's - "SASL encrypted packet length exceeds maximum allowed limit"
- Resolves: bug 982597 - Some attributes in cn=config should not be multivalued
- Resolves: bug 987009 - 389-ds-base - shebang with /usr/bin/env
- Resolves: bug 994690 - RFE: Allow dynamically adding/enabling/disabling/removing plugins without requiring a server restart
- Resolves: bug 1012991 - errorlog-level 16384 is listed as 0 in cn=config
- Resolves: bug 1013736 - Enabling/Disabling DNA plug-in throws "ldap_modify: Server Unwilling to Perform (53)" error
- Resolves: bug 1014380 - setup-ds.pl doesn't lookup the "root" group correctly
- Resolves: bug 1020459 - rsa_null_sha should not be enabled by default
- Resolves: bug 1024541 - start dirsrv after ntpd
- Resolves: bug 1029959 - Managed Entries betxnpreoperation - transaction not aborted upon failure to create managed entry
- Resolves: bug 1031216 - add dbmon.sh
- Resolves: bug 1044133 - Indexed search with filter containing '&' and "!" with attribute subtypes gives wrong result
- Resolves: bug 1044134 - should set LDAP_OPT_X_SASL_NOCANON to LDAP_OPT_ON by default
- Resolves: bug 1044135 - make connection buffer size adjustable
- Resolves: bug 1044137 - posix winsync should support ADD user/group entries from DS to AD
- Resolves: bug 1044138 - mep_pre_op: Unable to fetch origin entry
- Resolves: bug 1044139 - [RFE] Support RFC 4527 Read Entry Controls
- Resolves: bug 1044140 - Allow search to look up 'in memory RUV'
- Resolves: bug 1044141 - MMR stress test with dna enabled causes a deadlock
- Resolves: bug 1044142 - winsync doesn't sync DN valued attributes if DS DN value doesn't exist
- Resolves: bug 1044143 - modrdn + NSMMReplicationPlugin - Consumer failed to replay change
- Resolves: bug 1044144 - resurrected entry is not correctly indexed
- Resolves: bug 1044146 - Add a warning message when a connection hits the max number of threads
- Resolves: bug 1044147 - 7-bit check plugin does not work for userpassword attribute
- Resolves: bug 1044148 - The backend name provided to bak2db is not validated
- Resolves: bug 1044149 - Winsync should support range retrieval
- Resolves: bug 1044150 - 7-bit checking is not necessary for userPassword
- Resolves: bug 1044151 - With SeLinux, ports can be labelled per range. setup-ds.pl or setup-ds-admin.pl fail to detect already ranged labelled ports
- Resolves: bug 1044152 - ChainOnUpdate: "cn=directory manager" can modify userRoot on consumer without changes being chained or replicated. Directory integrity compromised.
- Resolves: bug 1044153 - mods optimizer
- Resolves: bug 1044154 - multi master replication allows schema violation
- Resolves: bug 1044156 - DS crashes with some 7-bit check plugin configurations
- Resolves: bug 1044157 - Some updates of "passwordgraceusertime" are useless when updating "userpassword"
- Resolves: bug 1044159 - [RFE] Support 'Content Synchronization Operation' (SyncRepl) - RFC 4533
- Resolves: bug 1044160 - remove-ds.pl should remove /var/lock/dirsrv
- Resolves: bug 1044162 - enhance retro changelog
- Resolves: bug 1044163 - updates to ruv entry are written to retro changelog
- Resolves: bug 1044164 - Password administrators should be able to violate password policy
- Resolves: bug 1044168 - Schema replication between DS versions may overwrite newer base schema
- Resolves: bug 1044169 - ACIs do not allow attribute subtypes in targetattr keyword
- Resolves: bug 1044170 - Allow memberOf suffixes to be configurable
- Resolves: bug 1044171 - Allow referential integrity suffixes to be configurable
- Resolves: bug 1044172 - Plugin library path validation prevents intentional loading of out-of-tree modules
- Resolves: bug 1044173 - make referential integrity configuration more flexible
- Resolves: bug 1044177 - allow configuring changelog trim interval
- Resolves: bug 1044179 - objectclass may, must lists skip rest of objectclass once first is found in sup
- Resolves: bug 1044180 - memberOf on a user is converted to lowercase
- Resolves: bug 1044181 - report unindexed internal searches
- Resolves: bug 1044183 - With 1.3.04 and subtree-renaming OFF, when a user is deleted after restarting the server, the same entry can't be added
- Resolves: bug 1044185 - dbscan on entryrdn should show all matching values
- Resolves: bug 1044187 - logconv.pl - RFE - add on option for a minimum etime for unindexed search stats
- Resolves: bug 1044188 - Recognize compressed log files
- Resolves: bug 1044191 - support TLSv1.1 and TLSv1.2, if supported by NSS
- Resolves: bug 1044193 - default nsslapd-sasl-max-buffer-size should be 2MB
- Resolves: bug 1044194 - Complex filter in a search request doen't work as expected.
- Resolves: bug 1044196 - Automember plug-in should treat MODRDN operations as ADD operations
- Resolves: bug 1044198 - Replication of the schema may overwrite consumer 'attributetypes' even if consumer definition is a superset
- Resolves: bug 1044202 - db2bak.pl issue when specifying non-default directory
- Resolves: bug 1044203 - Allow referint plugin to use an alternate config area
- Resolves: bug 1044205 - Allow memberOf to use an alternate config area
- Resolves: bug 1044210 - idl switch does not work
- Resolves: bug 1044211 - make old-idl tunable
- Resolves: bug 1044212 - IDL-style can become mismatched during partial restoration
- Resolves: bug 1044213 - backend performance - introduce optimization levels
- Resolves: bug 1044215 - using transaction batchval violates durability
- Resolves: bug 1044216 - examine replication code to reduce amount of stored state information
- Resolves: bug 1048980 - 7-bit check plugin not checking MODRDN operation
- Resolves: bug 1049030 - Windows Sync group issues
- Resolves: bug 1052751 - Page control does not work if effective rights control is specified
- Resolves: bug 1052754 - Allow nsDS5ReplicaBindDN to be a group DN
- Resolves: bug 1057803 - logconv errors when search has invalid bind dn
- Resolves: bug 1060032 - [RFE] Update lastLoginTime also in Account Policy plugin if account lockout is based on passwordExpirationTime.
- Resolves: bug 1061060 - betxn: retro changelog broken after cancelled transaction
- Resolves: bug 1061572 - improve dbgen rdn generation, output and man page.
- Resolves: bug 1063990 - single valued attribute replicated ADD does not work
- Resolves: bug 1064006 - Size returned by slapi_entry_size is not accurate
- Resolves: bug 1064986 - Replication retry time attributes cannot be added
- Resolves: bug 1067090 - Missing warning for invalid replica backoff configuration
- Resolves: bug 1072032 - Updating nsds5ReplicaHost attribute in a replication agreement fails with error 53
- Resolves: bug 1074306 - Under heavy stress, failure of turning a tombstone into glue makes the server hung
- Resolves: bug 1074447 - Part of DNA shared configuration is deleted after server restart
- Resolves: bug 1076729 - Continuous add/delete of an entry in MMR setup causes entryrdn-index conflict
- Resolves: bug 1077884 - ldap/servers/slapd/back-ldbm/dblayer.c: possible minor problem with sscanf
- Resolves: bug 1077897 - Memory leak with proxy auth control
- Resolves: bug 1079099 - Simultaneous adding a user and binding as the user could fail in the password policy check
- Resolves: bug 1080186 - Creating a glue fails if one above level is a conflict or missing
- Resolves: bug 1082967 - attribute uniqueness plugin fails when set as a chaining component
- Resolves: bug 1085011 - Directory Server crash reported from reliab15 execution
- Resolves: bug 1086890 - empty modify returns LDAP_INVALID_DN_SYNTAX
- Resolves: bug 1086902 - mem leak in do_bind when there is an error
- Resolves: bug 1086904 - mem leak in do_search - rawbase not freed upon certain errors
- Resolves: bug 1086908 - Performing deletes during tombstone purging results in operation errors
- Resolves: bug 1090178 - #481 breaks possibility to reassemble memberuid list
- Resolves: bug 1092099 - A replicated MOD fails (Unwilling to perform) if it targets a tombstone
- Resolves: bug 1092342 - nsslapd-ndn-cache-max-size accepts any invalid value.
- Resolves: bug 1092648 - Negative value of nsSaslMapPriority is not reset to lowest priority
- Resolves: bug 1097004 - Problem with deletion while replicated
- Resolves: bug 1098654 - db2bak.pl error with changelogdb
- Resolves: bug 1099654 - Normalization from old DN format to New DN format doesnt handel condition properly when there is space in a suffix after the seperator operator.
- Resolves: bug 1108405 - find a way to remove replication plugin errors messages "changelog iteration code returned a dummy entry with csn %s, skipping ..."
- Resolves: bug 1108407 - managed entry plugin fails to update managed entry pointer on modrdn operation
- Resolves: bug 1108865 - memory leak in ldapsearch filter objectclass=*
- Resolves: bug 1108870 - ACI warnings in error log
- Resolves: bug 1108872 - Logconv.pl with an empty access log gives lots of errors
- Resolves: bug 1108874 - logconv.pl memory continually grows
- Resolves: bug 1108881 - rsearch filter error on any search filter
- Resolves: bug 1108895 - [RFE - RHDS9] CLI report to monitor replication
- Resolves: bug 1108902 - rhds91 389-ds-base-1.2.11.15-31.el6_5.x86_64 crash in db4 __dbc_get_pp env = 0x0 ?
- Resolves: bug 1108909 - single valued attribute replicated ADD does not work
- Resolves: bug 1109334 - 389 Server crashes if uniqueMember is invalid syntax and memberOf plugin is enabled.
- Resolves: bug 1109336 - Parent numsubordinate count can be incorrectly updated if an error occurs
- Resolves: bug 1109339 - Nested tombstones become orphaned after purge
- Resolves: bug 1109354 - Tombstone purging can crash the server if the backend is stopped/disabled
- Resolves: bug 1109357 - Coverity issue in 1.3.3
- Resolves: bug 1109364 - valgrind - value mem leaks, uninit mem usage
- Resolves: bug 1109375 - provide default syntax plugin
- Resolves: bug 1109378 - Environment variables are not passed when DS is started via service
- Resolves: bug 1111364 - Updating winsync one-way sync does not affect the behaviour dynamically
- Resolves: bug 1112824 - Broken dereference control with the FreeIPA 4.0 ACIs
- Resolves: bug 1113605 - server restart wipes out index config if there is a default index
- Resolves: bug 1115177 - attrcrypt_generate_key calls slapd_pk11_TokenKeyGenWithFlags with improper macro
- Resolves: bug 1117021 - Server deadlock if online import started while server is under load
- Resolves: bug 1117975 - paged results control is not working in some cases when we have a subsuffix.
- Resolves: bug 1117979 - harden the list of ciphers available by default
- Resolves: bug 1117981 - Fix various typos in manpages & code
- Resolves: bug 1117982 - Fix hyphens used as minus signed and other manpage mistakes
- Resolves: bug 1118002 - server crashes deleting a replication agreement
- Resolves: bug 1118006 - RFE - forcing passwordmustchange attribute by non-cn=directory manager
- Resolves: bug 1118007 - [RFE] Make it possible for privileges to be provided to an admin user to import an LDIF file containing hashed passwords
- Resolves: bug 1118014 - Enhance ACIs to have more control over MODRDN operations
- Resolves: bug 1118021 - Return all attributes in rootdse without explicit request
- Resolves: bug 1118025 - Slow ldapmodify operation time for large quantities of multi-valued attribute values
- Resolves: bug 1118032 - Schema Replication Issue
- Resolves: bug 1118034 - 389 DS Server crashes and dies while handles paged searches from clients
- Resolves: bug 1118043 - Failed deletion of aci: no such attribute
- Resolves: bug 1118048 - If be_txn plugin fails in ldbm_back_add, adding entry is double freed.
- Resolves: bug 1118051 - Add switch to disable pre-hashed password checking
- Resolves: bug 1118054 - Make ldbm_back_seq independently support transactions
- Resolves: bug 1118055 - Add operations rejected by betxn plugins remain in cache
- Resolves: bug 1118057 - online import crashes server if using verbose error logging
- Resolves: bug 1118059 - add fixup-memberuid.pl script
- Resolves: bug 1118060 - winsync plugin modify is broken
- Resolves: bug 1118066 - memberof scope: allow to exclude subtrees
- Resolves: bug 1118069 - 389-ds production segfault: __memcpy_sse2_unaligned () at ../sysdeps/x86_64/multiarch/memcpy-sse2-unaligned.S:144
- Resolves: bug 1118074_DELETE_FN - plugin returned error" messages
- Resolves: bug 1118076 - ds logs many "Operation error fetching Null DN" messages
- Resolves: bug 1118077 - Improve import logging and abort handling
- Resolves: bug 1118079 - Multi master replication initialization incomplete after restore of one master
- Resolves: bug 1118080 - Don't add unhashed password mod if we don't have an unhashed value
- Resolves: bug 1118081 - Investigate betxn plugins to ensure they return the correct error code
- Resolves: bug 1118082 - The error result text message should be obtained just prior to sending result
- Resolves: bug 1123865 - CVE-2014-3562 389-ds-base: 389-ds: unauthenticated information disclosure [rhel-7.1] 

* Fri May  2 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-26
- release 1.3.1.6-26
- Resolves: bug 1085011 - Directory Server crash reported from reliab15 execution (Ticket 346)

* Mon Mar 31 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-25
- release 1.3.1.6-25
- Resolves: bug 1082740 - ns-slapd crash in reliability 15

* Thu Mar 13 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-24
- release 1.3.1.6-24
- Resolves: bug 1074084 - e_uniqueid fails to set if an entry is a conflict entry (Ticket 47735); regression - sub-type length in attribute type was mistakenly subtracted.

* Tue Mar 11 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-23
- Resolves: bug 1074850 - EMBARGOED CVE-2014-0132 389-ds-base: 389-ds: flaw in parsing authzid can lead to privilege escalation [rhel-7.0] (Ticket 47739 - directory server is insecurely misinterpreting authzid on a SASL/GSSAPI bind) (Added 0095-Ticket-47739-directory-server-is-insecurely-misinter.patch)

  Tue Mar 11 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-23
- release 1.3.1.6-22
- Resolves: bug 1074850 - EMBARGOED CVE-2014-0132 389-ds-base: 389-ds: flaw in parsing authzid can lead to privilege escalation [rhel-7.0] (Ticket 47739 - directory server is insecurely misinterpreting authzid on a SASL/GSSAPI bind)

* Mon Mar 10 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-22
- release 1.3.1.6-22
- Resolves: bug 1074084 - e_uniqueid fails to set if an entry is a conflict entry (Ticket 47735)

* Tue Feb 25 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-21
- release 1.3.1.6-21
- Resolves: bug 918694 - Fix covscan defect FORWARD_NULL (Ticket 408)
- Resolves: bug 918717 - Fix covscan defect COMPILER WARNINGS (Ticket 571)

* Tue Feb 25 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-20
- release 1.3.1.6-20
- Resolves: bug 1065242 - 389-ds-base, conflict occurs at yum installation if multilib_policy=all. (Ticket 47709)

* Tue Feb 18 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-19
- release 1.3.1.6-19
- Resolves: bug 1065971 - Enrolling a host into IdM/IPA always takes two attempts (Ticket 47704)

* Mon Feb  3 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-18
- release 1.3.1.6-18
- Resolves: bug 838656 - logconv.pl tool removes the access logs contents if "-M" is not correctly used (Ticket 471)
- Resolves: bug 922538 - improve dbgen rdn generation, output (Ticket 47374)
- Resolves: bug 970750 - flush.pl is not included in perl5 (Ticket 47374)
- Resolves: bug 1013898 - Fix various issues with logconv.pl (Ticket 471)

* Wed Jan 29 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-17
- release 1.3.1.6-17
- Resolves: bug 853106 - Deleting attribute present in nsslapd-allowed-to-delete-attrs returns Operations error (Ticket 443)
- Resolves: bug 1049525 - Server hangs in cos_cache when adding a user entry (Ticket 47649)
    
* Wed Jan 29 2014 Daniel Mach <dmach@redhat.com> - 1.3.1.6-16
- Mass rebuild 2014-01-24

* Tue Jan 21 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-15
- release 1.3.1.6-15
- Resolves: bug 918702 -  better error message when cache overflows (Ticket 342)
- Resolves: bug 1009679 - replication stops with excessive clock skew (Ticket 47516)
- Resolves: bug 1042855 - Unable to delete protocol timeout attribute (Ticket 47620)
- Resolves: bug 918694 - Fix crash when disabling/enabling the setting (Ticket 408)
- Resolves: bug 853355 - config_set_allowed_to_delete_attrs: Valgrind reports Invalid read (Ticket 47660)

* Wed Jan  8 2014 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-14
- release 1.3.1.6-14
- Resolves: bug 853355 - Possible to add invalid attribute to nsslapd-allowed-to-delete-attrs (Ticket 447) 
- Resolves: bug 1034739 - Impossible to configure nsslapd-allowed-sasl-mechanisms (Ticket 47613)
- Resolves: bug 1038639 - 389-ds rejects nsds5ReplicaProtocolTimeout attribut; Fix logically dead code; Fix dereferenced NULL pointer in agmtlist_modify_callback(); Fix missing left brackete (Ticket 47620)
- Resolves: bug 1042855 - nsds5ReplicaProtocolTimeout attribute is not validated when added to replication agreement; Config value validation improvement (Ticket 47620)
- Resolves: bug 918717 - server does not accept 0 length LDAP Control sequence (Ticket 571)
- Resolves: bug 1034902 - replica init/bulk import errors should be more verbose (Ticket 47606)
- Resolves: bug 1044219 - fix memleak caused by 47347 (Ticket 47623)
- Resolves: bug 1049522 - Crash after replica is installed; Fix cherry-pick error for 1.3.2 and 1.3.1 (Ticket 47620)
- Resolves: bug 1049568 - changelog iteration should ignore cleaned rids when getting the minCSN (Ticket 47627) 

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.3.1.6-13
- Mass rebuild 2013-12-27

* Tue Dec 10 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-12
- release 1.3.1.6-12
- Resolves: bug 1038639 - 389-ds rejects nsds5ReplicaProtocolTimeout attribute (Ticket 47620)
- Resolves: bug 1034898 - automember plugin task memory leaks (Ticket 47592)
- Resolves: bug 1034451 - Possible to specify invalid SASL mechanism in nsslapd-allowed-sasl-mechanisms (Ticket 47614)
- Resolves: bug 1032318 - entries with empty objectclass attribute value can be hidden (Ticket 47591)
- Resolves: bug 1032316 - attrcrypt fails to find unlocked key (Ticket 47596)
- Resolves: bug 1031227 - Reduce lock scope in retro changelog plug-in (Ticket 47599)
- Resolves: bug 1031226 - Convert ldbm_back_seq code to be transaction aware (Ticket 47598)
- Resolves: bug 1031225 - Convert retro changelog plug-in to betxn (Ticket 47597)
- Resolves: bug 1031223 - hard coded limit of 64 masters in agreement and changelog code (Ticket 47587)
- Resolves: bug 1034739 - Impossible to configure nsslapd-allowed-sasl-mechanisms (Ticket 47613)
- Resolves: bug 1035824 - Automember betxnpreoperation - transaction not aborted when group entry does not exist (Ticket 47622)

* Thu Nov 21 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.6-11
- Resolves: bug 1024979 - CVE-2013-4485 389-ds-base: DoS due to improper handling of ger attr searches

* Tue Nov 12 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.6-10
- release 1.3.1.6-10
- Resolves: bug 1018893 DS91: ns-slapd stuck in DS_Sleep
-     had to revert earlier change - does not work and breaks ipa

* Tue Nov 12 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-9
- release 1.3.1.6-9
- Resolves: bug 1028440 - Winsync replica initialization and incremental updates from DS to AD fails on RHEL
- Resolves: bug 1027502 - Replication Failures related to skipped entries due to cleaned rids
- Resolves: bug 1027047 - Winsync plugin segfault during incremental backoff

* Wed Nov  6 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-8
- release 1.3.1.6-8
- Resolves: bug 971111 - DNA plugin failed to fetch replication agreement 
- Resolves: bug 1026931 - 1.2.11.29 crash when removing entries from cache

* Mon Oct 21 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.6-7
- Resolves: bug 1018893 DS91: ns-slapd stuck in DS_Sleep
- Resolves: bug 1018914 fixup memberof task does not work: task entry not added 

* Fri Oct 11 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.6-6
- Resolves: bug 1013900 - logconv: some stats do not work across server restarts
-  previous patch introduced regressions
-  fixed by c2eced0 ticket #47550 and e2a880b Ticket #47550 and 8b10f83 Ticket #47551
- Resolves: bug 1008610 - tmpfiles.d references /var/lock when they should reference /run/lock
-  previous patch not complete, fixed by a11be5c Ticket 47513
- Resolves: bug 1016749 - DS crashes when "cn=Directory Manager" is changing it's password
-  cherry picked upstream f786600 Ticket 47329 and b67e230 Coverity Fixes
- Resolves: bug 1015252 locale "nl" not supported by collation plugin
- Resolves: bug 1016317 Need to update supported locales
- Resolves: bug 1016722 memory leak in range searches

* Tue Oct  1 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.6-5
- Resolves: bug 1013896 - logconv.pl - Use of comma-less variable list is deprecated
- Resolves: bug 1008256 - backend txn plugin fixup tasks should be done in a txn
- Resolves: bug 1013738 - CLEANALLRUV doesnt run across all replicas
- Resolves: bug 1011220 - PassSync removes User must change password flag on the Windows side
- Resolves: bug 1008610 - tmpfiles.d references /var/lock when they should reference /run/lock
- Resolves: bug 1012125 - Set up replcation/agreement before initializing the sub suffix, the sub suffix is not found by ldapsearch
- Resolves: bug 1013063 - RUV tombstone search with scope "one" doesn`t work
- Resolves: bug 1013893 - Indexed search are logged with 'notes=U' in the access logs
- Resolves: bug 1013894 - improve logconv.pl performance with large access logs
- Resolves: bug 1013898 - Fix various issues with logconv.pl
- Resolves: bug 1013897 - logconv.pl uses /var/tmp for BDB temp files
- Resolves: bug 1013900 - logconv: some stats do not work across server restarts
- Resolves: bug 1014354 - Coverity fixes - 12023, 12024, and 12025

* Fri Sep 13 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-4
- bump version to 1.3.1.6-4
- Resolves Bug 1007988 - Under specific values of nsDS5ReplicaName, replication may get broken or updates missing (Ticket 47489)
- Resolves Bug 853931 - Allow macro aci keywords to be case-insensitive (Ticket 449)
- Resolves Bug 1006563 - automember rebuild task not working as expected (Ticket 47507)

* Fri Sep  6 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.6-3
- Ticket #47455 - valgrind - value mem leaks, uninit mem usage
- Ticket 47500 - start-dirsrv/restart-dirsrv/stop-disrv do not register with systemd correctly

* Mon Aug 26 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-2
- bump version to 1.3.1.6-2
- Resolves Bug 1000633 - ns-slapd crash due to bogus DN
- Ticket #47488 - Users from AD sub OU does not sync to IPA

* Thu Aug 01 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.6-1
- bump version to 1.3.1.6
- Ticket 47455 - valgrind - value mem leaks, uninit mem usage
- fix coverity 11915 - dead code - introduced with fix for ticket 346
- fix coverity 11895 - null deref - caused by fix to ticket 47392
- fix compiler warning in posix winsync code for posix_group_del_memberuid_callback
- Fix compiler warnings for Ticket 47395 and 47397
- fix compiler warning (cherry picked from commit 904416f4631d842a105851b4a9931ae17822a107)
- Ticket 47450 - Fix compiler formatting warning errors for 32/64 bit arch
- fix compiler warnings
- Fix compiler warning (cherry picked from commit ec6ebc0b0f085a82041d993ab2450a3922ef5502)

* Tue Jul 30 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.5-1
- bump version to 1.3.1.5
- Ticket 47456 - delete present values should append values to deleted values
- Ticket 47455 - valgrind - value mem leaks, uninit mem usage
- Ticket 47448 - Segfault in 389-ds-base-1.3.1.4-1.fc19 when setting up FreeIPA replication
- Ticket 47440 - Fix runtime errors caused by last patch.
- Ticket 47440 - Fix compilation warnings and header files
- Ticket 47405 - CVE-2013-2219 ACLs inoperative in some search scenarios
- Ticket 47447 - logconv.pl man page missing -m,-M,-B,-D
- Ticket 47378 - fix recent compiler warnings
- Ticket 47427 - Overflow in nsslapd-disk-monitoring-threshold
- Ticket 47449 - deadlock after adding and deleting entries
- Ticket 47441 - Disk Monitoring not checking filesystem with logs
- Ticket 47427 - Overflow in nsslapd-disk-monitoring-threshold

* Fri Jul 19 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.4-1
- bump version to 1.3.1.4
- Ticket 47435 - Very large entryusn values after enabling the USN plugin and the lastusn value is negat
- Ticket 47424 - Replication problem with add-delete requests on single-valued attributes
- Ticket 47367 - (phase 2) ldapdelete returns non-leaf entry error while trying to remove a leaf entry
- Ticket 47367 - (phase 1) ldapdelete returns non-leaf entry error while trying to remove a leaf entry
- Ticket 47421 - memory leaks in set_krb5_creds
- Ticket 346 - version 4 Slow ldapmodify operation time for large quantities of multi-valued attribute v
- Ticket 47369  version2 - provide default syntax plugin
- Ticket 47427 - Overflow in nsslapd-disk-monitoring-threshold
- Ticket 47339 - RHDS denies MODRDN access if ACI list contains any DENY rule
- Ticket 47427 - Overflow in nsslapd-disk-monitoring-threshold
- Ticket 47428 - Memory leak in 389-ds-base 1.2.11.15
- Ticket 47392 - ldbm errors when adding/modifying/deleting entries
- Ticket 47385 - Disk Monitoring is not triggered as expected.
- Ticket 47410 - changelog db deadlocks with DNA and replication

* Fri Jul 19 2013 Rich Megginson <rmeggins@redhat.com> - 1.3.1.3-1
- bump version to 1.3.1.3
- Ticket 47374 - flush.pl is not included in perl5
- Ticket 47391 - deleting and adding userpassword fails to update the password (additional fix)
- Ticket 47393 - Attribute are not encrypted on a consumer after a full initialization
- Ticket 47395 47397 - v2 correct behaviour of account policy if only stateattr is configured or no alternate attr is configured
- Ticket 47396 - crash on modrdn of tombstone
- Ticket 47400 - MMR stress test with dna enabled causes a deadlock
- Ticket 47409 - allow setting db deadlock rejection policy
- Ticket 47419 - Unhashed userpassword can accidentally get removed from mods
- Ticket 47420 - An upgrade script 80upgradednformat.pl fails to handle a server instance name incuding '-'

* Fri Jul 12 2013 Jan Safranek <jsafrane@redhat.com> - 1.3.1.2-2
- Rebuilt for new net-snmp

* Sat Jun 15 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.2-1
- bump version to 1.3.1.2
- Ticket 47391 - deleting and adding userpassword fails to update the password
- Coverity Fixes (Part 7)

* Fri Jun 14 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.1-1
- bump version to 1.3.1.1
- Ticket 402 - nhashed#user#password in entry extension
- Ticket 511 - Revision - allow turning off vattr lookup in search entry return
- Ticket 580 - Wrong error code return when using EXTERNAL SASL and no client certificate
- Ticket 47327 - error syncing group if group member user is not synced
- Ticket 47355 - dse.ldif doesn't replicate update to nsslapd-sasl-mapping-fallback
- Ticket 47359 - new ldap connections can block ldaps and ldapi connections
- Ticket 47362 - ipa upgrade selinuxusermap data not replicating
- Ticket 47375 - flush_ber error sending back start_tls response will deadlock
- Ticket 47376 - DESC should not be empty as per RFC 2252 (ldapv3)
- Ticket 47377 - make listen backlog size configurable
- Ticket 47378 - fix recent compiler warnings
- Ticket 47383 - connections attribute in cn=snmp,cn=monitor is counted twice
- Ticket 47385 - DS not shutting down when disk monitoring threshold is reached
- Coverity Fixes (part 1)
- Coverity Fixes (Part 2)
- Coverity Fixes (Part 3)
- Coverity Fixes (Part 4)
- Coverity Fixes (Part 5)

* Thu May 02 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.1.0-1
- bump version to 1.3.1.0
- Ticket 332 - Command line perl scripts should attempt most secure connection type first
- Ticket 342 - better error message when cache overflows
- Ticket 417 - RFE - forcing passwordmustchange attribute by non-cn=directory manager
- Ticket 419 - logconv.pl - improve memory management
- Ticket 422 - 389-ds-base - Can't call method "getText"
- Ticket 433 - multiple bugs in start-dirsrv, stop-dirsrv, restart-dirsrv scripts
- Ticket 458 - RFE - Make it possible for privileges to be provided to an admin user to import an LDIF file containing hashed passwords
- Ticket 471 - logconv.pl tool removes the access logs contents if "-M" is not correctly used
- Ticket 487 - Possible to add invalid attribute values to PAM PTA plugin configuration
- Ticket 502 - setup-ds.pl script should wait if "semanage.trans.LOCK" presen
- Ticket 505 - use lock-free access name2asi and oid2asi tables (additional)
- Ticket 508 - lock-free access to FrontendConfig structure
- Ticket 511 - allow turning off vattr lookup in search entry return
- Ticket 525 - Introducing a user visible configuration variable for controlling replication retry time
- Ticket 528 - RFE - get rid of instance specific scripts
- Ticket 529 - dn normalization must handle multiple space characters in attributes
- Ticket 532 - RUV is not getting updated for both Master and consumer
- Ticket 533 - only scan for attributes to decrypt if there are encrypted attrs configured
- Ticket 534 - RFE: Add SASL mappings fallback
- Ticket 537 - Improvement of range search
- Ticket 539 - logconv.pl should handle microsecond timing
- Ticket 543 - Sorting with attributes in ldapsearch gives incorrect result
- Ticket 545 - Segfault during initial LDIF import: str2entry_dupcheck()
- Ticket 547 - Incorrect assumption in ndn cache
- Ticket 550 - posix winsync will not create memberuid values if group entry become posix group in the same sync interval
- Ticket 551 - Multivalued rootdn-days-allowed in RootDN Access Control plugin always results in access control violation
- Ticket 552 - Adding rootdn-open-time without rootdn-close-time to RootDN Acess Control results in inconsistent configuration
- Ticket 558 - Replication - make timeout for protocol shutdown configurable
- Ticket 561 - disable writing unhashed#user#password to changelog
- Ticket 563 - DSCreate.pm: Error messages cannot be used in the if expression since they could be localized.
- Ticket 565 - turbo mode and replication - allow disable of turbo mode
- Ticket 571 - server does not accept 0 length LDAP Control sequence
- Ticket 574 - problems with dbcachesize disk space calculation
- Ticket 583 - dirsrv fails to start on reboot due to /var/run/dirsrv permissions
- Ticket 585 - Behaviours of "db2ldif -a <filename>" and "db2ldif.pl -a <filename>" are inconsistent
- Ticket 587 - Replication error messages in the DS error logs
- Ticket 588 - Create MAN pages for command line scripts
- Ticket 600 - Server should return unavailableCriticalExtension when processing a badly formed critical control
- Ticket 603 - A logic error in str2simple
- Ticket 604 - Required attribute not checked during search operation
- Ticket 608 - Posix Winsync plugin throws "posix_winsync_end_update_cb: failed to add task entry" error message
- Ticket 611 - logconv.pl missing stats for StartTLS, LDAPI, and AUTOBIND
- Ticket 612 - improve dbgen rdn generation, output
- Ticket 613 - ldclt: add timestamp, interval, nozeropad, other improvements
- Ticket 616 - High contention on computed attribute lock
- Ticket 618 - Crash at shutdown while stopping replica agreements
- Ticket 620 - Better logging of error messages for 389-ds-base
- Ticket 621 - modify operations without values need to be written to the changelog
- Ticket 622 - DS logging errors "libdb: BDB0171 seek: 2147483648: (262144 * 8192) + 0: No such file or directory
- Ticket 631 - Replication: "Incremental update started" status message without consumer initialized
- Ticket 633 - allow nsslapd-nagle to be disabled, and also tcp cork
- Ticket 47299 - allow cmdline scripts to work with non-root user
- Ticket 47302 - get rid of sbindir start/stop/restart slapd scripts
- Ticket 47303 - start/stop/restart dirsrv scripts should report and error if no instances
- Ticket 47304 - reinitialization of a master with a disabled agreement hangs
- Ticket 47311 - segfault in db2ldif(trigger by a cleanallruv task)
- Ticket 47312 - replace PR_GetFileInfo with PR_GetFileInfo64
- Ticket 47315 - filter option in fixup-memberof requires more clarification
- Ticket 47325 - Crash at shutdown on a replica aggrement
- Ticket 47330 - changelog db extension / upgrade is obsolete
- Ticket 47336 - logconv.pl -m not working for all stats
- Ticket 47341 - logconv.pl -m time calculation is wrong
- Ticket 47343 - 389-ds-base: Does not support aarch64 in f19 and rawhide
- Ticket 47347 - Simple paged results should support async search
- Ticket 47348 - add etimes to per second/minute stats
- Ticket 47349 - DS instance crashes under a high load

* Thu Mar 28 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0.5-1
- bump version to 1.3.0.5
- Ticket 47308 - unintended information exposure when anonymous access is set to rootdse
- Ticket 628 - crash in aci evaluation
- Ticket 627 - ns-slapd crashes sporadically with segmentation fault in libslapd.so
- Ticket 634 - Deadlock in DNA plug-in Ticket #576 - DNA: use event queue for config update only at the start up
- Ticket 632 - 389-ds-base cannot handle Kerberos tickets with PAC
- Ticket 623 - cleanAllRUV task fails to cleanup config upon completion

* Mon Mar 11 2013 Mark Reynolds <mreynolds@redhat.com> - 1.3.0.4-1
- e53d691 bump version to 1.3.0.4
- Bug 912964 - CVE-2013-0312 389-ds: unauthenticated denial of service vulnerability in handling of LDAPv3 control data
- Ticket 570 - DS returns error 20 when replacing values of a multi-valued attribute (only when replication is enabled)
- Ticket 490 - Slow role performance when using a lot of roles
- Ticket 590 - ns-slapd segfaults while trying to delete a tombstone entry

* Wed Feb 13 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0.3-1
- bump version to 1.3.0.3
- Ticket #584 - Existence of an entry is not checked when its password is to be deleted
- Ticket 562 - Crash when deleting suffix

* Fri Feb 01 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.3.0.2-2
- Rebuild for icu 50

* Wed Jan 16 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0.2-1
- bump version to 1.3.0.2
- Ticket #542 - Cannot dynamically set nsslapd-maxbersize

* Wed Jan 16 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0.1-1
- bump version to 1.3.0.1
- Ticket 556 - Don't overwrite certmap.conf during upgrade

* Tue Jan 08 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0.0-1
- bump version to 1.3.0.0

* Tue Jan 08 2013 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0-0.3.rc3
- bump version to 1.3.0.rc3
- Ticket 549 - DNA plugin no longer reports additional info when range is depleted
- Ticket 541 - need to set plugin as off in ldif template
- Ticket 541 - RootDN Access Control plugin is missing after upgrade 

* Fri Dec 14 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0-0.2.rc2
- bump version to 1.3.0.rc2
- Trac Ticket #497 - Escaped character cannot be used in the substring search filter
- Ticket 509 - lock-free access to be->be_suffixlock
- Trac Ticket #522 - betxn: upgrade is not implemented yet

* Tue Dec 11 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.3.0-0.1.rc1
- bump version to 1.3.0.rc1
- Ticket #322 - Create DOAP description for the 389 Directory Server project
- Trac Ticket #499 - Handling URP results is not corrrect
- Ticket 509 - lock-free access to be->be_suffixlock
- Ticket 456 - improve entry cache sizing
- Trac Ticket #531 - loading an entry from the database should use str2entry_f
- Trac Ticket #536 - Clean up compiler warnings for 1.3
- Trac Ticket #531 - loading an entry from the database should use str2entry_fast
- Ticket 509 - lock-free access to be->be_suffixlock
- Ticket 527 - ns-slapd segfaults if it cannot rename the logs
- Ticket 395 - RFE: 389-ds shouldn't advertise in the rootDSE that we can handle a sasl mech if we really can't
- Ticket 216 - disable replication agreements
- Ticket 518 - dse.ldif is 0 length after server kill or machine kill
- Ticket 393 - Change in winSyncInterval does not take immediate effect
- Ticket 20 - Allow automember to work on entries that have already been added
- Coverity Fixes
- Ticket 349 - nsViewFilter syntax issue in 389DS 1.2.5
- Ticket 337 - improve CLEANRUV functionality
- Fix for ticket 504
- Ticket 394 - modify-delete userpassword
- minor fixes for bdb 4.2/4.3 and mozldap
- Trac Ticket #276 - Multiple threads simultaneously working on connection's private buffer causes ns-slapd to abort
- Fix for ticket 465: cn=monitor showing stats for other db instances
- Ticket 507 - use mutex for FrontendConfig lock instead of rwlock
- Fix for ticket 510 Avoid creating an attribute just to determine the syntax for a type, look up the syntax directly by type
- Coverity defect: Resource leak 13110
- Ticket 517 - crash in DNA if no dnaMagicRegen is specified
- Trac Ticket #520 - RedHat Directory Server crashes (segfaults) when moving ldap entry
- Trac Ticket #519 - Search with a complex filter including range search is slow
- Trac Ticket #500 - Newly created users with organizationalPerson objectClass fails to sync from AD to DS with missing attribute error
- Trac Ticket #311 - IP lookup failing with multiple DNS entries
- Trac Ticket #447 - Possible to add invalid attribute to nsslapd-allowed-to-delete-attrs
- Trac Ticket #443 - Deleting attribute present in nsslapd-allowed-to-delete-attrs returns Operations error
- Ticket #503 - Improve AD version in winsync log message
- Trac Ticket #190 - Un-resolvable server in replication agreement produces unclear error message
- Coverity fixes
- Trac Ticket #391 - Slapd crashes when deleting backends while operations are still in progress
- Trac Ticket #448 - Possible to set invalid macros in Macro ACIs
- Trac Ticket #498 - Cannot abaondon simple paged result search
- Coverity defects
- Trac Ticket #494 - slapd entered to infinite loop during new index addition
- Fixing compiler warnings in the posix-winsync plugin
- Coverity defects
- Ticket 147 - Internal Password Policy usage very inefficient
- Ticket 495 - internalModifiersname not updated by DNA plugin
- Revert "Ticket 495 - internalModifiersname not updated by DNA plugin"
- Ticket 495 - internalModifiersname not updated by DNA plugin
- Ticket 468 - if pam_passthru is enabled, need to AC_CHECK_HEADERS([security/pam_appl.h])
- Ticket 486 - nsslapd-enablePlugin should not be multivalued
- Ticket 488 - Doc: DS error log messages with typo
- Trac Ticket #451 - Allow db2ldif to be quiet
- Ticket #491 - multimaster_extop_cleanruv returns wrong error codes
- Ticket #481 - expand nested posix groups
- Trac Ticket #455 - Insufficient rights to unhashed#user#password when user deletes his password
- Ticket #446 - anonymous limits are being applied to directory manager

* Tue Oct 9 2012 Mark Reynolds <mareynol@redhat.com> - 1.3.0.a1-1
Ticket #28 	MOD operations with chained delete/add get back error 53 on backend config
Ticket #173 	ds-logpipe.py script's man page and script help should be updated for -t option.
Ticket #196 	RFE: Interpret IPV6 addresses for ACIs, replication, and chaining 
Ticket #218 	RFE - Make RIP working with Replicated Entries 
Ticket #328 	make sure all internal search filters are properly escaped 
Ticket #329 	389-admin build fails on F-18 with new apache 	
Ticket #344 	deadlock in replica_write_ruv
Ticket #351 	use betxn plugins by default
Ticket #352 	make cos, roles, views betxn aware 
Ticket #356 	logconv.pl - RFE - track bind info
Ticket #365 	Audit log - clear text password in user changes 
Ticket #370 	Opening merge qualifier CoS entry using RHDS console changes the entry. 
Ticket #372 	Setting nsslapd-listenhost or nsslapd-securelistenhost breaks ACI processing 	
Ticket #386 	Overconsumption of memory with large cachememsize and heavy use of ldapmodify 	
Ticket #402 	unhashedTicket #userTicket #password in entry extension 	
Ticket #408 	Create a normalized dn cache 	
Ticket #453 	db2index with -tattrname:type,type fails 	
Ticket #461 	fix build problem with mozldap c sdk 	
Ticket #462 	add test for include file mntent.h 	
Ticket #463 	different parameters of getmntent in Solaris

* Tue Sep 25 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.15-1
- Trac Ticket #470 - 389 prevents from adding a posixaccount with userpassword after schema reload
- Ticket 477 - CLEANALLRUV if there are only winsync agmts task will hang
- Ticket 457 - dirsrv init script returns 0 even when few or all instances fail to start
- Ticket 473 - change VERSION.sh to have console version be major.minor
- Ticket 475 - Root DN Access Control - improve value checking for config
- Trac Ticket #466 - entry_apply_mod - ADD: Failed to set unhashed#user#password to extension
- Ticket 474 - Root DN Access Control - days allowed not working correctly
- Ticket 467 - CLEANALLRUV abort task should be able to ignore down replicas
- 0b79915 fix compiler warnings in ticket 374 code
- Ticket 452 - automember rebuild task adds users to groups that do not match the configuration scope

* Fri Sep  7 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.14-1
- Ticket 450 - CLEANALLRUV task gets stuck on winsync replication agreement
- Ticket 386 - large memory growth with ldapmodify(heap fragmentation)
-  this patch doesn't fix the bug - it allows us to experiment with
-  different values of mxfast
- Ticket #374 - consumer can go into total update mode for no reason

* Tue Sep  4 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.13-1
- Ticket #426 - support posix schema for user and group sync
-   1) plugin config ldif must contain pluginid, etc. during upgrade or it
-      will fail due to schema errors
-   2) posix winsync should have a lower precedence (25) than the default (50)
-      so that it will be run first
-   3) posix winsync should support the Winsync API v3 - the v2 functions are
-      just stubs for now - but the precedence cb is active

* Thu Aug 30 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.12-1
- 8e5087a Coverity defects - 13089: Dereference after null check ldbm_back_delete
- Trac Ticket #437 - variable dn should not be used in ldbm_back_delete
- ba1f5b2 fix coverity resource leak in windows_plugin_add
- e3e81db Simplify program flow: change while loops to for
- a0d5dc0 Fix logic errors: del_mod should be latched (might not be last mod), and avoid skipping add-mods (int value 0)
- 0808f7e Simplify program flow: make adduids/moduids/deluids action blocks all similar
- 77eb760 Simplify program flow: eliminate unnecessary continue
- c9e9db7 Memory leaks: unmatched slapi_attr_get_valueset and slapi_value_new
- a4ca0cc Change "return"s in modGroupMembership to "break"s to avoid leaking
- d49035c Factorize into new isPosixGroup function
- 3b61c03 coverity - posix winsync mem leaks, null check, deadcode, null ref, use after free
- 33ce2a9 fix mem leaks with parent dn log message, setting winsync windows domain
- Ticket #440 - periodic dirsync timed event causes server to loop repeatedly
- Ticket #355 - winsync should not delete entry that appears to be out of scope
- Ticket 436 - nsds5ReplicaEnabled can be set with any invalid values.
- 487932d coverity - mbo dead code - winsync leaks, deadcode, null check, test code
- 2734a71 CLEANALLRUV coverity fixes
- Ticket #426 - support posix schema for user and group sync
- Ticket #430 - server to server ssl client auth broken with latest openldap

* Mon Aug 20 2012 Mark Reynolds <mareynol@redhat.com> - 1.2.11.11-1
6c0778f bumped version to 1.2.11.11
Ticket 429 - added nsslapd-readonly to DS schema
Ticket 403 - fix CLEANALLRUV regression from last commit
Trac Ticket #346 - Slow ldapmodify operation time for large quantities of multi-valued attribute values

* Wed Aug 15 2012 Mark Reynolds <mareynol@redhat.com> - 1.2.11.10-1
db6b354 bumped version to 1.2.11.10
Ticket 403 - CLEANALLRUV revisions

* Tue Aug 7 2012 Mark Reynolds <mareynol@redhat.com> - 1.2.11.9-1
ea05e69 Bumped version to 1.2.11.9
Ticket 407 - dna memory leak - fix crash from prev fix

* Fri Aug 3 2012 Mark Reynolds <mareynol@redhat.com> - 1.2.11.8-1
ddcf669 bump version to 1.2.11.8 for offical release
Ticket #425 - support multiple winsync plugins
Ticket 403 - cleanallruv coverity fixes
Ticket 407 - memory leak in dna plugin
Ticket 403 - CLEANALLRUV feature
Ticket 413 - "Server is unwilling to perform" when running ldapmodify on nsds5ReplicaStripAttrs
3168f04 Coverity defects
5ff0a02 COVERITY FIXES
Ticket #388 - Improve replication agreement status messages
0760116 Update the slapi-plugin documentation on new slapi functions, and added a slapi function for checking on shutdowns
Ticket #369 - restore of replica ldif file on second master after deleting two records shows only 1 deletion
Ticket #409 - Report during startup if nsslapd-cachememsize is too small
Ticket #412 - memberof performance enhancement
12813: Uninitialized pointer read string_values2keys
Ticket #346 - Slow ldapmodify operation time for large quantities of multi-valued attribute values
Ticket #346 - Slow ldapmodify operation time for large quantities of multi-valued attribute values
Ticket #410 - Referential integrity plug-in does not work when update interval is not zero
Ticket #406 - Impossible to rename entry (modrdn) with Attribute Uniqueness plugin enabled
Ticket #405 - referint modrdn not working if case is different
Ticket 399 - slapi_ldap_bind() doesn't check bind results

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11.7-2.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Petr Pisar <ppisar@redhat.com> - 1.2.11.7-2.1
- Perl 5.16 rebuild

* Wed Jun 27 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.7-2
- Ticket 378 - unhashed#user#password visible after changing password
-  fix func declaration from previous patch
- Ticket 366 - Change DS to purge ticket from krb cache in case of authentication error

* Wed Jun 27 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.7-1
- Trac Ticket 396 - Account Usability Control Not Working

* Thu Jun 21 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.6-1
- Ticket #378 - audit log does not log unhashed password: enabled, by default.
- Ticket #378 - unhashed#user#password visible after changing password
- Ticket #365 - passwords in clear text in the audit log

* Tue Jun 19 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.5-2
- workaround for https://bugzilla.redhat.com/show_bug.cgi?id=833529

* Mon Jun 18 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.5-1
- Ticket #387 - managed entry sometimes doesn't delete the managed entry
- 5903815 improve txn test index handling
- Ticket #360 - ldapmodify returns Operations error - fix delete caching
- bcfa9e3 Coverity Fix for CLEANALLRUV
- Trac Ticket #335 - transaction retries need to be cache aware
- Ticket #389 - ADD operations not in audit log
- 44cdc84 fix coverity issues with uninit vals, no return checking
- Ticket 368 - Make the cleanAllRUV task one step
- Ticket #110 - RFE limiting root DN by host, IP, time of day, day of week

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1.2.11.4-1.1
- Perl 5.16 rebuild

* Tue May 22 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.4-1
- Ticket #360 - ldapmodify returns Operations error
- Ticket #321 - krbExtraData is being null modified and replicated on each ssh login
- Trac Ticket #359 - Database RUV could mismatch the one in changelog under the stress
- Ticket #361: Bad DNs in ACIs can segfault ns-slapd
- Trac Ticket #338 - letters in object's cn get converted to lowercase when renaming object
- Ticket #337 - Improve CLEANRUV task

* Sat May  5 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.3-1
- Ticket #358 - managed entry doesn't delete linked entry

* Fri May  4 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.2-1
- Ticket #351 - use betxn plugins by default
-   revert - make no plugins betxn by default - too great a risk
-   for deadlocks until we can test this better
- Ticket #348 - crash in ldap_initialize with multiple threads
-   fixes PR_Init problem in ldclt

* Wed May  2 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11.1-1
- f227f11 Suppress alert on unavailable port with forced setup
- Ticket #353 - coverity 12625-12629 - leaks, dead code, unchecked return
- Ticket #351 - use betxn plugins by default
- Trac Ticket #345 - db deadlock return should not log error
- Ticket #348 - crash in ldap_initialize with multiple threads
- Ticket #214 - Adding Replication agreement should complain if required nsds5ReplicaCredentials not supplied
- Ticket #207 - [RFE] enable attribute that tracks when a password was last set
- Ticket #216 - RFE - Disable replication agreements
- Ticket #337 - RFE - Improve CLEANRUV functionality
- Ticket #326 - MemberOf plugin should work on all backends
- Trac Ticket #19 - Convert entryUSN plugin to transaction aware type
- Ticket #347 - IPA dirsvr seg-fault during system longevity test
- Trac Ticket #310 - Avoid calling escape_string() for logged DNs
- Trac Ticket #338 - letters in object's cn get converted to lowercase when renaming object
- Ticket #183 - passwordMaxFailure should lockout password one sooner
- Trac Ticket #335 - transaction retries need to be cache aware
- Ticket #336 - [abrt] 389-ds-base-1.2.10.4-2.fc16: index_range_read_ext: Process /usr/sbin/ns-slapd was killed by signal 11 (SIGSEGV)
- Ticket #325 - logconv.pl : use of getopts to parse command line options
- Ticket #336 - [abrt] 389-ds-base-1.2.10.4-2.fc16: index_range_read_ext: Process /usr/sbin/ns-slapd was killed by signal 11 (SIGSEGV)
- 554e29d Coverity Fixes
- Trac Ticket #46 - (additional 2) setup-ds-admin.pl does not like ipv6 only hostnames
- Ticket #183 - passwordMaxFailure should lockout password one sooner - and should be configurable to avoid regressions
- Ticket #315 - small fix to libglobs
- Ticket #315 - ns-slapd exits/crashes if /var fills up
- Ticket #20 - Allow automember to work on entries that have already been added
- Trac Ticket #45 - Fine Grained Password policy: if passwordHistory is on, deleting the password fails.

* Fri Mar 30 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.11-0.1.a1
- 453eb97 schema def must have DESC '' - close paren must be preceded by space
- Trac Ticket #46 - (additional) setup-ds-admin.pl does not like ipv6 only hostnames
- Ticket #331 - transaction errors with db 4.3 and db 4.2
- Ticket #261 - Add Solaris i386
- Ticket #316 and Ticket #70 - add post add/mod and AD add callback hooks
- Ticket #324 - Sync with group attribute containing () fails
- Ticket #319 - ldap-agent crashes on start with signal SIGSEGV
- 77cacd9 coverity 12606 Logically dead code
- Trac Ticket #303 - make DNA range requests work with transactions
- Ticket #320 - allow most plugins to be betxn plugins
- Ticket #24 - Add nsTLS1 to the DS schema
- Ticket #271 - Slow shutdown when you have 100+ replication agreements
- TIcket #285 - compilation fixes for '--format-security'
- Ticket 211 - Avoid preop range requests non-DNA operations
- Ticket #271 - replication code cleanup
- Ticket 317 - RHDS fractional replication with excluded password policy attributes leads to wrong error messages.
- Ticket #308 - Automembership plugin fails if data and config area mixed in the plugin configuration
- Ticket #292 - logconv.pl reporting unindexed search with different search base than shown in access logs
- 6f8680a coverity 12563 Read from pointer after free (fix 2)
- e6a9b22 coverity 12563 Read from pointer after free
- 245d494 Config changes fail because of unknown attribute "internalModifiersname"
- Ticket #191  - Implement SO_KEEPALIVE in network calls
- Ticket #289 - allow betxn plugin config changes
- 93adf5f destroy the entry cache and dn cache in the dse post op delete callback
- e2532d8 init txn thread private data for all database modes
- Ticket #291 - cannot use & in a sasl map search filter
- 6bf6e79 Schema Reload crash fix
- 60b2d12 Fixing compiler warnings
- Trac Ticket #260 - 389 DS does not support multiple paging controls on a single connection
- Ticket #302 - use thread local storage for internalModifiersName & internalCreatorsName
- fdcc256 Minor bug fix introcuded by commit 69c9f3bf7dd9fe2cadd5eae0ab72ce218b78820e
- Ticket #306 - void function cannot return value
- ticket 181 - Allow PAM passthru plug-in to have multiple config entries
- ticket 211 - Use of uninitialized variables in ldbm_back_modify()
- Ticket #74 - Add schema for DNA plugin (RFE)
- Ticket #301 - implement transaction support using thread local storage
- Ticket #211 - dnaNextValue gets incremented even if the user addition fails
- 144af59 coverity uninit var and resource leak
- Trac Ticket #34 - remove-ds.pl does not remove everything
- Trac Ticket #169 - allow 389 to use db5
- bc78101 fix compiler warning in acct policy plugin
- Trac Ticket #84 - 389 Directory Server Unnecessary Checkpoints
- Trac Ticket #27 - SASL/PLAIN binds do not work
- Ticket #129 - Should only update modifyTimestamp/modifiersName on MODIFYops
- Ticket #17 - new replication optimizations

* Tue Mar 27 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.2.10.4-4
- Ticket #46 - (revised) setup-ds-admin.pl does not like ipv6 only hostnames
- Ticket #66 - 389-ds-base spec file does not have a BuildRequires on gcc-c++

* Fri Mar 23 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.2.10.4-3
- Ticket #46 - setup-ds-admin.pl does not like ipv6 only hostnames

* Wed Mar 21 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.4-2
- get rid of posttrans - move update code to post

* Tue Mar 13 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.4-1
- Ticket #305 - Certain CMP operations hang or cause ns-slapd to crash

* Mon Mar  5 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.3-1
- b05139b memleak in normalize_mods2bvals
- c0eea24 memleak in mep_parse_config_entry
- 90bc9eb handle null smods
- Ticket #305 - Certain CMP operations hang or cause ns-slapd to crash
- Ticket #306 - void function cannot return value
- ticket 304 - Fix kernel version checking in dsktune

* Thu Feb 23 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.2-1
- Trac Ticket #298 - crash when replicating orphaned tombstone entry
- Ticket #281 - TLS not working with latest openldap
- Trac Ticket #290 - server hangs during shutdown if betxn pre/post op fails
- Trac Ticket #26 - Please support setting defaultNamingContext in the rootdse

* Tue Feb 14 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.2.10.1-2
- Ticket #124 - add Provides: ldif2ldbm to rpm

* Tue Feb 14 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.1-1
- Ticket #294 - 389 DS Segfaults during replica install in FreeIPA

* Mon Feb 13 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10.0-1
- Ticket 284 - Remove unnecessary SNMP MIB files
- Ticket 51 - memory leaks in 389-ds-base-1.2.8.2-1.el5?
- Ticket 175 - logconv.pl improvements

* Fri Feb 10 2012 Noriko Hosoi <nhosoi@redhat.com> - 1.2.10-0.10.rc1.2
- Introducing use_db4 macro to support db5 (libdb).

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1.2.10-0.10.rc1.1
- Rebuild against PCRE 8.30

* Thu Feb  2 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.10.rc1
- ad9dd30 coverity 12488 Resource leak In attr_index_config(): Leak of memory or pointers to system resources
- Ticket #281 - TLS not working with latest openldap
- Ticket #280 - extensible binary filters do not work
- Ticket #279 - filter normalization does not use matching rules
- Trac Ticket #275 - Invalid read reported by valgrind
- Ticket #277 - cannot set repl referrals or state
- Ticket #278 - Schema replication update failed: Invalid syntax
- Ticket #39 - Account Policy Plugin does not work for simple binds when PAM Pass Through Auth plugin is enabled
- Ticket #13 - slapd process exits when put the database on read only mode while updates are coming to the server
- Ticket #87 - Manpages fixes
- c493fb4 fix a couple of minor coverity issues
- Ticket #55 - Limit of 1024 characters for nsMatchingRule
- Trac Ticket #274 - Reindexing entryrdn fails if ancestors are also tombstoned
- Ticket #6 - protocol error from proxied auth operation
- Ticket #38 - nisDomain schema is incorrect
- Ticket #273 - ruv tombstone searches don't work after reindex entryrdn
- Ticket #29 - Samba3-schema is missing sambaTrustedDomainPassword
- Ticket #22 - RFE: Support sendmail LDAP routing schema
- Ticket #161 - Review and address latest Coverity issues
- Ticket #140 - incorrect memset parameters
- Trac Ticket 35 - Log not clear enough on schema errors
- Trac Ticket 139 - eliminate the use of char *dn in favor of Slapi_DN *dn
- Trac Ticket #52 - FQDN set to nsslapd-listenhost makes the server start fail if IPv4-mapped-IPv6 address is given

* Tue Jan 24 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.9.a8
- Ticket #272 - add tombstonenumsubordinates to schema

* Mon Jan 23 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.8.a7
- fixes for systemd - remove .pid files after shutting down servers
- Ticket #263 - add systemd include directive
- Ticket #264 - upgrade needs better check for "server is running"

* Fri Jan 20 2012 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.7.a7
- Ticket #262 - pid file not removed with systemd
- Ticket #50 - server should not call a plugin after the plugin close function is called
- Ticket #18 - Data inconsitency during replication
- Ticket #49 - better handling for server shutdown while long running tasks are active
- Ticket #15 - Get rid of rwlock.h/rwlock.c and just use slapi_rwlock instead
- Ticket #257 - repl-monitor doesn't work if leftmost hostnames are the same
- Ticket #12 - 389 DS DNA Plugin / Replication failing on GSSAPI
- 6aaeb77 add a hack to disable sasl hostname canonicalization
- Ticket 168 - minssf should not apply to rootdse
- Ticket #177 - logconv.pl doesn't detect restarts
- Ticket #159 - Managed Entry Plugin runs against managed entries upon any update without validating
- Ticket 75 - Unconfigure plugin opperations are being called.
- Ticket 26 - Please support setting defaultNamingContext in the rootdse.
- Ticket #71 - unable to delete managed entry config
- Ticket #167 - Mixing transaction and non-transaction plugins can cause deadlock
- Ticket #256 - debug build assertion in ACL_EvalDestroy()
- Ticket #4 - bak2db gets stuck in infinite loop
- Ticket #162 - Infinite loop / spin inside strcmpi_fast, acl_read_access_allowed_on_attr, server DoS
- Ticket #3: acl cache overflown problem
- Ticket 1 - pre-normalize filter and pre-compile substring regex - and other optimizations
- Ticket 2 - If node entries are tombstone'd, subordinate entries fail to get the full DN.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-0.6.a6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 15 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.6.a6
- Bug 755725 - 389 programs linked against openldap crash during shutdown
- Bug 755754 - Unable to start dirsrv service using systemd
- Bug 745259 - Incorrect entryUSN index under high load in replicated environment
- d439e3a use slapi_hexchar2int and slapi_str_to_u8 everywhere
- 5910551 csn_init_as_string should not use sscanf
- b53ba00 reduce calls to csn_as_string and slapi_log_error
- c897267 fix member variable name error in slapi_uniqueIDFormat
- 66808e5 uniqueid formatting - use slapi_u8_to_hex instead of sprintf
- 580a875 csn_as_string - use slapi_uN_to_hex instead of sprintf
- Bug 751645 - crash when simple paged fails to send entry to client
- Bug 752155 - Use restorecon after creating init script lock file

* Fri Nov  4 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.5.a5
- Bug 751495 - 'setup-ds.pl -u' fails with undefined routine 'updateSystemD'
- Bug 750625 750624 750622 744946 Coverity issues
- Bug 748575 - part 2 - rhds81 modrdn operation and 100% cpu use in replication
- Bug 748575 - rhds81 modrn operation and 100% cpu use in replication
- Bug 745259 - Incorrect entryUSN index under high load in replicated environment
- f639711 Reduce the number of DN normalization
- c06a8fa Keep unhashed password psuedo-attribute in the adding entry
- Bug 744945 - nsslapd-counters attribute value cannot be set to "off"
- 8d3b921 Use new PLUGIN_CONFIG_ENTRY feature to allow switching between txn and regular
- d316a67 Change referential integrity to be a betxnpostoperation plugin

* Fri Oct  7 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10-0.4.a4
- Bug 741744 - part3 - MOD operations with chained delete/add get back error 53
- 1d2f5a0 make memberof transaction aware and able to be a betxnpostoperation plug in
- b6d3ba7 pass the plugin config entry to the plugin init function
- 28f7bfb set the ENTRY_POST_OP for modrdn betxnpostoperation plugins
- Bug 743966 - Compiler warnings in account usability plugin

* Wed Oct  5 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10.a3-0.3
- 498c42b fix transaction support in ldbm_delete

* Wed Oct  5 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10.a2-0.2
- Bug 740942 - allow resource limits to be set for paged searches independently of limits for other searches/operations
- Bug 741744 - MOD operations with chained delete/add get back error 53 on backend config
- Bug 742324 - allow nsslapd-idlistscanlimit to be set dynamically and per-user

* Wed Sep 21 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.10.a1-0.1
- Bug 695736 - Providing native systemd file

* Wed Sep  7 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.10-2
- corrected source

* Wed Sep  7 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.10-1
- Bug 735114 - renaming a managed entry does not update mepmanagedby

* Thu Sep  1 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.9-1
- Bug 735121 - simple paged search + ip/dns based ACI hangs server
- Bug 722292 - (cov#11030) Leak of mapped_sdn in winsync rename code
- Bug 703990 - cross-platform - Support upgrade from Red Hat Directory Server
- Introducing an environment variable USE_VALGRIND to clean up the entry cache and dn cache on exit.

* Wed Aug 31 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.8-1
- Bug 732153 - subtree and user account lockout policies implemented?
- Bug 722292 - Entries in DS are not updated properly when using WinSync API

* Wed Aug 24 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.7-1
- Bug 733103 - large targetattr list with syntax errors cause server to crash or hang
- Bug 633803 - passwordisglobalpolicy attribute brakes TLS chaining
- Bug 732541 - Ignore error 32 when adding automember config
- Bug 728592 - Allow ns-slapd to start with an invalid server cert

* Wed Aug 10 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.6-1
- Bug 728510 - Run dirsync after sending updates to AD
- Bug 729717 - Fatal error messages when syncing deletes from AD
- Bug 729369 - upgrade DB to upgrade from entrydn to entryrdn format is not working.
- Bug 729378 - delete user subtree container in AD + modify password in DS == DS crash
- Bug 723937 - Slapi_Counter API broken on  32-bit F15
-   fixed again - separate tests for atomic ops and atomic bool cas

* Mon Aug  8 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.5-1
- Bug 727511 - ldclt SSL search requests are failing with "illegal error number -1" error
-  Fix another coverity NULL deref in previous patch

* Thu Aug  4 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.4-1
- Bug 727511 - ldclt SSL search requests are failing with "illegal error number -1" error
-  Fix coverity NULL deref in previous patch

* Wed Aug  3 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.3-1
- Bug 727511 - ldclt SSL search requests are failing with "illegal error number -1" error
-  previous patch broke build on el5

* Wed Aug  3 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.2-1
- Bug 727511 - ldclt SSL search requests are failing with "illegal error number -1" error

* Tue Aug  2 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.1-2
- Bug 723937 - Slapi_Counter API broken on  32-bit F15
-   fixed to use configure test for GCC provided 64-bit atomic functions

* Wed Jul 27 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.1-1
- Bug 663752 - Cert renewal for attrcrypt and encchangelog
-   this was "re-fixed" due to a deadlock condition with cl2ldif task cancel
- Bug 725953 - Winsync: DS entries fail to sync to AD, if the User's CN entry contains a comma
- Bug 725743 - Make memberOf use PRMonitor for it's operation lock
- Bug 725542 - Instance upgrade fails when upgrading 389-ds-base package
- Bug 723937 - Slapi_Counter API broken on  32-bit F15

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1.2.9.0-1.2
- Perl mass rebuild

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1.2.9.0-1.1
- Perl mass rebuild

* Fri Jul 15 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9.0-1
- Bug 720059 - RDN with % can cause crashes or missing entries
- Bug 709468 - RSA Authentication Server timeouts when using simple paged results on RHDS 8.2.
- Bug 691313 - Need TLS/SSL error messages in repl status and errors log
- Bug 712855 - Directory Server 8.2 logs "Netscape Portable Runtime error -5961 (TCP connection reset by peer.)" to error log whereas Directory Server 8.1 did not
- Bug 713209 - Update sudo schema
- Bug 719069 - clean up compiler warnings in 389-ds-base 1.2.9
- Bug 718303 - Intensive updates on masters could break the consumer's cache
- Bug 711679 - unresponsive LDAP service when deleting vlv on replica

* Mon Jun 27 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9-0.2.a2
- 389-ds-base-1.2.9.a2
- look for separate openldap ldif library
- Split automember regex rules into separate entries
- writing Inf file shows SchemaFile = ARRAY(0xhexnum)
- add support for ldif files with changetype: add
- Bug 716980 - winsync uses old AD entry if new one not found
- Bug 697694 - rhds82 - incr update state stop_fatal_error "requires administrator action", with extop_result: 9
- bump console version to 1.2.6
- Bug 711679 - unresponsive LDAP service when deleting vlv on replica
- Bug 703703 - setup-ds-admin.pl asks for legal agreement to a non-existant file
- Bug 706209 - LEGAL: RHEL6.1 License issue for 389-ds-base package
- Bug 663752 - Cert renewal for attrcrypt and encchangelog
- Bug 706179 - DS can not restart after create a new objectClass has entryusn attribute
- Bug 711906 - ns-slapd segfaults using suffix referrals
- Bug 707384 - only allow FIPS approved cipher suites in FIPS mode
- Bug 710377 - Import with chain-on-update crashes ns-slapd
- Bug 709826 - Memory leak: when extra referrals configured

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.9-0.1.a1.2
- Perl mass rebuild

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.2.9-0.1.a1.1
- Perl 5.14 mass rebuild

* Thu May 26 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.9-0.1.a1
- 389-ds-base-1.2.9.a1
- Auto Membership
- More Coverity fixes

* Mon May  2 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8.3-1
- 389-ds-base-1.2.8.3
- Bug 700145 - userpasswd not replicating
- Bug 700557 - Linked attrs callbacks access free'd pointers after close
- Bug 694336 - Group sync hangs Windows initial Sync
- Bug 700215 - ldclt core dumps
- Bug 695779 - windows sync can lose old values when a new value is added
- Bug 697027 - 12 - minor memory leaks found by Valgrind + TET

* Thu Apr 14 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8.2-1
- 389-ds-base-1.2.8.2
- Bug 696407 - If an entry with a mixed case RDN is turned to be
-    a tombstone, it fails to assemble DN from entryrdn

* Fri Apr  8 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8.1-1
- 389-ds-base-1.2.8.1
- Bug 693962 - Full replica push loses some entries with multi-valued RDNs

* Tue Apr  5 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8.0-1
- 389-ds-base-1.2.8.0
- Bug 693473 - rhds82 rfe - windows_tot_run to log Sizelimit exceeded instead of LDAP error - -1
- Bug 692991 - rhds82 - windows_tot_run: failed to obtain data to send to the consumer; LDAP error - -1
- Bug 693466 - Unable to change schema online
- Bug 693503 - matching rules do not inherit from superior attribute type
- Bug 693455 - nsMatchingRule does not work with multiple values
- Bug 693451 - cannot use localized matching rules
- Bug 692331 - Segfault on index update during full replication push on 1.2.7.5

* Mon Apr  4 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.10.rc5
- 389-ds-base-1.2.8.rc5
- Bug 692469 - Replica install fails after step for "enable GSSAPI for replication"

* Tue Mar 29 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.9.rc4
- 389-ds-base-1.2.8.rc4
- Bug 668385 - DS pipe log script is executed as many times as the dirsrv serv
ice is restarted
- 389-ds-base-1.2.8.rc3
- Bug 690955 - Mrclone fails due to the replica generation id mismatch

* Tue Mar 22 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.8.rc2
- 389-ds-base-1.2.8 release candidate 2 - git tag 389-ds-base-1.2.8.rc2
- Bug 689537 - (cov#10610) Fix Coverity NULL pointer dereferences
- Bug 689866 - ns-newpwpolicy.pl needs to use the new DN format
- Bug 681015 - RFE: allow fine grained password policy duration attributes
-              in days, hours, minutes, as well
- Bug 684996 - Exported tombstone cannot be imported correctly
- Bug 683250 - slapd crashing when traffic replayed
- Bug 668909 - Can't modify replication agreement in some cases
- Bug 504803 - Allow maxlogsize to be set if logmaxdiskspace is -1
- Bug 644784 - Memory leak in "testbind.c" plugin
- Bug 680558 - Winsync plugin fails to restrain itself to the configured subtree

* Mon Mar  7 2011 Caolán McNamara <caolanm@redhat.com> - 1.2.8-0.7.rc1
- rebuild for icu 4.6

* Wed Mar  2 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.6.rc1
- 389-ds-base-1.2.8 release candidate 1 - git tag 389-ds-base-1.2.8.rc1
- Bug 518890 - setup-ds-admin.pl - improve hostname validation
- Bug 681015 - RFE: allow fine grained password policy duration attributes in 
-     days, hours, minutes, as well
- Bug 514190 - setup-ds-admin.pl --debug does not log to file
- Bug 680555 - ns-slapd segfaults if I have more than 100 DBs
- Bug 681345 - setup-ds.pl should set SuiteSpotGroup automatically
- Bug 674852 - crash in ldap-agent when using OpenLDAP
- Bug 679978 - modifying attr value crashes the server, which is supposed to
-     be indexed as substring type, but has octetstring syntax
- Bug 676655 - winsync stops working after server restart
- Bug 677705 - ds-logpipe.py script is failing to validate "-s" and
-     "--serverpid" options with "-t".
- Bug 625424 - repl-monitor.pl doesn't work in hub node

* Mon Feb 28 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.5.a3
- Bug 676598 - 389-ds-base multilib: file conflicts
- split off libs into a separate -libs package

* Thu Feb 24 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.4.a3
- do not create /var/run/dirsrv - setup will create it instead
- remove the fedora-ds initscript upgrade stuff - we do not support that anymore
- convert the remaining lua stuff to plain old shell script

* Wed Feb  9 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.3.a3
- 1.2.8.a3 release - git tag 389-ds-base-1.2.8.a3
- Bug 675320 - empty modify operation with repl on or lastmod off will crash server
- Bug 675265 - preventryusn gets added to entries on a failed delete
- Bug 677774 - added support for tmpfiles.d
- Bug 666076 - dirsrv crash (1.2.7.5) with multiple simple paged result search
es
- Bug 672468 - Don't use empty path elements in LD_LIBRARY_PATH
- Bug 671199 - Don't allow other to write to rundir
- Bug 678646 - Ignore tombstone operations in managed entry plug-in
- Bug 676053 - export task followed by import task causes cache assertion
- Bug 677440 - clean up compiler warnings in 389-ds-base 1.2.8
- Bug 675113 - ns-slapd core dump in windows_tot_run if oneway sync is used
- Bug 676689 - crash while adding a new user to be synced to windows
- Bug 604881 - admin server log files have incorrect permissions/ownerships
- Bug 668385 - DS pipe log script is executed as many times as the dirsrv serv
ice is restarted
- Bug 675853 - dirsrv crash segfault in need_new_pw()

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-0.2.a2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Rich Megginson <rmeggins@redhat.com> - 1.2.8-0.2.a2
- 1.2.8.a2 release - git tag 389-ds-base-1.2.8.a2
- Bug 674430 - Improve error messages for attribute uniqueness
- Bug 616213 - insufficient stack size for HP-UX on PA-RISC
- Bug 615052 - intrinsics and 64-bit atomics code fails to compile
-    on PA-RISC
- Bug 151705 - Need to update Console Cipher Preferences with new ciphers
- Bug 668862 - init scripts return wrong error code
- Bug 670616 - Allow SSF to be set for local (ldapi) connections
- Bug 667935 - DS pipe log script's logregex.py plugin is not redirecting the 
-    log output to the text file
- Bug 668619 - slapd stops responding
- Bug 624547 - attrcrypt should query the given slot/token for
-    supported ciphers
- Bug 646381 - Faulty password for nsmultiplexorcredentials does not give any 
-    error message in logs

* Fri Jan 21 2011 Nathan Kinder <nkinder@redhat.com> - 1.2.8-0.1.a1
- 1.2.8-0.1.a1 release - git tag 389-ds-base-1.2.8.a1
- many bug fixes

* Thu Dec 16 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.5-1
- 1.2.7.5 release - git tag 389-ds-base-1.2.7.5
- Bug 663597 - Memory leaks in normalization code

* Tue Dec 14 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.4-2
- Resolves: bug 656541 - use %ghost on files in /var/lock

* Fri Dec 10 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.4-1
- 1.2.7.4 release - git tag 389-ds-base-1.2.7.4
- Bug 661792 - Valid managed entry config rejected

* Wed Dec  8 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.3-1
- 1.2.7.3 release - git tag 389-ds-base-1.2.7.3
- Bug 658312 - Invalid free in Managed Entry plug-in
- Bug 641944 - Don't normalize non-DN RDN values

* Fri Dec  3 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.2-1
- 1.2.7.2 release - git tag 389-ds-base-1.2.7.2
- Bug 659456 - Incorrect usage of ber_printf() in winsync code
- Bug 658309 - Process escaped characters in managed entry mappings
- Bug 197886 - Initialize return value for UUID generation code
- Bug 658312 - Allow mapped attribute types to be quoted
- Bug 197886 - Avoid overflow of UUID generator

* Tue Nov 23 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.1-2
- last commit had bogus commit log

* Tue Nov 23 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7.1-1
- 1.2.7.1 release - git tag 389-ds-base-1.2.7.1
- Bug 656515 - Allow Name and Optional UID syntax for grouping attributes
- Bug 656392 - Remove calls to ber_err_print()
- Bug 625950 - hash nsslapd-rootpw changes in audit log

* Tue Nov 16 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.7-2
- 1.2.7 release - git tag 389-ds-base-1.2.7

* Fri Nov 12 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.7-1
- Bug 648949 - Merge dirsrv and dirsrv-admin policy modules into base policy

* Tue Nov  9 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.6.a5
- 1.2.7.a5 release - git tag 389-ds-base-1.2.7.a5
- Bug 643979 - Strange byte sequence for attribute with no values (nsslapd-ref
erral)
- Bug 635009 - Add one-way AD sync capability
- Bug 572018 - Upgrading from 1.2.5 to 1.2.6.a2 deletes userRoot
- put replication config entries in separate file
- Bug 567282 - server can not abandon searchRequest of "simple paged results"
- Bug 329751 - "nested" filtered roles searches candidates more than needed
- Bug 521088 - DNA should check ACLs before getting a value from the range

* Mon Nov  1 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.5.a4
- 1.2.7.a4 release - git tag 389-ds-base-1.2.7.a4
- Bug 647932 - multiple memberOf configuration adding memberOf where there is 
no member
- Bug 491733 - dbtest crashes
- Bug 606545 - core schema should include numSubordinates
- Bug 638773 - permissions too loose on pid and lock files
- Bug 189985 - Improve attribute uniqueness error message
- Bug 619623 - attr-unique-plugin ignores requiredObjectClass on modrdn operat
ions
- Bug 619633 - Make attribute uniqueness obey requiredObjectClass

* Wed Oct 27 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.4.a3
- 1.2.7.a3 release - a2 was never released - this is a rebuild to pick up
- Bug 644608 - RHDS 8.1->8.2 upgrade fails to properly migrate ACIs
- Adding the ancestorid fix code to ##upgradednformat.pl.

* Fri Oct 22 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.3.a3
- 1.2.7.a3 release - a2 was never released
- Bug 644608 - RHDS 8.1->8.2 upgrade fails to properly migrate ACIs
- Bug 629681 - Retro Changelog trimming does not behave as expected
- Bug 645061 - Upgrade: 06inetorgperson.ldif and 05rfc4524.ldif
-              are not upgraded in the server instance schema dir

* Tue Oct 19 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.2.a2
- 1.2.7.a2 release - a1 was the OpenLDAP testday release
- git tag 389-ds-base-1.2.7.a2
- added openldap support on platforms that use openldap with moznss
- for crypto (F-14 and later)
- many bug fixes
- Account Policy Plugin (keep track of last login, disable old accounts)

* Fri Oct  8 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.7-0.1.a1
- added openldap support

* Wed Sep 29 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6.1-3
- bump rel to rebuild again

* Mon Sep 27 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6.1-2
- bump rel to rebuild

* Thu Sep 23 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6.1-1
- This is the 1.2.6.1 release - git tag 389-ds-base-1.2.6.1
- Bug 634561 - Server crushes when using Windows Sync Agreement
- Bug 635987 - Incorrect sub scope search result with ACL containing ldap:///self
- Bug 612264 - ACI issue with (targetattr='userPassword')
- Bug 606920 - anonymous resource limit- nstimelimit - also applied to "cn=directory manager"
- Bug 631862 - crash - delete entries not in cache + referint

* Thu Aug 26 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-1
- This is the final 1.2.6 release

* Tue Aug 10 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.11.rc7
- 1.2.6 release candidate 7
- git tag 389-ds-base-1.2.6.rc7
- Bug 621928 - Unable to enable replica (rdn problem?) on 1.2.6 rc6

* Mon Aug  2 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.10.rc6
- 1.2.6 release candidate 6
- git tag 389-ds-base-1.2.6.rc6
- Bug 617013 - repl-monitor.pl use cpu upto 90%
- Bug 616618 - 389 v1.2.5 accepts 2 identical entries with different DN formats
- Bug 547503 - replication broken again, with 389 MMR replication and TCP errors
- Bug 613833 - Allow dirsrv_t to bind to rpc ports
- Bug 612242 - membership change on DS does not show on AD
- Bug 617629 - Missing aliases in new schema files
- Bug 619595 - Upgrading sub suffix under non-normalized suffix disappears
- Bug 616608 - SIGBUS in RDN index reads on platforms with strict alignments
- Bug 617862 - Replication: Unable to delete tombstone errors
- Bug 594745 - Get rid of dirsrv_lib_t label

* Wed Jul 14 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.9.rc3
- make selinux-devel explicit Require the base package in order
- to comply with Fedora Licensing Guidelines

* Thu Jul  1 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.8.rc3
- 1.2.6 release candidate 3
- git tag 389-ds-base-1.2.6.rc3
- Bug 603942 - null deref in _ger_parse_control() for subjectdn
- 609256  - Selinux: pwdhash fails if called via Admin Server CGI
- 578296  - Attribute type entrydn needs to be added when subtree rename switch is on
- 605827 - In-place upgrade: upgrade dn format should not run in setup-ds-admin.pl
- Bug 604453 - SASL Stress and Server crash: Program quits with the assertion failure in PR_Poll
- Bug 604453 - SASL Stress and Server crash: Program quits with the assertion failure in PR_Poll
- 606920 - anonymous resource limit - nstimelimit - also applied to "cn=directory manager"

* Wed Jun 16 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.7.rc2
- 1.2.6 release candidate 2

* Mon Jun 14 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.6-0.6.rc1
- install replication session plugin header with devel package

* Wed Jun  9 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.5.rc1
- 1.2.6 release candidate 1

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1.2.6-0.4.a4.1
- Mass rebuild with perl-5.12.0

* Wed May 26 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.4.a4
- 1.2.6.a4 release

* Wed Apr  7 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.6-0.4.a3
- 1.2.6.a3 release
- add managed entries plug-in
- many bug fixes
- moved selinux subpackage into base package

* Fri Apr  2 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.6-0.3.a2
- rebuild for icu 4.4

* Tue Mar  2 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.6-0.2.a2
- 1.2.6.a2 release
- add support for matching rules
- many bug fixes

* Thu Jan 14 2010 Nathan Kinder <nkinder@redhat.com> - 1.2.6-0.1.a1
- 1.2.6.a1 release
- Added SELinux policy and subpackages

* Tue Jan 12 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.5-1
- 1.2.5 final release

* Mon Jan  4 2010 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.5.rc4
- 1.2.5.rc4 release

* Thu Dec 17 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.4.rc3
- 1.2.5.rc3 release

* Mon Dec  7 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.3.rc2
- 1.2.5.rc2 release

* Wed Dec  2 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.2.rc1
- 1.2.5.rc1 release

* Thu Nov 12 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.5-0.1.a1
- 1.2.5.a1 release

* Thu Oct 29 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.4-1
- 1.2.4 release
- resolves bug 221905 - added support for Salted MD5 (SMD5) passwords - primarily for migration
- resolves bug 529258 - Make upgrade remove obsolete schema from 99user.ldif

* Mon Sep 14 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.3-1
- 1.2.3 release
- added template-initconfig to %files
- %posttrans now runs update to update the server instances
- servers are shutdown, then restarted if running before install
- scriptlets mostly use lua now to pass data among scriptlet phases

* Tue Sep 01 2009 Caolán McNamara <caolanm@redhat.com> - 1.2.2-2
- rebuild with new openssl to fix dependencies

* Tue Aug 25 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.2-1
- backed out - added template-initconfig to %files - this change is for the next major release
- bump version to 1.2.2
- fix reopened 509472 db2index all does not reindex all the db backends correctly
- fix 518520 -  pre hashed salted passwords do not work
- see https://bugzilla.redhat.com/show_bug.cgi?id=518519 for the list of
- bugs fixed in 1.2.2

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.1-5
- rebuilt with new openssl

* Wed Aug 19 2009 Noriko Hosoi <nhosoi@redhat.com> - 1.2.1-4
- added template-initconfig to %files

* Wed Aug 12 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.1-3
- added BuildRequires pcre

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.1-1
- change name to 389
- change version to 1.2.1
- added initial support for numeric string syntax
- added initial support for syntax validation
- added initial support for paged results including sorting

* Tue Apr 28 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.0-4
- final release 1.2.0
- Resolves: bug 475338 - LOG: the intenal type of maxlogsize, maxdiskspace and minfreespace should be 64-bit integer
- Resolves: bug 496836 - SNMP ldap-agent on Solaris: Unable to open semaphore for server: 389
- CVS tag: FedoraDirSvr_1_2_0 FedoraDirSvr_1_2_0_20090428

* Mon Apr  6 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.0-3
- re-enable ppc builds

* Thu Apr  2 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.0-2
- exclude ppc builds - needs extensive porting work

* Mon Mar 30 2009 Rich Megginson <rmeggins@redhat.com> - 1.2.0-1
- new release 1.2.0
- Made devel package depend on mozldap-devel
- only create run dir if it does not exist
- CVS tag: FedoraDirSvr_1_2_0_RC1 FedoraDirSvr_1_2_0_RC1_20090330

* Thu Oct 30 2008 Noriko Hosoi <nhosoi@redhat.com> - 1.1.3-7
- added db4-utils to Requires for verify-db.pl

* Mon Oct 13 2008 Noriko Hosoi <nhosoi@redhat.com> - 1.1.3-6
- Enabled LDAPI autobind

* Thu Oct  9 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-5
- updated update to patch bug463991-bdb47.patch

* Thu Oct  9 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-4
- updated patch bug463991-bdb47.patch

* Mon Sep 29 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-3
- added patch bug463991-bdb47.patch
- make ds work with bdb 4.7

* Wed Sep 24 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-2
- rolled back bogus winsync memory leak fix

* Tue Sep 23 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.3-1
- winsync api improvements for modify operations

* Fri Jun 13 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.2-1
- This is the 1.1.2 release.  The bugs fixed can be found here
- https://bugzilla.redhat.com/showdependencytree.cgi?id=452721
- Added winsync-plugin.h to the devel subpackage

* Fri Jun  6 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.1-2
- bump rev to rebuild and pick up new version of ICU

* Fri May 23 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.1-1
- 1.1.1 release candidate - several bug fixes

* Wed Apr 16 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.0.1-4
- fix bugzilla 439829 - patch to allow working with NSS 3.11.99 and later

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.0.1-3
- add patch to allow server to work with NSS 3.11.99 and later
- do NSS_Init after fork but before detaching from console

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.1.0.1-3
- add Requires for versioned perl (libperl.so)

* Wed Feb 27 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.0.1-2
- previous fix for 434403 used the wrong patch
- this is the right one

* Wed Feb 27 2008 Rich Megginson <rmeggins@redhat.com> - 1.1.0.1-1
- Resolves bug 434403 - GCC 4.3 build fails
- Rolled new source tarball which includes Nathan's fix for the struct ucred
- NOTE: Change version back to 1.1.1 for next release
- this release was pulled from CVS tag FedoraDirSvr110_gcc43

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.0-5
- Autorebuild for GCC 4.3

* Thu Dec 20 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-4
- This is the GA release of Fedora DS 1.1
- Removed version numbers for BuildRequires and Requires
- Added full URL to source tarball

* Fri Dec 07 2007 Release Engineering <rel-eng at fedoraproject dot org> - 1.1.0-3
- Rebuild for deps

* Wed Nov  7 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-2.0
- This is the beta2 release
- new file added to package - /etc/sysconfig/dirsrv - for setting
- daemon environment as is usual in other linux daemons

* Thu Aug 16 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.2
- fix build breakage due to open()
- mock could not find BuildRequires: db4-devel >= 4.2.52
- mock works if >= version is removed - it correctly finds db4.6

* Fri Aug 10 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.1
- Change pathnames to use the pkgname macro which is dirsrv
- get rid of cvsdate in source name

* Fri Jul 20 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.3.20070720
- Added Requires for perldap, cyrus sasl plugins
- Removed template-migrate* files
- Added perl module directory
- Removed install.inf - setup-ds.pl can now easily generate one

* Mon Jun 18 2007 Nathan Kinder <nkinder@redhat.com> - 1.1.0-0.2.20070320
- added requires for mozldap-tools

* Tue Mar 20 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.1.20070320
- update to latest sources
- added migrateTo11 to allow migrating instances from 1.0.x to 1.1
- ldapi support
- fixed pam passthru plugin ENTRY method

* Fri Feb 23 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.1.20070223
- Renamed package to fedora-ds-base, but keep names of paths/files/services the same
- use the shortname macro (fedora-ds) for names of paths, files, and services instead
- of name, so that way we can continue to use e.g. /etc/fedora-ds instead of /etc/fedora-ds-base
- updated to latest sources

* Tue Feb 13 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-0.1.20070213
- More cleanup suggested by Dennis Gilmore
- This is the fedora extras candidate based on cvs tag FedoraDirSvr110a1

* Fri Feb  9 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.el4.20070209
- latest sources
- added init scripts
- use /etc as instconfigdir

* Wed Feb  7 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.el4.20070207
- latest sources
- moved all executables to _bindir

* Mon Jan 29 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.el4.20070129
- latest sources
- added /var/tmp/fedora-ds to dirs

* Fri Jan 26 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-8.el4.20070125
- added logconv.pl
- added slapi-plugin.h to devel package
- added explicit dirs for /var/log/fedora-ds et. al.

* Thu Jan 25 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-7.el4.20070125
- just move all .so files into the base package from the devel package

* Thu Jan 25 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-6.el4.20070125
- Move the plugin *.so files into the main package instead of the devel
- package because they are loaded directly by name via dlopen

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-5.el4.20070125
- Move the script-templates directory to datadir/fedora-ds

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-4.el4.20070119
- change mozldap to mozldap6

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-3.el4.20070119
- remove . from cvsdate define

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-2.el4.20070119
- Having a problem building in Brew - may be Release format

* Fri Jan 19 2007 Rich Megginson <rmeggins@redhat.com> - 1.1.0-1.el4.cvs20070119
- Changed version to 1.1.0 and added Release 1.el4.cvs20070119
- merged in changes from Fedora Extras candidate spec file

* Mon Jan 15 2007 Rich Megginson <rmeggins@redhat.com> - 1.1-0.1.cvs20070115
- Bump component versions (nspr, nss, svrcore, mozldap) to their latest
- remove unneeded patches

* Tue Jan 09 2007 Dennis Gilmore <dennis@ausil.us> - 1.1-0.1.cvs20070108
- update to a cvs snapshot
- fedorafy the spec 
- create -devel subpackage
- apply a patch to use mozldap not mozldap6
- apply a patch to allow --prefix to work correctly

* Mon Dec 4 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-16
- Fixed the problem where the server would crash upon shutdown in dblayer
- due to a race condition among the database housekeeping threads
- Fix a problem with normalized absolute paths for db directories

* Tue Nov 28 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-15
- Touch all of the ldap/admin/src/scripts/*.in files so that they
- will be newer than their corresponding script template files, so
- that make will rebuild them.

* Mon Nov 27 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-14
- Chown new schema files when copying during instance creation

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-13
- Configure will get ldapsdk_bindir from pkg-config, or $libdir/mozldap6

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-12
- use eval to sed ./configure into ../configure

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-11
- jump through hoops to be able to run ../configure

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-10
- Need to make built dir in setup section

* Tue Nov 21 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-9
- The template scripts needed to use @libdir@ instead of hardcoding
- /usr/lib
- Use make DESTDIR=$RPM_BUILD_ROOT install instead of % makeinstall
- do the actual build in a "built" subdirectory, until we remove
- the old script templates

* Thu Nov 16 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-8
- Make replication plugin link with libdb

* Wed Nov 15 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-7
- Have make define LIBDIR, BINDIR, etc. for C code to use
- especially for create_instance.h

* Tue Nov 14 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-6
- Forgot to checkin new config.h.in for AC_CONFIG_HEADERS

* Tue Nov 14 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-5
- Add perldap as a Requires; update sources

* Thu Nov 9 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-4
- Fix ds_newinst.pl
- Remove obsolete #defines

* Thu Nov 9 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-3
- Update sources; rebuild to populate brew yum repo with dirsec-nss

* Tue Nov 7 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-2
- Update sources

* Thu Nov 2 2006 Rich Megginson <rmeggins@redhat.com> - 1.0.99-1
- initial revision
