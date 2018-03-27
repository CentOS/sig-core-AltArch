Name: grubby
Version: 8.28
Release: 23%{?dist}
Summary: Command line tool for updating bootloader configs
Group: System Environment/Base
License: GPLv2+
URL: http://git.fedorahosted.org/git/grubby.git
Source0: https://git.fedorahosted.org/cgit/grubby.git/snapshot/%{name}-%{version}-1.tar.bz2
Source1: prune_debug
Patch0001: 0001-Only-set-RPM_OPT_FLAGS-if-undefined.patch
Patch0002: 0002-If-we-re-using-multiboot-add-a-new-mbmodule-not-an-i.patch
Patch0003: 0003-Use-PREFIX-during-make-install.patch
Patch0004: 0004-Honor-linux16-and-initrd16.patch
Patch0005: 0005-If-we-re-on-a-zipl-based-platform-use-banner-passed-.patch
Patch0006: 0006-Support-devicetree-directive-in-grub2.patch
Patch0007: 0007-Actually-USE-DEVTREE-in-new-kernel-pkg.patch
Patch0008: 0008-Use-the-correct-load-commands-for-aarch64-efi.patch
Patch0009: 0009-Always-choose-linux-initrd-on-efi-only-platforms.patch
Patch0010: 0010-extlinux-Understand-default-properly.patch
Patch0011: 0011-extlinux-Add-test-suite.patch
Patch0012: 0012-grub-Fix-a-crash-with-kernel-line-without-being-prec.patch
Patch0013: 0013-grub-Remove-a-redundant-test.patch
Patch0014: 0014-Fix-bad-check-for-new-kernel-pkg-s-command-line-argu.patch
Patch0015: 0015-Previous-ARM-64-bit-test-had-the-wrong-compiler-defi.patch
Patch0016: 0016-Actually-do-a-fix-for-rhbz-1082318-that-fixes-the-is.patch
Patch0017: 0017-Strip-the-LT_END-line-from-a-new-stanza-before-addin.patch
Patch0018: 0018-Fix-a-wrong-test-case-lacked-boot-filesystem.patch
Patch0019: 0019-Don-t-go-past-the-last-element-of-indexVars-in-findE.patch
Patch0020: 0020-Tell-a-slightly-better-fib-about-default-bootloader-.patch
Patch0021: 0021-Make-findTemplate-actually-return-the-saved-default.patch
Patch0022: 0022-Support-filtering-update-kernel-by-title-as-well.patch
Patch0023: 0023-Conditionally-create-debug-entries-when-installing-k.patch
Patch0024: 0024-Always-error-check-getLineByType.patch
Patch0025: 0025-Get-the-error-checking-on-getLineByType-return-right.patch
Patch0026: 0026-Fix-ppc-kernelName-when-invoked-by-installkernel.patch
Patch0027: 0027-Update-grubby-man-page-for-Power8-PPC64LE.patch
Patch0028: 0028-Update-man-page-to-include-default-config-file-for-s.patch
Patch0029: 0029-Split-the-test-case-for-rescue-images-into-tests-wit.patch
Patch0030: 0030-Actually-get-the-test-from-a7800d8f-right.patch
Patch0031: 0031-Strdup-the-right-place-in-title-extraction.patch
Patch0032: 0032-Make-the-cases-for-0cb78dab-actually-work-not-just-n.patch
Patch0033: 0033-grub2ExtractTitle-and-extractTitle-don-t-do-the-same.patch
Patch0034: 0034-Set-envFile-from-env-when-bootloader-is-not-specifie.patch
Patch0035: 0035-grubby-properly-handle-mixed-and-and-nested-quotes.patch
Patch0036: 0036-Don-t-put-spaces-in-debug-entries-on-zipl-platforms.patch
Patch0037: 0037-Drop-SEGV-handler.patch
Patch0038: 0038-Add-a-bunch-of-tests-for-various-default-kernel-titl.patch
Patch0039: 0039-Emit-better-systemd-debug-settings-on-debug-entries.patch
Patch0040: 0040-Make-the-grub1-defaultkernel-test-more-reliable.patch
Patch0041: 0041-Work-around-aarch64-not-having-quite-the-same-grub-c.patch
Patch0042: 0042-ppc64le-sync-grub.cfg-changes-to-disk-1212114.patch
Patch0043: 0043-Make-it-possible-to-run-test.sh-verbose-from-the-mak.patch
Patch0044: 0044-Don-t-leak-from-one-extractTitle-call.patch
Patch0045: 0045-Better-formatting.patch
Patch0046: 0046-Make-SET_VARIABLE-get-handled-individually-in-GetNex.patch
Patch0047: 0047-Specify-bootloader-directory-in-the-test-case-for-11.patch
Patch0048: 0048-Fix-some-coverity-concerns.patch
Patch0049: 0049-Always-do-the-rungrubby-debug-after-the-normal-kerne.patch
Patch0050: 0050-grubby-add-set-index-to-specify-which-position-to-ad.patch
Patch0051: 0051-Fix-thinko-on-set-index-naming.patch
Patch0052: 0052-Fix-a-typo-on-the-rhel-7.3-branch.patch
Patch0053: 0053-Add-a-test-case-for-a-failure-rmarshall-saw-in-set-i.patch
Patch0054: 0054-Ensure-command-line-updates-also-honor-set-index.patch
Patch0055: 0055-Change-debug-entry-insertion-order-rhbz-1285601.patch
Patch0056: 0056-Reorganize-grubby-man-page-1232168.patch
Patch0057: 0057-Update-grubby-man-page-contents-bz1232168.patch
Patch0058: 0058-Fix-inline-help-typo-1232168.patch
Patch0059: 0059-More-edits-for-grubby.8-1232168.patch
Patch0060: 0060-Minor-man-page-changes-1232168.patch
Patch0061: 0061-Rename-setDefaultImage-variables.patch
Patch0062: 0062-Add-index-constant-definitions-instead-of-open-coded.patch
Patch0063: 0063-Track-configuration-modifications.patch
Patch0064: 0064-Fix-some-test-cases-where-the-resulting-default-inde.patch
Patch0065: 0065-Don-t-assume-make-default-just-because-set-index-was.patch
Patch0066: 0066-Clarify-set-default-index-in-the-man-page.patch
Patch0067: 0067-Add-multi-entry-removal-test-1285601.patch
Patch0068: 0068-Fix-findTemplate-index-logic-1285601.patch
Patch0069: 0069-Write-correct-default-to-environment-1285601.patch
Patch0070: 0070-Initialize-variable-for-ppc-environment-1285601.patch
Patch0071: 0071-Fix-initial-saved_entry-read-issue-1285601.patch
Patch0072: 0072-Add-s390-s390x-info-test-1285601.patch
Patch0073: 0073-Fix-info-for-s390x-s390-1285601.patch
Patch0074: 0074-Add-s390-s390x-set-default-index-test-1285601.patch
Patch0075: 0075-Fix-setDefaultImage-for-s390-s390x-1285601.patch

