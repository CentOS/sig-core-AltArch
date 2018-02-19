Summary: The GNU Scientific Library for numerical analysis
Name: gsl
Version: 1.15
Release: 13%{?dist}
URL: http://www.gnu.org/software/gsl/
Source: ftp://ftp.gnu.org/gnu/gsl/%{name}-%{version}.tar.gz
Patch0: gsl-1.10-lib64.patch
Patch1: gsl-1.14-link.patch
Patch2: gsl-1.15-atlas.patch
#ode-initval2 upstream patches up to revision 4788
Patch3: gsl-1.15-odeinitval2_upstream_rev4788.patch
# info part of this package is under GFDL license
# eigen/nonsymmv.c and eigen/schur.c
# contains rutiens which are part of LAPACK - under BSD style license
License: GPLv3 and GFDL and BSD
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: pkgconfig
BuildRequires: atlas-devel

%description
The GNU Scientific Library (GSL) is a collection of routines for
numerical analysis, written in C.

%package devel
Summary: Libraries and the header files for GSL development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info 
Requires: pkgconfig, automake

%description devel
The gsl-devel package contains the header files necessary for 
developing programs using the GSL (GNU Scientific Library).

%prep
%setup -q
%patch0 -p1 -b .lib64
%patch1 -p1 -b .libs
%patch2 -p1 -b .atlas
%patch3 -p1 -b .ode
iconv -f windows-1252 -t utf-8 THANKS  > THANKS.aux
touch -r THANKS THANKS.aux
mv THANKS.aux THANKS

%build
%configure CFLAGS="$CFLAGS -fgnu89-inline"
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags} LDFLAGS="$LDFLAGS -L%{_libdir}/atlas/"

