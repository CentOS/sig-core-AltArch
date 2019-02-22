# We have to override the new %%install behavior because, well... the kernel is special.
%global __spec_install_pre %{___build_pre}

Summary: The Linux kernel

# For a stable, released kernel, released_kernel should be 1. For rawhide
# and/or a kernel built from an rc or git snapshot, released_kernel should
# be 0.
%global released_kernel 1

# Sign modules on x86.  Make sure the config files match this setting if more
# architectures are added.
%ifarch %{ix86} x86_64
%global signkernel 1
%global signmodules 1
%global zipmodules 1
%else
%global signkernel 0
%global signmodules 1
%global zipmodules 1
%endif

%if %{zipmodules}
%global zipsed -e 's/\.ko$/\.ko.xz/'
%endif

# define buildid .local

# baserelease defines which build revision of this kernel version we're
# building.  We used to call this fedora_build, but the magical name
# baserelease is matched by the rpmdev-bumpspec tool, which you should use.
#
# We used to have some extra magic weirdness to bump this automatically,
# but now we don't.  Just use: rpmdev-bumpspec -c 'comment for changelog'
# When changing base_sublevel below or going from rc to a final kernel,
# reset this by hand to 1 (or to 0 and then use rpmdev-bumpspec).
# scripts/rebase.sh should be made to do that for you, actually.
#
# NOTE: baserelease must be > 0 or bad things will happen if you switch
#       to a released kernel (released version will be < rc version)
#
# For non-released -rc kernels, this will be appended after the rcX and
# gitX tags, so a 3 here would become part of release "0.rcX.gitX.3"
#
%global baserelease 300
%global fedora_build %{baserelease}

# base_sublevel is the kernel version we're starting with and patching
# on top of -- for example, 3.1-rc7-git1 starts with a 3.0 base,
# which yields a base_sublevel of 0.
%define base_sublevel 19

## If this is a released kernel ##
%if 0%{?released_kernel}

# Do we have a -stable update to apply?
%define stable_update 23
# Set rpm version accordingly
%if 0%{?stable_update}
%define stablerev %{stable_update}
%define stable_base %{stable_update}
%endif
%define rpmversion 4.%{base_sublevel}.%{stable_update}

## The not-released-kernel case ##
%else
# The next upstream release sublevel (base_sublevel+1)
%define upstream_sublevel %(echo $((%{base_sublevel} + 1)))
# The rc snapshot level
%global rcrev 0
# The git snapshot level
%define gitrev 0
# Set rpm version accordingly
%define rpmversion 4.%{upstream_sublevel}.0
%endif
# Nb: The above rcrev and gitrev values automagically define Patch00 and Patch01 below.

# What parts do we want to build?  We must build at least one kernel.
# These are the kernels that are built IF the architecture allows it.
# All should default to 1 (enabled) and be flipped to 0 (disabled)
# by later arch-specific checks.

# The following build options are enabled by default.
# Use either --without <opt> in your rpmbuild command or force values
# to 0 in here to disable them.
#
# standard kernel
%define with_up        %{?_without_up:        0} %{?!_without_up:        1}
# kernel PAE (only valid for i686 (PAE) and ARM (lpae))
%define with_pae       %{?_without_pae:       0} %{?!_without_pae:       1}
# kernel-debug
%define with_debug     %{?_without_debug:     0} %{?!_without_debug:     1}
# kernel-headers
%define with_headers   %{?_without_headers:   0} %{?!_without_headers:   1}
%define with_cross_headers   %{?_without_cross_headers:   0} %{?!_without_cross_headers:   1}
# kernel-debuginfo
%define with_debuginfo %{?_without_debuginfo: 0} %{?!_without_debuginfo: 1}
# Want to build a the vsdo directories installed
%define with_vdso_install %{?_without_vdso_install: 0} %{?!_without_vdso_install: 1}
#
# Additional options for user-friendly one-off kernel building:
#
# Only build the base kernel (--with baseonly):
%define with_baseonly  %{?_with_baseonly:     1} %{?!_with_baseonly:     0}
# Only build the pae kernel (--with paeonly):
%define with_paeonly   %{?_with_paeonly:      1} %{?!_with_paeonly:      0}
# Only build the debug kernel (--with dbgonly):
%define with_dbgonly   %{?_with_dbgonly:      1} %{?!_with_dbgonly:      0}
#
# should we do C=1 builds with sparse
%define with_sparse    %{?_with_sparse:       1} %{?!_with_sparse:       0}
#
# Cross compile requested?
%define with_cross    %{?_with_cross:         1} %{?!_with_cross:        0}
#
# build a release kernel on rawhide
%define with_release   %{?_with_release:      1} %{?!_with_release:      0}

# verbose build, i.e. no silent rules and V=1
%define with_verbose %{?_with_verbose:        1} %{?!_with_verbose:      0}

# Set debugbuildsenabled to 1 for production (build separate debug kernels)
#  and 0 for rawhide (all kernels are debug kernels).
# See also 'make debug' and 'make release'.
%define debugbuildsenabled 1

# Kernel headers are being split out into a separate package
%if 0%{?fedora}
%define with_headers 0
%define with_cross_headers 0
%endif

%if %{with_verbose}
%define make_opts V=1
%else
%define make_opts -s
%endif

# Want to build a vanilla kernel build without any non-upstream patches?
%define with_vanilla %{?_with_vanilla: 1} %{?!_with_vanilla: 0}

# pkg_release is what we'll fill in for the rpm Release: field
%if 0%{?released_kernel}

%define pkg_release %{fedora_build}%{?buildid}%{?dist}

%else

# non-released_kernel
%if 0%{?rcrev}
%define rctag .rc%rcrev
%else
%define rctag .rc0
%endif
%if 0%{?gitrev}
%define gittag .git%gitrev
%else
%define gittag .git0
%endif
%define pkg_release 0%{?rctag}%{?gittag}.%{fedora_build}%{?buildid}%{?dist}

%endif

# The kernel tarball/base version
%define kversion 4.%{base_sublevel}

%define make_target bzImage
%define image_install_path boot

%define KVERREL %{version}-%{release}.%{_target_cpu}
%define hdrarch %_target_cpu
%define asmarch %_target_cpu

%if 0%{!?nopatches:1}
%define nopatches 0
%endif

%if %{with_vanilla}
%define nopatches 1
%endif

%if %{nopatches}
%define variant -vanilla
%endif

%if !%{debugbuildsenabled}
%define with_debug 0
%endif

%if !%{with_debuginfo}
%define _enable_debug_packages 0
%endif
%define debuginfodir /usr/lib/debug
# Needed because we override almost everything involving build-ids
# and debuginfo generation. Currently we rely on the old alldebug setting.
%global _build_id_links alldebug

# kernel PAE is only built on ARMv7 in rawhide.
# Fedora 27 and earlier still support PAE, so change this on rebases.
# %ifnarch i686 armv7hl
%ifnarch armv7hl
%define with_pae 0
%endif

# if requested, only build base kernel
%if %{with_baseonly}
%define with_pae 0
%define with_debug 0
%endif

# if requested, only build pae kernel
%if %{with_paeonly}
%define with_up 0
%define with_debug 0
%endif

# if requested, only build debug kernel
%if %{with_dbgonly}
%if %{debugbuildsenabled}
%define with_up 0
%define with_pae 0
%endif
%define with_pae 0
%endif

%define all_x86 i386 i686

%if %{with_vdso_install}
%define use_vdso 1
%endif

# Overrides for generic default options

# don't do debug builds on anything but i686 and x86_64
%ifnarch i686 x86_64
%define with_debug 0
%endif

# don't build noarch kernels or headers (duh)
%ifarch noarch
%define with_up 0
%define with_headers 0
%define with_cross_headers 0
%define all_arch_configs kernel-%{version}-*.config
%endif

# sparse blows up on ppc
%ifnarch %{power64}
%define with_sparse 0
%endif

# Per-arch tweaks

%ifarch %{all_x86}
%define asmarch x86
%define hdrarch i386
%define pae PAE
%define all_arch_configs kernel-%{version}-i?86*.config
%define kernel_image arch/x86/boot/bzImage
%endif

%ifarch x86_64
%define asmarch x86
%define all_arch_configs kernel-%{version}-x86_64*.config
%define kernel_image arch/x86/boot/bzImage
%endif

%ifarch %{power64}
%define asmarch powerpc
%define hdrarch powerpc
%define make_target vmlinux
%define kernel_image vmlinux
%define kernel_image_elf 1
%ifarch ppc64le
%define all_arch_configs kernel-%{version}-ppc64le*.config
%endif
%endif

%ifarch s390x
%define asmarch s390
%define hdrarch s390
%define all_arch_configs kernel-%{version}-s390x.config
%define kernel_image arch/s390/boot/bzImage
%endif

%ifarch %{arm}
%define all_arch_configs kernel-%{version}-arm*.config
%define skip_nonpae_vdso 1
%define asmarch arm
%define hdrarch arm
%define pae lpae
%define make_target bzImage
%define kernel_image arch/arm/boot/zImage
# http://lists.infradead.org/pipermail/linux-arm-kernel/2012-March/091404.html
%define kernel_mflags KALLSYMS_EXTRA_PASS=1
# we only build headers/perf/tools on the base arm arches
# just like we used to only build them on i386 for x86
%ifnarch armv7hl
%define with_headers 0
%define with_cross_headers 0
%endif
%endif

%ifarch aarch64
%define all_arch_configs kernel-%{version}-aarch64*.config
%define asmarch arm64
%define hdrarch arm64
%define make_target Image.gz
%define kernel_image arch/arm64/boot/Image.gz
%endif

# Should make listnewconfig fail if there's config options
# printed out?
%if %{nopatches}
%define listnewconfig_fail 0
%define configmismatch_fail 0
%else
%define listnewconfig_fail 1
%define configmismatch_fail 1
%endif

# To temporarily exclude an architecture from being built, add it to
# %%nobuildarches. Do _NOT_ use the ExclusiveArch: line, because if we
# don't build kernel-headers then the new build system will no longer let
# us use the previous build of that package -- it'll just be completely AWOL.
# Which is a BadThing(tm).

# We only build kernel-headers on the following...
%define nobuildarches i386

%ifarch %nobuildarches
%define with_up 0
%define with_pae 0
%define with_debuginfo 0
%define with_debug 0
%define _enable_debug_packages 0
%endif

%define with_pae_debug 0
%if %{with_pae}
%define with_pae_debug %{with_debug}
%endif

# Architectures we build tools/cpupower on
%define cpupowerarchs %{ix86} x86_64 %{power64} %{arm} aarch64

%if %{use_vdso}

%if 0%{?skip_nonpae_vdso}
%define _use_vdso 0
%else
%define _use_vdso 1
%endif

%else
%define _use_vdso 0
%endif


#
# Packages that need to be installed before the kernel is, because the %%post
# scripts use them.
#
%define kernel_prereq  coreutils, systemd >= 203-2, /usr/bin/kernel-install
%define initrd_prereq  dracut >= 027


Name: kernel%{?variant}
License: GPLv2 and Redistributable, no modification permitted
URL: https://www.kernel.org/
Version: %{rpmversion}
Release: %{pkg_release}
# DO NOT CHANGE THE 'ExclusiveArch' LINE TO TEMPORARILY EXCLUDE AN ARCHITECTURE BUILD.
# SET %%nobuildarches (ABOVE) INSTEAD
ExclusiveArch: %{all_x86} x86_64 s390x %{arm} aarch64 ppc64le
ExclusiveOS: Linux
%ifnarch %{nobuildarches}
Requires: kernel-core-uname-r = %{KVERREL}%{?variant}
Requires: kernel-modules-uname-r = %{KVERREL}%{?variant}
%endif

Conflicts: xorg-x11-drv-vmmouse < 14.0.0

