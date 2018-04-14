%{?scl:%scl_package valgrind}

Summary: Tool for finding memory management bugs in programs
Name: %{?scl_prefix}valgrind
Version: 3.13.0
Release: 10%{?dist}
Epoch: 1
License: GPLv2+
URL: http://www.valgrind.org/
Group: Development/Debuggers

# Only necessary for RHEL, will be ignored on Fedora
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Are we building for a Software Collection?
%{?scl:%global is_scl 1}
%{!?scl:%global is_scl 0}

# Only arches that are supported upstream as multilib and that the distro
# has multilib builds for should set build_multilib 1. In practice that
# is only x86_64 and ppc64 (but not in fedora 21 and later, and never
# for ppc64le or when building for scl).
%global build_multilib 0

%ifarch x86_64
 %global build_multilib 1
%endif

%ifarch ppc64
  %if %{is_scl}
    %global build_multilib 0
  %else
    %if 0%{?rhel}
      %global build_multilib 1
    %endif
    %if 0%{?fedora}
      %global build_multilib (%fedora < 21)
    %endif
  %endif
%endif

# Note s390x doesn't have an openmpi port available.
# We never want the openmpi subpackage when building a software collecton
%if %{is_scl}
  %global build_openmpi 0
%else
  %ifarch %{ix86} x86_64 ppc ppc64 ppc64le %{arm} aarch64
    %global build_openmpi 1
  %else
    %global build_openmpi 0
  %endif
%endif

# Whether to run the full regtest or only a limited set
# The full regtest includes gdb_server integration tests.
# On arm the gdb integration tests hang for unknown reasons.
# On rhel6 the gdb_server tests hang.
# On rhel7 they hang on ppc64 and ppc64le.
%ifarch %{arm}
  %global run_full_regtest 0
%else
  %if 0%{?rhel} == 6
    %global run_full_regtest 0
  %else
    %if 0%{?rhel} == 7
      %ifarch ppc64 ppc64le
        %global run_full_regtest 0
      %else
        %global run_full_regtest 1
      %endif
    %else
      %global run_full_regtest 1
    %endif
  %endif
%endif

# Generating minisymtabs doesn't really work for the staticly linked
# tools. Note (below) that we don't strip the vgpreload libraries at all
# because valgrind might read and need the debuginfo in those (client)
# libraries for better error reporting and sometimes correctly unwinding.
# So those will already have their full symbol table.
%undefine _include_minidebuginfo

Source0: ftp://sourceware.org/pub/valgrind/valgrind-%{version}.tar.bz2

# Needs investigation and pushing upstream
Patch1: valgrind-3.9.0-cachegrind-improvements.patch

# KDE#211352 - helgrind races in helgrind's own mythread_wrapper
Patch2: valgrind-3.9.0-helgrind-race-supp.patch

# Make ld.so supressions slightly less specific.
Patch3: valgrind-3.9.0-ldso-supp.patch

# KDE#381272  ppc64 doesn't compile test_isa_2_06_partx.c without VSX support
Patch4: valgrind-3.13.0-ppc64-check-no-vsx.patch

# KDE#381289 epoll_pwait can have a NULL sigmask.
Patch5: valgrind-3.13.0-epoll_pwait.patch

# KDE#381274 powerpc too chatty even with --sigill-diagnostics=no
Patch6: valgrind-3.13.0-ppc64-diag.patch

# KDE#381556 arm64: Handle feature registers access on 4.11 Linux kernel
# Workaround that masks CPUID support in HWCAP on aarch64 (#1464211)
Patch7: valgrind-3.13.0-arm64-hwcap.patch

# RHBZ#1466017 ARM ld.so index warnings.
# KDE#381805 arm32 needs ld.so index hardwire for new glibc security fixes
Patch8: valgrind-3.13.0-arm-index-hardwire.patch

# KDE#381769 Use ucontext_t instead of struct ucontext
Patch9: valgrind-3.13.0-ucontext_t.patch

# valgrind svn r16453 Fix some tests failure with GDB 8.0
Patch10: valgrind-3.13.0-gdb-8-testfix.patch

# valgrind svn r16454. disable vgdb poll in the child after fork
Patch11: valgrind-3.13.0-disable-vgdb-child.patch

# KDE#382998 xml-socket doesn't work
Patch12: valgrind-3.13.0-xml-socket.patch

# KDE#385334
# PPC64, vpermr, xxperm, xxpermr fix Iop_Perm8x16 selector field
# PPC64, revert the change to vperm instruction.
# KDE#385183
# PPC64, Add support for xscmpeqdp, xscmpgtdp, xscmpgedp, xsmincdp instructions
# PPC64, Fix bug in vperm instruction.
# KDE#385210
# PPC64, Re-implement the vpermr instruction using the Iop_Perm8x16.
# KDE#385208
# PPC64, Use the vperm code to implement the xxperm inst.
# PPC64, Replace body of generate_store_FPRF with C helper function.
# PPC64, Add support for the Data Stream Control Register (DSCR)
Patch13: valgrind-3.13.0-ppc64-vex-fixes.patch

# Fix eflags handling in amd64 instruction tests
Patch14: valgrind-3.13.0-amd64-eflags-tests.patch

# KDE#385868 ld.so _dl_runtime_resolve_avx_slow conditional jump warning
Patch15: valgrind-3.13.0-suppress-dl-trampoline-sse-avx.patch

# Implement static TLS code for more platforms
Patch16: valgrind-3.13.0-static-tls.patch

# KDE#386397 PPC64 valgrind truncates powerpc timebase to 32-bits.
Patch17: valgrind-3.13.0-ppc64-timebase.patch

# RHEL7 specific patches.

# RHBZ#996927 Ignore PPC floating point phased out category.
# The result might differ on ppc vs ppc64 and config.h ends up as
# public header under /usr/include/valgrind causing multilib problems.
# The result would only be used for two test cases.
Patch7001: valgrind-3.11.0-ppc-fppo.patch
%if %{build_multilib}

# Ensure glibc{,-devel} is installed for both multilib arches
BuildRequires: /lib/libc.so.6 /usr/lib/libc.so /lib64/libc.so.6 /usr/lib64/libc.so
%endif

%if 0%{?fedora} >= 15
BuildRequires: glibc-devel >= 2.14
%else
%if 0%{?rhel} >= 6
BuildRequires: glibc-devel >= 2.12
%else
BuildRequires: glibc-devel >= 2.5
%endif
%endif

%if %{build_openmpi}
BuildRequires: openmpi-devel >= 1.3.3
%endif

# For %%build and %%check.
# In case of a software collection, pick the matching gdb and binutils.
%if %{run_full_regtest}
BuildRequires: %{?scl_prefix}gdb
%endif
BuildRequires: %{?scl_prefix}binutils

# gdbserver_tests/filter_make_empty uses ps in test
BuildRequires: procps

# Some testcases require g++ to build
BuildRequires: gcc-c++

# check_headers_and_includes uses Getopt::Long
%if 0%{?fedora}
BuildRequires: perl-generators
%endif
BuildRequires: perl(Getopt::Long)

%{?scl:Requires:%scl_runtime}

