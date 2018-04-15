Summary: A set of basic GNU tools commonly used in shell scripts
Name:    coreutils
Version: 8.22
Release: 21%{?dist}
License: GPLv3+
Group:   System Environment/Base
Url:     http://www.gnu.org/software/coreutils/
Source0: ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tar.xz
Source101:  coreutils-DIR_COLORS
Source102:  coreutils-DIR_COLORS.lightbgcolor
Source103:  coreutils-DIR_COLORS.256color
Source105:  coreutils-colorls.sh
Source106:  coreutils-colorls.csh

# From upstream
#Fix segfault in cp (in selinux context code)
Patch1: coreutils-8.22-cp-selinux.patch
#Mark veritas filesystem as remote (use polling)
Patch2: coreutils-8.22-vxfs-noinotify.patch
#Fix sparse test on xfs and btrfs filesystems
Patch3: coreutils-8.22-xfs-tests.patch
#Add dd option for progress reporting
Patch4: coreutils-8.22-dd-progress.patch
#Separate -Z and --context options where necessary in --help and manpage
Patch5: coreutils-8.22-selinux-optionsseparate.patch
#Handle du bindmount cycles more gracefully
Patch6: coreutils-8.22-du-bindmountcycles.patch
#Prevent possible race condition for hardlinks in mv
Patch7: coreutils-8.22-mv-hardlinksrace.patch
#Use new version of getdisk function in df (better results)
Patch8: coreutils-8.22-df-getdisk.patch
#Use new version of find_mount_list function
Patch9: coreutils-8.22-df-filtermountlistupdate.patch
#Prevent potential corruption of sparse files in cp
Patch10: coreutils-8.22-cp-sparsecorrupt.patch
#improve dirent d_type support verification (xfs build failure, #1263341)
Patch11: coreutils-8.22-xfsbuildfailure.patch
#Update filesystem magic lists from latest upstream (coreutils-8.25)
Patch12: coreutils-8.22-newfilesystems.patch
#Fix crash in date with empty TZ envvar
Patch13: coreutils-8.22-date-emptyTZ.patch
#df -l: do not hang on a dead autofs mount point (#1309247)
Patch14: coreutils-8.22-df-autofs.patch 

# ls: allow interruption when reading slow directories (#1421802)
Patch15: coreutils-8.22-ls-interruption.patch

# df: do not stat file systems that do not satisfy the -t/-x args (#1511947)
Patch17: coreutils-8.22-df-stat.patch

# Our patches
#general patch to workaround koji build system issues
Patch100: coreutils-6.10-configuration.patch
#add note about no difference between binary/text mode on Linux - md5sum manpage
Patch101: coreutils-6.10-manpages.patch
#temporarily workaround probable kernel issue with TCSADRAIN(#504798)
Patch102: coreutils-7.4-sttytcsadrain.patch
#do display processor type for uname -p/-i based on uname(2) syscall
Patch103: coreutils-8.2-uname-processortype.patch
#df --direct
Patch104: coreutils-df-direct.patch
#add note about mkdir --mode behaviour into info documentation(#610559)
Patch107: coreutils-8.4-mkdir-modenote.patch
#fix gnulib tests on ppc64le
Patch108: coreutils-8.22-ppc64le.patch
#fix groups for session in id
Patch109: coreutils-8.22-id-groups.patch
#fix some non-default tests failing in beaker environment(#1247641)
Patch110: coreutils-8.22-non-defaulttests.patch
#Fix sort -h for other than first field
Patch111: coreutils-8.22-sort-blanks.patch

# sh-utils
#add info about TZ envvar to date manpage
Patch703: sh-utils-2.0.11-dateman.patch
Patch713: coreutils-4.5.3-langinfo.patch

# (sb) lin18nux/lsb compliance - multibyte functionality patch
Patch800: coreutils-i18n.patch

# fold: preserve new-lines in mutlibyte text (#1418505)
Patch801: coreutils-i18n-fold-newline.patch

#getgrouplist() patch from Ulrich Drepper.
Patch908: coreutils-getgrouplist.patch
#Prevent buffer overflow in who(1) (bug #158405).
Patch912: coreutils-overflow.patch
#Temporarily disable df symlink test, failing
Patch913: coreutils-8.22-temporarytestoff.patch
#Disable id/setgid.sh test, fix false positive failure of cp-a-selinux test 
# (#1266501, #1266500)
Patch914: coreutils-8.22-failingtests.patch

#SELINUX Patch - implements Redhat changes
#(upstream did some SELinux implementation unlike with RedHat patch)
Patch950: coreutils-selinux.patch
Patch951: coreutils-selinuxmanpages.patch

#Disable duplicate files test for mock
Patch1000: 0001-disable-test-for-mock-builds.patch


Conflicts: filesystem < 3
Provides: /bin/basename
Provides: /bin/cat
Provides: /bin/chgrp
Provides: /bin/chmod
Provides: /bin/chown
Provides: /bin/cp
Provides: /bin/cut
Provides: /bin/date
Provides: /bin/dd
Provides: /bin/df
Provides: /bin/echo
Provides: /bin/env
Provides: /bin/false
Provides: /bin/ln
Provides: /bin/ls
Provides: /bin/mkdir
Provides: /bin/mknod
Provides: /bin/mktemp
Provides: /bin/mv
Provides: /bin/nice
Provides: /bin/pwd
Provides: /bin/readlink
Provides: /bin/rm
Provides: /bin/rmdir
Provides: /bin/sleep
Provides: /bin/sort
Provides: /bin/stty
Provides: /bin/sync
Provides: /bin/touch
Provides: /bin/true
Provides: /bin/uname

BuildRequires: libselinux-devel
BuildRequires: libacl-devel
BuildRequires: gettext bison
BuildRequires: texinfo
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libcap-devel
BuildRequires: libattr-devel
BuildRequires: openssl-devel
BuildRequires: gmp-devel
BuildRequires: attr
BuildRequires: strace

Requires(pre): /sbin/install-info
Requires(preun): /sbin/install-info
Requires(post): /sbin/install-info
Requires(post): grep
Requires:       ncurses
Requires:       gmp

Provides: fileutils = %{version}-%{release}
Provides: sh-utils = %{version}-%{release}
Provides: stat = %{version}-%{release}
Provides: textutils = %{version}-%{release}
#old mktemp package had epoch 3, so we have to use 4 for coreutils
Provides: mktemp = 4:%{version}-%{release}
Provides: bundled(gnulib)
Obsoletes: mktemp < 4:%{version}-%{release}
Obsoletes: fileutils <= 4.1.9
Obsoletes: sh-utils <= 2.0.12
Obsoletes: stat <= 3.3
Obsoletes: textutils <= 2.0.21
#coreutils-libs dropped in f17
Obsoletes: coreutils-libs < 8.13

%description
These are the GNU core utilities.  This package is the combination of
the old GNU fileutils, sh-utils, and textutils packages.

%prep
%setup -q

# From upstream
%patch1 -p1 -b .nullcontext
%patch2 -p1 -b .vxfs
%patch3 -p1 -b .xfs
%patch4 -p1 -b .progress
%patch6 -p1 -b .bindmount
%patch7 -p1 -b .race
%patch8 -p1 -b .getdisk
%patch9 -p1 -b .findmnt
%patch10 -p1 -b .sparse
%patch11 -p1 -b .d_type
%patch12 -p1 -b .newfs
%patch13 -p1 -b .emptytz
%patch14 -p1 -b .df-autofs

# Our patches
%patch100 -p1 -b .configure
%patch101 -p1 -b .manpages
%patch102 -p1 -b .tcsadrain
%patch103 -p1 -b .sysinfo
%patch104 -p1 -b .dfdirect
%patch107 -p1 -b .mkdirmode
%patch108 -p1 -b .ppc64le
%patch109 -p1 -b .groups
%patch110 -p1 -b .nondefault
%patch111 -p1 -b .blanks

# sh-utils
%patch703 -p1 -b .dateman
%patch713 -p1 -b .langinfo

# li18nux/lsb
%patch800 -p1 -b .i18n

# Coreutils
%patch908 -p1 -b .getgrouplist
%patch912 -p1 -b .overflow
%patch913 -p1 -b .testoff
%patch914 -p1 -b .testfail

#SELinux
%patch950 -p1 -b .selinux
%patch951 -p1 -b .selinuxman
%patch5 -p1 -b .separate

#aarch64/armhfp mock test
%patch1000 -p1 -b .mock

# patches added in RHEL-7.5
%patch801 -p1
%patch15  -p1
%patch17  -p1

chmod a+x tests/misc/sort-mb-tests.sh tests/df/direct.sh tests/cp/no-ctx.sh tests/dd/stats.sh || :

#fix typos/mistakes in localized documentation(#439410, #440056)
find ./po/ -name "*.p*" | xargs \
 sed -i \
 -e 's/-dpR/-cdpR/'

%build
export CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing -fpic"
%{expand:%%global optflags %{optflags} -D_GNU_SOURCE=1}
#autoreconf -i -v
touch aclocal.m4 configure config.hin Makefile.in */Makefile.in
aclocal -I m4
autoconf --force
automake --copy --add-missing
%configure --enable-largefile \
           --with-openssl=optional ac_cv_lib_crypto_MD5=no \
           --enable-install-program=hostname,arch \
           --with-tty-group \
           DEFAULT_POSIX2_VERSION=200112 alternative=199209 || :