#
# List the packages used during the kernel build
#
BuildRequires: kmod, patch, bash, tar, git-core
BuildRequires: bzip2, xz, findutils, gzip, m4, perl-interpreter, perl-Carp, perl-devel, perl-generators, make, diffutils, gawk
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc, bison, flex
BuildRequires: net-tools, hostname, bc, elfutils-devel
%if %{with_sparse}
BuildRequires: sparse
%endif
BuildConflicts: rhbuildsys(DiskFree) < 500Mb
%if %{with_debuginfo}
BuildRequires: rpm-build, elfutils
BuildConflicts: rpm < 4.13.0.1-19
# Most of these should be enabled after more investigation
%undefine _include_minidebuginfo
%undefine _find_debuginfo_dwz_opts
%undefine _unique_build_ids
%undefine _unique_debug_names
%undefine _unique_debug_srcs
%undefine _debugsource_packages
%undefine _debuginfo_subpackages
%undefine _include_gdb_index
%global _find_debuginfo_opts -r
%global _missing_build_ids_terminate_build 1
%global _no_recompute_build_ids 1
%endif

%if %{signkernel}%{signmodules}
BuildRequires: openssl openssl-devel
%if %{signkernel}
BuildRequires: pesign >= 0.10-4
%endif
%endif

%if %{with_cross}
BuildRequires: binutils-%{_build_arch}-linux-gnu, gcc-%{_build_arch}-linux-gnu
%define cross_opts CROSS_COMPILE=%{_build_arch}-linux-gnu-
%endif

Source0: https://www.kernel.org/pub/linux/kernel/v4.x/linux-%{kversion}.tar.xz

Source11: x509.genkey
Source12: remove-binary-diff.pl
Source15: merge.pl
Source16: mod-extra.list
Source17: mod-extra.sh
Source18: mod-sign.sh
Source90: filter-x86_64.sh
Source91: filter-armv7hl.sh
Source92: filter-i686.sh
Source93: filter-aarch64.sh
Source94: filter-ppc64le.sh
Source95: filter-s390x.sh
Source99: filter-modules.sh
%define modsign_cmd %{SOURCE18}

Source20: kernel-aarch64.config
Source21: kernel-aarch64-debug.config
Source22: kernel-armv7hl.config
Source23: kernel-armv7hl-debug.config
Source24: kernel-armv7hl-lpae.config
Source25: kernel-armv7hl-lpae-debug.config
Source26: kernel-i686.config
Source27: kernel-i686-debug.config
Source30: kernel-ppc64le.config
Source31: kernel-ppc64le-debug.config
Source32: kernel-s390x.config
Source33: kernel-s390x-debug.config
Source34: kernel-x86_64.config
Source35: kernel-x86_64-debug.config

Source40: generate_all_configs.sh
Source41: generate_debug_configs.sh

Source42: process_configs.sh
Source43: generate_bls_conf.sh

# This file is intentionally left empty in the stock kernel. Its a nicety
# added for those wanting to do custom rebuilds with altered config opts.
Source1000: kernel-local

# Sources for kernel-tools
Source2000: cpupower.service
Source2001: cpupower.config

# Here should be only the patches up to the upstream canonical Linus tree.

# For a stable release kernel
%if 0%{?stable_update}
%if 0%{?stable_base}
%define    stable_patch_00  patch-4.%{base_sublevel}.%{stable_base}.xz
Source5000: %{stable_patch_00}
%endif

# non-released_kernel case
# These are automagically defined by the rcrev and gitrev values set up
# near the top of this spec file.
%else
%if 0%{?rcrev}
Source5000: patch-4.%{upstream_sublevel}-rc%{rcrev}.xz
%if 0%{?gitrev}
Source5001: patch-4.%{upstream_sublevel}-rc%{rcrev}-git%{gitrev}.xz
%endif
%else
# pre-{base_sublevel+1}-rc1 case
%if 0%{?gitrev}
Source5000: patch-4.%{base_sublevel}-git%{gitrev}.xz
%endif
%endif
%endif

## Patches needed for building this package

## compile fixes

# ongoing complaint, full discussion delayed until ksummit/plumbers
Patch002: 0001-iio-Use-event-header-from-kernel-tree.patch

%if !%{nopatches}

# Git trees.

# Standalone patches
# 100 - Generic long running patches

Patch110: lib-cpumask-Make-CPUMASK_OFFSTACK-usable-without-deb.patch

Patch111: input-kill-stupid-messages.patch

Patch112: die-floppy-die.patch

Patch113: no-pcspkr-modalias.patch

Patch114: silence-fbcon-logo.patch

Patch115: Kbuild-Add-an-option-to-enable-GCC-VTA.patch

Patch116: crash-driver.patch

Patch117: lis3-improve-handling-of-null-rate.patch

Patch118: scsi-sd_revalidate_disk-prevent-NULL-ptr-deref.patch

Patch119: namespaces-no-expert.patch

Patch120: ath9k-rx-dma-stop-check.patch

Patch121: xen-pciback-Don-t-disable-PCI_COMMAND-on-PCI-device-.patch

Patch122: Input-synaptics-pin-3-touches-when-the-firmware-repo.patch

# This no longer applies, let's see if it needs to be updated
# Patch123: firmware-Drop-WARN-from-usermodehelper_read_trylock-.patch

# 200 - x86 / secureboot

Patch201: efi-lockdown.patch

Patch202: KEYS-Allow-unrestricted-boot-time-addition-of-keys-t.patch

Patch203: Add-EFI-signature-data-types.patch

Patch204: Add-an-EFI-signature-blob-parser-and-key-loader.patch

Patch205: MODSIGN-Import-certificates-from-UEFI-Secure-Boot.patch

Patch206: MODSIGN-Support-not-importing-certs-from-db.patch

# bz 1497559 - Make kernel MODSIGN code not error on missing variables
Patch207: 0001-Make-get_cert_list-not-complain-about-cert-lists-tha.patch
Patch208: 0002-Add-efi_status_to_str-and-rework-efi_status_to_err.patch
Patch209: 0003-Make-get_cert_list-use-efi_status_to_str-to-print-er.patch

Patch210: disable-i8042-check-on-apple-mac.patch

Patch211: drm-i915-hush-check-crtc-state.patch

Patch212: efi-secureboot.patch

# 300 - ARM patches
Patch300: arm64-Add-option-of-13-for-FORCE_MAX_ZONEORDER.patch

# http://www.spinics.net/lists/linux-tegra/msg26029.html
Patch301: usb-phy-tegra-Add-38.4MHz-clock-table-entry.patch
# http://patchwork.ozlabs.org/patch/587554/
Patch302: ARM-tegra-usb-no-reset.patch

# https://patchwork.kernel.org/patch/10351797/
Patch303: ACPI-scan-Fix-regression-related-to-X-Gene-UARTs.patch
# rhbz 1574718
Patch304: ACPI-irq-Workaround-firmware-issue-on-X-Gene-based-m400.patch

# https://patchwork.kernel.org/patch/9820417/
Patch305: qcom-msm89xx-fixes.patch

# https://patchwork.kernel.org/project/linux-mmc/list/?submitter=71861
Patch306: arm-sdhci-esdhc-imx-fixes.patch

# https://www.spinics.net/lists/arm-kernel/msg670137.html
Patch307: arm64-ZynqMP-firmware-clock-drivers-core.patch

Patch308: arm64-96boards-Rock960-CE-board-support.patch
Patch309: arm64-rockchip-add-initial-Rockpro64.patch
Patch310: arm64-rk3399-add-idle-states.patch

Patch311: gpio-pxa-handle-corner-case-of-unprobed-device.patch

Patch330: bcm2835-cpufreq-add-CPU-frequency-control-driver.patch

# https://patchwork.kernel.org/patch/10686407/
Patch332: raspberrypi-Fix-firmware-calls-with-large-buffers.patch

# From 4.20, fix eth link/act lights on 3B+
Patch334: bcm2837-fix-eth-leds.patch

# Patches enabling device specific brcm firmware nvram
# https://www.spinics.net/lists/linux-wireless/msg178827.html
Patch340: brcmfmac-Remove-firmware-loading-code-duplication.patch

# Fix for AllWinner A64 Timer Errata, still not final
# https://patchwork.kernel.org/patch/10392891/
Patch350: arm64-arch_timer-Workaround-for-Allwinner-A64-timer-instability.patch
Patch351: arm64-dts-allwinner-a64-Enable-A64-timer-workaround.patch

# 400 - IBM (ppc/s390x) patches

# 500 - Temp fixes/CVEs etc

# rhbz 1476467
Patch501: Fix-for-module-sig-verification.patch

# rhbz 1431375
Patch502: input-rmi4-remove-the-need-for-artifical-IRQ.patch

# Ena fixes from 4.20
Patch503: ena-fixes.patch

# rhbz 1526312, patch is in 4.20, can be dropped on rebase
Patch507: 0001-HID-i2c-hid-override-HID-descriptors-for-certain-dev.patch

# Patches from 4.20 fixing black screen on CHT devices with i915.fastboot=1
Patch508: cherrytrail-pwm-lpss-fixes.patch

# rhbz 1526312 (accelerometer part of the bug), patches pending upstream
Patch510: iio-accel-kxcjk1013-Add-more-hardware-ids.patch

# rhbz 1645070 patch queued upstream for merging into 4.21
Patch516: asus-fx503-keyb.patch

# rhbz 1661961 patch merged upstream in 4.20
Patch517: 0001-Bluetooth-btsdio-Do-not-bind-to-non-removable-BCM434.patch

# CVE-2019-3459 and CVE-2019-3460 rbhz 1663176 1663179 1665925
Patch519: CVE-2019-3459-and-CVE-2019-3460.patch

##centos
Patch10002: 9999-centos-a83t-hdmi.patch
Patch11002: 9999-centos-r40sata.patch
##end centos

# END OF PATCH DEFINITIONS

%endif


%description
The kernel meta package

#
# This macro does requires, provides, conflicts, obsoletes for a kernel package.
#	%%kernel_reqprovconf <subpackage>
# It uses any kernel_<subpackage>_conflicts and kernel_<subpackage>_obsoletes
# macros defined above.
#
%define kernel_reqprovconf \
Provides: kernel = %{rpmversion}-%{pkg_release}\
Provides: kernel-%{_target_cpu} = %{rpmversion}-%{pkg_release}%{?1:+%{1}}\
Provides: kernel-drm-nouveau = 16\
Provides: kernel-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
Requires(pre): %{kernel_prereq}\
Requires(pre): %{initrd_prereq}\
Requires(pre): linux-firmware >= 20150904-56.git6ebf5d57\
Requires(preun): systemd >= 200\
Conflicts: xfsprogs < 4.3.0-1\
Conflicts: xorg-x11-drv-vmmouse < 13.0.99\
%{expand:%%{?kernel%{?1:_%{1}}_conflicts:Conflicts: %%{kernel%{?1:_%{1}}_conflicts}}}\
%{expand:%%{?kernel%{?1:_%{1}}_obsoletes:Obsoletes: %%{kernel%{?1:_%{1}}_obsoletes}}}\
%{expand:%%{?kernel%{?1:_%{1}}_provides:Provides: %%{kernel%{?1:_%{1}}_provides}}}\
# We can't let RPM do the dependencies automatic because it'll then pick up\
# a correct but undesirable perl dependency from the module headers which\
# isn't required for the kernel proper to function\
AutoReq: no\
AutoProv: yes\
%{nil}

%package headers
Summary: Header files for the Linux kernel for use by glibc
Obsoletes: glibc-kernheaders < 3.0-46
Provides: glibc-kernheaders = 3.0-46
%if "0%{?variant}"
Obsoletes: kernel-headers < %{rpmversion}-%{pkg_release}
Provides: kernel-headers = %{rpmversion}-%{pkg_release}
%endif
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package cross-headers
Summary: Header files for the Linux kernel for use by cross-glibc
%description cross-headers
Kernel-cross-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
cross-glibc package.