ExclusiveArch: %{ix86} x86_64 ppc ppc64 ppc64le s390x armv7hl aarch64
%ifarch %{ix86}
%define valarch x86
%define valsecarch %{nil}
%endif
%ifarch x86_64
%define valarch amd64
%define valsecarch x86
%endif
%ifarch ppc
%define valarch ppc32
%define valsecarch %{nil}
%endif
%ifarch ppc64
  %define valarch ppc64be
  %if %{build_multilib}
    %define valsecarch ppc32
  %else
    %define valsecarch %{nil}
  %endif
%endif
%ifarch ppc64le
%define valarch ppc64le
%define valsecarch %{nil}
%endif
%ifarch s390x
%define valarch s390x
%define valsecarch %{nil}
%endif
%ifarch armv7hl
%define valarch arm
%define valsecarch %{nil}
%endif
%ifarch aarch64
%define valarch arm64
%define valsecarch %{nil}
%endif

%description
Valgrind is an instrumentation framework for building dynamic analysis
tools. There are Valgrind tools that can automatically detect many
memory management and threading bugs, and profile your programs in
detail. You can also use Valgrind to build new tools. The Valgrind
distribution currently includes six production-quality tools: a memory
error detector (memcheck, the default tool), two thread error
detectors (helgrind and drd), a cache and branch-prediction profiler
(cachegrind), a call-graph generating cache and branch-prediction
profiler (callgrind), and a heap profiler (massif).

%package devel
Summary: Development files for valgrind
Group: Development/Debuggers
Requires: %{?scl_prefix}valgrind = %{epoch}:%{version}-%{release}
Provides: %{name}-static = %{epoch}:%{version}-%{release}

%description devel
Header files and libraries for development of valgrind aware programs
or valgrind plugins.

%if %{build_openmpi}
%package openmpi
Summary: OpenMPI support for valgrind
Group: Development/Debuggers
Requires: %{?scl_prefix}valgrind = %{epoch}:%{version}-%{release}

%description openmpi
A wrapper library for debugging OpenMPI parallel programs with valgrind.
See the section on Debugging MPI Parallel Programs with Valgrind in the
Valgrind User Manual for details.
%endif

%prep
%setup -q -n %{?scl:%{pkg_name}}%{!?scl:%{name}}-%{version}

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

# RHEL7 specific patches
%patch7001 -p1

%build
# We need to use the software collection compiler and binutils if available.
# The configure checks might otherwise miss support for various newer
# assembler instructions.
%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}

CC=gcc
%if %{build_multilib}
# Ugly hack - libgcc 32-bit package might not be installed
mkdir -p shared/libgcc/32
ar r shared/libgcc/32/libgcc_s.a
ar r shared/libgcc/libgcc_s_32.a
CC="gcc -B `pwd`/shared/libgcc/"
%endif

# Old openmpi-devel has version depended paths for mpicc.
%if %{build_openmpi}
%if 0%{?fedora} >= 13 || 0%{?rhel} >= 6
%define mpiccpath %{!?scl:%{_libdir}}%{?scl:%{_root_libdir}}/openmpi/bin/mpicc
%else
%define mpiccpath %{!?scl:%{_libdir}}%{?scl:%{_root_libdir}}/openmpi/*/bin/mpicc
%endif
%endif

# Filter out some flags that cause lots of valgrind test failures.
# Also filter away -O2, valgrind adds it wherever suitable, but
# not for tests which should be -O0, as they aren't meant to be
# compiled with -O2 unless explicitely requested. Same for any -mcpu flag.
# Ideally we will change this to only be done for the non-primary build
# and the test suite.
%undefine _hardened_build
OPTFLAGS="`echo " %{optflags} " | sed 's/ -m\(64\|3[21]\) / /g;s/ -fexceptions / /g;s/ -fstack-protector\([-a-z]*\) / / g;s/ -Wp,-D_FORTIFY_SOURCE=2 / /g;s/ -O2 / /g;s/ -mcpu=\([a-z0-9]\+\) / /g;s/^ //;s/ $//'`"
%configure CC="$CC" CFLAGS="$OPTFLAGS" CXXFLAGS="$OPTFLAGS" \
%if %{build_openmpi}
  --with-mpicc=%{mpiccpath} \
%endif
  GDB=%{_bindir}/gdb

make %{?_smp_mflags}

# Ensure there are no unexpected file descriptors open,
# the testsuite otherwise fails.
cat > close_fds.c <<EOF
#include <stdlib.h>
#include <unistd.h>
int main (int argc, char *const argv[])
{
  int i, j = sysconf (_SC_OPEN_MAX);
  if (j < 0)
    exit (1);
  for (i = 3; i < j; ++i)
    close (i);
  execvp (argv[1], argv + 1);
  exit (1);
}
EOF
gcc $RPM_OPT_FLAGS -o close_fds close_fds.c

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
mkdir docs/installed
mv $RPM_BUILD_ROOT%{_datadir}/doc/valgrind/* docs/installed/
rm -f docs/installed/*.ps

# We want the MPI wrapper installed under the openmpi libdir so the script
# generating the MPI library requires picks them up and sets up the right
# openmpi libmpi.so requires. Install symlinks in the original/upstream
# location for backwards compatibility.
%if %{build_openmpi}
pushd $RPM_BUILD_ROOT%{_libdir}
mkdir -p openmpi/valgrind
cd valgrind
mv libmpiwrap-%{valarch}-linux.so ../openmpi/valgrind/
ln -s ../openmpi/valgrind/libmpiwrap-%{valarch}-linux.so
popd
%endif

%if "%{valsecarch}" != ""
pushd $RPM_BUILD_ROOT%{_libdir}/valgrind/
rm -f *-%{valsecarch}-* || :
for i in *-%{valarch}-*; do
  j=`echo $i | sed 's/-%{valarch}-/-%{valsecarch}-/'`
  ln -sf ../../lib/valgrind/$j $j
done
popd
%endif

rm -f $RPM_BUILD_ROOT%{_libdir}/valgrind/*.supp.in

%ifarch %{ix86} x86_64
# To avoid multilib clashes in between i?86 and x86_64,
# tweak installed <valgrind/config.h> a little bit.
for i in HAVE_PTHREAD_CREATE_GLIBC_2_0 HAVE_PTRACE_GETREGS HAVE_AS_AMD64_FXSAVE64 \
%if 0%{?rhel} == 5
         HAVE_BUILTIN_ATOMIC HAVE_BUILTIN_ATOMIC_CXX \
%endif
         ; do
  sed -i -e 's,^\(#define '$i' 1\|/\* #undef '$i' \*/\)$,#ifdef __x86_64__\n# define '$i' 1\n#endif,' \
    $RPM_BUILD_ROOT%{_includedir}/valgrind/config.h
done
%endif

# We don't want debuginfo generated for the vgpreload libraries.
# Turn off execute bit so they aren't included in the debuginfo.list.
# We'll turn the execute bit on again in %%files.
chmod 644 $RPM_BUILD_ROOT%{_libdir}/valgrind/vgpreload*-%{valarch}-*so

%check
# Make sure some info about the system is in the build.log
# Add || true because rpm on copr EPEL6 acts weirdly and we don't want
# to break the build.
uname -a
rpm -q glibc gcc %{?scl_prefix}binutils || true
%if %{run_full_regtest}
rpm -q %{?scl_prefix}gdb || true
%endif

LD_SHOW_AUXV=1 /bin/true
cat /proc/cpuinfo

