%global _hardened_build 1

# Trim older changelog entries.
# https://lists.fedoraproject.org/pipermail/devel/2013-April/thread.html#181627
%global _changelog_trimtime %(date +%s -d "2 years ago")

# Verify tarball signature with GPGv2 (only possible for stable branches).
%global verify_tarball_signature 1

# Filter perl provides
%{?perl_default_filter}

Summary:       Access and modify virtual machine disk images
Name:          libguestfs
Epoch:         1
Version:       1.36.3
Release:       6%{?dist}.3
License:       LGPLv2+

# Source and patches.
URL:           http://libguestfs.org/
Source0:       http://libguestfs.org/download/1.36-stable/%{name}-%{version}.tar.gz

%if 0%{verify_tarball_signature}
Source1:       http://libguestfs.org/download/1.36-stable/%{name}-%{version}.tar.gz.sig
%endif

ExclusiveArch: x86_64 %{power64} aarch64

# RHEL 7 git repository is:
# https://github.com/libguestfs/libguestfs/tree/rhel-7.4
# Use 'copy-patches.sh' to copy the patches from the git repo
# to the current directory.

# Patches.
Patch0001:     0001-RHEL-7-Remove-libguestfs-live-RHBZ-798980.patch
Patch0002:     0002-RHEL-7-Remove-9p-APIs-from-RHEL-RHBZ-921710.patch
Patch0003:     0003-RHEL-7-Disable-unsupported-remote-drive-protocols-RH.patch
Patch0004:     0004-RHEL-7-Remove-User-Mode-Linux-RHBZ-1144197.patch
Patch0005:     0005-RHEL-7-v2v-Select-correct-qemu-binary-for-o-qemu-mod.patch
Patch0006:     0006-RHEL-7-v2v-Disable-the-qemu-boot-option-RHBZ-1147313.patch
Patch0007:     0007-RHEL-7-Revert-tests-rsync-Skip-this-test-when-the-ba.patch
Patch0008:     0008-RHEL-7-Revert-appliance-Change-example-ping-lines-to.patch
Patch0009:     0009-RHEL-7-Revert-launch-libvirt-Use-qemu-bridge-helper-.patch
Patch0010:     0010-RHEL-7-Revert-launch-libvirt-Better-error-when-bridg.patch
Patch0011:     0011-RHEL-7-Revert-appliance-add-dhcp-client-on-Mageia.patch
Patch0012:     0012-RHEL-7-Revert-appliance-add-dhcpcd-and-gptfdisk-on-A.patch
Patch0013:     0013-RHEL-7-Revert-appliance-Use-dhclient-or-dhcpcd-inste.patch
Patch0014:     0014-RHEL-7-Disable-alternate-Augeas-lenses.patch
Patch0015:     0015-RHEL-7-Fix-list-of-supported-sound-cards-to-match-RH.patch
Patch0016:     0016-RHEL-7-v2v-efi-Remove-references-to-Fedora-kraxel-s-.patch
Patch0017:     0017-RHEL-7-Reject-use-of-libguestfs-winsupport-features-.patch
Patch0018:     0018-RHEL-7-daemon-umount-all-Hack-to-avoid-umount-sysroo.patch
Patch0019:     0019-RHEL-7-Fix-tests-for-libguestfs-winsupport-7.2.patch
Patch0020:     0020-RHEL-7-Revert-v2v-Add-a-support-matrix-to-the-manual.patch
Patch0021:     0021-RHEL-7-All-qemu-kvm-in-RHEL-7-supports-discard-of-qc.patch
Patch0022:     0022-RHEL-7-tests-Disable-daemon-tests-that-require-the-u.patch
Patch0023:     0023-RHEL-7-v2v-Disable-the-virt-v2v-in-place-option.patch
Patch0024:     0024-RHEL-7-v2v-Remove-dcpath-option-RHBZ-1315237-RHBZ-14.patch
Patch0025:     0025-RHEL-7-v2v-i-disk-force-VNC-as-display-RHBZ-1372671.patch
Patch0026:     0026-RHEL-7-v2v-do-not-mention-SUSE-Xen-hosts-RHBZ-143020.patch
Patch0027:     0027-sysprep-Remove-DHCP_HOSTNAME-from-ifcfg-files-RHBZ-1.patch
Patch0028:     0028-p2v-v2v-Ensure-the-full-version-is-always-available-.patch
Patch0029:     0029-p2v-Run-fewer-scp-commands.patch
Patch0030:     0030-p2v-Fix-list-of-files-in-documentation.patch
Patch0031:     0031-p2v-tests-Fix-fake-scp-command-so-it-can-handle-mult.patch
Patch0032:     0032-v2v-windows-convert-fix-virtio-block-driver-installa.patch
Patch0033:     0033-v2v-o-qemu-Fix-creation-of-ICH6-sound-device.patch
Patch0034:     0034-ocaml-Add-Bytes.sub_string-function-to-Bytes-compat-.patch
Patch0035:     0035-mllib-Add-Char.hexdigit-function.patch
Patch0036:     0036-v2v-Implement-i-vmx-to-read-VMware-vmx-files-directl.patch
Patch0037:     0037-v2v-tests-Fix-i-vmx-test-so-it-is-more-stable.patch
Patch0038:     0038-v2v-o-rhv-Quote-parameter-to-rm-rf.patch
Patch0039:     0039-v2v-windows-Install-both-legacy-and-modern-virtio-ke.patch
Patch0040:     0040-v2v-o-rhv-Add-Windows-2016-Server-type-in-OVF-output.patch
Patch0041:     0041-daemon-lvm-Pass-yes-option-to-force-pvresize-RHBZ-14.patch
Patch0042:     0042-resize-make-sure-the-input-disk-is-read-only.patch
Patch0043:     0043-lib-libvirt-Pass-copyonread-flag-through-to-the-libv.patch
Patch0044:     0044-RHEL-7-v2v-disable-unconfig-of-manually-installed-VM.patch

# Use git for patch management.
BuildRequires: git

# Run autotools after applying the patches.
BuildRequires: autoconf, automake, libtool, gettext-devel

# Replacement README file for RHEL users.
Source4:       README-replacement.in

# Guestfish colour prompts.
Source5:       guestfish.sh

# Used to build the supermin appliance in Koji.
Source6:       yum.conf.in

# Keyring used to verify tarball signature.
%if 0%{verify_tarball_signature}
Source7:       libguestfs.keyring
%endif

# RHSRVANY and RHEV-APT, used for Windows virt-v2v conversions.
# RHSRVANY is built from source under Fedora from
# mingw32-srvany-1.0-15.20150115gitfd659e77.fc23.noarch
# RHEV-APT is taken from the RHEV Tools CD
# See https://bugzilla.redhat.com/show_bug.cgi?id=1186850
Source96:      rhsrvany.exe
Source97:      RHEV-Application-Provisioning-Tool.exe_4.12

Source98:      brew-overrides.sh
Source99:      copy-patches.sh

# Basic build requirements for the library and virt tools.
BuildRequires: gcc
BuildRequires: supermin5-devel >= 5.1.16-2
BuildRequires: hivex-devel >= 1.3.10-5.8.el7
BuildRequires: perl(Pod::Simple)
BuildRequires: perl(Pod::Man)
BuildRequires: /usr/bin/pod2text
BuildRequires: po4a
BuildRequires: augeas-devel
BuildRequires: readline-devel
BuildRequires: genisoimage
BuildRequires: libxml2-devel
BuildRequires: createrepo
BuildRequires: glibc-static
BuildRequires: libselinux-utils
BuildRequires: libselinux-devel
BuildRequires: fuse, fuse-devel
BuildRequires: pcre-devel
BuildRequires: file-devel
BuildRequires: libvirt-devel
BuildRequires: gperf
BuildRequires: flex
BuildRequires: bison
BuildRequires: libdb-utils
BuildRequires: cpio
BuildRequires: libconfig-devel
BuildRequires: xz-devel
BuildRequires: zip
BuildRequires: unzip
BuildRequires: systemd-units
BuildRequires: netpbm-progs
BuildRequires: icoutils
%ifnarch aarch64 %{power64}
# RHBZ#1177910
BuildRequires: libvirt-daemon-kvm
%endif
#BuildRequires: perl(Expect)
BuildRequires: libacl-devel
BuildRequires: libcap-devel
#BuildRequires: libldm-devel
BuildRequires: yajl-devel
BuildRequires: systemd-devel
BuildRequires: bash-completion
BuildRequires: /usr/bin/ping
BuildRequires: /usr/bin/wget
BuildRequires: curl
BuildRequires: xz
BuildRequires: gtk3-devel
BuildRequires: dbus-devel
BuildRequires: /usr/bin/qemu-img
BuildRequires: perl(Win::Hivex)
BuildRequires: perl(Win::Hivex::Regedit)
%if 0%{verify_tarball_signature}
BuildRequires: gnupg2
%endif

# For language bindings.
# Build using OCaml with fix for CVE-2015-8869.
BuildRequires: ocaml >= 4.01.0-22.7.el7
BuildRequires: ocaml-ocamldoc
# Make sure to get the performance fix for findlib.
BuildRequires: ocaml-findlib-devel >= 1.3.3-7.el7
BuildRequires: ocaml-gettext-devel
BuildRequires: lua
BuildRequires: lua-devel
BuildRequires: perl-devel
BuildRequires: perl-macros
BuildRequires: perl(Sys::Virt)
BuildRequires: perl(Test::More)
BuildRequires: perl(Test::Pod) >= 1.00
BuildRequires: perl(Test::Pod::Coverage) >= 1.00
BuildRequires: perl(Module::Build)
BuildRequires: perl(ExtUtils::CBuilder)
BuildRequires: perl(Locale::TextDomain)
BuildRequires: python-devel
BuildRequires: libvirt-python
BuildRequires: ruby-devel
BuildRequires: rubygem-rake
BuildRequires: rubygem(minitest)
#BuildRequires: rubygem(test-unit)
BuildRequires: ruby-irb
BuildRequires: java-1.7.0-openjdk
BuildRequires: java-1.7.0-openjdk-devel
BuildRequires: jpackage-utils
#BuildRequires: php-devel
#BuildRequires: erlang-erts
#BuildRequires: erlang-erl_interface
BuildRequires: glib2-devel
BuildRequires: gobject-introspection-devel
BuildRequires: gjs
#%ifarch %{golang_arches}
#BuildRequires: golang
#%endif

# Build requirements for the appliance.
#
# Get the initial list by doing:
#   for f in `cat appliance/packagelist`; do echo $f; done | sort -u
# However you have to edit the list down to packages which exist in
# current RHEL, since supermin ignores non-existent packages.
BuildRequires: acl attr augeas-libs bash binutils btrfs-progs bzip2 coreutils cpio cryptsetup curl diffutils dosfstools e2fsprogs file findutils gawk gdisk genisoimage grep gzip hivex iproute iputils kernel kmod kpartx less libcap libselinux libxml2 lsof lsscsi lvm2 lzop mdadm openssh-clients parted pciutils pcre policycoreutils procps psmisc qemu-img rsync scrub sed squashfs-tools strace systemd tar udev util-linux vim-minimal which xfsprogs xz yajl
%ifarch x86_64
BuildRequires: gfs2-utils
%endif
%ifarch %{ix86} x86_64
BuildRequires: syslinux syslinux-extlinux
%endif

# For building the appliance.
Requires:      supermin5 >= 5.1.16-2

# The daemon dependencies are not included automatically, because it
# is buried inside the appliance, so list them here.
Requires:      augeas-libs
Requires:      libacl
Requires:      libcap
Requires:      hivex >= 1.3.10-5.8.el7
Requires:      pcre
Requires:      libselinux
Requires:      systemd-libs
Requires:      yajl

# RHBZ#1211321
Requires:      kernel

# Older lvmetad "forgets" VGs if you change their UUID.  libguestfs
# since 1.34 enables lvmetad.  So we must ensure we have new enough
# LVM:
Requires:      lvm2 >= 7:2.02.166-1.el7

# For core inspection API.
Requires:      libdb-utils
Requires:      osinfo-db

# For core mount-local (FUSE) API.
Requires:      fuse

# For core disk-create API.
Requires:      /usr/bin/qemu-img

# For libvirt backend.
%ifarch %{ix86} x86_64 %{arm} aarch64 %{power64}
Requires:      libvirt-daemon-kvm >= 1.2.8-3
%endif
%ifarch aarch64
Requires:      AAVMF
# RHBZ#1177910
# RHBZ#1463646
Requires:      qemu-kvm
%endif
%ifarch %{power64}
# RHBZ#1177910
Requires:      qemu-kvm-rhev
%endif

# https://fedoraproject.org/wiki/Packaging:No_Bundled_Libraries#Packages_granted_exceptions
Provides:      bundled(gnulib)

# Conflicts with libguestfs-winsupport from RHEL 7.0.  You need to
# use the RHEL 7.2+ package.
Conflicts:     libguestfs-winsupport < 7.2


%description
Libguestfs is a library for accessing and modifying virtual machine
disk images.  http://libguestfs.org

It can be used to make batch configuration changes to guests, get
disk used/free statistics (virt-df), migrate between hypervisors
(virt-p2v, virt-v2v), perform backups and guest clones, change
registry/UUID/hostname info, build guests from scratch (virt-builder)
and much more.

Libguestfs uses Linux kernel and qemu code, and can access any type of
guest filesystem that Linux and qemu can, including but not limited
to: ext2/3/4, btrfs, FAT and NTFS, LVM, many different disk partition
schemes, qcow, qcow2, vmdk.

Libguestfs for Red Hat Enterprise Linux is split into several subpackages.
The basic subpackages are:

               libguestfs  C library
         libguestfs-tools  virt-* tools, guestfish and guestmount (FUSE)
       libguestfs-tools-c  only the subset of virt tools written in C
                             (for reduced dependencies)
                 virt-dib  safe and secure diskimage-builder replacement
                 virt-v2v  convert virtual machines to run on KVM (V2V)
           virt-p2v-maker  convert physical machines to run on KVM (P2V)

For enhanced features, install:

          libguestfs-gfs2  adds Global Filesystem (GFS2) support
 libguestfs-inspect-icons  adds support for inspecting guest icons
        libguestfs-rescue  enhances virt-rescue shell with more tools
         libguestfs-rsync  rsync to/from guest filesystems
           libguestfs-xfs  adds XFS support

For developers:

         libguestfs-devel  C/C++ header files and library
  libguestfs-benchmarking  Benchmarking utilities

Language bindings:

 libguestfs-gobject-devel  GObject bindings and GObject Introspection
    libguestfs-java-devel  Java bindings
              lua-guestfs  Lua bindings
   ocaml-libguestfs-devel  OCaml bindings
         perl-Sys-Guestfs  Perl bindings
        python-libguestfs  Python bindings
          ruby-libguestfs  Ruby bindings


%ifarch aarch64 x86_64
%package benchmarking
Summary:       Benchmarking utilities for %{name}
Requires:      %{name} = %{epoch}:%{version}-%{release}


%description benchmarking
%{name}-benchmarking contains utilities for benchmarking and
performance analysis of %{name}, and also for general
understanding of the performance of the kernel and qemu when booting
small appliances.
%endif


%package devel
Summary:       Development tools and libraries for %{name}
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      pkgconfig

# For libguestfs-make-fixed-appliance.
Requires:      xz
Requires:      %{name}-tools-c = %{epoch}:%{version}-%{release}


%description devel
%{name}-devel contains development tools and libraries
for %{name}.


%ifarch x86_64
%package gfs2
Summary:       GFS2 support for %{name}
License:       LGPLv2+
Requires:      %{name} = %{epoch}:%{version}-%{release}

%description gfs2
This adds GFS2 support to %{name}.  Install it if you want to process
disk images containing GFS2.
%endif


%package rescue
Summary:       Additional tools for virt-rescue
License:       LGPLv2+
Requires:      %{name}-tools-c = %{epoch}:%{version}-%{release}

%description rescue
This adds additional tools to use inside the virt-rescue shell,
such as ssh, network utilities, editors and debugging utilities.


%package rsync
Summary:       rsync support for %{name}
License:       LGPLv2+
Requires:      %{name} = %{epoch}:%{version}-%{release}

%description rsync
This adds rsync support to %{name}.  Install it if you want to use
rsync to upload or download files into disk images.


%package xfs
Summary:       XFS support for %{name}
License:       LGPLv2+
Requires:      %{name} = %{epoch}:%{version}-%{release}

%description xfs
This adds XFS support to %{name}.  Install it if you want to process
disk images containing XFS.


%package inspect-icons
Summary:       Additional dependencies for inspecting guest icons
License:       LGPLv2+
BuildArch:     noarch
Requires:      %{name} = %{epoch}:%{version}-%{release}

Requires:      netpbm-progs
Requires:      icoutils


%description inspect-icons
%{name}-inspect-icons is a metapackage that pulls in additional
dependencies required by libguestfs to pull icons out of non-Linux
guests.  Install this package if you want libguestfs to be able to
inspect non-Linux guests and display icons from them.

The only reason this is a separate package is to avoid core libguestfs
having to depend on Perl.  See https://bugzilla.redhat.com/1194158


%package tools-c
Summary:       System administration tools for virtual machines
License:       GPLv2+
Requires:      %{name} = %{epoch}:%{version}-%{release}

# for guestfish:
#Requires:      /usr/bin/emacs #theoretically, but too large
Requires:      /usr/bin/hexedit
Requires:      /usr/bin/less
Requires:      /usr/bin/man
Requires:      /usr/bin/vi

# Obsolete and replace earlier packages.
# NB: This was present in RHEL 7.0, removed accidentally in RHEL 7.1
# (causing RHBZ#1212002), then re-added.  Make sure to remove this
# section completely in RHEL 8.0.
Provides:      guestfish = %{epoch}:%{version}-%{release}
Obsoletes:     guestfish < %{epoch}:%{version}-%{release}
Provides:      libguestfs-mount = %{epoch}:%{version}-%{release}
Obsoletes:     libguestfs-mount < %{epoch}:%{version}-%{release}