%package debuginfo-common-%{_target_cpu}
Summary: Kernel source files used by %{name}-debuginfo packages
Provides: installonlypkg(kernel)
%description debuginfo-common-%{_target_cpu}
This package is required by %{name}-debuginfo subpackages.
It provides the kernel source files common to all builds.

#
# This macro creates a kernel-<subpackage>-debuginfo package.
#	%%kernel_debuginfo_package <subpackage>
#
%define kernel_debuginfo_package() \
%package %{?1:%{1}-}debuginfo\
Summary: Debug information for package %{name}%{?1:-%{1}}\
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}\
Provides: %{name}%{?1:-%{1}}-debuginfo-%{_target_cpu} = %{version}-%{release}\
Provides: installonlypkg(kernel)\
AutoReqProv: no\
%description %{?1:%{1}-}debuginfo\
This package provides debug information for package %{name}%{?1:-%{1}}.\
This is required to use SystemTap with %{name}%{?1:-%{1}}-%{KVERREL}.\
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '/.*/%%{KVERREL}%{?1:[+]%{1}}/.*|/.*%%{KVERREL}%{?1:\+%{1}}(\.debug)?' -o debuginfo%{?1}.list}\
%{nil}

#
# This macro creates a kernel-<subpackage>-devel package.
#	%%kernel_devel_package <subpackage> <pretty-name>
#
%define kernel_devel_package() \
%package %{?1:%{1}-}devel\
Summary: Development package for building kernel modules to match the %{?2:%{2} }kernel\
Provides: kernel%{?1:-%{1}}-devel-%{_target_cpu} = %{version}-%{release}\
Provides: kernel-devel-%{_target_cpu} = %{version}-%{release}%{?1:+%{1}}\
Provides: kernel-devel-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
Provides: installonlypkg(kernel)\
AutoReqProv: no\
Requires(pre): findutils\
Requires: findutils\
Requires: perl-interpreter\
%description %{?1:%{1}-}devel\
This package provides kernel headers and makefiles sufficient to build modules\
against the %{?2:%{2} }kernel package.\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules-extra package.
#	%%kernel_modules_extra_package <subpackage> <pretty-name>
#
%define kernel_modules_extra_package() \
%package %{?1:%{1}-}modules-extra\
Summary: Extra kernel modules to match the %{?2:%{2} }kernel\
Provides: kernel%{?1:-%{1}}-modules-extra-%{_target_cpu} = %{version}-%{release}\
Provides: kernel%{?1:-%{1}}-modules-extra-%{_target_cpu} = %{version}-%{release}%{?1:+%{1}}\
Provides: kernel%{?1:-%{1}}-modules-extra = %{version}-%{release}%{?1:+%{1}}\
Provides: installonlypkg(kernel-module)\
Provides: kernel%{?1:-%{1}}-modules-extra-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
Requires: kernel-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
Requires: kernel%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules-extra\
This package provides less commonly used kernel modules for the %{?2:%{2} }kernel package.\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules package.
#	%%kernel_modules_package <subpackage> <pretty-name>
#
%define kernel_modules_package() \
%package %{?1:%{1}-}modules\
Summary: kernel modules to match the %{?2:%{2}-}core kernel\
Provides: kernel%{?1:-%{1}}-modules-%{_target_cpu} = %{version}-%{release}\
Provides: kernel-modules-%{_target_cpu} = %{version}-%{release}%{?1:+%{1}}\
Provides: kernel-modules = %{version}-%{release}%{?1:+%{1}}\
Provides: installonlypkg(kernel-module)\
Provides: kernel%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
Requires: kernel-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules\
This package provides commonly used kernel modules for the %{?2:%{2}-}core kernel package.\
%{nil}

#
# this macro creates a kernel-<subpackage> meta package.
#	%%kernel_meta_package <subpackage>
#
%define kernel_meta_package() \
%package %{1}\
summary: kernel meta-package for the %{1} kernel\
Requires: kernel-%{1}-core-uname-r = %{KVERREL}%{?variant}+%{1}\
Requires: kernel-%{1}-modules-uname-r = %{KVERREL}%{?variant}+%{1}\
Provides: installonlypkg(kernel)\
%description %{1}\
The meta-package for the %{1} kernel\
%{nil}

#
# This macro creates a kernel-<subpackage> and its -devel and -debuginfo too.
#	%%define variant_summary The Linux kernel compiled for <configuration>
#	%%kernel_variant_package [-n <pretty-name>] <subpackage>
#
%define kernel_variant_package(n:) \
%package %{?1:%{1}-}core\
Summary: %{variant_summary}\
Provides: kernel-%{?1:%{1}-}core-uname-r = %{KVERREL}%{?variant}%{?1:+%{1}}\
Provides: installonlypkg(kernel)\
%ifarch %{power64}\
Obsoletes: kernel-bootwrapper\
%endif\
%{expand:%%kernel_reqprovconf}\
%if %{?1:1} %{!?1:0} \
%{expand:%%kernel_meta_package %{?1:%{1}}}\
%endif\
%{expand:%%kernel_devel_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%{expand:%%kernel_modules_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%{expand:%%kernel_modules_extra_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%{expand:%%kernel_debuginfo_package %{?1:%{1}}}\
%{nil}

# Now, each variant package.

%if %{with_pae}
%ifnarch armv7hl
%define variant_summary The Linux kernel compiled for PAE capable machines
%kernel_variant_package %{pae}
%description %{pae}-core
This package includes a version of the Linux kernel with support for up to
64GB of high memory. It requires a CPU with Physical Address Extensions (PAE).
The non-PAE kernel can only address up to 4GB of memory.
Install the kernel-PAE package if your machine has more than 4GB of memory.
%else
%define variant_summary The Linux kernel compiled for Cortex-A15
%kernel_variant_package %{pae}
%description %{pae}-core
This package includes a version of the Linux kernel with support for
Cortex-A15 devices with LPAE and HW virtualisation support
%endif


%define variant_summary The Linux kernel compiled with extra debugging enabled for PAE capable machines
%kernel_variant_package %{pae}debug
Obsoletes: kernel-PAE-debug
%description %{pae}debug-core
This package includes a version of the Linux kernel with support for up to
64GB of high memory. It requires a CPU with Physical Address Extensions (PAE).
The non-PAE kernel can only address up to 4GB of memory.
Install the kernel-PAE package if your machine has more than 4GB of memory.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.
%endif

%define variant_summary The Linux kernel compiled with extra debugging enabled
%kernel_variant_package debug
%description debug-core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.

# And finally the main -core package

%define variant_summary The Linux kernel
%kernel_variant_package
%description core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.


%prep
# do a few sanity-checks for --with *only builds
%if %{with_baseonly}
%if !%{with_up}%{with_pae}
echo "Cannot build --with baseonly, up build is disabled"
exit 1
%endif
%endif

%if "%{baserelease}" == "0"
echo "baserelease must be greater than zero"
exit 1
%endif

# more sanity checking; do it quietly
if [ "%{patches}" != "%%{patches}" ] ; then
  for patch in %{patches} ; do
    if [ ! -f $patch ] ; then
      echo "ERROR: Patch  ${patch##/*/}  listed in specfile but is missing"
      exit 1
    fi
  done
fi 2>/dev/null

patch_command='patch -p1 -F1 -s'
ApplyPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  if ! grep -E "^Patch[0-9]+: $patch\$" %{_specdir}/${RPM_PACKAGE_NAME%%%%%{?variant}}.spec ; then
    if [ "${patch:0:8}" != "patch-4." ] ; then
      echo "ERROR: Patch  $patch  not listed as a source patch in specfile"
      exit 1
    fi
  fi 2>/dev/null
  case "$patch" in
  *.bz2) bunzip2 < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *.gz)  gunzip  < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *.xz)  unxz    < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *) $patch_command ${1+"$@"} < "$RPM_SOURCE_DIR/$patch" ;;
  esac
}

# don't apply patch if it's empty
ApplyOptionalPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  local C=$(wc -l $RPM_SOURCE_DIR/$patch | awk '{print $1}')
  if [ "$C" -gt 9 ]; then
    ApplyPatch $patch ${1+"$@"}
  fi
}

# First we unpack the kernel tarball.
# If this isn't the first make prep, we use links to the existing clean tarball
# which speeds things up quite a bit.

# Update to latest upstream.
%if 0%{?released_kernel}
%define vanillaversion 4.%{base_sublevel}
# non-released_kernel case
%else
%if 0%{?rcrev}
%define vanillaversion 4.%{upstream_sublevel}-rc%{rcrev}
%if 0%{?gitrev}
%define vanillaversion 4.%{upstream_sublevel}-rc%{rcrev}-git%{gitrev}
%endif
%else
# pre-{base_sublevel+1}-rc1 case
%if 0%{?gitrev}
%define vanillaversion 4.%{base_sublevel}-git%{gitrev}
%else
%define vanillaversion 4.%{base_sublevel}
%endif
%endif
%endif

# %%{vanillaversion} : the full version name, e.g. 2.6.35-rc6-git3
# %%{kversion}       : the base version, e.g. 2.6.34

# Use kernel-%%{kversion}%%{?dist} as the top-level directory name
# so we can prep different trees within a single git directory.

# Build a list of the other top-level kernel tree directories.
# This will be used to hardlink identical vanilla subdirs.
sharedirs=$(find "$PWD" -maxdepth 1 -type d -name 'kernel-4.*' \
            | grep -x -v "$PWD"/kernel-%{kversion}%{?dist}) ||:

# Delete all old stale trees.
if [ -d kernel-%{kversion}%{?dist} ]; then
  cd kernel-%{kversion}%{?dist}
  for i in linux-*
  do
     if [ -d $i ]; then
       # Just in case we ctrl-c'd a prep already
       rm -rf deleteme.%{_target_cpu}
       # Move away the stale away, and delete in background.
       mv $i deleteme-$i
       rm -rf deleteme* &
     fi
  done
  cd ..
fi

# Generate new tree
if [ ! -d kernel-%{kversion}%{?dist}/vanilla-%{vanillaversion} ]; then

  if [ -d kernel-%{kversion}%{?dist}/vanilla-%{kversion} ]; then

    # The base vanilla version already exists.
    cd kernel-%{kversion}%{?dist}

    # Any vanilla-* directories other than the base one are stale.
    for dir in vanilla-*; do
      [ "$dir" = vanilla-%{kversion} ] || rm -rf $dir &
    done

  else

    rm -f pax_global_header
    # Look for an identical base vanilla dir that can be hardlinked.
    for sharedir in $sharedirs ; do
      if [[ ! -z $sharedir  &&  -d $sharedir/vanilla-%{kversion} ]] ; then
        break
      fi
    done
    if [[ ! -z $sharedir  &&  -d $sharedir/vanilla-%{kversion} ]] ; then
%setup -q -n kernel-%{kversion}%{?dist} -c -T
      cp -al $sharedir/vanilla-%{kversion} .
    else
%setup -q -n kernel-%{kversion}%{?dist} -c
      mv linux-%{kversion} vanilla-%{kversion}
    fi

  fi

%if "%{kversion}" != "%{vanillaversion}"

  for sharedir in $sharedirs ; do
    if [[ ! -z $sharedir  &&  -d $sharedir/vanilla-%{vanillaversion} ]] ; then
      break
    fi
  done
  if [[ ! -z $sharedir  &&  -d $sharedir/vanilla-%{vanillaversion} ]] ; then

    cp -al $sharedir/vanilla-%{vanillaversion} .

  else

    # Need to apply patches to the base vanilla version.
    cp -al vanilla-%{kversion} vanilla-%{vanillaversion}
    cd vanilla-%{vanillaversion}

