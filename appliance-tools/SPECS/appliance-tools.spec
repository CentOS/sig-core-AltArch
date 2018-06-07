%{!?python2_sitelib: %global python2_sitelib %(%{__python} -c "import distutils.sysconfig as d; print d.get_python_lib()")}

%define debug_package %{nil}

Name: appliance-tools
Summary: Tools for building Appliances
Version: 008.0
Release: 8%{?dist}
License: GPLv2
Group: System Environment/Base
URL: https://pagure.io/appliance-tools

Source0: https://releases.pagure.org/%{name}/%{name}-%{version}.tar.bz2

# Patches backported from upstream
Patch0: 0001-Set-releasever.patch
Patch1: 0002-Make-it-possible-to-disable-compression.patch
Patch3: 0001-Use-block-size-with-xz-to-make-seekable-xz-compresse.patch
Patch4: 0001-Remove-usage-of-kickstart.get_modules-rhbz-1544075.patch

Patch9999: 9999-revert-bca4b0df03b2831c31ace011fdcf3c6e73c9df66.patch

# Ensure system deps are installed (rhbz#1409536)
Requires: python-imgcreate
Requires: python-urlgrabber
Requires: curl rsync kpartx
Requires: zlib
Requires: qemu-img
Requires: xz
Requires: xfsprogs
Requires: sssd-client
BuildRequires: python2-devel
BuildRequires: /usr/bin/pod2man
BuildArch: noarch


%description
Tools for generating appliance images on Fedora based systems including
derived distributions such as RHEL, CentOS and others.

%prep
%autosetup -p1

%build
make

%install
%make_install

# Removing license as we'll mark it as license file later
rm -fv %{buildroot}%{_pkgdocdir}/COPYING