# for virt-builder:
Requires:      gnupg
Requires:      xz
#Requires:     nbdkit, nbdkit-plugin-xz
Requires:      curl


%description tools-c
This package contains miscellaneous system administrator command line
tools for virtual machines.

Note that you should install %{name}-tools (which pulls in
this package).  This package is only used directly when you want
to avoid dependencies on Perl.


%package tools
Summary:       System administration tools for virtual machines
License:       GPLv2+
BuildArch:     noarch
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      %{name}-tools-c = %{epoch}:%{version}-%{release}

# NB: Only list deps here which are not picked up automatically.
Requires:      perl(Sys::Virt)
Requires:      perl(Win::Hivex) >= 1.2.7


%description tools
This package contains miscellaneous system administrator command line
tools for virtual machines.

Guestfish is the Filesystem Interactive SHell, for accessing and
modifying virtual machine disk images from the command line and shell
scripts.

The guestmount command lets you mount guest filesystems on the host
using FUSE and %{name}.

Virt-alignment-scan scans virtual machines looking for partition
alignment problems.

Virt-builder is a command line tool for rapidly making disk images
of popular free operating systems.

Virt-cat is a command line tool to display the contents of a file in a
virtual machine.

Virt-copy-in and virt-copy-out are command line tools for uploading
and downloading files and directories to and from virtual machines.

Virt-customize is a command line tool for customizing virtual machine
disk images.

Virt-df is a command line tool to display free space on virtual
machine filesystems.  Unlike other tools, it doesn’t just display the
amount of space allocated to a virtual machine, but can look inside
the virtual machine to see how much space is really being used.  It is
like the df(1) command, but for virtual machines, except that it also
works for Windows virtual machines.

Virt-diff shows the differences between virtual machines.

Virt-edit is a command line tool to edit the contents of a file in a
virtual machine.

Virt-filesystems is a command line tool to display the filesystems,
partitions, block devices, LVs, VGs and PVs found in a disk image
or virtual machine.  It replaces the deprecated programs
virt-list-filesystems and virt-list-partitions with a much more
capable tool.

Virt-format is a command line tool to erase and make blank disks.

Virt-get-kernel extracts a kernel/initrd from a disk image.

Virt-inspector examines a virtual machine and tries to determine the
version of the OS, the kernel version, what drivers are installed,
whether the virtual machine is fully virtualized (FV) or
para-virtualized (PV), what applications are installed and more.

Virt-log is a command line tool to display the log files from a
virtual machine.

Virt-ls is a command line tool to list out files in a virtual machine.

Virt-make-fs is a command line tool to build a filesystem out of
a collection of files or a tarball.

Virt-rescue provides a rescue shell for making interactive,
unstructured fixes to virtual machines.

Virt-resize can resize existing virtual machine disk images.

Virt-sparsify makes virtual machine disk images sparse (thin-provisioned).

Virt-sysprep lets you reset or unconfigure virtual machines in
preparation for cloning them.

Virt-tail follows (tails) a log file within a guest, like 'tail -f'.

Virt-tar-in and virt-tar-out are archive, backup and upload tools
for virtual machines.  These replace the deprecated program virt-tar.

Virt-win-reg lets you look at and modify the Windows Registry of
Windows virtual machines.


%package -n virt-dib
Summary:       Safe and secure diskimage-builder replacement
License:       GPLv2+

Requires:      %{name} = %{epoch}:%{version}-%{release}


%description -n virt-dib
Virt-dib is a safe and secure alternative to the OpenStack
diskimage-builder command.  It is compatible with most
diskimage-builder elements.


%ifnarch %{power64}
%package -n virt-v2v
Summary:       Convert a virtual machine to run on KVM
License:       GPLv2+

Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      %{name}-tools-c = %{epoch}:%{version}-%{release}
# First version that added support for ssh, curl, json: URLs.
# (RHBZ#1226683, RHBZ#1226684, RHBZ#1226697).
Requires:      qemu-kvm >= 1.5.3-92.el7

# For Windows conversions.
%ifarch x86_64 aarch64
Requires:      libguestfs-winsupport >= 7.2
%endif

Requires:      gawk
Requires:      gzip
Requires:      unzip
Requires:      curl
Requires:      /usr/bin/virsh

# Ensure the UEFI firmware is available, to properly convert
# EFI guests (RHBZ#1429643).
%ifarch x86_64
Requires:      OVMF
%endif
%ifarch aarch64
Requires:      AAVMF
%endif


%description -n virt-v2v
Virt-v2v converts virtual machines from non-KVM hypervisors
to run under KVM.

To convert physical machines, see the virt-p2v-maker package.
%endif


%package -n virt-p2v-maker
Summary:       Convert a physical machine to run on KVM
License:       GPLv2+

Requires:      gawk
Requires:      gzip

# virt-p2v-make-disk runs virt-builder:
Requires:      %{name}-tools-c = %{epoch}:%{version}-%{release}

# virt-p2v-make-kickstart runs strip:
Requires:      binutils


%description -n virt-p2v-maker
Virt-p2v converts (virtualizes) physical machines so they can be run
as virtual machines under KVM.

This package contains the tools needed to make a virt-p2v boot CD or
USB key which is booted on the physical machine to perform the
conversion.  You also need virt-v2v installed somewhere else to
complete the conversion.

To convert virtual machines from other hypervisors, see virt-v2v.


%package bash-completion
Summary:       Bash tab-completion scripts for %{name} tools
BuildArch:     noarch
Requires:      bash-completion >= 2.0
Requires:      %{name}-tools-c = %{epoch}:%{version}-%{release}


%description bash-completion
Install this package if you want intelligent bash tab-completion
for guestfish, guestmount and various virt-* tools.


%package -n ocaml-%{name}
Summary:       OCaml bindings for %{name}
Requires:      %{name} = %{epoch}:%{version}-%{release}


%description -n ocaml-%{name}
ocaml-%{name} contains OCaml bindings for %{name}.

This is for toplevel and scripting access only.  To compile OCaml
programs which use %{name} you will also need ocaml-%{name}-devel.


%package -n ocaml-%{name}-devel
Summary:       OCaml bindings for %{name}
Requires:      ocaml-%{name} = %{epoch}:%{version}-%{release}


%description -n ocaml-%{name}-devel
ocaml-%{name}-devel contains development libraries
required to use the OCaml bindings for %{name}.


%package -n perl-Sys-Guestfs
Summary:       Perl bindings for %{name} (Sys::Guestfs)
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))


%description -n perl-Sys-Guestfs
perl-Sys-Guestfs contains Perl bindings for %{name} (Sys::Guestfs).


%package -n python-%{name}
Summary:       Python bindings for %{name}
Requires:      %{name} = %{epoch}:%{version}-%{release}

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%description -n python-%{name}
python-%{name} contains Python bindings for %{name}.


%package -n ruby-%{name}
Summary:       Ruby bindings for %{name}
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      ruby(release) = 2.0.0
Requires:      ruby
Provides:      ruby(guestfs) = %{version}

%description -n ruby-%{name}
ruby-%{name} contains Ruby bindings for %{name}.


%package java
Summary:       Java bindings for %{name}
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      java-headless >= 1.7.0
Requires:      jpackage-utils

%description java
%{name}-java contains Java bindings for %{name}.

If you want to develop software in Java which uses %{name}, then
you will also need %{name}-java-devel.


%package java-devel
Summary:       Java development package for %{name}
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      %{name}-java = %{epoch}:%{version}-%{release}

%description java-devel
%{name}-java-devel contains the tools for developing Java software
using %{name}.

See also %{name}-javadoc.


%package javadoc
Summary:       Java documentation for %{name}
BuildArch:     noarch
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      %{name}-java = %{epoch}:%{version}-%{release}
Requires:      jpackage-utils

%description javadoc
%{name}-javadoc contains the Java documentation for %{name}.


%package -n lua-guestfs
Summary:       Lua bindings for %{name}
Requires:      %{name} = %{epoch}:%{version}-%{release}
Requires:      lua

%description -n lua-guestfs
lua-guestfs contains Lua bindings for %{name}.


%package gobject
Summary:       GObject bindings for %{name}
Requires:      %{name} = %{epoch}:%{version}-%{release}

%description gobject
%{name}-gobject contains GObject bindings for %{name}.

To develop software against these bindings, you need to install
%{name}-gobject-devel.


%package gobject-devel
Summary:       GObject bindings for %{name}
Requires:      %{name}-gobject = %{epoch}:%{version}-%{release}
Requires:      gtk-doc

%description gobject-devel
%{name}-gobject contains GObject bindings for %{name}.

This package is needed if you want to write software using the
GObject bindings.  It also contains GObject Introspection information.


%package gobject-doc
Summary:       Documentation for %{name} GObject bindings
BuildArch:     noarch
Requires:      %{name}-gobject-devel = %{epoch}:%{version}-%{release}

%description gobject-doc
%{name}-gobject-doc contains documentation for
%{name} GObject bindings.


%package man-pages-ja
Summary:       Japanese (ja) man pages for %{name}
BuildArch:     noarch
Requires:      %{name} = %{epoch}:%{version}-%{release}

%description man-pages-ja
%{name}-man-pages-ja contains Japanese (ja) man pages
for %{name}.


%package man-pages-uk
Summary:       Ukrainian (uk) man pages for %{name}
BuildArch:     noarch
Requires:      %{name} = %{epoch}:%{version}-%{release}

%description man-pages-uk
%{name}-man-pages-uk contains Ukrainian (uk) man pages
for %{name}.


%prep
%if 0%{verify_tarball_signature}
tmphome="$(mktemp -d)"
gpgv2 --homedir "$tmphome" --keyring %{SOURCE7} %{SOURCE1} %{SOURCE0}
%endif
%setup -q

# For sVirt to work, the local temporary directory we use in the tests
# must be labelled the same way as /tmp.  This doesn't work if either
# the directory is on NFS (no SELinux labels) or if SELinux is
# disabled, hence the tests.
if [ "$(stat -f -L -c %T .)" != "nfs" ] && \
   [ "$(getenforce | tr '[A-Z]' '[a-z]')" != "disabled" ]; then
    chcon --reference=/tmp tmp
fi

# Use git to manage patches.
# http://rwmj.wordpress.com/2011/08/09/nice-rpm-git-patch-management-trick/
git init
git config user.email "libguestfs@redhat.com"
git config user.name "libguestfs"
git add .
git commit -a -q -m "%{version} baseline"
git am %{patches}

# Patches affect Makefile.am and configure.ac, so rerun autotools.
autoreconf
autoconf

mkdir -p daemon/m4

# Replace developer-centric README that ships with libguestfs, with
# our replacement file.
mv README README.orig
sed 's/@VERSION@/%{version}/g' < %{SOURCE4} > README


%build
# Test if network is available.
ip addr list ||:
ip route list ||:
if ping -c 3 -w 20 8.8.8.8 && wget http://libguestfs.org -O /dev/null; then
  extra=
else
  mkdir cachedir repo
  # -n 1 because of RHBZ#980502.
  find /var/cache/{dnf,yum} -type f -name '*.rpm' -print0 | \
    xargs -0 -n 1 cp -t repo
  createrepo repo
  sed -e "s|@PWD@|$(pwd)|" %{SOURCE6} > yum.conf
  extra=--with-supermin-packager-config=$(pwd)/yum.conf
fi

# aarch64/ppc64/ppc64le doesn't yet have a working qemu available in
# brew, and for that reason we have to hack things here.  See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1125575#c18
# https://bugzilla.redhat.com/show_bug.cgi?id=1177910
%ifarch aarch64 %{power64}
export vmchannel_test=no
export QEMU=/usr/libexec/qemu-kvm
%endif

# In RHEL >= 7.1, supermin 5 has a different name:
export SUPERMIN=%{_bindir}/supermin5

%{configure} \
  --with-default-backend=libvirt \
  --with-extra="rhel=%{rhel},release=%{release},libvirt" \
  --with-qemu="qemu-kvm qemu-system-%{_build_arch} qemu" \
  --disable-php \
  --disable-haskell \
  --disable-erlang \
  --disable-golang \
  $extra

# Building index-parse.c by hand works around a race condition in the
# autotools cruft, where two or more copies of yacc race with each
# other, resulting in a corrupted file.
#
# 'INSTALLDIRS' ensures that Perl and Ruby libs are installed in the
# vendor dir not the site dir.
make -j1 -C builder index-parse.c
make V=1 INSTALLDIRS=vendor %{?_smp_mflags}


%check

# Can't test on aarch64 or ppc64/ppc64le yet because we don't have
# a working qemu available in brew.
%ifnarch aarch64 %{power64}

# Note that the major tests are done after the package has been built.
#
# Here we only do a sanity check that kernel/qemu/libvirt/appliance is
# not broken.
#
# To perform the full test suite, see instructions here:
# https://www.redhat.com/archives/libguestfs/2015-September/msg00078.html

export LIBGUESTFS_DEBUG=1
export LIBGUESTFS_TRACE=1
export LIBVIRT_DEBUG=1