cp %{SOURCE12} .

# Update vanilla to the latest upstream.
# (non-released_kernel case only)
%if 0%{?rcrev}
    xzcat %{SOURCE5000} | ./remove-binary-diff.pl | patch -p1 -F1 -s
%if 0%{?gitrev}
    xzcat %{SOURCE5001} | ./remove-binary-diff.pl | patch -p1 -F1 -s
%endif
%else
# pre-{base_sublevel+1}-rc1 case
%if 0%{?gitrev}
    xzcat %{SOURCE5000} | ./remove-binary-diff.pl | patch -p1 -F1 -s
%endif
%endif
    git init
    git config user.email "noreply@centos.org"
    git config user.name "AltArch Kernel"
    git config gc.auto 0
    git add .
    git commit -a -q -m "baseline"

    cd ..

  fi

%endif

else

  # We already have all vanilla dirs, just change to the top-level directory.
  cd kernel-%{kversion}%{?dist}

fi

# Now build the fedora kernel tree.
cp -al vanilla-%{vanillaversion} linux-%{KVERREL}

cd linux-%{KVERREL}
if [ ! -d .git ]; then
    git init
    git config user.email "noreply@centos.org"
    git config user.name "AltArch Kernel"
    git config gc.auto 0
    git add .
    git commit -a -q -m "baseline"
fi


# released_kernel with possible stable updates
%if 0%{?stable_base}
# This is special because the kernel spec is hell and nothing is consistent
xzcat %{SOURCE5000} | patch -p1 -F1 -s
git commit -a -m "Stable update"
%endif

# Note: Even in the "nopatches" path some patches (build tweaks and compile
# fixes) will always get applied; see patch defition above for details

git am %{patches}

# END OF PATCH APPLICATIONS

# Any further pre-build tree manipulations happen here.

chmod +x scripts/checkpatch.pl
chmod +x tools/objtool/sync-check.sh
mv COPYING COPYING-%{version}

# This Prevents scripts/setlocalversion from mucking with our version numbers.
touch .scmversion

# Deal with configs stuff
mkdir configs
cd configs

# Drop some necessary files from the source dir into the buildroot
cp $RPM_SOURCE_DIR/kernel-*.config .
cp %{SOURCE1000} .
cp %{SOURCE15} .
cp %{SOURCE40} .
cp %{SOURCE41} .
cp %{SOURCE43} .

%if !%{debugbuildsenabled}
# The normal build is a really debug build and the user has explicitly requested
# a release kernel. Change the config files into non-debug versions.
%if !%{with_release}
VERSION=%{version} ./generate_debug_configs.sh
%else
VERSION=%{version} ./generate_all_configs.sh
%endif

%else
VERSION=%{version} ./generate_all_configs.sh
%endif

# Merge in any user-provided local config option changes
%ifnarch %nobuildarches
for i in %{all_arch_configs}
do
  mv $i $i.tmp
  ./merge.pl %{SOURCE1000} $i.tmp > $i
  rm $i.tmp
done
%endif

# only deal with configs if we are going to build for the arch
%ifnarch %nobuildarches

%if !%{debugbuildsenabled}
rm -f kernel-%{version}-*debug.config
%endif

%define make make %{?cross_opts}

CheckConfigs() {
     ./check_configs.awk $1 $2 > .mismatches
     if [ -s .mismatches ]
     then
	echo "Error: Mismatches found in configuration files"
	cat .mismatches
	exit 1
     fi
}

cp %{SOURCE42} .
OPTS=""
%if %{listnewconfig_fail}
	OPTS="$OPTS -n"
%endif
%if %{configmismatch_fail}
	OPTS="$OPTS -c"
%endif
./process_configs.sh $OPTS kernel %{rpmversion}

# end of kernel config
%endif

cd ..
# End of Configs stuff

# get rid of unwanted files resulting from patch fuzz
find . \( -name "*.orig" -o -name "*~" \) -delete >/dev/null

# remove unnecessary SCM files
find . -name .gitignore -delete >/dev/null

cd ..

###
### build
###
%build

%if %{with_sparse}
%define sparse_mflags	C=1
%endif

cp_vmlinux()
{
  eu-strip --remove-comment -o "$2" "$1"
}

# These are for host programs that get built as part of the kernel and
# are required to be packaged in kernel-devel for building external modules.
# Since they are userspace binaries, they are required to pickup the hardening
# flags defined in the macros. The --build-id=uuid is a trick to get around
# debuginfo limitations: Typically, find-debuginfo.sh will update the build
# id of all binaries to allow for parllel debuginfo installs. The kernel
# can't use this because it breaks debuginfo for the vDSO so we have to
# use a special mechanism for kernel and modules to be unique. Unfortunately,
# we still have userspace binaries which need unique debuginfo and because
# they come from the kernel package, we can't just use find-debuginfo.sh to
# rewrite only those binaries. The easiest option right now is just to have
# the build id be a uuid for the host programs.
#
# Note we need to disable these flags for cross builds because the flags
# from redhat-rpm-config assume that host == target so target arch
# flags cause issues with the host compiler.
%if !%{with_cross}
%define build_hostcflags  %{?build_cflags}
%define build_hostldflags %{?build_ldflags} -Wl,--build-id=uuid
%endif

BuildKernel() {
    MakeTarget=$1
    KernelImage=$2
    Flavour=$4
    DoVDSO=$3
    Flav=${Flavour:++${Flavour}}
    InstallName=${5:-vmlinuz}

    # Pick the right config file for the kernel we're building
    Config=kernel-%{version}-%{_target_cpu}${Flavour:+-${Flavour}}.config
    DevelDir=/usr/src/kernels/%{KVERREL}${Flav}

    # When the bootable image is just the ELF kernel, strip it.
    # We already copy the unstripped file into the debuginfo package.
    if [ "$KernelImage" = vmlinux ]; then
      CopyKernel=cp_vmlinux
    else
      CopyKernel=cp
    fi

    KernelVer=%{version}-%{release}.%{_target_cpu}${Flav}
    echo BUILDING A KERNEL FOR ${Flavour} %{_target_cpu}...

    %if 0%{?stable_update}
    # make sure SUBLEVEL is incremented on a stable release.  Sigh 3.x.
    perl -p -i -e "s/^SUBLEVEL.*/SUBLEVEL = %{?stablerev}/" Makefile
    %endif

    # make sure EXTRAVERSION says what we want it to say
    # Trim the release if this is a CI build, since KERNELVERSION is limited to 64 characters
    ShortRel=$(perl -e "print \"%{release}\" =~ s/\.pr\.[0-9A-Fa-f]{32}//r")
    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -${ShortRel}.%{_target_cpu}${Flav}/" Makefile

    # if pre-rc1 devel kernel, must fix up PATCHLEVEL for our versioning scheme
    %if !0%{?rcrev}
    %if 0%{?gitrev}
    perl -p -i -e 's/^PATCHLEVEL.*/PATCHLEVEL = %{upstream_sublevel}/' Makefile
    %endif
    %endif

    # and now to start the build process

    make %{?make_opts} mrproper
    cp configs/$Config .config

    %if %{signkernel}%{signmodules}
    cp %{SOURCE11} certs/.
    %endif

    Arch=`head -1 .config | cut -b 3-`
    echo USING ARCH=$Arch

    make %{?make_opts} HOSTCFLAGS="%{?build_hostcflags}" HOSTLDFLAGS="%{?build_hostldflags}" ARCH=$Arch olddefconfig

    # This ensures build-ids are unique to allow parallel debuginfo
    perl -p -i -e "s/^CONFIG_BUILD_SALT.*/CONFIG_BUILD_SALT=\"%{KVERREL}\"/" .config
    %{make} %{?make_opts} HOSTCFLAGS="%{?build_hostcflags}" HOSTLDFLAGS="%{?build_hostldflags}" ARCH=$Arch %{?_smp_mflags} $MakeTarget %{?sparse_mflags} %{?kernel_mflags}
    %{make} %{?make_opts} HOSTCFLAGS="%{?build_hostcflags}" HOSTLDFLAGS="%{?build_hostldflags}" ARCH=$Arch %{?_smp_mflags} modules %{?sparse_mflags} || exit 1

    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer
%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/%{image_install_path}
%endif

%ifarch %{arm} aarch64
    %{make} %{?make_opts} ARCH=$Arch dtbs dtbs_install INSTALL_DTBS_PATH=$RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer
    cp -r $RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer $RPM_BUILD_ROOT/lib/modules/$KernelVer/dtb
    find arch/$Arch/boot/dts -name '*.dtb' -type f -delete
%endif

    # Start installing the results
    install -m 644 .config $RPM_BUILD_ROOT/boot/config-$KernelVer
    install -m 644 .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/config
    install -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-$KernelVer
    install -m 644 System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/System.map

    # We estimate the size of the initramfs because rpm needs to take this size
    # into consideration when performing disk space calculations. (See bz #530778)
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initramfs-$KernelVer.img bs=1M count=20

    if [ -f arch/$Arch/boot/zImage.stub ]; then
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/%{image_install_path}/zImage.stub-$KernelVer || :
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/lib/modules/$KernelVer/zImage.stub-$KernelVer || :
    fi
    %if %{signkernel}
    # Sign the image if we're using EFI
    %pesign -s -i $KernelImage -o vmlinuz.signed
    if [ ! -s vmlinuz.signed ]; then
        echo "pesigning failed"
        exit 1
    fi
    mv vmlinuz.signed $KernelImage
    %endif
    $CopyKernel $KernelImage \
                $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    chmod 755 $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    cp $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer $RPM_BUILD_ROOT/lib/modules/$KernelVer/$InstallName

    # hmac sign the kernel for FIPS
    echo "Creating hmac file: $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac"
    ls -l $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    sha512hmac $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer | sed -e "s,$RPM_BUILD_ROOT,," > $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac;
    cp $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac $RPM_BUILD_ROOT/lib/modules/$KernelVer/.vmlinuz.hmac

    # Override $(mod-fw) because we don't want it to install any firmware
    # we'll get it from the linux-firmware package and we don't want conflicts
    %{make} %{?make_opts} ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT modules_install KERNELRELEASE=$KernelVer mod-fw=

    # add an a noop %%defattr statement 'cause rpm doesn't like empty file list files
    echo '%%defattr(-,-,-)' > ../kernel${Flavour:+-${Flavour}}-ldsoconf.list
    if [ $DoVDSO -ne 0 ]; then
        %{make} %{?make_opts} ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT vdso_install KERNELRELEASE=$KernelVer
        if [ -s ldconfig-kernel.conf ]; then
            install -D -m 444 ldconfig-kernel.conf \
                $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernel-$KernelVer.conf
            echo /etc/ld.so.conf.d/kernel-$KernelVer.conf >> ../kernel${Flavour:+-${Flavour}}-ldsoconf.list
        fi
        rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/vdso/.build-id
    fi

    # And save the headers/makefiles etc for building modules against
    #
    # This all looks scary, but the end result is supposed to be:
    # * all arch relevant include/ files
    # * all Makefile/Kconfig files
    # * all script/ files

    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/source
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    (cd $RPM_BUILD_ROOT/lib/modules/$KernelVer ; ln -s build source)
    # dirs for additional modules per module-init-tools, kbuild/modules.txt
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/extra
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/updates
    # first copy everything
    cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp Module.symvers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -s Module.markers ]; then
      cp Module.markers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi
    # then drop all but the needed Makefiles/Kconfig files
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Documentation
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    cp .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -f tools/objtool/objtool ]; then
      cp -a tools/objtool/objtool $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools/objtool/ || :
      # these are a few files associated with objtool
      cp -a --parents tools/build/Build.include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
      cp -a --parents tools/build/Build $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
      cp -a --parents tools/build/fixdep.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
      cp -a --parents tools/scripts/utilities.mak $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
      # also more than necessary but it's not that many more files
      cp -a --parents tools/objtool/* $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
      cp -a --parents tools/lib/str_error_r.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
      cp -a --parents tools/lib/string.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
      cp -a --parents tools/lib/subcmd/* $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
    if [ -d arch/$Arch/scripts ]; then
      cp -a arch/$Arch/scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch} || :
    fi
    if [ -f arch/$Arch/*lds ]; then
      cp -a arch/$Arch/*lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch}/ || :
    fi
    if [ -f arch/%{asmarch}/kernel/module.lds ]; then
      cp -a --parents arch/%{asmarch}/kernel/module.lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*.o
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/*/*.o
%ifarch %{power64}
    cp -a --parents arch/powerpc/lib/crtsavres.[So] $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    if [ -d arch/%{asmarch}/include ]; then
      cp -a --parents arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