%check
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}:$LD_LIBRARY_PATH
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT install='install -p'
# remove unpackaged files from the buildroot
rm -rf $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# remove static libraries
rm -r $RPM_BUILD_ROOT%{_libdir}/*.a


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post devel
if [ -f %{_infodir}/gsl-ref.info.gz ]; then
    /sbin/install-info %{_infodir}/gsl-ref.info %{_infodir}/dir || :
fi

%preun devel
if [ "$1" = 0 ]; then
    if [ -f %{_infodir}/gsl-ref.info.gz ]; then
	/sbin/install-info --delete %{_infodir}/gsl-ref.info %{_infodir}/dir || :
    fi
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README THANKS TODO
%{_libdir}/*so.*
%{_bindir}/gsl-histogram
%{_bindir}/gsl-randist
%{_mandir}/man1/gsl-histogram.1*
%{_mandir}/man1/gsl-randist.1*

%files devel
%defattr(-,root,root,-)
%doc AUTHORS COPYING
%{_bindir}/gsl-config*
%{_datadir}/aclocal/*
%{_includedir}/*
%{_infodir}/*info*
%{_libdir}/*.so
%{_libdir}/pkgconfig/gsl.pc
%{_mandir}/man1/gsl-config.1*
%{_mandir}/man3/*.3*

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.15-13
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.15-12
- Mass rebuild 2013-12-27

* Tue Sep 24 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.15-11
- resolves: #1009067
- linked against atlas 3.10.1

* Wed Jan 30 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.15-8
- self test moved to %%check section

* Tue Jan 29 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.15-7
- run self-tests after build
- updated ode-initval2 to upstream revision 4788

* Mon Nov 19 2012 Frantisek Kluknavsky <fkluknav@redhat.com> - 1.15-6
- minor cleanup of gsl.spec

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Sep 27 2011 Peter Schiffer <pschiffe@redhat.com> - 1.15-3
- resolves: #741138
  removed unnecessary Requires: atlas

* Mon May  9 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 1.15-2
- resolves: #695148
  link gsl against atlas package for blas operations

* Mon May  9 2011 Ivana Hutarova Varekova <varekova@redhat.com> - 1.15-1
- update to 1.15

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed May  5 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.14-1
- update to 1.14
- Resolves: #560219
             Library not linked correctly

* Wed Mar  3 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.13-2
- remove the static subpackage

* Tue Sep 15 2009 Ivana Varekova <varekova@redhat.com> - 1.13-1
- update to 1.13

* Mon Aug 17 2009 Ivana Varekova <varekova@redhat.com> - 1.12-6
- fix preun and post scripts (#517568)

* Mon Aug 10 2009 Ivana Varekova <varekova@redhat.com> - 1.12-5
- fix installation with --excludedocs option (#515971)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 07 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 1.12-3
- Remove rpaths (fix BZ#487823).

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Ivana Varekova <varekova@redhat.com> - 1.12-1
- update to 1.12

* Tue Sep 16 2008 Ivana Varekova <varekova@redhat.com> - 1.11-4
- Resolves: #462369 - remove %%{_datadir}/aclocal
- add automake dependency

* Mon Jul 28 2008 Ivana Varekova <varekova@redhat.com> - 1.11-3
- add -fgnu89-inline flag to solve gcc4.3 problem 
  remove gcc43 patch

* Wed Jun 18 2008 Ivana Varekova <varekova@redhat.com> - 1.11-2
- Resolves: #451006
  programs build with gcc 4.3 based on gsl require -fgnu89-inline 

* Mon Jun 16 2008 Ivana Varekova <varekova@redhat.com> - 1.11-1
- update to 1.11

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.10-10
- Autorebuild for GCC 4.3

* Thu Nov  1 2007 Ivana Varekova <varekova@redhat.com> - 1.10-9
- source file change
- spec cleanup

* Thu Nov  1 2007 Ivana Varekova <varekova@redhat.com> - 1.10-8
- fix man-pages directories

* Tue Oct 30 2007 Ivana Varekova <varekova@redhat.com> - 1.10-7
- add man pages

* Fri Oct 26 2007 Ivana Varekova <varekova@redhat.com> - 1.10-6
- minor spec changes

* Thu Oct 25 2007 Ivana Varekova <varekova@redhat.com> - 1.10-5
- minor spec changes

* Wed Oct 24 2007 Ivana Varekova <varekova@redhat.com> - 1.10-4
- add pkgconfig dependency
- separate static libraries to -static subpackage
- fix gsl-config script - thanks Patrice Dumas

* Tue Sep 23 2007 Ivana Varekova <varekova@redhat.com> - 1.10-3
- remove *.la files
- add pkgconfig configure file
- change source
- spec file cleanup

* Wed Sep 19 2007 Ivana Varekova <varekova@redhat.com> - 1.10-2
- update license tag

* Wed Sep 19 2007 Ivana Varekova <varekova@redhat.com> - 1.10-1
- update to 1.10
- change license tag

* Tue May 22 2007 Ivana Varekova <varekova@redhat.com> - 1.9-1
- update  to 1.9

* Wed Mar 14 2007 Ivana Varekova <varekova@redhat.com> - 1.8-3
- incorporate the package review feedback

* Mon Jan 22 2007 Ivana Varekova <varekova@redhat.com> - 1.8-2
- Resolves: 223700
  fix non-failsafe install-info problem
- spec file cleanup

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.8-1.1
- rebuild

* Fri May  5 2006 Ivana Varekova <varekova@redhat.com> - 1.8-1
- update to 1.8

* Fri Mar  3 2006 Ivana Varekova <varekova@redhat.com> - 1.7-2
- fix multilib problem

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.7-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.7-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Ivana Varekova <varekova@redhat.com> 1.7-1
- update to 1.7

* Mon Mar  7 2005 Ivana Varekova <varekova@redhat.com> 1.6-2
- rebuilt

* Thu Jan  6 2005 Ivana Varekova <varekova@redhat.com> 1.6-1
- update to 1.6 

* Wed Dec 15 2004 Ivana Varekova <varekova@redhat.com>
- fix bug #142696 gsl-config outputs invalid flags on multilib 64-bit 
architectures

* Fri Jul 02 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.5

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Aug 21 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.4

* Wed Jun 25 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.3

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 1.1.1-4
- remove unpackaged files from the buildroot

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Mar 21 2002 Trond Eivind Glomsrød <teg@redhat.com>
- 1.1.1 bugfix release
- Stop the gsl-config script from printing -I/usr/include 
  and -L/usr/lib (#59500)


* Wed Feb 27 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.1-1
- 1.1
- Update URL and location

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Dec 13 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.0-1
- 1.0
- Split into gsl and gsl-devel
- update description (#56926)

* Thu Jul 19 2001 Preston Brown <pbrown@redhat.com>
- upgrade to 0.9

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Thu Jan 18 2001 Preston Brown <pbrown@redhat.com>
- prereq install-info (#24250)

* Mon Dec 11 2000 Preston Brown <pbrown@redhat.com>
- 0.7, remove excludearch for ia64

* Sun Jul 30 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- fix %%post to be a real shell and add ldconfig to %%post

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 19 2000 Preston Brown <pbrown@redhat.com>
- don't include the info dir file...

* Sat Jun 17 2000 Bill Nottingham <notting@redhat.com>
- add %%defattr

* Mon Jun 12 2000 Preston Brown <pbrown@redhat.com>
- 0.6, FHS paths
- exclude ia64, it is having issues

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 2)

* Thu Mar 11 1999 Bill Nottingham <notting@redhat.com>
- update to 0.3f
- add patches to fix glibc-2.1 compilation, doc oddity

* Thu Feb 25 1999 Bill Nottingham <notting@redhat.com>
- new summary/description, work around automake oddity

* Tue Jan 12 1999 Michael K. Johnson <johnsonm@redhat.com>
- libtoolize for arm

* Thu Sep 10 1998 Cristian Gafton <gafton@redhat.com>
- spec file fixups

* Sat May 9 1998 Michael Fulbright <msf@redhat.com>
- started with package for gmp from Toshio Kuratomi <toshiok@cats.ucsc.edu>
- cleaned up file list
- fixed up install-info support