if ! make quickcheck QUICKCHECK_TEST_TOOL_ARGS="-t 1200"; then
    cat $HOME/.cache/libvirt/qemu/log/*
    exit 1
fi

%endif


%install
# This file is creeping over 1 MB uncompressed, and since it is
# included in the -devel subpackage, compress it to reduce
# installation size.
gzip -9 ChangeLog

# 'INSTALLDIRS' ensures that Perl and Ruby libs are installed in the
# vendor dir not the site dir.
make DESTDIR=$RPM_BUILD_ROOT INSTALLDIRS=vendor install

# Delete static libraries.
rm $( find $RPM_BUILD_ROOT -name '*.a' | grep -v /ocaml/ )

# Delete libtool files.
find $RPM_BUILD_ROOT -name '*.la' -delete

# Delete some bogus Perl files.
find $RPM_BUILD_ROOT -name perllocal.pod -delete
find $RPM_BUILD_ROOT -name .packlist -delete
find $RPM_BUILD_ROOT -name '*.bs' -delete
find $RPM_BUILD_ROOT -name 'bindtests.pl' -delete

# Remove obsolete binaries (RHBZ#947438).
rm $RPM_BUILD_ROOT%{_bindir}/virt-list-filesystems
rm $RPM_BUILD_ROOT%{_bindir}/virt-list-partitions
rm $RPM_BUILD_ROOT%{_bindir}/virt-tar
rm $RPM_BUILD_ROOT%{_mandir}/man1/virt-list-filesystems.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/virt-list-partitions.1*
rm $RPM_BUILD_ROOT%{_mandir}/man1/virt-tar.1*

# Don't use versioned jar file (RHBZ#1022133).
# See: https://bugzilla.redhat.com/show_bug.cgi?id=1022184#c4
mv $RPM_BUILD_ROOT%{_datadir}/java/%{name}-%{version}.jar \
  $RPM_BUILD_ROOT%{_datadir}/java/%{name}.jar

# Move installed documentation back to the source directory so
# we can install it using a %%doc rule.
mv $RPM_BUILD_ROOT%{_docdir}/libguestfs installed-docs
gzip --best installed-docs/*.xml

# Split up the monolithic packages file in the supermin appliance so
# we can install dependencies in subpackages.
pushd $RPM_BUILD_ROOT%{_libdir}/guestfs/supermin.d
function move_to
{
    grep -Ev "^$1$" < packages > packages-t
    mv packages-t packages
    echo "$1" >> "$2"
}
move_to curl            zz-packages-dib
move_to kpartx          zz-packages-dib
move_to qemu-img        zz-packages-dib
move_to which           zz-packages-dib
%ifarch x86_64
move_to gfs2-utils      zz-packages-gfs2
%endif
move_to iputils         zz-packages-rescue
move_to openssh-clients zz-packages-rescue
move_to pciutils        zz-packages-rescue
move_to strace          zz-packages-rescue
move_to vim-minimal     zz-packages-rescue
move_to rsync           zz-packages-rsync
move_to xfsprogs        zz-packages-xfs
popd

# If there is a bogus dependency on kernel-rt, rename it to 'kernel'
# instead.  This happens when the version of kernel-rt in brew is
# greater than the version of kernel (kernel-rt 'Provides: kernel').
pushd $RPM_BUILD_ROOT%{_libdir}/guestfs/supermin.d
sed 's/^kernel-rt$/kernel/' < packages > packages-t
mv packages-t packages
popd

# Guestfish colour prompts.
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

# Virt-tools data directory.
mkdir -p $RPM_BUILD_ROOT%{_datadir}/virt-tools
cp %{SOURCE96} $RPM_BUILD_ROOT%{_datadir}/virt-tools/rhsrvany.exe
cp %{SOURCE97} $RPM_BUILD_ROOT%{_datadir}/virt-tools/rhev-apt.exe

%ifarch %{power64}
# We don't ship virt-v2v on POWER (RHBZ#1287826).
rm $RPM_BUILD_ROOT%{_bindir}/virt-p2v*
rm $RPM_BUILD_ROOT%{_bindir}/virt-v2v*
rm $RPM_BUILD_ROOT%{_mandir}/man1/virt-p2v*
rm $RPM_BUILD_ROOT%{_mandir}/man1/virt-v2v*
rm -r $RPM_BUILD_ROOT%{_libdir}/virt-p2v
rm -r $RPM_BUILD_ROOT%{_datadir}/virt-p2v
rm -r $RPM_BUILD_ROOT%{_datadir}/virt-tools
%endif

# Delete the v2v test harness.  (This might or might not exist
# depending on extra BRs installed when the package is built, so use
# '-f' option here.)
rm -rf $RPM_BUILD_ROOT%{_libdir}/ocaml/v2v_test_harness
rm -rf $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs/dllv2v_test_harness*
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/virt-v2v-test-harness.1*

%ifnarch %{power64}
# Delete kiwi tools.
rm $RPM_BUILD_ROOT%{_bindir}/virt-p2v-make-kiwi
rm $RPM_BUILD_ROOT%{_mandir}/man1/virt-p2v-make-kiwi.1*
%endif

# Remove the .gitignore file from ocaml/html which will be copied to docdir.
rm ocaml/html/.gitignore

%ifarch aarch64 x86_64
# Copy the benchmarking tools and man pages, since upstream doesn't
# install them by default.  NB Don't install the libtool wrapper scripts.
libtool --mode=install install -m 0755 utils/boot-analysis/boot-analysis $RPM_BUILD_ROOT%{_bindir}/libguestfs-boot-analysis
libtool --mode=install install -m 0755 utils/boot-benchmark/boot-benchmark $RPM_BUILD_ROOT%{_bindir}/libguestfs-boot-benchmark
install -m 0755 utils/boot-benchmark/boot-benchmark-range.pl $RPM_BUILD_ROOT%{_bindir}/libguestfs-boot-benchmark-range.pl
install -m 0644 utils/boot-analysis/boot-analysis.1 $RPM_BUILD_ROOT%{_mandir}/man1/libguestfs-boot-analysis.1
install -m 0644 utils/boot-benchmark/boot-benchmark.1 $RPM_BUILD_ROOT%{_mandir}/man1/libguestfs-boot-benchmark.1
%endif

# Find locale files.
%find_lang %{name}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post java -p /sbin/ldconfig

%postun java -p /sbin/ldconfig


%files -f %{name}.lang
%doc COPYING README
%{_bindir}/libguestfs-test-tool
%{_libdir}/guestfs/
%exclude %{_libdir}/guestfs/supermin.d/zz-packages-*
%{_libdir}/libguestfs.so.*
%{_mandir}/man1/guestfs-faq.1*
%{_mandir}/man1/guestfs-performance.1*
%{_mandir}/man1/guestfs-recipes.1*
%{_mandir}/man1/guestfs-release-notes.1*
%{_mandir}/man1/guestfs-security.1*
%{_mandir}/man1/libguestfs-test-tool.1*


%ifarch aarch64 x86_64
%files benchmarking
%{_bindir}/libguestfs-boot-analysis
%{_bindir}/libguestfs-boot-benchmark
%{_bindir}/libguestfs-boot-benchmark-range.pl
%{_mandir}/man1/libguestfs-boot-analysis.1*
%{_mandir}/man1/libguestfs-boot-benchmark.1*
%endif


%files devel
%doc AUTHORS BUGS ChangeLog.gz HACKING TODO README
%doc examples/*.c
%doc installed-docs/*
%{_libdir}/libguestfs.so
%{_sbindir}/libguestfs-make-fixed-appliance
%{_mandir}/man1/guestfs-building.1*
%{_mandir}/man1/guestfs-hacking.1*
%{_mandir}/man1/guestfs-internals.1*
%{_mandir}/man1/guestfs-testing.1*
%{_mandir}/man1/libguestfs-make-fixed-appliance.1*
%{_mandir}/man3/guestfs.3*
%{_mandir}/man3/guestfs-examples.3*
%{_mandir}/man3/libguestfs.3*
%{_includedir}/guestfs.h
%{_libdir}/pkgconfig/libguestfs.pc

%ifarch x86_64
%files gfs2
%{_libdir}/guestfs/supermin.d/zz-packages-gfs2
%endif

%files rsync
%{_libdir}/guestfs/supermin.d/zz-packages-rsync

%files rescue
%{_libdir}/guestfs/supermin.d/zz-packages-rescue

%files xfs
%{_libdir}/guestfs/supermin.d/zz-packages-xfs


%files inspect-icons
# no files


%files tools-c
%doc README
%config(noreplace) %{_sysconfdir}/libguestfs-tools.conf
%{_sysconfdir}/virt-builder
%dir %{_sysconfdir}/xdg/virt-builder
%dir %{_sysconfdir}/xdg/virt-builder/repos.d
%config %{_sysconfdir}/xdg/virt-builder/repos.d/*
%config %{_sysconfdir}/profile.d/guestfish.sh
%{_mandir}/man5/libguestfs-tools.conf.5*
%{_bindir}/guestfish
%{_mandir}/man1/guestfish.1*
%{_bindir}/guestmount
%{_mandir}/man1/guestmount.1*
%{_bindir}/guestunmount
%{_mandir}/man1/guestunmount.1*
%{_bindir}/virt-alignment-scan
%{_mandir}/man1/virt-alignment-scan.1*
%{_bindir}/virt-builder
%{_mandir}/man1/virt-builder.1*
%{_bindir}/virt-cat
%{_mandir}/man1/virt-cat.1*
%{_bindir}/virt-copy-in
%{_mandir}/man1/virt-copy-in.1*
%{_bindir}/virt-copy-out
%{_mandir}/man1/virt-copy-out.1*
%{_bindir}/virt-customize
%{_mandir}/man1/virt-customize.1*
%{_bindir}/virt-df
%{_mandir}/man1/virt-df.1*
%{_bindir}/virt-diff
%{_mandir}/man1/virt-diff.1*
%{_bindir}/virt-edit
%{_mandir}/man1/virt-edit.1*
%{_bindir}/virt-filesystems
%{_mandir}/man1/virt-filesystems.1*
%{_bindir}/virt-format
%{_mandir}/man1/virt-format.1*
%{_bindir}/virt-get-kernel
%{_mandir}/man1/virt-get-kernel.1*
%{_bindir}/virt-index-validate
%{_mandir}/man1/virt-index-validate.1*
%{_bindir}/virt-inspector
%{_mandir}/man1/virt-inspector.1*
%{_bindir}/virt-log
%{_mandir}/man1/virt-log.1*
%{_bindir}/virt-ls
%{_mandir}/man1/virt-ls.1*
%{_bindir}/virt-make-fs
%{_mandir}/man1/virt-make-fs.1*
%{_bindir}/virt-rescue
%{_mandir}/man1/virt-rescue.1*
%{_bindir}/virt-resize
%{_mandir}/man1/virt-resize.1*
%{_bindir}/virt-sparsify
%{_mandir}/man1/virt-sparsify.1*
%{_bindir}/virt-sysprep
%{_mandir}/man1/virt-sysprep.1*
%{_bindir}/virt-tail
%{_mandir}/man1/virt-tail.1*
%{_bindir}/virt-tar-in
%{_mandir}/man1/virt-tar-in.1*
%{_bindir}/virt-tar-out
%{_mandir}/man1/virt-tar-out.1*


%files tools
%doc README
%{_bindir}/virt-win-reg
%{_mandir}/man1/virt-win-reg.1*


%files -n virt-dib
%doc COPYING README
%{_bindir}/virt-dib
%{_mandir}/man1/virt-dib.1*
%{_libdir}/guestfs/supermin.d/zz-packages-dib


%ifnarch %{power64}
%files -n virt-v2v
%doc COPYING README v2v/TODO
%{_bindir}/virt-v2v
%{_bindir}/virt-v2v-copy-to-local
%{_mandir}/man1/virt-v2v.1*
%{_mandir}/man1/virt-v2v-copy-to-local.1*
%{_datadir}/virt-tools


%files -n virt-p2v-maker
%doc COPYING README
%{_bindir}/virt-p2v-make-disk
%{_bindir}/virt-p2v-make-kickstart
%{_mandir}/man1/virt-p2v.1*
%{_mandir}/man1/virt-p2v-make-disk.1*
%{_mandir}/man1/virt-p2v-make-kickstart.1*
%{_datadir}/virt-p2v
%{_libdir}/virt-p2v
%endif


%files bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/guestfish
%{_datadir}/bash-completion/completions/guestmount
%{_datadir}/bash-completion/completions/guestunmount
%{_datadir}/bash-completion/completions/virt-*


%files -n ocaml-%{name}
%{_libdir}/ocaml/guestfs
%exclude %{_libdir}/ocaml/guestfs/*.a
%exclude %{_libdir}/ocaml/guestfs/*.cmxa
%exclude %{_libdir}/ocaml/guestfs/*.cmx
%exclude %{_libdir}/ocaml/guestfs/*.mli
%{_libdir}/ocaml/stublibs/dllmlguestfs.so
%{_libdir}/ocaml/stublibs/dllmlguestfs.so.owner


%files -n ocaml-%{name}-devel
%doc ocaml/examples/*.ml ocaml/html
%{_libdir}/ocaml/guestfs/*.a
%{_libdir}/ocaml/guestfs/*.cmxa
%{_libdir}/ocaml/guestfs/*.cmx
%{_libdir}/ocaml/guestfs/*.mli
%{_mandir}/man3/guestfs-ocaml.3*


%files -n perl-Sys-Guestfs
%doc perl/examples/*.pl
%{perl_vendorarch}/*
%{_mandir}/man3/Sys::Guestfs.3pm*
%{_mandir}/man3/guestfs-perl.3*


%files -n python-%{name}
%doc python/examples/*.py
%{python_sitearch}/libguestfsmod.so
%{python_sitearch}/guestfs.py
%{python_sitearch}/guestfs.pyc
%{python_sitearch}/guestfs.pyo
%{_mandir}/man3/guestfs-python.3*


%files -n ruby-%{name}
%doc ruby/examples/*.rb
%doc ruby/doc/site/*
%{ruby_vendorlibdir}/guestfs.rb
%{ruby_vendorarchdir}/_guestfs.so
%{_mandir}/man3/guestfs-ruby.3*


%files java
%{_libdir}/libguestfs_jni*.so.*
%{_datadir}/java/*.jar


%files java-devel
%doc java/examples/*.java
%{_libdir}/libguestfs_jni*.so
%{_mandir}/man3/guestfs-java.3*


%files javadoc
%{_javadocdir}/%{name}


%files -n lua-guestfs
%doc lua/examples/*.lua
%doc lua/examples/LICENSE
%{_libdir}/lua/*/guestfs.so
%{_mandir}/man3/guestfs-lua.3*


%files gobject
%{_libdir}/libguestfs-gobject-1.0.so.0*
%{_libdir}/girepository-1.0/Guestfs-1.0.typelib