%ifarch aarch64
    # arch/arm64/include/asm/xen references arch/arm
    cp -a --parents arch/arm/include/asm/xen $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    # arch/arm64/include/asm/opcodes.h references arch/arm
    cp -a --parents arch/arm/include/asm/opcodes.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    # include the machine specific headers for ARM variants, if available.
%ifarch %{arm}
    if [ -d arch/%{asmarch}/mach-${Flavour}/include ]; then
      cp -a --parents arch/%{asmarch}/mach-${Flavour}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
    # include a few files for 'make prepare'
    cp -a --parents arch/arm/tools/gen-mach-types $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/arm/tools/mach-types $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/

%endif
    cp -a include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
%ifarch %{ix86} x86_64
    # files for 'make prepare' to succeed with kernel-devel
    cp -a --parents arch/x86/entry/syscalls/syscall_32.tbl $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/entry/syscalls/syscalltbl.sh $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/entry/syscalls/syscallhdr.sh $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/entry/syscalls/syscall_64.tbl $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs_32.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs_64.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs_common.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    # Yes this is more includes than we probably need. Feel free to sort out
    # dependencies if you so choose.
    cp -a --parents tools/include/* $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/purgatory.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/stack.S $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/string.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/setup-x86_64.S $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/entry64.S $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/boot/string.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/boot/string.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/boot/ctype.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    # Make sure the Makefile and version.h have a matching timestamp so that
    # external modules can be built
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/generated/uapi/linux/version.h

    # Copy .config to include/config/auto.conf so "make prepare" is unnecessary.
    cp $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/.config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/config/auto.conf

%if %{with_debuginfo}
    eu-readelf -n vmlinux | grep "Build ID" | awk '{print $NF}' > vmlinux.id
    cp vmlinux.id $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/vmlinux.id

    #
    # save the vmlinux file for kernel debugging into the kernel-debuginfo rpm
    #
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    cp vmlinux $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
%endif

    find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name "*.ko" -type f >modnames

    # mark modules executable so that strip-to-file can strip them
    xargs --no-run-if-empty chmod u+x < modnames

    # Generate a list of modules for block and networking.

    grep -F /drivers/ modnames | xargs --no-run-if-empty nm -upA |
    sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

    collect_modules_list()
    {
      sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef |
        LC_ALL=C sort -u > $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
      if [ ! -z "$3" ]; then
        sed -r -e "/^($3)\$/d" -i $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
      fi
    }

    collect_modules_list networking \
      'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|rt(l_|2x00)(pci|usb)_probe|register_netdevice'
    collect_modules_list block \
      'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_alloc_queue|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size' 'pktcdvd.ko|dm-mod.ko'
    collect_modules_list drm \
      'drm_open|drm_init'
    collect_modules_list modesetting \
      'drm_crtc_init'

    # detect missing or incorrect license tags
    ( find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name '*.ko' | xargs /sbin/modinfo -l | \
        grep -E -v 'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' ) && exit 1

    # remove files that will be auto generated by depmod at rpm -i time
    pushd $RPM_BUILD_ROOT/lib/modules/$KernelVer/
        rm -f modules.{alias*,builtin.bin,dep*,*map,symbols*,devname,softdep}
    popd

    # Call the modules-extra script to move things around
    %{SOURCE17} $RPM_BUILD_ROOT/lib/modules/$KernelVer %{SOURCE16}

    #
    # Generate the kernel-core and kernel-modules files lists
    #

    # Copy the System.map file for depmod to use, and create a backup of the
    # full module tree so we can restore it after we're done filtering
    cp System.map $RPM_BUILD_ROOT/.
    pushd $RPM_BUILD_ROOT
    mkdir restore
    cp -r lib/modules/$KernelVer/* restore/.

    # don't include anything going into k-m-e in the file lists
    rm -rf lib/modules/$KernelVer/extra

    # Find all the module files and filter them out into the core and modules
    # lists.  This actually removes anything going into -modules from the dir.
    find lib/modules/$KernelVer/kernel -name *.ko | sort -n > modules.list
    cp $RPM_SOURCE_DIR/filter-*.sh .
    %{SOURCE99} modules.list %{_target_cpu}
    rm filter-*.sh

    # Run depmod on the resulting module tree and make sure it isn't broken
    depmod -b . -aeF ./System.map $KernelVer &> depmod.out
    if [ -s depmod.out ]; then
        echo "Depmod failure"
        cat depmod.out
        exit 1
    else
        rm depmod.out
    fi
    # remove files that will be auto generated by depmod at rpm -i time
    pushd $RPM_BUILD_ROOT/lib/modules/$KernelVer/
        rm -f modules.{alias*,builtin.bin,dep*,*map,symbols*,devname,softdep}
    popd

    # Go back and find all of the various directories in the tree.  We use this
    # for the dir lists in kernel-core
    find lib/modules/$KernelVer/kernel -mindepth 1 -type d | sort -n > module-dirs.list

    # Cleanup
    rm System.map
    cp -r restore/* lib/modules/$KernelVer/.
    rm -rf restore
    popd

    # Make sure the files lists start with absolute paths or rpmbuild fails.
    # Also add in the dir entries
    sed -e 's/^lib*/\/lib/' %{?zipsed} $RPM_BUILD_ROOT/k-d.list > ../kernel${Flavour:+-${Flavour}}-modules.list
    sed -e 's/^lib*/%dir \/lib/' %{?zipsed} $RPM_BUILD_ROOT/module-dirs.list > ../kernel${Flavour:+-${Flavour}}-core.list
    sed -e 's/^lib*/\/lib/' %{?zipsed} $RPM_BUILD_ROOT/modules.list >> ../kernel${Flavour:+-${Flavour}}-core.list

    # Cleanup
    rm -f $RPM_BUILD_ROOT/k-d.list
    rm -f $RPM_BUILD_ROOT/modules.list
    rm -f $RPM_BUILD_ROOT/module-dirs.list

%if %{signmodules}
    # Save the signing keys so we can sign the modules in __modsign_install_post
    cp certs/signing_key.pem certs/signing_key.pem.sign${Flav}
    cp certs/signing_key.x509 certs/signing_key.x509.sign${Flav}
%endif

    # Move the devel headers out of the root file system
    mkdir -p $RPM_BUILD_ROOT/usr/src/kernels
    mv $RPM_BUILD_ROOT/lib/modules/$KernelVer/build $RPM_BUILD_ROOT/$DevelDir

    # This is going to create a broken link during the build, but we don't use
    # it after this point.  We need the link to actually point to something
    # when kernel-devel is installed, and a relative link doesn't work across
    # the F17 UsrMove feature.
    ln -sf $DevelDir $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    # prune junk from kernel-devel
    find $RPM_BUILD_ROOT/usr/src/kernels -name ".*.cmd" -delete

    # build a BLS config for this kernel
    %{SOURCE43} "$KernelVer" "$RPM_BUILD_ROOT" "%{?variant}"
}

###
# DO it...
###

# prepare directories
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/boot
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}

cd linux-%{KVERREL}


%if %{with_debug}
BuildKernel %make_target %kernel_image %{_use_vdso} debug
%endif

%if %{with_pae_debug}
BuildKernel %make_target %kernel_image %{use_vdso} %{pae}debug
%endif

%if %{with_pae}
BuildKernel %make_target %kernel_image %{use_vdso} %{pae}
%endif

%if %{with_up}
BuildKernel %make_target %kernel_image %{_use_vdso}
%endif

# In the modsign case, we do 3 things.  1) We check the "flavour" and hard
# code the value in the following invocations.  This is somewhat sub-optimal
# but we're doing this inside of an RPM macro and it isn't as easy as it
# could be because of that.  2) We restore the .tmp_versions/ directory from
# the one we saved off in BuildKernel above.  This is to make sure we're
# signing the modules we actually built/installed in that flavour.  3) We
# grab the arch and invoke mod-sign.sh command to actually sign the modules.
#
# We have to do all of those things _after_ find-debuginfo runs, otherwise
# that will strip the signature off of the modules.

%define __modsign_install_post \
  if [ "%{signmodules}" -eq "1" ]; then \
    if [ "%{with_pae}" -ne "0" ]; then \
      %{modsign_cmd} certs/signing_key.pem.sign+%{pae} certs/signing_key.x509.sign+%{pae} $RPM_BUILD_ROOT/lib/modules/%{KVERREL}+%{pae}/ \
    fi \
    if [ "%{with_debug}" -ne "0" ]; then \
      %{modsign_cmd} certs/signing_key.pem.sign+debug certs/signing_key.x509.sign+debug $RPM_BUILD_ROOT/lib/modules/%{KVERREL}+debug/ \
    fi \
    if [ "%{with_pae_debug}" -ne "0" ]; then \
      %{modsign_cmd} certs/signing_key.pem.sign+%{pae}debug certs/signing_key.x509.sign+%{pae}debug $RPM_BUILD_ROOT/lib/modules/%{KVERREL}+%{pae}debug/ \
    fi \
    if [ "%{with_up}" -ne "0" ]; then \
      %{modsign_cmd} certs/signing_key.pem.sign certs/signing_key.x509.sign $RPM_BUILD_ROOT/lib/modules/%{KVERREL}/ \
    fi \
  fi \
  if [ "%{zipmodules}" -eq "1" ]; then \
    find $RPM_BUILD_ROOT/lib/modules/ -type f -name '*.ko' | xargs xz; \
  fi \
%{nil}

###
### Special hacks for debuginfo subpackages.
###

# This macro is used by %%install, so we must redefine it before that.
%define debug_package %{nil}

%if %{with_debuginfo}

%ifnarch noarch
%global __debug_package 1
%files -f debugfiles.list debuginfo-common-%{_target_cpu}
%endif

%endif

#
# Disgusting hack alert! We need to ensure we sign modules *after* all
# invocations of strip occur, which is in __debug_install_post if
# find-debuginfo.sh runs, and __os_install_post if not.
#
%define __spec_install_post \
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__modsign_install_post}

###
### install
###

%install

cd linux-%{KVERREL}

# We have to do the headers install before the tools install because the
# kernel headers_install will remove any header files in /usr/include that
# it doesn't install itself.

%if %{with_headers}
# Install kernel headers
make ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

find $RPM_BUILD_ROOT/usr/include \
     \( -name .install -o -name .check -o \
        -name ..install.cmd -o -name ..check.cmd \) -delete

%endif

%if %{with_cross_headers}
mkdir -p $RPM_BUILD_ROOT/usr/tmp-headers
make ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr/tmp-headers headers_install_all

find $RPM_BUILD_ROOT/usr/tmp-headers/include \
     \( -name .install -o -name .check -o \
        -name ..install.cmd -o -name ..check.cmd \) -delete