# Make sure a basic binary runs. There should be no errors.
./vg-in-place --error-exitcode=1 /bin/true

# Build the test files with the software collection compiler if available.
%{?scl:PATH=%{_bindir}${PATH:+:${PATH}}}
# Make sure no extra CFLAGS, CXXFLAGS or LDFLAGS leak through,
# the testsuite sets all flags necessary. See also configure above.
make %{?_smp_mflags} CFLAGS="" CXXFLAGS="" LDFLAGS="" check

# Workaround https://bugzilla.redhat.com/show_bug.cgi?id=1434601
# for gdbserver tests.
export PYTHONCOERCECLOCALE=0

echo ===============TESTING===================
%if %{run_full_regtest}
  ./close_fds make regtest || :
%else
  ./close_fds make nonexp-regtest || :
%endif

# Make sure test failures show up in build.log
# Gather up the diffs (at most the first 20 lines for each one)
MAX_LINES=20
diff_files=`find . -name '*.diff' | sort`
if [ z"$diff_files" = z ] ; then
   echo "Congratulations, all tests passed!" >> diffs
else
   for i in $diff_files ; do
      echo "=================================================" >> diffs
      echo $i                                                  >> diffs
      echo "=================================================" >> diffs
      if [ `wc -l < $i` -le $MAX_LINES ] ; then
         cat $i                                                >> diffs
      else
         head -n $MAX_LINES $i                                 >> diffs
         echo "<truncated beyond $MAX_LINES lines>"            >> diffs
      fi
   done
fi
cat diffs
echo ===============END TESTING===============