##only for arm
Patch1000: 1000-Update-extlinux.conf-with-sed-instead-of-backporting.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig glib2-devel popt-devel 
BuildRequires: libblkid-devel git
# for make test / getopt:
BuildRequires: util-linux-ng
%ifarch aarch64 i686 x86_64 ppc ppc64
BuildRequires: /usr/bin/grub2-editenv
%endif
%ifarch s390 s390x
Requires: s390utils-base
%endif
%ifarch %{arm}
Requires: uboot-tools
Requires: extlinux-bootloader
%endif
Requires: system-release

%description
grubby  is  a command line tool for updating and displaying information about 
the configuration files for the grub, lilo, elilo (ia64),  yaboot (powerpc)  
and zipl (s390) boot loaders. It is primarily designed to be used from scripts
which install new kernels and need to find information about the current boot 
environment.

%prep
%setup -q -n %{name}-%{version}-1

git init
git config user.email "noone@example.com"
git config user.name "no one"
git add .
git commit -a -q -m "%{version} baseline"
git am %{patches} </dev/null
git config --unset user.email
git config --unset user.name

%build
make %{?_smp_mflags}

%check
make test

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT PREFIX=%{_prefix} mandir=%{_mandir}
install -d -m 0755 $RPM_BUILD_ROOT/usr/libexec/grubby/
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT/usr/libexec/grubby/
%ifarch %{arm}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/
install -p uboot $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/uboot
touch $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/kernel
mkdir -p $RPM_BUILD_ROOT/boot
echo " " >> $RPM_BUILD_ROOT/boot/boot.scr
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
/usr/libexec/grubby/prune_debug