# Copy all the architectures we care about to their respective asm directories
for arch in arm arm64 powerpc s390 x86 ; do
mkdir -p $RPM_BUILD_ROOT/usr/${arch}-linux-gnu/include
mv $RPM_BUILD_ROOT/usr/tmp-headers/include/arch-${arch}/asm $RPM_BUILD_ROOT/usr/${arch}-linux-gnu/include/
cp -a $RPM_BUILD_ROOT/usr/tmp-headers/include/asm-generic $RPM_BUILD_ROOT/usr/${arch}-linux-gnu/include/.
done

# Remove the rest of the architectures
rm -rf $RPM_BUILD_ROOT/usr/tmp-headers/include/arch*
rm -rf $RPM_BUILD_ROOT/usr/tmp-headers/include/asm-*

# Copy the rest of the headers over
for arch in arm arm64 powerpc s390 x86 ; do
cp -a $RPM_BUILD_ROOT/usr/tmp-headers/include/* $RPM_BUILD_ROOT/usr/${arch}-linux-gnu/include/.
done

rm -rf $RPM_BUILD_ROOT/usr/tmp-headers
%endif

###
### clean
###

###
### scripts
###

#
# This macro defines a %%post script for a kernel*-devel package.
#	%%kernel_devel_post [<subpackage>]
#
%define kernel_devel_post() \
%{expand:%%post %{?1:%{1}-}devel}\
if [ -f /etc/sysconfig/kernel ]\
then\
    . /etc/sysconfig/kernel || exit $?\
fi\
if [ "$HARDLINK" != "no" -a -x /usr/sbin/hardlink ]\
then\
    (cd /usr/src/kernels/%{KVERREL}%{?1:+%{1}} &&\
     /usr/bin/find . -type f | while read f; do\
       hardlink -c /usr/src/kernels/*.fc*.*/$f $f\
     done)\
fi\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules-extra package.
# It also defines a %%postun script that does the same thing.
#	%%kernel_modules_extra_post [<subpackage>]
#
%define kernel_modules_extra_post() \
%{expand:%%post %{?1:%{1}-}modules-extra}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules-extra}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules package.
# It also defines a %%postun script that does the same thing.
#	%%kernel_modules_post [<subpackage>]
#
%define kernel_modules_post() \
%{expand:%%post %{?1:%{1}-}modules}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

# This macro defines a %%posttrans script for a kernel package.
#	%%kernel_variant_posttrans [<subpackage>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_posttrans() \
%{expand:%%posttrans %{?1:%{1}-}core}\
/bin/kernel-install add %{KVERREL}%{?1:+%{1}} /lib/modules/%{KVERREL}%{?1:+%{1}}/vmlinuz || exit $?\
%{nil}

#
# This macro defines a %%post script for a kernel package and its devel package.
#	%%kernel_variant_post [-v <subpackage>] [-r <replace>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_post(v:r:) \
%{expand:%%kernel_devel_post %{?-v*}}\
%{expand:%%kernel_modules_post %{?-v*}}\
%{expand:%%kernel_modules_extra_post %{?-v*}}\
%{expand:%%kernel_variant_posttrans %{?-v*}}\
%{expand:%%post %{?-v*:%{-v*}-}core}\
%{-r:\
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ] &&\
   [ -f /etc/sysconfig/kernel ]; then\
  /bin/sed -r -i -e 's/^DEFAULTKERNEL=%{-r*}$/DEFAULTKERNEL=kernel%{?-v:-%{-v*}}/' /etc/sysconfig/kernel || exit $?\
fi}\
%{nil}

#
# This macro defines a %%preun script for a kernel package.
#	%%kernel_variant_preun <subpackage>
#
%define kernel_variant_preun() \
%{expand:%%preun %{?1:%{1}-}core}\
/bin/kernel-install remove %{KVERREL}%{?1:+%{1}} /lib/modules/%{KVERREL}%{?1:+%{1}}/vmlinuz || exit $?\
%{nil}

%kernel_variant_preun
%kernel_variant_post -r kernel-smp

%if %{with_pae}
%kernel_variant_preun %{pae}
%kernel_variant_post -v %{pae} -r (kernel|kernel-smp)

%kernel_variant_post -v %{pae}debug -r (kernel|kernel-smp)
%kernel_variant_preun %{pae}debug
%endif

%kernel_variant_preun debug
%kernel_variant_post -v debug

if [ -x /sbin/ldconfig ]
then
    /sbin/ldconfig -X || exit $?
fi

###
### file lists
###

