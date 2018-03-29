Name:           irqbalance
Version:        1.0.7
Release:        10%{?dist}
Epoch:          3
Summary:        IRQ balancing daemon

Group:          System Environment/Base
License:        GPLv2
Url:            https://github.com/Irqbalance/irqbalance
Source0:        https://github.com/Irqbalance/irqbalance/archive/v%{version}.tar.gz
Source1:        irqbalance.sysconfig

BuildRequires:  autoconf automake libtool libcap-ng
BuildRequires:  glib2-devel pkgconfig libcap-ng-devel
%ifnarch %{arm}
BuildRequires:  numactl-devel
Requires: numactl-libs
%endif
BuildRequires:  systemd-units
Requires(post): systemd-units
Requires(postun):systemd-units
Requires(preun):systemd-units
#Requires(triggerun):systemd-units

%define _hardened_build 1

ExclusiveArch: %{ix86} x86_64 ia64 ppc ppc64 ppc64le %{arm} aarch64

Patch1: irqbalance-1.0.4-env-file-path.patch
Patch2: irqbalance-1.0.6-man_IRQBALANCE_BANNED_CPUS.patch
Patch3: irqbalance-1.0.7-ignore_affinity_hint.patch
Patch4: irqbalance-1.0.8-removing-unused-variable-cache_stat.patch
Patch5: irqbalance-1.0.8-Manpage-note-about-ignoring-of-pid-in-some-cases.patch
Patch6: irqbalance-1.0.8-irqbalance-signal-handling-tuning.patch
Patch7: irqbalance-1.0.8-Warning-when-irqbalance-hasn-t-root-privileges.patch
Patch8: irqbalance-1.0.7-manpage-hostname.patch
Patch9: irqbalance-1.0.8-import-__bitmap_parselist-from-Linux-kernel.patch
Patch10:irqbalance-1.0.8-fix-cpulist_parse-definition-to-match-bitmap_parseli.patch
Patch11:irqbalance-1.0.8-parse-isolcpus-from-proc-cmdline-to-set-up-banned_cp.patch
Patch12:irqbalance-1.0.8-fix-memory-leak-in-classify-code.patch
Patch13:irqbalance-1.0.8-separate-cmomand-line-banned-irqs.patch
Patch14:irqbalance-1.0.8-parse-isolcpus-and-nohz-cpus-from-sysfs.patch
Patch15:irqbalance-1.0.8-Invalid-parsing-for-isolated-and-nohz_full-cpu-masks.patch
Patch16:irqbalance-1.0.9-irqbalance-set-IRQBALANCE_DEBUG-variable-implies-for.patch
Patch17:irqbalance-node-package.patch

%description
irqbalance is a daemon that evenly distributes IRQ load across
multiple CPUs for enhanced performance.

%prep
%setup -q
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

%build
./autogen.sh
%{configure}
CFLAGS="%{optflags}" make %{?_smp_mflags}

%install
install -D -p -m 0755 %{name} %{buildroot}%{_sbindir}/%{name}
install -D -p -m 0644 ./misc/irqbalance.service %{buildroot}%{_unitdir}/irqbalance.service
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}

install -d %{buildroot}%{_mandir}/man1/
install -p -m 0644 ./irqbalance.1 %{buildroot}%{_mandir}/man1/

