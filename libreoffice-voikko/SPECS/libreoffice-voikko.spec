Name:           libreoffice-voikko
Version:        3.4
Release:        4%{?dist}
Summary:        Finnish spellchecker and hyphenator extension for LibreOffice

Group:          Applications/Productivity
License:        GPLv3+
URL:            http://voikko.sourceforge.net/
# The usual format of stable release URLs
Source0:        http://downloads.sourceforge.net/voikko/%{name}-%{version}.tar.gz
# The usual format of test release URLs
#Source0:        http://www.puimula.org/htp/testing/%{name}-%{version}rc2.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%global libo_version 4.0
%global libo %{_libdir}/libreoffice
%global libo_sdk %{libo}/sdk

BuildRequires:    libreoffice-sdk%{?_isa} >= %{libo_version}
BuildRequires:    libvoikko-devel%{?_isa}
Requires:         libreoffice-core%{?_isa} >= %{libo_version}
# Renamed from openffice.org-voikko
Provides:         openoffice.org-voikko = %{version}-%{release}
Obsoletes:        openoffice.org-voikko < 3.1.2-6

# The location of the installed extension. Apparently the directory name must
# end with .uno.pkg or unopkg will fail.
%define voikkoext %{libo}/share/extensions/voikko.uno.pkg

%description
This package contains a Finnish spell-checking and hyphenation component for
LibreOffice. The actual spell-checking and hyphenation functionality is
provided by the Voikko library.


%prep
%setup -q
sed -i 's|-BUCR||g' Makefile

%build
. %{libo_sdk}/setsdkenv_unix.sh
# CC_FLAGS needs to be overwritten because the default value adds an extra -O
# COMP_LINK_FLAGS needs to be overwritten because the default value adds an
# rpath
make extension-files "CC_FLAGS=-c -fpic -fvisibility=hidden" "OPT_FLAGS=$RPM_OPT_FLAGS" "COMP_LINK_FLAGS=-shared" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
# This needs to be run every time before calling make
. %{libo_sdk}/setsdkenv_unix.sh
make install-unpacked DESTDIR=$RPM_BUILD_ROOT%{voikkoext}
# Set the library executable so debuginfo can be extracted.
chmod +x $RPM_BUILD_ROOT%{voikkoext}/voikko.so


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{voikkoext}
%doc ChangeLog COPYING README


%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.4-4
- Mass rebuild 2014-01-24

* Wed Jan 08 2014 Caolán McNamara <caolanm@redhat.com> - 3.4-3
- Resolves: rhbz#1048874 fix FTBFS

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.4-2
- Mass rebuild 2013-12-27

* Sun Apr 14 2013 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.4-1
- New upstream release
- Rebuilt for LibreOffice 4.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Feb 04 2012 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.3-1
- New upstream release for LibreOffice 3.5

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 02 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.2-4
- Specify CC_FLAGS and COMP_LINK_FLAGS so that an extra -O switch and setting an
  rpath are avoided.

* Sun Sep 25 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.2-3
- Remove the versioned dependency on libvoikko
- Bump the obsoleted openoffice.org-voikko version

* Sun Sep 18 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.2-2
- Build in the build section, install in the install section
- Add the _isa macro to the libreoffice dependencies

* Sun Aug 28 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.2-1
- Package renamed from openoffice.org-voikko to libreoffice-voikko
- First upstream libreoffice-voikko release

* Tue Jul 19 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.1.2-4
- Fix FTBFS (rhbz #716053)
- Update required LibreOffice version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 30 2010 Caolán McNamara <caolanm@redhat.com> - 3.1.2-2
- rebuild for LibreOffice

* Thu Aug 05 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.1.2-1
- New upstream release
- Remove both patches, upstreamed

* Tue Jul 27 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.1-5
- Fix for rhbz #618151, switch group elements to node elements in config.xcu,
  patch by David Tardon

* Wed Jul 14 2010 Caolán McNamara <caolanm@redhat.com> - 3.1-4
- Rebuild for OpenOffice.org 3.3

* Fri Jan 22 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.1-3
- Add patch from SVN to partly fix broken configuration handling, which
  may lead to an OO.o crash (rhbz#549289)

* Thu Nov 19 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.1-2
- Update for OpenOffice.org 3.2

* Mon Aug 10 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.1-1
- Update source URL to "official" upstream and bump version accordingly.
- The tarball is the same as in RC2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-0.3.rc2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Apr 13 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.1-0.2.rc2
- New release candidate

* Mon Apr 06 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.1-0.1.rc1
- New release candidate
- Grammar checking enabled

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.0.1-2
- Rebuild for OOO310_m1
- No need to use a define for unopkg anymore

* Wed Jan 21 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.0.1-1
- openoffice.org-voikko 3.0.1
- Drop integrated OOO 3.0.1 compatibility patch
- Require OOO 3.0.1

* Sun Dec 28 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.0-5
- Add patch from upstream to fix FTBFS with OOO300_m14, the grammar
  checking framework was changed

* Wed Nov 19 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.0-4
- Add Epoch 1 to all openoffice.org-core pre-/post-Requires to avoid bugs such
  as rhbz #472093 (incorrect openoffice.org-core dependency)

* Mon Oct 13 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.0-3
- Remove unneeded openoffice.org-core Requires, rpmbuild should detect that
  automatically. Keep libvoikko >= 2.0 Requires as instructed by upstream
  release notes, rpmbuild can't detected that automatically.

* Mon Oct 06 2008 Caolán McNamara <caolanm@redhat.com> - 3.0-2
- add --force to protect against installing by rpm an extension which was
  previously installed manually

* Thu Aug 28 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.0-1
- openoffice.org-voikko 3.0

* Wed Jul 30 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.0-0.2.rc1
- New release candidate:
  - Require libvoikko >= 2.0
  - Don't build with SHOW_UGLY_WARNINGS anymore

* Fri Jul 25 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.0-0.1.pre4
- New pre-release
- License changed to GPLv3+
- Require openoffice.org >= 3.0.0
- Drop unneeded 3 layer patch
- Build with new SHOW_UGLY_WARNINGS=1 option as this is a test release

* Tue Jun 03 2008 Caolán McNamara <caolan@redhat.com> - 2.2-5
- add openoffice.org-voikko-2.2-3layer.patch to build against 3 layer OOo

* Sat Apr 26 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2-4
- Build with RPM_OPT_FLAGS, adds FORTIFY_SOURCE etc.

* Thu Apr 03 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2-3
- Update the package to match the newest extension guidelines:
  - Change location
  - Update openoffice.org-* Requires

* Sun Feb 17 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2-2
- Upstream released 2.2
- Remove the "temporary $HOME hack" and all -env options, since unopkg has 
  been patched to take care of all that

* Tue Feb 12 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2-0.2.rc1
- Use the package name, not a Debian leftover environment variable as an mktemp
  template

* Mon Feb 11 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2-0.1.rc1
- 2.2rc1
- Use new install-unpacked make target, no need to unzip the extension
  anymore
- This target both compiles and installs, so do everything in install and
  leave build empty
- Set $HOME to be a temporary directory while using unopkg. Otherwise unopkg
  causes problems if the package is installed with sudo
- Rebuild for GCC 4.3

* Wed Jan 23 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-1
- Bump release for the initial Fedora build

* Mon Jan 21 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-0.2
- Make one define a bit cleaner
- Changes by Caolán McNamara:
  - Unpack the component at install time
  - Make a non-empty debuginfo package
  - Install the extension to /usr/lib/

* Mon Jan 21 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-0.1
- Initial package