%if %{with_headers}
%files headers
/usr/include/*
%endif

%if %{with_cross_headers}
%files cross-headers
/usr/*-linux-gnu/include/*
%endif

# empty meta-package
%files
# This is %%{image_install_path} on an arch where that includes ELF files,
# or empty otherwise.
%define elf_image_install_path %{?kernel_image_elf:%{image_install_path}}

#
# This macro defines the %%files sections for a kernel package
# and its devel and debuginfo packages.
#	%%kernel_variant_files [-k vmlinux] <condition> <subpackage>
#
%define kernel_variant_files(k:) \
%if %{2}\
%{expand:%%files -f kernel-%{?3:%{3}-}core.list %{?1:-f kernel-%{?3:%{3}-}ldsoconf.list} %{?3:%{3}-}core}\
%{!?_licensedir:%global license %%doc}\
%license linux-%{KVERREL}/COPYING-%{version}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/%{?-k:%{-k*}}%{!?-k:vmlinuz}\
%ghost /%{image_install_path}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-%{KVERREL}%{?3:+%{3}}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/.vmlinuz.hmac \
%ghost /%{image_install_path}/.vmlinuz-%{KVERREL}%{?3:+%{3}}.hmac \
%ifarch %{arm} aarch64\
/lib/modules/%{KVERREL}%{?3:+%{3}}/dtb \
%ghost /%{image_install_path}/dtb-%{KVERREL}%{?3:+%{3}} \
%endif\
%attr(600,root,root) /lib/modules/%{KVERREL}%{?3:+%{3}}/System.map\
%ghost /boot/System.map-%{KVERREL}%{?3:+%{3}}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/config\
%ghost /boot/config-%{KVERREL}%{?3:+%{3}}\
%ghost /boot/initramfs-%{KVERREL}%{?3:+%{3}}.img\
%dir /lib/modules\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}/kernel\
/lib/modules/%{KVERREL}%{?3:+%{3}}/build\
/lib/modules/%{KVERREL}%{?3:+%{3}}/source\
/lib/modules/%{KVERREL}%{?3:+%{3}}/updates\
/lib/modules/%{KVERREL}%{?3:+%{3}}/bls.conf\
%if %{1}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/vdso\
%endif\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.*\
%{expand:%%files -f kernel-%{?3:%{3}-}modules.list %{?3:%{3}-}modules}\
%{expand:%%files %{?3:%{3}-}devel}\
%defverify(not mtime)\
/usr/src/kernels/%{KVERREL}%{?3:+%{3}}\
%{expand:%%files %{?3:%{3}-}modules-extra}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/extra\
%if %{with_debuginfo}\
%ifnarch noarch\
%{expand:%%files -f debuginfo%{?3}.list %{?3:%{3}-}debuginfo}\
%endif\
%endif\
%if %{?3:1} %{!?3:0}\
%{expand:%%files %{3}}\
%endif\
%endif\
%{nil}

%kernel_variant_files %{_use_vdso} %{with_up}
%kernel_variant_files %{_use_vdso} %{with_debug} debug
%kernel_variant_files %{use_vdso} %{with_pae} %{pae}
%kernel_variant_files %{use_vdso} %{with_pae_debug} %{pae}debug

# plz don't put in a version string unless you're going to tag
# and build.
#
#
%changelog
* Fri Feb 15 2019 Pablo Greco <pablo@fliagreco.com.ar> - 4.19.23-300
- Linux v4.19.23

* Thu Jan 17 2019 Pablo Greco <pablo@fliagreco.com.ar> - 4.19.16-300
- Roll in CentOS Mods
- Add patches for A83T and R40

* Thu Jan 17 2019 Pablo Greco <pablo@fliagreco.com.ar> - 4.19.16-300
- Linux v4.19.16

* Mon Jan 14 2019 Jeremy Cline <jcline@redhat.com> - 4.19.15-300
- Linux v4.19.15
- Fix CVE-2019-3459 and CVE-2019-3460 (rbhz 1663176 1663179 1665925)

* Wed Jan 09 2019 Jeremy Cline <jcline@redhat.com> - 4.19.14-300
- Linux v4.19.14

* Wed Jan 09 2019 Justin M. Forbes <jforbes@fedoraproject.org>
- Fix CVE-2019-3701 (rhbz 1663729 1663730)

* Mon Jan  7 2019 Hans de Goede <hdegoede@redhat.com>
- Add patch to fix bluetooth on RPI 3B+ registering twice (rhbz#1661961)

* Sat Dec 29 2018 Jeremy Cline <jcline@redhat.com> - 4.19.13-300
- Linux v4.19.13

* Thu Dec 27 2018 Hans de Goede <hdegoede@redhat.com>
- Set CONFIG_REALTEK_PHY=y to workaround realtek ethernet issues (rhbz 1650984)

* Mon Dec 24 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.19.12-301
- Another fix for issue affecting Raspberry Pi 3-series WiFi (rhbz 1652093)

* Sat Dec 22 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.19.12-300
- Linux v4.19.12

* Thu Dec 20 2018 Jeremy Cline <jcline@redhat.com> - 4.19.11-300
- Linux v4.19.11

* Mon Dec 17 2018 Jeremy Cline <jcline@redhat.com> - 4.19.10-300
- Linux v4.19.10

* Fri Dec 14 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.19.9-301
- Fix Raspberry Pi issues affecting WiFi (rhbz 1652093)

* Thu Dec 13 2018 Jeremy Cline <jcline@redhat.com> - 4.19.9-300
- Linux v4.19.9

* Tue Dec 11 2018 Hans de Goede <hdegoede@redhat.com>
- Really fix non functional hotkeys on Asus FX503VD (#1645070)

* Mon Dec 10 2018 Jeremy Cline <jcline@redhat.com> - 4.19.8-300
- Linux v4.19.8

* Thu Dec  6 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Fix for ethernet LEDs on Raspberry Pi 3B+

* Wed Dec 05 2018 Jeremy Cline <jcline@redhat.com> - 4.19.7-300
- Linux v4.19.7

* Wed Dec 05 2018 Jeremy Cline <jeremy@jcline.org>
- Fix corruption bug in direct dispatch for blk-mq

* Tue Dec 04 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Fix CVE-2018-19824 (rhbz 1655816 1655817)

* Mon Dec 03 2018 Jeremy Cline <jeremy@jcline.org>
- Fix very quiet speakers on the Thinkpad T570 (rhbz 1554304)

* Mon Dec  3 2018 Hans de Goede <hdegoede@redhat.com>
- Fix non functional hotkeys on Asus FX503VD (#1645070)

* Sun Dec 02 2018 Jeremy Cline <jcline@redhat.com> - 4.19.6-300
- Linux v4.19.6

* Thu Nov 29 2018 Jeremy Cline <jeremy@jcline.org>
- Fix a problem with some rtl8168 chips (rhbz 1650984)
- Fix slowdowns and crashes for AMD GPUs in pre-PCIe-v3 slots

* Tue Nov 27 2018 Jeremy Cline <jcline@redhat.com> - 4.19.5-300
- Linux v4.19.5
- Fix CVE-2018-16862 (rhbz 1649017 1653122)
- Fix CVE-2018-19407 (rhbz 1652656 1652658)

* Mon Nov 26 2018 Jeremy Cline <jeremy@jcline.org>
- Fixes a null pointer dereference with Nvidia and vmwgfx drivers (rhbz 1650224)

* Fri Nov 23 2018 Peter Robinson <pbrobinson@fedoraproject.org> - 4.19.4-300
- Linux v4.19.4

* Thu Nov 22 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Fixes for Rockchips 3399 devices

* Wed Nov 21 2018 Jeremy Cline <jcline@redhat.com> - 4.19.3-300
- Linux v4.19.3

* Tue Nov 20 2018 Hans de Goede <hdegoede@redhat.com>
- Turn on CONFIG_PINCTRL_GEMINILAKE on x86_64 (rhbz#1639155)
- Add a patch fixing touchscreens on HP AMD based laptops (rhbz#1644013)
- Add a patch fixing KIOX010A accelerometers (rhbz#1526312)

* Sat Nov 17 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.19.2-301
- Fix WiFi on Raspberry Pi 3 on aarch64 (rhbz 1649344)
- Fixes for Raspberry Pi hwmon driver and firmware interface

* Fri Nov 16 2018 Hans de Goede <hdegoede@redhat.com>
- Add patches from 4.20 fixing black screen on CHT devices with i915.fastboot=1

* Thu Nov 15 2018 Hans de Goede <hdegoede@redhat.com>
- Add patch fixing touchpads on some Apollo Lake devices not working (#1526312)

* Wed Nov 14 2018 Jeremy Cline <jcline@redhat.com> - 4.19.2-300
- Linux v4.19.2
- Fix CVE-2018-18710 (rhbz 1645140 1648485)

* Mon Nov 12 2018 Laura Abbott <labbott@redhat.com> - 4.18.18-300
- Linux v4.18.18

* Mon Nov 05 2018 Laura Abbott <labbott@redhat.com> - 4.18.17-300
- Linux v4.18.17

* Tue Oct 23 2018 Laura Abbott <labbott@redhat.com>
- Add i915 eDP fixes

* Sat Oct 20 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.18.16-300
- Linux v4.18.16
- Fix network on some i.MX6 devices (rhbz 1628209)

* Thu Oct 18 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.18.15-300
- Linux v4.18.15

* Thu Oct 18 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Add patch to fix mSD on 96boards Hikey

* Tue Oct 16 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Fixes to Rock960 series of devices, improves stability considerably
- Raspberry Pi graphics fix

* Mon Oct 15 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.18.14-300
- Linux v4.18.14

* Fri Oct 12 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Rebase device specific NVRAM files on brcm WiFi devices to latest

* Fri Oct 12 2018 Jeremy Cline <jeremy@jcline.org>
- Fix the microphone on Lenovo G50-30s (rhbz 1249364)

* Wed Oct 10 2018 Laura Abbott <labbott@redhat.com> - 4.18.13-300
- Linux v4.18.13

* Mon Oct 08 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Revert drm/amd/pp: Send khz clock values to DC for smu7/8 (rhbz 1636249)

* Thu Oct 04 2018 Laura Abbott <labbott@redhat.com> - 4.18.12-300
- Linux v4.18.12

* Wed Oct  3 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Fixes for Ampere platforms

* Wed Oct 03 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Fix arm64 kvm priv escalation (rhbz 1635475 1635476)

* Mon Oct 01 2018 Laura Abbott <labbott@redhat.com>
- Disable CONFIG_CRYPTO_DEV_SP_PSP (rhbz 1608242)

* Mon Oct  1 2018 Laura Abbott <labbott@redhat.com>
- Fix for Intel Sensor Hub (rhbz 1634250)

* Mon Oct  1 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.18.11-301
- Support loading device specific NVRAM files on brcm WiFi devices

* Sun Sep 30 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Fixes for AllWinner A64 NICs

* Sun Sep 30 2018 Laura Abbott <labbott@redhat.com> - 4.18.11-300
- Linux v4.18.11

* Wed Sep 26 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Add thermal trip to bcm283x (Raspberry Pi) cpufreq
- Add initial RockPro64 DT support
- Add Pine64-LTS support and some other AllWinner-A64 fixes

* Wed Sep 26 2018 Laura Abbott <labbott@redhat.com> - 4.18.10-300
- Linux v4.18.10

* Wed Sep 26 2018 Laura Abbott <labbott@redhat.com>
- Fix powerpc IPv6 (rhbz 1628394)

* Mon Sep 24 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Fix CVE-2018-14633 (rhbz 1626035 1632185)

* Thu Sep 20 2018 Laura Abbott <labbott@redhat.com> - 4.18.9-300
- Linux v4.18.9
- Fixes CVE-2018-17182 (rhbz 1631205 1631206)

* Sun Sep 16 2018 Laura Abbott <labbott@redhat.com> - 4.18.8-300
- Linux v4.18.8

* Fri Sep 14 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Additional Fixes for CVE-2018-5391 (rhbz 1616059)

* Thu Sep 13 2018 Laura Abbott <labbott@redhat.com>
- Use the CPU RNG for entropy (rhbz 1572944)

* Thu Sep 13 2018 Laura Abbott <labbott@redhat.com>
- HID fixes (rhbz 1627963 1628715)

* Thu Sep 13 2018 Hans de Goede <hdegoede@redhat.com>
- Add patch silencing "EFI stub: UEFI Secure Boot is enabled." at boot

* Mon Sep 10 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Add 96boards rk3399 Ficus and Rock960 support

* Mon Sep 10 2018 Laura Abbott <labbott@redhat.com> - 4.18.7-300
- Linux v4.18.7

* Wed Sep 05 2018 Laura Abbott <labbott@redhat.com> - 4.18.6-300
- Linux v4.18.6

* Fri Aug 24 2018 Laura Abbott <labbott@redhat.com> - 4.18.5-300
- Linux v4.18.5

* Wed Aug 22 2018 Laura Abbott <labbott@redhat.com> - 4.18.4-300
- Linux v4.18.4

* Wed Aug 22 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Re-add mvebu a3700 ATF memory exclusion
- Upstream fix for dwc2 on some ARM platforms

* Mon Aug 20 2018 Laura Abbott <labbott@redhat.com> - 4.18.3-300
- Linux v4.18.3

* Mon Aug 20 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Fix CVE-2018-15471 (rhbz 1610555 1618414)

* Fri Aug 17 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Add fix and re-enable BPF JIT on ARMv7

* Thu Aug 16 2018 Laura Abbott <labbott@redhat.com> - 4.18.1-300
- Linux v4.18.1

* Wed Aug 15 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Drop PPC64 (Big Endian) configs

* Mon Aug 13 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-1
- Linux v4.18
- Disable debugging options.

* Mon Aug 13 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Disable speck crypto cipher

* Sat Aug 11 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Add ZYNQMP clock and firmware driver

* Fri Aug 10 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc8.git2.1
- Linux v4.18-rc8-4-gfedb8da96355

* Fri Aug 10 2018 Hans de Goede <hdegoede@redhat.com>
- Sync FRAMEBUFFER_CONSOLE_DEFERRED_TAKEOVER bugfix with upstream

* Wed Aug 08 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc8.git1.1
- Linux v4.18-rc8-2-g1236568ee3cb

* Wed Aug 08 2018 Laura Abbott <labbott@redhat.com>
- Reenable debugging options.

* Mon Aug 06 2018 Hans de Goede <hdegoede@redhat.com>
- Add one more FRAMEBUFFER_CONSOLE_DEFERRED_TAKEOVER bugfix patch

* Mon Aug 06 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc8.git0.1
- Linux v4.18-rc8

* Mon Aug 06 2018 Laura Abbott <labbott@redhat.com>
- Disable debugging options.

* Sat Aug 04 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc7.git3.1
- Linux v4.18-rc7-178-g0b5b1f9a78b5

* Thu Aug 02 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc7.git2.1
- Linux v4.18-rc7-112-g6b4703768268

* Thu Aug  2 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Add ARM Helios4 support

* Wed Aug 01 2018 Hans de Goede <hdegoede@redhat.com>
- Add patch fixing FRAMEBUFFER_CONSOLE_DEFERRED_TAKEOVER breaking
  VT switching when combined with vgacon (rhbz#1610562)
- Enable Apollo Lake Whiskey Cove PMIC support

* Wed Aug 01 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc7.git1.1
- Linux v4.18-rc7-90-gc1d61e7fe376

* Wed Aug 01 2018 Laura Abbott <labbott@redhat.com>
- Reenable debugging options.

* Wed Aug 01 2018 Jeremy Cline <jeremy@jcline.org>
- Enable AEGIS and MORUS ciphers (rhbz 1610180)

* Tue Jul 31 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Add two bcm283x vc4 stability patches
- Some AllWinner MMC driver fixes

* Tue Jul 31 2018 Hans de Goede <hdegoede@redhat.com>
- Add patch to fix FRAMEBUFFER_CONSOLE_DEFERRED_TAKEOVER on s390x and
  re-enable FRAMEBUFFER_CONSOLE_DEFERRED_TAKEOVER on s390x

* Mon Jul 30 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc7.git0.1
- Linux v4.18-rc7

* Mon Jul 30 2018 Laura Abbott <labbott@redhat.com>
- Disable debugging options.

* Mon Jul 30 2018 Hans de Goede <hdegoede@redhat.com>
- Add patch queued in -next to make quiet more quiet
- Add patches queued in -next to make efifb / fbcon retain the vendor logo
  (ACPI BRGT boot graphics) until the first text is output to the console
- Enable support for ICN8505 touchscreen used on some Cherry Trail tablets

* Fri Jul 27 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Enable FPGA Manager kernel framework

* Fri Jul 27 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc6.git3.1
- Linux v4.18-rc6-152-gcd3f77d74ac3
- Disable headers in preparation for kernel headers split

* Thu Jul 26 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc6.git2.1
- Linux v4.18-rc6-110-g6e77b267723c

* Thu Jul 26 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Add Raspberry Pi voltage sensor driver

* Wed Jul 25 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc6.git1.1
- Linux v4.18-rc6-93-g9981b4fb8684

* Wed Jul 25 2018 Laura Abbott <labbott@redhat.com>
- Reenable debugging options.

* Mon Jul 23 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc6.git0.1
- Linux v4.18-rc6

* Mon Jul 23 2018 Laura Abbott <labbott@redhat.com>
- Disable debugging options.

* Fri Jul 20 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc5.git4.1
- Linux v4.18-rc5-290-g28c20cc73b9c

* Thu Jul 19 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc5.git3.1
- Linux v4.18-rc5-264-gf39f28ff82c1

* Wed Jul 18 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc5.git2.1
- Linux v4.18-rc5-37-g3c53776e29f8

* Tue Jul 17 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc5.git1.1
- Linux v4.18-rc5-36-g30b06abfb92b
- Fix aio uapi breakage (rhbz 1601529)

* Tue Jul 17 2018 Laura Abbott <labbott@redhat.com>
- Reenable debugging options.

* Mon Jul 16 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc5.git0.1
- Linux v4.18-rc5

* Mon Jul 16 2018 Laura Abbott <labbott@redhat.com>
- Disable debugging options.

* Fri Jul 13 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc4.git4.1
- Linux v4.18-rc4-71-g63f047771621

* Thu Jul 12 2018 Laura Abbott <labbott@redhat.com>
- Proper support for parallel debuginfo and hardening flags

* Thu Jul 12 2018 Javier Martinez Canillas <javierm@redhat.com>
- Drop the id field from generated BLS snippets

* Thu Jul 12 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc4.git3.1
- Linux v4.18-rc4-69-gc25c74b7476e

* Wed Jul 11 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc4.git2.1
- Linux v4.18-rc4-17-g1e09177acae3

* Tue Jul 10 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc4.git1.1
- Linux v4.18-rc4-7-g092150a25cb7

* Tue Jul 10 2018 Laura Abbott <labbott@redhat.com>
- Reenable debugging options.

* Mon Jul 09 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc4.git0.1
- Linux v4.18-rc4

* Mon Jul 09 2018 Laura Abbott <labbott@redhat.com>
- Disable debugging options.

* Mon Jul  9 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Add fix for AllWinner A64 timer scew errata

* Fri Jul 06 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc3.git3.1
- Linux v4.18-rc3-183-gc42c12a90545

* Thu Jul 05 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc3.git2.1
- Linux v4.18-rc3-134-g06c85639897c

* Tue Jul 03 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc3.git1.1
- Linux v4.18-rc3-107-gd0fbad0aec1d

* Tue Jul 03 2018 Laura Abbott <labbott@redhat.com>
- Reenable debugging options.

* Mon Jul 02 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc3.git0.1
- Linux v4.18-rc3

* Mon Jul 02 2018 Laura Abbott <labbott@redhat.com>
- Disable debugging options.

* Fri Jun 29 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc2.git4.1
- Linux v4.18-rc2-207-gcd993fc4316d

* Fri Jun 29 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Add a possible i.MX6 sdhci fix

* Thu Jun 28 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc2.git3.1
- Linux v4.18-rc2-132-gf57494321cbf

* Tue Jun 26 2018 Laura Abbott <labbott@redhat.com>
- Enable leds-pca9532 module (rhbz 1595163)

* Tue Jun 26 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc2.git2.1
- Linux v4.18-rc2-44-g813835028e9a

* Mon Jun 25 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc2.git1.1
- Linux v4.18-rc2-37-g6f0d349d922b
- Fix for aarch64 bpf (rhbz 1594447)

* Mon Jun 25 2018 Laura Abbott <labbott@redhat.com>
- Reenable debugging options.

* Mon Jun 25 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc2.git0.1
- Linux v4.18-rc2

* Mon Jun 25 2018 Laura Abbott <labbott@redhat.com>
- Disable debugging options.

* Mon Jun 25 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Disable BFP JIT on ARMv7 as it's currently broken
- Remove forced console on aarch64, legacy config (rhbz 1594402)

* Fri Jun 22 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc1.git4.1
- Linux v4.18-rc1-189-g894b8c000ae6

* Thu Jun 21 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc1.git3.1
- Linux v4.18-rc1-107-g1abd8a8f39cd

* Wed Jun 20 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc1.git2.1
- Linux v4.18-rc1-52-g81e97f01371f

* Tue Jun 19 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc1.git1.1
- Linux v4.18-rc1-43-gba4dbdedd3ed

* Tue Jun 19 2018 Laura Abbott <labbott@redhat.com>
- Reenable debugging options.

* Mon Jun 18 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc1.git0.1
- Linux v4.18-rc1

* Mon Jun 18 2018 Laura Abbott <labbott@redhat.com>
- Disable debugging options.

* Fri Jun 15 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc0.git10.1
- Linux v4.17-12074-g4c5e8fc62d6a

* Fri Jun 15 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- ARM updates for 4.18, cleanup some dropped config options
- Disable zoron driver, moved to staging for removal upstream

* Thu Jun 14 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc0.git9.1
- Linux v4.17-11928-g2837461dbe6f

* Wed Jun 13 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc0.git8.1
- Linux v4.17-11782-gbe779f03d563

* Wed Jun 13 2018 Jeremy Cline <jeremy@jcline.org>
- Fix kexec_file_load pefile signature verification (rhbz 1470995)

* Tue Jun 12 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc0.git7.1
- Linux v4.17-11346-g8efcf34a2639

* Mon Jun 11 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Secure Boot updates

* Mon Jun 11 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc0.git6.1
- Linux v4.17-10288-ga2225d931f75

* Fri Jun 08 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc0.git5.1
- Linux v4.17-7997-g68abbe729567

* Thu Jun 07 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc0.git4.1
- Linux v4.17-6625-g1c8c5a9d38f6

* Wed Jun 06 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc0.git3.1
- Linux v4.17-3754-g135c5504a600

* Tue Jun 05 2018 Jeremy Cline <jeremy@jcline.org>
- Enable CONFIG_SCSI_DH on s390x (rhbz 1586189)

* Tue Jun 05 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc0.git2.1
- Linux v4.17-1535-g5037be168f0e

* Mon Jun 04 2018 Laura Abbott <labbott@redhat.com> - 4.18.0-0.rc0.git1.1
- Linux v4.17-505-g9214407d1237

* Mon Jun 04 2018 Laura Abbott <labbott@redhat.com>
- Reenable debugging options.

* Mon Jun 04 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-1
- Linux v4.17
- Disable debugging options.

* Sun Jun  3 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Initial support for Raspberry Pi cpufreq driver

* Thu May 31 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc7.git2.1
- Linux v4.17-rc7-43-gdd52cb879063

* Wed May 30 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc7.git1.1
- Linux v4.17-rc7-31-g0044cdeb7313
- Reenable debugging options.

* Tue May 29 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc7.git0.1
- Linux v4.17-rc7

* Tue May 29 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Disable debugging options.

* Fri May 25 2018 Jeremy Cline <jcline@redhat.com> - 4.17.0-0.rc6.git3.1
- Linux v4.17-rc6-224-g62d18ecfa641

* Fri May 25 2018 Jeremy Cline <jeremy@jcline.org>
- Fix for incorrect error message about parsing PCCT (rhbz 1435837)

* Thu May 24 2018 Justin M. Forbes <jforbes@redhat.com> - 4.17.0-0.rc6.git2.1
- Linux v4.17-rc6-158-gbee797529d7c
- Reenable debugging options.

* Mon May 21 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc6.git1.1
- Linux v4.17-rc6-146-g5997aab0a11e

* Mon May 21 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc6.git0.1
- Linux v4.17-rc6
- Disable debugging options.

* Sun May 20 2018 Hans de Goede <hdegoede@redhat.com>
- Enable GPIO_AMDPT, PINCTRL_AMD and X86_AMD_PLATFORM_DEVICE Kconfig options
  to fix i2c and GPIOs not working on AMD based laptops (rhbz#1510649)

* Fri May 18 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc5.git3.1
- Linux v4.17-rc5-110-g2c71d338bef2

* Thu May 17 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc5.git2.1
- Linux v4.17-rc5-65-g58ddfe6c3af9

* Tue May 15 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc5.git1.1
- Linux v4.17-rc5-20-g21b9f1c7e319
- Reenable debugging options.

* Mon May 14 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc5.git0.1
- Linux v4.17-rc5

* Mon May 14 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Disable debugging options.

* Fri May 11 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc4.git4.1
- Linux v4.17-rc4-96-g41e3e1082367

* Thu May 10 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Add fix from linux-next for mvebu Armada 8K macbin boot regression

* Thu May 10 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc4.git3.1
- Linux v4.17-rc4-38-g008464a9360e

* Wed May 09 2018 Jeremy Cline <jeremy@jcline.org>
- Workaround for m400 uart irq firmware description (rhbz 1574718)

* Wed May 09 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc4.git2.1
- Linux v4.17-rc4-31-g036db8bd9637

* Tue May 08 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc4.git1.1
- Linux v4.17-rc4-12-gf142f08bf7ec
- Reenable debugging options.

* Mon May 07 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc4.git0.1
- Linux v4.17-rc4

* Mon May 07 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Disable debugging options.

* Sat May  5 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Fix USB-2 on Tegra devices

* Fri May 04 2018 Laura Abbott <labbott@redhat.com>
- Fix for building out of tree modules on powerpc (rhbz 1574604)

* Fri May 04 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc3.git4.1
- Linux v4.17-rc3-148-g625e2001e99e

* Thu May 03 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc3.git3.1
- Linux v4.17-rc3-36-gc15f6d8d4715

* Wed May 02 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc3.git2.1
- Linux v4.17-rc3-13-g2d618bdf7163

* Tue May 01 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc3.git1.1
- Linux v4.17-rc3-5-gfff75eb2a08c
- Reenable debugging options.

* Mon Apr 30 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc3.git0.1
- Linux v4.17-rc3

* Mon Apr 30 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Disable debugging options.

* Fri Apr 27 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc2.git3.1
- Linux v4.17-rc2-155-g0644f186fc9d

* Fri Apr 27 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Enable QLogic NICs on ARM

* Thu Apr 26 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc2.git2.1
- Linux v4.17-rc2-104-g69bfd470f462

* Wed Apr 25 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Add fixes for Marvell a37xx EspressoBin
- Update to latest Raspberry Pi 3+ fixes
- More fixes for lan78xx on the Raspberry Pi 3+

* Tue Apr 24 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc2.git1.1
- Linux v4.17-rc2-58-g24cac7009cb1
- Reenable debugging options.

* Mon Apr 23 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc2.git0.1
- Linux v4.17-rc2

* Mon Apr 23 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Disable debugging options.

* Sun Apr 22 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Add quirk patch to fix X-Gene 1 console on HP m400/Mustang (RHBZ 1531140)

* Fri Apr 20 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc1.git3.1
- Linux v4.17-rc1-93-g43f70c960180

* Thu Apr 19 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc1.git2.1
- Linux v4.17-rc1-28-g87ef12027b9b

* Thu Apr 19 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Enable UFS storage options on ARM

* Wed Apr 18 2018 Justin M. Forbes <jforbes@fedoraproject.org>
- Fix rhbz 1565354

* Tue Apr 17 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Enable drivers for Xilinx ZYMQ-MP Ultra96
- Initial support for PocketBeagle

* Tue Apr 17 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc1.git1.1
- Linux v4.17-rc1-21-ga27fc14219f2
- Reenable debugging options.

* Mon Apr 16 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc1.git0.1
- Linux v4.17-rc1
- Disable debugging options.

* Fri Apr 13 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc0.git9.1
- Linux v4.16-11958-g16e205cf42da

* Thu Apr 12 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc0.git8.1
- Linux v4.16-11766-ge241e3f2bf97

* Thu Apr 12 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Patch to fix nouveau on Tegra platforms
- Enable IOMMU on Exynos now upstream does
- Disable tps65217-charger on BeagleBone to fix USB-OTG port rhbz 1487399
- Add fix for the BeagleBone boot failure
- Further fix for ThunderX ZIP driver

* Wed Apr 11 2018 Laura Abbott <labbott@redhat.com>
- Enable JFFS2 and some MTD modules (rhbz 1474493)
- Enable a few infiniband options (rhbz 1291902)

* Wed Apr 11 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc0.git7.1
- Linux v4.16-11490-gb284d4d5a678

* Tue Apr 10 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc0.git6.1
- Linux v4.16-10929-gc18bb396d3d2

* Mon Apr  9 2018 Peter Robinson <pbrobinson@fedoraproject.org>
- Fixes for Cavium ThunderX ZIP driver stability

* Mon Apr 09 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc0.git5.1
- Linux v4.16-10608-gf8cf2f16a7c9

* Fri Apr 06 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc0.git4.1
- Linux v4.16-9576-g38c23685b273

* Thu Apr 05 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc0.git3.1
- Linux v4.16-7248-g06dd3dfeea60

* Wed Apr 04 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc0.git2.1
- Linux v4.16-5456-g17dec0a94915

* Tue Apr 03 2018 Justin M. Forbes <jforbes@fedoraproject.org> - 4.17.0-0.rc0.git1.1
- Linux v4.16-2520-g642e7fd23353
- Reenable debugging options.

* Mon Apr  2 2018 Peter Robinson <pbrobinson@fedoraproject.org> 4.16.0-2
- Improvements for the Raspberry Pi 3+
- Fixes and minor improvements to Raspberry Pi 2/3

* Mon Apr 02 2018 Jeremy Cline <jeremy@jcline.org> - 4.16.0-1
- Linux v4.16
- Disable debugging options.

###
# The following Emacs magic makes C-c C-e use UTC dates.
# Local Variables:
# rpm-change-log-uses-utc: t
# End:
###