%files
%defattr(-,root,root)
%doc COPYING AUTHORS
%{_sbindir}/irqbalance
%{_unitdir}/irqbalance.service
%{_mandir}/man1/*
%config(noreplace) %{_sysconfdir}/sysconfig/irqbalance

%post
%systemd_post irqbalance.service

%preun
%systemd_preun irqbalance.service

%postun
%systemd_postun_with_restart irqbalance.service

%triggerun -- irqbalance < 2:0.56-3
if /sbin/chkconfig --level 3 irqbalance ; then
    /bin/systemctl enable irqbalance.service >/dev/null 2>&1 || :
fi
/sbin/chkconfig --del irqbalance >/dev/null 2>&1 || :

%changelog
* Thu Mar 29 2018 Pablo Greco <pablo@fliagreco.com.ar> - 3:1.0.7-10
- Fix build on armhfp

* Tue May 16 2017 Petr Oros <poros@redhat.com> - 3:1.0.7-10
- irqbalance node package patch
- Resolves: #1444195

* Tue Apr 4 2017 Petr Oros <poros@redhat.com> - 3:1.0.7-9
- set IRQBALANCE_DEBUG variable implies foreground mode
- Resolves: #1361211

* Tue Dec 20 2016 Petr Oros <poros@redhat.com> - 3:1.0.7-8
- Fix Epoch in version
- Resolves: #1393539

* Wed Nov 30 2016 Petr Oros <poros@redhat.com> - 2:1.0.7-7
- Fix Invalid parsing for isolated and nohz_full cpu masks
- Resolves: #1393539

* Tue Feb 02 2016 Petr Holasek <pholasek@redhat.com> - 2:1.0.7-6
- nohz and isolated cpus are read from sysfs (#1264130)

* Mon Jul 13 2015 Petr Holasek <pholasek@redhat.com> - 2:1.0.7-5
- banned irqs aren't touched (#1237356)

* Fri Jun 12 2015 Petr Holasek <pholasek@redhat.com> - 2:1.0.7-4
- fixed memory leak in pci bus parsing code (#1225319)

* Tue May 05 2015 Petr Holasek <pholasek@redhat.com> - 2:1.0.7-3
- fixed putting irqs on isolated cpus (#1201552)

* Tue Jan 06 2015 Petr Holasek <pholasek@redhat.com> - 2:1.0.7-2
- fixed unused variable revealed by covscan
- fixed ignored pid argument (#1155632)
- warning when irqbalance started under non-root (#1155799)
- more robust signal handling (#1158937)
- fixed hostname in manpage (#1162251)

* Tue Aug 19 2014 Petr Holasek <pholasek@redhat.com> - 2:1.0.7-1
- Rebased to version 1.0.7 (#1018140)

* Mon Aug 04 2014 Petr Holasek <pholasek@redhat.com> - 2:1.0.6-7
- ppc64le has been added to exclusive archs (#1125551)

* Tue Jul 29 2014 Petr Holasek <pholasek@redhat.com> - 2:1.0.6-6
- aarch64 has been added to exclusive archs (#1055729)

* Mon Feb 10 2014 Petr Holasek <pholasek@redhat.com> - 2:1.0.6-5
- Fixed irqbalance web adresses in spec (bz1060810)
- Default hintpolicy adjusted (bz1060814)
- Missing autogen.sh call fixed

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2:1.0.6-4
- Mass rebuild 2013-12-27

* Thu Oct 31 2013 Petr Holasek <pholasek@redhat.com> - 2:1.0.6-3
- Fixed env variable man page description (bz1020633)

* Tue Sep 10 2013 Petr Holasek <pholasek@redhat.com> - 2:1.0.6-2
- Fixed CPU hotplug/hotunplug sigsegv (bz998494)

* Mon Aug 12 2013 Petr Holasek <pholasek@redhat.com> - 2:1.0.6-1
- Rebased to version 1.0.6 (bz996171)

* Tue Jul 30 2013 Petr Holasek <pholasek@redhat.com> - 2:1.0.5-5
- Man page and --help output were fixed (bz948372)

* Fri Jul 26 2013 Petr Holasek <pholasek@redhat.com> - 2:1.0.5-4
- Hardened build

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Petr Holasek <pholasek@redhat.com> - 2:1.0.5-1
- Rebased to version 1.0.5

* Wed Aug 29 2012 Petr Holasek <pholasek@redhat.com> - 2:1.0.4-2
- Env file path edited

* Mon Aug 27 2012 Petr Holasek <pholasek@redhat.com> - 2:1.0.4-1
- Rebased to version 1.0.4

* Wed Aug 22 2012 Petr Holasek <pholasek@redhat.com> - 2:1.0.3-5
- Make irqbalance scan for new irqs when it detects new irqs (bz832815)
- Fixes SIGFPE crash for some banning configuration (bz849792)
- Fixes affinity_hint values processing (bz832815)
- Adds banirq and bansript options (bz837049)
- imake isn't needed for building any more (bz844359)
- Fixes clogging of syslog (bz837646)
- Added IRQBALANCE_ARGS variable for passing arguments via systemd(bz837048)
- Fixes --hint-policy=subset behavior (bz844381)

* Sun Apr 15 2012 Petr Holasek <pholasek@redhat.com> - 2:1.0.3-4
- Updated libnuma dependencies

* Sun Feb  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2:1.0.3-3
- Build on ARM

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 02 2011 Neil Horman <nhorman@redhat.com> - 2:1.0.3-1
- Updated to latest upstream release

* Fri Nov 04 2011 Neil Horman <nhorman@redhat.com> - 2:1.0.2-1
- Updated to latest upstream release

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.0-4
- Rebuilt for glibc bug#747377

* Fri Oct 21 2011 Neil Horman <nhorman@redhat.com> - 2:1.0-3
- Fix another crash on non-numa systems (bz 748070)

* Mon Oct 17 2011 Neil Horman <nhorman@redhat.com> - 2:1.0-2
- Fix crash for systems with no numa node support

* Wed Oct 12 2011 Neil Horman <nhorman@redhat.com> - 2:1.0-1
- Update irqbalance to latest upstream version

* Fri May  6 2011 Bill Nottingham <notting@redhat.com> - 2:0.56-4
- fix upgrade trigger

* Fri Apr  8 2011 Peter Robinson <pbrobinson@gmail.com> - 2:0.56-3
- Fix build in rawhide
- Add license file to rpm
- Cleanup spec file

* Fri Mar 25 2011 Anton Arapov <anton@redhat.com> - 2:0.56-3
- rework init in order to respect systemd. (bz 659622)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jun 10 2010 Neil Horman <nhorman@redhat.com> - 2:0.56-1
- Updated to latest upstream version

* Wed Sep 09 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-25
- Fixing BuildRequires

* Fri Sep 04 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-24
- Fixing irqbalance initscript (bz 521246)

* Wed Sep 02 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-23
- Fixing BuildRequires for new config script

* Tue Sep 01 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-22
- Fixing BuildRequires for new config script

* Tue Sep 01 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-21
- Fixing BuildRequires for new config script

* Tue Sep 01 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-20
- Fixing BuildRequires for new config script

* Tue Sep 01 2009 Neil Horman <nhorman@redhat.com> - 2:0.55-19
- Incorporate capng (bz 520699)

* Fri Jul 31 2009 Peter Lemenkov <lemenkov@gmail.com> - 2:0.55-18
- Added back accidentaly forgotten imake

* Fri Jul 31 2009 Peter Lemenkov <lemenkov@gmail.com> - 2:0.55-17
- Cosmetic fixes in spec-file
- Fixed rpmlint error in the init-script

* Tue Jul 28 2009 Peter Lemenkov <lemenkov@gmail.com> - 2:0.55-16
- Many imrovements in spec-file

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.55-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 6 2009 Neil Horman <nhorman@redhat.com>
- Update spec file to build for i586 as per new build guidelines (bz 488849)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.55-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Dec 12 2008 Neil Norman <nhorman@redhat.com> - 2:0.55-12
- Remove odd Netorking dependence from irqbalance (bz 476179)

* Fri Aug 01 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2:0.55-11
- fix license tag

* Wed Jun 04 2008 Neil Horman <nhorman@redhat.com> - 2:0.55-10
- Update man page to explain why irqbalance exits on single cache (bz 449949)

* Tue Mar 18 2008 Neil Horman <nhorman@redhat.com> - 2:0.55-9
- Rediff pid-file patch to not remove initial parse_cpu_tree (bz 433270)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2:0.55-8
- Autorebuild for GCC 4.3

* Thu Nov 01 2007 Neil Horman <nhorman@redhat.com> - 2:0.55-7
- Update to properly hadndle pid files (bz 355231)

* Thu Oct 04 2007 Neil Horman <nhorman@redhat.com> - 2:0.55-6
- Fix irqbalance init script (bz 317219)

* Fri Sep 28 2007 Neil Horman <nhorman@redhat.com> - 2:0.55-5
- Install pie patch
- Grab Ulis cpuparse cleanup (bz 310821)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2:0.55-4
- Rebuild for selinux ppc32 issue.

* Thu Jul 05 2007 Neil Horman <nhorman@redhat.com> - 0.55.3
- Fixing LSB requirements (bz 246959)

* Tue Dec 12 2006 Neil Horman <nhorman@redhat.com> - 0.55-2
- Fixing typos in spec file (bz 219301)

* Tue Dec 12 2006 Neil Horman <nhorman@redhat.com> - 0.55-1
- Updating to version 0.55

* Mon Dec 11 2006 Neil Horman <nhorman@redhat.com> - 0.54-1
- Update irqbalance to new version released at www.irqbalance.org

* Wed Nov 15 2006 Neil Horman <nhorman@redhat.com> - 1.13-8
- Add ability to set default affinity mask (bz 211148)

* Wed Nov 08 2006 Neil Horman <nhorman@redhat.com> - 1.13-7
- fix up irqbalance to detect multicore (not ht) (bz 211183)

* Thu Nov 02 2006 Neil Horman <nhorman@redhat.com> - 1.13-6
- bumping up MAX_INTERRUPTS to support xen kernels
- rediffing patch1 and patch3 to remove fuzz

* Tue Oct 17 2006 Neil Horman <nhorman@redhat.com> - 1.13-5
- Making oneshot mean oneshot always (bz 211178)

* Wed Sep 13 2006 Peter Jones <pjones@redhat.com> - 1.13-4
- Fix subsystem locking

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 1.13-2
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)
- Remove hack to use cvs checkin ID as release as it doesn't follow
  packaging guidelines

* Tue Aug 01 2006 Neil Horman <nhorman@redhat.com>
- Change license to GPL in version 0.13

* Sat Jul 29 2006 Dave Jones <davej@redhat.com>
- identify a bunch more classes.

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Tue Jul 11 2006 Dave Jones <davej@redhat.com>
- Further lazy rebalancing tweaks.

* Sun Feb 26 2006 Dave Jones <davej@redhat.com>
- Don't rebalance IRQs where no interrupts have occured.

* Sun Feb 12 2006 Dave Jones <davej@redhat.com>
- Build for ppc[64] too.

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild with gcc4

* Tue Feb  8 2005 Dave Jones <davej@redhat.com>
- Build as pie, also -D_FORTIFY_SOURCE=2

* Tue Jan 11 2005 Dave Jones <davej@redhat.com>
- Add missing Obsoletes: kernel-utils.

* Mon Jan 10 2005 Dave Jones <davej@redhat.com>
- Start irqbalance in runlevel 2 too. (#102064)

* Sat Dec 18 2004 Dave Jones <davej@redhat.com>
- Initial packaging, based on kernel-utils.