%files
%defattr(-,root,root,-)
%doc COPYING
%{_prefix}/sbin/installkernel
%{_prefix}/sbin/new-kernel-pkg
%{_prefix}/sbin/grubby
%{_mandir}/man8/*.8*
/usr/libexec/grubby/prune_debug
%ghost %config(noreplace) %{_sysconfdir}/sysconfig/kernel
%ifarch %{arm}
%config(noreplace) %{_sysconfdir}/sysconfig/uboot
%config(noreplace) /boot/boot.scr
%endif

%changelog
* Tue Mar 27 2018 pablo@fliagreco.com.ar - 8.28-23
- Add extlinux-bootloader require on armhfp

* Wed Mar 21 2018 pablo@fliagreco.com.ar - 8.28-23
- Fix fdtdir on extlinux.conf

* Tue Mar 21 2017 rmarshall@redhat.com - 8.28-23
- Fixes --info flag on s390/s390x.
  Related: rhbz#1285601
- Fixes --set-default-index on s390/s390x.
  Related: rhbz#1285601
- Allows prune_debug to run on s390/s390x.
  Resolves: rhbz#1285601

* Mon Mar 06 2017 rmarshall@redhat.com - 8.28-22
- Resolve issues found by coverity scan.
  Resolves: rhbz#1285601

* Mon Mar 06 2017 rmarshall@redhat.com - 8.28-21
- Resolve issues with the recent grubby logic patches that
  appeared on the ppc platform. Fix a problem that occurred
  on systems where no kernel update had ever been installed.
  Resolves: rhbz#1285601
- Specify the actual prune_debug file in sources.
  Resolves: rhbz#1285601

* Thu Feb 09 2017 rmarshall@redhat.com - 8.28-20
- Added invocations for prune_debug to spec file
  Resolves: #1285601

* Thu Feb 09 2017 rmarshall@redhat.com - 8.28-19
- Fixed an issue where grubby's logic set the wrong default
  boot entry.
  Resolves: #1285601

* Fri Jul 01 2016 rmarshall@redhat.com - 8.28-18
- Patched new-kernel-pkg so that kernel installations when MAKEDEBUG is
  set would put the debugging entries after the non-debugging entries.
  Resolves: #1285601
- Re-numbered the last set of patches to go with the flow. No actual
  changes to the patches; just a git mv to rename.
- Re-organized and updated the grubby man page contents to include some
  features that were not documented as well as correct typos and
  re-write some entries for better clarity.
  Resolves: #1232168

* Mon Oct 26 2015 Peter Jones <pjones@redhat.com> - 8.28-17
- Fix the ordering of creating the debug entries, so they don't get picked
  when we're choosing kernel command line defaults on upgrades.
  Related: rhbz#1212128

* Thu Sep 10 2015 Peter Jones <pjones@redhat.com> - 8.28-16
- Fix some coverity concerns and other issues with 8.28-15...
  Resolves: rhbz#1152550

* Thu Sep 10 2015 Peter Jones <pjones@redhat.com> - 8.28-15
- Fix some coverity concerns and other issues with 8.28-14 (sigh)
  Resolves: rhbz#1152550

* Tue Sep 01 2015 Peter Jones <pjones@redhat.com> - 8.28-14
- Handle "set variable" commands separately from other parsing in grubby's
  GetNextLine()
  Resolves: rhbz#1152550

* Wed Aug 05 2015 Robert Marshall <rmarshall@redhat.com> - 8.28-13
- Ensure file changes sync to disk on ppc64le platform.
  Related: rhbz#1212114

* Thu Jul 02 2015 Peter Jones <pjones@redhat.com> - 8.28-12
- Do a better job recognizing "title" and "default" position and formatting
  on extlinux
  Resolves: rhbz#1200045
- Do a better job recognizing stanza names and defaults on grub1 and grub2
  Related: rhbz#1142545
- (reordered some patches to match the ordering in master)
  Related: rhbz#1200045
  Related: rhbz#1142545
- Add test suite coverage and minor fixes related to zipl and
  --default-{kernel,index,title}
  Related: rhbz#1184014
- Use systemd debug options that work on RHEL 7
  Resolves: rhbz#1212128

* Tue Nov 11 2014 Peter Jones <pjones@redhat.com> - 8.28-11
- Fix a memory corruption issue we're hitting on s390/s390x
  Resolves: rhbz#1152152
- Don't use spaces on zipl platforms to describe debugging entries
  Related: rhbz#1152152

* Thu Sep 25 2014 Peter Jones <pjones@redhat.com> - 8.28-10
- Use the correct load commands for aarch64 efi.
  Resolves: rhbz#1081269
- Support "devicetree" directive in grub2.
  Resolves: rhbz#1063534
- Explain the default bootloaders and configuration paths slightly better
  in the manual.
  Resolves: rhbz#1001664
- Conditionally create debug entries when installing kernels.
  Resolves: rhbz#957681
- Make sure --banner from the command line is used correctly.
  Resolves: rhbz#1032048

* Thu Mar 06 2014 Peter Jones <pjones@redhat.com> - 8.28-8
- Fix crash when config file doesn't match command line.
  Related: rhbz#1070646
- Make crashes work with abrt better.
  Resolves: rhbz#1070646

* Wed Jan 29 2014 Peter Jones <pjones@redhat.com> - 8.28-7
- Update to make sure the source url is correct.
  Related: rhbz#1034743

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 8.28-6
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 8.28-5
- Mass rebuild 2013-12-27

* Fri Dec 06 2013 Peter Jones <pjones@redhat.com> - 8.28-4
- Make patch from -3 only do that on x86.
  Resolves: rhbz#1034743

* Wed Nov 27 2013 d.marlin <dmarlin@redhat.com>
- Only set RPM_OPT_FLAGS if undefined to avoid overwriting 
  the platform defaults.
  Resolves: rhbz#1023793

* Mon Nov 18 2013 Peter Jones <pjones@redhat.com> - 8.28-3
- Honor linux16 and initrd16 in grub.cfg
  Resolves: rhbz#1031192

* Fri Sep 13 2013 Peter Jones <pjones@redhat.com> - 8.28-2
- Use %%{_prefix} during "make install" (rpmdiff)

* Fri Aug 02 2013 Peter Jones <pjones@redhat.com> - 8.28-1
- More work on grub's "saved_entry" system.
  Resolves: rhbz#808021

* Tue Jul 30 2013 Peter Jones <pjones@redhat.com> - 8.27-1
- Make grubby understand grub's "saved_entry" system
  Resolves: rhbz#808021
- BuildRequire grub2 on appropriate platforms, for the test suite.
  Related: rhbz#808021

* Fri Jun 07 2013 Dennis Gilmore <dennis@ausil.us> - 8.26-2
- add patch to update extlinux.conf file on arm if it exists

* Fri May 10 2013 Peter Jones <pjones@redhat.com> - 8.26-1
- Conditionally call arm-boot-config's boot.scr generator if available
  Resolves: rhbz#952428

* Tue Apr 09 2013 Peter Jones <pjones@redhat.com> - 8.25-1
- Error instead of segfaulting if we can't find any working config
  Resolves: rhbz#912873
  Resolves: rhbz#751608

* Tue Mar 19 2013 Peter Jones <pjones@redhat.com> - 8.24-1
- Fix module remove code from Harald (#923441)

* Mon Mar 11 2013 Peter Jones <pjones@redhat.com> - 8.23-1
- Update to 8.23
- Fix empty root device in case of an empty /etc/fstab (lemenkov)
- General refactoring and cleanup (harald)
- Don't clean up modules.* so aggressively (harald)

* Wed Feb 20 2013 Peter Jones <pjones@redhat.com> - 8.22-3
- Add --debug style logging (for both success and failures) to /var/log/grubby

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Peter Jones <pjones@redhat.com> - 8.22-1
- Revert test case for rhbz#742885 - it's a work in progress that isn't
  ready yet.

* Fri Jan 04 2013 Peter Jones <pjones@redhat.com> - 8.21-1
- Use systemd vconsole.conf and locale.conf if present
  Resolves rhbz#881908
- Avoid unnecessary stat calls (from Ville Skyttä)
  Resolves rhbz#741135
- Spelling fixes (Ville Skyttä)
- Add a test case for rhbz#742885
- Handle case-insensitive extlinux config files properly (from Johannes Weiner)

* Tue Oct 02 2012 Peter Jones <pjones@redhat.com> - 8.20-1
- Handle linuxefi initrd and removal correctly.
  Resolves: rhbz#859285

* Wed Sep 26 2012 Peter Jones <pjones@redhat.com> - 8.19-1
- Don't accidentally migrate from linuxefi back to linux
  Related: rhbz#859285

* Fri Sep 21 2012 Peter Jones <pjones@redhat.com> - 8.18-1
- Change the way the kernel load address is determined for ARM U-Boot.

* Wed Aug 08 2012 Peter Jones <pjones@redhat.com> - 8.17-1
- Update to 8.17
- Fixes a "make test" failure.

* Wed Aug 08 2012 Peter Jones <pjones@redhat.com> - 8.16-1
- Update to 8.16
- Handle "linuxefi" directive on grub2/uefi machines.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Peter Jones <pjones@redhat.com> - 8.15-1
- Update to 8.15
- Revert dirname change from 8.13; it was wrong.

* Thu Jun 14 2012 Peter Jones <pjones@redhat.com> - 8.14-1
- Update to 8.14 to fix a build problem.

* Thu Jun 14 2012 Peter Jones <pjones@redhat.com> - 8.13-1
- Update to 8.13
- Add some more ARM tweaks (dmartin)
- Better support for other distros (crosa)

* Tue Jun 12 2012 Peter Jones <pjones@redhat.com> - 8.12-2
- Support UBOOT_IMGADDR override on ARM (blc)

* Thu May 31 2012 Peter Jones <pjones@redhat.com> - 8.12-1
- Update to 8.12
- Preserve trailing indentation when splitting line elements (mads)
  Resolves: rhbz#742720
- Pick last device mounted on / (pjones,bcl)
  Related: rhbz#820340
  Related: rhbz#820351

* Wed Mar 21 2012 Peter Jones <pjones@redhat.com> - 8.11-1
- Update to 8.11
  Resolves: rhbz#805310

* Thu Mar 15 2012 Peter Jones <pjones@redhat.com> - 8.10-1
- Update to 8.10
- Use "isquote" where appropriate
- Make --remove-kenrel support titles in grub2 (jianzhong.huang)
- Use grub2 if it's there on ppc.

* Fri Mar 02 2012 Peter Jones <pjones@redhat.com> - 8.9-1
- Refactor grub2 title extraction, making it a function (Cleber Rosa)
- Include prefix when printing kernel information (Cleber Rosa)
- Implement support for "default saved" for grub2 (Cleber Rosa)
- Try to display title when printing information with '--info' (Cleber Rosa)
- new-kernel-pkg fails to find U-Boot. (D. Marlin)
- Add support to new-kernel-pkg to recognize ARCH == armv5tel needed for Kir
  (D.Marlin)
- Include a / when one is missing in paths (#769641)
- Fix hard coded paths so kernel's "make install" will DTRT.
- Fix endswith() to correctly test its input for validity.

* Tue Feb 07 2012 Dennis Gilmore <dennis@ausil.us> - 8.8-3
- add uboot-tools requires on arm arches
- add uboot config file on arm arches

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Peter Jones <pjones@redhat.com> - 8.8-1
- Fix test cases from 8.7 to work on a system without /boot mounted.

* Tue Dec 20 2011 Peter Jones <pjones@redhat.com> - 8.7-1
- Add a --debug to try to help diagnose "No suitable template". (sandeen,pjones)

* Mon Dec 19 2011 Peter Jones <pjones@redhat.com> - 8.6-1
- Fix a "make test" errors introduced in 8.4-1

* Sat Dec 17 2011 Peter Jones <pjones@redhat.com> - 8.5-1
- Don't hardcode dracut path
  Resolves: #768645

* Thu Dec 08 2011 Adam Williamson <awilliam@redhat.com> - 8.4-1
- Update to 8.4:
	+ fix Loading... line for updated kernels
	+ Add new '--default-title' feature
	+ Add new '--default-index' feature
	+ add feature for testing the output of a grubby command
	+ Fix detection when comparing stage1 to MBR
	+ do not link against glib-2.0
	+ Don't crash if grubConfig not found
	+ Adding extlinux support for new-kernel-pkg
	+ Look for Debian / Ubuntu grub config files (#703260)
	+ Make grubby recognize Ubuntu's spin of Grub2 (#703260)

* Thu Sep 29 2011 Peter Jones <pjones@redhat.com> - 8.3-1
- Fix new-kernel-pkg invocation of grubby for grub (patch from Mads Kiilerich)
  Resolves: rhbz#725185

* Wed Sep 14 2011 Peter Jones <pjones@redhat.com> - 8.2-1
- Fixes for xen (from Michael Petullo)
  Resolves: rhbz#658387

* Fri Jul 22 2011 Peter Jones <pjones@redhat.com> - 8.1-1
- Update to 8.1
- Fix miss-spelled variable name in new-kernel-pkg

* Thu Jul 21 2011 Peter Jones <pjones@redhat.com> - 8.0-1
- Add support for grub2.

* Tue Jun 07 2011 Brian C. Lane <bcl@redhat.com> - 7.0.18-1
- Bump version to 7.0.18 (bcl)
- Fixup new-kernel-pkg errors (#711493) (bcl)

* Mon Jun 06 2011 Peter Jones <pjones@redhat.com> - 7.0.17-1
- Fix references to wrong program name in new-kernel-pkg.8
  Resolves: rhbz#663981

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Karsten Hopp <karsten@redhat.com> 7.0.16-2
- add BR utils-linux-ng for getopt

* Tue Jul 13 2010 Brian C. Lane <bcl@redhat.com> - 7.0.16-1
- Update to 7.0.16
- Add patch to check the return value of getuuidbydev
- Resolves: rhbz#592294

* Wed Apr 14 2010 Peter Jones <pjones@redhat.com> - 7.0.15-1
- Update to 7.0.15
- Add man pages for installkernel and new-kernel-pkg
  Resolves: rhbz#529333

* Wed Apr 14 2010 Peter Jones <pjones@redhat.com> - 7.0.14-1
- Update to 7.0.14

* Thu Feb 11 2010 Peter Jones <pjones@redhat.com> - 7.0.13-1
- Strip boot partition prefix from initrd path if present during --update.
  Related: rhbz#557922
- add host only support for local kernel compiles (airlied)

* Mon Feb 08 2010 Peter Jones <pjones@redhat.com> - 7.0.12-1
- compare rootdev using uuid instead of stat, for better btrfs support (josef)
  Resolves: rhbz#530108

* Mon Feb 08 2010 Peter Jones <pjones@redhat.com> - 7.0.11-1
- Make it possible to update the initrd without any other change.
  Related: rhbz#557922

* Fri Feb 05 2010 Peter Jones <pjones@redhat.com> - 7.0.10-1
- Make --update able to add an initramfs.
  Related: rhbz#557922

* Mon Nov 30 2009 Peter Jones <pjones@redhat.com> - 7.0.9-3
- Use s390utils-base as the s390 dep, not s390utils
  Related: rhbz#540565

* Tue Nov 24 2009 Peter Jones <pjones@redhat.com> - 7.0.9-2
- Add s390utils dep when on s390, since new-kernel-package needs it.
  Resolves: rhbz#540565

* Fri Oct 30 2009 Peter Jones <pjones@redhat.com> - 7.0.9-1
- Add support for dracut to installkernel (notting)

* Thu Oct  1 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.8-1
- Stop using nash

* Fri Sep 11 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.7-1
- Remove writing rd_plytheme=$theme to kernel args in dracut mode (hansg)
- Add a couple of test cases for extra initrds (rstrode)
- Allow tmplLine to be NULL in getInitrdVal (rstrode)

* Fri Sep 11 2009 Peter Jones <pjones@redhat.com> - 7.0.6-1
- Fix test case breakage from 7.0.5 (rstrode)

* Fri Sep 11 2009 Peter Jones <pjones@redhat.com> - 7.0.5-1
- Add support for plymouth as a second initrd. (rstrode)
  Resolves: rhbz#520515

* Wed Sep 09 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.4-1
- Add --dracut cmdline argument for %post generation of dracut initrd

* Wed Aug 26 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.3-1
- Silence error when no /etc/sysconfig/keyboard (#517187)

* Fri Aug  7 2009 Hans de Goede <hdegoede@redhat.com> - 7.0.2-1
- Add --add-dracut-args new-kernel-pkg cmdline option

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 17 2009 Jeremy Katz <katzj@redhat.com> - 7.0.1-1
- Fix blkid usage (#124246)

* Wed Jun 24 2009 Jeremy Katz <katzj@redhat.com> - 7.0-1
- BR libblkid-devel now instead of e2fsprogs-devel
- Add bits to switch to using dracut for new-kernel-pkg

* Wed Jun  3 2009 Jeremy Katz <katzj@redhat.com> - 6.0.86-2
- add instructions for checking out from git

* Tue Jun  2 2009 Jeremy Katz <katzj@redhat.com> - 6.0.86-1
- initial build after splitting out from mkinitrd