%files
%doc README
%doc config/fedora-aos.ks
%license COPYING
%{_mandir}/man*/*
%{_bindir}/appliance-creator
%{_bindir}/ec2-converter
%dir %{python2_sitelib}/appcreate
%dir %{python2_sitelib}/ec2convert
%{python2_sitelib}/appcreate/*
%{python2_sitelib}/ec2convert/*
/usr/share/doc/appliance-tools/COPYING
/usr/share/doc/appliance-tools/README

%changelog
* Thu Jun  7 2018 Pablo Greco <pablo@fliagreco.com.ar> - 008.0-8
- Revert patches to make it work on el7

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 008.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 15 2017 Iryna Shcherbina <ishcherb@redhat.com> - 008.0-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 008.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 12 2017 Neal Gompa <ngompa13@gmail.com> - 008.0-4
- Use 16 MiB block size for xz compression (#984704)

* Tue Feb 28 2017 Neal Gompa <ngompa13@gmail.com> - 008.0-3
- Backport patches to make more RPi friendly (#1270606)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 008.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Feb 04 2017 Neal Gompa <ngompa13@gmail.com> - 008.0-1
- Dropped merged patches
- Moved to pagure
- Modernize spec and fix changelog entries

* Mon Jan 02 2017 Neal Gompa <ngompa13@gmail.com> - 007.8-14
- Add missing Epoch for python-imgcreate dependency (#1409650)

* Mon Jan 02 2017 Neal Gompa <ngompa13@gmail.com> - 007.8-13
- Bump python-imgcreate dependency to ensure system deps are installed (#1409536)

* Mon Dec 19 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 007.8-12
- Add missing python-urlgrabber dependency (RHBZ #1405942)

* Tue Dec 06 2016 Neal Gompa <ngompa13@gmail.com> 007.8-11
- Change dependency from livecd-tools to python-imgcreate
- Fix for python-imgcreate v24 compatibility

* Tue Sep 20 2016 Peter Robinson <pbrobinson@fedoraproject.org> 007.8-10
- Fix swap partition type creation
- Set boot partition as bootable

* Sat Sep 17 2016 Peter Robinson <pbrobinson@fedoraproject.org> 007.8-9
- Allow 4 primary partitions

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 007.8-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 007.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Oct 11 2015 Lubomir Rintel <lkundrak@v3.sk> - 007.8-6
- Add a dependency on sssd-client
- Remove thincrust.org references

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 007.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Aug 21 2014 Dennis Gilmore <dennis@ausil.us> - 007.8-4
- add a hack to preload the sss nss library

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 007.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 26 2014 Dennis Gilmore <dennis@ausil.us> - 007.8-1
- drop image-minimiser
- change partitioning alignment to be optimal rhbz#990469
- change default timeout in extlinux config
* Wed Mar 05 2014 Dennis Gilmore <dennis@ausil.us> - 007.7-2
- Require xfsprogs

* Tue Feb 11 2014 Dennis Gilmore <dennis@ausil.us> - 007.7-1
- make sure the package list is available when we need it

* Tue Feb 11 2014 Dennis Gilmore <dennis@ausil.us> - 007.6-1
- use a slightly different path for extlinux-bootloader package

* Mon Feb 10 2014 Dennis Gilmore <dennis@ausil.us> - 007.5-1
- arm needs extlinux-bootloader to provide for extlinux support 
- not syslinux-extlinux

* Mon Aug 26 2013 Dennis Gilmore <dennis@ausil.us> - 007.4-1
- refacter how re deal with each mount point old version did not handle swap

* Mon Aug 26 2013 Dennis Gilmore <dennis@ausil.us> - 007.3-1
- make sure that we only have a single instance of each mount point

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 007.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Dennis Gilmore <dennis@ausil.us> - 007.2-1
- fix up call to xz

* Fri Jun 21 2013 Dennis Gilmore <dennis@ausil.us> - 007.1-1
- xz compress raw images

* Fri Jun 07 2013 Dennis Gilmore <dennis@ausil.us> - 007.0-1
- specify filesystem type when creating partitions
- extlinux fixes from mattdm
- dont use -F 32 when making vfat partition

* Thu May 23 2013 Dennis Gilmore <dennis@ausil.us> - 006.6-1
- really start at 1mb
- compress qcow2 by default
- make sure we dont destroy our newly created vfat partition

* Wed May 22 2013 Dennis Gilmore <dennis@ausil.us> - 006.5-2
- add patch to read vfat uuid earlier
- leave first mb free

* Sun May 19 2013 Dennis Gilmore <dennis@ausil.us> - 006.5-1
- fix writing out kickstart file

* Sat May 18 2013 Dennis Gilmore <dennis@ausil.us> - 006.4-1
- write out kickstart file
- correctly write out extlinux config
- dont require --ondisk for partitions

* Sun May 12 2013 Dennis Gilmore <dennis@ausil.us> - 006.3-2
- add patch for typo fixes in extlinux config from mattdm

* Fri May 10 2013 Dennis Gilmore <dennis@ausil.us> - 006.3-1.1
- BuildRequires: /usr/bin/pod2man

* Fri May 10 2013 Dennis Gilmore <dennis@ausil.us> - 006.3-1
- update to 006.3
- use UUID's for fstab and root lines
- support making vfat partition for /boot/uboot
- support extlinux as a bootloader

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 006.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Aug 09 2012 Marek Goldmann <mgoldman@redhat.com> - 006.2-1
- Upstream release 006.2

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 006.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 13 2012 Dennis Gilmore <dennis@ausil.us> - 006.1-3
- add patch to always write out a legacy grub config file

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 006.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 11 2011 Marek Goldmann <mgoldman@redhat.com> - 006.1-1
- Upstream release 006.1
- Search for grub files also in ARCH-pc directories

* Fri Nov 11 2011 Marek Goldmann <mgoldman@redhat.com> - 006-1
- Support for GRUB2 rhbz#744390
- Align partitions by default
- Search for grub files also in ARCH-unknown directories
- Allow to build appliances without GRUB installed at all

* Sat Oct 29 2011 Dennis Gilmore <dennis@ausil.us> - 005-1.nogrubhack.2
- update hack to work around no grub being installed so we can compose ec2 images

* Sat Oct 29 2011 Dennis Gilmore <dennis@ausil.us> - 005-1.nogrubhack
- add a hack to work around no grub being installed so we can compose ec2 images

* Mon Apr 04 2011 Alan Pevec <apevec@redhat.com> 005-1
- image-minimizer: support drop-keep-drop
- image-minimizer: add droprpm/keeprpm
- Added sub-package for image minimizer (dhuff)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 004.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 20 2010 Adam Tkac <atkac redhat com> - 004.5-1
- rebuild to ensure NVR in F14 is bigger than in F13
- merge following changes from F12 branch [David Huff]:
  - Fixed error while installing grub
  - Fixed issue with Fedora 12 using dracut to generate initrd
  - Fixed issue with Fedora 12 parted error

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 004.4-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 004.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 07 2009 David Huff <dhuff@redhat.com> -004.4
- added functionality include additional modules in ramdisk 

* Mon Dec 01 2008 David Huff <dhuff@redhat.com> -004.2
- changed form ExclusiveArch to EcludeArch to fix broken deps

* Mon Dec 01 2008 David Huff <dhuff@redhat.com> - 004
- bumped version for rebuild for Python 2.6
- Allow the user to pass in --version and --release command line paramneters (bkearney)
- Patches to integrate ec2 conversion into the adk (bkeareny)
- Allow the appliance-creator to use remote urls with the new image tools (bkearney)

* Fri Nov 14 2008 David Huff <dhuff@redhat.com> - 003.9
- Fixed bug in globbing files under a directory (pmyers)

* Fri Nov 14 2008 David Huff <dhuff@redhat.com> - 003.8
- Fixed bug that causes appliance-creator to stacktrace when -i is omitted (pmyers)

* Wed Nov 12 2008 David Huff <dhuff@redhat.com> - 003.7
- Fixed problem with -i only taking one file, now can include a dir
- Fixed versioning of source file, ie. 003.7

* Mon Nov 10 2008 David Huff <dhuff@redhat.com> - 003-6
- Fixed broken dependencies for specific archs where qemu is not available

* Fri Nov 07 2008 David Huff <dhuff@redhat.com> - 003-5
- Added error for Incomplete partition info (#465988)
- Fixed problem with long move operations (#466278)
- Fixed error converting disk formats (#464798)
- Added support for tar archives (#470292)
- Added md5/sha256 disk signature support (jboggs)
- Modified zip functionality can now do with or with out 64bit ext.
- Added support for including extra file in the package (#470337)
- Added option for -o outdir, no longer uses name
- OutPut is now in a seprate dir under appliance name

* Wed Sep 17 2008 David Huff <dhuff@redhat.com> - 003-4
- Removed all the kickstart files in the config dir to mirror livecd-tools
- Added the image minimization to the refactored code (BKearney)
- multiple interface issue (#460922)
- added --format option to specity disk image format
- added --package option to specify output, currently only .zip supported
- added --vmem and --vcpu options
- Merged ec2-converter code (jboggs)

* Tue Aug 26 2008 David Huff <dhuff@redhat.com> - 003-3
- release 3 fixes minor build errors 

* Wed Jul 09 2008 David Huff <dhuff@redhat.com> - 003-1
- version 003 is build for latest version of livecd-tools with patches

* Wed Jul 09 2008 Alan Pevec <apevec@redhat.com> 002-1
- import imgcreate.fs refactoring and other changes
  to make it work with Fedora-9 livecd-tools-0.17.1 w/o Thincrust patches
- version 002 is for f9 branch to work with stock f9 livecd-tools

* Wed Jun 11 2008 David Huff <dhuff@redhat.com> - 001-3
- fixed dependancys

* Tue Jun 10 2008 David Huff <dhuff@redhat.com> - 001-2
- Undated opt parser
- fixed grub issue
- build aginsted newer livecd-tools for selinux issues

* Wed May 14 2008 David Huff <dhuff@redhat.com> - 001
- Initial build.