%files gobject-devel
%{_libdir}/libguestfs-gobject-1.0.so
%{_includedir}/guestfs-gobject.h
%dir %{_includedir}/guestfs-gobject
%{_includedir}/guestfs-gobject/*.h
%{_datadir}/gir-1.0/Guestfs-1.0.gir
%{_libdir}/pkgconfig/libguestfs-gobject-1.0.pc


%files gobject-doc
%{_datadir}/gtk-doc/html/guestfs


%files man-pages-ja
%lang(ja) %{_mandir}/ja/man1/*.1*
%lang(ja) %{_mandir}/ja/man3/*.3*
%lang(ja) %{_mandir}/ja/man5/*.5*


%files man-pages-uk
%lang(uk) %{_mandir}/uk/man1/*.1*
%lang(uk) %{_mandir}/uk/man3/*.3*
%lang(uk) %{_mandir}/uk/man5/*.5*


%changelog
* Wed Aug 02 2017 Pino Toscano <ptoscano@redhat.com> - 1:1.36.3-6.el7_4.3
- v2v: disable unconfiguration of manually installed VMware tools.
  resolves: rhbz#1480623

* Mon Jul 17 2017 Pino Toscano <ptoscano@redhat.com> - 1:1.36.3-6.el7_4.2
- Make sure kernel-rt is never used as Requires.
  resolves: rhbz#1471829

* Wed Jul 12 2017 Pino Toscano <ptoscano@redhat.com> - 1:1.36.3-6.el7_4.1
- Enable the copyonread flag when running the appliance using libvirt.
  resolves: rhbz#1469902

* Thu Jun 22 2017 Pino Toscano <ptoscano@redhat.com> - 1:1.36.3-6
- Rebase to libguestfs 1.36 in RHEL 7.4.
  resolves: rhbz#1359086
- v2v: always use names for libvirt pools
  resolves: rhbz#1141631
- v2v: correctly find GRUB in RHEL UEFI guests
- v2v: uninstall VMware tools packages from guests
  resolves: rhbz#1155150
- v2v: install RHEV-APT only when using -o rhev/-o vdsm
  resolves: rhbz#1161019
- New API: btrfs-filesystem-show
  resolves: rhbz#1164765
- p2v: always enable debugging when running virt-v2v
  resolves: rhbz#1167623
- libguestfs prefers virtio-pci on aarch64
  resolves: rhbz#1237250
- v2v: make sure to copy all the driver files on Windows
  resolves: rhbz#1255610
- Better tolerate corrupted Windows hivex; bump the hivex BuildRequires and
  Requires to >= 1.3.10-5.8.el7
  resolves: rhbz#1311890
- v2v: ignore all the environment variables for proxy when exporting from
  vCenter
  resolves: rhbz#1354507
- virt-sysprep can deal with full-LUKS encrypted guests
  resolves: rhbz#1362649
- All the tools have bash completion scripts.
  resolves: rhbz#1367738
- v2v: do not remove Processor and Intelppm nodes in Windows guests
  resolves: rhbz#1372668
- Fix SELinux relabelling in old RHEL 6 guests, by adjusting a broken
  regular expression in file_contexts file
  resolves: rhbz#1374232
- v2v: set all the properties on creation when exporting to Glance
  resolves: rhbz#1374405
- v2v: set hw_video_model when exporting to Glance
  resolves: rhbz#1374651
- v2v: fix OVA conversion as root using the libvirt backend
  resolves: rhbz#1375157
- Various improvements and fixes to the documentation
  resolves: rhbz#1377081
  resolves: rhbz#1390876
  resolves: rhbz#1398070
  resolves: rhbz#1425306
- v2v: support <listen type='socket'> and <listen type='none'>
  resolves: rhbz#1378022
- v2v: allow libvirt >= 2.1.0 for vCenter conversions
  resolves: rhbz#1379240
- p2v: enable mnemonics in the GUI
  resolves: rhbz#1379289
- Split virt-p2v, and the tools for it, in an own package: virt-p2v-maker
  resolves: rhbz#1382275
- Correctly parse mount options in btrfs entries in /etc/fstab.
  resolves: rhbz#1383517
- Read secrets from libvirt domains, when inspecting them
  resolves: rhbz#1392798
- v2v: add --vdsm-compat=1.1 flag for VDSM
  resolves: rhbz#1400205
- Fix inspection with UsrMove and /usr in a separate partition
  resolves: rhbz#1401474
- v2v: improve import compatibility with OVAs produced by AWS
  resolves: rhbz#1402301
- resize: allow URIs for the output disk
  resolves: rhbz#1404182
- Disable EDD when launching the appliance
  resolves: rhbz#1404287
- v2v: increase the memory allocated to the appliance
  resolves: rhbz#1418283
- p2v: switch from GTK+ 2 to GTK+ 3
- p2v: add dbus-devel as BuildRequires to disable suspension during the
  conversion
- libguestfs-java: bump the java-headless Require to >= 1.7.0, matching the
  Build-Require, and the generated bytecode
  resolves: rhbz#1364518
- Do not try to use/write to /var/cache/yum & /var/log/yum.log
- Bump ocaml-findlib-devel BuildRequires to >= 1.3.3-7.el7, because of
  RHBZ#1403897
- v2v: remove --dcpath & --dcPath from --help output too
  resolves: rhbz#1429430
- v2v: force VNC as display for -i disk, as SDL is not supported
  resolves: rhbz#1372671
- v2v, p2v: rename rhvm network to ovirtmgmt
  resolves: rhbz#1429491
- v2v: when exporting to local disk, check that UEFI firmware is installed
  before conversion
  resolves: rhbz#1429506
- dib: actually generate SHA256 checksums when using --checksum
  resolves: rhbz#1430184
- v2v: do not mention SUSE Xen hosts as supported
  resolves: rhbz#1430203
- v2v: depend on OVMF/AAVMF, for converting EFI guests
  resolves: rhbz#1429643
- v2v: use absolute path when using an OVA as backing file
  resolves: rhbz#1430680
- v2v: support Debian/Ubuntu guests
  resolves: rhbz#1387213
- sysprep: remove DHCP_HOSTNAME entries
  resolves: rhbz#1427529
- v2v: avoid repeated "run virt-v2v -v -x" message on error
  resolves: rhbz#1167623
- bash-completion: add script for virt-v2v-copy-to-local
  resolves: rhbz#1367738
- v2v: fix virtio block driver installation for Windows 10 and Windows 2016
  resolves: rhbz#1434737
- Replace the libosinfo dependency with osinfo-db, since we are only using
  the osinfo database.
- v2v: fix virtio driver installation for Windows 8 UEFI
  resolves: rhbz#1431579
- v2v: new 'vmx' import method
  resolves: rhbz#1441197
- v2v: properly identify Windows 2016 guests when exporting them to RHV-M
  resolves: rhbz#1447202
- Run pvresize in non-interactive mode
  resolves: rhbz#1460692
- resize: make sure the input disk is read-only
  resolves: rhbz#1463714
- Switch qemu-kvm-rhev dependency to qemu-kvm on aarch64
  resolves: rhbz#1463646

* Tue Aug 30 2016 Richard W.M. Jones <rjones@redhat.com> - 1:1.32.7-3
- Rebase to libguestfs 1.32 in RHEL 7.3
  resolves: rhbz#1218766
- The full tests are now run after the package has been built.
- New tool and subpackage: virt-dib (safe diskimage-builder replacement).
- New subpackage libguestfs-inspect-icons to reduce dependencies of main pkg
  (see https://bugzilla.redhat.com/1194158).
- New tool: virt-get-kernel.
- Depend on java-headless instead of full java.
- New tool: virt-v2v-copy-to-local.
- Disable virt-v2v subpackage on ppc64 etc
  resolves: rhbz#1287826
- v2v: Remove VirtualBox Additions correctly
  resolves: rhbz#1296606
- Add clearer warnings sections to all man pages
  resolves: rhbz#1293527
- v2v: Disable the --in-place option.
- v2v: Support conversion of Windows > 7
  resolves: rhbz#1190669
- Add code to verify tarball signatures.
- General performance improvements.
- v2v: Prevent duplicate -b, -n, -oa options
  resolves: rhbz#1326266
  resolves: rhbz#1325825
- v2v: Unquote UUID and LABEL in fstab (util-linux 1335671)
- v2v: Fix alignment issues in treeviews in conversion dialog
  resolves: rhbz#1340407
- p2v: spinner should be hidden when it stops spinning
  resolves: rhbz#1341564
- p2v: ethtool command is not supported on p2v client
  resolves: rhbz#1341608
- p2v: Add ifconfig command to ISO
  resolves: rhbz#1342447
- p2v: Warn if virt-p2v-make-disk used on a partition
  resolves: rhbz#1342337
- Build using OCaml with fix for CVE-2015-8869.
  resolves: rhbz#1343101
- customize: Add --uninstall option (upstream 1343375)
- p2v: Document permissions on id_rsa file
  resolves: rhbz#1343414
- p2v: Print full curl error message
  resolves: rhbz#1343423
- get-kernel: Fix --format auto
  resolves: rhbz#1341984
- v2v: Provide better <Origin/> information to RHEV-M
  resolves: rhbz#1342398
- customize: Give an error if --truncate-recursive path does not exist
  resolves: rhbz#1345809
- sysprep: Add --network option so that --install option can be used
  resolves: rhbz#1345813
- p2v: Print proper error if incorrect password is given
  resolves: rhbz#1227599
- p2v: Print ssh error if incorrect hostname is given
  resolves: rhbz#1167916
- p2v: Display progress of operation in non-GUI mode
  resolves: rhbz#1229386
- p2v: Add a dialog confirming the user really means to cancel
  resolves: rhbz#1340464
- p2v: log window should process colour escapes and backspaces
  resolves: rhbz#1314244
- v2v: Fix installation of virtio drivers with *.dll files
  resolves: rhbz#1311373
- p2v: Improve error message when ssh login to conversion server fails
  resolves: rhbz#1348900
- v2v: Remove --dcpath parameter from manual
  resolves: rhbz#1315237
- v2v: Fix conversion of guests with floppy drives
  resolves: rhbz#1309706
- p2v: Better error when sudo requires a password
  resolves: rhbz#1340809
- v2v: Refuse to convert if there is < 1GB free in temporary directory
  resolves: rhbz#1316479
- inspection: Get Windows drive letters for GPT disks
  resolves: rhbz#1349237
- p2v: Add disk utils and display serial number of disks
  resolves: rhbz#855058
- p2v: Fix timeout error when connecting to unresponsive ssh server
  resolves: rhbz#1350363
- Remove external dependency generator.  Use supermin RPM deps instead.
  related: rhbz#1309796
- p2v: Flush messages to the journal immediately
  resolves: rhbz#1229386
- customize: Fix --install on ppc64le
  resolves: rhbz#1264835
- lib: Fix finding icons in Windows 7 64 bit guests
  resolevs: rhbz#1352761
- v2v: Add virsh --quiet flag when running virt-v2v --quiet
  resolves: rhbz#1358142
- lib: Fix inspection of ISOs with latest libosinfo
  resolves: rhbz#1359652
- dib: Fix run_command exit handlers on failure
  resolves: rhbz#1362357
- dib: Rework run of extra-data.d hooks
  resolves: rhbz#1362354
- Miscellaneous fixes to man pages and --help output
  resolves: rhbz#1362668
- lib: Specify backing format for read-only files
  resolves: rhbz#1354335
- Fix --selinux-relabel option
  resolves: rhbz#1362669
- sparsify: Fix --in-place option with UEFI guest
  resolves: rhbz#1364347
- p2v: Use latest linux-firmware in ISO
  resolves: rhbz#1364419
- v2v: Fix guest name when using -i disk
  resolves: rhbz#1365005
- p2v: Fix GUI message.
- v2v: Make fstrim message clearer
  resolves: rhbz#1366456
- v2v: Fix conversion of UEFI guests when Secure Boot OVMF installed
  resolves: rhbz#1367615
- lib: Fix assert-fail if port is missing in libvirt XML
  resolves: rhbz#1370424

* Mon Sep 14 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.55
- Fix previous commit by applying the patch this time (1243493)

* Sun Sep 13 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.54
- v2v: Permit libguestfs-winsupport to be used by virt-win-reg and
  virt-inspector (1243493)

* Thu Sep 10 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.53
- v2v: Error if certain options appear twice on the command line (1261242)
- v2v: Add --dcpath parameter to allow dcPath to be overridden (1256823)
- v2v: Partially revert: Fix OVF XML to enable qxl display (1260590)
- v2v: Detect AVG Technologies as AV software (1261436)
  resolves: rhbz#1261281

* Tue Sep  8 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.52
- v2v: Warn if Group Policy or AV software may result in 7B boot failure
  (1260689)
- v2v: Fix OVF XML to enable qxl display
  resolves: rhbz#1260590

* Tue Sep  1 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.51
- v2v: Fix handling of extra slashes in dcPath calculation
  resolves: rhbz#1258342 rhbz#1256823
- v2v: Fix -oa preallocation option
  resolves: rhbz#1251909

* Sun Aug 30 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.50
- v2v:
  * When debugging, dump OVF to stderr.
  * Ignore missing kernels from grub
    resolves: rhbz#1230412
  * Calculate VMware dcPath correctly (1256823)
  * Map empty VMware network or bridge name to default (1257895)
- p2v:
  * Wait for network to come online before testing connection
    resolves: rhbz#1256222
- Fix tests to run correctly with libguestfs-winsupport 7.2.

* Wed Aug 05 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.49
- p2v: Closing incoming ports on the virt-p2v ISO
  resolves: rhbz#1248678

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.48
- v2v: Include lsof in base appliance
  resolves: rhbz#1246032

* Thu Jul 23 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.47
- v2v: Work around 'umount: /sysroot: target is busy'
  resolves: rhbz#1246032
- v2v: Permit libguestfs-winsupport to be used by virt-win-reg and
  virt-inspector
  resolves: rhbz#1243493

* Tue Jul  7 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.46
- v2v: Refuse to convert Windows > 7
  reverts: rhbz#1190669
- v2v: Depend directly on libguestfs-xfs
  resolves: rhbz#1240275
- v2v: Inclusion of libguestfs-winsupport in RHEL 7.2
  resolves: rhbz#1240274, rhbz#1240276

* Mon Jul  6 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.44
- v2v: Fix error message when grub.conf is malformed
  resolves: rhbz#1239053
- v2v: Various fixes to conversion of UEFI systems
  resolves: rhbz#1184690

* Thu Jul  2 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.43
- virt-sysprep: Don't delete /var/spool/at/.SEQ
  resolves: rhbz#1238579

* Wed Jul  1 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.42
- v2v: Fix installation of virtio drivers in Windows 2008 and 2008 R2
  resolves: rhbz#1237869
  related: rhbz#1234351

* Tue Jun 30 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.41
- v2v: Extend the timeout when converting from VMware
  resolves: rhbz#1146007
- v2v: Fix memory safety when freeing libxml2 objects.
- v2v: Add comment to OVF output if actual_size field is estimated.

* Thu Jun 25 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.40
- v2v: Disable support for Windows > 7.
  reverts: rhbz#1190669
- v2v: Add support for getting drivers from virtio-win ISO
  resolves: rhbz#1234351

* Tue Jun 16 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.39
- v2v: Depend on qemu-kvm instead of qemu-kvm-rhev (except on aarch64/power).
- v2v: Don't fail if one of the input disks is blank
  resolves: rhbz#1232192
- p2v: Fix parsing of p2v.memory parameter (1229262).

* Tue Jun 09 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.38
- p2v: Set conversion status when conversion is cancelled
  resolves: rhbz#1226794
- p2v: Fix kernel command line parsing
  resolves: rhbz#1229340
- p2v: In command line mode, power off machine after conversion
  resolves: rhbz#1229385
- Fix for rebased systemd in RHEL 7.2.

* Fri May 29 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.37
- ppc64le: Rebuild with fixed OCaml compiler
  resolves: rhbz#1224676, rhbz#1224675
- Fix virt-sparsify on qcow2 files when using qemu-kvm
  resolves: rhbz#1225467
- Remove some perl dependencies which are no longer actually used.
- Further attempts to fix qemu-kvm dependency on aarch64, ppc64le
  resolves: rhbz#1177910

* Tue May 19 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.36
- p2v: Fix network in virt-p2v appliance
  resolves: rhbz#1222975
- p2v: Display network card MAC and vendor in conversion dialog (855059).
- p2v: More fixes to Add Network Connection dialog
  related: rhbz#1167921
- virt-builder: Fix --selinux-relabel flag on cross-arch builds
  resolves: rhbz#1222993

* Tue May 12 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.35
- Further attempts to fix qemu-kvm dependency on aarch64, ppc64, ppc64le
  resolves: rhbz#1177910
- v2v: Fix memory leak in earlier fix for bug 889082
  resolves: rhbz#889082

* Mon May 11 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.33
- p2v: Add restrictions for vCPUs and memory in client
  resolves: rhbz#823758
- v2v: Check if guest with same name already exists in libvirt
  resolves: rhbz#889082
- p2v: Add Network Connection dialog
  resolves: rhbz#1167921
- v2v: Fix list of operating system variants passed to RHEV
  resolves: rhbz#1219857, rhbz#1213324, rhbz#1213691
- ppc64: Remove part of temporary workaround
  related: rhbz#1177910

* Thu Apr 30 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.32
- v2v: Support conversion of EFI guests
  resolves: rhbz#1184690

* Tue Apr 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.31
- v2v: Keep listen address for VNC (updated fix)
  resolves: rhbz#1174073

* Fri Apr 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.29
- v2v: Convert sound card of guests
  resolves: rhbz#1176493

* Mon Apr 20 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.28
- Remove 'ssh:' URLs from documentation
  resolves: rhbz#1212677
- libguestfs-tools-c 'provides' guestfish
  (NB: will be removed in RHEL 8, use 'Requires: /usr/bin/guestfish' instead)
  resolves: rhbz#1212002
- v2v: Fix: warning: unknown guest operating system: windows when converting
  to RHEV targets
  resolves: rhbz#1213324
- v2v: Fix: warning: fstrim: fstrim: /sysroot/: FITRIM ioctl failed
  resolves: rhbz#1168144

* Thu Apr 16 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.26
- v2v: Keep listen address for VNC
  resolves: rhbz#1174073
- v2v: Preserve display port configuration when converting guests
- v2v: Support conversion of guests with disk type volume
  resolves: rhbz#1146832
- v2v: Initial support for gzipped ova imports.
  related: rhbz#1186800

* Mon Apr 13 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.25
- Enable rbd (Ceph) support.
- rbd: Implement drive secrets
  resolves: rhbz#1159030
- virt-resize: Fix 'no space left on device' when resizing extended partition
  resolves: rhbz#1172660
- v2v: Update RHEV-APT to latest
  resolves: rhbz#1186850
- v2v: Update rhsrvany.exe to latest
  resolves: rhbz#1187231
- Drop dependency on selinux-policy
  resolves: rhbz#1196705
- Depend on fuse
  resolves: rhbz#1201507
- v2v: Allow configurable location for virtio drivers [1209225]
- Various fixes for setting long labels
  resolves: rhbz#1164708
- Fix mknod APIs not stripping permission bits from mode
  resolves: rhbz#1182463
- Allow LIBGUESTFS_TRACE=0, LIBGUESTFS_DEBUG=true etc
  resolves: rhbz#1175196
- Fix typo in description of ping-daemon API
  resolves: rhbz#1175676
- Disable gfs2 subpackage on !x86-64 [1211333]

* Mon Apr 13 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.24
- Open RHEL 7.2 branch.
- Import brew-overrides.sh into dist-git.
- copy-patches.sh: Relax arbitrary requirement to split patches into
  backports and RHEL 7 specific patches.
- v2v: Add --vdsm-ovf-output option
  resolves: rhbz#1176598
- v2v: Fix -o vdsm to work with multiple data domains
  resolves: rhbz#1176591
- v2v: Support conversions of Windows >= 8
  resolves: rhbz#1190669
- v2v: Document that vCenter >= 5.0 is required
  resolves: rhbz#1174200

* Thu Feb  5 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.23
- Fix virt-resize (and hence virt-builder --size) on guests using
  UEFI bootloaders.

* Mon Jan 26 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.22
- aarch64: Increase default appliance memory size.
- Make gfs2-utils conditional on x86, as it will not be supported on ARM.
- inspection: aarch64: Backport fix for inspection of EFI guests.

* Fri Jan 23 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.20
- aarch64: Depend on AAVMF package.

* Thu Jan 22 2015 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.19
- aarch64: Add support for AAVMF
  resolves: rhbz#1184504

* Mon Dec 15 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.18
- v2v: Copy graphics password from source to destination
  resolves: rhbz#1174123
- p2v: Allow ports to be reused and specify source port number
  resolves: rhbz#1167774
- p2v: Fix "Conversion was successful" dialog appearing on failure
  resolves: rhbz#1167601

* Wed Dec 10 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.17
- v2v: Fix modifications to default kernel for legacy grub.
  resolves: rhbz#1170073

* Mon Dec  8 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.16
- p2v: Wait for qemu-nbd to start up before starting virt-v2v
  resolves: rhbz#1167774

* Fri Dec  5 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.15
- v2v: Document Windows Group Policy problems causing 0x0000007B BSOD
  resolves: rhbz#1161333
- v2v: Fix conversion of RHEL 3 guests
  resolves: rhbz#1171130
- v2v: Fix conversion of RHEL 4 guests that use epoch
  resolves: rhbz#1170685
- v2v: Favour non-debug kernels over debug kernels
  resolves: rhbz#1170073
- p2v: Fix kickstart for virt-p2v
  resolves: rhbz#1168632
- Fixed some documentation mistakes.

* Thu Nov 27 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.14
- p2v: Add Reboot button to the GUI
  resolves: rhbz#1165564
- p2v: Fixes to 'Cancel Conversion' button
  resolves: rhbz#1165569
- v2v: -i ova: Remove incorrect warning for disks with no parent controller
  resolves: rhbz#1167302
- resize: Capture errors from ntfsresize
  resolves: rhbz#1166618

* Thu Nov 20 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.13
- v2v: Fix device mapping of /boot/grub2/device.map
  resolves: rhbz#1165975
- v2v: Fix 'no volume groups found' because of old LVM cache file
  resolves: rhbz#1164853

* Tue Nov 18 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.12
- v2v: Fix device remapping for RHEL guests
  resolves: rhbz#1151725

* Mon Nov 17 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.11
- Fix inspect-get-icon on RHEL 7 guests
  resolves: rhbz#1164619
- Fix description of set-append (append) and get-append commands
  resolves: rhbz#1164732
- Fix small typo in release notes.
  resolves: rhbz#1164697

* Thu Nov 13 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.10
- v2v: -o glance: Fix metadata for disk type and NIC
  resolves: rhbz#1161575
- check xfs label lengths
  resolves: rhbz#1162966

* Thu Nov  6 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.9
- v2v: Fix kernel detection when multiple kernels are installed
  resolves: rhbz#1161250

* Thu Nov  6 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.8
- p2v: Explain in the man page why the virt-p2v ISO is used.
- p2v: Ensure we are using virt-v2v >= 1.28.
- v2v: Add bounds check to Xml.xpathobj_node function.
- v2v: Ensure --bridge and --network args are documented correctly in --help
- v2v: -i libvirt vcenter: Change 'esx:' to 'vcenter:' in errors/warnings.
- v2v: Ignore small filesystems when checking for sufficient free space.
- v2v: Document minimum free filesystem space requirements.
  related: rhbz#1021149
- customize: firstboot: make sure to run Linux scripts only once
  resolves: rhbz#1160043
- customize: firstboot: fix Linux log output
  resolves: rhbz#1160199

* Mon Nov  3 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.7
- guestfish: Fix tab completion of filenames on XFS and elsewhere
  resolves: rhbz#1153844
- v2v: Ensure <features/> are set in output so ACPI etc works
  resolves: rhbz#1159258
- v2v: Add --password-file parameter
  resolves: rhbz#1158526

* Wed Oct 29 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.6
- p2v: Add firmware and usb-storage module to virt-p2v-make-disk.
  resolves: rhbz#1157691

* Fri Oct 24 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.5
- virt-sysprep & virt-customize: Fix password setting problems
  resolves: rhbz#1141626, rhbz#1147065
- virt-inspector: document that -a option can take a URI
  resolves: rhbz#1156301
- bash-completion: use symlinks instead of copying files
  resolves: rhbz#1156298

* Thu Oct 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.4
- v2v: Fix handling of relative paths in -i ova
  resolves: rhbz#1155121
- v2v: disable uninstallation of VMware drivers on Linux for RHEL 7.1
  resolves: rhbz#1155610

* Wed Oct 22 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.3
- v2v: Fix conversion from NBD sources
  resolves: rhbz#1153589
- v2v: BR zip and unzip, and require unzip, for ZIP support in -i ova mode
  related: rhbz#1152998

* Mon Oct 20 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.2
- v2v: Add support for ZIP and *.vmdk.gz to -i ova
  resolves: rhbz#1152998
- virt-ls: Add a field for directory files when using --csv option
  resolves: rhbz#1151900
- v2v: Mitigate hangs when run against a very slow VMware vCenter server
  resolves: rhbz#1153589
- cat, diff: Avoid double slashes in paths
  resolves: rhbz#1151910

* Sat Oct 18 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.28.1-1.1
- Final rebase to stable libguestfs branch 1.28.
  resolves: rhbz#1021149
- Drop dist tag for BuildRequires, so it builds on ppc64le.
  resolves: rhbz#1149640
- Make sure we require the latest libvirt, so virt-v2v can access ESX.
- Fix guestfish colour prompts when using white-on-black terminal
  resolves: rhbz#1144201
- Disable libguestfs UML backend mode
  resolves: rhbz#1144197
- Enable ppc64, ppc64le and aarch64.
  On ppc64 we currently have to disable build-time testing of qemu.
  resolves: rhbz#1125575
- Remove unnecessary BR for libnl3 in RHEL < 7.1.
- Integrate changes from Rawhide.
- Add workaround for buggy libvirt 1.2.8.
- Move virt-v2v into a separate subpackage and make it depend on qemu-kvm-rhev.
- Add rhsrvany and RHEV Application Provisioning Tool to virt-v2v.
- Change Fedora -> RHEL in description.
- Disable some more protocol tests.
- Enable tests.
- Enable guestfish colour prompts.
- Add new tool virt-log.
- Enabling bash-completions subpackage means we need to BR bash-completion.
- Package libguestfs 1.27/1.28 for RHEL 7.1.
- Enable bash-completion.

* Mon Mar  3 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-22
- Fix Ruby bindings
  resolves: rhbz#1072079

* Wed Feb 12 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-21
- Fix segfault in guestfs_list_filesystems when presented with a
  corrupt btrfs filesystem
  resolves: rhbz#1064008

* Tue Feb 11 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-20
- Valid GUIDs when used as parameter to part-set-gpt-type
  resolves: rhbz#1008417

* Wed Feb 05 2014 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-19
- Fix placement of *.py[co] files
  resolves: rhbz#1061155
- Remove bogus license file from daemon
  resolves: rhbz#1061160
- Prevent virt-sparsify from overwriting block or char devices
  resolves: rhbz#1056556
- mount-local should give a clearer error if root is not mounted
  resolves: rhbz#1057492

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:1.22.6-18
- Mass rebuild 2013-12-27

* Thu Dec 05 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-17
- Rebuild for updated procps SONAME.
  resolves: rhbz#1037795

* Wed Nov 20 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-16
- Allow virt-win-reg command to work with URIs
  resolves: rhbz#912193

* Thu Oct 31 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-15
- Add libguestfs-tools.conf(5) man page
  resolves: rhbz#1019891
- Drop PHP bindings
  resolves: rhbz#1020021
- Disable Haskell & Erlang (in case someone has these dependencies
  installed and tries to rebuild the package).

* Wed Oct 16 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-12
- Backport: "daemon: Fix xfs_info parser because of new format."
  which is required to fix libguestfs tests.
  related: rhbz#1019503

* Wed Oct 16 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-11
- Further fixes for kvmclock
  resolves: rhbz#998109
- Document that blockdev-setbsz is deprecated and should not be used
  resolves: rhbz#1016465

* Wed Oct 16 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-10
- Fix CVE-2013-4419: insecure temporary directory handling for
  guestfish's network socket
  resolves: rhbz#1019503

* Thu Sep 26 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-9
- Use 'host-passthrough' instead of 'host-model' (RHBZ#1011922)
- Fix mount-loop failed to setup loop device: No such file or directory
  resolves: rhbz#1011907

* Fri Sep 13 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-8
- Backport 'cachemode' property of 'add_drive'
  resolves: rhbz#1003291
- Improve error reporting from aug_init
  related: rhbz# 1003685

* Thu Aug 29 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-5
- Various fixes to tar-out 'excludes'
  resolves: rhbz#1001875
- Document use of glob + rsync-out
  resolves: rhbz#1001876
- Document mke2fs blockscount
  resolves: rhbz#1002032
- Fix virt-format MBR partition type byte, add --label option to
  virt-format and virt-make-fs, and allow labels to be set on DOS filesystems
  resolves: rhbz#1000428
- Fix javadoc location to use _javadocdir macro.
- Call ldconfig in java post and postun scripts.
- Do not explicitly depend on perl-devel.
- Compress the ChangeLog and *.xml files in devel package.
- Create new subpackage gobject-doc for the huge HTML documentation.
- Make javadoc, gobject-doc, bash-completion, man-pages-*, tools packages
  'noarch'.
- Enable gzip-compressed appliance.
- Note this requires supermin >= 4.1.4.

* Tue Aug 27 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.6-4
- New upstream stable version 1.22.6.
  resolves: rhbz#995712, rhbz#998750, rhbz#998485
- Backport set-UUID API and related
  resolves: rhbz#995176
- Enable kvmclock
  resolves: rhbz#998109
- Add upstream APIs guestfs_add_drive_scratch, guestfs_remount.

* Tue Jul 30 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.5-3
- Backport support for virt-sysprep -a URI option
  resolves: rhbz#968785

* Mon Jul 29 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.5-2
- New upstream stable version 1.22.5.
- Fix virt-sysprep --firstboot option
  resolves: rhbz#988862
- Disable unsupported remote drives
  resolves: rhbz#962113
- cap-get-file returns empty string instead of error if no capabilities
  resolves: rhbz#989356

* Fri Jul 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.4-2
- New upstream stable version 1.22.4.
- Move virt-sysprep to libguestfs-tools-c package
  resolves: rhbz#975573
- Remove 9p APIs from RHEL
  resolves: rhbz#921710
- Reenable swapon test
  resolves: rhbz#911674
- Reenable file architecture test
  resolves: rhbz#911678
- Fix mkfs blocksize option when using xfs
  resolves: rhbz#976250
- Fix double-free when kernel link fails during launch
  resolves: rhbz#983691
- Fix disk-format "JSON parse error" when target file does not exist
  resolves: rhbz#980338
- Fix documentation for acl-set-file
  resolves: rhbz#985856
- libguestfs-devel should depend on full ENVR of libguestfs-tools-c.
- Require /usr/bin/vi instead of /bin/vi for UsrMove.

* Mon Jun  3 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.22.2-1
- New upstream version 1.22.2.
- Do not need to remove guestfsd man page, since libguestfs no longer
  installs it.

* Mon May 20 2013 Daniel Mach <dmach@redhat.com> - 1:1.21.33-1.1.el7
- Rebuild for cyrus-sasl

* Mon Apr 29 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.33-1.el7
- New upstream version 1.21.33.
- Rebuild for renamed Kerberos library.
  resolves: rhbz#957616
- Skip gnulib tests which fail.
- Skip NBD test since there is no NBD in RHEL.

* Wed Apr 17 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.21.31-1.el7.1
- Rebase RHEL 7 onto libguestfs 1.21.
- Update spec file from Rawhide.

* Tue Apr  9 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.5-4
- In RHEL 7, 'ruby(abi)' has been replaced by 'ruby(release)'
  and the version of the ruby ABI/release is now 2.0.0.

* Fri Apr  5 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.5-3
- Remove man pages of deprecated programs.

* Tue Apr  2 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.5-2
- Remove deprecated programs virt-tar, virt-list-filesystems and
  virt-list-partitions from RHEL 7.

* Sun Mar 31 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.5-1
- New upstream version 1.20.5.
- Remove ruby vendor patch.
- Set INSTALLDIRS=vendor on both make and make install rules.

* Tue Mar  5 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.3-1
- New upstream version 1.20.3.

* Fri Feb 15 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.2-1
- New upstream version 1.20.2.
- Synchronize list of tests to be skipped with local list.
- Use openjdk instead of java (GCJ).
- Add BRs: libcap.
- Ship the gobject pkgconfig file.

* Mon Feb 11 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.1-7
- 'febootstrap' has been renamed 'supermin'.
  resolves: rhbz#909573

* Sat Jan 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.1-6
- Add explicit BR on seabios-bin to work around RHBZ#901542.

* Fri Jan 18 2013 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.1-5
- Bump and rebuild.

* Fri Dec 21 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.1-4
- Go over all non-upstream patches from RHEL 6 and add appropriate ones
  to RHEL 7:
  * Emphasize libguestfs-winsupport.
  * Remove libguestfs-live ('unix' attach-method).
  * Exclude iptables.
  * Ignore /etc/release file if /etc/redhat-release file exists.
  resolves: rhbz#889536, rhbz#889537, rhbz#889538, rhbz#873219
- Do not number patches.

* Thu Dec 20 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.1-3
- New upstream version 1.20.1.

* Tue Dec 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.0-5
- Remove RHEL-conditionals, since I have branched spec file for RHEL 7.
- Add BR gdisk.
- Change to using git to manage patches.
- Add copy-patches.sh script.
- Disable libguestfs live (RHEL only).
- "Fedora" -> "RHEL" in replacement README file.
- "fedora" -> "rhel" in version extra field.

* Mon Dec 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.0-2
- Use 'make check -k' so we get to see all test failures at once.
- For RHEL 7:
  * Do not depend on perl(Expect) (only needed to test virt-rescue).
  * Depend on /usr/bin/qemu-img instead of qemu-img package, since the
    package name (but not the binary) is different in RHEL 7.
  * Add workaround for libvirt/KVM bug RHBZ#878406.
  * Do not depend on libvirt-daemon-qemu.
  * Do not depend on libldm (not yet in RHEL 7: RHBZ#887894).

* Thu Dec 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.20.0-1
- New upstream version 1.20.0.
- New source URL for this branch.
- Reconcile upstream packagelist, BRs and Requires lists.
- Requires newest SELinux policy so that SVirt works.
- Fix patch 2.  Actually, remove and replace with a small script.

* Sat Dec 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.66-1
- New upstream version 1.19.66.

* Fri Nov 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.65-2
- Add a hack to work around glibc header bug <rpc/svc.h>.

* Thu Nov 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.65-1
- New upstream version 1.19.65.

* Sat Nov 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.64-1
- New upstream version 1.19.64.

* Sat Nov 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.63-3
- Re-add: Non-upstream patch to add the noapic flag on the kernel
  command line on i386 only.  This works around a bug in 32-bit qemu,
  https://bugzilla.redhat.com/show_bug.cgi?id=857026

* Fri Nov 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.63-2
- Remove non-upstream patch designed to work around
  https://bugzilla.redhat.com/show_bug.cgi?id=857026
  to see if this has been fixed.
- Re-enable tests on i686 to see if
  https://bugzilla.redhat.com/show_bug.cgi?id=870042
  has been fixed.

* Fri Nov 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.63-1
- New upstream version 1.19.63.

* Tue Nov 20 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.62-1
- New upstream version 1.19.62.

* Mon Nov 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.61-1
- New upstream version 1.19.61.

* Sat Nov 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.60-2
- Remove Lua bogus libtool *.la file.

* Sat Nov 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.60-1
- New upstream version 1.19.60.

* Tue Nov 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.59-1
- New upstream version 1.19.59.

* Sat Nov 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.58-1
- New upstream version 1.19.58.

* Thu Nov 08 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.57-1
- New upstream version 1.19.57.

* Tue Nov 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.56-3
- Add upstream patch to disable virt-format test, and disable
  it because wipefs utility is broken.

* Sat Nov 03 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.56-2
- Add upstream patch to fix wipefs test.

* Fri Nov 02 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.56-1
- New upstream version 1.19.56.

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.55-1
- New upstream version 1.19.55.

* Mon Oct 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.54-1
- New upstream version 1.19.54.

* Wed Oct 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.53-3
- Disable tests on ix86 because qemu/kernel is broken (RHBZ#870042).

* Wed Oct 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.53-2
- Add upstream patch to fix guestfish tests.

* Fri Oct 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.53-1
- New upstream version 1.19.53.

* Sun Oct 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.52-1
- New upstream version 1.19.52.

* Thu Oct 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.51-1
- New upstream version 1.19.51.

* Thu Oct 11 2012 Petr Pisar <ppisar@redhat.com> - 1:1.19.50-2
- Correct perl dependencies

* Thu Oct 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.50-1
- New upstream version 1.19.50.

* Wed Oct 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.49-3
- Upstream patch to workaround btrfs problems with kernel 3.7.0.

* Tue Oct 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.49-2
- Install all libguestfs-live-service udev rules into /usr/lib/udev/rules.d.

* Tue Oct 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.49-1
- New upstream version 1.19.49.

* Sun Oct 07 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.48-1
- New upstream version 1.19.48.

* Mon Oct 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.46-1
- New upstream version 1.19.46.

* Wed Sep 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.45-1
- New upstream version 1.19.45.

* Tue Sep 25 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.44-2
- Enable sVirt (NB: requires libvirt >= 0.10.2-3, selinux-policy >= 3.11.1-23).
- Add upstream patch to label the custom $TMPDIR used in test-launch-race.

* Mon Sep 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.44-1
- New upstream version 1.19.44.

* Sat Sep 22 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.43-1
- New upstream version 1.19.43.

* Tue Sep 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.42-2
- New upstream version 1.19.42.
- Rebase sVirt (disable) patch.

* Sun Sep 16 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.41-1
- New upstream version 1.19.41.

* Fri Sep 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.40-3
- Add (non-upstream) patch to add the noapic flag on the kernel
  command line on i386 only.  This works around a bug in 32-bit qemu.

* Wed Sep 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.40-2
- Enable tests because RHBZ#853408 has been fixed in qemu-1.2.0-3.fc18.

* Wed Sep 05 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.40-1
- New upstream version 1.19.40.

* Tue Sep 04 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.39-1
- New upstream version 1.19.39.

* Mon Sep 03 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.38-1
- New upstream version 1.19.38.

* Fri Aug 31 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.37-1
- New upstream version 1.19.37.

* Thu Aug 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.36-2
- New upstream version 1.19.36.
- Require libvirt-daemon-qemu (for libvirt attach method).

* Thu Aug 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.36-1
- Switch to using libvirt as the backend for running the appliance.  See:
  https://www.redhat.com/archives/libguestfs/2012-August/msg00070.html
- Use configure RPM macro instead of ./configure.

* Wed Aug 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.35-1
- New upstream version 1.19.35.

* Wed Aug 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.34-2
- Add upstream patch to fix Perl bindtests on 32 bit.

* Tue Aug 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.34-1
- New upstream version 1.19.34.

* Tue Aug 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.33-1
- New upstream version 1.19.33.

* Mon Aug 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.33-3
- Fix Perl examples directory so we only include the examples.
- Add Java examples to java-devel RPM.

* Tue Aug 21 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.33-2
- New upstream version 1.19.33.
- Reenable tests.

* Sat Aug 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.32-1
- New upstream version 1.19.32.

* Wed Aug 15 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.31-1
- New upstream version 1.19.31.

* Tue Aug 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.30-1
- New upstream version 1.19.30.

* Sat Aug 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.29-2
- New upstream version 1.19.29.
- Remove RELEASE NOTES from doc section, and add equivalent man page.

* Fri Aug 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.28-4
- Bump and rebuild.

* Thu Aug 02 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.28-3
- New upstream version 1.19.28.
- Update libguestfs-find-requires to generate ordinary lib dependencies.

* Wed Aug  1 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.27-2
- Disable tests because of RHBZ#844485.

* Mon Jul 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.27-1
- New upstream version 1.19.27.

* Thu Jul 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.26-2
- Remove old RPM-isms like defattr.
- Add upstream patches to fix use of 'run' script in tests.

* Thu Jul 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.26-1
- New upstream version 1.19.26.

* Tue Jul 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.25-1
- New upstream version 1.19.25.

* Mon Jul 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.24-1
- New upstream version 1.19.24.

* Sun Jul 22 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.23-1
- New upstream version 1.19.23.

* Thu Jul 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.22-2
- Add upstream patch to skip mount-local test if /dev/fuse not writable.

* Thu Jul 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.22-1
- New upstream version 1.19.22.

* Wed Jul 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.21-1
- New upstream version 1.19.21.

* Tue Jul 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.20-1
- New upstream version 1.19.20.

* Mon Jul 16 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.19-1
- New upstream version 1.19.19.

* Tue Jul 10 2012 Petr Pisar <ppisar@redhat.com> - 1:1.19.18-2
- Perl 5.16 rebuild

* Mon Jul 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.18-1
- New upstream version 1.19.18.

* Fri Jul 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.17-1
- New upstream version 1.19.17.

* Wed Jul 04 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.16-1
- New upstream version 1.19.16.

* Fri Jun 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.15-1
- New upstream version 1.19.15.

* Thu Jun 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.14-1
- New upstream version 1.19.14.

* Wed Jun 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.13-2
- New upstream version 1.19.13.
- Add upstream patch to fix GObject/Javascript tests.

* Tue Jun 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.12-1
- New upstream version 1.19.12.

* Mon Jun 25 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.11-1
- New upstream version 1.19.11.

* Fri Jun 22 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.10-1
- New upstream version 1.19.10.

* Mon Jun 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.9-1
- New upstream version 1.19.9.

* Thu Jun 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.8-1
- New upstream version 1.19.8.

* Thu Jun 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.7-2
- New upstream version 1.19.7.
- Require febotstrap >= 3.17.

* Tue Jun 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.6-2
- Require febootstrap >= 3.16.

* Tue Jun 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.6-1
- New upstream version 1.19.6.

* Tue Jun 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.6-1
- New upstream version 1.19.6.
- This version defaults to using virtio-scsi.
- Requires qemu >= 1.0.
- Requires febootstrap >= 3.15.

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 1:1.19.5-2
- Perl 5.16 rebuild

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.5-1
- New upstream version 1.19.5.

* Thu Jun 07 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.4-1
- New upstream version 1.19.4.

* Fri Jun 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.3-2
- New upstream version 1.19.3.
- Remove patches which are now upstream.

* Tue May 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.2-3
- Remove obsolete list of bugs in make check rule.
- Remove some obsolete test workarounds.
- Disable i386 tests (because of RHBZ#825944).

* Mon May 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.2-2
- Include patches to fix udev.

* Mon May 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.2-1
- New upstream version 1.19.2.

* Sat May 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.1-1
- New upstream version 1.19.1.

* Mon May 21 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.19.0-1
- New upstream version 1.19.0.

* Thu May 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.43-1
- New upstream version 1.17.43.

* Thu May 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.42-4
- On RHEL 7 only, remove reiserfs-utils, zerofree.

* Thu May 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.42-3
- On RHEL 7 only, remove nilfs-utils.

* Tue May 15 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.42-2
- Bundled gnulib (RHBZ#821767).

* Mon May 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.42-1
- New upstream version 1.17.42.

* Fri May 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.41-1
- New upstream version 1.17.41.

* Tue May 08 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.40-1
- New upstream version 1.17.40.

* Tue May  8 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.39-3
- Disable hfsplus-tools on RHEL 7.

* Thu May 03 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.39-2
- BR perl-XML-XPath to run the new XML test.

* Thu May 03 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.39-1
- New upstream version 1.17.39.

* Wed May 02 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.38-3
- Remove explicit runtime deps for old virt-sysprep.
- Add explicit runtime dep on fuse (RHBZ#767852, thanks Pádraig Brady).
- Remove explicit versioned dep on glibc.

* Tue May  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1:1.17.38-2
- Update supported filesystems for ARM

* Tue May 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.38-1
- New upstream version 1.17.38.

* Tue May 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.37-2
- Add guestfs-faq(1) (FAQ is now a man page).

* Tue May 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.37-1
- New upstream version 1.17.37.

* Fri Apr 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.36-2
- Add upstream patch to fix installation of gobject headers.

* Thu Apr 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.36-1
- New upstream version 1.17.36.

* Thu Apr 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.35-1
- New upstream version 1.17.35.

* Tue Apr 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.34-1
- New upstream version 1.17.34.

* Mon Apr 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.33-1
- New upstream version 1.17.33.

* Tue Apr 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.32-1
- New upstream version 1.17.32.

* Mon Apr 16 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.31-1
- New upstream version 1.17.31.

* Fri Apr 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.30-1
- New upstream version 1.17.30.

* Thu Apr 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.29-1
- New upstream version 1.17.29.

* Thu Apr 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.28-2
- Enable ruby 1.9 patch in RHEL 7 (RHBZ#812139).

* Thu Apr 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.28-1
- New upstream version 1.17.28.

* Wed Apr 11 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.27-2
- Add guestfs-performance(1) manual page.

* Tue Apr 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.27-1
- New upstream version 1.17.27.

* Tue Apr 03 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.26-1
- New upstream version 1.17.26.

* Mon Apr 02 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.25-1
- New upstream version 1.17.25.

* Sun Apr 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.24-1
- New upstream version 1.17.24.

* Sun Apr 01 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.23-1
- New upstream version 1.17.23.

* Thu Mar 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.22-2
- Include all gobject header files.
- Include gtk-doc, and depend on the gtk-doc package at runtime.

* Thu Mar 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.22-1
- New upstream version 1.17.22.

* Thu Mar 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.21-2
- Bump and rebuild.

* Wed Mar 21 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.21-1
- New upstream version 1.17.21.

* Mon Mar 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.20-3
- Reenable LUKS, since RHBZ#804345 is reported to be fixed.

* Sun Mar 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.20-2
- Disable LUKS tests because LUKS is broken in Rawhide (RHBZ#804345).

* Sat Mar 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.20-1
- New upstream version 1.17.20.

* Sat Mar 17 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.19-2
- Add libguestfs-make-fixed-appliance (with man page).

* Fri Mar 16 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.19-1
- New upstream version 1.17.19.

* Thu Mar 15 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.18-1
- New upstream version 1.17.18.

* Wed Mar 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.17-1
- New upstream version 1.17.17.

* Wed Mar 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.16-2
- Bump and rebuild.

* Tue Mar 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.16-1
- New upstream version 1.17.16.

* Mon Mar 12 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.15-1
- New upstream version 1.17.15.

* Fri Mar 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.14-1
- New upstream version 1.17.14.

* Thu Mar 08 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.13-1
- New upstream version 1.17.13.

* Thu Mar 08 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.12-2
- Enable Japanese man pages, since these are in a better state upstream.

* Wed Mar 07 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.12-1
- New upstream version 1.17.12.

* Wed Mar 07 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.11-2
- Require netpbm-progs, icoutils.  These are needed for icon generation
  during inspection, but were not being pulled in before.

* Mon Mar 05 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.11-1
- New upstream version 1.17.11.

* Sat Mar 03 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.10-2
- New upstream version 1.17.10.
- Rebase Ruby patch against new libguestfs.

* Wed Feb 29 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.9-1
- New upstream version 1.17.9.

* Wed Feb 15 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.8-1
- New upstream version 1.17.8.

* Mon Feb 13 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.7-1
- New upstream version 1.17.7.

* Fri Feb 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.6-1
- +BR ruby-irb.
- Make virtio unconditional.  It's been a very long time since disabling
  virtio was a good idea.
- Disable some packages not available in RHEL 7.
- New upstream version 1.17.6.

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1:1.17.5-3
- Rebuild against PCRE 8.30

* Thu Feb  9 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.5-2
- Rebuild with ruby(abi) = 1.9.1.

* Wed Feb  8 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.5-1
- New upstream version 1.17.5.
- Remove usrmove workaround patch, now upstream.

* Wed Feb  8 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.4-8
- Further Ruby 1.9 changes.

* Tue Feb 07 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.4-7
- Bump and rebuild for Ruby update.

* Mon Feb  6 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.4-6
- Add workaround for usrmove in Fedora.

* Wed Feb  1 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.4-1
- New upstream version 1.17.4.
- Remove patch now upstream.

* Sat Jan 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.3-2
- New upstream version 1.17.3.
- Remove patch now upstream.
- Add upstream patch to fix OCaml bytecode compilation.

* Fri Jan 27 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.2-3
- Upstream patch to work with udev >= 176.

* Thu Jan 26 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.2-2
- New upstream version 1.17.2.
- Use libdb-utils instead of old db4-utils.
- net-tools is no longer used; replaced by iproute (RHBZ#784647).
- Try re-enabling tests on i686.

* Tue Jan 24 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.17.1-1
- New upstream version 1.17.1.

* Mon Jan 23 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.16.0-1
- New upstream version 1.16.0.
- Remove patches which are now upstream.
- GObject: Move *.typelib file to base gobject package.

* Sun Jan 22 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.19-1
- New upstream version 1.15.19.
- +BR psmisc for the appliance.
- Includes GObject bindings in libguestfs-gobject and
  libguestfs-gobject-devel subpackages.
- Include upstream patches for PHP 5.4.

* Thu Jan 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.18-1
- New upstream version 1.15.18.

* Wed Jan 18 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.17-1
- New upstream version 1.15.17.
- New tool: virt-format.

* Tue Jan 10 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.16-1
- New upstream version 1.15.16.

* Sun Jan  8 2012 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.15-2
- New upstream version 1.15.15.
- Updated gnulib fixes builds with gcc 4.7.
- Rebuild for OCaml 3.12.1.
- Add explicit BR perl-hivex, required for various Perl virt tools.

* Fri Dec 23 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.14-1
- New upstream version 1.15.14.
- Remove three patches, now upstream.

* Thu Dec 22 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.13-4
- New upstream version 1.15.13.
- Fixes Security: Mitigate possible privilege escalation via SG_IO ioctl
  (CVE-2011-4127, RHBZ#757071).
- Add three upstream patches to fix 'make check'.

* Thu Dec 22 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.12-1
- New upstream version 1.15.12.

* Fri Dec  9 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.11-1
- New upstream version 1.15.11.

* Tue Dec  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.10-1
- New upstream version 1.15.10.
- Remove patch, now upstream.

* Sat Dec  3 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.9-2
- New upstream version 1.15.9.
- Add upstream patch to fix Augeas library detection.
- Appliance explicitly requires libxml2 (because Augeas >= 0.10 requires it),
  although it was implicitly included already.

* Tue Nov 29 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.8-1
- New upstream version 1.15.8.

* Tue Nov 29 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.7-1
- New upstream version 1.15.7.

* Thu Nov 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.6-1
- New upstream version 1.15.6.

* Mon Nov 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.5-1
- New upstream version 1.15.5.
- Add guestfs-testing(1) man page.

* Thu Nov 17 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.4-2
- New upstream version 1.15.4.
- Remove patch which is now upstream.
- libguestfs_jni.a is no longer built.

* Fri Nov 11 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.3-3
- Add upstream patch to disable part of virt-df test.

* Thu Nov 10 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.3-1
- New upstream version 1.15.3.
- Fix list of BuildRequires so they precisely match the appliance.

* Thu Nov  3 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.2-1
- New upstream version 1.15.2.
- ocaml-pcre is no longer required for virt-resize.
- xmlstarlet is no longer required for virt-sysprep.

* Tue Nov  1 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.1-1
- New upstream version 1.15.1.

* Fri Oct 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.15.0-1
- Stable branch 1.14.0 was released.  This is the new development
  branch version 1.15.0.

* Wed Oct 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.26-1
- New upstream version 1.13.26.

* Wed Oct 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.25-1
- New upstream version 1.13.25.

* Mon Oct 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.24-1
- New upstream version 1.13.24.
- This version includes upstream workarounds for broken qemu, so both
  non-upstream patches have now been removed from Fedora.

* Fri Oct 21 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.13.23-1.1
- rebuild with new gmp without compat lib

* Thu Oct 20 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.23-1
- New upstream version 1.13.23.

* Wed Oct 19 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.22-2
- New upstream version 1.13.22.
- Remove 3x upstream patches.
- Renumber the two remaining non-upstream patches as patch0, patch1.
- Rebase patch1.

* Mon Oct 17 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.21-4
- Add upstream patch to skip FUSE tests if there is no /dev/fuse.
  This allows us also to remove the Fedora-specific patch which
  disabled these tests before.

* Sat Oct 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.21-3
- Add upstream patch to fix virt-sysprep test.

* Fri Oct 14 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.21-2
- New upstream version 1.13.21.
- Move virt-sysprep to libguestfs-tools, to avoid pulling in extra
  dependencies for RHEV-H.  This tool is not likely to be useful
  for RHEV-H in its current form anyway.
- Change BR cryptsetup-luks -> cryptsetup since that package changed.

* Wed Oct 12 2011 Peter Schiffer <pschiffe@redhat.com> - 1:1.13.20-1.1
- rebuild with new gmp

* Tue Oct 11 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.20-1
- New upstream version 1.13.20.

* Sat Oct  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.19-1
- New upstream version 1.13.19.
- New tool: virt-sysprep.
- Remove the old guestfish and libguestfs-mount packages, and put these
  tools into libguestfs-tools.  This change is long overdue, but is also
  necessitated by the new virt-sysprep tool.  This new tool would pull
  in guestfish anyway, so having separate packages makes no sense.
- Remove old obsoletes for virt-cat, virt-df, virt-df2 and virt-inspector,
  since those packages existed only in much older Fedora.

* Wed Oct  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.18-1
- New upstream version 1.13.18.
- New tool: virt-alignment-scan.

* Tue Oct  4 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.17-1
- New upstream version 1.13.17.
- New tool: virt-sparsify.

* Sat Oct  1 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.16-1
- New upstream version 1.13.16.

* Thu Sep 29 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.15-2
- Rearrange description to make it clearer.
- virt-resize was written in OCaml.  Move it to libguestfs-tools-c
  subpackage since it doesn't require Perl.

* Wed Sep 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.15-1
- New upstream version 1.13.15.
- Add lzop program to the appliance (for compress-out API).
- Remove upstream patch.

* Mon Sep 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.14-2
- Upstream patch to fix timer check failures during boot (RHBZ#502058).

* Sat Sep 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.14-1
- New upstream version 1.13.14.

* Wed Sep 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.13-1
- Add Erlang bindings in erlang-libguestfs subpackage.
- Remove upstream patch.

* Fri Sep 16 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.12-4
- Don't require grub.  See RHBZ#737261.
- Note this (hopefully temporarily) breaks guestfs_grub_install API.
- Include upstream patch to add guestfs_grub_install into an optional group.

* Wed Sep 14 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.12-1
- New upstream version 1.13.12.

* Thu Sep  1 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.11-1
- New upstream version 1.13.11.

* Tue Aug 30 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.10-2
- Remove MAKEDEV dependency (RHBZ#727247).

* Sun Aug 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.10-1
- New upstream version 1.13.10.

* Fri Aug 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.9-1
- New upstream version 1.13.9.

* Fri Aug 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.8-1
- New upstream version 1.13.8.
- Static python library is no longer built, so don't rm it.

* Tue Aug 23 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.7-1
- New upstream version 1.13.7.
- configure --with-extra version string contains Fedora release.
- Build with make V=1 to display full compile commands.
- Remove /usr/sbin PATH setting, not used for a very long time.

* Fri Aug 19 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.6-2
- New upstream version 1.13.6.
- Rebase non-upstream patch to fix qemu -machine option.

* Wed Aug 17 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.5-1
- New upstream version 1.13.5.

* Thu Aug 11 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.4-1
- New upstream version 1.13.4.

* Mon Aug  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.3-4
- New upstream version 1.13.3.
- 'test-getlogin_r.c:55: assertion failed' test must now be fixed in
  gnulib/tests directory instead of daemon/tests (the latter directory
  no longer exists).
- Only run testsuite on x86_64 because of qemu bug.

* Tue Aug  2 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.13.2-3
- Switch Rawhide to use the new development branch (1.13).
- New upstream version 1.13.2.
- Remove upstream patch.
- Ensure config.log is printed, even in the error case.

* Tue Jul 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.1-4
- New upstream stable branch version 1.12.1.
- Remove 5 x upstream patches.
- Add non-upstream patch to deal with broken qemu -machine option.
- Add upstream patch to fix segfault in OCaml bindings.

* Tue Jul 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.0-11
- Bump and rebuild.

* Fri Jul 22 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.0-10
- Rebuild against fixed hivex 1.2.7-7 in dist-f16-perl.

* Thu Jul 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.0-9
- Attempt rebuild in dist-f16-perl.

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 1:1.12.0-8
- Perl mass rebuild

* Thu Jul 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.0-4
- Disable tests, use quickcheck, because of RHBZ#723555, RHBZ#723822.

* Wed Jul 20 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.0-2
- Readd patch to fix virtio-serial test for qemu 0.15.

* Wed Jul 20 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.12.0-1
- New stable version 1.12.0 for Fedora 16.
- Remove upstream patch.
- Disable tests on i686 (because of RHBZ#723555).

* Wed Jul 20 2011 Petr Sabata <contyk@redhat.com> - 1:1.11.20-3
- Perl mass rebuild

* Tue Jul 19 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.20-2
- Add upstream patch to fix virtio-serial test for qemu 0.15.

* Tue Jul 19 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.20-1
- New upstream version 1.11.20.
- Replace standard README file with one suited for Fedora.
- Add guestfs-java(3) manpage to libguestfs-java-devel package.

* Mon Jul 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.19-1
- New upstream version 1.11.19.
- Remove upstream patch.
- Add Ukrainian (uk) man pages subpackage.

* Fri Jul 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.18-2
- Add upstream patch to fix regression test.

* Fri Jul 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.18-1
- New upstream version 1.11.18.
- Force febootstrap >= 3.7 which contains a fix for latest Rawhide.
- Use --enable-install-daemon to install guestfsd.

* Thu Jul 14 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.17-1
- New upstream version 1.11.17.

* Wed Jul 13 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.16-1
- New upstream version 1.11.16.

* Tue Jul 12 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.15-1
- New upstream version 1.11.15.

* Wed Jul  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.14-1
- New upstream version 1.11.14.

* Wed Jul  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.13-3
- Further updates to libguestfs-live-service after feedback from
  Dan Berrange and Lennart Poettering.

* Tue Jul  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.13-2
- Add libguestfs-live-service subpackage.  This can be installed in
  virtual machines in order to enable safe editing of files in running
  guests (eg. guestfish --live).

* Thu Jun 30 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.13-1
- New upstream version 1.11.13.

* Wed Jun 29 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.12-3
- Bump and rebuild for parted 3.0.
- Depend on fixed parted >= 3.0-2.

* Tue Jun 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.12-1
- New upstream version 1.11.12.

* Tue Jun 21 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.11-1
- New upstream version 1.11.11.

* Mon Jun 20 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.10-3
- Temporarily stop setting CCFLAGS in perl subdirectory.
  See: http://bugs.debian.org/cgi-bin/bugreport.cgi?bug=628522

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.11.10-2
- Perl mass rebuild

* Fri Jun 10 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.10-1
- New upstream version 1.11.10.
- Enable tests since fix for RHBZ#710921 is in Rawhide kernel package.

* Fri Jun 10 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.11.9-8
- Perl 5.14 mass rebuild

* Sun Jun  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.9-7
- Build against new parted.
- Disable tests on i686 because of RHBZ#710921.
- Remove recipes/ doc directory.  This is no longer present because it
  was replaced by a guestfs-recipes(1) man page.

* Sat Jun  4 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.9-1
- New upstream version 1.11.9.

* Wed May 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.8-1
- New upstream version 1.11.8.
- "zero" command test is fixed now, so we don't need to skip it.

* Tue May 17 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.7-3
- New upstream version 1.11.7.
- Depends on hivex >= 1.2.7.
- Remove upstream patch.
- Skip test of "zero" command (RHBZ#705499).

* Mon May  9 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.5-2
- configure: Use Python platform-dependent site-packages.

* Mon May  9 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.5-1
- New upstream version 1.11.5.
- virt-edit has been rewritten in C, therefore this tool has been moved
  into the libguestfs-tools-c package.

* Sun May  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.4-1
- New upstream version 1.11.4.

* Fri Apr 22 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.3-1
- New upstream version 1.11.3.

* Mon Apr 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.2-1
- New upstream version 1.11.2.
- Fixes Python bindings when used in Python threads.
- Remove upstream patch.

* Sat Apr 16 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.1-2
- New upstream version 1.11.1.
- Add upstream patch so we don't depend on libtool.

* Fri Apr 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.0-2
- Bump and rebuild.

* Tue Apr 12 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.11.0-1
- New upstream development branch 1.11.0.
- New Source URL.
- Remove patches which are now upstream.

* Sun Apr 10 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.18-4
- Include further fixes to virt-resize from upstream.

* Sat Apr  9 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.18-2
- New upstream version 1.9.18.
- Requires ocaml-pcre for new virt-resize.
- Remove libguestfs-test-tool-helper program which is no longer used.
- Include upstream fix for virt-resize build.

* Wed Apr  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.17-2
- Remove partially translated Ukrainian manpages.

* Tue Apr  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.17-1
- New upstream version 1.9.17.

* Fri Apr  1 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.16-1
- New upstream version 1.9.16.

* Fri Apr  1 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.15-1
- New upstream version 1.9.15.
- Add BR libconfig-devel.
- Add /etc/libguestfs-tools.conf (config file for guestfish, guestmount,
  virt-rescue; in future for other tools as well).

* Mon Mar 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.14-1
- New upstream version 1.9.14.
- Include 'acl' as BR so virt-rescue gets getfacl and setfacl programs.

* Mon Mar 28 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.13-2
- Include 'attr' as BR (required for getfattr, setfattr programs in
  virt-rescue).

* Thu Mar 24 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.13-1
- New upstream version 1.9.13.

* Fri Mar 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.12-1
- New upstream version 1.9.12.

* Wed Mar 16 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.11-2
- Add runtime requires on minimum glibc because of newly readable binaries.

* Tue Mar 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.11-1
- New upstream version 1.9.11.
- Add generated Ruby documentation (rdoc).

* Tue Mar  8 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.10-1
- New upstream version 1.9.10.
- Remove patches (now upstream).

* Fri Mar  4 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.9-2
- Include upstream patches to fix virt-make-fs with qemu-img 0.14.

* Fri Mar  4 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.9-1
- New upstream version 1.9.9.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.8-1
- New upstream version 1.9.8.

* Sun Feb  6 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.7-7
- Rebuild against rpm-4.9.0-0.beta1.6.fc15 to fix OCaml deps.  See discussion:
  http://lists.fedoraproject.org/pipermail/devel/2011-February/148398.html

* Wed Feb  2 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.7-6
- Add temporary non-upstream patch to fix /etc/mtab.
  See: https://www.redhat.com/archives/libguestfs/2011-February/msg00006.html
- Add fix for regressions/rhbz557655.sh so it works when tracing is enabled.
- Add guestfs-perl(3) man page.

* Tue Feb  1 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.7-3
- Enable trace in 'make check' section.

* Sun Jan 30 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.7-1
- New upstream version 1.9.7.

* Wed Jan 26 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.6-2
- Bump and rebuild.

* Sat Jan 22 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.6-1
- New upstream version 1.9.6.

* Tue Jan 18 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.5-1
- New upstream version 1.9.5.

* Sat Jan 15 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.4-1
- New upstream version 1.9.4.

* Fri Jan 14 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.3-2
- Only runtime require febootstrap-supermin-helper (not whole of
  febootstrap).

* Tue Jan 11 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.3-1
- New upstream version 1.9.3.

* Wed Jan 05 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.2-2
- Bump and rebuild.

* Mon Jan  3 2011 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.2-1
- New upstream version 1.9.2.
- New tools: virt-copy-in, virt-copy-out, virt-tar-in, virt-tar-out.
  These are just shell script wrappers around guestfish so they are
  included in the guestfish package.

* Fri Dec 31 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.1-1
- New upstream version 1.9.1.

* Tue Dec 21 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.0-2
- Bump and rebuild.

* Sun Dec 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.9.0-1
- New upstream development branch 1.9.0.
- Include ROADMAP in devel package.

* Thu Dec 16 2010 Richard Jones <rjones@redhat.com> - 1:1.7.24-1
- New upstream version 1.7.24.
- Adds getxattr/lgetxattr APIs to support guestfs-browser.

* Sat Dec 11 2010 Richard Jones <rjones@redhat.com> - 1:1.7.23-1
- New upstream version 1.7.23.

* Sat Dec 11 2010 Richard Jones <rjones@redhat.com> - 1:1.7.22-1
- New upstream version 1.7.22.
- Depend on febootstrap 3.3 which fixes the checksum stability problem.

* Fri Dec 10 2010 Richard Jones <rjones@redhat.com> - 1:1.7.21-1
- New upstream version 1.7.21.

* Tue Dec  7 2010 Richard Jones <rjones@redhat.com> - 1:1.7.20-1
- New upstream version 1.7.20.
- Remove patches which are upstream.

* Tue Dec  7 2010 Richard Jones <rjones@redhat.com> - 1:1.7.19-15
- Rebuild appliance with febootstrap 3.1-5 because we accidentally
  reopened RHBZ#654638.

* Mon Dec  6 2010 Richard Jones <rjones@redhat.com> - 1:1.7.19-14
- Rebuild appliance properly using febootstrap 3.1 and alternate yum repo.

* Sun Dec  5 2010 Richard Jones <rjones@redhat.com> - 1:1.7.19-1
- New upstream development version 1.7.19.
- Appliance building in this version has been substantially rewritten
  and this requires febootstrap >= 3.0 to build.
- createrepo no longer required.
- Supermin appliance is the default.

* Wed Dec  1 2010 Richard Jones <rjones@redhat.com> - 1:1.7.18-1
- New upstream development version 1.7.18.

* Tue Nov 30 2010 Richard Jones <rjones@redhat.com> - 1:1.7.17-1
- New upstream development version 1.7.17.

* Fri Nov 26 2010 Richard Jones <rjones@redhat.com> - 1:1.7.16-1
- New upstream development version 1.7.16.
- guestfish no longer requires pod2text, hence no longer requires perl.
- Require febootstrap >= 2.11.

* Fri Nov 26 2010 Richard Jones <rjones@redhat.com> - 1:1.7.15-2
- New upstream development version 1.7.15.
- Split out new libguestfs-tools-c package from libguestfs-tools.
  . This is so that the -tools-c package can be pulled in by people
    wanting to avoid a dependency on Perl, while -tools pulls in everything
    as before.
  . The C tools currently are: cat, df, filesystems, fish, inspector, ls,
    mount, rescue.
  . guestfish still requires pod2text which requires perl.  This will be
    rectified in the next release.
  . libguestfs-tools no longer pulls in guestfish.
- guestfish also depends on: less, man, vi
- Add BR db4-utils (although since RPM needs it, it not really necessary).
- Runtime requires on db4-utils should be on core lib, not tools package.
- Change all "Requires: perl-Foo" to "Requires: perl(Foo)".

* Thu Nov 25 2010 Richard Jones <rjones@redhat.com> - 1:1.7.14-1
- New upstream development version 1.7.14.

* Wed Nov 24 2010 Richard Jones <rjones@redhat.com> - 1:1.7.13-3
- New upstream development version 1.7.13.
- New manual pages containing example code.
- Ship examples for C, OCaml, Ruby, Python.
- Don't ship HTML versions of man pages.
- Rebase no-fuse-test patch to latest version.

* Tue Nov 23 2010 Richard Jones <rjones@redhat.com> - 1:1.7.12-1
- New upstream development version 1.7.12.
- New tool: virt-filesystems.  virt-list-filesystems and virt-list-partitions
  are deprecated, but still included in the package.

* Wed Nov 17 2010 Richard Jones <rjones@redhat.com> - 1:1.7.11-1
- New upstream development version 1.7.11.
- Fix Source0 URL which had pointed to the 1.5 directory.
- virt-inspector is not a dependency of guestmount.

* Wed Nov 17 2010 Richard Jones <rjones@redhat.com> - 1:1.7.10-1
- New upstream development version 1.7.10.

* Tue Nov 16 2010 Richard Jones <rjones@redhat.com> - 1:1.7.9-1
- New upstream development version 1.7.9.

* Mon Nov 15 2010 Richard Jones <rjones@redhat.com> - 1:1.7.8-1
- New upstream development version 1.7.8.
- Add Obsoletes so perl-Sys-Guestfs overrides perl-libguestfs (RHBZ#652587).

* Mon Nov 15 2010 Richard Jones <rjones@redhat.com> - 1:1.7.7-1
- New upstream development version 1.7.7.
- Rename perl-libguestfs as perl-Sys-Guestfs (RHBZ#652587).

* Sat Nov 13 2010 Richard Jones <rjones@redhat.com> - 1:1.7.6-1
- New upstream development version 1.7.6.

* Sat Nov 13 2010 Richard Jones <rjones@redhat.com> - 1:1.7.5-2
- New upstream development version 1.7.5.
- Remove hand-installation of Ruby bindings.
- Remove upstream patch.

* Thu Nov 11 2010 Richard Jones <rjones@redhat.com> - 1:1.7.4-2
- New upstream development version 1.7.4.
- ocaml-xml-light is no longer required.
- Remove guestfs-actions.h and guestfs-structs.h.  Libguestfs now
  only exports a single <guestfs.h> header file.
- Add patch to fix broken Perl test.
- Remove workaround for RHBZ#563103.

* Mon Nov  8 2010 Richard Jones <rjones@redhat.com> - 1:1.7.3-1
- New upstream development version 1.7.3.
- Add AUTHORS file from tarball.

* Fri Nov  5 2010 Richard Jones <rjones@redhat.com> - 1:1.7.2-1
- New upstream development version 1.7.2.
- Add requires ruby to ruby-libguestfs package.

* Wed Nov  3 2010 Richard Jones <rjones@redhat.com> - 1:1.7.1-1
- New upstream development version 1.7.1.
- Add BR gperf.

* Tue Nov  2 2010 Richard Jones <rjones@redhat.com> - 1:1.7.0-1
- New upstream development branch and version 1.7.0.

* Fri Oct 29 2010 Richard Jones <rjones@redhat.com> - 1:1.5.26-1
- New upstream development version 1.5.26.

* Thu Oct 28 2010 Richard Jones <rjones@redhat.com> - 1:1.5.25-1
- New upstream development version 1.5.25.
- Rewritten virt-inspector.
- Requires febootstrap >= 2.10.
- New virt-inspector requires db_dump program.

* Wed Oct 27 2010 Richard Jones <rjones@redhat.com> - 1:1.5.24-2
- Attempt to run tests.

* Wed Oct 27 2010 Richard Jones <rjones@redhat.com> - 1:1.5.24-1
- New upstream development version 1.5.24.

* Sat Oct 23 2010 Richard Jones <rjones@redhat.com> - 1:1.5.23-1
- Fix for libguestfs: missing disk format specifier when adding a disk
  (RHBZ#642934, CVE-2010-3851).

* Tue Oct 19 2010 Richard Jones <rjones@redhat.com> - 1:1.5.22-1
- New upstream development version 1.5.22.

* Sat Oct  9 2010 Richard Jones <rjones@redhat.com> - 1:1.5.21-2
- guestfish no longer requires virt-inspector.

* Fri Oct  1 2010 Richard Jones <rjones@redhat.com> - 1:1.5.21-1
- New upstream development version 1.5.21.

* Sun Sep 26 2010 Richard Jones <rjones@redhat.com> - 1:1.5.20-1
- New upstream development version 1.5.20.

* Wed Sep 22 2010 Richard Jones <rjones@redhat.com> - 1:1.5.18-1
- New upstream development version 1.5.18.
- Note that guestfish '-a' and '-d' options were broken in 1.5.17, so
  upgrading to this version is highly recommended.

* Tue Sep 21 2010 Richard Jones <rjones@redhat.com> - 1:1.5.17-1
- New upstream development version 1.5.17.

* Wed Sep 15 2010 Richard Jones <rjones@redhat.com> - 1:1.5.16-1
- New upstream development version 1.5.16.

* Wed Sep 15 2010 Richard Jones <rjones@redhat.com> - 1:1.5.15-1
- New upstream development version 1.5.15.

* Tue Sep 14 2010 Richard Jones <rjones@redhat.com> - 1:1.5.14-1
- New upstream development version 1.5.14.

* Mon Sep 13 2010 Richard Jones <rjones@redhat.com> - 1:1.5.13-1
- New upstream version 1.5.13.
- Removed the patch workaround for RHBZ#630583.  The same workaround
  is now upstream (the bug is not fixed).

* Sat Sep 11 2010 Richard Jones <rjones@redhat.com> - 1:1.5.12-1
- New upstream version 1.5.12.

* Fri Sep 10 2010 Richard Jones <rjones@redhat.com> - 1:1.5.11-1
- New upstream version 1.5.11.
- Note: fixes a serious bug in guestfish 'copy-out' command.

* Thu Sep  9 2010 Richard Jones <rjones@redhat.com> - 1:1.5.10-1
- New upstream version 1.5.10.

* Wed Sep  8 2010 Richard Jones <rjones@redhat.com> - 1:1.5.9-2
- Disable tests, still failing because of RHBZ#630777.

* Wed Sep  8 2010 Richard Jones <rjones@redhat.com> - 1:1.5.9-1
- New upstream version 1.5.9.

* Mon Sep  6 2010 Richard Jones <rjones@redhat.com> - 1:1.5.8-2
- Add patch to work around RHBZ#630583 and reenable tests.

* Sat Sep  4 2010 Richard Jones <rjones@redhat.com> - 1:1.5.8-1
- New upstream version 1.5.8.
- Add BR po4a for translations of man pages.
- Add PHP bindings.
- Remove partially-translated Japanese webpages.

* Wed Sep  1 2010 Richard Jones <rjones@redhat.com> - 1:1.5.7-1
- New upstream version 1.5.7.
- 'debug' command is enabled by default now.

* Fri Aug 27 2010 Richard Jones <rjones@redhat.com> - 1:1.5.6-1
- New upstream version 1.5.6.

* Fri Aug 27 2010 Richard Jones <rjones@redhat.com> - 1:1.5.5-2
- Use bug-fixed febootstrap 2.9.

* Thu Aug 26 2010 Richard Jones <rjones@redhat.com> - 1:1.5.5-1
- New upstream version 1.5.5.

* Tue Aug 24 2010 Richard Jones <rjones@redhat.com> - 1:1.5.4-2
- Disable tests again, because the Rawhide kernel still won't boot.

* Tue Aug 24 2010 Richard Jones <rjones@redhat.com> - 1:1.5.4-1
- New upstream development version 1.5.4.
- Now requires febootstrap >= 2.8 and qemu >= 0.12.
- Re-enable tests because RHBZ#624854 is supposed to be fixed.
- Upstream Source URL has changed.

* Wed Aug 18 2010 Richard Jones <rjones@redhat.com> - 1:1.5.3-2
- Disable tests because of RHBZ#624854.

* Tue Aug 17 2010 Richard Jones <rjones@redhat.com> - 1:1.5.3-1
- New upstream development version 1.5.3.

* Wed Aug 11 2010 Richard Jones <rjones@redhat.com> - 1:1.5.2-6
- Bump and rebuild.

* Thu Aug 05 2010 Richard Jones - 1:1.5.2-5
- Bump and rebuild.

* Fri Jul 23 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jul 23 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.2-2
- New upstream development version 1.5.2.
- +BuildRequires: cryptsetup-luks.

* Wed Jul 21 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.1-1
- New upstream development version 1.5.1.

* Tue Jul 20 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.0-7
- Requires binutils (RHBZ#616437).

* Mon Jul 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.0-6
- Fix libguestfs-find-requires.sh for new location of hostfiles (RHBZ#615946).

* Thu Jul  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.0-5
- Include RELEASE-NOTES in devel package.

* Thu Jul  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.5.0-4
- New development branch 1.5.0.
- Remove two upstream patches.
- Work around permanently broken test-getlogin_r Gnulib test.

* Mon Jun 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.21-4
- Explicitly depend on e2fsprogs.
- Add patch to add e2fsprogs to the appliance.
- Add patch to fix GFS kernel module problem.

* Fri Jun 25 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 1:1.3.21-2
- Rebuild

* Wed Jun 16 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.21-1
- New upstream version 1.3.21.

* Tue Jun  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.20-1
- New upstream version 1.3.20.
- Since upstream commit a043b6854a0c4 we don't need to run make install
  twice.

* Fri Jun  4 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.19-1
- New upstream version 1.3.19.

* Wed Jun  2 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.18-1
- New upstream version 1.3.18.

* Thu May 27 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.17-1
- New upstream version 1.3.17.
- Change repo name to 'fedora-14'.

* Wed May 26 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.16-6
- Co-own bash_completion.d directory.

* Tue May 25 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.16-4
- New upstream version 1.3.16.
- Add guestfish bash tab completion script.

* Mon May 24 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.14-1
- New upstream version 1.3.14.

* Sun May 16 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.13-1
- New upstream version 1.3.13.
- Add BUGS to documentation.
- Force update of hivex dependency to 1.2.2 since it contains
  important registry import fixes.
- Remove patch1, now upstream.

* Fri May 14 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.12-3
- Backport supermin build fix from upstream.
- Further changes required for new layout of supermin appliance.

* Fri May 14 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.12-1
- New upstream version 1.3.12.
- febootstrap >= 2.7 is required at compile time and at runtime (at runtime
  because of the new febootstrap-supermin-helper).
- Bugs fixed: 591155 591250 576879 591142 588651 507810 521674 559963 516096.

* Sat May  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.11-1
- New upstream version 1.3.11.

* Fri May  7 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.10-2
- New upstream version 1.3.10.

* Thu May 06 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.9-2
- Bump and rebuild against updated libconfig

* Fri Apr 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.9-1
- New upstream version 1.3.9.

* Thu Apr 29 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.3.8-2
- Mass rebuild with perl-5.12.0

* Tue Apr 27 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.8-1
- New upstream version 1.3.8.

* Fri Apr 23 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.7-1
- New upstream version 1.3.7.
- NOTE: fixes a segfault in guestfish 1.3.6 when using the -a option.

* Thu Apr 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.6-1
- New upstream version 1.3.6.

* Mon Apr 19 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.5-1
- New upstream version 1.3.5.

* Sat Apr 17 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.4-1
- New upstream version 1.3.4.

* Sun Apr 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.3-1
- New upstream version 1.3.3.
- New virt-resize option --LV-expand.
- New API: lvresize-free.
- Fixes RHBZ#581501.

* Sun Apr 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.2-3
- Disable checksum-device test.

* Sat Apr 10 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.2-2
- Bump and rebuild.

* Sat Apr 10 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.2-1
- New upstream version 1.3.2.
- New APIs: checksum-device, part-del, part-get-bootable, part-get-mbr-id,
  part-set-mbr-id, vgscan, ntfsresize, txz-in, txz-out.
- Enhanced/fixed virt-resize tool.
- Enhanced virt-list-partitions tool.
- Fixes: 580016, 580650, 579155, 580556.

* Sat Apr 10 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.1-4
- Bump and rebuild.

* Thu Apr  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.1-3
- Runtime requires should only be on libguestfs-tools subpackage.

* Thu Apr  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.1-2
- Missing BR on qemu-img package.

* Thu Apr  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.3.1-1
- New upstream version 1.3.1.
- For explanation of apparently large version jump, see:
  https://www.redhat.com/archives/libguestfs/2010-April/msg00057.html
- New tool: virt-make-fs.
- New API: guestfs_zero_device.
- Fixes RHBZ#580246 (tar-in command hangs if uploading more than
  available space)
- Fixes RHBZ#579664 (guestfish doesn't report error when there is not
  enough space for image allocation)
- +BR perl-String-ShellQuote (for virt-make-fs).

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.89-1
- New upstream version 1.0.89.
- Improved version of virt-win-reg.
- Many smaller bugfixes.
- Requires hivex >= 1.2.1.
- Remove TERM=dumb patch which is now upstream.

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.88-7
- Backport of TERM=dumb patch from upstream.
- Workaround failure caused by RHBZ#575734.
- Workaround unknown failure of test_swapon_label_0.

* Tue Mar 30 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.88-5
- Attempted workaround for RHBZ#563103, so we can reenable tests.

* Fri Mar 26 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.88-2
- Remember to check in the new sources.

* Fri Mar 26 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.88-1
- New upstream version 1.0.88.
- Mainly small bugfixes.
- Update Spanish translation of libguestfs (RHBZ#576876).
- Use ext4 dev tools on RHEL 5 (RHBZ#576688).
- Add support for minix filesystem (RHBZ#576689).

* Fri Mar 26 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.87-2
- Add vim-minimal to BR, it is now required by the appliance.

* Tue Mar 23 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.87-1
- New upstream version 1.0.87.
- New tools: virt-resize and virt-list-partitions.
- New APIs: guestfs_copy_size; APIs for querying the relationship between
  LVM objects.
- Add vim to the virt-rescue appliance.

* Fri Mar 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.86-1
- New upstream version 1.0.86.
- libguestfs-supermin-helper rewritten in C (from shell), reduces
  appliance boot time by 2-3 seconds.
- Fix parsing of integers in guestfish on 32 bit platforms (RHBZ#569757
  and RHBZ#567567).
- Enhance virt-inspector output for Windows guests.
- Add product_name field to virt-inspector output for all guests.
- Weaken dependencies on libntfs-3g.so, don't include SONAME in dep.
- Remove false dependency on libply (plymouth libraries).
- Spanish translation (RHBZ#570181).
- Fix bash regexp quoting bug.

* Fri Mar 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-4
- Bump and rebuild.

* Thu Mar 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-3
- Bump and rebuild.

* Sat Mar 06 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-2
- Bump and rebuild.

* Mon Mar  1 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.85-1
- New upstream version 1.0.85.
- Remove hivex, now a separate upstream project and package.
- Remove supermin quoting patch, now upstream.

* Mon Mar  1 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-6
- Fix quoting in supermin-split script (RHBZ#566511).
- Don't include bogus './builddir' entries in supermin hostfiles
  (RHBZ#566512).

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-4
- Don't include generator.ml in rpm.  It's 400K and almost no one will need it.
- Add comments to spec file about how repo building works.
- Whitespace changes in the spec file.

* Mon Feb 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-3
- Bump and rebuild.

* Tue Feb 16 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-2
- Bump and rebuild.

* Fri Feb 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.84-1
- New upstream version 1.0.84.

* Fri Feb 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.83-8
- Bump and rebuild.

* Thu Feb 11 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-7
- Disable tests.  These fail in Koji (on RHEL 5 kernel) because of a
  bug in preadv/pwritev emulation in glibc (RHBZ#563103).

* Tue Feb  9 2010 Matthew Booth <mbooth@redhat.com> - 1.0.83-6
- Change buildnonet to buildnet
- Allow buildnet, mirror, updates, virtio and runtests to be configured by user
  macros.

* Mon Feb  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-5
- libguestfs-tools should require perl-XML-Writer (RHBZ#562858).

* Mon Feb  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-4
- Use virtio for block device access (RHBZ#509383 is fixed).

* Fri Feb  5 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-3
- Rebuild: possible timing-related build problem in Koji.

* Fri Feb  5 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.83-2
- New upstream release 1.0.83.
- This release fixes:
  Add Marathi translations (RHBZ#561671).
  Polish translations (RHBZ#502533).
  Add Gujarti translations (Sweta Kothari) (RHBZ#560918).
  Update Oriya translations (thanks Manoj Kumar Giri) (RHBZ#559498).
  Set locale in C programs so l10n works (RHBZ#559962).
  Add Tamil translation (RHBZ#559877) (thanks to I.Felix)
  Update Punjabi translation (RHBZ#559480) (thanks Jaswinder Singh)
- There are significant fixes to hive file handling.
- Add hivexsh and manual page.
- Remove two patches, now upstream.

* Sun Jan 31 2010 Richard W.M. Jones <rjones@redhat.com> - 1:1.0.82-7
- Bump and rebuild.

* Fri Jan 29 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.82-6
- Backport a better fix for RHBZ557655 test from upstream.
- Backport fix for unreadable yum.log from upstream.

* Thu Jan 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.82-3
- Backport RHBZ557655 test fix from upstream.

* Thu Jan 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.82-1
- New upstream version 1.0.82.  This includes the two patches
  we were carrying, so those are now removed.
- This release fixes:
  RHBZ#559498 (Oriya translation).
  RHBZ#559480 (Punjabi translation).
  RHBZ#558593 (Should prevent corruption by multilib).
  RHBZ#559237 (Telugu translation).
  RHBZ#557655 (Use xstrtol/xstrtoll to parse integers in guestfish).
  RHBZ#557195 (Missing crc kernel modules for recent Linux).
- In addition this contains numerous fixes to the hivex library
  for parsing Windows Registry files, making hivex* and virt-win-reg
  more robust.
- New API call 'filesize'.

* Thu Jan 28 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-8
- Backport special handling of libgcc_s.so.
- Backport unreadable files patch from RHEL 6 / upstream.

* Fri Jan 22 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-5
- Require febootstrap >= 2.6 (RHBZ#557262).

* Thu Jan 21 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-4
- Rebuild for unannounced soname bump (libntfs-3g.so).

* Fri Jan 15 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-3
- Rebuild for unannounced soname bump (libplybootsplash.so).

* Thu Jan 14 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-2
- Rebuild for broken dependency (iptables soname bump).

* Wed Jan 13 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.81-1
- New upstream version 1.0.81.
- Remove two upstream patches.
- virt-inspector: Make RPM application data more specific (RHBZ#552718).

* Tue Jan 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-14
- Reenable tests because RHBZ#553689 is fixed.

* Tue Jan 12 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-13
- Rebuild because of libparted soname bump (1.9 -> 2.1).

* Fri Jan  8 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-12
- qemu in Rawhide is totally broken (RHBZ#553689).  Disable tests.

* Thu Jan  7 2010 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-11
- Remove gfs-utils (deprecated and removed from Fedora 13 by the
  upstream Cluster Suite developers).
- Include patch to fix regression in qemu -serial stdio option.

* Tue Dec 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-10
- Remove some debugging statements which were left in the requires
  script by accident.

* Mon Dec 21 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-9
- Generate additional requires for supermin (RHBZ#547496).

* Fri Dec 18 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-3
- Work around udevsettle command problem (RHBZ#548121).
- Enable tests.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-2
- Disable tests because of RHBZ#548121.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.80-1
- New upstream release 1.0.80.
- New Polish translations (RHBZ#502533).
- Give a meaningful error if no usable kernels are found (RHBZ#539746).
- New tool: virt-list-filesystems

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 1:1.0.79-3
- rebuild against perl 5.10.1

* Wed Nov 18 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.79-2
- New upstream release 1.0.79.
- Adds FUSE test script and multiple fixes for FUSE (RHBZ#538069).
- Fix virt-df in Xen (RHBZ#538041).
- Improve speed of supermin appliance.
- Disable FUSE-related tests because Koji doesn't currently allow them.
  fuse: device not found, try 'modprobe fuse' first

* Tue Nov 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.78-2
- New upstream release 1.0.78.
- Many more filesystem types supported by this release - add them
  as dependencies.

* Tue Nov  3 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.77-1
- New upstream release 1.0.77.
- Support for mounting guest in host using FUSE (guestmount command).
- hivex*(1) man pages should be in main package, not -devel, since
  they are user commands.
- libguestfs-tools: Fix "self-obsoletion" issue raised by rpmlint.
- perl: Remove bogus script Sys/bindtests.pl.

* Thu Oct 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.75-2
- New upstream release 1.0.75.
- New library: libhivex.
- New tools: virt-win-reg, hivexml, hivexget.
- Don't require chntpw.
- Add BR libxml2-devel, accidentally omitted before.

* Tue Oct 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.74-1
- New upstream release 1.0.74.
- New API call: guestfs_find0.
- New tools: virt-ls, virt-tar.

* Wed Oct 14 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.73-1
- New upstream release 1.0.73.
- OCaml library now depends on xml-light.
- Deal with installed documentation.

* Tue Sep 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.72-2
- Force rebuild.

* Wed Sep 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.72-1
- New upstream release 1.0.72.
- New tools: virt-edit, virt-rescue.
- Combine virt-cat, virt-df, virt-edit, virt-inspector and virt-rescue
  into a single package called libguestfs-tools.

* Tue Sep 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.71-2
- New upstream release 1.0.71.

* Fri Sep 18 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.70-2
- Perl bindings require perl-XML-XPath (fixed RHBZ#523547).

* Tue Sep 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.70-1
- New upstream release 1.0.70.
- Fixes build problem related to old version of GNU gettext.

* Tue Sep 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.69-1
- New upstream release 1.0.69.
- Reenable the tests (because RHBZ#516543 is supposed to be fixed).
- New main loop code should fix RHBZ#501888, RHBZ#504418.
- Add waitpid along guestfs_close path (fixes RHBZ#518747).

* Wed Aug 19 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.68-2
- New upstream release 1.0.68.
- BR genisoimage.

* Thu Aug 13 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.67-2
- New upstream release 1.0.67.

* Fri Aug  7 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.66-5
- Set network interface to ne2k_pci (workaround for RHBZ#516022).
- Rerun autoconf because patch touches configure script.

* Thu Aug  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.66-1
- New upstream release 1.0.66.

* Wed Jul 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.65-1
- New upstream release 1.0.65.
- Add Obsoletes for virt-df2 (RHBZ#514309).
- Disable tests because of ongoing TCG problems with newest qemu in Rawhide.

* Thu Jul 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.64-3
- RHBZ#513249 bug in qemu is now fixed, so try to rebuild and run tests.
- However RHBZ#503236 still prevents us from testing on i386.

* Thu Jul 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.64-1
- New upstream release 1.0.64.
- New tool 'libguestfs-test-tool'.

* Wed Jul 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.61-1
- New upstream release 1.0.61.
- New tool / subpackage 'virt-cat'.
- New BR perl-libintl.

* Wed Jul 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.60-2
- Fix runtime Requires so they use epoch correctly.

* Tue Jul 14 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.60-1
- New upstream release 1.0.60.

* Fri Jul 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.58-2
- New upstream release 1.0.58.

* Fri Jul 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.57-1
- New upstream release 1.0.57.
- New tool virt-df (obsoletes existing package with this name).
- RHBZ#507066 may be fixed, so reenable tests.

* Tue Jul  7 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.56-2
- New upstream release 1.0.56.
- Don't rerun generator.

* Thu Jul  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.55-1
- New upstream release 1.0.55.
- New manual page libguestfs(3).

* Mon Jun 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.54-2
- New upstream release 1.0.54.
- +BR perl-XML-Writer.

* Wed Jun 24 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.53-1
- New upstream release 1.0.53.
- Disable all tests (because of RHBZ#507066).

* Wed Jun 24 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.52-1
- New upstream release 1.0.52.

* Mon Jun 22 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.51-1
- New upstream release 1.0.51.
- Removed patches which are now upstream.

* Sat Jun 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.49-5
- Remove workaround for RHBZ#507007, since bug is now fixed.
- Pull in upstream patch to fix pclose checking
  (testing as possible fix for RHBZ#507066).
- Pull in upstream patch to check waitpid return values
  (testing as possible fix for RHBZ#507066).

* Fri Jun 19 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.49-2
- New upstream release 1.0.49.
- Add workaround for RHBZ#507007.

* Tue Jun 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.48-2
- Accidentally omitted the supermin image from previous version.

* Tue Jun 16 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.48-1
- New upstream release 1.0.48.
- Should fix all the brokenness from 1.0.47.
- Requires febootstrap >= 2.3.

* Mon Jun 15 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.47-2
- New upstream release 1.0.47.
- Enable experimental supermin appliance build.
- Fix path to appliance.

* Fri Jun 12 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.45-2
- New upstream release 1.0.45.

* Wed Jun 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.44-2
- Disable ppc/ppc64 tests again because of RHBZ#505109.

* Wed Jun 10 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.44-1
- New upstream version 1.0.44.
- Try enabling tests on ppc & ppc64 since it looks like the bug(s?)
  in qemu which might have caused them to fail have been fixed.

* Tue Jun  9 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.43-1
- New upstream version 1.0.43.
- New upstream URL.
- Requires chntpw program.

* Sat Jun  6 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.42-1
- New upstream version 1.0.42.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.41-1
- New upstream version 1.0.41.
- Fixes a number of regressions in RHBZ#503169.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.40-1
- New upstream version 1.0.40.

* Thu Jun  4 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.39-1
- New upstream version 1.0.39.
- Fixes:
  . libguestfs /dev is too sparse for kernel installation/upgrade (RHBZ#503169)
  . OCaml bindings build failure (RHBZ#502309)

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.38-2
- Disable tests on ix86 because of RHBZ#503236.

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.38-1
- New upstream version 1.0.38.

* Fri May 29 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.37-1
- New upstream version 1.0.37.
- Fixes:
  . "mkdir-p" should not throw errors on preexisting directories (RHBZ#503133)
  . cramfs and squashfs modules should be available in libguestfs appliances
      (RHBZ#503135)

* Thu May 28 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.36-2
- New upstream version 1.0.36.
- Rerun the generator in prep section.

* Thu May 28 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.35-1
- New upstream version 1.0.35.
- Fixes multiple bugs in bindings parameters (RHBZ#501892).

* Wed May 27 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.34-1
- New upstream version 1.0.34.

* Wed May 27 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.33-1
- New upstream version 1.0.33.
- --with-java-home option is no longer required.
- Upstream contains potential fixes for:
    501878 built-in commands like 'alloc' and 'help' don't autocomplete
    501883 javadoc messed up in libguestfs java documentation
    501885 Doesn't detect missing Java, --with-java-home=no should not be needed
    502533 Polish translation of libguestfs
    n/a    Allow more ext filesystem kmods (Charles Duffy)

* Tue May 26 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.32-2
- New upstream version 1.0.32.
- Use %%find_lang macro.

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.31-1
- Rebuild for OCaml 3.11.1.
- New upstream version 1.0.31.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.30-1
- New upstream version 1.0.30.  Now includes test-bootbootboot.sh script.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.29-3
- New upstream version 1.0.29 (fixes RHBZ#502007 RHBZ#502018).
- This should allow us to enable tests for i386 and x86-64.
- Added test-bootbootboot.sh script which was missed from 1.0.29 tarball.
- Pass kernel noapic flag to workaround RHBZ#502058.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.28-1
- New upstream version 1.0.28.  Nothing has visibly changed, but
  the source has been gettextized and we want to check that doesn't
  break anything.

* Thu May 21 2009 Richard Jones <rjones@redhat.com> - 1.0.27-3
- Change requirement from qemu -> qemu-kvm (RHBZ#501761).

* Tue May 19 2009 Richard Jones <rjones@redhat.com> - 1.0.27-2
- New upstream version 1.0.27.

* Mon May 18 2009 Richard Jones <rjones@redhat.com> - 1.0.26-6
- Experimentally try to reenable ppc and ppc64 builds.
- Note BZ numbers which are causing tests to fail.

* Mon May 18 2009 Richard Jones <rjones@redhat.com> - 1.0.26-1
- New upstream version 1.0.26.

* Tue May 12 2009 Richard Jones <rjones@redhat.com> - 1.0.25-4
- New upstream version 1.0.25.
- Enable debugging when running the tests.
- Disable tests - don't work correctly in Koji.

* Tue May 12 2009 Richard Jones <rjones@redhat.com> - 1.0.24-1
- New upstream version 1.0.24.
- BRs glibc-static for the new command tests.
- Enable tests.

* Mon May 11 2009 Richard Jones <rjones@redhat.com> - 1.0.23-2
- New upstream version 1.0.23.
- Don't try to use updates during build.

* Fri May  8 2009 Richard Jones <rjones@redhat.com> - 1.0.21-3
- New upstream version 1.0.21.

* Thu May  7 2009 Richard Jones <rjones@redhat.com> - 1.0.20-2
- New upstream version 1.0.20.

* Thu May  7 2009 Richard Jones <rjones@redhat.com> - 1.0.19-1
- New upstream version 1.0.19.

* Tue Apr 28 2009 Richard Jones <rjones@redhat.com> - 1.0.15-1
- New upstream version 1.0.15.

* Fri Apr 24 2009 Richard Jones <rjones@redhat.com> - 1.0.12-1
- New upstream version 1.0.12.

* Wed Apr 22 2009 Richard Jones <rjones@redhat.com> - 1.0.6-1
- New upstream version 1.0.6.

* Mon Apr 20 2009 Richard Jones <rjones@redhat.com> - 1.0.2-1
- New upstream version 1.0.2.

* Thu Apr 16 2009 Richard Jones <rjones@redhat.com> - 0.9.9-12
- Multiple fixes to get it to scratch build in Koji.

* Sat Apr  4 2009 Richard Jones <rjones@redhat.com> - 0.9.9-1
- Initial build.