# Regenerate manpages
touch man/*.x
# Do not regenerate fs-is-local.h
touch src/fs-is-local.h

make all %{?_smp_mflags}

# XXX docs should say /var/run/[uw]tmp not /etc/[uw]tmp
sed -i -e 's,/etc/utmp,/var/run/utmp,g;s,/etc/wtmp,/var/run/wtmp,g' doc/coreutils.texi

%check
make check

%install
make DESTDIR=$RPM_BUILD_ROOT install

# man pages are not installed with make install
make mandir=$RPM_BUILD_ROOT%{_mandir} install-man

# fix japanese catalog file
if [ -d $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES ]; then
   mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/ja/LC_MESSAGES
   mv $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC/LC_MESSAGES/*mo \
      $RPM_BUILD_ROOT%{_datadir}/locale/ja/LC_MESSAGES
   rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/ja_JP.EUC
fi

bzip2 -9f ChangeLog

# let be compatible with old fileutils, sh-utils and textutils packages :
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}

# chroot was in /usr/sbin :
mv $RPM_BUILD_ROOT{%_bindir,%_sbindir}/chroot

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -p -c -m644 %SOURCE101 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS
install -p -c -m644 %SOURCE102 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS.lightbgcolor
install -p -c -m644 %SOURCE103 $RPM_BUILD_ROOT%{_sysconfdir}/DIR_COLORS.256color
install -p -c -m644 %SOURCE105 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.sh
install -p -c -m644 %SOURCE106 $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/colorls.csh

# These come from util-linux and/or procps.
for i in hostname uptime kill ; do
    rm $RPM_BUILD_ROOT{%{_bindir}/$i,%{_mandir}/man1/$i.1}
done

# Compress ChangeLogs from before the fileutils/textutils/etc merge
bzip2 -f9 old/*/C*

# Use hard links instead of symbolic links for LC_TIME files (bug #246729).
find %{buildroot}%{_datadir}/locale -type l | \
(while read link
 do
   target=$(readlink "$link")
   rm -f "$link"
   ln "$(dirname "$link")/$target" "$link"
 done)

%find_lang %name

# (sb) Deal with Installed (but unpackaged) file(s) found
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%pre
# We must deinstall these info files since they're merged in
# coreutils.info. else their postun'll be run too late
# and install-info will fail badly because of duplicates
for file in sh-utils textutils fileutils; do
  if [ -f %{_infodir}/$file.info.gz ]; then
    /sbin/install-info --delete %{_infodir}/$file.info.gz --dir=%{_infodir}/dir &> /dev/null || :
  fi
done