%files
%defattr(-,root,root)
%doc COPYING NEWS README_*
%doc docs/installed/html docs/installed/*.pdf
%{_bindir}/*
%dir %{_libdir}/valgrind
# Install everything in the libdir except the .so and .a files.
# The vgpreload so files might file mode adjustment (see below).
# The libmpiwrap so files go in the valgrind-openmpi package.
# The .a archives go into the valgrind-devel package.
%{_libdir}/valgrind/*[^ao]
# Turn on executable bit again for vgpreload libraries.
# Was disabled in %%install to prevent debuginfo stripping.
%attr(0755,root,root) %{_libdir}/valgrind/vgpreload*-%{valarch}-*so
# And install the symlinks to the secarch files if the exist.
# These are separate from the above because %%attr doesn't work
# on symlinks.
%if "%{valsecarch}" != ""
%{_libdir}/valgrind/vgpreload*-%{valsecarch}-*so
%endif
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/valgrind
%dir %{_libdir}/valgrind
%{_libdir}/valgrind/*.a
%{_libdir}/pkgconfig/*

%if %{build_openmpi}
%files openmpi
%defattr(-,root,root)
%dir %{_libdir}/valgrind
%{_libdir}/openmpi/valgrind/libmpiwrap*.so
%{_libdir}/valgrind/libmpiwrap*.so
%endif

%changelog
* Thu Nov  2 2017 Mark Wielaard <mjw@redhat.com> - 3.13.0-10
- Add valgrind-3.13.0-ppc64-timebase.patch (#1508148)

* Tue Oct 17 2017 Mark Wielaard <mjw@redhat.com> - 3.13.0-9
- valgrind 3.13.0 (fedora).
- Update description.
- Drop all upstreamed patches.
- Add valgrind-3.13.0-ppc64-check-no-vsx.patch
- Add valgrind-3.13.0-epoll_pwait.patch (#1462258)
- Add valgrind-3.13.0-ppc64-diag.patch
- Add valgrind-3.13.0-arm64-hwcap.patch (#1464211)
- Add valgrind-3.13.0-arm-index-hardwire.patch (#1466017)
- Add valgrind-3.13.0-ucontext_t.patch
- Add valgrind-3.13.0-gdb-8-testfix.patch
- Add valgrind-3.13.0-disable-vgdb-child.patch
- Add --error-exitcode=1 to /bin/true check.
- Add valgrind-3.13.0-xml-socket.patch
- Add valgrind-3.13.0-ppc64-vex-fixes.patch
- Add valgrind-3.13.0-amd64-eflags-tests.patch
- Add valgrind-3.13.0-suppress-dl-trampoline-sse-avx.patch
- Add valgrind-3.13.0-static-tls.patch
- Workaround gdb/python bug in testsuite (#1434601)

* Thu Sep 21 2017 Mark Wielaard <mjw@redhat.com> - 3.12.0-9
- Add valgrind-3.12.0-ll-sc-fallback[1234].patch (#1492753)

* Tue Mar 28 2017 Mark Wielaard <mjw@redhat.com> - 3.12.0-8
- Add valgrind-3.12.0-powerpc-register-pair.patch (#1437030)
- Add valgrind-3.12.0-ppc64-isa-3_00.patch (#1437032)

* Sat Feb 18 2017 Mark Wielaard <mjw@redhat.com> - 3.12.0-7
- Rebase to 3.12.0 fedora backports (#1391217, #1385006, #1368706, #1270889)

* Thu Jul 21 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-24
- Add valgrind-3.11.0-pcmpxstrx-0x70-0x19.patch (#1354557)

* Tue Jun 21 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-23
- Update valgrind-3.11.0-ppoll-mask.patch (#1347626)

* Mon May 30 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-22
- Add valgrind-3.11.0-arm64-handle_at.patch
- Add valgrind-3.11.0-ppc64-syscalls.patch

* Fri Apr 29 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-21
- Add valgrind-3.11.0-deduppoolalloc.patch (#1328347)
- Add valgrind-3.11.0-ppc-bcd-addsub.patch (#1331738)
- Add valgrind-3.11.0-ppc64-vgdb-vr-regs.patch (#1331774)

* Fri Apr 15 2016 Mark Wielaard <mjw@redhat.com> - 3.11.0-20
- Rebase to fedora 3.11.0
  (#1316512 #1306844 #1305962 #1298888 #1296318 #1271754 #1265566 #1265557)

* Fri Aug 28 2015 Mark Wielaard <mjw@redhat.com> - 3.10.0-16
- Patch both 32 and 64 in valgrind-3.10.1-ppc32-tabortdc.patch (#1257623)

* Thu Aug 27 2015 Mark Wielaard <mjw@redhat.com> - 3.10.0-15
- Add valgrind-3.10.1-ppc32-tabortdc.patch (#1257623)

* Mon Aug 10 2015 Mark Wielaard <mjw@redhat.com> - 3.10.0-14
- Add setuid and setresgid to valgrind-3.10.1-aarch64-syscalls.patch (#1251181)

* Mon Aug 03 2015 Mark Wielaard <mjw@redhat.com> - 3.10.0-13
- Add valgrind-3.10.1-ppc64-hwcap2.patch (#1249381)

* Wed Jul 29 2015 Mark Wielaard <mjw@redhat.com> - 3.10.0-12
- Add valgrind-3.10.1-kernel-4.0.patch (#1247557)

* Thu Jul 09 2015 Mark Wielaard <mjw@redhat.com> - 3.10.0-11
- Add valgrind-3.10.1-s390x-fiebra.patch (#1181993)

* Tue Jul 07 2015 Mark Wielaard <mjw@redhat.com> - 3.10.0-10
- Add valgrind-3.10.1-di_notify_mmap.patch (#1237206)

* Thu May 28 2015 Mark Wielaard <mjw@redhat.com> - 3.10.0-9
- Add valgrind-3.10-1-ppc64-sigpending.patch. (#1225964)

* Thu May 28 2015 Mark Wielaard <mjw@redhat.com> - 3.10.0-8
- Add valgrind-3.10-s390-spechelper.patch. (#1190169)
- Add valgrind-3.10.1-aarch64-syscalls.patch. (#1188622)
- Add accept4 to valgrind-3.10.1-aarch64-syscalls.patch. (#1190660)
- Add valgrind-3.10.1-ppc64-accept4.patch. (#1190660)
- Add valgrind-3.10.1-send-recv-mmsg.patch. (#1192103)
- Add mount and umount2 to valgrind-3.10.1-aarch64-syscalls.patch. (#1193796)

* Tue Jan 13 2015 Mark Wielaard <mjw@redhat.com> - 3.10.0-7
- Add valgrind-3.10.1-mempcpy.patch (#1178813)

* Wed Nov 19 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-6
- Add getgroups/setgroups to valgrind-3.10.0-aarch64-syscalls.patch

* Tue Nov  4 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-5
- Merge valgrind-3.10.0-aarch64-times.patch
  and valgrind-3.10.0-aarch64-getsetsid.patch
  into valgrind-3.10.0-aarch64-syscalls.patch
  add fdatasync, msync, pread64, setreuid, setregid,
  mknodat, fchdir, chroot, fchownat, fchmod and fchown.
- Add valgrind-3.10.0-aarch64-frint.patch
- Add valgrind-3.10.0-fcvtmu.patch
- Add valgrind-3.10.0-aarch64-fcvta.patch

* Sat Oct 11 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-4
- Add valgrind-3.10.0-aarch64-times.patch
- Add valgrind-3.10.0-aarch64-getsetsid.patch
- Add valgrind-3.10.0-aarch64-dmb-sy.patch

* Mon Sep 15 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-3
- Add valgrind-3.10.0-old-ppc32-instr-magic.patch.

* Fri Sep 12 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-2
- Fix ppc32 multilib handling on ppc64[be].
- Drop ppc64 secondary for ppc32 primary support.
- Except for armv7hl we don't support any other arm[32] arch.

* Thu Sep 11 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-1
- Update to 3.10.0 final.
- Don't run dwz or generate minisymtab.
- Remove valgrind-3.9.0-s390x-ld-supp.patch fixed upstream.
- Add valgrind-openmpi for ppc64le.

* Tue Sep  2 2014 Mark Wielaard <mjw@redhat.com> - 3.10.0-0.1.BETA1
- Update to official upstream 3.10.0 BETA1.
  - Enables inlined frames in stacktraces.

* Mon Mar 10 2014 Mark Wielaard <mjw@redhat.com> - 3.9.0-6
- Add valgrind-3.9.0-ppc64-priority.patch. (#1073613)

* Fri Feb 21 2014 Mark Wielaard <mjw@redhat.com> - 3.9.0-5
- Add valgrind-3.9.0-s390-dup3.patch. (#1067486)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1:3.9.0-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:3.9.0-3
- Mass rebuild 2013-12-27

* Thu Dec 12 2013 Mark Wielaard <mjw@redhat.com>
- Add valgrind-3.9.0-manpage-memcheck-options.patch. (#1040914)
- Add valgrind-3.9.0-s390-fpr-pair.patch. (#1036615)

* Thu Nov 28 2013 Mark Wielaard <mjw@redhat.com> - 3.9.0-2.2
- Add valgrind-3.9.0-s390x-ld-supp.patch. (#1032282)
- Add valgrind-3.9.0-xabort.patch. (#1035704)

* Wed Nov 20 2013 Mark Wielaard <mjw@redhat.com> - 3.9.0-2.1
- Add valgrind-3.9.0-dwz-alt-buildid.patch. (#1029875)

* Thu Nov  7 2013 Mark Wielaard <mjw@redhat.com> - 3.9.0-1.2
- Remove unnecessary and unapplied valgrind-3.8.1-movntdqa.patch
- Remove valgrind-3.9.0-s390x-workarounds.patch
- Add valgrind-3.9.0-s390-risbg.patch (#1018325)

* Fri Nov  1 2013 Mark Wielaard <mjw@redhat.com> - 3.9.0-1.1
- Add s390x workarounds. (#1018325)

* Fri Nov  1 2013 Mark Wielaard <mjw@redhat.com> - 3.9.0-1
- Upgrade to valgrind 3.9.0 final.
- Remove support for really ancient GCCs (valgrind-3.9.0-config_h.patch).
- Add valgrind-3.9.0-amd64_gen_insn_test.patch.
- Remove and cleanup fake 32-bit libgcc package.

* Mon Oct 28 2013 Mark Wielaard <mjw@redhat.com> - 3.9.0-0.1.TEST1
- Upgrade to valgrind 3.9.0.TEST1
- Remove patches that are now upstream:
  - valgrind-3.8.1-abbrev-parsing.patch
  - valgrind-3.8.1-af-bluetooth.patch
  - valgrind-3.8.1-aspacemgr_VG_N_SEGs.patch
  - valgrind-3.8.1-avx2-bmi-fma.patch.gz
  - valgrind-3.8.1-avx2-prereq.patch
  - valgrind-3.8.1-bmi-conf-check.patch
  - valgrind-3.8.1-capget.patch
  - valgrind-3.8.1-cfi_dw_ops.patch
  - valgrind-3.8.1-dwarf-anon-enum.patch
  - valgrind-3.8.1-filter_gdb.patch
  - valgrind-3.8.1-find-buildid.patch
  - valgrind-3.8.1-gdbserver_exit.patch
  - valgrind-3.8.1-gdbserver_tests-syscall-template-source.patch
  - valgrind-3.8.1-glibc-2.17-18.patch
  - valgrind-3.8.1-index-supp.patch
  - valgrind-3.8.1-initial-power-isa-207.patch
  - valgrind-3.8.1-manpages.patch
  - valgrind-3.8.1-memcheck-mc_translate-Iop_8HLto16.patch
  - valgrind-3.8.1-mmxext.patch
  - valgrind-3.8.1-movntdqa.patch
  - valgrind-3.8.1-new-manpages.patch
  - valgrind-3.8.1-openat.patch
  - valgrind-3.8.1-overlap_memcpy_filter.patch
  - valgrind-3.8.1-pie.patch
  - valgrind-3.8.1-pkg-config.patch
  - valgrind-3.8.1-power-isa-205-deprecation.patch
  - valgrind-3.8.1-ppc-32-mode-64-bit-instr.patch
  - valgrind-3.8.1-ppc-setxattr.patch
  - valgrind-3.8.1-proc-auxv.patch
  - valgrind-3.8.1-ptrace-include-configure.patch
  - valgrind-3.8.1-ptrace-setgetregset.patch
  - valgrind-3.8.1-ptrace-thread-area.patch
  - valgrind-3.8.1-regtest-fixlets.patch
  - valgrind-3.8.1-s390-STFLE.patch
  - valgrind-3.8.1-s390_tsearch_supp.patch
  - valgrind-3.8.1-sendmsg-flags.patch
  - valgrind-3.8.1-sigill_diag.patch
  - valgrind-3.8.1-static-variables.patch
  - valgrind-3.8.1-stpncpy.patch
  - valgrind-3.8.1-text-segment.patch
  - valgrind-3.8.1-wcs.patch
  - valgrind-3.8.1-x86_amd64_features-avx.patch
  - valgrind-3.8.1-xaddb.patch
  - valgrind-3.8.1-zero-size-sections.patch
- Remove special case valgrind-3.8.1-enable-armv5.patch.
- Remove valgrind-3.8.1-x86-backtrace.patch, rely on new upstream fp/cfi
  try-cache mechanism.

* Mon Oct 14 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-31
- Fix multilib issue with HAVE_PTRACE_GETREGS in config.h.

* Thu Sep 26 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-30
- Add valgrind-3.8.1-index-supp.patch (#1011713)
- Ignore PPC floating point phased out category. (#996927).

* Wed Sep 25 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-29
- Filter out -mcpu= so tests are compiled with the right flags. (#996927).

* Mon Sep 23 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-28
- Implement SSE4 MOVNTDQA insn (valgrind-3.8.1-movntdqa.patch)
- Don't BuildRequire /bin/ps, just BuildRequire procps
  (procps-ng provides procps).

* Thu Sep 05 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-27
- Fix power_ISA2_05 testcase (valgrind-3.8.1-power-isa-205-deprecation.patch)
- Fix ppc32 make check build (valgrind-3.8.1-initial-power-isa-207.patch)
- Add valgrind-3.8.1-mmxext.patch

* Wed Aug 21 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-26
- Allow building against glibc 2.18. (#999169)

* Thu Aug 15 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-25
- Add valgrind-3.8.1-s390-STFLE.patch
  s390 message-security assist (MSA) instruction extension not implemented.

* Wed Aug 14 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-24
- Add valgrind-3.8.1-power-isa-205-deprecation.patch
  Deprecation of some ISA 2.05 POWER6 instructions.
- Fixup auto-foo generation of new manpage doc patch.

* Wed Aug 14 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-23
- tests/check_isa-2_07_cap should be executable.

* Tue Aug 13 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-22
- Add valgrind-3.8.1-initial-power-isa-207.patch
  Initial ISA 2.07 support for POWER8-tuned libc.

* Thu Aug 08 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-21
- Don't depend on docdir location and version in openmpi subpackage
  description (#993938).
- Enable openmpi subpackage also on arm.

* Thu Aug 08 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-20
- Add valgrind-3.8.1-ptrace-include-configure.patch (#992847)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.8.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1:3.8.1-18
- Perl 5.18 rebuild

* Mon Jul 08 2013 Mark Wielaard <mjw@redhat.com> - 3.8.1-17
- Add valgrind-3.8.1-dwarf-anon-enum.patch
- Cleanup valgrind-3.8.1-sigill_diag.patch .orig file changes (#949687).
- Add valgrind-3.8.1-ppc-setxattr.patch
- Add valgrind-3.8.1-new-manpages.patch
- Add valgrind-3.8.1-ptrace-thread-area.patch
- Add valgrind-3.8.1-af-bluetooth.patch

* Tue May 28 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1:3.8.1-16
- Provide virtual -static package in -devel subpackage (#609624).

* Thu Apr 25 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-15
- Add valgrind-3.8.1-zero-size-sections.patch. Resolves issues with zero
  sized .eh_frame sections on ppc64.

* Thu Apr 18 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-14
- fixup selinux file context when doing a scl build.
- Enable regtest suite on ARM.
- valgrind-3.8.1-abbrev-parsing.patch, drop workaround, enable real fix.
- Fix -Ttext-segment configure check. Enables s390x again.
- BuildRequire ps for testsuite.

* Tue Apr 02 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-13
- Fix quoting in valgrind valgrind-3.8.1-enable-armv5.patch and
  remove arm configure hunk from valgrind-3.8.1-text-segment.patch #947440
- Replace valgrind-3.8.1-text-segment.patch with upstream variant.
- Add valgrind-3.8.1-regtest-fixlets.patch.

* Wed Mar 20 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-12
- Add valgrind-3.8.1-text-segment.patch
- Don't undefine _missing_build_ids_terminate_build.

* Tue Mar 12 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-11
- Add valgrind-3.8.1-manpages.patch

* Fri Mar 01 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-10
- Don't disable -debuginfo package generation, but do undefine
  _missing_build_ids_terminate_build.

* Thu Feb 28 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-9
- Replace valgrind-3.8.1-sendmsg-flags.patch with upstream version.

* Tue Feb 19 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-8
- Add valgrind-3.8.1-sendmsg-flags.patch
- Add valgrind-3.8.1-ptrace-setgetregset.patch
- Add valgrind-3.8.1-static-variables.patch

* Thu Feb 07 2013 Jon Ciesla <limburgher@gmail.com> 1:3.8.1-7
- Merge review fixes, BZ 226522.

* Wed Jan 16 2013 Mark Wielaard <mjw@redhat.com> 3.8.1-6
- Allow building against glibc-2.17.

* Sun Nov  4 2012 Mark Wielaard <mjw@redhat.com> 3.8.1-5
- Add valgrind-3.8.1-stpncpy.patch (KDE#309427)
- Add valgrind-3.8.1-ppc-32-mode-64-bit-instr.patch (#810992, KDE#308573)
- Add valgrind-3.8.1-sigill_diag.patch (#810992, KDE#309425)

* Tue Oct 16 2012 Mark Wielaard <mjw@redhat.com> 3.8.1-4
- Add valgrind-3.8.1-xaddb.patch (#866793, KDE#307106)

* Mon Oct 15 2012 Mark Wielaard <mjw@redhat.com> 3.8.1-3
- Add valgrind-3.8.1-x86_amd64_features-avx.patch (KDE#307285)
- Add valgrind-3.8.1-gdbserver_tests-syscall-template-source.patch (KDE#307155)
- Add valgrind-3.8.1-overlap_memcpy_filter.patch (KDE#307290)
- Add valgrind-3.8.1-pkg-config.patch (#827219, KDE#307729)
- Add valgrind-3.8.1-proc-auxv.patch (KDE#253519)
- Add valgrind-3.8.1-wcs.patch (#755242, KDE#307828)
- Add valgrind-3.8.1-filter_gdb.patch (KDE#308321)
- Add valgrind-3.8.1-gdbserver_exit.patch (#862795, KDE#308341)
- Add valgrind-3.8.1-aspacemgr_VG_N_SEGs.patch (#730303, KDE#164485)
- Add valgrind-3.8.1-s390_tsearch_supp.patch (#816244, KDE#308427)

* Fri Sep 21 2012 Mark Wielaard <mjw@redhat.com> 3.8.1-2
- Add valgrind-3.8.1-gdbserver_tests-mcinvoke-ppc64.patch
- Replace valgrind-3.8.1-cfi_dw_ops.patch with version as committed upstream.
- Remove erroneous printf change from valgrind-3.8.1-abbrev-parsing.patch.
- Add scalar testcase change to valgrind-3.8.1-capget.patch.

* Thu Sep 20 2012 Mark Wielaard <mjw@redhat.com> 3.8.1-1
- Add partial backport of upstream revision 12884
  valgrind-3.8.0-memcheck-mc_translate-Iop_8HLto16.patch
  without it AVX2 VPBROADCASTB insn is broken under memcheck.
- Add valgrind-3.8.0-cfi_dw_ops.patch (KDE#307038)
  DWARF2 CFI reader: unhandled DW_OP_ opcode 0x8 (DW_OP_const1u and friends)
- Add valgrind-3.8.0-avx2-prereq.patch.
- Remove accidentially included diffs for gdbserver_tests and helgrind/tests
  Makefile.in from valgrind-3.8.0-avx2-bmi-fma.patch.gz
- Remove valgrind-3.8.0-tests.patch tests no longer hang.
- Added SCL macros to support building as part of a Software Collection.
- Upgrade to valgrind 3.8.1.

* Wed Sep 12 2012 Mark Wielaard <mjw@redhat.com> 3.8.0-8
- Add configure fixup valgrind-3.8.0-bmi-conf-check.patch

* Wed Sep 12 2012 Mark Wielaard <mjw@redhat.com> 3.8.0-7
- Add valgrind-3.8.0-avx2-bmi-fma.patch (KDE#305728)

* Tue Sep 11 2012 Mark Wielaard <mjw@redhat.com> 3.8.0-6
- Add valgrind-3.8.0-lzcnt-tzcnt-bugfix.patch (KDE#295808)
- Add valgrind-3.8.0-avx-alignment-check.patch (KDE#305926)

* Mon Aug 27 2012 Mark Wielaard <mjw@redhat.com> 3.8.0-5
- Add valgrind-3.8.0-abbrev-parsing.patch for #849783 (KDE#305513).

* Sun Aug 19 2012 Mark Wielaard <mjw@redhat.com> 3.8.0-4
- Add valgrind-3.8.0-find-buildid.patch workaround bug #849435 (KDE#305431).

* Wed Aug 15 2012 Jakub Jelinek <jakub@redhat.com> 3.8.0-3
- fix up last change

* Wed Aug 15 2012 Jakub Jelinek <jakub@redhat.com> 3.8.0-2
- tweak up <valgrind/config.h> to allow simultaneous installation
  of valgrind-devel.{i686,x86_64} (#848146)

* Fri Aug 10 2012 Jakub Jelinek <jakub@redhat.com> 3.8.0-1
- update to 3.8.0 release
- from CFLAGS/CXXFLAGS filter just fortification flags, not arch
  specific flags
- on i?86 prefer to use CFI over %%ebp unwinding, as GCC 4.6+
  defaults to -fomit-frame-pointer

* Tue Aug 07 2012 Mark Wielaard <mjw@redhat.com> 3.8.0-0.1.TEST1.svn12858
- Update to 3.8.0-TEST1
- Clear CFLAGS CXXFLAGS LDFLAGS.
- Fix \ line continuation in configure line.

* Fri Aug 03 2012 Mark Wielaard <mjw@redhat.com> 3.7.0-7
- Fixup shadowing warnings valgrind-3.7.0-dwz.patch
- Add valgrind-3.7.0-ref_addr.patch (#842659, KDE#298864)

* Wed Jul 25 2012 Mark Wielaard <mjw@redhat.com> 3.7.0-6
- handle dwz DWARF compressor output (#842659, KDE#302901)
- allow glibc 2.16.

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May  7 2012 Jakub Jelinek <jakub@redhat.com> 3.7.0-4
- adjust suppressions so that it works even with ld-2.15.so (#806854)
- handle DW_TAG_unspecified_type and DW_TAG_rvalue_reference_type
  (#810284, KDE#278313)
- handle .debug_types sections (#810286, KDE#284124)

* Sun Mar  4 2012 Peter Robinson <pbrobinson@fedoraproject.org> 3.7.0-2
- Fix building on ARM platform

* Fri Jan 27 2012 Jakub Jelinek <jakub@redhat.com> 3.7.0-1
- update to 3.7.0 (#769213, #782910, #772343)
- handle some further SCSI ioctls (#783936)
- handle fcntl F_SETOWN_EX and F_GETOWN_EX (#770746)

* Wed Aug 17 2011 Adam Jackson <ajax@redhat.com> 3.6.1-6
- rebuild for rpm 4.9.1 trailing / bug

* Thu Jul 21 2011 Jakub Jelinek <jakub@redhat.com> 3.6.1-5
- handle PLT unwind info (#723790, KDE#277045)

* Mon Jun 13 2011 Jakub Jelinek <jakub@redhat.com> 3.6.1-4
- fix memcpy/memmove redirection on x86_64 (#705790)

* Wed Jun  8 2011 Jakub Jelinek <jakub@redhat.com> 3.6.1-3
- fix testing against glibc 2.14

* Wed Jun  8 2011 Jakub Jelinek <jakub@redhat.com> 3.6.1-2
- fix build on ppc64 (#711608)
- don't fail if s390x support patch hasn't been applied,
  move testing into %%check (#708522)
- rebuilt against glibc 2.14

* Wed Feb 23 2011 Jakub Jelinek <jakub@redhat.com> 3.6.1-1
- update to 3.6.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:3.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 28 2011 Jakub Jelinek <jakub@redhat.com> 3.6.0-2
- rebuilt against glibc 2.13 (#673046)
- hook in pwrite64 syscall on ppc64 (#672858)
- fix PIE handling on ppc/ppc64 (#665289)

* Fri Nov 12 2010 Jakub Jelinek <jakub@redhat.com> 3.6.0-1
- update to 3.6.0
- add s390x support (#632354)
- provide a replacement for str{,n}casecmp{,_l} (#626470)

* Tue May 18 2010 Jakub Jelinek <jakub@redhat.com> 3.5.0-18
- rebuilt against glibc 2.12

* Mon Apr 12 2010 Jakub Jelinek <jakub@redhat.com> 3.5.0-16
- change pub_tool_basics.h not to include config.h (#579283)
- add valgrind-openmpi package for OpenMPI support (#565541)
- allow NULL second argument to capget (#450976)

* Wed Apr  7 2010 Jakub Jelinek <jakub@redhat.com> 3.5.0-15
- handle i686 nopw insns with more than one data16 prefix (#574889)
- DWARF4 support
- handle getcpu and splice syscalls

* Wed Jan 20 2010 Jakub Jelinek <jakub@redhat.com> 3.5.0-14
- fix build against latest glibc headers

* Wed Jan 20 2010 Jakub Jelinek <jakub@redhat.com> 3.5.0-13
- DW_OP_mod is unsigned modulus instead of signed
- fix up valgrind.pc (#551277)

* Mon Dec 21 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-12
- don't require offset field to be set in adjtimex's
  ADJ_OFFSET_SS_READ mode (#545866)

* Wed Dec  2 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-10
- add handling of a bunch of recent syscalls and fix some
  other syscall wrappers (Dodji Seketeli)
- handle prelink created split of .bss into .dynbss and .bss
  and similarly for .sbss and .sdynbss (#539874)

* Wed Nov  4 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-9
- rebuilt against glibc 2.11
- use upstream version of the ifunc support

* Wed Oct 28 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-8
- add preadv/pwritev syscall support

* Tue Oct 27 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-7
- add perf_counter_open syscall support (#531271)
- add handling of some sbb/adc insn forms on x86_64 (KDE#211410)

* Fri Oct 23 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-6
- ppc and ppc64 fixes

* Thu Oct 22 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-5
- add emulation of 0x67 prefixed loop* insns on x86_64 (#530165)

* Wed Oct 21 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-4
- handle reading of .debug_frame in addition to .eh_frame
- ignore unknown DWARF3 expressions in evaluate_trivial_GX
- suppress helgrind race errors in helgrind's own mythread_wrapper
- fix compilation of x86 tests on x86_64 and ppc tests

* Wed Oct 14 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-3
- handle many more DW_OP_* ops that GCC now uses
- handle the more compact form of DW_AT_data_member_location
- don't strip .debug_loc etc. from valgrind binaries

* Mon Oct 12 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-2
- add STT_GNU_IFUNC support (Dodji Seketeli, #518247)
- wrap inotify_init1 syscall (Dodji Seketeli, #527198)
- fix mmap/mprotect handling in memcheck (KDE#210268)

* Fri Aug 21 2009 Jakub Jelinek <jakub@redhat.com> 3.5.0-1
- update to 3.5.0

* Tue Jul 28 2009 Jakub Jelinek <jakub@redhat.com> 3.4.1-7
- handle futex ops newly added during last 4 years (#512121)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 3.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 13 2009 Jakub Jelinek <jakub@redhat.com> 3.4.1-5
- add support for DW_CFA_{remember,restore}_state

* Mon Jul 13 2009 Jakub Jelinek <jakub@redhat.com> 3.4.1-4
- handle version 3 .debug_frame, .eh_frame, .debug_info and
  .debug_line (#509197)

* Mon May 11 2009 Jakub Jelinek <jakub@redhat.com> 3.4.1-3
- rebuilt against glibc 2.10.1

* Wed Apr 22 2009 Jakub Jelinek <jakub@redhat.com> 3.4.1-2
- redirect x86_64 ld.so strlen early (#495645)

* Mon Mar  9 2009 Jakub Jelinek <jakub@redhat.com> 3.4.1-1
- update to 3.4.1

* Mon Feb  9 2009 Jakub Jelinek <jakub@redhat.com> 3.4.0-3
- update to 3.4.0

* Wed Apr 16 2008 Jakub Jelinek <jakub@redhat.com> 3.3.0-3
- add suppressions for glibc 2.8
- add a bunch of syscall wrappers (#441709)

* Mon Mar  3 2008 Jakub Jelinek <jakub@redhat.com> 3.3.0-2
- add _dl_start suppression for ppc/ppc64

* Mon Mar  3 2008 Jakub Jelinek <jakub@redhat.com> 3.3.0-1
- update to 3.3.0
- split off devel bits into valgrind-devel subpackage

* Thu Oct 18 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-7
- add suppressions for glibc >= 2.7

* Fri Aug 31 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-6
- handle new x86_64 nops (#256801, KDE#148447)
- add support for private futexes (KDE#146781)
- update License tag

* Fri Aug  3 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-5
- add ppc64-linux symlink in valgrind ppc.rpm, so that when
  rpm prefers 32-bit binaries over 64-bit ones 32-bit
  /usr/bin/valgrind can find 64-bit valgrind helper binaries
  (#249773)
- power5+ and power6 support (#240762)

* Thu Jun 28 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-4
- pass GDB=%%{_prefix}/gdb to configure to fix default
  --db-command (#220840)

* Wed Jun 27 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-3
- add suppressions for glibc >= 2.6
- avoid valgrind internal error if io_destroy syscall is
  passed a bogus argument

* Tue Feb 13 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-2
- fix valgrind.pc again

* Tue Feb 13 2007 Jakub Jelinek <jakub@redhat.com> 3.2.3-1
- update to 3.2.3

* Wed Nov  8 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-7
- some cachegrind improvements (Ulrich Drepper)

* Mon Nov  6 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-6
- fix valgrind.pc (#213149)
- handle Intel Core2 cache sizes in cachegrind (Ulrich Drepper)

* Wed Oct 25 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-5
- fix valgrind on ppc/ppc64 where PAGESIZE is 64K (#211598)

* Sun Oct  1 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-4
- adjust for glibc-2.5

* Wed Sep 27 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-3
- another DW_CFA_set_loc handling fix

* Tue Sep 26 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-2
- fix openat handling (#208097)
- fix DW_CFA_set_loc handling

* Tue Sep 19 2006 Jakub Jelinek <jakub@redhat.com> 3.2.1-1
- update to 3.2.1 bugfix release
  - SSE3 emulation fixes, reduce memcheck false positive rate,
    4 dozens of bugfixes

* Mon Aug 21 2006 Jakub Jelinek <jakub@redhat.com> 3.2.0-5
- handle the new i686/x86_64 nops (#203273)

* Fri Jul 28 2006 Jeremy Katz <katzj@redhat.com> - 1:3.2.0-4
- rebuild to bring ppc back

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1:3.2.0-3.1
- rebuild

* Fri Jun 16 2006 Jakub Jelinek <jakub@redhat.com> 3.2.0-3
- handle [sg]et_robust_list syscall on ppc{32,64}

* Fri Jun 16 2006 Jakub Jelinek <jakub@redhat.com> 3.2.0-2
- fix ppc64 symlink to 32-bit valgrind libdir
- handle a few extra ppc64 syscalls

* Thu Jun 15 2006 Jakub Jelinek <jakub@redhat.com> 3.2.0-1
- update to 3.2.0
  - ppc64 support

* Fri May 26 2006 Jakub Jelinek <jakub@redhat.com> 3.1.1-3
- handle [sg]et_robust_list syscalls on i?86/x86_64
- handle *at syscalls on ppc
- ensure on x86_64 both 32-bit and 64-bit glibc{,-devel} are
  installed in the buildroot (#191820)

* Wed Apr 12 2006 Jakub Jelinek <jakub@redhat.com> 3.1.1-2
- handle many syscalls that were unhandled before, especially on ppc

* Mon Apr  3 2006 Jakub Jelinek <jakub@redhat.com> 3.1.1-1
- upgrade to 3.1.1
  - many bugfixes

* Mon Mar 13 2006 Jakub Jelinek <jakub@redhat.com> 3.1.0-2
- add support for DW_CFA_val_offset{,_sf}, DW_CFA_def_cfa_sf
  and skip over DW_CFA_val_expression quietly
- adjust libc/ld.so filenames in glibc-2.4.supp for glibc 2.4
  release

* Mon Jan  9 2006 Jakub Jelinek <jakub@redhat.com> 3.1.0-1
- upgrade to 3.1.0 (#174582)
  - many bugfixes, ppc32 support

* Thu Oct 13 2005 Jakub Jelinek <jakub@redhat.com> 3.0.1-2
- remove Obsoletes for valgrind-callgrind, as it has been
  ported to valgrind 3.0.x already

* Sun Sep 11 2005 Jakub Jelinek <jakub@redhat.com> 3.0.1-1
- upgrade to 3.0.1
  - many bugfixes
- handle xattr syscalls on x86-64 (Ulrich Drepper)

* Fri Aug 12 2005 Jakub Jelinek <jakub@redhat.com> 3.0.0-3
- fix amd64 handling of cwtd instruction
- fix amd64 handling of e.g. sarb $0x4,val(%%rip)
- speedup amd64 insn decoding

* Fri Aug 12 2005 Jakub Jelinek <jakub@redhat.com> 3.0.0-2
- lower x86_64 stage2 base from 112TB down to 450GB, so that
  valgrind works even on 2.4.x kernels.  Still way better than
  1.75GB that stock valgrind allows

* Fri Aug 12 2005 Jakub Jelinek <jakub@redhat.com> 3.0.0-1
- upgrade to 3.0.0
  - x86_64 support
- temporarily obsolete valgrind-callgrind, as it has not been
  ported yet

* Tue Jul 12 2005 Jakub Jelinek <jakub@redhat.com> 2.4.0-3
- build some insn tests with -mmmx, -msse or -msse2 (#161572)
- handle glibc-2.3.90 the same way as 2.3.[0-5]

* Wed Mar 30 2005 Jakub Jelinek <jakub@redhat.com> 2.4.0-2
- resurrect the non-upstreamed part of valgrind_h patch
- remove 2.1.2-4G patch, seems to be upstreamed
- resurrect passing -fno-builtin in memcheck tests

* Sun Mar 27 2005 Colin Walters <walters@redhat.com> 2.4.0-1
- New upstream version 
- Update valgrind-2.2.0-regtest.patch to 2.4.0; required minor
  massaging
- Disable valgrind-2.1.2-4G.patch for now; Not going to touch this,
  and Fedora does not ship 4G kernel by default anymore
- Remove upstreamed valgrind-2.2.0.ioctls.patch
- Remove obsolete valgrind-2.2.0-warnings.patch; Code is no longer
  present
- Remove upstreamed valgrind-2.2.0-valgrind_h.patch
- Remove obsolete valgrind-2.2.0-unnest.patch and
  valgrind-2.0.0-pthread-stacksize.patch; valgrind no longer
  includes its own pthread library

* Thu Mar 17 2005 Jakub Jelinek <jakub@redhat.com> 2.2.0-10
- rebuilt with GCC 4

* Tue Feb  8 2005 Jakub Jelinek <jakub@redhat.com> 2.2.0-8
- avoid unnecessary use of nested functions for pthread_once
  cleanup

* Mon Dec  6 2004 Jakub Jelinek <jakub@redhat.com> 2.2.0-7
- update URL (#141873)

* Tue Nov 16 2004 Jakub Jelinek <jakub@redhat.com> 2.2.0-6
- act as if NVALGRIND is defined when using <valgrind.h>
  in non-m32/i386 programs (#138923)
- remove weak from VALGRIND_PRINTF*, make it static and
  add unused attribute

* Mon Nov  8 2004 Jakub Jelinek <jakub@redhat.com> 2.2.0-4
- fix a printout and possible problem with local variable
  usage around setjmp (#138254)

* Tue Oct  5 2004 Jakub Jelinek <jakub@redhat.com> 2.2.0-3
- remove workaround for buggy old makes (#134563)

* Fri Oct  1 2004 Jakub Jelinek <jakub@redhat.com> 2.2.0-2
- handle some more ioctls (Peter Jones, #131967)

* Thu Sep  2 2004 Jakub Jelinek <jakub@redhat.com> 2.2.0-1
- update to 2.2.0

* Thu Jul 22 2004 Jakub Jelinek <jakub@redhat.com> 2.1.2-3
- fix packaging of documentation

* Tue Jul 20 2004 Jakub Jelinek <jakub@redhat.com> 2.1.2-2
- allow tracing of 32-bit binaries on x86-64

* Tue Jul 20 2004 Jakub Jelinek <jakub@redhat.com> 2.1.2-1
- update to 2.1.2
- run make regtest as part of package build
- use glibc-2.3 suppressions instead of glibc-2.2 suppressions

* Thu Apr 29 2004 Colin Walters <walters@redhat.com> 2.0.0-1
- update to 2.0.0

* Tue Feb 25 2003 Jeff Johnson <jbj@redhat.com> 1.9.4-0.20030228
- update to 1.9.4 from CVS.
- dwarf patch from Graydon Hoare.
- sysinfo patch from Graydon Hoare, take 1.

* Fri Feb 14 2003 Jeff Johnson <jbj@redhat.com> 1.9.3-6.20030207
- add return codes to syscalls.
- fix: set errno after syscalls.

* Tue Feb 11 2003 Graydon Hoare <graydon@redhat.com> 1.9.3-5.20030207
- add handling for separate debug info (+fix).
- handle blocking readv/writev correctly.
- comment out 4 overly zealous pthread checks.

* Tue Feb 11 2003 Jeff Johnson <jbj@redhat.com> 1.9.3-4.20030207
- move _pthread_desc to vg_include.h.
- implement pthread_mutex_timedlock().
- implement pthread_barrier_wait().

* Mon Feb 10 2003 Jeff Johnson <jbj@redhat.com> 1.9.3-3.20030207
- import all(afaik) missing functionality from linuxthreads.

* Sun Feb  9 2003 Jeff Johnson <jbj@redhat.com> 1.9.3-2.20030207
- import more missing functionality from linuxthreads in glibc-2.3.1.

* Sat Feb  8 2003 Jeff Johnson <jbj@redhat.com> 1.9.3-1.20030207
- start fixing nptl test cases.

* Fri Feb  7 2003 Jeff Johnson <jbj@redhat.com> 1.9.3-0.20030207
- build against current 1.9.3 with nptl hacks.

* Tue Oct 15 2002 Alexander Larsson <alexl@redhat.com>
- Update to 1.0.4

* Fri Aug  9 2002 Alexander Larsson <alexl@redhat.com>
- Update to 1.0.0

* Wed Jul  3 2002 Alexander Larsson <alexl@redhat.com>
- Update to pre4.

* Tue Jun 18 2002 Alexander Larsson <alla@lysator.liu.se>
- Add threadkeys and extra suppressions patches. Bump epoch.

* Mon Jun 17 2002 Alexander Larsson <alla@lysator.liu.se>
- Updated to 1.0pre1

* Tue May 28 2002 Alex Larsson <alexl@redhat.com>
- Updated to 20020524. Added GLIBC_PRIVATE patch

* Thu May  9 2002 Jonathan Blandford <jrb@redhat.com>
- add missing symbol __pthread_clock_settime

* Wed May  8 2002 Alex Larsson <alexl@redhat.com>
- Update to 20020508

* Mon May  6 2002 Alex Larsson <alexl@redhat.com>
- Update to 20020503b

* Thu May  2 2002 Alex Larsson <alexl@redhat.com>
- update to new snapshot

* Mon Apr 29 2002 Alex Larsson <alexl@redhat.com> 20020428-1
- update to new snapshot

* Fri Apr 26 2002 Jeremy Katz <katzj@redhat.com> 20020426-1
- update to new snapshot

* Thu Apr 25 2002 Alex Larsson <alexl@redhat.com> 20020424-5
- Added stack patch. Commented out other patches.

* Wed Apr 24 2002 Nalin Dahyabhai <nalin@redhat.com> 20020424-4
- filter out GLIBC_PRIVATE requires, add preload patch

* Wed Apr 24 2002 Alex Larsson <alexl@redhat.com> 20020424-3
- Make glibc 2.2 and XFree86 4 the default supressions

* Wed Apr 24 2002 Alex Larsson <alexl@redhat.com> 20020424-2
- Added patch that includes atomic.h

* Wed Apr 24 2002 Alex Larsson <alexl@redhat.com> 20020424-1
- Initial build