%preun
if [ $1 = 0 ]; then
  if [ -f %{_infodir}/%{name}.info.gz ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
  fi
fi

%post
%{_bindir}/grep -v '(sh-utils)\|(fileutils)\|(textutils)' %{_infodir}/dir > \
  %{_infodir}/dir.rpmmodify || exit 0
    /bin/mv -f %{_infodir}/dir.rpmmodify %{_infodir}/dir
if [ -f %{_infodir}/%{name}.info.gz ]; then
  /sbin/install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
%dir %{_datadir}/locale/*/LC_TIME
%config(noreplace) %{_sysconfdir}/DIR_COLORS*
%config(noreplace) %{_sysconfdir}/profile.d/*
%doc COPYING ABOUT-NLS ChangeLog.bz2 NEWS README THANKS TODO old/*
%{_bindir}/arch
%{_bindir}/basename
%{_bindir}/cat
%{_bindir}/chgrp
%{_bindir}/chmod
%{_bindir}/chown
%{_bindir}/cp
%{_bindir}/cut
%{_bindir}/date
%{_bindir}/dd
%{_bindir}/df
%{_bindir}/echo
%{_bindir}/env
%{_bindir}/false
%{_bindir}/link
%{_bindir}/ln
%{_bindir}/ls
%{_bindir}/mkdir
%{_bindir}/mknod
%{_bindir}/mv
%{_bindir}/nice
%{_bindir}/pwd
%{_bindir}/readlink
%{_bindir}/rm
%{_bindir}/rmdir
%{_bindir}/sleep
%{_bindir}/sort
%{_bindir}/stty
%{_bindir}/sync
%{_bindir}/mktemp
%{_bindir}/touch
%{_bindir}/true
%{_bindir}/uname
%{_bindir}/unlink
%{_bindir}/[
%{_bindir}/base64
%{_bindir}/chcon
%{_bindir}/cksum
%{_bindir}/comm
%{_bindir}/csplit
%{_bindir}/dir
%{_bindir}/dircolors
%{_bindir}/dirname
%{_bindir}/du
%{_bindir}/expand
%{_bindir}/expr
%{_bindir}/factor
%{_bindir}/fmt
%{_bindir}/fold
%{_bindir}/groups
%{_bindir}/head
%{_bindir}/hostid
%{_bindir}/id
%{_bindir}/install
%{_bindir}/join
%{_bindir}/logname
%{_bindir}/md5sum
%{_bindir}/mkfifo
%{_bindir}/nl
%{_bindir}/nohup
%{_bindir}/nproc
%{_bindir}/numfmt
%{_bindir}/od
%{_bindir}/paste
%{_bindir}/pathchk
%{_bindir}/pinky
%{_bindir}/pr
%{_bindir}/printenv
%{_bindir}/printf
%{_bindir}/ptx
%{_bindir}/realpath
%{_bindir}/runcon
%{_bindir}/seq
%{_bindir}/sha1sum
%{_bindir}/sha224sum
%{_bindir}/sha256sum
%{_bindir}/sha384sum
%{_bindir}/sha512sum
%{_bindir}/shred
%{_bindir}/shuf
%{_bindir}/split
%{_bindir}/stat
%{_bindir}/stdbuf
%{_bindir}/sum
%{_bindir}/tac
%{_bindir}/tail
%{_bindir}/tee
%{_bindir}/test
%{_bindir}/timeout
%{_bindir}/tr
%{_bindir}/truncate
%{_bindir}/tsort
%{_bindir}/tty
%{_bindir}/unexpand
%{_bindir}/uniq
%{_bindir}/users
%{_bindir}/vdir
%{_bindir}/wc
%{_bindir}/who
%{_bindir}/whoami
%{_bindir}/yes
%{_infodir}/coreutils*
%{_libexecdir}/coreutils*
%{_mandir}/man*/*
%{_sbindir}/chroot

%changelog
* Sun Apr 15 2018 Fabian Arrotin <arrfab@centos.org> - 8.22-21
- add patch to disable skipduplicates test in mock

* Mon Dec 04 2017 Kamil Dudka <kdudka@redhat.com> - 8.22-21
- timeout: revert the last fix for a possible race (#1439465)

* Thu Nov 23 2017 Kamil Dudka <kdudka@redhat.com> - 8.22-20
- df: do not stat file systems that do not satisfy the -t/-x args (#1511947)

* Thu Sep 21 2017 Kamil Dudka <kdudka@redhat.com> - 8.22-19
- timeout: fix race possibly terminating wrong process (#1439465)
- ls: allow interruption when reading slow directories (#1421802)
- fold: preserve new-lines in mutlibyte text (#1418505)

* Fri Jul 01 2016 Ondrej Vasik <ovasik@redhat.com> - 8.22-18
- fix xfs build failure in chrooted environment (#1263341)
- update filesystem lists for stat and tail from latest upstream
  (#1327881, #1280357) 
- disable id/setgid.sh test(missing chroot feature), fix 
  cp-a-selinux test (#1266500,#1266501)
- colorls.sh - change detection of interactive shell for ksh
  compatibility (#1321648)
- fix date --date crash with empty or invalid TZ envvar (#1325786)
- df -l: do not hang on a dead autofs mount point (#1309247)
- sort -h: fix functionality of human readable numeric sort for other
  than first field (#1328360)

* Wed Nov 25 2015 Ondrej Vasik <ovasik@redhat.com> - 8.22-16
- cp: prevent potential sparse file corruption (#1284906)

* Sat Sep 12 2015 Ondrej Vasik <ovasik@redhat.com> - 8.22-15
- fix one more occurance of non-full path in colorls.sh (#1222223)

* Mon Aug 17 2015 Ondrej Vasik <ovasik@redhat.com> - 8.22-14
- fix several failing non-default(root,expensive) tests (#1247641)

* Mon Jul 06 2015 Ondrej Vasik <ovasik@redhat.com> - 8.22-13
- call utilities in colorls.* scripts with full path (#1222223)
- tail: disable inotify in --follow for vxfs (#1109083)
- remove circular dependency for util-linux (not relevant for RHEL 7 - #1155963)
- sort: do not look at more than specified keys for mb locales (#1148347)
- i18n patch: fix buffer overruns and compiler warnings (#1148347)
- xfs: fix dd sparse false test failure on btrfs and xfs (#1223041)
- dd: new status=progress level to print stats periodically (#1147701)
- id/groups - print correct group for session (#1115430)
- cp,install,mknod,mkfifo,mkdir: separate -Z and --context options
  in --help and manpage (#1084471)
- ls: clarify --scontext/--context/--lcontext options behaviour
  in info documentation, mention deprecation (#1099508)
- du: handle bindmount cycles more gracefully (#1238191)
- mv: prevent possible race condition for hardlinks (#1166570)
- df: improve filtering of NFS mounts and bind mounts
  (#1197463, #1100026, #1129661)

* Tue Aug 05 2014 Ondrej Vasik <ovasik@redhat.com> - 8.22-12
- fix test failure on ppc64le (#1112687)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 8.22-11
- Mass rebuild 2014-01-24

* Mon Jan 13 2014 Ondrej Vasik <ovasik@redhat.com> 8.22-10
- cp/mv/install: do not crash when getfscreatecon() is
  returning a NULL context
- fix the cut optimizations to UTF-8 locales only
- unset the unnecessary envvars after colorls scripts

* Fri Jan 10 2014 Ondrej Oprala <ooprala@redhat.com> 8.22-9
- Only use cut optimizations for UTF-8 locales (#1021403)

* Mon Jan 06 2014 Ondrej Oprala <ooprala@redhat.com> 8.22-8
- Don't use cut mb path if not necessary (#1021403)

* Mon Jan 06 2014 Ondrej Oprala <ooprala@redhat.com> 8.22-7
- Fix sorting by non-first field (#1003544)

* Fri Jan 03 2014 Ondrej Vasik <ovasik@redhat.com> 8.22-5
- do not modify SELinux contexts of existing parent
  directories when copying files (fix by P.Brady, #1045122)

* Fri Jan 03 2014 Ondrej Oprala <ooprala@redat.com> 8.22-4
- revert an old sort change and constrict it's condition

* Thu Jan 02 2014 Ondrej Vasik <ovasik@redhat.com> 8.22-3
- mark deprecated SELinux related downstream options as
  deprecated in usage/man
- temporarily disable setting SELinux contexts recursively
  for existing directories - broken (#1045122)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 8.22-2
- Mass rebuild 2013-12-27

* Tue Dec 17 2013 Ondrej Vasik <ovasik@redhat.com> 8.22-1
- new upstream version 8.22 (#1043552)
- temporarily df symlink test (incomplete upstream fix, not
  regression)
- enable build with openssl for better performance of
  HASHsum utilities (not for md5sum because of FIPS)
- turn on the multibyte path in the testsuite to cover
  i18n regressions
- fix possible colorls.csh script errors for tcsh with
  noclobber set and entered include file

* Thu Nov 28 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-14
- mv: fails to overwrite directory on cross-filesystem
  copy with EISDIR (#1035224)
- tail -F does not handle dead symlinks gracefully
  (#1035219)

* Mon Oct 14 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-13
- cp: correct error message for invalid arguments
  of '--no-preserve' (#1018206)

* Thu Aug 15 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-12
- pr -e, with a mix of backspaces and TABs, could corrupt the heap
  in multibyte locales (analyzed by J.Koncicky)
- Fix sort multibyte incompatibilities (by O.Oprala)
- change the TMP variable name in colorls.csh to _tmp (#981373)
- optimization of colorls scripts by Ville Skytta (#961012)

* Fri Apr 05 2013 Ondrej Oprala <ooprala@redhat.com 8.21-11
- Fix tmp file location in colorls scripts (#948008)

* Thu Mar 14 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-10
- DIR_COLORS.$TERM should have higher priority than
  DIR_COLORS.256color (#921651)

* Mon Mar 11 2013 Ondrej Oprala <ooprala@redhat.com> 8.21-9
- add support for INCLUDE in colorls scripts (#818069)

* Mon Mar 04 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-8
- fix factor on AArch64 (M.Salter, #917735)

* Fri Mar 01 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-7
- ls: colorize several new archive/compressed types (#868510)

* Sat Feb 23 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-6
- install: do proper cleanup when strip fails
  (O.Oprala, B.Voekler, #632444)

* Wed Feb 20 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-5
- fix multibyte issue in unexpand(by R.Kollar, #821262)

* Mon Feb 18 2013 Ondrej Oprala <ooprala@redhat.com> 8.21-4
- fix sort-mb-tests.sh test (B.Voelker)

* Mon Feb 18 2013 Mark Wielaard <mjw@redhat.com> 8.21-3
- fix coreutils-i18n.patch to terminate mbdelim string (#911929)

* Mon Feb 18 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-2
- remove unnecessary powerpc factor patch

* Fri Feb 15 2013 Ondrej Vasik <ovasik@redhat.com> 8.21-1
- new upstream release 8.21, update patches

* Thu Feb 07 2013 Ondrej Oprala <ooprala@redhat.com> 8.20-8
- add missing sort-mb-tests.sh to local.mk

* Tue Feb 05 2013 Ondrej Vasik <ovasik@redhat.com> 8.20-7
- add support for DTR/DSR control flow in stty(#445213)

* Wed Jan 23 2013 Ondrej Vasik <ovasik@redhat.com> 8.20-6
- fix multiple segmantation faults in i18n patch (by SUSE)
  (#869442, #902917)

* Thu Dec 20 2012 Ondrej Vasik <ovasik@redhat.com> 8.20-5
- seq: fix newline output when -s specified (upstream)

* Mon Dec 10 2012 Ondrej Vasik <ovasik@redhat.com> 8.20-4
- fix showing duplicates in df (#709351, O.Oprala, B.Voelker)

* Thu Dec 06 2012 Ondrej Vasik <ovasik@redhat.com> 8.20-3
- fix factor on 32bit powerpc (upstream, #884715)

* Mon Nov 05 2012 Ondrej Vasik <ovasik@redhat.com> 8.20-2
- disable the temporary O_SYNC fix (glibc is fixed - #872366)

* Sat Oct 27 2012 Ondrej Vasik <ovasik@redhat.com> 8.20-1
- new upstream release 8.20
- Temporarily require util-linux >= 2.22.1-3 (to prevent missing
  su/runuser on system)

* Mon Aug 20 2012 Ondrej Vasik <ovasik@redhat.com> 8.19-1
- new upstream release 8.19
- fix multibyte issues in cut and expand (M.Briza, #821260)

* Sun Aug 12 2012 Ondrej Vasik <ovasik@redhat.com> 8.18-1
- new upstream release 8.18
- su/runuser moved to util-linux

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 15 2012 Ondrej Vasik <ovasik@redhat.com> 8.17-3
- add virtual provides for bundled(gnulib) copylib (#821748)

* Fri May 11 2012 Ondrej Vasik <ovasik@redhat.com> 8.17-2
- ls: upstream fix - correctly show symlinks in /

* Fri May 11 2012 Ondrej Vasik <ovasik@redhat.com> 8.17-1
- new upstream release 8.17

* Fri May 04 2012 Ondrej Vasik <ovasik@redhat.com> 8.16-3
- add .htm and .shtml to colorized DIR_COLORS document
  type (#817218)

* Mon Apr 16 2012 Ondrej Vasik <ovasik@redhat.com> 8.16-2
- fix the tcsh colorls.csh behaviour in non-interactive
  mode (#804604)

* Mon Mar 26 2012 Ondrej Vasik <ovasik@redhat.com> 8.16-1
- new upstream release 8.16
- defuzz patches, remove already applied patches

* Thu Mar 08 2012 Ondrej Vasik <ovasik@redhat.com> 8.15-8
- fix regression in du -x with nondir argument (by J.Meyering)

* Wed Mar 07 2012 Ondrej Vasik <ovasik@redhat.com> 8.15-7
- fix sort segfault with multibyte locales (by P.Brady)

* Fri Feb 10 2012 Harald Hoyer <harald@redhat.com> 8.15-6
- turn on testsuite again

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 8.15-5
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 8.15-4
- add missing provides for the /usr-move

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 8.15-3
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Mon Jan 16 2012 Kamil Dudka <kdudka@redhat.com> - 8.15-2
- fix stack smashing, buffer overflow, and invalid output of pr (#772172)

* Sat Jan 07 2012 Ondrej Vasik <ovasik@redhat.com> - 8.15-1
- new upstream release 8.15

* Thu Jan 05 2012 Ondrej Vasik <ovasik@redhat.com> - 8.14-6
- do not use shebang in sourced colorls.csh

* Thu Jan 05 2012 Ondrej Vasik <ovasik@redhat.com> - 8.14-5
- fix pr -c and pr -v segfault with multibyte locales

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 8.14-4
- rebuild (gmp), last time, I promise

* Mon Oct 24 2011 Ondrej Vasik <ovasik@redhat.com> - 8.14-3
- require at least pam 1.1.3-7 (#748215)

* Thu Oct 20 2011 Ondrej Vasik <ovasik@redhat.com> - 8.14-2
- rebuild for gmp

* Wed Oct 12 2011 Ondrej Vasik <ovasik@redhat.com> - 8.14-1
- new upstream release 8.14

* Mon Sep 26 2011 Peter Schiffer <pschiffe@redhat.com> - 8.13-2.2
- rebuild with new gmp

* Mon Sep 12 2011 Ondrej Vasik <ovasik@redhat.com> - 8.13-2
- Obsolete coreutils-libs (#737287)

* Fri Sep 09 2011 Ondrej Vasik <ovasik@redhat.com> - 8.13-1
- new upstream release 8.13
- temporarily disable recently added multibyte checks in
  misc/cut test
- fix the SUSE fix for cut output-delimiter
- drop coreutils-libs subpackage, no longer needed

* Mon Sep 05 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-7
- incorporate some i18n patch fixes from OpenSUSE:
  - fix cut output-delimiter option
  - prevent infinite loop in sort when ignoring chars
  - prevent using unitialized variable in cut

* Tue Aug 23 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-6
- su: fix shell suspend in tcsh (#597928)

* Thu Aug 18 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-5
- variable "u" should be static in uname processor type patch

* Thu Aug 11 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-4
- deprecate non-upstream cp -Z/--context (install should be
  used instead of it), make it working if destination exists
  (#715557)

* Fri Jul 29 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-3
- use acl_extended_file_nofollow() if available (#692823)

* Fri Jul 15 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-2
- support ecryptfs mount of Private (postlogin into su.pamd)
  (#722323)

* Wed Apr 27 2011 Ondrej Vasik <ovasik@redhat.com> - 8.12-1
- new upstream release 8.12

* Thu Apr 14 2011 Ondrej Vasik <ovasik@redhat.com> - 8.11-2
- fix issue with df --direct(extra new line)

* Thu Apr 14 2011 Ondrej Vasik <ovasik@redhat.com> - 8.11-1
- new upstream release 8.11, defuzz patches

* Tue Mar 22 2011 Ondrej Vasik <ovasik@redhat.com> - 8.10-7
- add note about mkdir mode behaviour into info
  documentation (#610559)

* Mon Mar 14 2011 Ondrej Vasik <ovasik@redhat.com> - 8.10-6
- fix possible uninitalized variables usage caused by i18n
  patch(#683799)

* Fri Mar  4 2011 Ondrej Vasik <ovasik@redhat.com> - 8.10-5
- make coreutils build even without patches (with
  nopam, norunuser and noselinux variables)

* Thu Feb 17 2011 Ondrej Vasik <ovasik@redhat.com> - 8.10-4
- colorize documents by DIR_COLORS files(brown like mc)

* Thu Feb 17 2011 Ondrej Vasik <ovasik@redhat.com> - 8.10-3
- add several new TERMs to DIR_COLORS files(#678147)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 04 2011 Ondrej Vasik <ovasik@redhat.com> - 8.10-1
- new upstream release coreutils-8.10

* Sat Jan 08 2011 Dennis Gilmore <dennis@ausil.us> - 8.9-2
- drop no longer needed mkstemp patch for sparc 

* Tue Jan 04 2011 Ondrej Vasik <ovasik@redhat.com> - 8.9-1
- new upstream release coreutils-8.9

* Fri Dec 31 2010 Ondrej Vasik <ovasik@redhat.com> - 8.8-2
- The suffix length was dependent on the number of bytes
  or lines per file (#666293)

* Thu Dec 23 2010 Ondrej Vasik <ovasik@redhat.com> - 8.8-1
- fix parallel sorting issue (#655096)
- new upstream release coreutils-8.8 (#665164)

* Thu Nov 18 2010 Ondrej Vasik <ovasik@redhat.com> - 8.7-2
- don't prompt for password with runuser(#654367)

* Mon Nov 15 2010 Ondrej Vasik <ovasik@redhat.com> - 8.7-1
- new upstream release coreutils-8.7
- pam support in su consolidation with SUSE(#622700)

* Wed Nov 03 2010 Kamil Dudka <kdudka@redhat.com> - 8.6-3
- prevent sort from assertion failure in case LC_CTYPE does not match LC_TIME
  (#647938)

* Tue Oct 26 2010 Kamil Dudka <kdudka@redhat.com> - 8.6-2
- improve i18n support in sort (debug-keys test is now back)

* Wed Oct 20 2010 Ondrej Vasik <ovasik@redhat.com> - 8.6-1
- new upstream release 8.6
- remove applied patches, temporarily disable sort
  debug-keys test for multibyte locales (failing
  because of i18n patch)

* Thu Sep 30 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-10
- various fixes for case conversion in tr(#611274)

* Wed Sep 29 2010 jkeating - 8.5-9
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-8
- change assertion failure for invalid multibyte input
  in sort to less confusing error message(#591352)

* Wed Sep 08 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-7
- add RELRO protection to su as well (#630017)

* Mon Sep 06 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-6
- compile su with pie again (#630017)

* Mon Aug 30 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-5
- fix double free abort in tac (#628213)

* Thu Jul 22 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-4
- Add .ear, .war, .sar , for Java jar-like archives to
  dircolors (#616497)

* Fri Jul  2 2010 Dan Horák <dan[at]danny.cz> - 8.5-3
- rebuilt with the updated configuration patch
- drop the old -O1 exception for s390(x)
- updated the getgrouplist patch (Kamil Dudka)

* Tue Apr 27 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-2
- doublequote LS_COLORS in colorls.*sh scripts to speedup
  shell start(#586029)
- add patch for mkstemp on sparc64(Dennis Gilmore)
- update /etc/DIR_COLORS* files

* Mon Apr 26 2010 Ondrej Vasik <ovasik@redhat.com> - 8.5-1
- new upstream release 8.5

* Thu Apr 15 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-8
- move readlink from /usr/bin to bin, keep symlink in
  /usr/bin(#580682)

* Mon Mar 29 2010 Kamil Dudka <kdudka@redhat.com> - 8.4-7
- a new option df --direct

* Sat Mar 20 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-6
- run tput colors in colorls profile.d scripts only
  in the interactive mode(#450424)

* Fri Feb 12 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-5
- fix exit status of terminated child processes in su with
  pam(#559098)

* Fri Feb 05 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-4
- do not depend on selinux patch application in
  _require_selinux tests(#556350)

* Fri Jan 29 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-3
- do not fail tests if there are no loopdevices left
  (#558898)

* Tue Jan 26 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-2
- who doesn't determine user's message status correctly
  (#454261)

* Thu Jan 14 2010 Ondrej Vasik <ovasik@redhat.com> - 8.4-1
- new upstream release 8.4

* Fri Jan 08 2010 Ondrej Vasik <ovasik@redhat.com> - 8.3-1
- new upstream release 8.3

* Wed Jan 06 2010 Ondrej Vasik <ovasik@redhat.com> - 8.2-6
- require gmp-devel/gmp for large numbers support(#552846)

* Sun Dec 27 2009 Ondrej Vasik <ovasik@redhat.com> - 8.2-5
- fix misc/selinux root-only test(#550494)

* Sat Dec 19 2009 Ondrej Vasik <ovasik@redhat.com> - 8.2-4
- bring back uname -p/-i functionality except of the
  athlon hack(#548834)
- comment patches

* Wed Dec 16 2009 Ondrej Vasik <ovasik@redhat.com> - 8.2-3
- use grep instead of deprecated egrep in colorls.sh script
  (#548174)
- remove unnecessary versioned requires/conflicts
- remove non-upstream hack for uname -p

* Wed Dec 16 2009 Ondrej Vasik <ovasik@redhat.com> - 8.2-2
- fix DIR_COLORS.256color file

* Fri Dec 11 2009 Ondrej Vasik <ovasik@redhat.com> - 8.2-1
- new upstream release 8.2
- removed applied patches, temporarily do not run dup_cloexec()
  dependent gnulib tests failing in koji

* Fri Nov 27 2009 Ondrej Vasik <ovasik@redhat.com> - 8.1-1
- new upstream release 8.1
- fix build under koji (no test failures with underlying
  RHEL-5 XEN kernel due to unsearchable path and lack of
  futimens functionality)

* Wed Oct 07 2009 Ondrej Vasik <ovasik@redhat.com> - 8.0-2
- update /etc/DIR_COLORS* files

* Wed Oct 07 2009 Ondrej Vasik <ovasik@redhat.com> - 8.0-1
- New upstream release 8.0 (beta), defuzz patches,
  remove applied patches

* Mon Oct 05 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-7
- chcon no longer aborts on a selinux disabled system
  (#527142)

* Fri Oct 02 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-6
- ls -LR exits with status 2, not 0, when it encounters
  a cycle(#525402)
- ls: print "?", not "0" as inode of dereferenced dangling
  symlink(#525400)
- call the install-info on .gz info files

* Tue Sep 22 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-5
- improve and correct runuser documentation (#524805)

* Mon Sep 21 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-4
- add dircolors color for GNU lzip (#516897)

* Fri Sep 18 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-3
- fixed typo in DIR_COLORS.256color causing no color for
  multihardlink

* Wed Sep 16 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-2
- fix copying of extended attributes for read only source
  files

* Sat Sep 12 2009 Ondrej Vasik <ovasik@redhat.com> - 7.6-1
- new upstream bugfix release 7.6, removed applied patches,
  defuzzed the rest

* Thu Sep 10 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-6
- fix double free error in fold for singlebyte locales
  (caused by multibyte patch)

* Tue Sep 08 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-5
- fix sort -h for multibyte locales (reported via
  http://bugs.archlinux.org/task/16022)

* Thu Sep 03 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-4
- fixed regression where df -l <device> as regular user
  cause "Permission denied" (#520630, introduced by fix for
  rhbz #497830)

* Fri Aug 28 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-3
- ls -i: print consistent inode numbers also for mount points
  (#453709)

* Mon Aug 24 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-2
- Better fix than workaround the koji insufficient utimensat
  support issue to prevent failures in other packages

* Fri Aug 21 2009 Ondrej Vasik <ovasik@redhat.com> - 7.5-1
- New upstream release 7.5, remove already applied patches,
  defuzz few others, xz in default set(by dependencies),
  so no explicit br required
- skip two new tests on system with insufficient utimensat
  support(e.g. koji)
- libstdbuf.so in separate coreutils-libs subpackage
- update /etc/DIRCOLORS*

* Thu Aug 06 2009 Ondrej Vasik <ovasik@redhat.com> - 7.4-6
- do process install-info only with info files present(#515970)
- BuildRequires for xz, use xz tarball

* Wed Aug 05 2009 Kamil Dudka <kdudka@redhat.com> - 7.4-5
- ls -1U with two or more arguments (or with -R or -s) works properly again
- install runs faster again with SELinux enabled (#479502)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Ondrej Vasik <ovasik@redhat.com> 7.4-3
- do not ignore sort's version sort for multibyte locales
  (#509688)

* Thu Jun 18 2009 Ondrej Vasik <ovasik@redhat.com> 7.4-2
- temporarily workaround probable kernel issue with
  TCSADRAIN(#504798)

* Mon May 25 2009 Ondrej Vasik <ovasik@redhat.com> 7.4-1
- new upstream release 7.4, removed applied patches

* Thu Apr 23 2009 Ondrej Vasik <ovasik@redhat.com> 7.2-3
- fix segfaults in join (i18n patch) when using multibyte
  locales(#497368)

* Fri Apr 17 2009 Ondrej Vasik <ovasik@redhat.com> 7.2-2
- make mv xattr support failures silent (as is done for
  cp -a) - #496142

* Tue Mar 31 2009 Ondrej Vasik <ovasik@redhat.com> 7.2-1
- New upstream bugfix release 7.2
- removed applied patches
- temporarily disable strverscmp failing gnulib test

* Thu Mar 19 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-7
- do not ship /etc/DIR_COLORS.xterm - as many terminals
  use TERM xterm and black background as default - making
  ls color output unreadable
- shipping /etc/DIR_COLORS.lightbgcolor instead of it for
  light(white/gray) backgrounds
- try to preserve xattrs in cp -a when possible

* Mon Mar 02 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-6
- fix sort bugs (including #485715) for multibyte locales
  as well

* Fri Feb 27 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-5
- fix infinite loop in recursive cp (upstream, introduced
  by 7.1)

* Thu Feb 26 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-4
- fix showing ACL's for ls -Z (#487374), fix automatic
  column width for it as well

* Wed Feb 25 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-3
- fix couple of bugs (including #485715) in sort with
  determining end of fields(upstream)

* Wed Feb 25 2009 Ondrej Vasik <ovasik@redhat.com> 7.1-2
- workaround libcap issue with broken headers (#483548)
- fix gnulib testsuite failure (4x77 (skip) is not
  77(skip) ;) )

* Tue Feb 24 2009 Ondrej Vasik <ovasik@redhat.com> - 7.1-1
- New upstream release 7.1 (temporarily using tar.gz tarball
  as there are no xz utils in Fedora), removed applied
  patches, amended patches and LS_COLORS files

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Kamil Dudka <kdudka@redhat.com> - 7.0-7
- added BuildRequires for libattr-devel and attr

* Wed Jan 28 2009 Kamil Dudka <kdudka@redhat.com> - 7.0-6
- cp/mv: add --no-clobber (-n) option to not overwrite target
- cp/mv: add xattr support (#202823)

* Thu Dec 04 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-5
- fix info documentation for expr command as well(#474434)

* Thu Dec 04 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-4
- fixed syntax error w/ "expr" command using negative
  string/integer as first (i.e expr -125) - due to
  complexity of changes used diff against upstream git-head
  (#474434)
- enable total-awk test again (and skip it when df not working)

* Tue Nov 25 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-3
- package summary tuning

* Fri Nov 21 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-2
- added requirements for util-linux-ng >= 2.14
  because of file conflict in update from F-8/F-9(#472445)
- some sed cleanup, df totaltests patch changes (not working
  correctly yet :( )

* Wed Nov 12 2008 Ondrej Vasik <ovasik@redhat.com> - 7.0-1
- new upstream release
- modification/removal of related patches
- use automake 1.10.1 instead of 1.10a
- temporarily skip df --total tests (failures),
  timeout-paramaters (failure on ppc64)

* Mon Nov 03 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-17
- Requires: ncurses (#469277)

* Wed Oct 22 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-16
- make possible to disable capability in ls due to
  performance impact when not cached(#467508)
- do not patch generated manpages - generate them at build
  time
- do not mistakenly display -g and -G runuser option in su
  --help output

* Mon Oct 13 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-15
- fix several date issues(e.g. countable dayshifts, ignoring
  some cases of relative offset, locales conversions...)
- clarify ls exit statuses documentation (#446294)

* Sun Oct 12 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-14
- cp -Z now correctly separated in man page (#466646)
- cp -Z works again (#466653)
- make preservation of SELinux CTX non-mandatory for
  preserve=all cp option

* Wed Oct 08 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-13
- remove unimplemented (never accepted by upstream) option
  for chcon changes only. Removed from help and man.
- remove ugly lzma hack as lzma is now supported by setup
  macro

* Mon Oct 06 2008 Jarod Wilson <jarod@redhat.com> - 6.12-12
- fix up potential test failures when building in certain
  slightly quirky environments (part of bz#442352)

* Mon Oct 06 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-11
- added requires for libattr (#465569)

* Mon Sep 29 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-10
- seq should no longer fail to display final number of some
  float usages of seq with utf8 locales(#463556)

* Wed Aug 13 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-9
- mention that DISPLAY and XAUTHORITY envvars are preserved
  for pam_xauth in su -l (#450505)

* Mon Aug 04 2008 Kamil Dudka <kdudka@redhat.com> - 6.12-8
- ls -U1 now uses constant memory

* Wed Jul 23 2008 Kamil Dudka <kdudka@redhat.com> - 6.12-7
- dd: iflag=fullblock now read full blocks if possible
  (#431997, #449263)
- ls: --color now highlights files with capabilities (#449985)

* Wed Jul 16 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-6
- Get rid off fuzz in patches

* Fri Jul 04 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-5
- fix authors for basename and echo
- fix who info pages, print last runlevel only for printable
  chars

* Mon Jun 16 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-4
- print verbose output of chcon with newline after each 
  message (#451478)

* Fri Jun 06 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-3
- workaround for koji failures(#449910, #442352) now 
  preserves timestamps correctly - fallback to supported
  functions, added test case
- runuser binary is no longer doubled in /usr/bin/runuser

* Wed Jun 04 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-2
- workaround for strange koji failures(#449910,#442352)
- fixed ls -ZC segfault(#449866, introduced by 6.10-1 
  SELinux patch reworking) 

* Mon Jun 02 2008 Ondrej Vasik <ovasik@redhat.com> - 6.12-1
- New upstream release 6.12, adapted patches

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 6.11-5
- fix SHA256/SHA512 to work on sparc

* Tue May 20 2008 Ondrej Vasik <ovasik@redhat.com> - 6.11-4
- fixed a HUGE memory leak in install binary(#447410)

* Mon May 19 2008 Ondrej Vasik <ovasik@redhat.com> - 6.11-3
- added arch utility (from util-linux-ng)
- do not show executable file types without executable bit
  in colored ls as executable

* Wed Apr 23 2008 Ondrej Vasik <ovasik@redhat.com> - 6.11-2
- Do not show misleading scontext in id command when user
  is specified (#443485)
- Avoid possible test failures on non-english locales

* Mon Apr 21 2008 Ondrej Vasik <ovasik@redhat.com> - 6.11-1
- New upstream release 6.11 
- removed accepted patches + few minor patch changes

* Fri Apr 18 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-21
- fix wrong checksum line handling in sha1sum -c 
  command(#439531)

* Tue Apr 15 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-20
- fix possible segfault in sha1sum/md5sum command

* Mon Apr 14 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-19
- fix possible build-failure typo in i18n patch(#442205)

* Mon Apr  7 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-18
- fix colorls.sh syntax with Zsh (#440652)
- mention that cp -a includes -c option + mention cp -c 
  option in manpages (#440056)
- fix typo in runuser manpages (#439410)

* Sat Mar 29 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-17
- better workaround of glibc getoptc change(factor test)
- don't segfault mknod, mkfifo with invalid-selinux-context

* Thu Mar 27 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-16
- keep LS_COLORS when USER_LS_COLORS defined
- someupstream fixes:
- mkdir -Z invalid-selinux-context dir no longer segfaults
- ptx with odd number of backslashes no longer leads to buffer
  overflow
- paste -d'\' file" no longer ovveruns memory

* Wed Mar 26 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-15
- covered correct handling for some test conditions failures
  e.g. root build+selinux active and not running mcstrans(d)
  or selinux enforcing (#436717)

* Wed Mar 19 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-14
- mv: never unlink a destination file before calling rename
  (upstream, #438076)

* Mon Mar 17 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-13
- disable echo option separator behavior(added by #431005,
  request for removal #437653 + upstream)
- temporarily disabled longoptions change until full 
  clarification upstreamery (#431005)

* Tue Mar 11 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-12
- fixed harmless double close of stdout in dd(#436368)

* Thu Mar  6 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-11
- fixed broken order of params in stat(#435669)

* Tue Mar  4 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-10
- colorls.csh missing doublequotes (#435789)
- fixed possibility to localize verbose outputs

* Mon Mar  3 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-9
- consolidation of verbose output to stdout (upstream)

* Mon Feb 18 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-8
- use default security context in install - broken by 
  coreutils-6.10 update(#319231)
- some sh/csh scripts optimalizations(by ville.skytta@iki.fi,
  - #433189, #433190)

* Mon Feb 11 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-7
- keep old csh/sh usermodified colorls shell scripts
  but use the new ones(#432154)

* Thu Feb  7 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-6
- better 256-color support in colorls shell scripts
- color tuning(based on feedback in #429121)

* Mon Feb  4 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-5
- enabled 256-color support in colorls shell scripts(#429121)
- fixed syntax error in csh script(#431315)

* Thu Jan 31 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-4
- forgotten return in colorls.sh change

* Thu Jan 31 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-3
- fix unability of echo to display certain strings(added --
  separator, #431005)
- do not require only one long_opt for certain commands 
  e.g. sleep, yes - but use first usable (#431005)
- do not override userspecified LS_COLORS variable, but
  use it for colored ls(#430827)
- discard errors from dircolors to /dev/null + some tuning 
  of lscolor sh/csh scripts(#430823)
- do not consider files with SELinux security context as
  files having ACL in ls long format(#430779)

* Mon Jan 28 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-2
- some manpages improvements(#406981,#284881)
- fix non-versioned obsoletes of mktemp(#430407)

* Fri Jan 25 2008 Ondrej Vasik <ovasik@redhat.com> - 6.10-1
- New upstream release(changed %%prep because of lack of lzma
  support in %%setup macro)
- License GPLv3+
- removed patches cp-i-u,du-ls-upstream,statsecuritycontext,
  futimens,getdateYYYYMMDD,ls-x
- modified patches to be compilable after upstream changes
- selinux patch reworked to have backward compatibility with
  F8(cp,ls and stat behaviour differ from upstream in SELinux
  options)
- su-l/runuser-l pam file usage a bit documented(#368721)
- more TERMs for DIR_COLORS, added colors for audio files,
  more image/compress file types(taken from upstream 
  dircolors.hin)
- new file DIR_COLORS.256color which takes advantage from 
  256color term types-not really used yet(#429121)

* Wed Jan 16 2008 Ondrej Vasik <ovasik@redhat.com> - 6.9-17
- added several missing colored TERMs(including rxvt-unicode,
  screen-256color and xterm-256color) to DIR_COLORS and
  DIR_COLORS.xterm(#239266) 

* Wed Dec 05 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-16
- fix displaying of security context in stat(#411181)

* Thu Nov 29 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-15
- completed fix of wrong colored broken symlinks in ls(#404511)

* Fri Nov 23 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-14
- fixed bug in handling YYYYMMDD date format with relative
  signed offset(#377821)

* Tue Nov 13 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-13
- fixed bug in selinux patch which caused bad preserving
  of security context in install(#319231)

* Fri Nov 02 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-12
- added some upstream supported dircolors TERMs(#239266)
- fixed du output for unaccesible dirs(#250089)
- a bit of upstream tunning for symlinks

* Tue Oct 30 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-11
- allow cp -a to rewrite file on different filesystem(#219900)
  (based on upstream patch)

* Mon Oct 29 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-10
- modified coreutils-i18n.patch because of sort -R in
  a non C locales(fix by Andreas Schwab) (#249315)

* Mon Oct 29 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-9
- applied upstream patch for runuser to coreutils-selinux.patch(#232652)
- License tag to GPLv2+

* Thu Oct 25 2007 Ondrej Vasik <ovasik@redhat.com> - 6.9-8
- applied upstream patch for cp and mv(#248591)

* Thu Aug 23 2007 Pete Graner <pgraner@redhat.com> - 6.9-7
- Fix typo in spec file. (CVS merge conflict leftovers)

* Thu Aug 23 2007 Pete Graner <pgraner@redhat.com> - 6.9-6
- Remove --all-name from spec file its now provided in the upstream rpm's find-lang.sh
- Rebuild

* Tue Aug 14 2007 Tim Waugh <twaugh@redhat.com> 6.9-5
- Don't generate runuser.1 since we ship a complete manpage for it
  (bug #241662).

* Wed Jul  4 2007 Tim Waugh <twaugh@redhat.com> 6.9-4
- Use hard links instead of symbolic links for LC_TIME files (bug #246729).

* Wed Jun 13 2007 Tim Waugh <twaugh@redhat.com> 6.9-3
- Fixed 'ls -x' output (bug #240298).
- Disambiguate futimens() from the glibc implementation (bug #242321).

* Mon Apr 02 2007 Karsten Hopp <karsten@redhat.com> 6.9-2
- /bin/mv in %%post requires libselinux

* Mon Mar 26 2007 Tim Waugh <twaugh@redhat.com> 6.9-1
- 6.9.

* Fri Mar  9 2007 Tim Waugh <twaugh@redhat.com>
- Better install-info scriptlets (bug #225655).

* Thu Mar  1 2007 Tim Waugh <twaugh@redhat.com> 6.8-1
- 6.8+, in preparation for 6.9.

* Thu Feb 22 2007 Tim Waugh <twaugh@redhat.com> 6.7-9
- Use sed instead of perl for text replacement (bug #225655).
- Use install-info scriptlets from the guidelines (bug #225655).

* Tue Feb 20 2007 Tim Waugh <twaugh@redhat.com> 6.7-8
- Don't mark profile scripts as config files (bug #225655).
- Avoid extra directory separators (bug #225655).

* Mon Feb 19 2007 Tim Waugh <twaugh@redhat.com> 6.7-7
- Better Obsoletes/Provides versioning (bug #225655).
- Use better defattr (bug #225655).
- Be info file compression tolerant (bug #225655).
- Moved changelog compression to %%install (bug #225655).
- Prevent upstream changes being masked (bug #225655).
- Added a comment (bug #225655).
- Use install -p for non-compiled files (bug #225655).
- Use sysconfdir macro for /etc (bug #225655).
- Use Requires(pre) etc for install-info (bug #225655).

* Fri Feb 16 2007 Tim Waugh <twaugh@redhat.com> 6.7-6
- Provide version for stat (bug #225655).
- Fixed permissions on profile scripts (bug #225655).

* Wed Feb 14 2007 Tim Waugh <twaugh@redhat.com> 6.7-5
- Removed unnecessary stuff in pre scriptlet (bug #225655).
- Prefix sources with 'coreutils-' (bug #225655).
- Avoid %%makeinstall (bug #225655).

* Tue Feb 13 2007 Tim Waugh <twaugh@redhat.com> 6.7-4
- Ship COPYING file (bug #225655).
- Use datadir and infodir macros in %%pre scriptlet (bug #225655).
- Use spaces not tabs (bug #225655).
- Fixed build root.
- Change prereq to requires (bug #225655).
- Explicitly version some obsoletes tags (bug #225655).
- Removed obsolete pl translation fix.

* Mon Jan 22 2007 Tim Waugh <twaugh@redhat.com> 6.7-3
- Make scriptlet unconditionally succeed (bug #223681).

* Fri Jan 19 2007 Tim Waugh <twaugh@redhat.com> 6.7-2
- Build does not require libtermcap-devel.

* Tue Jan  9 2007 Tim Waugh <twaugh@redhat.com> 6.7-1
- 6.7.  No longer need sort-compatibility, rename, newhashes, timestyle,
  acl, df-cifs, afs or autoconf patches.

* Tue Jan  2 2007 Tim Waugh <twaugh@redhat.com>
- Prevent 'su --help' showing runuser-only options such as --group.

* Fri Nov 24 2006 Tim Waugh <twaugh@redhat.com> 5.97-16
- Unbreak id (bug #217177).

* Thu Nov 23 2006 Tim Waugh <twaugh@redhat.com> 5.97-15
- Fixed stat's 'C' format specifier (bug #216676).
- Misleading 'id -Z root' error message (bug #211089).

* Fri Nov 10 2006 Tim Waugh <twaugh@redhat.com> 5.97-14
- Clarified runcon man page (bug #213846).

* Tue Oct 17 2006 Tim Waugh <twaugh@redhat.com> 5.97-13
- Own LC_TIME locale directories (bug #210751).

* Wed Oct  4 2006 Tim Waugh <twaugh@redhat.com> 5.97-12
- Fixed 'cp -Z' when destination exists, again (bug #189967).

* Thu Sep 28 2006 Tim Waugh <twaugh@redhat.com> 5.97-11
- Back-ported rename patch (bug #205744).

* Tue Sep 12 2006 Tim Waugh <twaugh@redhat.com> 5.97-10
- Ignore 'cifs' filesystems for 'df -l' (bug #183703).
- Include -g/-G in runuser man page (part of bug #199344).
- Corrected runuser man page (bug #200620).

* Thu Aug 24 2006 Tim Waugh <twaugh@redhat.com> 5.97-9
- Fixed warnings in pam, i18n, sysinfo, selinux and acl patches (bug #203166).

* Wed Aug 23 2006 Tim Waugh <twaugh@redhat.com> 5.97-8
- Don't chdir until after PAM bits in su (bug #197659).

* Tue Aug 15 2006 Tim Waugh <twaugh@redhat.com> 5.97-7
- Fixed 'sort -b' multibyte problem (bug #199986).

* Fri Jul 21 2006 Tim Waugh <twaugh@redhat.com> 5.97-6
- Added runuser '-g' and '-G' options (bug #199344).
- Added su '--session-command' option (bug #199066).

* Tue Jul 18 2006 Tomas Mraz <tmraz@redhat.com> 5.97-5
- 'include' su and runuser scripts in su-l and runuser-l scripts

* Thu Jul 13 2006 David Howells <dhowells@redhat.com> 5.97-4
- split the PAM scripts for "su -l"/"runuser -l" from that of normal "su" and
  "runuser" (#198639)
- add keyinit instructions to PAM scripts

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.97-3.1
- rebuild

* Tue Jul 11 2006 Tomas Mraz <tmraz@redhat.com> 5.97-3
- allow root to su to expired user (#152420)

* Thu Jun 29 2006 Tim Waugh <twaugh@redhat.com> 5.97-2
- Allow 'sort +1 -2' (patch from upstream).

* Sun Jun 25 2006 Tim Waugh <twaugh@redhat.com> 5.97-1
- 5.97.  No longer need tempname or tee patches, or pl translation.

* Sun Jun 25 2006 Tim Waugh <twaugh@redhat.com> 5.96-4
- Include new hashes (bug #196369).  Patch from upstream.
- Build at -O1 on s390 for the moment (bug #196369).

* Fri Jun  9 2006 Tim Waugh <twaugh@redhat.com>
- Fix large file support for temporary files.

* Mon Jun  5 2006 Tim Waugh <twaugh@redhat.com> 5.96-3
- Fixed Polish translation.

* Mon May 22 2006 Tim Waugh <twaugh@redhat.com> 5.96-2
- 5.96.  No longer need proc patch.

* Fri May 19 2006 Tim Waugh <twaugh@redhat.com>
- Fixed pr properly in multibyte locales (bug #192381).

* Tue May 16 2006 Tim Waugh <twaugh@redhat.com> 5.95-3
- Upstream patch to fix cp -p when proc is not mounted (bug #190601).
- BuildRequires libacl-devel.

* Mon May 15 2006 Tim Waugh <twaugh@redhat.com>
- Fixed pr in multibyte locales (bug #189663).

* Mon May 15 2006 Tim Waugh <twaugh@redhat.com> 5.95-2
- 5.95.

* Wed Apr 26 2006 Tim Waugh <twaugh@redhat.com> 5.94-4
- Avoid redeclared 'tee' function.
- Fix 'cp -Z' when the destination exists (bug #189967).

* Thu Apr 20 2006 Tim Waugh <twaugh@redhat.com> 5.94-3
- Make 'ls -Z' output more consistent with other output formats.

* Fri Mar 24 2006 Tim Waugh <twaugh@redhat.com> 5.94-2
- 5.94.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 5.93-7.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 5.93-7.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 23 2006 Tim Waugh <twaugh@redhat.com>
- Fixed chcon(1) bug reporting address (bug #178523).

* Thu Jan  5 2006 Tim Waugh <twaugh@redhat.com> 5.93-7
- Don't suppress chown/chgrp errors in install(1) (bug #176708).

* Mon Jan  2 2006 Dan Walsh <dwalsh@redhat.com> 5.93-6
- Remove pam_selinux.so from su.pamd, not needed for targeted and Strict/MLS 
  will have to newrole before using.

* Fri Dec 23 2005 Tim Waugh <twaugh@redhat.com> 5.93-5
- Fix "sort -n" (bug #176468).

* Fri Dec 16 2005 Tim Waugh <twaugh@redhat.com>
- Explicitly set default POSIX2 version during configure stage.

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Tim Waugh <twaugh@redhat.com>
- Parametrize SELinux (bug #174067).
- Fix runuser.pamd (bug #173807).

* Thu Nov 24 2005 Tim Waugh <twaugh@redhat.com> 5.93-4
- Rebuild to pick up new glibc *at functions.
- Apply runuser PAM patch from bug #173807.  Ship runuser PAM file.

* Tue Nov 15 2005 Dan Walsh <dwalsh@redhat.com> 5.93-3
- Remove multiple from su.pamd

* Mon Nov 14 2005 Tim Waugh <twaugh@redhat.com> 5.93-2
- Call setsid() in su under some circumstances (bug #173008).
- Prevent runuser operating when setuid (bug #173113).

* Tue Nov  8 2005 Tim Waugh <twaugh@redhat.com> 5.93-1
- 5.93.
- No longer need alt-md5sum-binary, dircolors, mkdir, mkdir2 or tac patches.

* Fri Oct 28 2005 Tim Waugh <twaugh@redhat.com> 5.92-1
- Finished porting i18n patch to sort.c.
- Fixed for sort-mb-tests (avoid +n syntax).

* Fri Oct 28 2005 Tim Waugh <twaugh@redhat.com> 5.92-0.2
- Fix chgrp basic test.
- Include md5sum patch from ALT.

* Mon Oct 24 2005 Tim Waugh <twaugh@redhat.com> 5.92-0.1
- 5.92.
- No longer need afs, dircolors, utmp, gcc4, brokentest, dateseconds,
  chown, rmaccess, copy, stale-utmp, no-sign-extend, fchown patches.
- Updated acl, dateman, pam, langinfo, i18n, getgrouplist, selinux patches.
- Dropped printf-ll, allow_old_options, jday, zh_CN patches.
- NOTE: i18n patch not ported for sort(1) yet.

* Fri Sep 30 2005 Tomas Mraz <tmraz@redhat.com> - 5.2.1-56
- use include instead of pam_stack in pam config

* Fri Sep 9 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-55
- Reverse change to use raw functions

* Thu Sep  8 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-54
- Explicit setuid bit for /bin/su in file manifest (bug #167745).

* Tue Sep 6 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-53
- Allow id to run even when SELinux security context can not be run
- Change chcon to use raw functions.

* Tue Jun 28 2005 Tim Waugh <twaugh@redhat.com>
- Corrected comments in DIR_COLORS.xterm (bug #161711).

* Wed Jun 22 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-52
- Fixed stale-utmp patch so that 'who -r' and 'who -b' work
  again (bug #161264).

* Fri Jun 17 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-51
- Use upstream hostid fix.

* Thu Jun 16 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-50
- Don't display the sign-extended part of the host id (bug #160078).

* Tue May 31 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-49
- Eliminate bogus "can not preserve context" message when moving files.

* Wed May 25 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-48
- Prevent buffer overflow in who(1) (bug #158405).

* Fri May 20 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-47
- Better error checking in the pam patch (bug #158189).

* Mon May 16 2005 Dan Walsh <dwalsh@redhat.com> 5.2.1-46
- Fix SELinux patch to better handle MLS integration

* Mon May 16 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-45
- Applied Russell Coker's selinux changes (bug #157856).

* Fri Apr  8 2005 Tim Waugh <twaugh@redhat.com>
- Fixed pam patch from Steve Grubb (bug #154946).
- Use better upstream patch for "stale utmp".

* Tue Mar 29 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-44
- Added "stale utmp" patch from upstream.

* Thu Mar 24 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-43
- Removed patch that adds -C option to install(1).

* Wed Mar 16 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-42
- Fixed pam patch.
- Fixed broken configure test.
- Fixed build with GCC 4 (bug #151045).

* Wed Feb  9 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-41
- Jakub Jelinek's sort -t multibyte fixes (bug #147567).

* Sat Feb  5 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-40
- Undo last change (bug #145266).

* Fri Feb  4 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-38
- Special case for ia32e in uname (bug #145266).

* Thu Jan 13 2005 Tim Waugh <twaugh@redhat.com> 5.2.1-37
- Fixed zh_CN translation (bug #144845).  Patch from Mitrophan Chin.

* Tue Dec 28 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-36
- Fix to only setdefaultfilecon if not overridden by command line

* Mon Dec 27 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-35
- Change install to restorecon if it can

* Wed Dec 15 2004 Tim Waugh <twaugh@redhat.com>
- Fixed small bug in i18n patch.

* Mon Dec  6 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-34
- Don't set fs uid until after pam_open_session (bug #77791).

* Thu Nov 25 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-33
- Fixed colorls.csh (bug #139988).  Patch from Miloslav Trmac.

* Mon Nov  8 2004 Tim Waugh <twaugh@redhat.com>
- Updated URL (bug #138279).

* Mon Oct 25 2004 Steve Grubb <sgrubb@redhat.com> 5.2.1-32
- Handle the return code of function calls in runcon.

* Mon Oct 18 2004 Tim Waugh <twaugh@redhat.com>
- Prevent compiler warning in coreutils-i18n.patch (bug #136090).

* Tue Oct  5 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-31
- getgrouplist() patch from Ulrich Drepper.
- The selinux patch should be applied last.

* Mon Oct  4 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-30
- Mv runuser to /sbin

* Mon Oct  4 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-28
- Fix runuser man page.

* Mon Oct  4 2004 Tim Waugh <twaugh@redhat.com>
- Fixed build.

* Fri Sep 24 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-26
- Add runuser as similar to su, but only runable by root

* Fri Sep 24 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-25
- chown(1) patch from Ulrich Drepper.

* Tue Sep 14 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-24
- SELinux patch fix: don't display '(null)' if getfilecon() fails
  (bug #131196).

* Fri Aug 20 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-23
- Fixed colorls.csh quoting (bug #102412).
- Fixed another join LSB test failure (bug #121153).

* Mon Aug 16 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-22
- Fixed sort -t LSB test failure (bug #121154).
- Fixed join LSB test failure (bug #121153).

* Wed Aug 11 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-21
- Apply upstream patch to fix 'cp -a' onto multiply-linked files (bug #128874).
- SELinux patch fix: don't error out if lgetfilecon() returns ENODATA.

* Tue Aug 10 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-20
- Added 'konsole' TERM to DIR_COLORS (bug #129544).

* Wed Aug  4 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-19
- Added 'gnome' TERM to DIR_COLORS (bug #129112).
- Worked around a bash bug #129128.
- Fixed an i18n patch bug in cut (bug #129114).

* Tue Aug  3 2004 Tim Waugh <twaugh@redhat.com>
- Fixed colorls.{sh,csh} so that the l. and ll aliases are always defined
  (bug #128948).

* Tue Jul 13 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-18
- Fixed field extraction in sort (bug #127694).

* Fri Jun 25 2004 Tim Waugh <twaugh@redhat.com>
- Added 'TERM screen.linux' to DIR_COLORS (bug #78816).

* Wed Jun 23 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-17
- Move pam-xauth to after pam-selinux

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-15
- Fix ls -Z (bug #125447).

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com>
- Build requires bison (bug #125290).

* Fri Jun  4 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-14
- Fix selinux patch causing problems with ls --format=... (bug #125238).

* Thu Jun 3 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-13
- Change su to use pam_selinux open and pam_selinux close

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-12
- Don't call access() on symlinks about to be removed (bug #124699).

* Wed Jun  2 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-11
- Fix ja translation (bug #124862).

* Tue May 18 2004 Jeremy Katz <katzj@redhat.com> 5.2.1-10
- rebuild

* Mon May 17 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-9
- Mention pam in the info for su (bug #122592).
- Remove wheel group rant again (bug #122886).
- Change default behaviour for chgrp/chown (bug #123263).  Patch from
  upstream.

* Mon May 17 2004 Thomas Woerner <twoerner@redhat.com> 5.2.1-8
- compiling su PIE

* Wed May 12 2004 Tim Waugh <twaugh@redhat.com>
- Build requires new versions of autoconf and automake (bug #123098).

* Tue May  4 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-7
- Fix join -t (bug #122435).

* Tue Apr 20 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-6
- Fix 'ls -Z' displaying users/groups if stat() failed (bug #121292).

* Fri Apr 9 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-5
- Add ls -LZ fix
- Fix chcon to handle "."

* Wed Mar 17 2004 Tim Waugh <twaugh@redhat.com>
- Apply upstream fix for non-zero seconds for --date="10:00 +0100".

* Tue Mar 16 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-3
- If preserve fails, report as warning unless user requires preserve

* Tue Mar 16 2004 Dan Walsh <dwalsh@redhat.com> 5.2.1-2
- Make mv default to preserve on context

* Sat Mar 13 2004 Tim Waugh <twaugh@redhat.com> 5.2.1-1
- 5.2.1.

* Fri Mar 12 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-9
- Add '-Z' to 'ls --help' output (bug #118108).

* Fri Mar  5 2004 Tim Waugh <twaugh@redhat.com>
- Fix deref-args test case for rebuilding under SELinux (bug #117556).

* Wed Feb 25 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-8
- kill(1) offloaded to util-linux altogether.

* Tue Feb 24 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-7
- Ship the real '[', not a symlink.

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-6
- Apply Paul Eggert's chown patch (bug #116536).
- Merged chdir patch into pam patch where it belongs.

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-5
- Fixed i18n patch bug causing sort -M not to work (bug #116575).

* Sat Feb 21 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-4
- Reinstate kill binary, just not its man page (bug #116463).

* Sat Feb 21 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-3
- Updated ls-stat patch.

* Fri Feb 20 2004 Dan Walsh <dwalsh@redhat.com> 5.2.0-2
- fix chcon to ignore . and .. directories for recursing

* Fri Feb 20 2004 Tim Waugh <twaugh@redhat.com> 5.2.0-1
- Patch ls so that failed stat() is handled gracefully (Ulrich Drepper).
- 5.2.0.

* Thu Feb 19 2004 Tim Waugh <twaugh@redhat.com>
- More AFS patch tidying.

* Wed Feb 18 2004 Dan Walsh <dwalsh@redhat.com> 5.1.3-0.2
- fix chcon to handle -h qualifier properly, eliminate potential crash 

* Wed Feb 18 2004 Tim Waugh <twaugh@redhat.com>
- Stop 'sort -g' leaking memory (i18n patch bug #115620).
- Don't ship kill, since util-linux already does.
- Tidy AFS patch.

* Mon Feb 16 2004 Tim Waugh <twaugh@redhat.com> 5.1.3-0.1
- 5.1.3.
- Patches ported forward or removed.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 5.0-40
- rebuilt

* Tue Jan  20 2004 Dan Walsh <dwalsh@redhat.com> 5.0-39
- Change /etc/pam.d/su to remove preservuser and add multiple

* Tue Jan  20 2004 Dan Walsh <dwalsh@redhat.com> 5.0-38
- Change is_selinux_enabled to is_selinux_enabled > 0

* Tue Jan  20 2004 Dan Walsh <dwalsh@redhat.com> 5.0-37
- Add pam_selinux to pam file to allow switching of roles within selinux

* Fri Jan 16 2004 Tim Waugh <twaugh@redhat.com>
- The textutils-2.0.17-mem.patch is no longer needed.

* Thu Jan 15 2004 Tim Waugh <twaugh@redhat.com> 5.0-36
- Fixed autoconf test causing builds to fail.

* Tue Dec  9 2003 Dan Walsh <dwalsh@redhat.com> 5.0-35
- Fix copying to non xattr files

* Thu Dec  4 2003 Tim Waugh <twaugh@redhat.com> 5.0-34.sel
- Fix column widths problems in ls.

* Tue Dec  2 2003 Tim Waugh <twaugh@redhat.com> 5.0-33.sel
- Speed up md5sum by disabling speed-up asm.

* Wed Nov 19 2003 Dan Walsh <dwalsh@redhat.com> 5.0-32.sel
- Try again

* Wed Nov 19 2003 Dan Walsh <dwalsh@redhat.com> 5.0-31.sel
- Fix move on non SELinux kernels

* Fri Nov 14 2003 Tim Waugh <twaugh@redhat.com> 5.0-30.sel
- Fixed useless acl dependencies (bug #106141).

* Fri Oct 24 2003 Dan Walsh <dwalsh@redhat.com> 5.0-29.sel
- Fix id -Z

* Tue Oct 21 2003 Dan Walsh <dwalsh@redhat.com> 5.0-28.sel
- Turn on SELinux
- Fix chcon error handling

* Wed Oct 15 2003 Dan Walsh <dwalsh@redhat.com> 5.0-28
- Turn off SELinux

* Mon Oct 13 2003 Dan Walsh <dwalsh@redhat.com> 5.0-27.sel
- Turn on SELinux

* Mon Oct 13 2003 Dan Walsh <dwalsh@redhat.com> 5.0-27
- Turn off SELinux

* Mon Oct 13 2003 Dan Walsh <dwalsh@redhat.com> 5.0-26.sel
- Turn on SELinux

* Sun Oct 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without pam support

* Fri Oct 10 2003 Tim Waugh <twaugh@redhat.com> 5.0-23
- Make split(1) handle large files (bug #106700).

* Thu Oct  9 2003 Dan Walsh <dwalsh@redhat.com> 5.0-22
- Turn off SELinux

* Wed Oct  8 2003 Dan Walsh <dwalsh@redhat.com> 5.0-21.sel
- Cleanup SELinux patch

* Fri Oct  3 2003 Tim Waugh <twaugh@redhat.com> 5.0-20
- Restrict ACL support to only those programs needing it (bug #106141).
- Fix default PATH for LSB (bug #102567).

* Thu Sep 11 2003 Dan Walsh <dwalsh@redhat.com> 5.0-19
- Turn off SELinux

* Wed Sep 10 2003 Dan Walsh <dwalsh@redhat.com> 5.0-18.sel
- Turn on SELinux

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 5.0-17
- Turn off SELinux

* Tue Sep 2 2003 Dan Walsh <dwalsh@redhat.com> 5.0-16.sel
- Only call getfilecon if the user requested it.
- build with selinux

* Wed Aug 20 2003 Tim Waugh <twaugh@redhat.com> 5.0-14
- Documentation fix (bug #102697).

* Tue Aug 12 2003 Tim Waugh <twaugh@redhat.com> 5.0-13
- Made su use pam again (oops).
- Fixed another i18n bug causing sort --month-sort to fail.
- Don't run dubious stty test, since it fails when backgrounded
  (bug #102033).
- Re-enable make check.

* Fri Aug  8 2003 Tim Waugh <twaugh@redhat.com> 5.0-12
- Don't run 'make check' for this build (build environment problem).
- Another uninitialized variable in i18n (from bug #98683).

* Wed Aug 6 2003 Dan Walsh <dwalsh@redhat.com> 5.0-11
- Internationalize runcon
- Update latest chcon from NSA

* Wed Jul 30 2003 Tim Waugh <twaugh@redhat.com>
- Re-enable make check.

* Wed Jul 30 2003 Tim Waugh <twaugh@redhat.com> 5.0-9
- Don't run 'make check' for this build (build environment problem).

* Mon Jul 28 2003 Tim Waugh <twaugh@redhat.com> 5.0-8
- Actually use the ACL patch (bug #100519).

* Wed Jul 16 2003 Dan Walsh <dwalsh@redhat.com> 5.0-7
- Convert to SELinux

* Mon Jun  9 2003 Tim Waugh <twaugh@redhat.com>
- Removed samefile patch.  Now the test suite passes.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 28 2003 Tim Waugh <twaugh@redhat.com> 5.0-5
- Both kon and kterm support colours (bug #83701).
- Fix 'ls -l' alignment in zh_CN locale (bug #88346).

* Mon May 12 2003 Tim Waugh <twaugh@redhat.com> 5.0-4
- Prevent file descriptor leakage in du (bug #90563).
- Build requires recent texinfo (bug #90439).

* Wed Apr 30 2003 Tim Waugh <twaugh@redhat.com> 5.0-3
- Allow obsolete options unless POSIXLY_CORRECT is set.

* Sat Apr 12 2003 Tim Waugh <twaugh@redhat.com>
- Fold bug was introduced by i18n patch; fixed there instead.

* Fri Apr 11 2003 Matt Wilson <msw@redhat.com> 5.0-2
- fix segfault in fold (#88683)

* Sat Apr  5 2003 Tim Waugh <twaugh@redhat.com> 5.0-1
- 5.0.

* Mon Mar 24 2003 Tim Waugh <twaugh@redhat.com>
- Use _smp_mflags.

* Mon Mar 24 2003 Tim Waugh <twaugh@redhat.com> 4.5.11-2
- Remove overwrite patch.
- No longer seem to need nolibrt, errno patches.

* Thu Mar 20 2003 Tim Waugh <twaugh@redhat.com>
- No longer seem to need danglinglink, prompt, lug, touch_errno patches.

* Thu Mar 20 2003 Tim Waugh <twaugh@redhat.com> 4.5.11-1
- 4.5.11.
- Use packaged readlink.

* Wed Mar 19 2003 Tim Waugh <twaugh@redhat.com> 4.5.10-1
- 4.5.10.
- Update lug, touch_errno, acl, utmp, printf-ll, i18n, test-bugs patches.
- Drop fr_fix, LC_TIME, preserve, regex patches.

* Wed Mar 12 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-21
- Fixed another i18n patch bug (bug #82032).

* Tue Mar 11 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-20
- Fix sort(1) efficiency in multibyte encoding (bug #82032).

* Tue Feb 18 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-19
- Ship readlink(1) (bug #84200).

* Thu Feb 13 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-18
- Deal with glibc < 2.2 in %%pre scriplet (bug #84090).

* Wed Feb 12 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-16
- Require glibc >= 2.2 (bug #84090).

* Tue Feb 11 2003 Bill Nottingham <notting@redhat.com> 4.5.3-15
- fix group (#84095)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 4.5.3-14
- rebuilt

* Thu Jan 16 2003 Tim Waugh <twaugh@redhat.com>
- Fix rm(1) man page.

* Thu Jan 16 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-13
- Fix re_compile_pattern check.
- Fix su hang (bug #81653).

* Tue Jan 14 2003 Tim Waugh <twaugh@redhat.com> 4.5.3-11
- Fix memory size calculation.

* Tue Dec 17 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-10
- Fix mv error message (bug #79809).

* Mon Dec 16 2002 Tim Powers <timp@redhat.com> 4.5.3-9
- added PreReq on grep

* Fri Dec 13 2002 Tim Waugh <twaugh@redhat.com>
- Fix cp --preserve with multiple arguments.

* Thu Dec 12 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-8
- Turn on colorls for screen (bug #78816).

* Mon Dec  9 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-7
- Fix mv (bug #79283).
- Add patch27 (nogetline).

* Sun Dec  1 2002 Tim Powers <timp@redhat.com> 4.5.3-6
- use the su.pamd from sh-utils since it works properly with multilib systems

* Fri Nov 29 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-5
- Fix test suite quoting problems.

* Fri Nov 29 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-4
- Fix scriplets.
- Fix i18n patch so it doesn't break uniq.
- Fix several other patches to either make the test suite pass or
  not run the relevant tests.
- Run 'make check'.
- Fix file list.

* Thu Nov 28 2002 Tim Waugh <twaugh@redhat.com> 4.5.3-3
- Adapted for Red Hat Linux.
- Self-host for help2man.
- Don't ship readlink just yet (maybe later).
- Merge patches from fileutils and sh-utils (textutils ones are already
  merged it seems).
- Keep the binaries where the used to be (in particular, id and stat).

* Sun Nov 17 2002 Stew Benedict <sbenedict@mandrakesoft.com> 4.5.3-2mdk
- LI18NUX/LSB compliance (patch800)
- Installed (but unpackaged) file(s) - /usr/share/info/dir

* Thu Oct 31 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.3-1mdk
- new release
- rediff patch 180
- merge patch 150 into 180

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-6mdk
- move su back to /bin

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-5mdk
- patch 0 : lg locale is illegal and must be renamed lug (pablo)

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-4mdk
- fix conflict with procps

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-3mdk
- patch 105 : fix install -s

* Mon Oct 14 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-2mdk
- fix build
- don't chmode two times su
- build with large file support
- fix description
- various spec cleanups
- fix chroot installation
- fix missing /bin/env
- add old fileutils, sh-utils & textutils ChangeLogs

* Fri Oct 11 2002 Thierry Vignaud <tvignaud@mandrakesoft.com> 4.5.2-1mdk
- initial release (merge fileutils, sh-utils & textutils)
- obsoletes/provides: sh-utils/fileutils/textutils
- fileutils stuff go in 1xx range
- sh-utils stuff go in 7xx range
- textutils stuff go in 5xx range
- drop obsoletes patches 1, 2, 10 (somes files're gone but we didn't ship
  most of them)
- rediff patches 103, 105, 111, 113, 180, 706
- temporary disable patch 3 & 4
- fix fileutils url
