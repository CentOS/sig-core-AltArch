# Build time setting
%define rhev 0

%bcond_with     guest_agent     # disabled

%global SLOF_gittagdate 20120731

%global have_usbredir 1

%ifarch %{ix86} x86_64
    %global have_seccomp 1
    %global have_spice   1
%else
    %global have_usbredir 0
%endif

%ifnarch s390 s390x %{arm}
    %global have_librdma 1
    %global have_tcmalloc 1
%endif

%ifnarch x86_64
    %global build_only_sub 1
%endif

%ifarch %{ix86}
    %global kvm_target    i386
%endif
%ifarch x86_64
    %global kvm_target    x86_64
%endif
%ifarch %{power64}
    %global kvm_target    ppc64
%endif
%ifarch s390x s390
    %global kvm_target    s390x
%endif
%ifarch ppc
    %global kvm_target    ppc
%endif
%ifarch aarch64
    %global kvm_target    aarch64
%endif
%ifarch %{arm}
    %global kvm_target    arm
%endif

#Versions of various parts:

%define pkgname qemu-kvm
%define rhel_suffix -rhel
%define rhev_suffix -rhev

# Setup for RHEL/RHEV package handling
# We need to define tree suffixes:
# - pkgsuffix:             used for package name
# - extra_provides_suffix: used for dependency checking of other packages
# - conflicts_suffix:      used to prevent installation of both RHEL and RHEV

%if %{rhev}
    %global pkgsuffix %{rhev_suffix}
    %global extra_provides_suffix %{nil}
    %global conflicts_suffix %{rhel_suffix}
    %global obsoletes_version 15:0-0
%else
    %global pkgsuffix %{nil}
    %global extra_provides_suffix %{rhel_suffix}
    %global conflicts_suffix %{rhev_suffix}
%endif

# Macro to properly setup RHEL/RHEV conflict handling
%define rhel_rhev_conflicts()                                         \
Conflicts: %1%{conflicts_suffix}                                      \
Provides: %1%{extra_provides_suffix} = %{epoch}:%{version}-%{release} \
    %if 0%{?obsoletes_version:1}                                          \
Obsoletes: %1 < %{obsoletes_version}                                      \
    %endif

Summary: QEMU is a machine emulator and virtualizer
Name: %{pkgname}%{?pkgsuffix}
Version: 1.5.3
Release: 156%{?dist}.3
# Epoch because we pushed a qemu-1.0 package. AIUI this can't ever be dropped
Epoch: 10
License: GPLv2+ and LGPLv2+ and BSD
Group: Development/Tools
URL: http://www.qemu.org/
ExclusiveArch: x86_64 %{arm}
Requires: seabios-bin >= 1.7.2.2-5
Requires: sgabios-bin
Requires: seavgabios-bin
Requires: ipxe-roms-qemu
Requires: %{pkgname}-common%{?pkgsuffix} = %{epoch}:%{version}-%{release}
        %if 0%{?have_seccomp:1}
Requires: libseccomp >= 1.0.0
        %endif
%if 0%{!?build_only_sub:1}
Requires: glusterfs-api >= 3.6.0
%endif
Requires: libusbx >= 1.0.19
# OOM killer breaks builds with parallel make on s390(x)
%ifarch s390 s390x
    %define _smp_mflags %{nil}
%endif

Source0: http://wiki.qemu-project.org/download/qemu-%{version}.tar.bz2

Source1: qemu.binfmt
# Loads kvm kernel modules at boot
# Not needed anymore - required only for kvm on non i86 archs 
# where we do not ubuild kvm
# Source2: kvm.modules
# Creates /dev/kvm
Source3: 80-kvm.rules
# KSM control scripts
Source4: ksm.service
Source5: ksm.sysconfig
Source6: ksmctl.c
Source7: ksmtuned.service
Source8: ksmtuned
Source9: ksmtuned.conf
Source10: qemu-guest-agent.service
Source11: 99-qemu-guest-agent.rules
Source12: bridge.conf
Source13: qemu-ga.sysconfig
Source14: rhel6-virtio.rom
Source15: rhel6-pcnet.rom
Source16: rhel6-rtl8139.rom
Source17: rhel6-ne2k_pci.rom
Source18: bios-256k.bin
Source19: README.rhel6-gpxe-source
Source20: rhel6-e1000.rom
Source21: sample_images.tar

# libcacard build fixes (heading upstream)
Patch1: 0000-libcacard-fix-missing-symbols-in-libcacard.so.patch

# Fix migration from qemu-kvm 1.2 to qemu 1.3
#Patch3: 0002-Fix-migration-from-qemu-kvm-1.2.patch

# Flow control series
#Patch4: 0100-char-Split-out-tcp-socket-close-code-in-a-separate-f.patch
#Patch5: 0101-char-Add-a-QemuChrHandlers-struct-to-initialise-char.patch
#Patch6: 0102-iohandlers-Add-enable-disable_write_fd_handler-funct.patch
#Patch7: 0103-char-Add-framework-for-a-write-unblocked-callback.patch
#Patch8: 0104-char-Update-send_all-to-handle-nonblocking-chardev-w.patch
#Patch9: 0105-char-Equip-the-unix-tcp-backend-to-handle-nonblockin.patch
#Patch10: 0106-char-Throttle-when-host-connection-is-down.patch
#Patch11: 0107-virtio-console-Enable-port-throttling-when-chardev-i.patch
#Patch12: 0108-spice-qemu-char.c-add-throttling.patch
#Patch13: 0109-spice-qemu-char.c-remove-intermediate-buffer.patch
#Patch14: 0110-usb-redir-Add-flow-control-support.patch
#Patch15: 0111-char-Disable-write-callback-if-throttled-chardev-is-.patch
#Patch16: 0112-hw-virtio-serial-bus-replay-guest-open-on-destinatio.patch

# Migration compatibility
#Patch17: configure-add-enable-migration-from-qemu-kvm.patch
#Patch18: acpi_piix4-condition-on-minimum_version_id.patch
#Patch19: i8254-fix-migration-from-qemu-kvm-1.1.patch
#Patch20: pc_piix-add-compat-handling-for-qemu-kvm-vga-mem-size.patch
#Patch21: qxl-add-rom_size-compat-property.patch
#Patch22: docs-fix-generating-qemu-doc.html-with-texinfo5.patch
#Patch23: rtc-test-Fix-test-failures-with-recent-glib.patch
#Patch24: iscsi-look-for-pkg-config-file-too.patch
#Patch25: tcg-fix-occcasional-tcg-broken-problem.patch
#Patch26: qxl-better-vga-init-in-enter_vga_mode.patch

# Enable/disable supported features
#Patch27: make-usb-devices-configurable.patch
#Patch28: fix-scripts-make_device_config-sh.patch
Patch29: disable-unsupported-usb-devices.patch
Patch30: disable-unsupported-emulated-scsi-devices.patch
Patch31: disable-various-unsupported-devices.patch
Patch32: disable-unsupported-audio-devices.patch
Patch33: disable-unsupported-emulated-network-devices.patch
Patch34: use-kvm-by-default.patch
Patch35: disable-hpet-device.patch
Patch36: rename-man-page-to-qemu-kvm.patch
Patch37: change-path-from-qemu-to-qemu-kvm.patch

# Fix CPUID model/level values on Conroe/Penryn/Nehalem CPU models 
Patch38: pc-replace-upstream-machine-types-by-rhel7-types.patch
Patch39: target-i386-update-model-values-on-conroe-penryn-nehalem-cpu-models.patch
Patch40: target-i386-set-level-4-on-conroe-penryn-nehalem.patch

# RHEL guest( sata disk ) can not boot up (rhbz #981723)
#Patch41: ahci-Fix-FLUSH-command.patch
# Kill the "use flash device for BIOS unless KVM" misfeature (rhbz #963280)
Patch42: pc-Disable-the-use-flash-device-for-BIOS-unless-KVM-misfeature.patch
# Provide RHEL-6 machine types (rhbz #983991)
Patch43: qemu-kvm-Fix-migration-from-older-version-due-to-i8254-changes.patch
Patch44: pc-Add-machine-type-rhel6-0-0.patch
Patch45: pc-Drop-superfluous-RHEL-6-compat_props.patch
Patch46: vga-Default-vram_size_mb-to-16-like-prior-versions-of-RHEL.patch
Patch47: pc-Drop-RHEL-6-USB-device-compat_prop-full-path.patch
Patch48: pc-Drop-RHEL-6-compat_props-virtio-serial-pci-max_ports-vectors.patch
Patch49: pc-Drop-RHEL-6-compat_props-apic-kvm-apic-vapic.patch
Patch50: qxl-set-revision-to-1-for-rhel6-0-0.patch
Patch51: pc-Give-rhel6-0-0-a-kvmclock.patch
Patch52: pc-Add-machine-type-rhel6-1-0.patch
Patch53: pc-Add-machine-type-rhel6-2-0.patch
Patch54: pc-Add-machine-type-rhel6-3-0.patch
Patch55: pc-Add-machine-type-rhel6-4-0.patch
Patch56: pc-Add-machine-type-rhel6-5-0.patch
Patch57: e1000-Keep-capabilities-list-bit-on-for-older-RHEL-machine-types.patch
# Change s3/s4 default to "disable". (rhbz #980840)  
Patch58: misc-disable-s3-s4-by-default.patch
Patch59: pc-rhel6-compat-enable-S3-S4-for-6-1-and-lower-machine-types.patch
# Support Virtual Memory Disk Format in qemu (rhbz #836675)
Patch60: vmdk-Allow-reading-variable-size-descriptor-files.patch
Patch61: vmdk-refuse-to-open-higher-version-than-supported.patch
#Patch62: vmdk-remove-wrong-calculation-of-relative-path.patch
Patch63: block-add-block-driver-read-only-whitelist.patch

# query mem info from monitor would cause qemu-kvm hang [RHEL-7] (rhbz #970047)
Patch64: kvm-char-io_channel_send-don-t-lose-written-bytes.patch
Patch65: kvm-monitor-maintain-at-most-one-G_IO_OUT-watch.patch
# Throttle-down guest to help with live migration convergence (backport to RHEL7.0) (rhbz #985958)
Patch66: kvm-misc-Introduce-async_run_on_cpu.patch
Patch67: kvm-misc-Add-auto-converge-migration-capability.patch
Patch68: kvm-misc-Force-auto-convegence-of-live-migration.patch
# disable (for now) EFI-enabled roms (rhbz #962563)
Patch69: kvm-misc-Disable-EFI-enabled-roms.patch
# qemu-kvm "vPMU passthrough" mode breaks migration, shouldn't be enabled by default (rhbz #853101)
Patch70: kvm-target-i386-Pass-X86CPU-object-to-cpu_x86_find_by_name.patch
Patch71: kvm-target-i386-Disable-PMU-CPUID-leaf-by-default.patch
Patch72: kvm-pc-set-compat-pmu-property-for-rhel6-x-machine-types.patch
# Remove pending watches after virtserialport unplug (rhbz #992900)
# Patch73: kvm-virtio-console-Use-exitfn-for-virtserialport-too.patch
# Containment of error when an SR-IOV device encounters an error... (rhbz #984604)
Patch74: kvm-linux-headers-Update-to-v3-10-rc5.patch
Patch75: kvm-vfio-QEMU-AER-Qemu-changes-to-support-AER-for-VFIO-PCI-devices.patch

# update qemu-ga config & init script in RHEL7 wrt. fsfreeze hook (rhbz 969942)
Patch76: kvm-misc-qga-fsfreeze-main-hook-adapt-to-RHEL-7-RH-only.patch
# RHEL7 does not have equivalent functionality for __com.redhat_qxl_screendump (rhbz 903910)
Patch77: kvm-misc-add-qxl_screendump-monitor-command.patch
# SEP flag behavior for CPU models of RHEL6 machine types should be compatible (rhbz 960216)
Patch78: kvm-pc_piix-disable-CPUID_SEP-for-6-4-0-machine-types-and-below.patch
# crash command can not read the dump-guest-memory file when paging=false [RHEL-7] (rhbz 981582)
Patch79: kvm-dump-Move-stubs-into-libqemustub-a.patch
Patch80: kvm-cpu-Turn-cpu_paging_enabled-into-a-CPUState-hook.patch
Patch81: kvm-memory_mapping-Move-MemoryMappingList-typedef-to-qemu-typedefs-h.patch
Patch82: kvm-cpu-Turn-cpu_get_memory_mapping-into-a-CPUState-hook.patch
Patch83: kvm-dump-Abstract-dump_init-with-cpu_synchronize_all_states.patch
Patch84: kvm-memory_mapping-Improve-qemu_get_guest_memory_mapping-error-reporting.patch
Patch85: kvm-dump-clamp-guest-provided-mapping-lengths-to-ramblock-sizes.patch
Patch86: kvm-dump-introduce-GuestPhysBlockList.patch
Patch87: kvm-dump-populate-guest_phys_blocks.patch
Patch88: kvm-dump-rebase-from-host-private-RAMBlock-offsets-to-guest-physical-addresses.patch
# RHEL 7 qemu-kvm fails to build on F19 host due to libusb deprecated API (rhbz 996469)
Patch89: kvm-usb-host-libusb-Fix-building-with-libusb-git-master-code.patch
# Live migration support in virtio-blk-data-plane (rhbz 995030)
#Patch90: kvm-dataplane-sync-virtio-c-and-vring-c-virtqueue-state.patch
#Patch91: kvm-virtio-clear-signalled_used_valid-when-switching-from-dataplane.patch
#Patch92: kvm-vhost-clear-signalled_used_valid-on-vhost-stop.patch
Patch93: kvm-migration-notify-migration-state-before-starting-thread.patch
Patch94: kvm-dataplane-enable-virtio-blk-x-data-plane-on-live-migration.patch
#Patch95: kvm-dataplane-refuse-to-start-if-device-is-already-in-use.patch
# qemu-img resize can execute successfully even input invalid syntax (rhbz 992935)
Patch96: kvm-qemu-img-Error-out-for-excess-arguments.patch
# For bz#964304 - Windows guest agent service failed to be started
Patch97: kvm-osdep-add-qemu_get_local_state_pathname.patch
# For bz#964304 - Windows guest agent service failed to be started
Patch98: kvm-qga-determine-default-state-dir-and-pidfile-dynamica.patch
# For bz#964304 - Windows guest agent service failed to be started
Patch99: kvm-configure-don-t-save-any-fixed-local_statedir-for-wi.patch
# For bz#964304 - Windows guest agent service failed to be started
Patch100: kvm-qga-create-state-directory-on-win32.patch
# For bz#964304 - Windows guest agent service failed to be started
Patch101: kvm-qga-save-state-directory-in-ga_install_service-RHEL-.patch
# For bz#964304 - Windows guest agent service failed to be started
Patch102: kvm-Makefile-create-.-var-run-when-installing-the-POSIX-.patch
# For bz#980782 - kernel_irqchip defaults to off instead of on without -machine
Patch103: kvm-qemu-option-Fix-qemu_opts_find-for-null-id-arguments.patch
# For bz#980782 - kernel_irqchip defaults to off instead of on without -machine
Patch104: kvm-qemu-option-Fix-qemu_opts_set_defaults-for-corner-ca.patch
# For bz#980782 - kernel_irqchip defaults to off instead of on without -machine
Patch105: kvm-vl-New-qemu_get_machine_opts.patch
# For bz#980782 - kernel_irqchip defaults to off instead of on without -machine
Patch106: kvm-Fix-machine-options-accel-kernel_irqchip-kvm_shadow_.patch
# For bz#980782 - kernel_irqchip defaults to off instead of on without -machine
Patch107: kvm-microblaze-Fix-latent-bug-with-default-DTB-lookup.patch
# For bz#980782 - kernel_irqchip defaults to off instead of on without -machine
Patch108: kvm-Simplify-machine-option-queries-with-qemu_get_machin.patch
# For bz#838170 - Add live migration support for USB [xhci, usb-uas]
Patch109: kvm-pci-add-VMSTATE_MSIX.patch
# For bz#838170 - Add live migration support for USB [xhci, usb-uas]
Patch110: kvm-xhci-add-XHCISlot-addressed.patch
# For bz#838170 - Add live migration support for USB [xhci, usb-uas]
Patch111: kvm-xhci-add-xhci_alloc_epctx.patch
# For bz#838170 - Add live migration support for USB [xhci, usb-uas]
Patch112: kvm-xhci-add-xhci_init_epctx.patch
# For bz#838170 - Add live migration support for USB [xhci, usb-uas]
Patch113: kvm-xhci-add-live-migration-support.patch
# For bz#918907 - provide backwards-compatible RHEL specific machine types in QEMU - CPU features
Patch114: kvm-pc-set-level-xlevel-correctly-on-486-qemu32-CPU-mode.patch
# For bz#918907 - provide backwards-compatible RHEL specific machine types in QEMU - CPU features
Patch115: kvm-pc-Remove-incorrect-rhel6.x-compat-model-value-for-C.patch
# For bz#918907 - provide backwards-compatible RHEL specific machine types in QEMU - CPU features
Patch116: kvm-pc-rhel6.x-has-x2apic-present-on-Conroe-Penryn-Nehal.patch
# For bz#918907 - provide backwards-compatible RHEL specific machine types in QEMU - CPU features
Patch117: kvm-pc-set-compat-CPUID-0x80000001-.EDX-bits-on-Westmere.patch
# For bz#918907 - provide backwards-compatible RHEL specific machine types in QEMU - CPU features
Patch118: kvm-pc-Remove-PCLMULQDQ-from-Westmere-on-rhel6.x-machine.patch
# For bz#918907 - provide backwards-compatible RHEL specific machine types in QEMU - CPU features
Patch119: kvm-pc-SandyBridge-rhel6.x-compat-fixes.patch
# For bz#918907 - provide backwards-compatible RHEL specific machine types in QEMU - CPU features
Patch120: kvm-pc-Haswell-doesn-t-have-rdtscp-on-rhel6.x.patch
# For bz#972433 - "INFO: rcu_sched detected stalls" after RHEL7 kvm vm migrated
Patch121: kvm-i386-fix-LAPIC-TSC-deadline-timer-save-restore.patch
# For bz#996258 - boot guest with maxcpu=255 successfully but actually max number of vcpu is 160
Patch122: kvm-all.c-max_cpus-should-not-exceed-KVM-vcpu-limit.patch
# For bz#906937 - [Hitachi 7.0 FEAT][QEMU]Add a time stamp to error message (*)
Patch123: kvm-add-timestamp-to-error_report.patch
# For bz#906937 - [Hitachi 7.0 FEAT][QEMU]Add a time stamp to error message (*)
Patch124: kvm-Convert-stderr-message-calling-error_get_pretty-to-e.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch125: kvm-block-package-preparation-code-in-qmp_transaction.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch126: kvm-block-move-input-parsing-code-in-qmp_transaction.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch127: kvm-block-package-committing-code-in-qmp_transaction.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch128: kvm-block-package-rollback-code-in-qmp_transaction.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch129: kvm-block-make-all-steps-in-qmp_transaction-as-callback.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch130: kvm-blockdev-drop-redundant-proto_drv-check.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch131: kvm-block-Don-t-parse-protocol-from-file.filename.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch132: kvm-Revert-block-Disable-driver-specific-options-for-1.5.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch133: kvm-qcow2-Add-refcount-update-reason-to-all-callers.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch134: kvm-qcow2-Options-to-enable-discard-for-freed-clusters.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch135: kvm-qcow2-Batch-discards.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch136: kvm-block-Always-enable-discard-on-the-protocol-level.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch137: kvm-qapi.py-Avoid-code-duplication.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch138: kvm-qapi.py-Allow-top-level-type-reference-for-command-d.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch139: kvm-qapi-schema-Use-BlockdevSnapshot-type-for-blockdev-s.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch140: kvm-qapi-types.py-Implement-base-for-unions.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch141: kvm-qapi-visit.py-Split-off-generate_visit_struct_fields.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch142: kvm-qapi-visit.py-Implement-base-for-unions.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch143: kvm-docs-Document-QAPI-union-types.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch144: kvm-qapi-Add-visitor-for-implicit-structs.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch145: kvm-qapi-Flat-unions-with-arbitrary-discriminator.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch146: kvm-qapi-Add-consume-argument-to-qmp_input_get_object.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch147: kvm-qapi.py-Maintain-a-list-of-union-types.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch148: kvm-qapi-qapi-types.py-native-list-support.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch149: kvm-qapi-Anonymous-unions.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch150: kvm-block-Allow-driver-option-on-the-top-level.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch151: kvm-QemuOpts-Add-qemu_opt_unset.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch152: kvm-blockdev-Rename-I-O-throttling-options-for-QMP.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch153: kvm-qemu-iotests-Update-051-reference-output.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch154: kvm-blockdev-Rename-readonly-option-to-read-only.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch155: kvm-blockdev-Split-up-cache-option.patch
# For bz#1005818 - qcow2: Backport discard command line options
Patch156: kvm-qcow2-Use-dashes-instead-of-underscores-in-options.patch
# For bz#1006959 - qemu-iotests false positives
Patch157: kvm-qemu-iotests-filter-QEMU-version-in-monitor-banner.patch
# For bz#1006959 - qemu-iotests false positives
Patch158: kvm-tests-set-MALLOC_PERTURB_-to-expose-memory-bugs.patch
# For bz#1006959 - qemu-iotests false positives
Patch159: kvm-qemu-iotests-Whitespace-cleanup.patch
# For bz#1006959 - qemu-iotests false positives
Patch160: kvm-qemu-iotests-Fixed-test-case-026.patch
# For bz#1006959 - qemu-iotests false positives
Patch161: kvm-qemu-iotests-Fix-test-038.patch
# For bz#1006959 - qemu-iotests false positives
Patch162: kvm-qemu-iotests-Remove-lsi53c895a-tests-from-051.patch
# For bz#974887 - the screen of guest fail to display correctly when use spice + qxl driver
Patch163: kvm-spice-fix-display-initialization.patch
# For bz#921983 - Disable or remove emulated network devices that we will not support
Patch164: kvm-Remove-i82550-network-card-emulation.patch
# For bz#903914 - Disable or remove usb related devices that we will not support
Patch165: kvm-Remove-usb-wacom-tablet.patch
# For bz#903914 - Disable or remove usb related devices that we will not support
Patch166: kvm-Disable-usb-uas.patch
# For bz#947441 - HPET device must be disabled
Patch168: kvm-Remove-no-hpet-option.patch
# For bz#1002286 - Disable or remove device isa-parallel
Patch169: kvm-Disable-isa-parallel.patch
# For bz#949514 - fail to passthrough the USB3.0 stick to windows guest with xHCI controller under pc-i440fx-1.4
Patch170: kvm-xhci-implement-warm-port-reset.patch
# For bz#953304 - Serial number of some USB devices must be fixed for older RHEL machine types
Patch171: kvm-usb-add-serial-bus-property.patch
# For bz#953304 - Serial number of some USB devices must be fixed for older RHEL machine types
Patch172: kvm-rhel6-compat-usb-serial-numbers.patch
# For bz#995866 - fix vmdk support to ESX images
Patch173: kvm-vmdk-fix-comment-for-vmdk_co_write_zeroes.patch
# For bz#1007226 - Introduce bs->zero_beyond_eof
Patch174: kvm-gluster-Add-image-resize-support.patch
# For bz#1007226 - Introduce bs->zero_beyond_eof
Patch175: kvm-block-Introduce-bs-zero_beyond_eof.patch
# For bz#1007226 - Introduce bs->zero_beyond_eof
Patch176: kvm-block-Produce-zeros-when-protocols-reading-beyond-en.patch
# For bz#1007226 - Introduce bs->zero_beyond_eof
Patch177: kvm-gluster-Abort-on-AIO-completion-failure.patch
# For bz#1001131 - Disable or remove device usb-bt-dongle
Patch178: kvm-Preparation-for-usb-bt-dongle-conditional-build.patch
# For bz#1001131 - Disable or remove device usb-bt-dongle
Patch179: kvm-Remove-dev-bluetooth.c-dependency-from-vl.c.patch
# For bz#1009328 - [RFE] Nicer error report when qemu-kvm can't allocate guest RAM
Patch180: kvm-exec-Fix-Xen-RAM-allocation-with-unusual-options.patch
# For bz#1009328 - [RFE] Nicer error report when qemu-kvm can't allocate guest RAM
Patch181: kvm-exec-Clean-up-fall-back-when-mem-path-allocation-fai.patch
# For bz#1009328 - [RFE] Nicer error report when qemu-kvm can't allocate guest RAM
Patch182: kvm-exec-Reduce-ifdeffery-around-mem-path.patch
# For bz#1009328 - [RFE] Nicer error report when qemu-kvm can't allocate guest RAM
Patch183: kvm-exec-Simplify-the-guest-physical-memory-allocation-h.patch
# For bz#1009328 - [RFE] Nicer error report when qemu-kvm can't allocate guest RAM
Patch184: kvm-exec-Drop-incorrect-dead-S390-code-in-qemu_ram_remap.patch
# For bz#1009328 - [RFE] Nicer error report when qemu-kvm can't allocate guest RAM
Patch185: kvm-exec-Clean-up-unnecessary-S390-ifdeffery.patch
# For bz#1009328 - [RFE] Nicer error report when qemu-kvm can't allocate guest RAM
Patch186: kvm-exec-Don-t-abort-when-we-can-t-allocate-guest-memory.patch
# For bz#1009328 - [RFE] Nicer error report when qemu-kvm can't allocate guest RAM
Patch187: kvm-pc_sysfw-Fix-ISA-BIOS-init-for-ridiculously-big-flas.patch
# For bz#903918 - Disable or remove emulated SCSI devices we will not support
Patch188: kvm-virtio-scsi-Make-type-virtio-scsi-common-abstract.patch
# For bz#1009491 - move qga logfiles to new /var/log/qemu-ga/ directory [RHEL-7]
Patch189: kvm-qga-move-logfiles-to-new-directory-for-easier-SELinu.patch
# For bz#918907 - provide backwards-compatible RHEL specific machine types in QEMU - CPU features
Patch190: kvm-target-i386-add-cpu64-rhel6-CPU-model.patch
# For bz#903889 - The value of steal time in "top" command always is "0.0% st" after guest migration
Patch191: kvm-fix-steal-time-MSR-vmsd-callback-to-proper-opaque-ty.patch
# For bz#995866 - fix vmdk support to ESX images
Patch192: kvm-vmdk-Make-VMDK3Header-and-VmdkGrainMarker-QEMU_PACKE.patch
# For bz#995866 - fix vmdk support to ESX images
Patch193: kvm-vmdk-use-unsigned-values-for-on-disk-header-fields.patch
# For bz#995866 - fix vmdk support to ESX images
Patch194: kvm-qemu-iotests-add-poke_file-utility-function.patch
# For bz#995866 - fix vmdk support to ESX images
Patch195: kvm-qemu-iotests-add-empty-test-case-for-vmdk.patch
# For bz#995866 - fix vmdk support to ESX images
Patch196: kvm-vmdk-check-granularity-field-in-opening.patch
# For bz#995866 - fix vmdk support to ESX images
Patch197: kvm-vmdk-check-l2-table-size-when-opening.patch
# For bz#995866 - fix vmdk support to ESX images
Patch198: kvm-vmdk-check-l1-size-before-opening-image.patch
# For bz#995866 - fix vmdk support to ESX images
Patch199: kvm-vmdk-use-heap-allocation-for-whole_grain.patch
# For bz#995866 - fix vmdk support to ESX images
Patch200: kvm-vmdk-rename-num_gtes_per_gte-to-num_gtes_per_gt.patch
# For bz#995866 - fix vmdk support to ESX images
Patch201: kvm-vmdk-Move-l1_size-check-into-vmdk_add_extent.patch
# For bz#995866 - fix vmdk support to ESX images
Patch202: kvm-vmdk-fix-L1-and-L2-table-size-in-vmdk3-open.patch
# For bz#995866 - fix vmdk support to ESX images
Patch203: kvm-vmdk-support-vmfsSparse-files.patch
# For bz#995866 - fix vmdk support to ESX images
Patch204: kvm-vmdk-support-vmfs-files.patch
# For bz#1005036 - When using “-vga qxl” together with “-display vnc=:5” or “-display  sdl” qemu displays  pixel garbage
Patch205: kvm-qxl-fix-local-renderer.patch
# For bz#1008987 - pvticketlocks: add kvm feature kvm_pv_unhalt
Patch206: kvm-linux-headers-update-to-kernel-3.10.0-26.el7.patch
# For bz#1008987 - pvticketlocks: add kvm feature kvm_pv_unhalt
Patch207: kvm-target-i386-add-feature-kvm_pv_unhalt.patch
# For bz#1010881 - backport vcpu soft limit warning
Patch208: kvm-warn-if-num-cpus-is-greater-than-num-recommended.patch
# For bz#1007222 - QEMU core dumped when do hot-unplug virtio serial port during transfer file between host to guest with virtio serial through TCP socket
Patch209: kvm-char-move-backends-io-watch-tag-to-CharDriverState.patch
# For bz#1007222 - QEMU core dumped when do hot-unplug virtio serial port during transfer file between host to guest with virtio serial through TCP socket
Patch210: kvm-char-use-common-function-to-disable-callbacks-on-cha.patch
# For bz#1007222 - QEMU core dumped when do hot-unplug virtio serial port during transfer file between host to guest with virtio serial through TCP socket
Patch211: kvm-char-remove-watch-callback-on-chardev-detach-from-fr.patch
# For bz#1017049 - qemu-img refuses to open the vmdk format image its created
Patch212: kvm-block-don-t-lose-data-from-last-incomplete-sector.patch
# For bz#1017049 - qemu-img refuses to open the vmdk format image its created
Patch213: kvm-vmdk-fix-cluster-size-check-for-flat-extents.patch
# For bz#1017049 - qemu-img refuses to open the vmdk format image its created
Patch214: kvm-qemu-iotests-add-monolithicFlat-creation-test-to-059.patch
# For bz#1001604 - usb hub doesn't work properly (win7 sees downstream port #1 only).
Patch215: kvm-xhci-fix-endpoint-interval-calculation.patch
# For bz#1001604 - usb hub doesn't work properly (win7 sees downstream port #1 only).
Patch216: kvm-xhci-emulate-intr-endpoint-intervals-correctly.patch
# For bz#1001604 - usb hub doesn't work properly (win7 sees downstream port #1 only).
Patch217: kvm-xhci-reset-port-when-disabling-slot.patch
# For bz#1001604 - usb hub doesn't work properly (win7 sees downstream port #1 only).
Patch218: kvm-Revert-usb-hub-report-status-changes-only-once.patch
# For bz#1004290 - Use model 6 for qemu64 and intel cpus
Patch219: kvm-target-i386-Set-model-6-on-qemu64-qemu32-CPU-models.patch
# For bz#918907 - provide backwards-compatible RHEL specific machine types in QEMU - CPU features
Patch220: kvm-pc-rhel6-doesn-t-have-APIC-on-pentium-CPU-models.patch
# For bz#918907 - provide backwards-compatible RHEL specific machine types in QEMU - CPU features
Patch221: kvm-pc-RHEL-6-had-x2apic-set-on-Opteron_G-123.patch
# For bz#918907 - provide backwards-compatible RHEL specific machine types in QEMU - CPU features
Patch222: kvm-pc-RHEL-6-don-t-have-RDTSCP.patch
# For bz#1009285 - -device usb-storage,serial=... crashes with SCSI generic drive
Patch223: kvm-scsi-Fix-scsi_bus_legacy_add_drive-scsi-generic-with.patch
# For bz#1004175 - '-sandbox on'  option  cause  qemu-kvm process hang
Patch224: kvm-seccomp-fine-tuning-whitelist-by-adding-times.patch
# For bz#921465 - Migration can not finished even the "remaining ram" is already 0 kb
Patch225: kvm-block-add-bdrv_write_zeroes.patch
# For bz#921465 - Migration can not finished even the "remaining ram" is already 0 kb
Patch226: kvm-block-raw-add-bdrv_co_write_zeroes.patch
# For bz#921465 - Migration can not finished even the "remaining ram" is already 0 kb
Patch227: kvm-rdma-export-qemu_fflush.patch
# For bz#921465 - Migration can not finished even the "remaining ram" is already 0 kb
Patch228: kvm-block-migration-efficiently-encode-zero-blocks.patch
# For bz#921465 - Migration can not finished even the "remaining ram" is already 0 kb
Patch229: kvm-Fix-real-mode-guest-migration.patch
# For bz#921465 - Migration can not finished even the "remaining ram" is already 0 kb
Patch230: kvm-Fix-real-mode-guest-segments-dpl-value-in-savevm.patch
# For bz#921465 - Migration can not finished even the "remaining ram" is already 0 kb
Patch231: kvm-migration-add-autoconvergence-documentation.patch
# For bz#921465 - Migration can not finished even the "remaining ram" is already 0 kb
Patch232: kvm-migration-send-total-time-in-QMP-at-completed-stage.patch
# For bz#921465 - Migration can not finished even the "remaining ram" is already 0 kb
Patch233: kvm-migration-don-t-use-uninitialized-variables.patch
# For bz#921465 - Migration can not finished even the "remaining ram" is already 0 kb
Patch234: kvm-pc-drop-external-DSDT-loading.patch
# For bz#954195 - RHEL machines <=6.4 should not use mixemu
Patch235: kvm-hda-codec-refactor-common-definitions-into-a-header-.patch
# For bz#954195 - RHEL machines <=6.4 should not use mixemu
Patch236: kvm-hda-codec-make-mixemu-selectable-at-runtime.patch
# For bz#954195 - RHEL machines <=6.4 should not use mixemu
Patch237: kvm-audio-remove-CONFIG_MIXEMU-configure-option.patch
# For bz#954195 - RHEL machines <=6.4 should not use mixemu
Patch238: kvm-pc_piix-disable-mixer-for-6.4.0-machine-types-and-be.patch
# For bz#994414 - hot-unplug chardev with pty backend caused qemu Segmentation fault
Patch239: kvm-chardev-fix-pty_chr_timer.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch240: kvm-qemu-socket-zero-initialize-SocketAddress.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch241: kvm-qemu-socket-drop-pointless-allocation.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch242: kvm-qemu-socket-catch-monitor_get_fd-failures.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch243: kvm-qemu-char-check-optional-fields-using-has_.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch244: kvm-error-add-error_setg_file_open-helper.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch245: kvm-qemu-char-use-more-specific-error_setg_-variants.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch246: kvm-qemu-char-print-notification-to-stderr.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch247: kvm-qemu-char-fix-documentation-for-telnet-wait-socket-f.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch248: kvm-qemu-char-don-t-leak-opts-on-error.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch249: kvm-qemu-char-use-ChardevBackendKind-in-CharDriver.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch250: kvm-qemu-char-minor-mux-chardev-fixes.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch251: kvm-qemu-char-add-chardev-mux-support.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch252: kvm-qemu-char-report-udp-backend-errors.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch253: kvm-qemu-socket-don-t-leak-opts-on-error.patch
# For bz#922010 - RFE: support hotplugging chardev & serial ports
Patch254: kvm-chardev-handle-qmp_chardev_add-KIND_MUX-failure.patch
# For bz#1019474 - RHEL-7 can't load piix4_pm migration section from RHEL-6.5
Patch255: kvm-acpi-piix4-Enable-qemu-kvm-compatibility-mode.patch
# For bz#1004743 - XSAVE migration format not compatible between RHEL6 and RHEL7
Patch256: kvm-target-i386-support-loading-of-cpu-xsave-subsection.patch
# For bz#997817 - -boot order and -boot once regressed since RHEL-6
Patch257: kvm-vl-Clean-up-parsing-of-boot-option-argument.patch
# For bz#997817 - -boot order and -boot once regressed since RHEL-6
Patch258: kvm-qemu-option-check_params-is-now-unused-drop-it.patch
# For bz#997817 - -boot order and -boot once regressed since RHEL-6
Patch259: kvm-vl-Fix-boot-order-and-once-regressions-and-related-b.patch
# For bz#997817 - -boot order and -boot once regressed since RHEL-6
Patch260: kvm-vl-Rename-boot_devices-to-boot_order-for-consistency.patch
# For bz#997817 - -boot order and -boot once regressed since RHEL-6
Patch261: kvm-pc-Make-no-fd-bootchk-stick-across-boot-order-change.patch
# For bz#997817 - -boot order and -boot once regressed since RHEL-6
Patch262: kvm-doc-Drop-ref-to-Bochs-from-no-fd-bootchk-documentati.patch
# For bz#997817 - -boot order and -boot once regressed since RHEL-6
Patch263: kvm-libqtest-Plug-fd-and-memory-leaks-in-qtest_quit.patch
# For bz#997817 - -boot order and -boot once regressed since RHEL-6
Patch264: kvm-libqtest-New-qtest_end-to-go-with-qtest_start.patch
# For bz#997817 - -boot order and -boot once regressed since RHEL-6
Patch265: kvm-qtest-Don-t-reset-on-qtest-chardev-connect.patch
# For bz#997817 - -boot order and -boot once regressed since RHEL-6
Patch266: kvm-boot-order-test-New-covering-just-PC-for-now.patch
# For bz#1019352 - qemu-guest-agent: "guest-fsfreeze-freeze" deadlocks if the guest have mounted disk images
Patch267: kvm-qemu-ga-execute-fsfreeze-freeze-in-reverse-order-of-.patch
# For bz#989608 - [7.0 FEAT] qemu runtime support for librbd backend (ceph)
Patch268: kvm-rbd-link-and-load-librbd-dynamically.patch
# For bz#989608 - [7.0 FEAT] qemu runtime support for librbd backend (ceph)
Patch269: kvm-rbd-Only-look-for-qemu-specific-copy-of-librbd.so.1.patch
# For bz#989677 - [HP 7.0 FEAT]: Increase KVM guest supported memory to 4TiB
Patch270: kvm-seabios-paravirt-allow-more-than-1TB-in-x86-guest.patch
# For bz#1006468 - libiscsi initiator name should use vm UUID
Patch271: kvm-scsi-prefer-UUID-to-VM-name-for-the-initiator-name.patch
# For bz#928867 - Virtual PMU support during live migration - qemu-kvm
Patch272: kvm-target-i386-remove-tabs-from-target-i386-cpu.h.patch
# For bz#928867 - Virtual PMU support during live migration - qemu-kvm
Patch273: kvm-migrate-vPMU-state.patch
# For bz#1009993 - RHEL7 guests do not issue fdatasyncs on virtio-blk
Patch274: kvm-blockdev-do-not-default-cache.no-flush-to-true.patch
# For bz#1009993 - RHEL7 guests do not issue fdatasyncs on virtio-blk
Patch275: kvm-virtio-blk-do-not-relay-a-previous-driver-s-WCE-conf.patch
# For bz#907743 - qemu-ga: empty reason string for OpenFileFailed error
Patch276: kvm-rng-random-use-error_setg_file_open.patch
# For bz#907743 - qemu-ga: empty reason string for OpenFileFailed error
Patch277: kvm-block-mirror_complete-use-error_setg_file_open.patch
# For bz#907743 - qemu-ga: empty reason string for OpenFileFailed error
Patch278: kvm-blockdev-use-error_setg_file_open.patch
# For bz#907743 - qemu-ga: empty reason string for OpenFileFailed error
Patch279: kvm-cpus-use-error_setg_file_open.patch
# For bz#907743 - qemu-ga: empty reason string for OpenFileFailed error
Patch280: kvm-dump-qmp_dump_guest_memory-use-error_setg_file_open.patch
# For bz#907743 - qemu-ga: empty reason string for OpenFileFailed error
Patch281: kvm-savevm-qmp_xen_save_devices_state-use-error_setg_fil.patch
# For bz#907743 - qemu-ga: empty reason string for OpenFileFailed error
Patch282: kvm-block-bdrv_reopen_prepare-don-t-use-QERR_OPEN_FILE_F.patch
# For bz#907743 - qemu-ga: empty reason string for OpenFileFailed error
Patch283: kvm-qerror-drop-QERR_OPEN_FILE_FAILED-macro.patch
# For bz#787463 - disable ivshmem (was: [Hitachi 7.0 FEAT] Support ivshmem (Inter-VM Shared Memory))
Patch284: kvm-rhel-Drop-ivshmem-device.patch
# For bz#1001144 - Disable or remove device usb-host-linux
Patch285: kvm-usb-remove-old-usb-host-code.patch
# For bz#997702 - Migration from RHEL6.5 host to RHEL7.0 host is failed with virtio-net device
Patch286: kvm-Fix-migration-from-rhel6.5-to-rhel7-with-ipxe.patch
# For bz#994490 - Set per-machine-type SMBIOS strings
Patch287: kvm-pc-Don-t-prematurely-explode-QEMUMachineInitArgs.patch
# For bz#994490 - Set per-machine-type SMBIOS strings
Patch288: kvm-pc-Don-t-explode-QEMUMachineInitArgs-into-local-vari.patch
# For bz#994490 - Set per-machine-type SMBIOS strings
Patch289: kvm-smbios-Normalize-smbios_entry_add-s-error-handling-t.patch
# For bz#994490 - Set per-machine-type SMBIOS strings
Patch290: kvm-smbios-Convert-to-QemuOpts.patch
# For bz#994490 - Set per-machine-type SMBIOS strings
Patch291: kvm-smbios-Improve-diagnostics-for-conflicting-entries.patch
# For bz#994490 - Set per-machine-type SMBIOS strings
Patch292: kvm-smbios-Make-multiple-smbios-type-accumulate-sanely.patch
# For bz#994490 - Set per-machine-type SMBIOS strings
Patch293: kvm-smbios-Factor-out-smbios_maybe_add_str.patch
# For bz#994490 - Set per-machine-type SMBIOS strings
Patch294: kvm-hw-Pass-QEMUMachine-to-its-init-method.patch
# For bz#994490 - Set per-machine-type SMBIOS strings
Patch295: kvm-smbios-Set-system-manufacturer-product-version-by-de.patch
# For bz#994490 - Set per-machine-type SMBIOS strings
Patch296: kvm-smbios-Decouple-system-product-from-QEMUMachine.patch
# For bz#994490 - Set per-machine-type SMBIOS strings
Patch297: kvm-rhel-SMBIOS-type-1-branding.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch298: kvm-cow-make-reads-go-at-a-decent-speed.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch299: kvm-cow-make-writes-go-at-a-less-indecent-speed.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch300: kvm-cow-do-not-call-bdrv_co_is_allocated.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch301: kvm-block-keep-bs-total_sectors-up-to-date-even-for-grow.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch302: kvm-block-make-bdrv_co_is_allocated-static.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch303: kvm-block-do-not-use-total_sectors-in-bdrv_co_is_allocat.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch304: kvm-block-remove-bdrv_is_allocated_above-bdrv_co_is_allo.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch305: kvm-block-expect-errors-from-bdrv_co_is_allocated.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch306: kvm-block-Fix-compiler-warning-Werror-uninitialized.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch307: kvm-qemu-img-always-probe-the-input-image-for-allocated-.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch308: kvm-block-make-bdrv_has_zero_init-return-false-for-copy-.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch309: kvm-block-introduce-bdrv_get_block_status-API.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch310: kvm-block-define-get_block_status-return-value.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch311: kvm-block-return-get_block_status-data-and-flags-for-for.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch312: kvm-block-use-bdrv_has_zero_init-to-return-BDRV_BLOCK_ZE.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch313: kvm-block-return-BDRV_BLOCK_ZERO-past-end-of-backing-fil.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch314: kvm-qemu-img-add-a-map-subcommand.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch315: kvm-docs-qapi-document-qemu-img-map.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch316: kvm-raw-posix-return-get_block_status-data-and-flags.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch317: kvm-raw-posix-report-unwritten-extents-as-zero.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch318: kvm-block-add-default-get_block_status-implementation-fo.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch319: kvm-block-look-for-zero-blocks-in-bs-file.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch320: kvm-qemu-img-fix-invalid-JSON.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch321: kvm-block-get_block_status-set-pnum-0-on-error.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch322: kvm-block-get_block_status-avoid-segfault-if-there-is-no.patch
# For bz#989646 - Support backup vendors in qemu to access qcow disk readonly
Patch323: kvm-block-get_block_status-avoid-redundant-callouts-on-r.patch
# For bz#1025740 - Saving VM state on qcow2 images results in VM state corruption
Patch324: kvm-qcow2-Restore-total_sectors-value-in-save_vmstate.patch
# For bz#1025740 - Saving VM state on qcow2 images results in VM state corruption
Patch325: kvm-qcow2-Unset-zero_beyond_eof-in-save_vmstate.patch
# For bz#1025740 - Saving VM state on qcow2 images results in VM state corruption
Patch326: kvm-qemu-iotests-Test-for-loading-VM-state-from-qcow2.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch327: kvm-apic-rename-apic-specific-bitopts.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch328: kvm-hw-import-bitmap-operations-in-qdev-core-header.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch329: kvm-qemu-help-Sort-devices-by-logical-functionality.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch330: kvm-devices-Associate-devices-to-their-logical-category.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch331: kvm-Mostly-revert-qemu-help-Sort-devices-by-logical-func.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch332: kvm-qdev-monitor-Group-device_add-help-and-info-qdm-by-c.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch333: kvm-qdev-Replace-no_user-by-cannot_instantiate_with_devi.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch334: kvm-sysbus-Set-cannot_instantiate_with_device_add_yet.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch335: kvm-cpu-Document-why-cannot_instantiate_with_device_add_.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch336: kvm-apic-Document-why-cannot_instantiate_with_device_add.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch337: kvm-pci-host-Consistently-set-cannot_instantiate_with_de.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch338: kvm-ich9-Document-why-cannot_instantiate_with_device_add.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch339: kvm-piix3-piix4-Clean-up-use-of-cannot_instantiate_with_.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch340: kvm-vt82c686-Clean-up-use-of-cannot_instantiate_with_dev.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch341: kvm-isa-Clean-up-use-of-cannot_instantiate_with_device_a.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch342: kvm-qdev-Do-not-let-the-user-try-to-device_add-when-it-c.patch
# For bz#1001216 - Fix no_user or provide another way make devices unavailable with -device / device_add
Patch343: kvm-rhel-Revert-unwanted-cannot_instantiate_with_device_.patch
# For bz#1001076 - Disable or remove other block devices we won't support
Patch344: kvm-rhel-Revert-downstream-changes-to-unused-default-con.patch
# For bz#1001076 - Disable or remove other block devices we won't support
Patch345: kvm-rhel-Drop-cfi.pflash01-and-isa-ide-device.patch
# For bz#1001088 - Disable or remove display devices we won't support
Patch346: kvm-rhel-Drop-isa-vga-device.patch
# For bz#1001088 - Disable or remove display devices we won't support
Patch347: kvm-rhel-Make-isa-cirrus-vga-device-unavailable.patch
# For bz#1001123 - Disable or remove device ccid-card-emulated
Patch348: kvm-rhel-Make-ccid-card-emulated-device-unavailable.patch
# For bz#1005695 - QEMU should hide CPUID.0Dh values that it does not support
Patch349: kvm-x86-fix-migration-from-pre-version-12.patch
# For bz#1005695 - QEMU should hide CPUID.0Dh values that it does not support
Patch350: kvm-x86-cpuid-reconstruct-leaf-0Dh-data.patch
# For bz#920021 - qemu-kvm segment fault when reboot guest after hot unplug device with option ROM
Patch351: kvm-kvmvapic-Catch-invalid-ROM-size.patch
# For bz#920021 - qemu-kvm segment fault when reboot guest after hot unplug device with option ROM
Patch352: kvm-kvmvapic-Enter-inactive-state-on-hardware-reset.patch
# For bz#920021 - qemu-kvm segment fault when reboot guest after hot unplug device with option ROM
Patch353: kvm-kvmvapic-Clear-also-physical-ROM-address-when-enteri.patch
# For bz#987582 - Initial Virtualization Differentiation for RHEL7 (Live snapshots)
Patch354: kvm-block-optionally-disable-live-block-jobs.patch
# For bz#1022392 - Disable live-storage-migration in qemu-kvm (migrate -b/-i)
Patch355: kvm-migration-disable-live-block-migration-b-i-for-rhel-.patch
# For bz#987583 - Initial Virtualization Differentiation for RHEL7 (Ceph enablement)
Patch356: kvm-Build-ceph-rbd-only-for-rhev.patch
# For bz#1001180 - Disable or remove devices pci-serial-2x, pci-serial-4x
Patch357: kvm-rhel-Make-pci-serial-2x-and-pci-serial-4x-device-una.patch
# For bz#980415 - libusbx: error [_open_sysfs_attr] open /sys/bus/usb/devices/4-1/bConfigurationValue failed ret=-1 errno=2
Patch358: kvm-usb-host-libusb-Fix-reset-handling.patch
# For bz#980383 - The usb3.0 stick can't be returned back to host after shutdown guest with usb3.0 pass-through
Patch359: kvm-usb-host-libusb-Configuration-0-may-be-a-valid-confi.patch
# For bz#980383 - The usb3.0 stick can't be returned back to host after shutdown guest with usb3.0 pass-through
Patch360: kvm-usb-host-libusb-Detach-kernel-drivers-earlier.patch
# For bz#1010858 - Disable unused human monitor commands
Patch361: kvm-monitor-Remove-pci_add-command-for-Red-Hat-Enterpris.patch
# For bz#1010858 - Disable unused human monitor commands
Patch362: kvm-monitor-Remove-pci_del-command-for-Red-Hat-Enterpris.patch
# For bz#1010858 - Disable unused human monitor commands
Patch363: kvm-monitor-Remove-usb_add-del-commands-for-Red-Hat-Ente.patch
# For bz#1010858 - Disable unused human monitor commands
Patch364: kvm-monitor-Remove-host_net_add-remove-for-Red-Hat-Enter.patch
# For bz#990601 - pvpanic device triggers guest bugs when present by default
Patch365: kvm-fw_cfg-add-API-to-find-FW-cfg-object.patch
# For bz#990601 - pvpanic device triggers guest bugs when present by default
Patch366: kvm-pvpanic-use-FWCfgState-explicitly.patch
# For bz#990601 - pvpanic device triggers guest bugs when present by default
Patch367: kvm-pvpanic-initialization-cleanup.patch
# For bz#990601 - pvpanic device triggers guest bugs when present by default
Patch368: kvm-pvpanic-fix-fwcfg-for-big-endian-hosts.patch
# For bz#990601 - pvpanic device triggers guest bugs when present by default
Patch369: kvm-hw-misc-make-pvpanic-known-to-user.patch
# For bz#990601 - pvpanic device triggers guest bugs when present by default
Patch370: kvm-gdbstub-do-not-restart-crashed-guest.patch
# For bz#990601 - pvpanic device triggers guest bugs when present by default
Patch371: kvm-gdbstub-fix-for-commit-87f25c12bfeaaa0c41fb857713bbc.patch
# For bz#990601 - pvpanic device triggers guest bugs when present by default
Patch372: kvm-vl-allow-cont-from-panicked-state.patch
# For bz#990601 - pvpanic device triggers guest bugs when present by default
Patch373: kvm-hw-misc-don-t-create-pvpanic-device-by-default.patch
# For bz#1007176 - Add VPC and VHDX file formats as supported in qemu-kvm (read-only)
Patch374: kvm-block-vhdx-add-migration-blocker.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch375: kvm-block-drop-bs_snapshots-global-variable.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch376: kvm-block-move-snapshot-code-in-block.c-to-block-snapsho.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch377: kvm-block-fix-vvfat-error-path-for-enable_write_target.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch378: kvm-block-Bugfix-format-and-snapshot-used-in-drive-optio.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch379: kvm-iscsi-use-bdrv_new-instead-of-stack-structure.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch380: kvm-qcow2-Add-corrupt-bit.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch381: kvm-qcow2-Metadata-overlap-checks.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch382: kvm-qcow2-Employ-metadata-overlap-checks.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch383: kvm-qcow2-refcount-Move-OFLAG_COPIED-checks.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch384: kvm-qcow2-refcount-Repair-OFLAG_COPIED-errors.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch385: kvm-qcow2-refcount-Repair-shared-refcount-blocks.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch386: kvm-qcow2_check-Mark-image-consistent.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch387: kvm-qemu-iotests-Overlapping-cluster-allocations.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch388: kvm-w32-Fix-access-to-host-devices-regression.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch389: kvm-add-qemu-img-convert-n-option-skip-target-volume-cre.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch390: kvm-bdrv-Use-Error-for-opening-images.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch391: kvm-bdrv-Use-Error-for-creating-images.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch392: kvm-block-Error-parameter-for-open-functions.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch393: kvm-block-Error-parameter-for-create-functions.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch394: kvm-qemu-img-create-Emit-filename-on-error.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch395: kvm-qcow2-Use-Error-parameter.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch396: kvm-qemu-iotests-Adjustments-due-to-error-propagation.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch397: kvm-block-raw-Employ-error-parameter.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch398: kvm-block-raw-win32-Employ-error-parameter.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch399: kvm-blkdebug-Employ-error-parameter.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch400: kvm-blkverify-Employ-error-parameter.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch401: kvm-block-raw-posix-Employ-error-parameter.patch
# For bz#1026524 - Backport block layer error parameter patches
Patch402: kvm-block-raw-win32-Always-use-errno-in-hdev_open.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch403: kvm-qmp-Documentation-for-BLOCK_IMAGE_CORRUPTED.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch404: kvm-qcow2-Correct-snapshots-size-for-overlap-check.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch405: kvm-qcow2-CHECK_OFLAG_COPIED-is-obsolete.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch406: kvm-qcow2-Correct-endianness-in-overlap-check.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch407: kvm-qcow2-Switch-L1-table-in-a-single-sequence.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch408: kvm-qcow2-Use-pread-for-inactive-L1-in-overlap-check.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch409: kvm-qcow2-Remove-wrong-metadata-overlap-check.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch410: kvm-qcow2-Use-negated-overflow-check-mask.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch411: kvm-qcow2-Make-overlap-check-mask-variable.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch412: kvm-qcow2-Add-overlap-check-options.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch413: kvm-qcow2-Array-assigning-options-to-OL-check-bits.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch414: kvm-qcow2-Add-more-overlap-check-bitmask-macros.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch415: kvm-qcow2-Evaluate-overlap-check-options.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch416: kvm-qapi-types.py-Split-off-generate_struct_fields.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch417: kvm-qapi-types.py-Fix-enum-struct-sizes-on-i686.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch418: kvm-qapi-types-visit.py-Pass-whole-expr-dict-for-structs.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch419: kvm-qapi-types-visit.py-Inheritance-for-structs.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch420: kvm-blockdev-Introduce-DriveInfo.enable_auto_del.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch421: kvm-Implement-qdict_flatten.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch422: kvm-blockdev-blockdev-add-QMP-command.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch423: kvm-blockdev-Separate-ID-generation-from-DriveInfo-creat.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch424: kvm-blockdev-Pass-QDict-to-blockdev_init.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch425: kvm-blockdev-Move-parsing-of-media-option-to-drive_init.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch426: kvm-blockdev-Move-parsing-of-if-option-to-drive_init.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch427: kvm-blockdev-Moving-parsing-of-geometry-options-to-drive.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch428: kvm-blockdev-Move-parsing-of-boot-option-to-drive_init.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch429: kvm-blockdev-Move-bus-unit-index-processing-to-drive_ini.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch430: kvm-blockdev-Move-virtio-blk-device-creation-to-drive_in.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch431: kvm-blockdev-Remove-IF_-check-for-read-only-blockdev_ini.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch432: kvm-qemu-iotests-Check-autodel-behaviour-for-device_del.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch433: kvm-blockdev-Remove-media-parameter-from-blockdev_init.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch434: kvm-blockdev-Don-t-disable-COR-automatically-with-blockd.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch435: kvm-blockdev-blockdev_init-error-conversion.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch436: kvm-sd-Avoid-access-to-NULL-BlockDriverState.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch437: kvm-blockdev-fix-cdrom-read_only-flag.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch438: kvm-block-fix-backing-file-overriding.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch439: kvm-block-Disable-BDRV_O_COPY_ON_READ-for-the-backing-fi.patch
# For bz#978402 - [RFE] Add discard support to qemu-kvm layer
Patch440: kvm-block-Don-t-copy-backing-file-name-on-error.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch441: kvm-qemu-iotests-Try-creating-huge-qcow2-image.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch442: kvm-block-move-qmp-and-info-dump-related-code-to-block-q.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch443: kvm-block-dump-snapshot-and-image-info-to-specified-outp.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch444: kvm-block-add-snapshot-info-query-function-bdrv_query_sn.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch445: kvm-block-add-image-info-query-function-bdrv_query_image.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch446: kvm-qmp-add-ImageInfo-in-BlockDeviceInfo-used-by-query-b.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch447: kvm-vmdk-Implement-.bdrv_has_zero_init.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch448: kvm-qemu-iotests-Add-basic-ability-to-use-binary-sample-.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch449: kvm-qemu-iotests-Quote-TEST_IMG-and-TEST_DIR-usage.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch450: kvm-qemu-iotests-fix-test-case-059.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch451: kvm-qapi-Add-ImageInfoSpecific-type.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch452: kvm-block-Add-bdrv_get_specific_info.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch453: kvm-block-qapi-Human-readable-ImageInfoSpecific-dump.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch454: kvm-qcow2-Add-support-for-ImageInfoSpecific.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch455: kvm-qemu-iotests-Discard-specific-info-in-_img_info.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch456: kvm-qemu-iotests-Additional-info-from-qemu-img-info.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch457: kvm-vmdk-convert-error-code-to-use-errp.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch458: kvm-vmdk-refuse-enabling-zeroed-grain-with-flat-images.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch459: kvm-qapi-Add-optional-field-compressed-to-ImageInfo.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch460: kvm-vmdk-Only-read-cid-from-image-file-when-opening.patch
# For bz#980771 - [RFE]  qemu-img should be able to tell the compat version of a qcow2 image
Patch461: kvm-vmdk-Implment-bdrv_get_specific_info.patch
# For bz#1025877 - pci-assign lacks MSI affinity support
Patch462: kvm-pci-assign-Add-MSI-affinity-support.patch
# For bz#1025877 - pci-assign lacks MSI affinity support
Patch463: kvm-Fix-potential-resource-leak-missing-fclose.patch
# For bz#1025877 - pci-assign lacks MSI affinity support
Patch464: kvm-pci-assign-remove-the-duplicate-function-name-in-deb.patch
# For bz#922589 - e1000/rtl8139: qemu mac address can not be changed via set the hardware address in guest
Patch465: kvm-net-update-nic-info-during-device-reset.patch
# For bz#922589 - e1000/rtl8139: qemu mac address can not be changed via set the hardware address in guest
Patch466: kvm-net-e1000-update-network-information-when-macaddr-is.patch
# For bz#922589 - e1000/rtl8139: qemu mac address can not be changed via set the hardware address in guest
Patch467: kvm-net-rtl8139-update-network-information-when-macaddr-.patch
# For bz#1026689 - virtio-net: macaddr is reset but network info of monitor isn't updated
Patch468: kvm-virtio-net-fix-up-HMP-NIC-info-string-on-reset.patch
# For bz#1025477 - VFIO MSI affinity
Patch469: kvm-vfio-pci-VGA-quirk-update.patch
# For bz#1025477 - VFIO MSI affinity
Patch470: kvm-vfio-pci-Add-support-for-MSI-affinity.patch
# For bz#1026550 - QEMU VFIO update ROM loading code
Patch471: kvm-vfio-pci-Test-device-reset-capabilities.patch
# For bz#1026550 - QEMU VFIO update ROM loading code
Patch472: kvm-vfio-pci-Lazy-PCI-option-ROM-loading.patch
# For bz#1026550 - QEMU VFIO update ROM loading code
Patch473: kvm-vfio-pci-Cleanup-error_reports.patch
# For bz#1026550 - QEMU VFIO update ROM loading code
Patch474: kvm-vfio-pci-Add-dummy-PCI-ROM-write-accessor.patch
# For bz#1026550 - QEMU VFIO update ROM loading code
Patch475: kvm-vfio-pci-Fix-endian-issues-in-vfio_pci_size_rom.patch
# For bz#1025472 - Nvidia GPU device assignment - qemu-kvm - bus reset support
Patch476: kvm-linux-headers-Update-to-include-vfio-pci-hot-reset-s.patch
# For bz#1025472 - Nvidia GPU device assignment - qemu-kvm - bus reset support
Patch477: kvm-vfio-pci-Implement-PCI-hot-reset.patch
# For bz#1025474 - Nvidia GPU device assignment - qemu-kvm - NoSnoop support
Patch478: kvm-linux-headers-Update-for-KVM-VFIO-device.patch
# For bz#1025474 - Nvidia GPU device assignment - qemu-kvm - NoSnoop support
Patch479: kvm-vfio-pci-Make-use-of-new-KVM-VFIO-device.patch
# For bz#995866 - fix vmdk support to ESX images
Patch480: kvm-vmdk-Fix-vmdk_parse_extents.patch
# For bz#995866 - fix vmdk support to ESX images
Patch481: kvm-vmdk-fix-VMFS-extent-parsing.patch
# For bz#922589 - e1000/rtl8139: qemu mac address can not be changed via set the hardware address in guest
#Patch482: kvm-e1000-rtl8139-update-HMP-NIC-when-every-bit-is-writt.patch
# Patch 482 removed as it has to be discussed and should not be applied yet
# For bz#1005039 - add compat property to disable ctrl_mac_addr feature
Patch483: kvm-don-t-disable-ctrl_mac_addr-feature-for-6.5-machine-.patch
# For bz#848203 - MAC Programming for virtio over macvtap - qemu-kvm support
Patch484: kvm-qapi-qapi-visit.py-fix-list-handling-for-union-types.patch
# For bz#848203 - MAC Programming for virtio over macvtap - qemu-kvm support
Patch485: kvm-qapi-qapi-visit.py-native-list-support.patch
# For bz#848203 - MAC Programming for virtio over macvtap - qemu-kvm support
Patch486: kvm-qapi-enable-generation-of-native-list-code.patch
# For bz#848203 - MAC Programming for virtio over macvtap - qemu-kvm support
Patch487: kvm-net-add-support-of-mac-programming-over-macvtap-in-Q.patch
# For bz#1029539 - Machine type rhel6.1.0 and  balloon device cause migration fail from RHEL6.5 host to RHEL7.0 host
Patch488: kvm-pc-drop-virtio-balloon-pci-event_idx-compat-property.patch
# For bz#922463 - qemu-kvm core dump when virtio-net multi queue guest hot-unpluging vNIC
Patch489: kvm-virtio-net-only-delete-bh-that-existed.patch
# For bz#1029370 - [whql][netkvm][wlk] Virtio-net device handles RX multicast filtering improperly
Patch490: kvm-virtio-net-broken-RX-filtering-logic-fixed.patch
# For bz#1025138 - Read/Randread/Randrw performance regression
Patch491: kvm-block-Avoid-unecessary-drv-bdrv_getlength-calls.patch
# For bz#1025138 - Read/Randread/Randrw performance regression
Patch492: kvm-block-Round-up-total_sectors.patch
# For bz#1016952 - qemu-kvm man page guide wrong path for qemu-bridge-helper
Patch493: kvm-doc-fix-hardcoded-helper-path.patch
# For bz#971933 - QMP: add RHEL's vendor extension prefix
Patch494: kvm-introduce-RFQDN_REDHAT-RHEL-6-7-fwd.patch
# For bz#971938 - QMP: Add error reason to BLOCK_IO_ERROR event
Patch495: kvm-error-reason-in-BLOCK_IO_ERROR-BLOCK_JOB_ERROR-event.patch
# For bz#895041 - QMP: forward port I/O error debug messages
Patch496: kvm-improve-debuggability-of-BLOCK_IO_ERROR-BLOCK_JOB_ER.patch
# For bz#1029275 - Guest only find one 82576 VF(function 0) while use multifunction
Patch497: kvm-vfio-pci-Fix-multifunction-on.patch
# For bz#1026739 - qcow2: Switch to compat=1.1 default for new images
Patch498: kvm-qcow2-Change-default-for-new-images-to-compat-1.1.patch
# For bz#1026739 - qcow2: Switch to compat=1.1 default for new images
Patch499: kvm-qcow2-change-default-for-new-images-to-compat-1.1-pa.patch
# For bz#1032862 - virtio-rng-egd: repeatedly read same random data-block w/o considering the buffer offset
Patch500: kvm-rng-egd-offset-the-point-when-repeatedly-read-from-t.patch
# For bz#1007334 - CVE-2013-4344 qemu-kvm: qemu: buffer overflow in scsi_target_emulate_report_luns [rhel-7.0]
Patch501: kvm-scsi-Allocate-SCSITargetReq-r-buf-dynamically-CVE-20.patch
# For bz#1033810 - memory leak in using object_get_canonical_path()
Patch502: kvm-virtio-net-fix-the-memory-leak-in-rxfilter_notify.patch
# For bz#1033810 - memory leak in using object_get_canonical_path()
Patch503: kvm-qom-Fix-memory-leak-in-object_property_set_link.patch
# For bz#1036537 - Cross version migration from RHEL6.5 host to RHEL7.0 host with sound device failed.
Patch504: kvm-fix-intel-hda-live-migration.patch
# For bz#1029743 - qemu-kvm core dump after hot plug/unplug 82576 PF about 100 times
Patch505: kvm-vfio-pci-Release-all-MSI-X-vectors-when-disabled.patch
# For bz#921490 - qemu-kvm core dumped after hot plugging more than 11 VF through vfio-pci
Patch506: kvm-Query-KVM-for-available-memory-slots.patch
# For bz#1039501 - [provisioning] discard=on broken
Patch507: kvm-block-Dont-ignore-previously-set-bdrv_flags.patch
# For bz#997832 - Backport trace fixes proactively to avoid confusion and silly conflicts
Patch508: kvm-cleanup-trace-events.pl-New.patch
# For bz#997832 - Backport trace fixes proactively to avoid confusion and silly conflicts
Patch509: kvm-slavio_misc-Fix-slavio_led_mem_readw-_writew-tracepo.patch
# For bz#997832 - Backport trace fixes proactively to avoid confusion and silly conflicts
Patch510: kvm-milkymist-minimac2-Fix-minimac2_read-_write-tracepoi.patch
# For bz#997832 - Backport trace fixes proactively to avoid confusion and silly conflicts
Patch511: kvm-trace-events-Drop-unused-events.patch
# For bz#997832 - Backport trace fixes proactively to avoid confusion and silly conflicts
Patch512: kvm-trace-events-Fix-up-source-file-comments.patch
# For bz#997832 - Backport trace fixes proactively to avoid confusion and silly conflicts
Patch513: kvm-trace-events-Clean-up-with-scripts-cleanup-trace-eve.patch
# For bz#997832 - Backport trace fixes proactively to avoid confusion and silly conflicts
Patch514: kvm-trace-events-Clean-up-after-removal-of-old-usb-host-.patch
# For bz#1027571 - [virtio-win]win8.1 guest network can not resume automatically after do "set_link tap1 on"
Patch515: kvm-net-Update-netdev-peer-on-link-change.patch
# For bz#1003773 - When virtio-blk-pci device with dataplane is failed to be added, the drive cannot be released.
Patch516: kvm-qdev-monitor-Unref-device-when-device_add-fails.patch
# For bz#1003773 - When virtio-blk-pci device with dataplane is failed to be added, the drive cannot be released.
Patch517: kvm-qdev-Drop-misleading-qdev_free-function.patch
# For bz#1003773 - When virtio-blk-pci device with dataplane is failed to be added, the drive cannot be released.
Patch518: kvm-blockdev-fix-drive_init-opts-and-bs_opts-leaks.patch
# For bz#1003773 - When virtio-blk-pci device with dataplane is failed to be added, the drive cannot be released.
Patch519: kvm-libqtest-rename-qmp-to-qmp_discard_response.patch
# For bz#1003773 - When virtio-blk-pci device with dataplane is failed to be added, the drive cannot be released.
Patch520: kvm-libqtest-add-qmp-fmt-.-QDict-function.patch
# For bz#1003773 - When virtio-blk-pci device with dataplane is failed to be added, the drive cannot be released.
Patch521: kvm-blockdev-test-add-test-case-for-drive_add-duplicate-.patch
# For bz#1003773 - When virtio-blk-pci device with dataplane is failed to be added, the drive cannot be released.
Patch522: kvm-qdev-monitor-test-add-device_add-leak-test-cases.patch
# For bz#1003773 - When virtio-blk-pci device with dataplane is failed to be added, the drive cannot be released.
Patch523: kvm-qtest-Use-display-none-by-default.patch
# For bz#1034876 - export acpi tables to guests
Patch524: kvm-range-add-Range-structure.patch
# For bz#1034876 - export acpi tables to guests
Patch525: kvm-range-add-Range-to-typedefs.patch
# For bz#1034876 - export acpi tables to guests
Patch526: kvm-range-add-min-max-operations-on-ranges.patch
# For bz#1034876 - export acpi tables to guests
Patch527: kvm-qdev-Add-SIZE-type-to-qdev-properties.patch
# For bz#1034876 - export acpi tables to guests
Patch528: kvm-qapi-make-visit_type_size-fallback-to-type_int.patch
# For bz#1034876 - export acpi tables to guests
Patch529: kvm-pc-move-IO_APIC_DEFAULT_ADDRESS-to-include-hw-i386-i.patch
# For bz#1034876 - export acpi tables to guests
Patch530: kvm-pci-add-helper-to-retrieve-the-64-bit-range.patch
# For bz#1034876 - export acpi tables to guests
Patch531: kvm-pci-fix-up-w64-size-calculation-helper.patch
# For bz#1034876 - export acpi tables to guests
Patch532: kvm-refer-to-FWCfgState-explicitly.patch
# For bz#1034876 - export acpi tables to guests
Patch533: kvm-fw_cfg-move-typedef-to-qemu-typedefs.h.patch
# For bz#1034876 - export acpi tables to guests
Patch534: kvm-arch_init-align-MR-size-to-target-page-size.patch
# For bz#1034876 - export acpi tables to guests
Patch535: kvm-loader-store-FW-CFG-ROM-files-in-RAM.patch
# For bz#1034876 - export acpi tables to guests
Patch536: kvm-pci-store-PCI-hole-ranges-in-guestinfo-structure.patch
# For bz#1034876 - export acpi tables to guests
Patch537: kvm-pc-pass-PCI-hole-ranges-to-Guests.patch
# For bz#1034876 - export acpi tables to guests
Patch538: kvm-pc-replace-i440fx_common_init-with-i440fx_init.patch
# For bz#1034876 - export acpi tables to guests
Patch539: kvm-pc-don-t-access-fw-cfg-if-NULL.patch
# For bz#1034876 - export acpi tables to guests
Patch540: kvm-pc-add-I440FX-QOM-cast-macro.patch
# For bz#1034876 - export acpi tables to guests
Patch541: kvm-pc-limit-64-bit-hole-to-2G-by-default.patch
# For bz#1034876 - export acpi tables to guests
Patch542: kvm-q35-make-pci-window-address-size-match-guest-cfg.patch
# For bz#1034876 - export acpi tables to guests
Patch543: kvm-q35-use-64-bit-window-programmed-by-guest.patch
# For bz#1034876 - export acpi tables to guests
Patch544: kvm-piix-use-64-bit-window-programmed-by-guest.patch
# For bz#1034876 - export acpi tables to guests
Patch545: kvm-pc-fix-regression-for-64-bit-PCI-memory.patch
# For bz#1034876 - export acpi tables to guests
Patch546: kvm-cleanup-object.h-include-error.h-directly.patch
# For bz#1034876 - export acpi tables to guests
Patch547: kvm-qom-cleanup-struct-Error-references.patch
# For bz#1034876 - export acpi tables to guests
Patch548: kvm-qom-add-pointer-to-int-property-helpers.patch
# For bz#1034876 - export acpi tables to guests
Patch549: kvm-fw_cfg-interface-to-trigger-callback-on-read.patch
# For bz#1034876 - export acpi tables to guests
Patch550: kvm-loader-support-for-unmapped-ROM-blobs.patch
# For bz#1034876 - export acpi tables to guests
Patch551: kvm-pcie_host-expose-UNMAPPED-macro.patch
# For bz#1034876 - export acpi tables to guests
Patch552: kvm-pcie_host-expose-address-format.patch
# For bz#1034876 - export acpi tables to guests
Patch553: kvm-q35-use-macro-for-MCFG-property-name.patch
# For bz#1034876 - export acpi tables to guests
Patch554: kvm-q35-expose-mmcfg-size-as-a-property.patch
# For bz#1034876 - export acpi tables to guests
Patch555: kvm-i386-add-ACPI-table-files-from-seabios.patch
# For bz#1034876 - export acpi tables to guests
Patch556: kvm-acpi-add-rules-to-compile-ASL-source.patch
# For bz#1034876 - export acpi tables to guests
Patch557: kvm-acpi-pre-compiled-ASL-files.patch
# For bz#1034876 - export acpi tables to guests
Patch558: kvm-acpi-ssdt-pcihp-updat-generated-file.patch
# For bz#1034876 - export acpi tables to guests
Patch559: kvm-loader-use-file-path-size-from-fw_cfg.h.patch
# For bz#1034876 - export acpi tables to guests
Patch560: kvm-i386-add-bios-linker-loader.patch
# For bz#1034876 - export acpi tables to guests
Patch561: kvm-loader-allow-adding-ROMs-in-done-callbacks.patch
# For bz#1034876 - export acpi tables to guests
Patch562: kvm-i386-define-pc-guest-info.patch
# For bz#1034876 - export acpi tables to guests
Patch563: kvm-acpi-piix-add-macros-for-acpi-property-names.patch
# For bz#1034876 - export acpi tables to guests
Patch564: kvm-piix-APIs-for-pc-guest-info.patch
# For bz#1034876 - export acpi tables to guests
Patch565: kvm-ich9-APIs-for-pc-guest-info.patch
# For bz#1034876 - export acpi tables to guests
Patch566: kvm-pvpanic-add-API-to-access-io-port.patch
# For bz#1034876 - export acpi tables to guests
Patch567: kvm-hpet-add-API-to-find-it.patch
# For bz#1034876 - export acpi tables to guests
Patch568: kvm-hpet-fix-build-with-CONFIG_HPET-off.patch
# For bz#1034876 - export acpi tables to guests
Patch569: kvm-acpi-add-interface-to-access-user-installed-tables.patch
# For bz#1034876 - export acpi tables to guests
Patch570: kvm-pc-use-new-api-to-add-builtin-tables.patch
# For bz#1034876 - export acpi tables to guests
Patch571: kvm-i386-ACPI-table-generation-code-from-seabios.patch
# For bz#1034876 - export acpi tables to guests
Patch572: kvm-ssdt-fix-PBLK-length.patch
# For bz#1034876 - export acpi tables to guests
Patch573: kvm-ssdt-proc-update-generated-file.patch
# For bz#1034876 - export acpi tables to guests
Patch574: kvm-pc-disable-pci-info.patch
# For bz#1034876 - export acpi tables to guests
Patch575: kvm-acpi-build-fix-build-on-glib-2.22.patch
# For bz#1034876 - export acpi tables to guests
Patch576: kvm-acpi-build-fix-build-on-glib-2.14.patch
# For bz#1034876 - export acpi tables to guests
Patch577: kvm-acpi-build-fix-support-for-glib-2.22.patch
# For bz#1034876 - export acpi tables to guests
Patch578: kvm-acpi-build-Fix-compiler-warning-missing-gnu_printf-f.patch
# For bz#1034876 - export acpi tables to guests
Patch579: kvm-exec-Fix-prototype-of-phys_mem_set_alloc-and-related.patch
# For bz#1034876 - export acpi tables to guests
Patch580: kvm-hw-i386-Makefile.obj-use-PYTHON-to-run-.py-scripts-c.patch
# For bz#1026314
Patch581: kvm-seccomp-add-kill-to-the-syscall-whitelist.patch
Patch582: kvm-json-parser-fix-handling-of-large-whole-number-value.patch
Patch583: kvm-qapi-add-QMP-input-test-for-large-integers.patch
Patch584: kvm-qapi-fix-visitor-serialization-tests-for-numbers-dou.patch
Patch585: kvm-qapi-add-native-list-coverage-for-visitor-serializat.patch
Patch586: kvm-qapi-add-native-list-coverage-for-QMP-output-visitor.patch
Patch587: kvm-qapi-add-native-list-coverage-for-QMP-input-visitor-.patch
Patch588: kvm-qapi-lack-of-two-commas-in-dict.patch
Patch589: kvm-tests-QAPI-schema-parser-tests.patch
Patch590: kvm-tests-Use-qapi-schema-test.json-as-schema-parser-tes.patch
Patch591: kvm-qapi.py-Restructure-lexer-and-parser.patch
Patch592: kvm-qapi.py-Decent-syntax-error-reporting.patch
Patch593: kvm-qapi.py-Reject-invalid-characters-in-schema-file.patch
Patch594: kvm-qapi.py-Fix-schema-parser-to-check-syntax-systematic.patch
Patch595: kvm-qapi.py-Fix-diagnosing-non-objects-at-a-schema-s-top.patch
Patch596: kvm-qapi.py-Rename-expr_eval-to-expr-in-parse_schema.patch
Patch597: kvm-qapi.py-Permit-comments-starting-anywhere-on-the-lin.patch
Patch598: kvm-scripts-qapi.py-Avoid-syntax-not-supported-by-Python.patch
Patch599: kvm-tests-Fix-schema-parser-test-for-in-tree-build.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch600: kvm-add-a-header-file-for-atomic-operations.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch601: kvm-savevm-Fix-potential-memory-leak.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch602: kvm-migration-Fail-migration-on-bdrv_flush_all-error.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch603: kvm-rdma-add-documentation.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch604: kvm-rdma-introduce-qemu_update_position.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch605: kvm-rdma-export-yield_until_fd_readable.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch606: kvm-rdma-export-throughput-w-MigrationStats-QMP.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch607: kvm-rdma-introduce-qemu_file_mode_is_not_valid.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch608: kvm-rdma-introduce-qemu_ram_foreach_block.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch609: kvm-rdma-new-QEMUFileOps-hooks.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch610: kvm-rdma-introduce-capability-x-rdma-pin-all.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch611: kvm-rdma-update-documentation-to-reflect-new-unpin-suppo.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch612: kvm-rdma-bugfix-ram_control_save_page.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch613: kvm-rdma-introduce-ram_handle_compressed.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch614: kvm-rdma-core-logic.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch615: kvm-rdma-send-pc.ram.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch616: kvm-rdma-allow-state-transitions-between-other-states-be.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch617: kvm-rdma-introduce-MIG_STATE_NONE-and-change-MIG_STATE_S.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch618: kvm-rdma-account-for-the-time-spent-in-MIG_STATE_SETUP-t.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch619: kvm-rdma-bugfix-make-IPv6-support-work.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch620: kvm-rdma-forgot-to-turn-off-the-debugging-flag.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch621: kvm-rdma-correct-newlines-in-error-statements.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch622: kvm-rdma-don-t-use-negative-index-to-array.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch623: kvm-rdma-qemu_rdma_post_send_control-uses-wrongly-RDMA_W.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch624: kvm-rdma-use-DRMA_WRID_READY.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch625: kvm-rdma-memory-leak-RDMAContext-host.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch626: kvm-rdma-use-resp.len-after-validation-in-qemu_rdma_regi.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch627: kvm-rdma-validate-RDMAControlHeader-len.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch628: kvm-rdma-check-if-RDMAControlHeader-len-match-transferre.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch629: kvm-rdma-proper-getaddrinfo-handling.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch630: kvm-rdma-IPv6-over-Ethernet-RoCE-is-broken-in-linux-work.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch631: kvm-rdma-remaining-documentation-fixes.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch632: kvm-rdma-silly-ipv6-bugfix.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch633: kvm-savevm-fix-wrong-initialization-by-ram_control_load_.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch634: kvm-arch_init-right-return-for-ram_save_iterate.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch635: kvm-rdma-clean-up-of-qemu_rdma_cleanup.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch636: kvm-rdma-constify-ram_chunk_-index-start-end.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch637: kvm-migration-Fix-debug-print-type.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch638: kvm-arch_init-make-is_zero_page-accept-size.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch639: kvm-migration-ram_handle_compressed.patch
# For bz#1011720 - [HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM
Patch640: kvm-migration-fix-spice-migration.patch
# For bz#678368 - RFE: Support more than 8 assigned devices
Patch641: kvm-pci-assign-cap-number-of-devices-that-can-be-assigne.patch
# For bz#678368 - RFE: Support more than 8 assigned devices
Patch642: kvm-vfio-cap-number-of-devices-that-can-be-assigned.patch
# For bz#1039513 - backport remote wakeup for ehci
Patch643: kvm-Revert-usb-tablet-Don-t-claim-wakeup-capability-for-.patch
# For bz#1026554 - qemu: mempath: prefault pages manually
Patch644: kvm-mempath-prefault-pages-manually-v4.patch
# For bz#1007710 - [RFE] Enable qemu-img to support VMDK version 3
# For bz#1029852 - qemu-img fails to convert vmdk image with "qemu-img: Could not open 'image.vmdk'"
Patch645: kvm-vmdk-Allow-read-only-open-of-VMDK-version-3.patch
# For bz#1035132 - fail to boot and call trace with x-data-plane=on specified for rhel6.5 guest
Patch646: kvm-virtio_pci-fix-level-interrupts-with-irqfd.patch
# For bz#889051 - Commands "__com.redhat_drive_add/del" don' t exist in RHEL7.0
Patch647: kvm-QMP-Forward-port-__com.redhat_drive_del-from-RHEL-6.patch
# For bz#889051 - Commands "__com.redhat_drive_add/del" don' t exist in RHEL7.0
Patch648: kvm-QMP-Forward-port-__com.redhat_drive_add-from-RHEL-6.patch
# For bz#889051 - Commands "__com.redhat_drive_add/del" don' t exist in RHEL7.0
Patch649: kvm-HMP-Forward-port-__com.redhat_drive_add-from-RHEL-6.patch
# For bz#889051 - Commands "__com.redhat_drive_add/del" don' t exist in RHEL7.0
Patch650: kvm-QMP-Document-throttling-parameters-of-__com.redhat_d.patch
# For bz#889051 - Commands "__com.redhat_drive_add/del" don' t exist in RHEL7.0
Patch651: kvm-HMP-Disable-drive_add-for-Red-Hat-Enterprise-Linux.patch
Patch652: kvm-Revert-HMP-Disable-drive_add-for-Red-Hat-Enterprise-2.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch653: kvm-block-change-default-of-.has_zero_init-to-0.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch654: kvm-iscsi-factor-out-sector-conversions.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch655: kvm-iscsi-add-logical-block-provisioning-information-to-.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch656: kvm-iscsi-add-.bdrv_get_block_status.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch657: kvm-iscsi-split-discard-requests-in-multiple-parts.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch658: kvm-block-make-BdrvRequestFlags-public.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch659: kvm-block-add-flags-to-bdrv_-_write_zeroes.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch660: kvm-block-introduce-BDRV_REQ_MAY_UNMAP-request-flag.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch661: kvm-block-add-logical-block-provisioning-info-to-BlockDr.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch662: kvm-block-add-wrappers-for-logical-block-provisioning-in.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch663: kvm-block-iscsi-add-.bdrv_get_info.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch664: kvm-block-add-BlockLimits-structure-to-BlockDriverState.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch665: kvm-block-raw-copy-BlockLimits-on-raw_open.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch666: kvm-block-honour-BlockLimits-in-bdrv_co_do_write_zeroes.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch667: kvm-block-honour-BlockLimits-in-bdrv_co_discard.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch668: kvm-iscsi-set-limits-in-BlockDriverState.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch669: kvm-iscsi-simplify-iscsi_co_discard.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch670: kvm-iscsi-add-bdrv_co_write_zeroes.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch671: kvm-block-introduce-bdrv_make_zero.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch672: kvm-block-get_block_status-fix-BDRV_BLOCK_ZERO-for-unall.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch673: kvm-qemu-img-add-support-for-fully-allocated-images.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch674: kvm-qemu-img-conditionally-zero-out-target-on-convert.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch675: kvm-block-generalize-BlockLimits-handling-to-cover-bdrv_.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch676: kvm-block-add-flags-to-BlockRequest.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch677: kvm-block-add-flags-argument-to-bdrv_co_write_zeroes-tra.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch678: kvm-block-add-bdrv_aio_write_zeroes.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch679: kvm-block-handle-ENOTSUP-from-discard-in-generic-code.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch680: kvm-block-make-bdrv_co_do_write_zeroes-stricter-in-produ.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch681: kvm-vpc-vhdx-add-get_info.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch682: kvm-block-drivers-add-discard-write_zeroes-properties-to.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch683: kvm-block-drivers-expose-requirement-for-write-same-alig.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch684: kvm-block-iscsi-remove-.bdrv_has_zero_init.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch685: kvm-block-iscsi-updated-copyright.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch686: kvm-block-iscsi-check-WRITE-SAME-support-differently-dep.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch687: kvm-scsi-disk-catch-write-protection-errors-in-UNMAP.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch688: kvm-scsi-disk-reject-ANCHOR-1-for-UNMAP-and-WRITE-SAME-c.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch689: kvm-scsi-disk-correctly-implement-WRITE-SAME.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch690: kvm-scsi-disk-fix-WRITE-SAME-with-large-non-zero-payload.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch691: kvm-raw-posix-implement-write_zeroes-with-MAY_UNMAP-for-.patch.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch692: kvm-raw-posix-implement-write_zeroes-with-MAY_UNMAP-for-.patch.patch.patch.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch693: kvm-raw-posix-add-support-for-write_zeroes-on-XFS-and-bl.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch694: kvm-qemu-iotests-033-is-fast.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch695: kvm-qemu-img-add-support-for-skipping-zeroes-in-input-du.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch696: kvm-qemu-img-fix-usage-instruction-for-qemu-img-convert.patch.patch
# For bz#1007815 - fix WRITE SAME support
Patch697: kvm-block-iscsi-set-bdi-cluster_size.patch.patch
# For bz#1039557 - optimize qemu-img for thin provisioned images
Patch698: kvm-block-add-opt_transfer_length-to-BlockLimits.patch.patch
# For bz#1039557 - optimize qemu-img for thin provisioned images
Patch699: kvm-block-iscsi-set-bs-bl.opt_transfer_length.patch.patch
# For bz#1039557 - optimize qemu-img for thin provisioned images
Patch700: kvm-qemu-img-dynamically-adjust-iobuffer-size-during-con.patch.patch
# For bz#1039557 - optimize qemu-img for thin provisioned images
Patch701: kvm-qemu-img-round-down-request-length-to-an-aligned-sec.patch.patch
# For bz#1039557 - optimize qemu-img for thin provisioned images
Patch702: kvm-qemu-img-decrease-progress-update-interval-on-conver.patch.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch703: kvm-block-qemu-iotests-for-vhdx-read-sample-dynamic-imag.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch704: kvm-block-qemu-iotests-add-quotes-to-TEST_IMG-usage-io-p.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch705: kvm-block-qemu-iotests-fix-_make_test_img-to-work-with-s.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch706: kvm-block-qemu-iotests-add-quotes-to-TEST_IMG.base-usage.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch707: kvm-block-qemu-iotests-add-quotes-to-TEST_IMG-usage-in-0.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch708: kvm-block-qemu-iotests-removes-duplicate-double-quotes-i.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch709: kvm-block-vhdx-minor-comments-and-typo-correction.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch710: kvm-block-vhdx-add-header-update-capability.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch711: kvm-block-vhdx-code-movement-VHDXMetadataEntries-and-BDR.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch712: kvm-block-vhdx-log-support-struct-and-defines.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch713: kvm-block-vhdx-break-endian-translation-functions-out.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch714: kvm-block-vhdx-update-log-guid-in-header-and-first-write.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch715: kvm-block-vhdx-code-movement-move-vhdx_close-above-vhdx_.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch716: kvm-block-vhdx-log-parsing-replay-and-flush-support.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch717: kvm-block-vhdx-add-region-overlap-detection-for-image-fi.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch718: kvm-block-vhdx-add-log-write-support.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch719: kvm-block-vhdx-write-support.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch720: kvm-block-vhdx-remove-BAT-file-offset-bit-shifting.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch721: kvm-block-vhdx-move-more-endian-translations-to-vhdx-end.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch722: kvm-block-vhdx-break-out-code-operations-to-functions.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch723: kvm-block-vhdx-fix-comment-typos-in-header-fix-incorrect.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch724: kvm-block-vhdx-add-.bdrv_create-support.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch725: kvm-block-vhdx-update-_make_test_img-to-filter-out-vhdx-.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch726: kvm-block-qemu-iotests-for-vhdx-add-write-test-support.patch
# For bz#879234 - [RFE] qemu-img: Add/improve support for VHDX format
Patch727: kvm-block-vhdx-qemu-iotest-log-replay-of-data-sector.patch
# For bz#965636 - streaming with no backing file should not do anything
Patch728: kvm-block-stream-Don-t-stream-unbacked-devices.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch729: kvm-qemu-io-Let-open-pass-options-to-block-driver.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch730: kvm-qcow2.py-Subcommand-for-changing-header-fields.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch731: kvm-qemu-iotests-Remaining-error-propagation-adjustments.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch732: kvm-qemu-iotests-Add-test-for-inactive-L2-overlap.patch
# For bz#1004347 - Backport qcow2 corruption prevention patches
Patch733: kvm-qemu-iotests-Adjust-test-result-039.patch
# For bz#1048671 - virtio-net: mac_table change isn't recovered in error state
Patch734: kvm-virtio-net-don-t-update-mac_table-in-error-state.patch
# For bz#1032904 - qemu-img can not create libiscsi qcow2_v3 image
Patch735: kvm-qcow2-Zero-initialise-first-cluster-for-new-images.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch736: kvm-option-Add-assigned-flag-to-QEMUOptionParameter.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch737: kvm-qcow2-refcount-Snapshot-update-for-zero-clusters.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch738: kvm-qemu-iotests-Snapshotting-zero-clusters.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch739: kvm-block-Image-file-option-amendment.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch740: kvm-qcow2-cache-Empty-cache.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch741: kvm-qcow2-cluster-Expand-zero-clusters.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch742: kvm-qcow2-Save-refcount-order-in-BDRVQcowState.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch743: kvm-qcow2-Implement-bdrv_amend_options.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch744: kvm-qcow2-Correct-bitmap-size-in-zero-expansion.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch745: kvm-qcow2-Free-only-newly-allocated-clusters-on-error.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch746: kvm-qcow2-Add-missing-space-in-error-message.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch747: kvm-qemu-iotest-qcow2-image-option-amendment.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch748: kvm-qemu-iotests-New-test-case-in-061.patch
# For bz#1033490 - Cannot upgrade/downgrade qcow2 images
Patch749: kvm-qemu-iotests-Preallocated-zero-clusters-in-061.patch
# For bz#972773 - RHEL7: Clarify support statement in KVM help
Patch750: kvm-Add-support-statement-to-help-output.patch
# For bz#903910 - RHEL7 does not have equivalent functionality for __com.redhat_qxl_screendump
Patch751: kvm-__com.redhat_qxl_screendump-add-docs.patch
# For bz#999836 - -m 1 crashes
Patch752: kvm-vl-Round-memory-sizes-below-2MiB-up-to-2MiB.patch
# For bz#1044845 - QEMU seccomp sandbox - exit if seccomp_init() fails
Patch753: kvm-seccomp-exit-if-seccomp_init-fails.patch
# For bz#1034876 - export acpi tables to guests
Patch754: kvm-configure-make-iasl-option-actually-work.patch
# For bz#1034876 - export acpi tables to guests
Patch755: kvm-acpi-build-disable-with-no-acpi.patch
# For bz#1039513 - backport remote wakeup for ehci
Patch756: kvm-ehci-implement-port-wakeup.patch
# For bz#1026712 - Qemu core dumpd when boot guest with driver name as "virtio-pci"
# For bz#1046007 - qemu-kvm aborted when hot plug PCI device to guest with romfile and rombar=0
Patch757: kvm-qdev-monitor-Fix-crash-when-device_add-is-called-wit.patch
# For bz#1035001 - VHDX: journal log should not be replayed by default, but rather via qemu-img check -r all
Patch758: kvm-block-vhdx-improve-error-message-and-.bdrv_check-imp.patch
# For bz#1017650 - need to update qemu-img man pages on "VHDX" format
Patch759: kvm-docs-updated-qemu-img-man-page-and-qemu-doc-to-refle.patch
# For bz#1052340 - pvticketlocks: default on
Patch760: kvm-enable-pvticketlocks-by-default.patch
# For bz#997817 - -boot order and -boot once regressed since RHEL-6
Patch761: kvm-fix-boot-strict-regressed-in-commit-6ef4716.patch
# For bz#997817 - -boot order and -boot once regressed since RHEL-6
Patch762: kvm-vl-make-boot_strict-variable-static-not-used-outside.patch
# For bz#997559 - Improve live migration bitmap handling
Patch763: kvm-bitmap-use-long-as-index.patch
# For bz#997559 - Improve live migration bitmap handling
Patch764: kvm-memory-cpu_physical_memory_set_dirty_flags-result-is.patch
# For bz#997559 - Improve live migration bitmap handling
Patch765: kvm-memory-cpu_physical_memory_set_dirty_range-return-vo.patch
# For bz#997559 - Improve live migration bitmap handling
Patch766: kvm-exec-use-accessor-function-to-know-if-memory-is-dirt.patch
# For bz#997559 - Improve live migration bitmap handling
Patch767: kvm-memory-create-function-to-set-a-single-dirty-bit.patch
# For bz#997559 - Improve live migration bitmap handling
Patch768: kvm-exec-drop-useless-if.patch
# For bz#997559 - Improve live migration bitmap handling
Patch769: kvm-exec-create-function-to-get-a-single-dirty-bit.patch
# For bz#997559 - Improve live migration bitmap handling
Patch770: kvm-memory-make-cpu_physical_memory_is_dirty-return-bool.patch
# For bz#997559 - Improve live migration bitmap handling
Patch771: kvm-memory-all-users-of-cpu_physical_memory_get_dirty-us.patch
# For bz#997559 - Improve live migration bitmap handling
Patch772: kvm-memory-set-single-dirty-flags-when-possible.patch
# For bz#997559 - Improve live migration bitmap handling
Patch773: kvm-memory-cpu_physical_memory_set_dirty_range-always-di.patch
# For bz#997559 - Improve live migration bitmap handling
Patch774: kvm-memory-cpu_physical_memory_mask_dirty_range-always-c.patch
# For bz#997559 - Improve live migration bitmap handling
Patch775: kvm-memory-use-bit-2-for-migration.patch
# For bz#997559 - Improve live migration bitmap handling
Patch776: kvm-memory-make-sure-that-client-is-always-inside-range.patch
# For bz#997559 - Improve live migration bitmap handling
Patch777: kvm-memory-only-resize-dirty-bitmap-when-memory-size-inc.patch
# For bz#997559 - Improve live migration bitmap handling
Patch778: kvm-memory-cpu_physical_memory_clear_dirty_flag-result-i.patch
# For bz#997559 - Improve live migration bitmap handling
Patch779: kvm-bitmap-Add-bitmap_zero_extend-operation.patch
# For bz#997559 - Improve live migration bitmap handling
Patch780: kvm-memory-split-dirty-bitmap-into-three.patch
# For bz#997559 - Improve live migration bitmap handling
Patch781: kvm-memory-unfold-cpu_physical_memory_clear_dirty_flag-i.patch
# For bz#997559 - Improve live migration bitmap handling
Patch782: kvm-memory-unfold-cpu_physical_memory_set_dirty-in-its-o.patch
# For bz#997559 - Improve live migration bitmap handling
Patch783: kvm-memory-unfold-cpu_physical_memory_set_dirty_flag.patch
# For bz#997559 - Improve live migration bitmap handling
Patch784: kvm-memory-make-cpu_physical_memory_get_dirty-the-main-f.patch
# For bz#997559 - Improve live migration bitmap handling
Patch785: kvm-memory-cpu_physical_memory_get_dirty-is-used-as-retu.patch
# For bz#997559 - Improve live migration bitmap handling
Patch786: kvm-memory-s-mask-clear-cpu_physical_memory_mask_dirty_r.patch
# For bz#997559 - Improve live migration bitmap handling
Patch787: kvm-memory-use-find_next_bit-to-find-dirty-bits.patch
# For bz#997559 - Improve live migration bitmap handling
Patch788: kvm-memory-cpu_physical_memory_set_dirty_range-now-uses-.patch
# For bz#997559 - Improve live migration bitmap handling
Patch789: kvm-memory-cpu_physical_memory_clear_dirty_range-now-use.patch
# For bz#997559 - Improve live migration bitmap handling
Patch790: kvm-memory-s-dirty-clean-in-cpu_physical_memory_is_dirty.patch
# For bz#997559 - Improve live migration bitmap handling
Patch791: kvm-memory-make-cpu_physical_memory_reset_dirty-take-a-l.patch
# For bz#997559 - Improve live migration bitmap handling
Patch792: kvm-exec-Remove-unused-global-variable-phys_ram_fd.patch
# For bz#997559 - Improve live migration bitmap handling
Patch793: kvm-memory-cpu_physical_memory_set_dirty_tracking-should.patch
# For bz#997559 - Improve live migration bitmap handling
Patch794: kvm-memory-move-private-types-to-exec.c.patch
# For bz#997559 - Improve live migration bitmap handling
Patch795: kvm-memory-split-cpu_physical_memory_-functions-to-its-o.patch
# For bz#997559 - Improve live migration bitmap handling
Patch796: kvm-memory-unfold-memory_region_test_and_clear.patch
# For bz#997559 - Improve live migration bitmap handling
Patch797: kvm-use-directly-cpu_physical_memory_-api-for-tracki.patch
# For bz#997559 - Improve live migration bitmap handling
Patch798: kvm-refactor-start-address-calculation.patch
# For bz#997559 - Improve live migration bitmap handling
Patch799: kvm-memory-move-bitmap-synchronization-to-its-own-functi.patch
# For bz#997559 - Improve live migration bitmap handling
Patch800: kvm-memory-syncronize-kvm-bitmap-using-bitmaps-operation.patch
# For bz#997559 - Improve live migration bitmap handling
Patch801: kvm-ram-split-function-that-synchronizes-a-range.patch
# For bz#997559 - Improve live migration bitmap handling
Patch802: kvm-migration-synchronize-memory-bitmap-64bits-at-a-time.patch
# For bz#947785 - In rhel6.4 guest  sound recorder doesn't work when  playing audio
Patch803: kvm-intel-hda-fix-position-buffer.patch
# For bz#1003467 - Backport migration fixes from post qemu 1.6
Patch804: kvm-The-calculation-of-bytes_xfer-in-qemu_put_buffer-is-.patch
# For bz#1003467 - Backport migration fixes from post qemu 1.6
Patch805: kvm-migration-Fix-rate-limit.patch
# For bz#1017636 - PATCH: fix qemu using 50% host cpu when audio is playing
Patch806: kvm-audio-honor-QEMU_AUDIO_TIMER_PERIOD-instead-of-wakin.patch
# For bz#1017636 - PATCH: fix qemu using 50% host cpu when audio is playing
Patch807: kvm-audio-Lower-default-wakeup-rate-to-100-times-second.patch
# For bz#1017636 - PATCH: fix qemu using 50% host cpu when audio is playing
Patch808: kvm-audio-adjust-pulse-to-100Hz-wakeup-rate.patch
# For bz#918907 - provide backwards-compatible RHEL specific machine types in QEMU - CPU features
Patch809: kvm-pc-Fix-rhel6.-3dnow-3dnowext-compat-bits.patch
# For bz#1038603 - make seabios 256k for rhel7 machine types
Patch810: kvm-add-firmware-to-machine-options.patch
# For bz#1038603 - make seabios 256k for rhel7 machine types
Patch811: kvm-switch-rhel7-machine-types-to-big-bios.patch
# For bz#1034518 - boot order wrong with q35
Patch812: kvm-pci-fix-pci-bridge-fw-path.patch
# For bz#1031098 - Disable device smbus-eeprom
Patch813: kvm-hw-cannot_instantiate_with_device_add_yet-due-to-poi.patch
# For bz#1031098 - Disable device smbus-eeprom
Patch814: kvm-qdev-Document-that-pointer-properties-kill-device_ad.patch
# For bz#1044742 - Cannot create guest on remote RHEL7 host using F20 virt-manager, libvirt's qemu -no-hpet detection is broken
Patch815: kvm-Add-back-no-hpet-but-ignore-it.patch
# For bz#669524 - Confusing error message from -device <unknown dev>
Patch816: kvm-Revert-qdev-monitor-Fix-crash-when-device_add-is-cal.patch
# For bz#669524 - Confusing error message from -device <unknown dev>
Patch817: kvm-Revert-qdev-Do-not-let-the-user-try-to-device_add-wh.patch
# For bz#669524 - Confusing error message from -device <unknown dev>
Patch818: kvm-qdev-monitor-Clean-up-qdev_device_add-variable-namin.patch
# For bz#669524 - Confusing error message from -device <unknown dev>
Patch819: kvm-qdev-monitor-Fix-crash-when-device_add-is-called.2.patch.patch
# For bz#669524 - Confusing error message from -device <unknown dev>
Patch820: kvm-qdev-monitor-Avoid-qdev-as-variable-name.patch
# For bz#669524 - Confusing error message from -device <unknown dev>
Patch821: kvm-qdev-monitor-Inline-qdev_init-for-device_add.patch
# For bz#669524 - Confusing error message from -device <unknown dev>
Patch822: kvm-qdev-Do-not-let-the-user-try-to-device_add-when-it.2.patch.patch
# For bz#669524 - Confusing error message from -device <unknown dev>
Patch823: kvm-qdev-monitor-Avoid-device_add-crashing-on-non-device.patch
# For bz#669524 - Confusing error message from -device <unknown dev>
Patch824: kvm-qdev-monitor-Improve-error-message-for-device-nonexi.patch
# For bz#1003535 - qemu-kvm core dump when boot vm with more than 32 virtio disks/nics
Patch825: kvm-exec-change-well-known-physical-sections-to-macros.patch
# For bz#1003535 - qemu-kvm core dump when boot vm with more than 32 virtio disks/nics
Patch826: kvm-exec-separate-sections-and-nodes-per-address-space.patch
# For bz#1053699 - Backport Cancelled race condition fixes
Patch827: kvm-avoid-a-bogus-COMPLETED-CANCELLED-transition.patch
# For bz#1053699 - Backport Cancelled race condition fixes
Patch828: kvm-introduce-MIG_STATE_CANCELLING-state.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch829: kvm-vvfat-use-bdrv_new-to-allocate-BlockDriverState.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch830: kvm-block-implement-reference-count-for-BlockDriverState.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch831: kvm-block-make-bdrv_delete-static.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch832: kvm-migration-omit-drive-ref-as-we-have-bdrv_ref-now.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch833: kvm-xen_disk-simplify-blk_disconnect-with-refcnt.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch834: kvm-nbd-use-BlockDriverState-refcnt.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch835: kvm-block-use-BDS-ref-for-block-jobs.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch836: kvm-block-Make-BlockJobTypes-const.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch837: kvm-blockjob-rename-BlockJobType-to-BlockJobDriver.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch838: kvm-qapi-Introduce-enum-BlockJobType.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch839: kvm-qapi-make-use-of-new-BlockJobType.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch840: kvm-mirror-Don-t-close-target.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch841: kvm-mirror-Move-base-to-MirrorBlockJob.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch842: kvm-block-Add-commit_active_start.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch843: kvm-commit-Support-commit-active-layer.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch844: kvm-qemu-iotests-prefill-some-data-to-test-image.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch845: kvm-qemu-iotests-Update-test-cases-for-commit-active.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch846: kvm-commit-Remove-unused-check.patch
# For bz#921890 - Core dump when block mirror with "sync" is "none" and mode is "absolute-paths"
Patch847: kvm-blockdev-use-bdrv_getlength-in-qmp_drive_mirror.patch
# For bz#921890 - Core dump when block mirror with "sync" is "none" and mode is "absolute-paths"
Patch848: kvm-qemu-iotests-make-assert_no_active_block_jobs-common.patch
# For bz#921890 - Core dump when block mirror with "sync" is "none" and mode is "absolute-paths"
Patch849: kvm-block-drive-mirror-Check-for-NULL-backing_hd.patch
# For bz#921890 - Core dump when block mirror with "sync" is "none" and mode is "absolute-paths"
Patch850: kvm-qemu-iotests-Extend-041-for-unbacked-mirroring.patch
# For bz#921890 - Core dump when block mirror with "sync" is "none" and mode is "absolute-paths"
Patch851: kvm-qapi-schema-Update-description-for-NewImageMode.patch
# For bz#921890 - Core dump when block mirror with "sync" is "none" and mode is "absolute-paths"
Patch852: kvm-block-drive-mirror-Reuse-backing-HD-for-sync-none.patch
# For bz#921890 - Core dump when block mirror with "sync" is "none" and mode is "absolute-paths"
Patch853: kvm-qemu-iotests-Fix-test-041.patch
# For bz#1035644 - rhel7.0host + windows guest + virtio-win + 'chkdsk' in the guest gives qemu assertion in scsi_dma_complete
Patch854: kvm-scsi-bus-fix-transfer-length-and-direction-for-VERIF.patch
# For bz#1035644 - rhel7.0host + windows guest + virtio-win + 'chkdsk' in the guest gives qemu assertion in scsi_dma_complete
Patch855: kvm-scsi-disk-fix-VERIFY-emulation.patch
# For bz#1041301 - live snapshot merge (commit) of the active layer
Patch856: kvm-block-ensure-bdrv_drain_all-works-during-bdrv_delete.patch
# For bz#998708 - qemu-kvm: maximum vcpu should be recommended maximum
Patch857: kvm-use-recommended-max-vcpu-count.patch
# For bz#1049706 - MIss CPUID_EXT_X2APIC in Westmere cpu model
Patch858: kvm-pc-Create-pc_compat_rhel-functions.patch
# For bz#1049706 - MIss CPUID_EXT_X2APIC in Westmere cpu model
Patch859: kvm-pc-Enable-x2apic-by-default-on-more-recent-CPU-model.patch
# For bz#1019221 - Iscsi miss id sub-option in help output
Patch860: kvm-help-add-id-suboption-to-iscsi.patch
# For bz#1037503 - fix thin provisioning support for block device backends
Patch861: kvm-scsi-disk-add-UNMAP-limits-to-block-limits-VPD-page.patch
# For bz#1034876 - export acpi tables to guests
Patch862: kvm-qdev-Fix-32-bit-compilation-in-print_size.patch
# For bz#1034876 - export acpi tables to guests
Patch863: kvm-qdev-Use-clz-in-print_size.patch
# For bz#1026548 - i386: pc: align gpa<->hpa on 1GB boundary
Patch864: kvm-piix-gigabyte-alignment-for-ram.patch
# For bz#1026548 - i386: pc: align gpa<->hpa on 1GB boundary
Patch865: kvm-pc_piix-document-gigabyte_align.patch
# For bz#1026548 - i386: pc: align gpa<->hpa on 1GB boundary
Patch866: kvm-q35-gigabyle-alignment-for-ram.patch
# For bz#983344 - QEMU core dump and host will reboot when do hot-unplug a virtio-blk disk which use  the switch behind switch
Patch867: kvm-virtio-bus-remove-vdev-field.patch
# For bz#983344 - QEMU core dump and host will reboot when do hot-unplug a virtio-blk disk which use  the switch behind switch
Patch868: kvm-virtio-pci-remove-vdev-field.patch
# For bz#983344 - QEMU core dump and host will reboot when do hot-unplug a virtio-blk disk which use  the switch behind switch
Patch869: kvm-virtio-bus-cleanup-plug-unplug-interface.patch
# For bz#983344 - QEMU core dump and host will reboot when do hot-unplug a virtio-blk disk which use  the switch behind switch
Patch870: kvm-virtio-blk-switch-exit-callback-to-VirtioDeviceClass.patch
# For bz#983344 - QEMU core dump and host will reboot when do hot-unplug a virtio-blk disk which use  the switch behind switch
Patch871: kvm-virtio-serial-switch-exit-callback-to-VirtioDeviceCl.patch
# For bz#983344 - QEMU core dump and host will reboot when do hot-unplug a virtio-blk disk which use  the switch behind switch
Patch872: kvm-virtio-net-switch-exit-callback-to-VirtioDeviceClass.patch
# For bz#983344 - QEMU core dump and host will reboot when do hot-unplug a virtio-blk disk which use  the switch behind switch
Patch873: kvm-virtio-scsi-switch-exit-callback-to-VirtioDeviceClas.patch
# For bz#983344 - QEMU core dump and host will reboot when do hot-unplug a virtio-blk disk which use  the switch behind switch
Patch874: kvm-virtio-balloon-switch-exit-callback-to-VirtioDeviceC.patch
# For bz#983344 - QEMU core dump and host will reboot when do hot-unplug a virtio-blk disk which use  the switch behind switch
Patch875: kvm-virtio-rng-switch-exit-callback-to-VirtioDeviceClass.patch
# For bz#983344 - QEMU core dump and host will reboot when do hot-unplug a virtio-blk disk which use  the switch behind switch
Patch876: kvm-virtio-pci-add-device_unplugged-callback.patch
# For bz#1051438 - Error message contains garbled characters when unable to open image due to bad permissions (permission denied).
Patch877: kvm-block-use-correct-filename-for-error-report.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch878: kvm-Partially-revert-rhel-Drop-cfi.pflash01-and-isa-ide-.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch879: kvm-Revert-pc-Disable-the-use-flash-device-for-BIOS-unle.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch880: kvm-memory-Replace-open-coded-memory_region_is_romd.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch881: kvm-memory-Rename-readable-flag-to-romd_mode.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch882: kvm-isapc-Fix-non-KVM-qemu-boot-read-write-memory-for-is.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch883: kvm-add-kvm_readonly_mem_enabled.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch884: kvm-support-using-KVM_MEM_READONLY-flag-for-regions.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch885: kvm-pc_sysfw-allow-flash-pflash-memory-to-be-used-with-K.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch886: kvm-fix-double-free-the-memslot-in-kvm_set_phys_mem.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch887: kvm-sysfw-remove-read-only-pc_sysfw_flash_vs_rom_bug_com.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch888: kvm-pc_sysfw-remove-the-rom_only-property.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch889: kvm-pc_sysfw-do-not-make-it-a-device-anymore.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch890: kvm-hw-i386-pc_sysfw-support-two-flash-drives.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch891: kvm-i440fx-test-qtest_start-should-be-paired-with-qtest_.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch892: kvm-i440fx-test-give-each-GTest-case-its-own-qtest.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch893: kvm-i440fx-test-generate-temporary-firmware-blob.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch894: kvm-i440fx-test-verify-firmware-under-4G-and-1M-both-bio.patch
# For bz#1032346 - basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables)
Patch895: kvm-piix-fix-32bit-pci-hole.patch
# For bz#1041564 - [NFR] qemu: Returning the watermark for all the images opened for writing
Patch896: kvm-qapi-Add-backing-to-BlockStats.patch
# For bz#918907 - provide backwards-compatible RHEL specific machine types in QEMU - CPU features
Patch897: kvm-pc-Disable-RDTSCP-unconditionally-on-rhel6.-machine-.patch
# For bz#1056428 - "rdtscp" flag defined on Opteron_G5 model and cann't be exposed to guest
# For bz#874400 - "rdtscp" flag defined on Opteron_G5 model and cann't be exposed to guest
Patch898: kvm-pc-Disable-RDTSCP-on-AMD-CPU-models.patch
# For bz#1030301 - qemu-img can not merge live snapshot to backing file(r/w backing file via libiscsi)
Patch899: kvm-block-add-.bdrv_reopen_prepare-stub-for-iscsi.patch
# For bz#1044815 - vfio initfn succeeds even if IOMMU mappings fail
Patch900: kvm-vfio-pci-Fail-initfn-on-DMA-mapping-errors.patch
# For bz#1052030 - src qemu-kvm core dump after hotplug/unhotplug GPU device and do local migration
Patch901: kvm-vfio-Destroy-memory-regions.patch
# For bz#1048092 - manpage of qemu-img contains error statement about compat option
Patch902: kvm-docs-qcow2-compat-1.1-is-now-the-default.patch
# For bz#947812 - There's a shot voice after  'system_reset'  during playing music inside rhel6 guest w/ intel-hda device
Patch903: kvm-hda-codec-disable-streams-on-reset.patch
# For bz#1009297 - RHEL7.0 guest gui can not be used in dest host after migration
Patch904: kvm-QEMUBH-make-AioContext-s-bh-re-entrant.patch
# For bz#1009297 - RHEL7.0 guest gui can not be used in dest host after migration
Patch905: kvm-qxl-replace-pipe-signaling-with-bottom-half.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch906: kvm-block-fix-backing-file-segfault.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch907: kvm-block-Move-initialisation-of-BlockLimits-to-bdrv_ref.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch908: kvm-raw-Fix-BlockLimits-passthrough.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch909: kvm-block-Inherit-opt_transfer_length.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch910: kvm-block-Update-BlockLimits-when-they-might-have-change.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch911: kvm-qemu_memalign-Allow-small-alignments.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch912: kvm-block-Detect-unaligned-length-in-bdrv_qiov_is_aligne.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch913: kvm-block-Don-t-use-guest-sector-size-for-qemu_blockalig.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch914: kvm-block-rename-buffer_alignment-to-guest_block_size.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch915: kvm-raw-Probe-required-direct-I-O-alignment.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch916: kvm-block-Introduce-bdrv_aligned_preadv.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch917: kvm-block-Introduce-bdrv_co_do_preadv.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch918: kvm-block-Introduce-bdrv_aligned_pwritev.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch919: kvm-block-write-Handle-COR-dependency-after-I-O-throttli.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch920: kvm-block-Introduce-bdrv_co_do_pwritev.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch921: kvm-block-Switch-BdrvTrackedRequest-to-byte-granularity.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch922: kvm-block-Allow-waiting-for-overlapping-requests-between.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch923: kvm-block-use-DIV_ROUND_UP-in-bdrv_co_do_readv.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch924: kvm-block-Make-zero-after-EOF-work-with-larger-alignment.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch925: kvm-block-Generalise-and-optimise-COR-serialisation.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch926: kvm-block-Make-overlap-range-for-serialisation-dynamic.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch927: kvm-block-Fix-32-bit-truncation-in-mark_request_serialis.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch928: kvm-block-Allow-wait_serialising_requests-at-any-point.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch929: kvm-block-Align-requests-in-bdrv_co_do_pwritev.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch930: kvm-lock-Fix-memory-leaks-in-bdrv_co_do_pwritev.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch931: kvm-block-Assert-serialisation-assumptions-in-pwritev.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch932: kvm-block-Change-coroutine-wrapper-to-byte-granularity.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch933: kvm-block-Make-bdrv_pread-a-bdrv_prwv_co-wrapper.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch934: kvm-block-Make-bdrv_pwrite-a-bdrv_prwv_co-wrapper.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch935: kvm-iscsi-Set-bs-request_alignment.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch936: kvm-blkdebug-Make-required-alignment-configurable.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch937: kvm-blkdebug-Don-t-leak-bs-file-on-failure.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch938: kvm-qemu-io-New-command-sleep.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch939: kvm-qemu-iotests-Filter-out-qemu-io-prompt.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch940: kvm-qemu-iotests-Test-pwritev-RMW-logic.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch941: kvm-block-bdrv_aligned_pwritev-Assert-overlap-range.patch
# For bz#748906 - qemu fails on disk with 4k sectors and cache=off
Patch942: kvm-block-Don-t-call-ROUND_UP-with-negative-values.patch
# For bz#1026314 - qemu-kvm hang when use '-sandbox on'+'vnc'+'hda'
Patch943: kvm-seccomp-add-mkdir-and-fchmod-to-the-whitelist.patch
# For bz#1026314 - qemu-kvm hang when use '-sandbox on'+'vnc'+'hda'
Patch944: kvm-seccomp-add-some-basic-shared-memory-syscalls-to-the.patch
# For bz#1004143 - "test unit ready failed" on LUN 0 delays boot when a virtio-scsi target does not have any disk on LUN 0
Patch945: kvm-scsi-Support-TEST-UNIT-READY-in-the-dummy-LUN0.patch
# For bz#1039530 - add support for microsoft os descriptors
Patch946: kvm-usb-add-vendor-request-defines.patch
# For bz#1039530 - add support for microsoft os descriptors
Patch947: kvm-usb-move-usb_-hi-lo-helpers-to-header-file.patch
# For bz#1039530 - add support for microsoft os descriptors
Patch948: kvm-usb-add-support-for-microsoft-os-descriptors.patch
# For bz#1039530 - add support for microsoft os descriptors
Patch949: kvm-usb-add-microsoft-os-descriptors-compat-property.patch
# For bz#1039530 - add support for microsoft os descriptors
Patch950: kvm-usb-hid-add-microsoft-os-descriptor-support.patch
# For bz#1044182 - Relax qemu-kvm stack protection to -fstack-protector-strong
Patch951: kvm-configure-add-option-to-disable-fstack-protect.patch
# For bz#1004197 - Cannot hot-plug nic in windows VM when the vmem is larger
Patch952: kvm-exec-always-use-MADV_DONTFORK.patch
# For bz#1048080 - Qemu-kvm NUMA emulation failed
Patch953: kvm-pc-Save-size-of-RAM-below-4GB.patch
# For bz#1048080 - Qemu-kvm NUMA emulation failed
Patch954: kvm-acpi-Fix-PCI-hole-handling-on-build_srat.patch
# For bz#1017096 - Fail to migrate while the size of migrate-compcache less then 4096
Patch955: kvm-Add-check-for-cache-size-smaller-than-page-size.patch
# For bz#1047448 - qemu-kvm core  dump in src host when do migration with "migrate_set_capability xbzrle on and migrate_set_cache_size 10000G"
Patch956: kvm-XBZRLE-cache-size-should-not-be-larger-than-guest-me.patch
# For bz#1047448 - qemu-kvm core  dump in src host when do migration with "migrate_set_capability xbzrle on and migrate_set_cache_size 10000G"
Patch957: kvm-Don-t-abort-on-out-of-memory-when-creating-page-cach.patch
# For bz#1047448 - qemu-kvm core  dump in src host when do migration with "migrate_set_capability xbzrle on and migrate_set_cache_size 10000G"
Patch958: kvm-Don-t-abort-on-memory-allocation-error.patch
# For bz#1038540 - qemu-kvm aborted while cancel migration then restart it (with page delta compression)
Patch959: kvm-Set-xbzrle-buffers-to-NULL-after-freeing-them-to-avo.patch
# For bz#1038540 - qemu-kvm aborted while cancel migration then restart it (with page delta compression)
Patch960: kvm-migration-fix-free-XBZRLE-decoded_buf-wrong.patch
# For bz#1047254 - qemu-img failed to commit image
Patch961: kvm-block-resize-backing-file-image-during-offline-commi.patch
# For bz#1047254 - qemu-img failed to commit image
Patch962: kvm-block-resize-backing-image-during-active-layer-commi.patch
# For bz#1047254 - qemu-img failed to commit image
Patch963: kvm-block-update-block-commit-documentation-regarding-im.patch
# For bz#1047254 - qemu-img failed to commit image
Patch964: kvm-block-Fix-bdrv_commit-return-value.patch
# For bz#1047254 - qemu-img failed to commit image
Patch965: kvm-block-remove-QED-.bdrv_make_empty-implementation.patch
# For bz#1047254 - qemu-img failed to commit image
Patch966: kvm-block-remove-qcow2-.bdrv_make_empty-implementation.patch
# For bz#997878 - Kill -SIGUSR1 `pidof qemu-img convert` can not get progress of qemu-img
Patch967: kvm-qemu-progress-Drop-unused-include.patch
# For bz#997878 - Kill -SIGUSR1 `pidof qemu-img convert` can not get progress of qemu-img
Patch968: kvm-qemu-progress-Fix-progress-printing-on-SIGUSR1.patch
# For bz#997878 - Kill -SIGUSR1 `pidof qemu-img convert` can not get progress of qemu-img
Patch969: kvm-Documentation-qemu-img-Mention-SIGUSR1-progress-repo.patch
# For bz#1063942 - configure qemu-kvm with --disable-qom-cast-debug
Patch970: kvm-fix-guest-physical-bits-to-match-host-to-go-beyond-1.patch
# For bz#1065225 - QMP socket breaks on unexpected close
Patch971: kvm-monitor-Cleanup-mon-outbuf-on-write-error.patch
# For bz#1012365 - xhci usb storage lost in guest after wakeup from S3
Patch972: kvm-xhci-add-support-for-suspend-resume.patch
# For bz#1049176 - qemu-img core dump when using "-o preallocation=metadata,cluster_size=2048k" to create image of libiscsi lun
Patch973: kvm-qcow2-remove-n_start-and-n_end-of-qcow2_alloc_cluste.patch
# For bz#1049176 - qemu-img core dump when using "-o preallocation=metadata,cluster_size=2048k" to create image of libiscsi lun
Patch974: kvm-qcow2-fix-offset-overflow-in-qcow2_alloc_clusters_at.patch
# For bz#1055848 - qemu-img core dumped when cluster size is larger than the default value with opreallocation=metadata specified
Patch975: kvm-qcow2-check-for-NULL-l2meta.patch
# For bz#1055848 - qemu-img core dumped when cluster size is larger than the default value with opreallocation=metadata specified
Patch976: kvm-qemu-iotests-add-test-for-qcow2-preallocation-with-d.patch
# For bz#1069039 - -mem-prealloc option behaviour is opposite to expected
Patch977: kvm-mempath-prefault-fix-off-by-one-error.patch
# For bz#1065873 - qemu-img silently ignores options with multiple -o parameters
Patch978: kvm-qemu-option-has_help_option-and-is_valid_option_list.patch
# For bz#1065873 - qemu-img silently ignores options with multiple -o parameters
Patch979: kvm-qemu-img-create-Support-multiple-o-options.patch
# For bz#1065873 - qemu-img silently ignores options with multiple -o parameters
Patch980: kvm-qemu-img-convert-Support-multiple-o-options.patch
# For bz#1065873 - qemu-img silently ignores options with multiple -o parameters
Patch981: kvm-qemu-img-amend-Support-multiple-o-options.patch
# For bz#1065873 - qemu-img silently ignores options with multiple -o parameters
Patch982: kvm-qemu-img-Allow-o-help-with-incomplete-argument-list.patch
# For bz#1065873 - qemu-img silently ignores options with multiple -o parameters
Patch983: kvm-qemu-iotests-Check-qemu-img-command-line-parsing.patch
# For bz#1026184 - QMP: querying -drive option returns a NULL parameter list
Patch984: kvm-qmp-access-the-local-QemuOptsLists-for-drive-option.patch
# For bz#751937 - qxl triggers assert during iofuzz test
Patch985: kvm-qxl-add-sanity-check.patch
# For bz#1063417 - google stressapptest vs Migration
Patch986: kvm-Fix-two-XBZRLE-corruption-issues.patch
# For bz#1037956 - bnx2x: boot one guest to do vfio-pci with all PFs assigned in same group meet QEMU segmentation fault (Broadcom BCM57810 card)
Patch987: kvm-qdev-monitor-set-DeviceState-opts-before-calling-rea.patch
# For bz#1037956 - bnx2x: boot one guest to do vfio-pci with all PFs assigned in same group meet QEMU segmentation fault (Broadcom BCM57810 card)
Patch988: kvm-vfio-blacklist-loading-of-unstable-roms.patch
# For bz#1072339 - RHEV: Cannot start VMs that have more than 23 snapshots.
Patch989: kvm-block-Set-block-filename-sizes-to-PATH_MAX-instead-o.patch
# For bz#1004773 - Hyper-V guest OS id and hypercall MSRs not migrated
Patch990: kvm-target-i386-Move-hyperv_-static-globals-to-X86CPU.patch
# For bz#1057173 - KVM Hyper-V Enlightenment - New feature - hv-time (QEMU)
Patch991: kvm-Fix-uninitialized-cpuid_data.patch
# For bz#1004773 - Hyper-V guest OS id and hypercall MSRs not migrated
Patch992: kvm-fix-coexistence-of-KVM-and-Hyper-V-leaves.patch
# For bz#1004773 - Hyper-V guest OS id and hypercall MSRs not migrated
Patch993: kvm-make-availability-of-Hyper-V-enlightenments-depe.patch
# For bz#1004773 - Hyper-V guest OS id and hypercall MSRs not migrated
Patch994: kvm-make-hyperv-hypercall-and-guest-os-id-MSRs-migra.patch
# For bz#1004773 - Hyper-V guest OS id and hypercall MSRs not migrated
Patch995: kvm-make-hyperv-vapic-assist-page-migratable.patch
# For bz#1057173 - KVM Hyper-V Enlightenment - New feature - hv-time (QEMU)
Patch996: kvm-target-i386-Convert-hv_relaxed-to-static-property.patch
# For bz#1057173 - KVM Hyper-V Enlightenment - New feature - hv-time (QEMU)
Patch997: kvm-target-i386-Convert-hv_vapic-to-static-property.patch
# For bz#1057173 - KVM Hyper-V Enlightenment - New feature - hv-time (QEMU)
Patch998: kvm-target-i386-Convert-hv_spinlocks-to-static-property.patch
# For bz#1004773 - Hyper-V guest OS id and hypercall MSRs not migrated
Patch999: kvm-target-i386-Convert-check-and-enforce-to-static-prop.patch
# For bz#1057173 - KVM Hyper-V Enlightenment - New feature - hv-time (QEMU)
Patch1000: kvm-target-i386-Cleanup-foo-feature-handling.patch
# For bz#1057173 - KVM Hyper-V Enlightenment - New feature - hv-time (QEMU)
Patch1001: kvm-add-support-for-hyper-v-timers.patch
# For bz#1069541 - Segmentation fault when boot guest with dataplane=on
Patch1002: kvm-dataplane-Fix-startup-race.patch
# For bz#1057471 - fail to do hot-plug with "discard = on" with "Invalid parameter 'discard'" error
Patch1003: kvm-QMP-Relax-__com.redhat_drive_add-parameter-checking.patch
# For bz#993429 - kvm: test maximum number of vcpus supported (rhel7)
Patch1004: kvm-all-exit-in-case-max-vcpus-exceeded.patch
# For bz#1031526 - Can not commit snapshot when disk is using glusterfs:native backend
Patch1005: kvm-block-gluster-code-movements-state-storage-changes.patch
# For bz#1031526 - Can not commit snapshot when disk is using glusterfs:native backend
Patch1006: kvm-block-gluster-add-reopen-support.patch
# For bz#990989 - backport inline header virtio-net optimization
Patch1007: kvm-virtio-net-add-feature-bit-for-any-header-s-g.patch
# For bz#1073774 - e1000 ROM cause migrate fail  from RHEL6.5 host to RHEL7.0 host
Patch1008: kvm-pc-Add-RHEL6-e1000-gPXE-image.patch
# For bz#1064018 - abort from conflicting genroms
# For bz#1064018#c6 - abort from conflicting genroms
Patch1009: kvm-loader-rename-in_ram-has_mr.patch
# For bz#1064018 - abort from conflicting genroms
# For bz#1064018#c6 - abort from conflicting genroms
Patch1010: kvm-pc-avoid-duplicate-names-for-ROM-MRs.patch
# For bz#1073728 - progress bar doesn't display when converting with -p
Patch1011: kvm-qemu-img-convert-Fix-progress-output.patch
# For bz#1073728 - progress bar doesn't display when converting with -p
Patch1012: kvm-qemu-iotests-Test-progress-output-for-conversion.patch
# For bz#1067784 - qemu-kvm: block.c:850: bdrv_open_common: Assertion `bs->request_alignment != 0' failed. Aborted (core dumped)
Patch1013: kvm-iscsi-Use-bs-sg-for-everything-else-than-disks.patch
# For bz#1067784 - qemu-kvm: block.c:850: bdrv_open_common: Assertion `bs->request_alignment != 0' failed. Aborted (core dumped)
Patch1014: kvm-block-Fix-bs-request_alignment-assertion-for-bs-sg-1.patch
# For bz#1005103 - Migration should fail when migrate guest offline to a file which is specified to a readonly directory.
Patch1015: kvm-qemu_file-use-fwrite-correctly.patch
# For bz#1005103 - Migration should fail when migrate guest offline to a file which is specified to a readonly directory.
Patch1016: kvm-qemu_file-Fix-mismerge-of-use-fwrite-correctly.patch
# For bz#1046248 - qemu-kvm crash when send "info qtree" after hot plug a device with invalid addr
Patch1017: kvm-qdev-monitor-Set-properties-after-parent-is-assigned.patch
# For bz#1048575 - Segmentation fault occurs after migrate guest(use scsi disk and add stress) to des machine
Patch1018: kvm-block-Update-image-size-in-bdrv_invalidate_cache.patch
# For bz#1048575 - Segmentation fault occurs after migrate guest(use scsi disk and add stress) to des machine
Patch1019: kvm-qcow2-Keep-option-in-qcow2_invalidate_cache.patch
# For bz#1048575 - Segmentation fault occurs after migrate guest(use scsi disk and add stress) to des machine
Patch1020: kvm-qcow2-Check-bs-drv-in-copy_sectors.patch
# For bz#1048575 - Segmentation fault occurs after migrate guest(use scsi disk and add stress) to des machine
Patch1021: kvm-block-bs-drv-may-be-NULL-in-bdrv_debug_resume.patch
# For bz#1048575 - Segmentation fault occurs after migrate guest(use scsi disk and add stress) to des machine
Patch1022: kvm-iotests-Test-corruption-during-COW-request.patch
# For bz#1058173 - qemu-kvm core dump booting guest with scsi-generic disk attached when using built-in iscsi driver
Patch1023: kvm-scsi-Change-scsi-sense-buf-size-to-252.patch
# For bz#1058173 - qemu-kvm core dump booting guest with scsi-generic disk attached when using built-in iscsi driver
Patch1024: kvm-scsi-Fix-migration-of-scsi-sense-data.patch
# For bz#1078809 - can not boot qemu-kvm-rhev with rbd image
Patch1025: kvm-configure-Fix-bugs-preventing-Ceph-inclusion.patch
# For bz#1078308 - EMBARGOED CVE-2014-0150 qemu: virtio-net: fix guest-triggerable buffer overrun [rhel-7.0]
Patch1026: kvm-virtio-net-fix-guest-triggerable-buffer-overrun.patch
# For bz#1080170 - Default CPU model for rhel6.* machine-types is different from RHEL-6
Patch1027: kvm-pc-Use-cpu64-rhel6-CPU-model-by-default-on-rhel6-mac.patch
# For bz#1078607 - intel 82576 VF not work in windows 2008 x86 - Code 12 [TestOnly]
# For bz#1080170 - Default CPU model for rhel6.* machine-types is different from RHEL-6
Patch1028: kvm-target-i386-Copy-cpu64-rhel6-definition-into-qemu64.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1029: kvm-qemu-iotests-add-.-check-cloop-support.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1030: kvm-qemu-iotests-add-cloop-input-validation-tests.patch
# For bz#1079455 - CVE-2014-0144 qemu-kvm: Qemu: block: missing input validation [rhel-7.0]
Patch1031: kvm-block-cloop-validate-block_size-header-field-CVE-201.patch
# For bz#1079320 - CVE-2014-0143 qemu-kvm: Qemu: block: multiple integer overflow flaws [rhel-7.0]
Patch1032: kvm-block-cloop-prevent-offsets_size-integer-overflow-CV.patch
# For bz#1079455 - CVE-2014-0144 qemu-kvm: Qemu: block: missing input validation [rhel-7.0]
Patch1033: kvm-block-cloop-refuse-images-with-huge-offsets-arrays-C.patch
# For bz#1079455 - CVE-2014-0144 qemu-kvm: Qemu: block: missing input validation [rhel-7.0]
Patch1034: kvm-block-cloop-refuse-images-with-bogus-offsets-CVE-201.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1035: kvm-size-off-by-one.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1036: kvm-qemu-iotests-Support-for-bochs-format.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1037: kvm-bochs-Unify-header-structs-and-make-them-QEMU_PACKED.patch
# For bz#1079339 - CVE-2014-0147 qemu-kvm: Qemu: block: possible crash due signed types or logic error [rhel-7.0]
Patch1038: kvm-bochs-Use-unsigned-variables-for-offsets-and-sizes-C.patch
# For bz#1079320 - CVE-2014-0143 qemu-kvm: Qemu: block: multiple integer overflow flaws [rhel-7.0]
Patch1039: kvm-bochs-Check-catalog_size-header-field-CVE-2014-0143.patch
# For bz#1079315 - CVE-2014-0142 qemu-kvm: qemu: crash by possible division by zero [rhel-7.0]
Patch1040: kvm-bochs-Check-extent_size-header-field-CVE-2014-0142.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1041: kvm-bochs-Fix-bitmap-offset-calculation.patch
# For bz#1079455 - CVE-2014-0144 qemu-kvm: Qemu: block: missing input validation [rhel-7.0]
Patch1042: kvm-vpc-vhd-add-bounds-check-for-max_table_entries-and-b.patch
# For bz#1079315 - CVE-2014-0142 qemu-kvm: qemu: crash by possible division by zero [rhel-7.0]
Patch1043: kvm-vpc-Validate-block-size-CVE-2014-0142.patch
# For bz#1079455 - CVE-2014-0144 qemu-kvm: Qemu: block: missing input validation [rhel-7.0]
Patch1044: kvm-vdi-add-bounds-checks-for-blocks_in_image-and-disk_s.patch
# For bz#1079346 - CVE-2014-0148 qemu-kvm: Qemu: vhdx: bounds checking for block_size and logical_sector_size [rhel-7.0]
Patch1045: kvm-vhdx-Bounds-checking-for-block_size-and-logical_sect.patch
# For bz#1079455 - CVE-2014-0144 qemu-kvm: Qemu: block: missing input validation [rhel-7.0]
Patch1046: kvm-curl-check-data-size-before-memcpy-to-local-buffer.-.patch
# For bz#1079455 - CVE-2014-0144 qemu-kvm: Qemu: block: missing input validation [rhel-7.0]
Patch1047: kvm-qcow2-Check-header_length-CVE-2014-0144.patch
# For bz#1079455 - CVE-2014-0144 qemu-kvm: Qemu: block: missing input validation [rhel-7.0]
Patch1048: kvm-qcow2-Check-backing_file_offset-CVE-2014-0144.patch
# For bz#1079455 - CVE-2014-0144 qemu-kvm: Qemu: block: missing input validation [rhel-7.0]
Patch1049: kvm-qcow2-Check-refcount-table-size-CVE-2014-0144.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1050: kvm-qcow2-Validate-refcount-table-offset.patch
# For bz#1079455 - CVE-2014-0144 qemu-kvm: Qemu: block: missing input validation [rhel-7.0]
Patch1051: kvm-qcow2-Validate-snapshot-table-offset-size-CVE-2014-0.patch
# For bz#1079455 - CVE-2014-0144 qemu-kvm: Qemu: block: missing input validation [rhel-7.0]
Patch1052: kvm-qcow2-Validate-active-L1-table-offset-and-size-CVE-2.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1053: kvm-qcow2-Fix-backing-file-name-length-check.patch
# For bz#1079339 - CVE-2014-0147 qemu-kvm: Qemu: block: possible crash due signed types or logic error [rhel-7.0]
Patch1054: kvm-qcow2-Don-t-rely-on-free_cluster_index-in-alloc_refc.patch
# For bz#1079320 - CVE-2014-0143 qemu-kvm: Qemu: block: multiple integer overflow flaws [rhel-7.0]
Patch1055: kvm-qcow2-Avoid-integer-overflow-in-get_refcount-CVE-201.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1056: kvm-qcow2-Check-new-refcount-table-size-on-growth.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1057: kvm-qcow2-Fix-types-in-qcow2_alloc_clusters-and-alloc_cl.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1058: kvm-qcow2-Protect-against-some-integer-overflows-in-bdrv.patch
# For bz#1079320 - CVE-2014-0143 qemu-kvm: Qemu: block: multiple integer overflow flaws [rhel-7.0]
Patch1059: kvm-qcow2-Fix-new-L1-table-size-check-CVE-2014-0143.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1060: kvm-dmg-coding-style-and-indentation-cleanup.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1061: kvm-dmg-prevent-out-of-bounds-array-access-on-terminator.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1062: kvm-dmg-drop-broken-bdrv_pread-loop.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1063: kvm-dmg-use-appropriate-types-when-reading-chunks.patch
# For bz#1079325 - CVE-2014-0145 qemu-kvm: Qemu: prevent possible buffer overflows [rhel-7.0]
Patch1064: kvm-dmg-sanitize-chunk-length-and-sectorcount-CVE-2014-0.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1065: kvm-dmg-use-uint64_t-consistently-for-sectors-and-length.patch
# For bz#1079325 - CVE-2014-0145 qemu-kvm: Qemu: prevent possible buffer overflows [rhel-7.0]
Patch1066: kvm-dmg-prevent-chunk-buffer-overflow-CVE-2014-0145.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1067: kvm-block-vdi-bounds-check-qemu-io-tests.patch
# For bz#1079320 - CVE-2014-0143 qemu-kvm: Qemu: block: multiple integer overflow flaws [rhel-7.0]
Patch1068: kvm-block-Limit-request-size-CVE-2014-0143.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1069: kvm-qcow2-Fix-copy_sectors-with-VM-state.patch
# For bz#1079333 - CVE-2014-0146 qemu-kvm: Qemu: qcow2: NULL dereference in qcow2_open() error path [rhel-7.0]
Patch1070: kvm-qcow2-Fix-NULL-dereference-in-qcow2_open-error-path-.patch
# For bz#1079325 - CVE-2014-0145 qemu-kvm: Qemu: prevent possible buffer overflows [rhel-7.0]
Patch1071: kvm-qcow2-Fix-L1-allocation-size-in-qcow2_snapshot_load_.patch
# For bz#1079320 - CVE-2014-0143 qemu-kvm: Qemu: block: multiple integer overflow flaws [rhel-7.0]
Patch1072: kvm-qcow2-Check-maximum-L1-size-in-qcow2_snapshot_load_t.patch
# For bz#1066691 - qemu-kvm: include leftover patches from block layer security audit
Patch1073: kvm-qcow2-Limit-snapshot-table-size.patch
# For bz#1079320 - CVE-2014-0143 qemu-kvm: Qemu: block: multiple integer overflow flaws [rhel-7.0]
Patch1074: kvm-parallels-Fix-catalog-size-integer-overflow-CVE-2014.patch
# For bz#1079315 - CVE-2014-0142 qemu-kvm: qemu: crash by possible division by zero [rhel-7.0]
Patch1075: kvm-parallels-Sanity-check-for-s-tracks-CVE-2014-0142.patch
# For bz#740107 - [Hitachi 7.0 FEAT]  KVM: MCA Recovery for KVM guest OS memory
Patch1076: kvm-fix-machine-check-propagation.patch
# For bz#1081793 - qemu-img core dumped when creating a qcow2 image base on block device(iscsi or libiscsi)
Patch1077: kvm-qcow2-fix-dangling-refcount-table-entry.patch
# For bz#1081393 - qemu-img will prompt that 'leaked clusters were found' while creating images with '-o preallocation=metadata,cluster_size<=1024'
Patch1078: kvm-qcow2-link-all-L2-meta-updates-in-preallocate.patch
# For bz#1083413 - qemu-kvm: iSCSI: Failure. SENSE KEY:ILLEGAL_REQUEST(5) ASCQ:INVALID_FIELD_IN_CDB(0x2400)
Patch1079: kvm-iscsi-fix-indentation.patch
# For bz#1083413 - qemu-kvm: iSCSI: Failure. SENSE KEY:ILLEGAL_REQUEST(5) ASCQ:INVALID_FIELD_IN_CDB(0x2400)
Patch1080: kvm-iscsi-correctly-propagate-errors-in-iscsi_open.patch
# For bz#1083413 - qemu-kvm: iSCSI: Failure. SENSE KEY:ILLEGAL_REQUEST(5) ASCQ:INVALID_FIELD_IN_CDB(0x2400)
Patch1081: kvm-block-iscsi-query-for-supported-VPD-pages.patch
# For bz#1083413 - qemu-kvm: iSCSI: Failure. SENSE KEY:ILLEGAL_REQUEST(5) ASCQ:INVALID_FIELD_IN_CDB(0x2400)
Patch1082: kvm-block-iscsi-fix-segfault-if-writesame-fails.patch
# For bz#1083413 - qemu-kvm: iSCSI: Failure. SENSE KEY:ILLEGAL_REQUEST(5) ASCQ:INVALID_FIELD_IN_CDB(0x2400)
Patch1083: kvm-iscsi-recognize-invalid-field-ASCQ-from-WRITE-SAME-c.patch
# For bz#1083413 - qemu-kvm: iSCSI: Failure. SENSE KEY:ILLEGAL_REQUEST(5) ASCQ:INVALID_FIELD_IN_CDB(0x2400)
Patch1084: kvm-iscsi-ignore-flushes-on-scsi-generic-devices.patch
# For bz#1083413 - qemu-kvm: iSCSI: Failure. SENSE KEY:ILLEGAL_REQUEST(5) ASCQ:INVALID_FIELD_IN_CDB(0x2400)
Patch1085: kvm-iscsi-always-query-max-WRITE-SAME-length.patch
# For bz#1083413 - qemu-kvm: iSCSI: Failure. SENSE KEY:ILLEGAL_REQUEST(5) ASCQ:INVALID_FIELD_IN_CDB(0x2400)
Patch1086: kvm-iscsi-Don-t-set-error-if-already-set-in-iscsi_do_inq.patch
# For bz#1083413 - qemu-kvm: iSCSI: Failure. SENSE KEY:ILLEGAL_REQUEST(5) ASCQ:INVALID_FIELD_IN_CDB(0x2400)
Patch1087: kvm-iscsi-Remember-to-set-ret-for-iscsi_open-in-error-ca.patch
# For bz#1027565 - fail to reboot guest after migration from RHEL6.5 host to RHEL7.0 host
Patch1088: kvm-qemu_loadvm_state-shadow-SeaBIOS-for-VM-incoming-fro.patch
# For bz#1085701 - Guest hits call trace migrate from RHEL6.5 to RHEL7.0 host with -M 6.1 & balloon & uhci device
Patch1089: kvm-uhci-UNfix-irq-routing-for-RHEL-6-machtypes-RHEL-onl.patch
# For bz#1087980 - CVE-2014-2894 qemu-kvm: QEMU: out of bounds buffer accesses, guest triggerable via IDE SMART [rhel-7.1]
Patch1090: kvm-ide-Correct-improper-smart-self-test-counter-reset-i.patch
# For bz#1094285 - Hot plug CPU not working with RHEL6  machine types running on RHEL7 host.
Patch1091: kvm-pc-add-hot_add_cpu-callback-to-all-machine-types.patch
# For bz#1038914 - Guest can't receive any character transmitted from host after hot unplugging virtserialport then hot plugging again
Patch1092: kvm-char-restore-read-callback-on-a-reattached-hotplug-c.patch
# For bz#1052093 - qcow2 corruptions (leaked clusters after installing a rhel7 guest using virtio_scsi)
Patch1093: kvm-qcow2-Free-preallocated-zero-clusters.patch
# For bz#1052093 - qcow2 corruptions (leaked clusters after installing a rhel7 guest using virtio_scsi)
Patch1094: kvm-qemu-iotests-Discard-preallocated-zero-clusters.patch
# For bz#1066338 - Reduce the migrate cache size during migration causes qemu segment fault
Patch1095: kvm-XBZRLE-Fix-qemu-crash-when-resize-the-xbzrle-cache.patch
# For bz#1066338 - Reduce the migrate cache size during migration causes qemu segment fault
Patch1096: kvm-Provide-init-function-for-ram-migration.patch
# For bz#1066338 - Reduce the migrate cache size during migration causes qemu segment fault
Patch1097: kvm-Init-the-XBZRLE.lock-in-ram_mig_init.patch
# For bz#1066338 - Reduce the migrate cache size during migration causes qemu segment fault
Patch1098: kvm-XBZRLE-Fix-one-XBZRLE-corruption-issues.patch
# For bz#1074913 - migration can not finish with 1024k 'remaining ram' left after hotunplug 4 nics
Patch1099: kvm-Count-used-RAMBlock-pages-for-migration_dirty_pages.patch
# For bz#1095678 - CVE-2013-4148 qemu-kvm: qemu: virtio-net: buffer overflow on invalid state load [rhel-7.1]
Patch1100: kvm-virtio-net-fix-buffer-overflow-on-invalid-state-load.patch
# For bz#1095690 - CVE-2013-4150 qemu-kvm: qemu: virtio-net: out-of-bounds buffer write on invalid state load [rhel-7.1]
Patch1101: kvm-virtio-net-out-of-bounds-buffer-write-on-invalid-sta.patch
# For bz#1095685 - CVE-2013-4149 qemu-kvm: qemu: virtio-net: out-of-bounds buffer write on load [rhel-7.1]
Patch1102: kvm-virtio-net-out-of-bounds-buffer-write-on-load.patch
# For bz#1095695 - CVE-2013-4151 qemu-kvm: qemu: virtio: out-of-bounds buffer write on invalid state load [rhel-7.1]
Patch1103: kvm-virtio-out-of-bounds-buffer-write-on-invalid-state-l.patch
# For bz#1095738 - CVE-2013-6399 qemu-kvm: qemu: virtio: buffer overrun on incoming migration [rhel-7.1]
Patch1104: kvm-virtio-avoid-buffer-overrun-on-incoming-migration.patch
# For bz#1095742 - CVE-2013-4542 qemu-kvm: qemu: virtio-scsi: buffer overrun on invalid state load [rhel-7.1]
Patch1105: kvm-virtio-scsi-fix-buffer-overrun-on-invalid-state-load.patch
# For bz#1095783 - CVE-2014-0182 qemu-kvm: qemu: virtio: out-of-bounds buffer write on state load with invalid config_len [rhel-7.1]
Patch1106: kvm-virtio-validate-config_len-on-load.patch
# For bz#1095766 - CVE-2013-4535 CVE-2013-4536 qemu-kvm: qemu: virtio: insufficient validation of num_sg when mapping [rhel-7.1]
Patch1107: kvm-virtio-validate-num_sg-when-mapping.patch
# For bz#1095766 - CVE-2013-4535 CVE-2013-4536 qemu-kvm: qemu: virtio: insufficient validation of num_sg when mapping [rhel-7.1]
Patch1108: kvm-virtio-allow-mapping-up-to-max-queue-size.patch
# For bz#1095747 - CVE-2013-4541 qemu-kvm: qemu: usb: insufficient sanity checking of setup_index+setup_len in post_load [rhel-7.1]
Patch1109: kvm-usb-sanity-check-setup_index-setup_len-in-post_load.patch
# For bz#1095743 - CVE-2013-4541 qemu-kvm: qemu: usb: insufficient sanity checking of setup_index+setup_len in post_load [rhel-6.5.z]
# For bz#1095747 - CVE-2013-4541 qemu-kvm: qemu: usb: insufficient sanity checking of setup_index+setup_len in post_load [rhel-7.1]
Patch1110: kvm-usb-sanity-check-setup_index-setup_len-in-post_l2.patch
# For bz#1095716 - CVE-2013-4529 qemu-kvm: qemu: hw/pci/pcie_aer.c: buffer overrun on invalid state load [rhel-7.1]
Patch1111: kvm-vmstate-reduce-code-duplication.patch
# For bz#1095716 - CVE-2013-4529 qemu-kvm: qemu: hw/pci/pcie_aer.c: buffer overrun on invalid state load [rhel-7.1]
Patch1112: kvm-vmstate-add-VMS_MUST_EXIST.patch
# For bz#1095716 - CVE-2013-4529 qemu-kvm: qemu: hw/pci/pcie_aer.c: buffer overrun on invalid state load [rhel-7.1]
Patch1113: kvm-vmstate-add-VMSTATE_VALIDATE.patch
# For bz#1095707 - CVE-2013-4527 qemu-kvm: qemu: hpet: buffer overrun on invalid state load [rhel-7.1]
Patch1114: kvm-hpet-fix-buffer-overrun-on-invalid-state-load.patch
# For bz#1095716 - CVE-2013-4529 qemu-kvm: qemu: hw/pci/pcie_aer.c: buffer overrun on invalid state load [rhel-7.1]
Patch1115: kvm-hw-pci-pcie_aer.c-fix-buffer-overruns-on-invalid-sta.patch
# For bz#1096829 - CVE-2014-3461 qemu-kvm: Qemu: usb: fix up post load checks [rhel-7.1]
Patch1116: kvm-usb-fix-up-post-load-checks.patch
# For bz#1097230 - CVE-2014-0222 qemu-kvm: Qemu: qcow1: validate L2 table size to avoid integer overflows [rhel-7.1]
Patch1117: kvm-qcow-correctly-propagate-errors.patch
# For bz#1097230 - CVE-2014-0222 qemu-kvm: Qemu: qcow1: validate L2 table size to avoid integer overflows [rhel-7.1]
Patch1118: kvm-qcow1-Make-padding-in-the-header-explicit.patch
# For bz#1097230 - CVE-2014-0222 qemu-kvm: Qemu: qcow1: validate L2 table size to avoid integer overflows [rhel-7.1]
Patch1119: kvm-qcow1-Check-maximum-cluster-size.patch
# For bz#1097230 - CVE-2014-0222 qemu-kvm: Qemu: qcow1: validate L2 table size to avoid integer overflows [rhel-7.1]
Patch1120: kvm-qcow1-Validate-L2-table-size-CVE-2014-0222.patch
# For bz#1097237 - CVE-2014-0223 qemu-kvm: Qemu: qcow1: validate image size to avoid out-of-bounds memory access [rhel-7.1]
Patch1121: kvm-qcow1-Validate-image-size-CVE-2014-0223.patch
# For bz#1097237 - CVE-2014-0223 qemu-kvm: Qemu: qcow1: validate image size to avoid out-of-bounds memory access [rhel-7.1]
Patch1122: kvm-qcow1-Stricter-backing-file-length-check.patch
# For bz#1098976 - 2x RHEL 5.10 VM running on RHEL 7 KVM have low TCP_STREAM throughput
Patch1123: kvm-zero-initialize-KVM_SET_GSI_ROUTING-input.patch
# For bz#1098976 - 2x RHEL 5.10 VM running on RHEL 7 KVM have low TCP_STREAM throughput
Patch1124: kvm-skip-system-call-when-msi-route-is-unchanged.patch
# For bz#1113009 - Migration failed with virtio-blk from RHEL6.5.0 host to RHEL7.0 host
Patch1125: kvm-Allow-mismatched-virtio-config-len.patch
# For bz#1074219 - qemu core dump when install a RHEL.7 guest(xhci) with migration
Patch1126: kvm-xhci-fix-overflow-in-usb_xhci_post_load.patch
# For bz#1086598 - migrate_cancel wont take effect on previouly wrong migrate -d cmd
Patch1127: kvm-migration-qmp_migrate-keep-working-after-syntax-erro.patch
# For bz#1026314 - qemu-kvm hang when use '-sandbox on'+'vnc'+'hda'
Patch1128: kvm-seccomp-add-shmctl-mlock-and-munlock-to-the-syscall-.patch
# For bz#1076326 - qemu-kvm does not quit when booting guest w/ 161 vcpus and "-no-kvm"
Patch1129: kvm-exit-when-no-kvm-and-vcpu-count-160.patch
# For bz#1086987 - src qemu crashed when starting migration in inmigrate mode
Patch1130: kvm-Disallow-outward-migration-while-awaiting-incoming-m.patch
# For bz#1088695 - there are four "gluster" in qemu-img supported format list
# For bz#1093983 - there are three "nbd" in qemu-img supported format list
Patch1131: kvm-block-Ignore-duplicate-or-NULL-format_name-in-bdrv_i.patch
# For bz#1097020 - [RFE] qemu-img: Add/improve Disk2VHD tools creating VHDX images
Patch1132: kvm-block-vhdx-account-for-identical-header-sections.patch
# For bz#1095877 - segmentation fault in qemu-kvm due to use-after-free of a SCSIGenericReq (host device pass-through)
Patch1133: kvm-aio-Fix-use-after-free-in-cancellation-path.patch
# For bz#1021788 - the error message "scsi generic interface too old" is wrong more often than not
Patch1134: kvm-scsi-disk-Improve-error-messager-if-can-t-get-versio.patch
# For bz#1021788 - the error message "scsi generic interface too old" is wrong more often than not
Patch1135: kvm-scsi-Improve-error-messages-more.patch
# For bz#1096645 - [FJ7.0 Bug] RHEL7.0 guest attaching 150 or more virtio-blk disks fails to start up
Patch1136: kvm-memory-Don-t-call-memory_region_update_coalesced_ran.patch
# For bz#1098602 - kvmclock: Ensure time in migration never goes backward (backport)
Patch1137: kvm-kvmclock-Ensure-time-in-migration-never-goes-backwar.patch
# For bz#1098602 - kvmclock: Ensure time in migration never goes backward (backport)
Patch1138: kvm-kvmclock-Ensure-proper-env-tsc-value-for-kvmclock_cu.patch
# For bz#990724 - qemu-kvm failing when invalid machine type is provided
Patch1139: kvm-vl.c-Output-error-on-invalid-machine-type.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1140: kvm-migration-dump-vmstate-info-as-a-json-file-for-stati.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1141: kvm-vmstate-static-checker-script-to-validate-vmstate-ch.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1142: kvm-tests-vmstate-static-checker-add-dump1-and-dump2-fil.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1143: kvm-tests-vmstate-static-checker-incompat-machine-types.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1144: kvm-tests-vmstate-static-checker-add-version-error-in-ma.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1145: kvm-tests-vmstate-static-checker-version-mismatch-inside.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1146: kvm-tests-vmstate-static-checker-minimum_version_id-chec.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1147: kvm-tests-vmstate-static-checker-remove-a-section.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1148: kvm-tests-vmstate-static-checker-remove-a-field.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1149: kvm-tests-vmstate-static-checker-remove-last-field-in-a-.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1150: kvm-tests-vmstate-static-checker-change-description-name.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1151: kvm-tests-vmstate-static-checker-remove-Fields.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1152: kvm-tests-vmstate-static-checker-remove-Description.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1153: kvm-tests-vmstate-static-checker-remove-Description-insi.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1154: kvm-tests-vmstate-static-checker-remove-a-subsection.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1155: kvm-tests-vmstate-static-checker-remove-Subsections.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1156: kvm-tests-vmstate-static-checker-add-substructure-for-us.patch
# For bz#1118707 - VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info
Patch1157: kvm-tests-vmstate-static-checker-add-size-mismatch-insid.patch
# For bz#1116728 - Backport qemu_bh_schedule() race condition fix
Patch1158: kvm-aio-fix-qemu_bh_schedule-bh-ctx-race-condition.patch
# For bz#999789 - qemu should give a more friendly prompt when didn't specify read-only for VMDK format disk
Patch1159: kvm-block-Improve-driver-whitelist-checks.patch
# For bz#1029271 - Format specific information (create type) was wrong when create it specified subformat='streamOptimized'
Patch1160: kvm-vmdk-Fix-format-specific-information-create-type-for.patch
# For bz#1095645 - vectors of virtio-scsi-pci will be 0 when set vectors>=129
Patch1161: kvm-virtio-pci-Report-an-error-when-msix-vectors-init-fa.patch
# For bz#1096576 - QEMU core dumped when boot up two scsi-hd disk on the same virtio-scsi-pci controller in Intel host
Patch1162: kvm-scsi-Report-error-when-lun-number-is-in-use.patch
# For bz#1017685 - Gluster etc. should not be a dependency of vscclient and libcacard
Patch1163: kvm-util-Split-out-exec_dir-from-os_find_datadir.patch
# For bz#1017685 - Gluster etc. should not be a dependency of vscclient and libcacard
Patch1164: kvm-rules.mak-fix-obj-to-a-real-relative-path.patch
# For bz#1017685 - Gluster etc. should not be a dependency of vscclient and libcacard
Patch1165: kvm-rules.mak-allow-per-object-cflags-and-libs.patch
# For bz#1017685 - Gluster etc. should not be a dependency of vscclient and libcacard
Patch1166: kvm-block-use-per-object-cflags-and-libs.patch
# For bz#1039791 - qemu-img creates truncated VMDK image with subformat=twoGbMaxExtentFlat
Patch1167: kvm-vmdk-Fix-creating-big-description-file.patch
# For bz#1065724 - rx filter incorrect when guest disables VLAN filtering
Patch1168: kvm-virtio-net-Do-not-filter-VLANs-without-F_CTRL_VLAN.patch
# For bz#1065724 - rx filter incorrect when guest disables VLAN filtering
Patch1169: kvm-virtio-net-add-vlan-receive-state-to-RxFilterInfo.patch
# For bz#1116941 - Return value of virtio_load not checked in virtio_rng_load
Patch1170: kvm-virtio-rng-check-return-value-of-virtio_load.patch
# For bz#1074403 - qemu-kvm can not give any warning hint when set sndbuf with negative value
Patch1171: kvm-qapi-treat-all-negative-return-of-strtosz_suffix-as-.patch
# For bz#1107821 - rdma migration: seg if destination isn't listening
Patch1172: kvm-rdma-bug-fixes.patch
# For bz#1122151 - Pass close from qemu-ga
Patch1173: kvm-virtio-serial-report-frontend-connection-state-via-m.patch
# For bz#1122151 - Pass close from qemu-ga
Patch1174: kvm-char-report-frontend-open-closed-state-in-query-char.patch
# For bz#1129552 - backport "acpi: fix tables for no-hpet configuration"
Patch1175: kvm-acpi-fix-tables-for-no-hpet-configuration.patch
# For bz#1130603 - advertise active commit to libvirt
Patch1176: kvm-mirror-Fix-resource-leak-when-bdrv_getlength-fails.patch
# For bz#1130603 - advertise active commit to libvirt
Patch1177: kvm-blockjob-Add-block_job_yield.patch
# For bz#1130603 - advertise active commit to libvirt
Patch1178: kvm-mirror-Go-through-ready-complete-process-for-0-len-i.patch
# For bz#1130603 - advertise active commit to libvirt
Patch1179: kvm-qemu-iotests-Test-BLOCK_JOB_READY-event-for-0Kb-imag.patch
# For bz#1130603 - advertise active commit to libvirt
Patch1180: kvm-block-make-top-argument-to-block-commit-optional.patch
# For bz#1130603 - advertise active commit to libvirt
Patch1181: kvm-qemu-iotests-Test-0-length-image-for-mirror.patch
# For bz#1130603 - advertise active commit to libvirt
Patch1182: kvm-mirror-Fix-qiov-size-for-short-requests.patch
# For bz#1064260 - Handle properly --enable-fstack-protector option
Patch1183: kvm-Enforce-stack-protector-usage.patch
# For bz#1134408 - [HP 7.1 FEAT] Increase qemu-kvm's VCPU limit to 240
Patch1184: kvm-pc-increase-maximal-VCPU-count-to-240.patch
# For bz#1136534 - glusterfs backend does not support discard
Patch1185: kvm-gluster-Add-discard-support-for-GlusterFS-block-driv.patch
# For bz#1088150 - qemu-img coredumpd when try to create a gluster format image
Patch1186: kvm-gluster-default-scheme-to-gluster-and-host-to-localh.patch
# For bz#996011 - vlan and queues options cause core dumped when qemu-kvm process quit(or ctrl+c)
Patch1187: kvm-qdev-properties-system.c-Allow-vlan-or-netdev-for-de.patch
# For bz#1054077 - qemu crash when reboot win7 guest with spice display
Patch1189: kvm-spice-move-qemu_spice_display_-from-spice-graphics-t.patch
# For bz#1054077 - qemu crash when reboot win7 guest with spice display
Patch1190: kvm-spice-move-spice_server_vm_-start-stop-calls-into-qe.patch
# For bz#1054077 - qemu crash when reboot win7 guest with spice display
Patch1191: kvm-spice-stop-server-for-qxl-hard-reset.patch
# For bz#1064156 - [qxl] The guest show black screen while resumed guest which managedsaved in pmsuspended status.
Patch1192: kvm-qemu-Adjust-qemu-wakeup.patch
# For bz#1122147 - CVE-2014-5263 vmstate_xhci_event: fix unterminated field list
Patch1193: kvm-vmstate_xhci_event-fix-unterminated-field-list.patch
# For bz#1122147 - CVE-2014-5263 vmstate_xhci_event: fix unterminated field list
Patch1194: kvm-vmstate_xhci_event-bug-compat-with-RHEL-7.0-RHEL-onl.patch
# For bz#1139702 - pflash (UEFI varstore) migration shortcut for libvirt [RHEL]
Patch1195: kvm-pflash_cfi01-write-flash-contents-to-bdrv-on-incomin.patch
# For bz#1123372 - qemu-kvm crashed when doing iofuzz testing
Patch1196: kvm-ide-test-Add-enum-value-for-DEV.patch
# For bz#1123372 - qemu-kvm crashed when doing iofuzz testing
Patch1197: kvm-ide-test-Add-FLUSH-CACHE-test-case.patch
# For bz#1123372 - qemu-kvm crashed when doing iofuzz testing
Patch1198: kvm-ide-Fix-segfault-when-flushing-a-device-that-doesn-t.patch
# For bz#1139118 - CVE-2014-3615 qemu-kvm: Qemu: crash when guest sets high resolution [rhel-7.1]
Patch1201: kvm-vbe-make-bochs-dispi-interface-return-the-correct-me.patch
# For bz#1139118 - CVE-2014-3615 qemu-kvm: Qemu: crash when guest sets high resolution [rhel-7.1]
Patch1202: kvm-vbe-rework-sanity-checks.patch
# For bz#1139118 - CVE-2014-3615 qemu-kvm: Qemu: crash when guest sets high resolution [rhel-7.1]
Patch1203: kvm-spice-display-add-display-channel-id-to-the-debug-me.patch
# For bz#1139118 - CVE-2014-3615 qemu-kvm: Qemu: crash when guest sets high resolution [rhel-7.1]
Patch1204: kvm-spice-make-sure-we-don-t-overflow-ssd-buf.patch
# For bz#1105880 - bug in scsi_block_new_request() function introduced by upstream commit 137745c5c60f083ec982fe9e861e8c16ebca1ba8
Patch1205: kvm-scsi-disk-fix-bug-in-scsi_block_new_request-introduc.patch
# For bz#1131316 - fail to specify wwn for virtual IDE CD-ROM
Patch1206: kvm-ide-Add-wwn-support-to-IDE-ATAPI-drive.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1207: kvm-vmdk-Allow-vmdk_create-to-work-with-protocol.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1208: kvm-block-make-vdi-bounds-check-match-upstream.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1209: kvm-vdi-say-why-an-image-is-bad.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1210: kvm-block-do-not-abuse-EMEDIUMTYPE.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1211: kvm-cow-correctly-propagate-errors.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1212: kvm-block-Use-correct-width-in-format-strings.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1213: kvm-vdi-remove-double-conversion.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1214: kvm-block-vdi-Error-out-immediately-in-vdi_create.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1215: kvm-vpc-Implement-.bdrv_has_zero_init.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1216: kvm-block-vpc-use-QEMU_PACKED-for-on-disk-structures.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1217: kvm-block-allow-bdrv_unref-to-be-passed-NULL-pointers.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1218: kvm-block-vdi-use-block-layer-ops-in-vdi_create-instead-.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1219: kvm-block-use-the-standard-ret-instead-of-result.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1220: kvm-block-vpc-use-block-layer-ops-in-vpc_create-instead-.patch
# For bz#1098086 - RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs)
Patch1221: kvm-block-iotest-update-084-to-test-static-VDI-image-cre.patch
# For bz#1122925 - Maintain relative path to backing file image during live merge (block-commit)
Patch1222: kvm-block-add-helper-function-to-determine-if-a-BDS-is-i.patch
# For bz#1122925 - Maintain relative path to backing file image during live merge (block-commit)
Patch1223: kvm-block-extend-block-commit-to-accept-a-string-for-the.patch
# For bz#1122925 - Maintain relative path to backing file image during live merge (block-commit)
Patch1224: kvm-block-add-backing-file-option-to-block-stream.patch
# For bz#1122925 - Maintain relative path to backing file image during live merge (block-commit)
Patch1225: kvm-block-add-__com.redhat_change-backing-file-qmp-comma.patch
# For bz#1116117 - [Intel 7.1 FEAT] Broadwell new instructions support for KVM - qemu-kvm
Patch1226: kvm-target-i386-Broadwell-CPU-model.patch
# For bz#1116117 - [Intel 7.1 FEAT] Broadwell new instructions support for KVM - qemu-kvm
Patch1227: kvm-pc-Add-Broadwell-CPUID-compatibility-bits.patch
# For bz#1142290 - guest is stuck when setting balloon memory with large guest-stats-polling-interval
Patch1228: kvm-virtio-balloon-fix-integer-overflow-in-memory-stats-.patch
# For bz#980747 - flood with 'xhci: wrote doorbell while xHC stopped or paused' when redirected USB Webcam from usb-host with xHCI controller
Patch1229: kvm-usb-hcd-xhci-QOM-Upcast-Sweep.patch
# For bz#980747 - flood with 'xhci: wrote doorbell while xHC stopped or paused' when redirected USB Webcam from usb-host with xHCI controller
Patch1230: kvm-usb-hcd-xhci-QOM-parent-field-cleanup.patch
# For bz#1046873 - fail to be recognized the hotpluging usb-storage device with xhci controller in win2012R2 guest
Patch1231: kvm-uhci-egsm-fix.patch
# For bz#1046574 - fail to passthrough the USB speaker redirected from usb-redir with xhci controller
# For bz#1088116 - qemu crash when device_del usb-redir
Patch1232: kvm-usb-redir-fix-use-after-free.patch
# For bz#980833 - xhci: FIXME: endpoint stopped w/ xfers running, data might be lost
Patch1233: kvm-xhci-remove-leftover-debug-printf.patch
# For bz#980833 - xhci: FIXME: endpoint stopped w/ xfers running, data might be lost
Patch1234: kvm-xhci-add-tracepoint-for-endpoint-state-changes.patch
# For bz#980833 - xhci: FIXME: endpoint stopped w/ xfers running, data might be lost
Patch1235: kvm-xhci-add-port-to-slot_address-tracepoint.patch
# For bz#1075846 - qemu-kvm core dumped when hotplug/unhotplug USB3.0 device multi times
Patch1236: kvm-usb-parallelize-usb3-streams.patch
# For bz#1075846 - qemu-kvm core dumped when hotplug/unhotplug USB3.0 device multi times
Patch1237: kvm-xhci-Init-a-transfers-xhci-slotid-and-epid-member-on.patch
# For bz#980833 - xhci: FIXME: endpoint stopped w/ xfers running, data might be lost
Patch1238: kvm-xhci-Add-xhci_epid_to_usbep-helper-function.patch
# For bz#980833 - xhci: FIXME: endpoint stopped w/ xfers running, data might be lost
Patch1239: kvm-xhci-Fix-memory-leak-on-xhci_disable_ep.patch
# For bz#1075846 - qemu-kvm core dumped when hotplug/unhotplug USB3.0 device multi times
Patch1240: kvm-usb-Also-reset-max_packet_size-on-ep_reset.patch
# For bz#1075846 - qemu-kvm core dumped when hotplug/unhotplug USB3.0 device multi times
Patch1241: kvm-usb-Fix-iovec-memleak-on-combined-packet-free.patch
# For bz#980747 - flood with 'xhci: wrote doorbell while xHC stopped or paused' when redirected USB Webcam from usb-host with xHCI controller
Patch1242: kvm-usb-hcd-xhci-Remove-unused-sstreamsm-member-from-XHC.patch
# For bz#980747 - flood with 'xhci: wrote doorbell while xHC stopped or paused' when redirected USB Webcam from usb-host with xHCI controller
Patch1243: kvm-usb-hcd-xhci-Remove-unused-cancelled-member-from-XHC.patch
# For bz#980747 - flood with 'xhci: wrote doorbell while xHC stopped or paused' when redirected USB Webcam from usb-host with xHCI controller
Patch1244: kvm-usb-hcd-xhci-Report-completion-of-active-transfer-wi.patch
# For bz#980747 - flood with 'xhci: wrote doorbell while xHC stopped or paused' when redirected USB Webcam from usb-host with xHCI controller
Patch1245: kvm-usb-hcd-xhci-Update-endpoint-context-dequeue-pointer.patch
# For bz#980833 - xhci: FIXME: endpoint stopped w/ xfers running, data might be lost
Patch1246: kvm-xhci-Add-a-few-missing-checks-for-disconnected-devic.patch
# For bz#1111450 - Guest crash when hotplug usb while disable virt_use_usb
Patch1247: kvm-usb-Add-max_streams-attribute-to-endpoint-info.patch
# For bz#1111450 - Guest crash when hotplug usb while disable virt_use_usb
Patch1248: kvm-usb-Add-usb_device_alloc-free_streams.patch
# For bz#980833 - xhci: FIXME: endpoint stopped w/ xfers running, data might be lost
Patch1249: kvm-xhci-Call-usb_device_alloc-free_streams.patch
# For bz#1111450 - Guest crash when hotplug usb while disable virt_use_usb
Patch1250: kvm-uhci-invalidate-queue-on-device-address-changes.patch
# For bz#949385 - passthrough USB speaker to win2012 guest fail to work well
Patch1251: kvm-xhci-iso-fix-time-calculation.patch
# For bz#949385 - passthrough USB speaker to win2012 guest fail to work well
Patch1252: kvm-xhci-iso-allow-for-some-latency.patch
# For bz#980747 - flood with 'xhci: wrote doorbell while xHC stopped or paused' when redirected USB Webcam from usb-host with xHCI controller
Patch1253: kvm-xhci-switch-debug-printf-to-tracepoint.patch
# For bz#980833 - xhci: FIXME: endpoint stopped w/ xfers running, data might be lost
Patch1254: kvm-xhci-use-DPRINTF-instead-of-fprintf-stderr.patch
# For bz#980833 - xhci: FIXME: endpoint stopped w/ xfers running, data might be lost
Patch1255: kvm-xhci-child-detach-fix.patch
# For bz#1075846 - qemu-kvm core dumped when hotplug/unhotplug USB3.0 device multi times
Patch1256: kvm-usb-add-usb_pick_speed.patch
# For bz#980833 - xhci: FIXME: endpoint stopped w/ xfers running, data might be lost
Patch1257: kvm-xhci-make-port-reset-trace-point-more-verbose.patch
# For bz#1111450 - Guest crash when hotplug usb while disable virt_use_usb
Patch1258: kvm-usb-initialize-libusb_device-to-avoid-crash.patch
# For bz#1097363 - qemu ' KVM internal error. Suberror: 1'  when  query cpu frequently during pxe boot in Intel "Q95xx" host
Patch1259: kvm-target-i386-get-CPL-from-SS.DPL.patch
# For bz#1088112 - [Fujitsu 7.1 FEAT]:QEMU: capturing trace data all the time using ftrace-based tracing
Patch1260: kvm-trace-use-unique-Red-Hat-version-number-in-simpletra.patch
# For bz#1088112 - [Fujitsu 7.1 FEAT]:QEMU: capturing trace data all the time using ftrace-based tracing
Patch1261: kvm-trace-add-pid-field-to-simpletrace-record.patch
# For bz#1088112 - [Fujitsu 7.1 FEAT]:QEMU: capturing trace data all the time using ftrace-based tracing
Patch1262: kvm-simpletrace-add-support-for-trace-record-pid-field.patch
# For bz#1088112 - [Fujitsu 7.1 FEAT]:QEMU: capturing trace data all the time using ftrace-based tracing
Patch1263: kvm-simpletrace-add-simpletrace.py-no-header-option.patch
# For bz#1088112 - [Fujitsu 7.1 FEAT]:QEMU: capturing trace data all the time using ftrace-based tracing
Patch1264: kvm-trace-extract-stap_escape-function-for-reuse.patch
# For bz#1088112 - [Fujitsu 7.1 FEAT]:QEMU: capturing trace data all the time using ftrace-based tracing
Patch1265: kvm-trace-add-tracetool-simpletrace_stap-format.patch
# For bz#1088112 - [Fujitsu 7.1 FEAT]:QEMU: capturing trace data all the time using ftrace-based tracing
Patch1266: kvm-trace-install-simpletrace-SystemTap-tapset.patch
# For bz#1088112 - [Fujitsu 7.1 FEAT]:QEMU: capturing trace data all the time using ftrace-based tracing
Patch1267: kvm-trace-install-trace-events-file.patch
# For bz#1088112 - [Fujitsu 7.1 FEAT]:QEMU: capturing trace data all the time using ftrace-based tracing
Patch1268: kvm-trace-add-SystemTap-init-scripts-for-simpletrace-bri.patch
# For bz#1088112 - [Fujitsu 7.1 FEAT]:QEMU: capturing trace data all the time using ftrace-based tracing
Patch1269: kvm-trace-add-systemtap-initscript-README-file-to-RPM.patch
# For bz#1152969 - Qemu-kvm got stuck when migrate to wrong RDMA ip
Patch1270: kvm-rdma-Fix-block-during-rdma-migration.patch
# For bz#1026314 - BUG: qemu-kvm hang when use '-sandbox on'+'vnc'+'hda'
Patch1271: kvm-seccomp-add-semctl-to-the-syscall-whitelist.patch
# For bz#1098602 - kvmclock: Ensure time in migration never goes backward (backport)
# For bz#1130428 - After migration of RHEL7.1 guest with "-vga qxl", GUI console is hang
Patch1272: kvm-Revert-kvmclock-Ensure-proper-env-tsc-value-for-kvmc.patch
# For bz#1098602 - kvmclock: Ensure time in migration never goes backward (backport)
# For bz#1130428 - After migration of RHEL7.1 guest with "-vga qxl", GUI console is hang
Patch1273: kvm-Revert-kvmclock-Ensure-time-in-migration-never-goes-.patch
# For bz#1098602 - kvmclock: Ensure time in migration never goes backward (backport)
# For bz#1130428 - After migration of RHEL7.1 guest with "-vga qxl", GUI console is hang
Patch1274: kvm-Introduce-cpu_clean_all_dirty.patch
# For bz#1098602 - kvmclock: Ensure time in migration never goes backward (backport)
# For bz#1130428 - After migration of RHEL7.1 guest with "-vga qxl", GUI console is hang
Patch1275: kvm-kvmclock-Ensure-proper-env-tsc-value-for-kvmclock.v2.patch
# For bz#1098602 - kvmclock: Ensure time in migration never goes backward (backport)
# For bz#1130428 - After migration of RHEL7.1 guest with "-vga qxl", GUI console is hang
Patch1276: kvm-kvmclock-Ensure-time-in-migration-never-goes-back.v2.patch
# For bz#1144820 - CVE-2014-3640 qemu-kvm: qemu: slirp: NULL pointer deref in sosendto() [rhel-7.1]
Patch1277: kvm-slirp-udp-fix-NULL-pointer-dereference-because-of-un.patch
# For bz#1049734 - PCI: QEMU crash on illegal operation: attaching a function to a non multi-function device
Patch1278: kvm-hw-pci-fix-error-flow-in-pci-multifunction-init.patch
# For bz#1111107 - Remove Q35 machine type from qemu-kvm
Patch1279: kvm-rhel-Drop-machine-type-pc-q35-rhel7.0.0.patch
# For bz#1088822 - hot-plug a virtio-scsi disk via 'blockdev-add' always cause QEMU quit
Patch1280: kvm-virtio-scsi-Plug-memory-leak-on-virtio_scsi_push_eve.patch
# For bz#1089606 - QEMU will not reject invalid number of queues (num_queues = 0) specified for virtio-scsi
Patch1281: kvm-virtio-scsi-Report-error-if-num_queues-is-0-or-too-l.patch
# For bz#1089606 - QEMU will not reject invalid number of queues (num_queues = 0) specified for virtio-scsi
Patch1282: kvm-virtio-scsi-Fix-memory-leak-when-realize-failed.patch
# For bz#1089606 - QEMU will not reject invalid number of queues (num_queues = 0) specified for virtio-scsi
Patch1283: kvm-virtio-scsi-Fix-num_queue-input-validation.patch
# For bz#1104748 - 48% reduction in IO performance for KVM guest, io=native
Patch1284: kvm-Revert-linux-aio-use-event-notifiers.patch
# For bz#1088176 - QEMU fail to check whether duplicate ID for block device drive using 'blockdev-add' to hotplug
Patch1285: kvm-libcacard-link-against-qemu-error.o-for-error_report.patch
# For bz#1088176 - QEMU fail to check whether duplicate ID for block device drive using 'blockdev-add' to hotplug
Patch1286: kvm-error-Add-error_abort.patch
# For bz#1088176 - QEMU fail to check whether duplicate ID for block device drive using 'blockdev-add' to hotplug
Patch1287: kvm-blockdev-Fail-blockdev-add-with-encrypted-images.patch
# For bz#1088176 - QEMU fail to check whether duplicate ID for block device drive using 'blockdev-add' to hotplug
Patch1288: kvm-blockdev-Fix-NULL-pointer-dereference-in-blockdev-ad.patch
# For bz#1088176 - QEMU fail to check whether duplicate ID for block device drive using 'blockdev-add' to hotplug
Patch1289: kvm-qemu-iotests-Test-a-few-blockdev-add-error-cases.patch
# For bz#1088176 - QEMU fail to check whether duplicate ID for block device drive using 'blockdev-add' to hotplug
Patch1290: kvm-block-Add-errp-to-bdrv_new.patch
# For bz#1088176 - QEMU fail to check whether duplicate ID for block device drive using 'blockdev-add' to hotplug
Patch1291: kvm-qemu-img-Avoid-duplicate-block-device-IDs.patch
# For bz#1088176 - QEMU fail to check whether duplicate ID for block device drive using 'blockdev-add' to hotplug
Patch1292: kvm-block-Catch-duplicate-IDs-in-bdrv_new.patch
# For bz#1138691 - Allow qemu-img to bypass the host cache (check, compare, convert, rebase, amend)
Patch1293: kvm-qemu-img-Allow-source-cache-mode-specification.patch
# For bz#1138691 - Allow qemu-img to bypass the host cache (check, compare, convert, rebase, amend)
Patch1294: kvm-qemu-img-Allow-cache-mode-specification-for-amend.patch
# For bz#1138691 - Allow qemu-img to bypass the host cache (check, compare, convert, rebase, amend)
Patch1295: kvm-qemu-img-clarify-src_cache-option-documentation.patch
# For bz#1138691 - Allow qemu-img to bypass the host cache (check, compare, convert, rebase, amend)
Patch1296: kvm-qemu-img-fix-rebase-src_cache-option-documentation.patch
# For bz#1138691 - Allow qemu-img to bypass the host cache (check, compare, convert, rebase, amend)
Patch1297: kvm-qemu-img-fix-img_compare-flags-error-path.patch
# For bz#1141667 - Qemu crashed if reboot guest after hot remove AC97 sound device
Patch1298: kvm-ac97-register-reset-via-qom.patch
# For bz#1085232 - Ilegal guest requests on block devices pause the VM
Patch1299: kvm-virtio-blk-Factor-common-checks-out-of-virtio_blk_ha.patch
# For bz#1085232 - Ilegal guest requests on block devices pause the VM
Patch1300: kvm-virtio-blk-Bypass-error-action-and-I-O-accounting-on.patch
# For bz#1085232 - Ilegal guest requests on block devices pause the VM
Patch1301: kvm-virtio-blk-Treat-read-write-beyond-end-as-invalid.patch
# For bz#1085232 - Ilegal guest requests on block devices pause the VM
Patch1302: kvm-ide-Treat-read-write-beyond-end-as-invalid.patch
# For bz#1085232 - Ilegal guest requests on block devices pause the VM
Patch1303: kvm-ide-only-constrain-read-write-requests-to-drive-size.patch
# For bz#1161563 - invalid QEMU NOTEs in vmcore that is dumped for multi-VCPU guests
Patch1304: kvm-dump-RHEL-specific-fix-for-CPUState-bug-introduced-b.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1305: kvm-dump-guest-memory-Check-for-the-correct-return-value.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1306: kvm-dump-const-qualify-the-buf-of-WriteCoreDumpFunction.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1307: kvm-dump-add-argument-to-write_elfxx_notes.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1308: kvm-dump-add-API-to-write-header-of-flatten-format.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1309: kvm-dump-add-API-to-write-vmcore.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1310: kvm-dump-add-API-to-write-elf-notes-to-buffer.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1311: kvm-dump-add-support-for-lzo-snappy.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1312: kvm-dump-add-members-to-DumpState-and-init-some-of-them.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1313: kvm-dump-add-API-to-write-dump-header.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1314: kvm-dump-add-API-to-write-dump_bitmap.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1315: kvm-dump-add-APIs-to-operate-DataCache.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1316: kvm-dump-add-API-to-write-dump-pages.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1317: kvm-dump-Drop-qmp_dump_guest_memory-stub-and-build-for-a.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1318: kvm-dump-make-kdump-compressed-format-available-for-dump.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1319: kvm-Define-the-architecture-for-compressed-dump-format.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1320: kvm-dump-add-query-dump-guest-memory-capability-command.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1321: kvm-dump-Drop-pointless-error_is_set-DumpState-member-er.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1322: kvm-dump-fill-in-the-flat-header-signature-more-pleasing.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1323: kvm-dump-simplify-write_start_flat_header.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1324: kvm-dump-eliminate-DumpState.page_shift-guest-s-page-shi.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1325: kvm-dump-eliminate-DumpState.page_size-guest-s-page-size.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1326: kvm-dump-select-header-bitness-based-on-ELF-class-not-EL.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1327: kvm-dump-hoist-lzo_init-from-get_len_buf_out-to-dump_ini.patch
# For bz#1157798 - [FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command
Patch1328: kvm-dump-simplify-get_len_buf_out.patch
# For bz#1087724 - [Fujitsu 7.1 FEAT]: qemu-img should use fallocate() system call for "preallocation=full" option
Patch1329: kvm-rename-parse_enum_option-to-qapi_enum_parse-and-make.patch
# For bz#1087724 - [Fujitsu 7.1 FEAT]: qemu-img should use fallocate() system call for "preallocation=full" option
Patch1330: kvm-qapi-introduce-PreallocMode-and-new-PreallocModes-fu.patch
# For bz#1087724 - [Fujitsu 7.1 FEAT]: qemu-img should use fallocate() system call for "preallocation=full" option
Patch1331: kvm-raw-posix-Add-falloc-and-full-preallocation-option.patch
# For bz#1087724 - [Fujitsu 7.1 FEAT]: qemu-img should use fallocate() system call for "preallocation=full" option
Patch1332: kvm-qcow2-Add-falloc-and-full-preallocation-option.patch
# For bz#1161890 - [abrt] qemu-kvm: pixman_image_get_data(): qemu-kvm killed by SIGSEGV
Patch1333: kvm-vga-fix-invalid-read-after-free.patch
# For bz#1140618 - Should replace "qemu-system-i386" by "/usr/libexec/qemu-kvm" in manpage of qemu-kvm for our official qemu-kvm build
Patch1334: kvm-Use-qemu-kvm-in-documentation-instead-of-qemu-system.patch
# For bz#1157645 - CVE-2014-7815 qemu-kvm: qemu: vnc: insufficient bits_per_pixel from the client sanitization [rhel-7.1]
Patch1335: kvm-vnc-sanitize-bits_per_pixel-from-the-client.patch
# For bz#1138639 - fail to login spice session with password + expire time
Patch1336: kvm-spice-call-qemu_spice_set_passwd-during-init.patch
# For bz#1160237 - qemu-img convert intermittently corrupts output images
Patch1337: kvm-block-raw-posix-Try-both-FIEMAP-and-SEEK_HOLE.patch
# For bz#1160237 - qemu-img convert intermittently corrupts output images
Patch1338: kvm-block-raw-posix-Fix-disk-corruption-in-try_fiemap.patch
# For bz#1160237 - qemu-img convert intermittently corrupts output images
Patch1339: kvm-block-raw-posix-use-seek_hole-ahead-of-fiemap.patch
# For bz#1160237 - qemu-img convert intermittently corrupts output images
Patch1340: kvm-raw-posix-Fix-raw_co_get_block_status-after-EOF.patch
# For bz#1160237 - qemu-img convert intermittently corrupts output images
Patch1341: kvm-raw-posix-raw_co_get_block_status-return-value.patch
# For bz#1160237 - qemu-img convert intermittently corrupts output images
Patch1342: kvm-raw-posix-SEEK_HOLE-suffices-get-rid-of-FIEMAP.patch
# For bz#1160237 - qemu-img convert intermittently corrupts output images
Patch1343: kvm-raw-posix-The-SEEK_HOLE-code-is-flawed-rewrite-it.patch
# For bz#1071776 - Migration "expected downtime" does not refresh after reset to a new value
Patch1344: kvm-migration-static-variables-will-not-be-reset-at-seco.patch
# For bz#1098976 - 2x RHEL 5.10 VM running on RHEL 7 KVM have low TCP_STREAM throughput
Patch1345: kvm-vfio-pci-Add-debug-config-options-to-disable-MSI-X-K.patch
# For bz#1098976 - 2x RHEL 5.10 VM running on RHEL 7 KVM have low TCP_STREAM throughput
Patch1346: kvm-vfio-correct-debug-macro-typo.patch
# For bz#1098976 - 2x RHEL 5.10 VM running on RHEL 7 KVM have low TCP_STREAM throughput
Patch1347: kvm-vfio-pci-Fix-MSI-X-debug-code.patch
# For bz#1098976 - 2x RHEL 5.10 VM running on RHEL 7 KVM have low TCP_STREAM throughput
Patch1348: kvm-vfio-pci-Fix-MSI-X-masking-performance.patch
# For bz#1098976 - 2x RHEL 5.10 VM running on RHEL 7 KVM have low TCP_STREAM throughput
Patch1349: kvm-vfio-Fix-MSI-X-vector-expansion.patch
# For bz#1098976 - 2x RHEL 5.10 VM running on RHEL 7 KVM have low TCP_STREAM throughput
Patch1350: kvm-vfio-Don-t-cache-MSIMessage.patch
# For bz#1046007 - qemu-kvm aborted when hot plug PCI device to guest with romfile and rombar=0
Patch1351: kvm-hw-pci-fixed-error-flow-in-pci_qdev_init.patch
# For bz#1046007 - qemu-kvm aborted when hot plug PCI device to guest with romfile and rombar=0
Patch1352: kvm-hw-pci-fixed-hotplug-crash-when-using-rombar-0-with-.patch
# For bz#1074219 - qemu core dump when install a RHEL.7 guest(xhci) with migration
Patch1353: kvm-xhci-add-sanity-checks-to-xhci_lookup_uport.patch
# For bz#1140742 - Enable native support for Ceph
Patch1354: kvm-Revert-Build-ceph-rbd-only-for-rhev.patch
# For bz#1140742 - Enable native support for Ceph
Patch1355: kvm-Revert-rbd-Only-look-for-qemu-specific-copy-of-librb.patch
# For bz#1140742 - Enable native support for Ceph
Patch1356: kvm-Revert-rbd-link-and-load-librbd-dynamically.patch
# For bz#1002493 - qemu-img convert rate about 100k/second from qcow2/raw to vmdk format on nfs system file
Patch1357: kvm-qemu-iotests-Test-case-for-backing-file-deletion.patch
# For bz#1134237 - Opening malformed VMDK description file should fail
Patch1358: kvm-qemu-iotests-Add-sample-image-and-test-for-VMDK-vers.patch
# For bz#1134237 - Opening malformed VMDK description file should fail
Patch1359: kvm-vmdk-Check-VMFS-extent-line-field-number.patch
# For bz#1002493 - qemu-img convert rate about 100k/second from qcow2/raw to vmdk format on nfs system file
Patch1360: kvm-qemu-iotests-Introduce-_unsupported_imgopts.patch
# For bz#1002493 - qemu-img convert rate about 100k/second from qcow2/raw to vmdk format on nfs system file
Patch1361: kvm-qemu-iotests-Add-_unsupported_imgopts-for-vmdk-subfo.patch
# For bz#1134241 - QEMU fails to correctly read/write on VMDK with big flat extent
Patch1362: kvm-vmdk-Fix-big-flat-extent-IO.patch
# For bz#1134251 - Opening an obviously truncated VMDK image should fail
Patch1363: kvm-vmdk-Check-for-overhead-when-opening.patch
# For bz#1134251 - Opening an obviously truncated VMDK image should fail
Patch1364: kvm-block-vmdk-add-basic-.bdrv_check-support.patch
# For bz#1134237 - Opening malformed VMDK description file should fail
Patch1365: kvm-qemu-iotest-Make-077-raw-only.patch
# For bz#1002493 - qemu-img convert rate about 100k/second from qcow2/raw to vmdk format on nfs system file
Patch1366: kvm-qemu-iotests-Don-t-run-005-on-vmdk-split-formats.patch
# For bz#1134251 - Opening an obviously truncated VMDK image should fail
Patch1367: kvm-vmdk-extract-vmdk_read_desc.patch
# For bz#1134251 - Opening an obviously truncated VMDK image should fail
Patch1368: kvm-vmdk-push-vmdk_read_desc-up-to-caller.patch
# For bz#1134251 - Opening an obviously truncated VMDK image should fail
Patch1369: kvm-vmdk-do-not-try-opening-a-file-as-both-image-and-des.patch
# For bz#1134251 - Opening an obviously truncated VMDK image should fail
Patch1370: kvm-vmdk-correctly-propagate-errors.patch
# For bz#1134251 - Opening an obviously truncated VMDK image should fail
Patch1371: kvm-block-vmdk-do-not-report-file-offset-for-compressed-.patch
# For bz#1134251 - Opening an obviously truncated VMDK image should fail
Patch1372: kvm-vmdk-Fix-d-and-lld-to-PRI-in-format-strings.patch
# For bz#1134251 - Opening an obviously truncated VMDK image should fail
Patch1373: kvm-vmdk-Fix-x-to-PRIx32-in-format-strings-for-cid.patch
# For bz#1134283 - qemu-img convert from ISO to streamOptimized fails
Patch1374: kvm-qemu-img-Convert-by-cluster-size-if-target-is-compre.patch
# For bz#1134283 - qemu-img convert from ISO to streamOptimized fails
Patch1375: kvm-vmdk-Implement-.bdrv_write_compressed.patch
# For bz#1134283 - qemu-img convert from ISO to streamOptimized fails
Patch1376: kvm-vmdk-Implement-.bdrv_get_info.patch
# For bz#1134283 - qemu-img convert from ISO to streamOptimized fails
Patch1377: kvm-qemu-iotests-Test-converting-to-streamOptimized-from.patch
# For bz#1134283 - qemu-img convert from ISO to streamOptimized fails
Patch1378: kvm-vmdk-Fix-local_err-in-vmdk_create.patch
# For bz#1002493 - qemu-img convert rate about 100k/second from qcow2/raw to vmdk format on nfs system file
Patch1379: kvm-fpu-softfloat-drop-INLINE-macro.patch
# For bz#1002493 - qemu-img convert rate about 100k/second from qcow2/raw to vmdk format on nfs system file
Patch1380: kvm-block-New-bdrv_nb_sectors.patch
# For bz#1002493 - qemu-img convert rate about 100k/second from qcow2/raw to vmdk format on nfs system file
Patch1381: kvm-vmdk-Optimize-cluster-allocation.patch
# For bz#1002493 - qemu-img convert rate about 100k/second from qcow2/raw to vmdk format on nfs system file
Patch1382: kvm-vmdk-Handle-failure-for-potentially-large-allocation.patch
# For bz#1002493 - qemu-img convert rate about 100k/second from qcow2/raw to vmdk format on nfs system file
Patch1383: kvm-vmdk-Use-bdrv_nb_sectors-where-sectors-not-bytes-are.patch
# For bz#1002493 - qemu-img convert rate about 100k/second from qcow2/raw to vmdk format on nfs system file
Patch1384: kvm-vmdk-fix-vmdk_parse_extents-extent_file-leaks.patch
# For bz#1002493 - qemu-img convert rate about 100k/second from qcow2/raw to vmdk format on nfs system file
Patch1385: kvm-vmdk-fix-buf-leak-in-vmdk_parse_extents.patch
# For bz#1002493 - qemu-img convert rate about 100k/second from qcow2/raw to vmdk format on nfs system file
Patch1386: kvm-vmdk-Fix-integer-overflow-in-offset-calculation.patch
# For bz#1163078 - CVE-2014-7840 qemu-kvm: qemu: insufficient parameter validation during ram load [rhel-7.1]
Patch1387: kvm-migration-fix-parameter-validation-on-ram-load-CVE-2.patch
# For bz#1175325 - Delete cow block driver
Patch1388: kvm-block-delete-cow-block-driver.patch
# For bz#1180942 - qemu core dumped when unhotplug gpu card assigned to guest
Patch1389: kvm-vfio-pci-Fix-interrupt-disabling.patch
# For bz#1169456 - CVE-2014-8106 qemu-kvm: qemu: cirrus: insufficient blit region checks [rhel-7.1]
Patch1390: kvm-cirrus-fix-blit-region-check.patch
# For bz#1169456 - CVE-2014-8106 qemu-kvm: qemu: cirrus: insufficient blit region checks [rhel-7.1]
Patch1391: kvm-cirrus-don-t-overflow-CirrusVGAState-cirrus_bltbuf.patch
# For bz#1198958 - Add rhel-6.6.0 machine type to RHEL 7.1.z to support RHEL 6.6 to RHEL 7.1 live migration
Patch1392: kvm-pc-add-rhel6.6.0-machine-type.patch
# For bz#1155671 - [Fujitsu 7.2 FEAT]: QEMU: Add tracepoints in system shutdown
Patch1393: kvm-trace-add-qemu_system_powerdown_request-and-qemu_sys.patch
# For bz#1139562 - qemu-kvm with vhost=off and sndbuf=100 crashed when stop it during pktgen test from guest to host
Patch1394: kvm-virtio-net-drop-assert-on-vm-stop.patch
# For bz#1086168 - qemu-kvm can not cancel migration in src host when network of dst host failed
Patch1395: kvm-socket-shutdown.patch
# For bz#1086168 - qemu-kvm can not cancel migration in src host when network of dst host failed
Patch1396: kvm-Handle-bi-directional-communication-for-fd-migration.patch
# For bz#1086168 - qemu-kvm can not cancel migration in src host when network of dst host failed
Patch1397: kvm-migration_cancel-shutdown-migration-socket.patch
# For bz#1032412 - opening read-only iscsi lun as read-write should fail
Patch1398: kvm-iscsi-Refuse-to-open-as-writable-if-the-LUN-is-write.patch
# For bz#1176283 - [migration]migration failed when configure guest with OVMF bios + machine type=rhel6.5.0
Patch1399: kvm-main-set-current_machine-before-calling-machine-init.patch
# For bz#1176283 - [migration]migration failed when configure guest with OVMF bios + machine type=rhel6.5.0
Patch1400: kvm-pc_sysfw-prevent-pflash-and-or-mis-sized-firmware-fo.patch
# For bz#892258 - ide CDROM io/data errors after migration
Patch1401: kvm-Restore-atapi_dma-flag-across-migration.patch
# For bz#892258 - ide CDROM io/data errors after migration
Patch1402: kvm-atapi-migration-Throw-recoverable-error-to-avoid-rec.patch
Patch1403: kvm-build-reenable-local-builds-to-pass-enable-debug-RHE.patch
# For bz#1184363 - Qemu process fails to start with a multipath device with all paths failed
Patch1404: kvm-raw-posix-Fail-gracefully-if-no-working-alignment-is.patch
# For bz#1184363 - Qemu process fails to start with a multipath device with all paths failed
Patch1405: kvm-block-Add-Error-argument-to-bdrv_refresh_limits.patch
# For bz#828493 - [Hitachi 7.2 FEAT] Extract guest memory dump from qemu-kvm core
Patch1406: kvm-Python-lang-gdb-script-to-extract-x86_64-guest-vmcor.patch
# For bz#1210503 - vfio improve PCI ROM loading error handling
Patch1407: kvm-vfio-warn-if-host-device-rom-can-t-be-read.patch
# For bz#1210503 - vfio improve PCI ROM loading error handling
Patch1408: kvm-vfio-Do-not-reattempt-a-failed-rom-read.patch
# For bz#1210503 - vfio improve PCI ROM loading error handling
Patch1409: kvm-vfio-Correction-in-vfio_rom_read-when-attempting-rom.patch
# For bz#1210504 - vfio: Fix overrun after readlink() fills buffer completely
Patch1410: kvm-vfio-Fix-overrun-after-readlink-fills-buffer-complet.patch
# For bz#1210505 - vfio: use correct runstate
Patch1411: kvm-vfio-use-correct-runstate.patch
# For bz#1181267 - vfio-pci: Fix BAR size overflow
Patch1412: kvm-vfio-pci-Fix-BAR-size-overflow.patch
# For bz#1210508 - vfio: Use vfio type1 v2 IOMMU interface
Patch1413: kvm-vfio-Use-vfio-type1-v2-IOMMU-interface.patch
# For bz#1210509 - vfio-pci: Enable device request notification support
Patch1414: kvm-vfio-pci-Enable-device-request-notification-support.patch
# For bz#1181267 - vfio-pci: Fix BAR size overflow
Patch1415: kvm-vfio-pci-Further-fix-BAR-size-overflow.patch
# For bz#1210504 - vfio: Fix overrun after readlink() fills buffer completely
Patch1416: kvm-vfio-pci-Fix-error-path-sign.patch
# For bz#1210510 - Sync MTRRs with KVM and disable on reset
Patch1417: kvm-x86-Use-common-variable-range-MTRR-counts.patch
# For bz#1210510 - Sync MTRRs with KVM and disable on reset
Patch1418: kvm-x86-kvm-Add-MTRR-support-for-kvm_get-put_msrs.patch
# For bz#1210510 - Sync MTRRs with KVM and disable on reset
Patch1419: kvm-x86-Clear-MTRRs-on-vCPU-reset.patch
# For bz#1206497 - CVE-2015-1779 qemu-kvm: qemu: vnc: insufficient resource limiting in VNC websockets decoder [rhel-7.2]
Patch1420: kvm-CVE-2015-1779-incrementally-decode-websocket-frames.patch
# For bz#1206497 - CVE-2015-1779 qemu-kvm: qemu: vnc: insufficient resource limiting in VNC websockets decoder [rhel-7.2]
Patch1421: kvm-CVE-2015-1779-limit-size-of-HTTP-headers-from-websoc.patch
# For bz#1200295 - QEMU segfault when doing unaligned zero write to non-512 disk
Patch1422: kvm-qemu-iotests-Test-unaligned-4k-zero-write.patch
# For bz#1200295 - QEMU segfault when doing unaligned zero write to non-512 disk
Patch1423: kvm-block-Fix-NULL-deference-for-unaligned-write-if-qiov.patch
# For bz#1200295 - QEMU segfault when doing unaligned zero write to non-512 disk
Patch1424: kvm-qemu-iotests-Test-unaligned-sub-block-zero-write.patch
# For bz#1219270 - CVE-2015-3456 qemu-kvm: qemu: floppy disk controller flaw [rhel-7.2]
Patch1425: kvm-fdc-force-the-fifo-access-to-be-in-bounds-of-the-all.patch
# For bz#1208808 - creating second and further snapshot takes ages
Patch1426: kvm-qcow2-Pass-discard-type-to-qcow2_discard_clusters.patch
# For bz#1208808 - creating second and further snapshot takes ages
Patch1427: kvm-qcow2-Discard-VM-state-in-active-L1-after-creating-s.patch
# For bz#1217850 - qemu-kvm: Enable build on aarch64
Patch1428: kvm-configure-Require-libfdt-for-arm-ppc-microblaze-soft.patch
# For bz#1217850 - qemu-kvm: Enable build on aarch64
Patch1429: kvm-configure-Add-handling-code-for-AArch64-targets.patch
# For bz#1217850 - qemu-kvm: Enable build on aarch64
Patch1430: kvm-configure-permit-compilation-on-arm-aarch64.patch
# For bz#1217850 - qemu-kvm: Enable build on aarch64
Patch1431: kvm-Remove-redhat-extensions-from-qmp-events.txt.patch
# For bz#1217351 - Overflow in malloc size calculation in VMDK driver
Patch1432: kvm-vmdk-Fix-overflow-if-l1_size-is-0x20000000.patch
# For bz#1226683 - [virt-v2v] Backport upstream ssh driver to qemu-kvm
Patch1433: kvm-block-ssh-Drop-superfluous-libssh2_session_last_errn.patch
# For bz#1226683 - [virt-v2v] Backport upstream ssh driver to qemu-kvm
Patch1434: kvm-block-ssh-Propagate-errors-through-check_host_key.patch
# For bz#1226683 - [virt-v2v] Backport upstream ssh driver to qemu-kvm
Patch1435: kvm-block-ssh-Propagate-errors-through-authenticate.patch
# For bz#1226683 - [virt-v2v] Backport upstream ssh driver to qemu-kvm
Patch1436: kvm-block-ssh-Propagate-errors-through-connect_to_ssh.patch
# For bz#1226683 - [virt-v2v] Backport upstream ssh driver to qemu-kvm
Patch1437: kvm-block-ssh-Propagate-errors-to-open-and-create-method.patch
# For bz#1226683 - [virt-v2v] Backport upstream ssh driver to qemu-kvm
Patch1438: kvm-ssh-Don-t-crash-if-either-host-or-path-is-not-specif.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1439: kvm-curl-Replaced-old-error-handling-with-error-reportin.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1440: kvm-curl-Fix-long-line.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1441: kvm-curl-Remove-unnecessary-use-of-goto.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1442: kvm-curl-Fix-return-from-curl_read_cb-with-invalid-state.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1443: kvm-curl-Remove-erroneous-sleep-waiting-for-curl-complet.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1444: kvm-curl-Whitespace-only-changes.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1445: kvm-block-curl-Implement-the-libcurl-timer-callback-inte.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1446: kvm-curl-Remove-unnecessary-explicit-calls-to-internal-e.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1447: kvm-curl-Eliminate-unnecessary-use-of-curl_multi_socket_.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1448: kvm-curl-Ensure-all-informationals-are-checked-for-compl.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1449: kvm-curl-Fix-hang-reading-from-slow-connections.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1450: kvm-curl-Fix-build-when-curl_multi_socket_action-isn-t-a.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1451: kvm-curl-Remove-broken-parsing-of-options-from-url.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1452: kvm-curl-refuse-to-open-URL-from-HTTP-server-without-ran.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1453: kvm-curl-Add-sslverify-option.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1454: kvm-block-Drop-superfluous-conditionals-around-g_free.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1455: kvm-curl-Handle-failure-for-potentially-large-allocation.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1456: kvm-block.curl-adding-timeout-option.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1457: kvm-curl-Allow-a-cookie-or-cookies-to-be-sent-with-http-.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1458: kvm-curl-The-macro-that-you-have-to-uncomment-to-get-deb.patch
# For bz#1226684 - [virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https
Patch1459: kvm-block-curl-Improve-type-safety-of-s-timeout.patch
# For bz#1185737 - qemu-kvm hang when boot with usb-host and sandbox was enabled
Patch1460: kvm-seccomp-add-timerfd_create-and-timerfd_settime-to-th.patch
# For bz#1226697 - [virt-v2v] Allow json: filenames in qemu-img
Patch1461: kvm-qdict-Add-qdict_join.patch
# For bz#1226697 - [virt-v2v] Allow json: filenames in qemu-img
Patch1462: kvm-block-Allow-JSON-filenames.patch
# For bz#1230808 - [abrt] qemu-system-x86: __memcmp_sse4_1(): qemu-system-x86_64 killed by SIGSEGV
Patch1463: kvm-spice-display-fix-segfault-in-qemu_spice_create_upda.patch
# For bz#1142857 - [abrt] qemu-kvm: bdrv_error_action(): qemu-kvm killed by SIGABRT
# For bz#1142857 - [abrt] qemu-kvm: bdrv_error_action(): qemu-kvm killed by SIGABRT
# For bz#(aka - 
# For bz#8*10^6/7) - XFree86 apparently sets xhost to ill inital values
Patch1464: kvm-atomics-add-explicit-compiler-fence-in-__atomic-memo.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1465: kvm-qcow2-Put-cache-reference-in-error-case.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1466: kvm-qcow2-Catch-bdrv_getlength-error.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1467: kvm-block-Introduce-qemu_try_blockalign.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1468: kvm-qcow2-Catch-host_offset-for-data-allocation.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1469: kvm-iotests-Add-test-for-image-header-overlap.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1470: kvm-block-Catch-bs-drv-in-bdrv_check.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1471: kvm-qapi-block-Add-fatal-to-BLOCK_IMAGE_CORRUPTED.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1472: kvm-qcow2-Add-qcow2_signal_corruption.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1473: kvm-qcow2-Use-qcow2_signal_corruption-for-overlaps.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1474: kvm-qcow2-Check-L1-L2-reftable-entries-for-alignment.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1475: kvm-iotests-Add-more-tests-for-qcow2-corruption.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1476: kvm-qcow2-fix-leak-of-Qcow2DiscardRegion-in-update_refco.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1477: kvm-qcow2-Do-not-overflow-when-writing-an-L1-sector.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1478: kvm-iotests-Add-test-for-qcow2-L1-table-update.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1479: kvm-block-Add-qemu_-try_-blockalign0.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1480: kvm-qcow2-Calculate-refcount-block-entry-count.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1481: kvm-qcow2-Fix-leaks-in-dirty-images.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1482: kvm-qcow2-Split-qcow2_check_refcounts.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1483: kvm-qcow2-Use-sizeof-refcount_table.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1484: kvm-qcow2-Pull-check_refblocks-up.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1485: kvm-qcow2-Use-int64_t-for-in-memory-reftable-size.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1486: kvm-qcow2-Split-fail-code-in-L1-and-L2-checks.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1487: kvm-qcow2-Let-inc_refcounts-return-errno.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1488: kvm-qcow2-Let-inc_refcounts-resize-the-reftable.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1489: kvm-qcow2-Reuse-refcount-table-in-calculate_refcounts.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1490: kvm-qcow2-Fix-refcount-blocks-beyond-image-end.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1491: kvm-qcow2-Do-not-perform-potentially-damaging-repairs.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1492: kvm-qcow2-Rebuild-refcount-structure-during-check.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1493: kvm-qcow2-Clean-up-after-refcount-rebuild.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1494: kvm-iotests-Fix-test-outputs.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1495: kvm-iotests-Add-test-for-potentially-damaging-repairs.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1496: kvm-qcow2-Drop-REFCOUNT_SHIFT.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1497: kvm-block-Respect-underlying-file-s-EOF.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1498: kvm-qcow2-Fix-header-extension-size-check.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1499: kvm-qcow2.py-Add-required-padding-for-header-extensions.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1500: kvm-block-Don-t-probe-for-unknown-backing-file-format.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1501: kvm-qcow2-Add-two-more-unalignment-checks.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1502: kvm-iotests-Add-tests-for-more-corruption-cases.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1503: kvm-qcow2-Respect-new_block-in-alloc_refcount_block.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1504: kvm-iotests-Add-tests-for-refcount-table-growth.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1505: kvm-qcow2-Fix-header-update-with-overridden-backing-file.patch
# For bz#1129893 - Backport additional qcow2 corruption prevention and image repair patches
Patch1506: kvm-qcow2-Flush-pending-discards-before-allocating-clust.patch
# For bz#1229646 - CVE-2015-3214 qemu-kvm: qemu: i8254: out-of-bounds memory access in pit_ioport_read function [rhel-7.2]
Patch1507: kvm-i8254-fix-out-of-bounds-memory-access-in-pit_ioport_.patch
# For bz#1233350 - [Intel 7.2 FEAT] Expose MPX feature to guest - qemu-kvm
Patch1508: kvm-target-i386-fix-cpuid-leaf-0x0d.patch
# For bz#1233350 - [Intel 7.2 FEAT] Expose MPX feature to guest - qemu-kvm
Patch1509: kvm-target-i386-Intel-MPX.patch
# For bz#1233350 - [Intel 7.2 FEAT] Expose MPX feature to guest - qemu-kvm
Patch1510: kvm-always-update-the-MPX-model-specific-register.patch
# For bz#1233350 - [Intel 7.2 FEAT] Expose MPX feature to guest - qemu-kvm
Patch1511: kvm-target-i386-bugfix-of-Intel-MPX.patch
# For bz#1233350 - [Intel 7.2 FEAT] Expose MPX feature to guest - qemu-kvm
Patch1512: kvm-target-i386-fix-set-of-registers-zeroed-on-reset.patch
# For bz#1233350 - [Intel 7.2 FEAT] Expose MPX feature to guest - qemu-kvm
Patch1513: kvm-target-i386-Add-mpx-CPU-feature-name.patch
# For bz#1233350 - [Intel 7.2 FEAT] Expose MPX feature to guest - qemu-kvm
Patch1514: kvm-target-i386-Avoid-shifting-left-into-sign-bit.patch
# For bz#1233350 - [Intel 7.2 FEAT] Expose MPX feature to guest - qemu-kvm
Patch1515: kvm-target-i386-add-Intel-AVX-512-support.patch
# For bz#1213881 - enable using tcmalloc for memory allocation in qemu-kvm
Patch1516: kvm-configure-Add-support-for-tcmalloc.patch
# For bz#1205100 - qemu-kvm: Qemu: PRDT overflow from guest to host [rhel-7.2]
Patch1517: kvm-ahci.c-mask-unused-flags-when-reading-size-PRDT-DBC.patch
# For bz#1205100 - qemu-kvm: Qemu: PRDT overflow from guest to host [rhel-7.2]
Patch1518: kvm-ide-Correct-handling-of-malformed-short-PRDTs.patch
# For bz#1243690 - EMBARGOED CVE-2015-5154 qemu-kvm: qemu: ide: atapi: heap overflow during I/O buffer memory access [rhel-7.2]
Patch1519: kvm-ide-Check-array-bounds-before-writing-to-io_buffer-C.patch
# For bz#1243690 - EMBARGOED CVE-2015-5154 qemu-kvm: qemu: ide: atapi: heap overflow during I/O buffer memory access [rhel-7.2]
Patch1520: kvm-ide-atapi-Fix-START-STOP-UNIT-command-completion.patch
# For bz#1243690 - EMBARGOED CVE-2015-5154 qemu-kvm: qemu: ide: atapi: heap overflow during I/O buffer memory access [rhel-7.2]
Patch1521: kvm-ide-Clear-DRQ-after-handling-all-expected-accesses.patch
# For bz#1235812 - block/curl: Fix generic "Input/output error" on failure
Patch1522: kvm-block-curl-Don-t-lose-original-error-when-a-connecti.patch
# For bz#1244347 - Quirk for Chelsio T5 MSI-X PBA
Patch1523: kvm-vfio-pci-Add-pba_offset-PCI-quirk-for-Chelsio-T5-dev.patch
# For bz#1238639 - qemu-img shows error message for backing file twice
Patch1524: kvm-block-Print-its-file-name-if-backing-file-opening-fa.patch
# For bz#1238639 - qemu-img shows error message for backing file twice
Patch1525: kvm-block-Propagate-error-in-bdrv_img_create.patch
# For bz#1238639 - qemu-img shows error message for backing file twice
Patch1526: kvm-iotests-Add-test-for-non-existing-backing-file.patch
# For bz#1243731 - smart card emulation doesn't work with USB3 (nec-xhci) controller
Patch1527: kvm-usb-ccid-add-missing-wakeup-calls.patch
# For bz#1217349 - qemu-img vpc driver segfault
Patch1528: kvm-vpc-Handle-failure-for-potentially-large-allocations.patch
# For bz#1217349 - qemu-img vpc driver segfault
Patch1529: kvm-block-vpc-prevent-overflow-if-max_table_entries-0x40.patch
# For bz#1217349 - qemu-img vpc driver segfault
Patch1530: kvm-block-qemu-iotests-add-check-for-multiplication-over.patch
# For bz#1249718 - Segfault occurred at Dst VM while completed migration upon ENOSPC
Patch1531: kvm-virtio-scsi-use-virtqueue_map_sg-when-loading-reques.patch
# For bz#1249718 - Segfault occurred at Dst VM while completed migration upon ENOSPC
Patch1532: kvm-scsi-disk-fix-cmd.mode-field-typo.patch
# For bz#1248766 - CVE-2015-5165 qemu-kvm: Qemu: rtl8139 uninitialized heap memory information leakage to guest [rhel-7.2]
Patch1533: kvm-rtl8139-avoid-nested-ifs-in-IP-header-parsing-CVE-20.patch
# For bz#1248766 - CVE-2015-5165 qemu-kvm: Qemu: rtl8139 uninitialized heap memory information leakage to guest [rhel-7.2]
Patch1534: kvm-rtl8139-drop-tautologous-if-ip-.-statement-CVE-2015-.patch
# For bz#1248766 - CVE-2015-5165 qemu-kvm: Qemu: rtl8139 uninitialized heap memory information leakage to guest [rhel-7.2]
Patch1535: kvm-rtl8139-skip-offload-on-short-Ethernet-IP-header-CVE.patch
# For bz#1248766 - CVE-2015-5165 qemu-kvm: Qemu: rtl8139 uninitialized heap memory information leakage to guest [rhel-7.2]
Patch1536: kvm-rtl8139-check-IP-Header-Length-field-CVE-2015-5165.patch
# For bz#1248766 - CVE-2015-5165 qemu-kvm: Qemu: rtl8139 uninitialized heap memory information leakage to guest [rhel-7.2]
Patch1537: kvm-rtl8139-check-IP-Total-Length-field-CVE-2015-5165.patch
# For bz#1248766 - CVE-2015-5165 qemu-kvm: Qemu: rtl8139 uninitialized heap memory information leakage to guest [rhel-7.2]
Patch1538: kvm-rtl8139-skip-offload-on-short-TCP-header-CVE-2015-51.patch
# For bz#1248766 - CVE-2015-5165 qemu-kvm: Qemu: rtl8139 uninitialized heap memory information leakage to guest [rhel-7.2]
Patch1539: kvm-rtl8139-check-TCP-Data-Offset-field-CVE-2015-5165.patch
# For bz#1171576 - test case 064 and 070 of qemu-iotests fail for vhdx with qemu-kvm-1.5.3-83.el7
Patch1540: kvm-block-update-test-070-for-vhdx.patch
# For bz#1219217 - Coverity-detected defect: call to fcntl without checking return value
Patch1541: kvm-block-coverity-fix-check-return-value-for-fcntl-in-g.patch
# For bz#922014 - RFE: support hotplugging chardev & serial ports (Windows guests)
Patch1542: kvm-serial-reset-state-at-startup.patch
# For bz#1134670 - fail to specify the physical_block_size/logical_block_size value not 512 for IDE disk
Patch1543: kvm-ide-Check-validity-of-logical-block-size.patch
# For bz#1191226 - libvirt requires rtc-reset-reinjection command, backport it to RHEL7.1
Patch1544: kvm-mc146818rtc-add-rtc-reset-reinjection-QMP-command.patch
# For bz#1218919 - Coverity-detected defect: buffer overrun at uri.c:2035
Patch1545: kvm-Drop-superfluous-conditionals-around-g_strdup.patch
# For bz#1218919 - Coverity-detected defect: buffer overrun at uri.c:2035
Patch1546: kvm-util-Drop-superfluous-conditionals-around-g_free.patch
# For bz#1218919 - Coverity-detected defect: buffer overrun at uri.c:2035
Patch1547: kvm-util-Fuse-g_malloc-memset-into-g_new0.patch
# For bz#1218919 - Coverity-detected defect: buffer overrun at uri.c:2035
Patch1548: kvm-util-uri-uri_new-can-t-fail-drop-dead-error-handling.patch
# For bz#1218919 - Coverity-detected defect: buffer overrun at uri.c:2035
Patch1549: kvm-util-uri-realloc2n-can-t-fail-drop-dead-error-handli.patch
# For bz#1218919 - Coverity-detected defect: buffer overrun at uri.c:2035
Patch1550: kvm-util-uri-URI-member-path-can-be-null-compare-more-ca.patch
# For bz#1218919 - Coverity-detected defect: buffer overrun at uri.c:2035
Patch1551: kvm-util-uri-Add-overflow-check-to-rfc3986_parse_port.patch
# For bz#1170974 - test case 025 of qemu-iotests fail for raw with qemu-kvm-1.5.3-83.el7.x86_64
Patch1552: kvm-qemu-iotests-Filter-qemu-io-output-in-025.patch
# For bz#1270341 - qemu-kvm build failure race condition in tests/ide-test
Patch1553: kvm-qtest-ide-test-disable-flush-test.patch
# For bz#1268879 - Camera stops work after remote-viewer re-connection [qemu-kvm]
Patch1554: kvm-ehci-clear-suspend-bit-on-detach.patch
# For bz#1277248 - ceph.conf properties override qemu's command-line properties
Patch1555: kvm-rbd-make-qemu-s-cache-setting-override-any-ceph-sett.patch
# For bz#1277248 - ceph.conf properties override qemu's command-line properties
Patch1556: kvm-rbd-fix-ceph-settings-precedence.patch
# For bz#1265427 - contents of MSR_TSC_AUX are not migrated
Patch1557: kvm-target-i386-get-put-MSR_TSC_AUX-across-reset-and-mig.patch
# For bz#1252757 - [RHEL-7.2-qmu-kvm] Package is 100% lost when ping from host to Win2012r2 guest with 64000 size
Patch1558: kvm-rtl8139-Fix-receive-buffer-overflow-check.patch
# For bz#1252757 - [RHEL-7.2-qmu-kvm] Package is 100% lost when ping from host to Win2012r2 guest with 64000 size
Patch1559: kvm-rtl8139-Do-not-consume-the-packet-during-overflow-in.patch
# For bz#1283116 - [abrt] qemu-img: get_block_status(): qemu-img killed by SIGABRT
Patch1560: kvm-raw-posix-Fix-.bdrv_co_get_block_status-for-unaligne.patch
# For bz#1269738 - Vlan table display repeat four times in qmp when queues=4
Patch1561: kvm-net-Make-qmp_query_rx_filter-with-name-argument-more.patch
# For bz#1298048 - CVE-2016-1714 qemu-kvm: Qemu: nvram: OOB r/w access in processing firmware configurations [rhel-7.3]
Patch1562: kvm-fw_cfg-add-check-to-validate-current-entry-value-CVE.patch
# For bz#1296044 - qemu-kvm: insufficient loop termination conditions in start_xmit() and e1000_receive() [rhel-7.3]
Patch1563: kvm-e1000-eliminate-infinite-loops-on-out-of-bounds-tran.patch
# For bz#1285453 - An NBD client can cause QEMU main loop to block when connecting to built-in NBD server
Patch1564: kvm-nbd-Always-call-close_fn-in-nbd_client_new.patch
# For bz#1285453 - An NBD client can cause QEMU main loop to block when connecting to built-in NBD server
Patch1565: kvm-nbd-server-Coroutine-based-negotiation.patch
# For bz#1285453 - An NBD client can cause QEMU main loop to block when connecting to built-in NBD server
Patch1566: kvm-nbd-client_close-on-error-in-nbd_co_client_start.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1567: kvm-qemu-io-Remove-unused-args_command.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1568: kvm-cutils-Support-P-and-E-suffixes-in-strtosz.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1569: kvm-qemu-io-Make-cvtnum-a-wrapper-around-strtosz_suffix.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1570: kvm-qemu-io-Handle-cvtnum-errors-in-alloc.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1571: kvm-qemu-io-Don-t-use-global-bs-in-command-implementatio.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1572: kvm-qemu-io-Split-off-commands-to-qemu-io-cmds.c.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1573: kvm-qemu-io-Factor-out-qemuio_command.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1574: kvm-qemu-io-Move-help-function.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1575: kvm-qemu-io-Move-quit-function.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1576: kvm-qemu-io-Move-qemu_strsep-to-cutils.c.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1577: kvm-qemu-io-Move-functions-for-registering-and-running-c.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1578: kvm-qemu-io-Move-command_loop-and-friends.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1579: kvm-qemu-io-Move-remaining-helpers-from-cmd.c.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1580: kvm-qemu-io-Interface-cleanup.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1581: kvm-qemu-io-Use-the-qemu-version-for-V.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1582: kvm-Make-qemu-io-commands-available-in-HMP.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1583: kvm-blkdebug-Add-BLKDBG_FLUSH_TO_OS-DISK-events.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1584: kvm-qemu-io-fix-cvtnum-lval-types.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1585: kvm-qemu-io-Check-for-trailing-chars.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1586: kvm-qemu-io-Correct-error-messages.patch
# For bz#1272523 - qemu-kvm build failure race condition in tests/ide-test
Patch1587: kvm-ide-test-fix-failure-for-test_flush.patch
# For bz#1331413 - EMBARGOED CVE-2016-3710 qemu-kvm: qemu: incorrect banked access bounds checking in vga module [rhel-7.3]
Patch1588: kvm-vga-Remove-some-should-be-done-in-BIOS-comments.patch
# For bz#1331413 - EMBARGOED CVE-2016-3710 qemu-kvm: qemu: incorrect banked access bounds checking in vga module [rhel-7.3]
Patch1589: kvm-vga-fix-banked-access-bounds-checking-CVE-2016-xxxx.patch
# For bz#1331413 - EMBARGOED CVE-2016-3710 qemu-kvm: qemu: incorrect banked access bounds checking in vga module [rhel-7.3]
Patch1590: kvm-vga-add-vbe_enabled-helper.patch
# For bz#1331413 - EMBARGOED CVE-2016-3710 qemu-kvm: qemu: incorrect banked access bounds checking in vga module [rhel-7.3]
Patch1591: kvm-vga-factor-out-vga-register-setup.patch
# For bz#1331413 - EMBARGOED CVE-2016-3710 qemu-kvm: qemu: incorrect banked access bounds checking in vga module [rhel-7.3]
Patch1592: kvm-vga-update-vga-register-setup-on-vbe-changes.patch
# For bz#1331413 - EMBARGOED CVE-2016-3710 qemu-kvm: qemu: incorrect banked access bounds checking in vga module [rhel-7.3]
Patch1593: kvm-vga-make-sure-vga-register-setup-for-vbe-stays-intac.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1594: kvm-vmdk-Leave-bdi-intact-if-ENOTSUP-in-vmdk_get_info.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1595: kvm-vmdk-Use-g_random_int-to-generate-CID.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1596: kvm-vmdk-Fix-comment-to-match-code-of-extent-lines.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1597: kvm-vmdk-Clean-up-descriptor-file-reading.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1598: kvm-vmdk-Check-descriptor-file-length-when-reading-it.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1599: kvm-vmdk-Remove-unnecessary-initialization.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1600: kvm-vmdk-Set-errp-on-failures-in-vmdk_open_vmdk4.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1601: kvm-block-vmdk-make-ret-variable-usage-clear.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1602: kvm-block-vmdk-move-string-allocations-from-stack-to-the.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1603: kvm-block-vmdk-fixed-sizeof-error.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1604: kvm-vmdk-Widen-before-shifting-32-bit-header-field.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1605: kvm-vmdk-Fix-next_cluster_sector-for-compressed-write.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1606: kvm-vmdk-Fix-index_in_cluster-calculation-in-vmdk_co_get.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1607: kvm-vmdk-Use-vmdk_find_index_in_cluster-everywhere.patch
# For bz#1299250 - qemu-img created VMDK images are unbootable
Patch1608: kvm-vmdk-Fix-next_cluster_sector-for-compressed-write2.patch
# For bz#1299116 - qemu-img created VMDK images lead to "Not a supported disk format (sparse VMDK version too old)"
Patch1609: kvm-vmdk-Create-streamOptimized-as-version-3.patch
# For bz#1299116 - qemu-img created VMDK images lead to "Not a supported disk format (sparse VMDK version too old)"
Patch1610: kvm-vmdk-Fix-converting-to-streamOptimized.patch
# For bz#1299116 - qemu-img created VMDK images lead to "Not a supported disk format (sparse VMDK version too old)"
Patch1611: kvm-vmdk-Fix-calculation-of-block-status-s-offset.patch
# For bz#1312289 - "qemu-kvm: /builddir/build/BUILD/qemu-1.5.3/hw/scsi/virtio-scsi.c:533: virtio_scsi_push_event: Assertion `event == 0' failed" after hotplug 20 virtio-scsi disks then hotunplug them
Patch1612: kvm-virtio-scsi-Prevent-assertion-on-missed-events.patch
# For bz#1177318 - Guest using rbd based image as disk failed to start when sandbox was enabled
Patch1613: kvm-seccomp-adding-sysinfo-system-call-to-whitelist.patch
# For bz#1330969 - match the OEM ID and OEM Table ID fields of the FADT and the RSDT to those of the SLIC
Patch1614: kvm-acpi-strip-compiler-info-in-built-in-DSDT.patch
# For bz#1330969 - match the OEM ID and OEM Table ID fields of the FADT and the RSDT to those of the SLIC
Patch1615: kvm-acpi-fix-endian-ness-for-table-ids.patch
# For bz#1330969 - match the OEM ID and OEM Table ID fields of the FADT and the RSDT to those of the SLIC
Patch1616: kvm-acpi-support-specified-oem-table-id-for-build_header.patch
# For bz#1330969 - match the OEM ID and OEM Table ID fields of the FADT and the RSDT to those of the SLIC
Patch1617: kvm-acpi-take-oem_id-in-build_header-optionally.patch
# For bz#1330969 - match the OEM ID and OEM Table ID fields of the FADT and the RSDT to those of the SLIC
Patch1618: kvm-acpi-expose-oem_id-and-oem_table_id-in-build_rsdt.patch
# For bz#1330969 - match the OEM ID and OEM Table ID fields of the FADT and the RSDT to those of the SLIC
Patch1619: kvm-acpi-add-function-to-extract-oem_id-and-oem_table_id.patch
# For bz#1330969 - match the OEM ID and OEM Table ID fields of the FADT and the RSDT to those of the SLIC
Patch1620: kvm-pc-set-the-OEM-fields-in-the-RSDT-and-the-FADT-from-.patch
# For bz#1156635 - Libvirt is confused that qemu-kvm exposes 'block-job-cancel' but not 'block-stream'
Patch1621: kvm-block-jobs-qemu-kvm-rhel-differentiation.patch
# For bz#1283198 - RFE: backport max monitor limitation from Qemu upstream
Patch1622: kvm-qxl-allow-to-specify-head-limit-to-qxl-driver.patch
# For bz#1283198 - RFE: backport max monitor limitation from Qemu upstream
Patch1623: kvm-qxl-Fix-new-function-name-for-spice-server-library.patch
# For bz#1268345 - posix_fallocate emulation on NFS fails with Bad file descriptor if fd is opened O_WRONLY
Patch1624: kvm-block-raw-posix-Open-file-descriptor-O_RDWR-to-work-.patch
# For bz#1256741 - "CapsLock" will work as "\" when boot a guest with usb-kbd
Patch1625: kvm-hw-input-hid.c-Fix-capslock-hid-code.patch
# For bz#1340971 - qemu: accel=tcg does not implement SSE 4 properly
Patch1626: kvm-target-i386-fix-pcmpxstrx-equal-ordered-strstr-mode.patch
# For bz#1336491 - Ship FD connection patches qemu-kvm part
Patch1627: kvm-spice-do-not-require-TCP-ports.patch
# For bz#1346982 - Regression from CVE-2016-3712: windows installer fails to start
Patch1628: kvm-vga-add-sr_vbe-register-set.patch
# For bz#1340929 - CVE-2016-5126 qemu-kvm: Qemu: block: iscsi: buffer overflow in iscsi_aio_ioctl [rhel-7.3]
Patch1629: kvm-block-iscsi-avoid-potential-overflow-of-acb-task-cdb.patch
# For bz#1327599 - Add Skylake CPU model
Patch1630: kvm-target-i386-add-feature-flags-for-CPUID-EAX-0xd-ECX-.patch
# For bz#1327599 - Add Skylake CPU model
Patch1631: kvm-target-i386-add-Skylake-Client-cpu-model.patch
# For bz#1318199 - expose host BLKSECTGET limit in scsi-block (qemu-kvm)
Patch1632: kvm-util-introduce-MIN_NON_ZERO.patch
# For bz#1318199 - expose host BLKSECTGET limit in scsi-block (qemu-kvm)
Patch1633: kvm-BlockLimits-introduce-max_transfer_length.patch
# For bz#1318199 - expose host BLKSECTGET limit in scsi-block (qemu-kvm)
Patch1634: kvm-block-backend-expose-bs-bl.max_transfer_length.patch
# For bz#1318199 - expose host BLKSECTGET limit in scsi-block (qemu-kvm)
Patch1635: kvm-scsi-generic-Merge-block-max-xfer-len-in-INQUIRY-res.patch
# For bz#1318199 - expose host BLKSECTGET limit in scsi-block (qemu-kvm)
Patch1636: kvm-raw-posix-Fetch-max-sectors-for-host-block-device.patch
# For bz#1318199 - expose host BLKSECTGET limit in scsi-block (qemu-kvm)
Patch1637: kvm-scsi-Advertise-limits-by-blocksize-not-512.patch
# For bz#1318199 - expose host BLKSECTGET limit in scsi-block (qemu-kvm)
Patch1638: kvm-util-Fix-MIN_NON_ZERO.patch
# For bz#1355730 - spice-gtk shows outdated screen state after migration [qemu-kvm]
Patch1639: kvm-qxl-factor-out-qxl_get_check_slot_offset.patch
# For bz#1355730 - spice-gtk shows outdated screen state after migration [qemu-kvm]
Patch1640: kvm-qxl-store-memory-region-and-offset-instead-of-pointe.patch
# For bz#1355730 - spice-gtk shows outdated screen state after migration [qemu-kvm]
Patch1641: kvm-qxl-fix-surface-migration.patch
# For bz#1355730 - spice-gtk shows outdated screen state after migration [qemu-kvm]
Patch1642: kvm-qxl-fix-qxl_set_dirty-call-in-qxl_dirty_one_surface.patch
# For bz#1359729 - CVE-2016-5403 qemu-kvm: Qemu: virtio: unbounded memory allocation on host via guest leading to DoS [rhel-7.3]
Patch1643: kvm-virtio-error-out-if-guest-exceeds-virtqueue-size.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1644: kvm-json-parser-drop-superfluous-assignment-for-token-va.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1645: kvm-qjson-Apply-nesting-limit-more-sanely.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1646: kvm-qjson-Don-t-crash-when-input-exceeds-nesting-limit.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1647: kvm-check-qjson-Add-test-for-JSON-nesting-depth-limit.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1648: kvm-qjson-Spell-out-some-silent-assumptions.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1649: kvm-qjson-Give-each-of-the-six-structural-chars-its-own-.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1650: kvm-qjson-Inline-token_is_keyword-and-simplify.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1651: kvm-qjson-Inline-token_is_escape-and-simplify.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1652: kvm-qjson-replace-QString-in-JSONLexer-with-GString.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1653: kvm-qjson-Convert-to-parser-to-recursive-descent.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1654: kvm-qjson-store-tokens-in-a-GQueue.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1655: kvm-qjson-surprise-allocating-6-QObjects-per-token-is-ex.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1656: kvm-qjson-Limit-number-of-tokens-in-addition-to-total-si.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1657: kvm-json-streamer-Don-t-leak-tokens-on-incomplete-parse.patch
# For bz#1276036 - Crash on QMP input exceeding limits
Patch1658: kvm-json-streamer-fix-double-free-on-exiting-during-a-pa.patch
# For bz#1360137 - GLib-WARNING **: gmem.c:482: custom memory allocation vtable not supported
Patch1659: kvm-trace-remove-malloc-tracing.patch
# For bz#1367040 - QEMU crash when guest notifies non-existent virtqueue
Patch1660: kvm-virtio-validate-the-existence-of-handle_output-befor.patch
# For bz#1371619 - Flags xsaveopt xsavec xgetbv1 are missing on qemu-kvm
Patch1661: kvm-Fix-backport-of-target-i386-add-feature-flags-for-CP.patch
# For bz#1373088 - [FJ7.3 Bug]: virsh dump with both --memory-only and --format option fails
Patch1662: kvm-Add-skip_dump-flag-to-ignore-memory-region-during-du.patch
# For bz#1372459 - [Intel 7.3 Bug] SKL-SP Guest cpu doesn't support avx512 instruction sets(avx512bw, avx512dq and avx512vl) (qemu-kvm)
Patch1663: kvm-target-i386-Add-support-for-FEAT_7_0_ECX.patch
# For bz#1372459 - [Intel 7.3 Bug] SKL-SP Guest cpu doesn't support avx512 instruction sets(avx512bw, avx512dq and avx512vl) (qemu-kvm)
Patch1664: kvm-target-i386-Add-more-Intel-AVX-512-instructions-supp.patch
# For bz#1285453 - An NBD client can cause QEMU main loop to block when connecting to built-in NBD server
Patch1665: kvm-nbd-server-Set-O_NONBLOCK-on-client-fd.patch
# For bz#1376542 - RHSA-2016-1756 breaks migration of instances
Patch1666: kvm-virtio-recalculate-vq-inuse-after-migration.patch
# For bz#1377087 - shutdown rhel 5.11 guest failed and stop at "system halted"
Patch1667: kvm-hw-i386-regenerate-checked-in-AML-payload-RHEL-only.patch
# For bz#1377968 - [RHEL7.3] KVM guest shuts itself down after 128th reboot
Patch1668: kvm-virtio-introduce-virtqueue_unmap_sg.patch
# For bz#1377968 - [RHEL7.3] KVM guest shuts itself down after 128th reboot
Patch1669: kvm-virtio-introduce-virtqueue_discard.patch
# For bz#1377968 - [RHEL7.3] KVM guest shuts itself down after 128th reboot
Patch1670: kvm-virtio-decrement-vq-inuse-in-virtqueue_discard.patch
# For bz#1377968 - [RHEL7.3] KVM guest shuts itself down after 128th reboot
Patch1671: kvm-balloon-fix-segfault-and-harden-the-stats-queue.patch
# For bz#1377968 - [RHEL7.3] KVM guest shuts itself down after 128th reboot
Patch1672: kvm-virtio-balloon-discard-virtqueue-element-on-reset.patch
# For bz#1377968 - [RHEL7.3] KVM guest shuts itself down after 128th reboot
Patch1673: kvm-virtio-zero-vq-inuse-in-virtio_reset.patch
# For bz#1377968 - [RHEL7.3] KVM guest shuts itself down after 128th reboot
Patch1674: kvm-virtio-add-virtqueue_rewind.patch
# For bz#1377968 - [RHEL7.3] KVM guest shuts itself down after 128th reboot
Patch1675: kvm-virtio-balloon-fix-stats-vq-migration.patch
# For bz#1375507 - "threads" option is overwritten if both "sockets" and "cores" is set on -smp
Patch1676: kvm-vl-Don-t-silently-change-topology-when-all-smp-optio.patch
# For bz#1398218 - CVE-2016-2857 qemu-kvm: Qemu: net: out of bounds read in net_checksum_calculate() [rhel-7.4]
Patch1677: kvm-net-check-packet-payload-length.patch
# For bz#1342489 - Flickering Fedora 24 Login Screen on RHEL 7
Patch1678: kvm-qxl-Only-emit-QXL_INTERRUPT_CLIENT_MONITORS_CONFIG-o.patch
# For bz#1151859 - [RFE] Allow the libgfapi logging level to be controlled.
Patch1679: kvm-gluster-correctly-propagate-errors.patch
# For bz#1151859 - [RFE] Allow the libgfapi logging level to be controlled.
Patch1680: kvm-gluster-Correctly-propagate-errors-when-volume-isn-t.patch
# For bz#1151859 - [RFE] Allow the libgfapi logging level to be controlled.
Patch1681: kvm-block-gluster-add-support-for-selecting-debug-loggin.patch
# For bz#1342768 - [Intel 7.4 Bug] qemu-kvm crashes with Linux kernel 4.6.0 or above
Patch1682: kvm-memory-Allow-access-only-upto-the-maximum-alignment-.patch
# For bz#1361488 - system_reset should clear pending request for error (virtio-blk)
Patch1683: kvm-virtio-blk-Release-s-rq-queue-at-system_reset.patch
# For bz#1418233 - CVE-2017-2615 qemu-kvm: Qemu: display: cirrus: oob access while doing bitblt copy backward mode [rhel-7.4]
Patch1684: kvm-cirrus_vga-fix-off-by-one-in-blit_region_is_unsafe.patch
# For bz#1418233 - CVE-2017-2615 qemu-kvm: Qemu: display: cirrus: oob access while doing bitblt copy backward mode [rhel-7.4]
Patch1685: kvm-display-cirrus-check-vga-bits-per-pixel-bpp-value.patch
# For bz#1418233 - CVE-2017-2615 qemu-kvm: Qemu: display: cirrus: oob access while doing bitblt copy backward mode [rhel-7.4]
Patch1686: kvm-display-cirrus-ignore-source-pitch-value-as-needed-i.patch
# For bz#1418233 - CVE-2017-2615 qemu-kvm: Qemu: display: cirrus: oob access while doing bitblt copy backward mode [rhel-7.4]
Patch1687: kvm-cirrus-handle-negative-pitch-in-cirrus_invalidate_re.patch
# For bz#1418233 - CVE-2017-2615 qemu-kvm: Qemu: display: cirrus: oob access while doing bitblt copy backward mode [rhel-7.4]
Patch1688: kvm-cirrus-allow-zero-source-pitch-in-pattern-fill-rops.patch
# For bz#1418233 - CVE-2017-2615 qemu-kvm: Qemu: display: cirrus: oob access while doing bitblt copy backward mode [rhel-7.4]
Patch1689: kvm-cirrus-fix-blit-address-mask-handling.patch
# For bz#1418233 - CVE-2017-2615 qemu-kvm: Qemu: display: cirrus: oob access while doing bitblt copy backward mode [rhel-7.4]
Patch1690: kvm-cirrus-fix-oob-access-issue-CVE-2017-2615.patch
# For bz#1419898 - Documentation inaccurate for __com.redhat_qxl_screendump and __com.redhat_drive_add
Patch1691: kvm-HMP-Fix-user-manual-typo-of-__com.redhat_qxl_screend.patch
# For bz#1419898 - Documentation inaccurate for __com.redhat_qxl_screendump and __com.redhat_drive_add
Patch1692: kvm-HMP-Fix-documentation-of-__com.redhat.drive_add.patch
# For bz#1420492 - EMBARGOED CVE-2017-2620 qemu-kvm: Qemu: display: cirrus: potential arbitrary code execution via cirrus_bitblt_cputovideo [rhel-7.4]
Patch1693: kvm-cirrus-fix-patterncopy-checks.patch
# For bz#1420492 - EMBARGOED CVE-2017-2620 qemu-kvm: Qemu: display: cirrus: potential arbitrary code execution via cirrus_bitblt_cputovideo [rhel-7.4]
Patch1694: kvm-Revert-cirrus-allow-zero-source-pitch-in-pattern-fil.patch
# For bz#1420492 - EMBARGOED CVE-2017-2620 qemu-kvm: Qemu: display: cirrus: potential arbitrary code execution via cirrus_bitblt_cputovideo [rhel-7.4]
Patch1695: kvm-cirrus-add-blit_is_unsafe-call-to-cirrus_bitblt_cput.patch
# For bz#1368375 - [Intel 7.4 Bug] qemu-kvm does not support “-cpu IvyBridge”
Patch1696: kvm-target-i386-add-Ivy-Bridge-CPU-model.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1697: kvm-x86-add-AVX512_4VNNIW-and-AVX512_4FMAPS-features.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1698: kvm-target-i386-kvm_cpu_fill_host-Kill-unused-code.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1699: kvm-target-i386-kvm_cpu_fill_host-No-need-to-check-level.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1700: kvm-target-i386-kvm_cpu_fill_host-No-need-to-check-CPU-v.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1701: kvm-target-i386-kvm_cpu_fill_host-No-need-to-check-xleve.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1702: kvm-target-i386-kvm_cpu_fill_host-Set-all-feature-words-.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1703: kvm-target-i386-kvm_cpu_fill_host-Fill-feature-words-in-.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1704: kvm-target-i386-kvm_check_features_against_host-Kill-fea.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1705: kvm-target-i386-Make-TCG-feature-filtering-more-readable.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1706: kvm-target-i386-Filter-FEAT_7_0_EBX-TCG-features-too.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1707: kvm-target-i386-Filter-KVM-and-0xC0000001-features-on-TC.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1708: kvm-target-i386-Define-TCG_-_FEATURES-earlier-in-cpu.c.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1709: kvm-target-i386-Loop-based-copying-and-setting-unsetting.patch
# For bz#1382122 - [Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu
Patch1710: kvm-target-i386-Loop-based-feature-word-filtering-in-TCG.patch
# For bz#1430606 - Can't build qemu-kvm with newer spice packages
Patch1711: kvm-spice-remove-spice-experimental.h-include.patch
# For bz#1430606 - Can't build qemu-kvm with newer spice packages
Patch1712: kvm-spice-replace-use-of-deprecated-API.patch
# For bz#1377977 - qemu-kvm coredump in vnc_raw_send_framebuffer_update [rhel-7.4]
Patch1713: kvm-ui-vnc-introduce-VNC_DIRTY_PIXELS_PER_BIT-macro.patch
# For bz#1377977 - qemu-kvm coredump in vnc_raw_send_framebuffer_update [rhel-7.4]
Patch1714: kvm-ui-vnc-derive-cmp_bytes-from-VNC_DIRTY_PIXELS_PER_BI.patch
# For bz#1377977 - qemu-kvm coredump in vnc_raw_send_framebuffer_update [rhel-7.4]
Patch1715: kvm-ui-vnc-optimize-dirty-bitmap-tracking.patch
# For bz#1377977 - qemu-kvm coredump in vnc_raw_send_framebuffer_update [rhel-7.4]
Patch1716: kvm-ui-vnc-optimize-setting-in-vnc_dpy_update.patch
# For bz#1377977 - qemu-kvm coredump in vnc_raw_send_framebuffer_update [rhel-7.4]
Patch1717: kvm-ui-vnc-fix-vmware-VGA-incompatiblities.patch
# For bz#1377977 - qemu-kvm coredump in vnc_raw_send_framebuffer_update [rhel-7.4]
Patch1718: kvm-ui-vnc-fix-potential-memory-corruption-issues.patch
# For bz#1377977 - qemu-kvm coredump in vnc_raw_send_framebuffer_update [rhel-7.4]
Patch1719: kvm-vnc-fix-memory-corruption-CVE-2015-5225.patch
# For bz#1377977 - qemu-kvm coredump in vnc_raw_send_framebuffer_update [rhel-7.4]
Patch1720: kvm-vnc-fix-overflow-in-vnc_update_stats.patch
# For bz#1335751 - CVE-2016-4020 qemu-kvm: Qemu: i386: leakage of stack memory to guest in kvmvapic.c [rhel-7.4]
Patch1721: kvm-i386-kvmvapic-initialise-imm32-variable.patch
# For bz#1427176 - test cases of qemu-iotests failed
Patch1722: kvm-qemu-iotests-Filter-out-actual-image-size-in-067.patch
# For bz#1427176 - test cases of qemu-iotests failed
Patch1723: kvm-qcow2-Don-t-rely-on-free_cluster_index-in-alloc_ref2.patch
# For bz#1427176 - test cases of qemu-iotests failed
Patch1724: kvm-qemu-iotests-Fix-core-dump-suppression-in-test-039.patch
# For bz#1427176 - test cases of qemu-iotests failed
Patch1725: kvm-qemu-io-Add-sigraise-command.patch
# For bz#1427176 - test cases of qemu-iotests failed
Patch1726: kvm-iotests-Filter-for-Killed-in-qemu-io-output.patch
# For bz#1427176 - test cases of qemu-iotests failed
Patch1727: kvm-iotests-Fix-test-039.patch
# For bz#1427176 - test cases of qemu-iotests failed
Patch1728: kvm-blkdebug-Add-bdrv_truncate.patch
# For bz#1427176 - test cases of qemu-iotests failed
Patch1729: kvm-vhdx-Fix-zero-fill-iov-length.patch
# For bz#1427176 - test cases of qemu-iotests failed
Patch1730: kvm-qemu-iotests-Disable-030-040-041.patch
# For bz#1415830 - [Intel 7.4 FEAT] Enable vpopcntdq for KNM - qemu/kvm
Patch1731: kvm-x86-add-AVX512_VPOPCNTDQ-features.patch
# For bz#1419818 - CVE-2017-5898 qemu-kvm: Qemu: usb: integer overflow in emulated_apdu_from_guest [rhel-7.4]
Patch1732: kvm-usb-ccid-check-ccid-apdu-length.patch
# For bz#1419818 - CVE-2017-5898 qemu-kvm: Qemu: usb: integer overflow in emulated_apdu_from_guest [rhel-7.4]
Patch1733: kvm-usb-ccid-better-bulk_out-error-handling.patch
# For bz#1419818 - CVE-2017-5898 qemu-kvm: Qemu: usb: integer overflow in emulated_apdu_from_guest [rhel-7.4]
Patch1734: kvm-usb-ccid-move-header-size-check.patch
# For bz#1419818 - CVE-2017-5898 qemu-kvm: Qemu: usb: integer overflow in emulated_apdu_from_guest [rhel-7.4]
Patch1735: kvm-usb-ccid-add-check-message-size-checks.patch
# For bz#1430060 - CVE-2016-9603 qemu-kvm: Qemu: cirrus: heap buffer overflow via vnc connection [rhel-7.4]
Patch1736: kvm-fix-cirrus_vga-fix-OOB-read-case-qemu-Segmentation-f.patch
# For bz#1430060 - CVE-2016-9603 qemu-kvm: Qemu: cirrus: heap buffer overflow via vnc connection [rhel-7.4]
Patch1737: kvm-cirrus-vnc-zap-bitblit-support-from-console-code.patch
# For bz#1430060 - CVE-2016-9603 qemu-kvm: Qemu: cirrus: heap buffer overflow via vnc connection [rhel-7.4]
Patch1738: kvm-cirrus-add-option-to-disable-blitter.patch
# For bz#1430060 - CVE-2016-9603 qemu-kvm: Qemu: cirrus: heap buffer overflow via vnc connection [rhel-7.4]
Patch1739: kvm-cirrus-fix-cirrus_invalidate_region.patch
# For bz#1430060 - CVE-2016-9603 qemu-kvm: Qemu: cirrus: heap buffer overflow via vnc connection [rhel-7.4]
Patch1740: kvm-cirrus-stop-passing-around-dst-pointers-in-the-blitt.patch
# For bz#1430060 - CVE-2016-9603 qemu-kvm: Qemu: cirrus: heap buffer overflow via vnc connection [rhel-7.4]
Patch1741: kvm-cirrus-stop-passing-around-src-pointers-in-the-blitt.patch
# For bz#1430060 - CVE-2016-9603 qemu-kvm: Qemu: cirrus: heap buffer overflow via vnc connection [rhel-7.4]
Patch1742: kvm-cirrus-fix-off-by-one-in-cirrus_bitblt_rop_bkwd_tran.patch
# For bz#1327593 - [Intel 7.4 FEAT] KVM Enable the XSAVEC, XSAVES and XRSTORS instructions
Patch1743: kvm-target-i386-get-set-migrate-XSAVES-state.patch
# For bz#1299875 - system_reset should clear pending request for error (IDE)
Patch1744: kvm-ide-fix-halted-IO-segfault-at-reset.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1745: kvm-char-serial-cosmetic-fixes.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1746: kvm-char-serial-Use-generic-Fifo8.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1747: kvm-char-serial-serial_ioport_write-Factor-out-common-co.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1748: kvm-char-serial-fix-copy-paste-error-fifo8_is_full-vs-em.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1749: kvm-char-serial-Fix-emptyness-check.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1750: kvm-char-serial-Fix-emptyness-handling.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1751: kvm-serial-poll-the-serial-console-with-G_IO_HUP.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1752: kvm-serial-change-retry-logic-to-avoid-concurrency.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1753: kvm-qemu-char-ignore-flow-control-if-a-PTY-s-slave-is-no.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1754: kvm-serial-check-if-backed-by-a-physical-serial-port-at-.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1755: kvm-serial-reset-thri_pending-on-IER-writes-with-THRI-0.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1756: kvm-serial-clean-up-THRE-TEMT-handling.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1757: kvm-serial-update-LSR-on-enabling-disabling-FIFOs.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1758: kvm-serial-only-resample-THR-interrupt-on-rising-edge-of.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1759: kvm-serial-make-tsr_retry-unsigned.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1760: kvm-serial-simplify-tsr_retry-reset.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1761: kvm-serial-separate-serial_xmit-and-serial_watch_cb.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1762: kvm-serial-remove-watch-on-reset.patch
# For bz#1451470 - RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop
Patch1763: kvm-char-change-qemu_chr_fe_add_watch-to-return-unsigned.patch
# For bz#1456983 - Character device regression due to missing patch
Patch1764: kvm-spice-fix-spice_chr_add_watch-pre-condition.patch
# For bz#1455745 - Backport fix for broken logic that's supposed to ensure memory slots are page aligned
Patch1765: kvm-Fix-memory-slot-page-alignment-logic-bug-1455745.patch
# For bz#1452067 - migration can confuse serial port user
Patch1766: kvm-Do-not-hang-on-full-PTY.patch
# For bz#1452067 - migration can confuse serial port user
Patch1767: kvm-serial-fixing-vmstate-for-save-restore.patch
# For bz#1452067 - migration can confuse serial port user
Patch1768: kvm-serial-reinstate-watch-after-migration.patch
# For bz#1451614 - CVE-2017-9524 qemu-kvm: segment fault when private user nmap qemu-nbd server [rhel-7.4]
Patch1769: kvm-nbd-Fully-initialize-client-in-case-of-failed-negoti.patch
# For bz#1451614 - CVE-2017-9524 qemu-kvm: segment fault when private user nmap qemu-nbd server [rhel-7.4]
Patch1770: kvm-nbd-Fix-regression-on-resiliency-to-port-scan.patch
# For bz#1435352 - qemu started with "-vnc none,..." doesn't support any VNC authentication
Patch1771: kvm-vnc-allow-to-connect-with-add_client-when-vnc-none.patch
# For bz#1480428 - KVM: windows guest migration from EL6 to EL7 fails.
Patch1772: kvm-virtio-net-dynamic-network-offloads-configuration.patch
# For bz#1480428 - KVM: windows guest migration from EL6 to EL7 fails.
Patch1773: kvm-Workaround-rhel6-ctrl_guest_offloads-machine-type-mi.patch
# For bz#1387648 - [Intel 7.5 FEAT] Memory Protection Keys for qemu-kvm
Patch1774: kvm-target-i386-Add-PKU-and-and-OSPKE-support.patch
# For bz#1492559 - virtio-blk mutiwrite merge causes too big IO
Patch1775: kvm-block-Limit-multiwrite-merge-downstream-only.patch
# For bz#1466463 - CVE-2017-10664 qemu-kvm: Qemu: qemu-nbd: server breaks with SIGPIPE upon client abort [rhel-7.5]
Patch1776: kvm-qemu-nbd-Ignore-SIGPIPE.patch
# For bz#1476641 - ui/vnc_keysym.h is very out of date and does not correctly support many Eastern European keyboards
Patch1777: kvm-qemu-char-add-Czech-characters-to-VNC-keysyms.patch
# For bz#1476641 - ui/vnc_keysym.h is very out of date and does not correctly support many Eastern European keyboards
Patch1778: kvm-qemu-char-add-missing-characters-used-in-keymaps.patch
# For bz#1476641 - ui/vnc_keysym.h is very out of date and does not correctly support many Eastern European keyboards
Patch1779: kvm-qemu-char-add-cyrillic-characters-numerosign-to-VNC-.patch
# For bz#1461672 - qemu-img core dumped when create external snapshot through ssh protocol without specifying image size
Patch1780: kvm-block-ssh-Use-QemuOpts-for-runtime-options.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1781: kvm-vfio-pass-device-to-vfio_mmap_bar-and-use-it-to-set-.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1782: kvm-hw-vfio-pci-Rename-VFIODevice-into-VFIOPCIDevice.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1783: kvm-hw-vfio-pci-generalize-mask-unmask-to-any-IRQ-index.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1784: kvm-hw-vfio-pci-introduce-minimalist-VFIODevice-with-fd.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1785: kvm-hw-vfio-pci-add-type-name-and-group-fields-in-VFIODe.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1786: kvm-hw-vfio-pci-handle-reset-at-VFIODevice.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1787: kvm-hw-vfio-pci-Introduce-VFIORegion.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1788: kvm-hw-vfio-pci-use-name-field-in-format-strings.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1789: kvm-vfio-Add-sysfsdev-property-for-pci-platform.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1790: kvm-vfio-remove-bootindex-property-from-qdev-to-qom.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1791: kvm-vfio-pci-Handle-host-oversight.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1792: kvm-vfio-pci-Fix-incorrect-error-message.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1793: kvm-vfio-Wrap-VFIO_DEVICE_GET_REGION_INFO.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1794: kvm-vfio-Generalize-region-support.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1795: kvm-vfio-Enable-sparse-mmap-capability.patch
# For bz#1494181 - Backport vGPU support to qemu-kvm
Patch1796: kvm-vfio-Handle-zero-length-sparse-mmap-ranges.patch
# For bz#1486642 - CVE-2017-13672 qemu-kvm: Qemu: vga: OOB read access during display update [rhel-7.5]
Patch1797: kvm-bswap.h-Remove-cpu_to_32wu.patch
# For bz#1486642 - CVE-2017-13672 qemu-kvm: Qemu: vga: OOB read access during display update [rhel-7.5]
Patch1798: kvm-hw-use-ld_p-st_p-instead-of-ld_raw-st_raw.patch
# For bz#1486642 - CVE-2017-13672 qemu-kvm: Qemu: vga: OOB read access during display update [rhel-7.5]
Patch1799: kvm-vga-Start-cutting-out-non-32bpp-conversion-support.patch
# For bz#1486642 - CVE-2017-13672 qemu-kvm: Qemu: vga: OOB read access during display update [rhel-7.5]
Patch1800: kvm-vga-Remove-remainder-of-old-conversion-cruft.patch
# For bz#1486642 - CVE-2017-13672 qemu-kvm: Qemu: vga: OOB read access during display update [rhel-7.5]
Patch1801: kvm-vga-Separate-LE-and-BE-conversion-functions.patch
# For bz#1486642 - CVE-2017-13672 qemu-kvm: Qemu: vga: OOB read access during display update [rhel-7.5]
Patch1802: kvm-vga-Rename-vga_template.h-to-vga-helpers.h.patch
# For bz#1486642 - CVE-2017-13672 qemu-kvm: Qemu: vga: OOB read access during display update [rhel-7.5]
Patch1803: kvm-vga-stop-passing-pointers-to-vga_draw_line-functions.patch
# For bz#1450396 - Add support for AMD EPYC processors
Patch1804: kvm-target-i386-Add-Intel-SHA_NI-instruction-support.patch
# For bz#1450396 - Add support for AMD EPYC processors
Patch1805: kvm-target-i386-cpu-Add-new-EPYC-CPU-model.patch
# For bz#1501510 - Add Skylake-Server CPU model (qemu-kvm)
Patch1806: kvm-target-i386-Enable-clflushopt-clwb-pcommit-instructi.patch
# For bz#1501510 - Add Skylake-Server CPU model (qemu-kvm)
Patch1807: kvm-i386-add-Skylake-Server-cpu-model.patch
# For bz#1501295 - CVE-2017-15289 qemu-kvm: Qemu: cirrus: OOB access issue in  mode4and5 write functions [rhel-7.5]
Patch1808: kvm-vga-drop-line_offset-variable.patch
# For bz#1501295 - CVE-2017-15289 qemu-kvm: Qemu: cirrus: OOB access issue in  mode4and5 write functions [rhel-7.5]
Patch1809: kvm-vga-Add-mechanism-to-force-the-use-of-a-shadow-surfa.patch
# For bz#1501295 - CVE-2017-15289 qemu-kvm: Qemu: cirrus: OOB access issue in  mode4and5 write functions [rhel-7.5]
Patch1810: kvm-vga-handle-cirrus-vbe-mode-wraparounds.patch
# For bz#1501295 - CVE-2017-15289 qemu-kvm: Qemu: cirrus: OOB access issue in  mode4and5 write functions [rhel-7.5]
Patch1811: kvm-cirrus-fix-oob-access-in-mode4and5-write-functions.patch
# For bz#1470244 - reboot leads to shutoff of qemu-kvm-vm if i6300esb-watchdog set to poweroff
Patch1812: kvm-i6300esb-Fix-signed-integer-overflow.patch
# For bz#1470244 - reboot leads to shutoff of qemu-kvm-vm if i6300esb-watchdog set to poweroff
Patch1813: kvm-i6300esb-fix-timer-overflow.patch
# For bz#1470244 - reboot leads to shutoff of qemu-kvm-vm if i6300esb-watchdog set to poweroff
Patch1814: kvm-i6300esb-remove-muldiv64.patch
# For bz#1501121 - CVE-2017-14167 qemu-kvm: Qemu: i386: multiboot OOB access while loading kernel image [rhel-7.5]
Patch1815: kvm-multiboot-validate-multiboot-header-address-values.patch
# For bz#1417864 - Qemu-kvm starts with unspecified port
Patch1816: kvm-qemu-option-reject-empty-number-value.patch
# For bz#1491434 - KVM leaks file descriptors when attaching and detaching virtio-scsi block devices
Patch1817: kvm-block-linux-aio-fix-memory-and-fd-leak.patch
# For bz#1491434 - KVM leaks file descriptors when attaching and detaching virtio-scsi block devices
Patch1818: kvm-linux-aio-Fix-laio-resource-leak.patch
# For bz#1508745 - CVE-2017-13711 qemu-kvm: Qemu: Slirp: use-after-free when sending response [rhel-7.5]
Patch1819: kvm-slirp-cleanup-leftovers-from-misc.h.patch
# For bz#1508745 - CVE-2017-13711 qemu-kvm: Qemu: Slirp: use-after-free when sending response [rhel-7.5]
Patch1820: kvm-Avoid-embedding-struct-mbuf-in-other-structures.patch
# For bz#1508745 - CVE-2017-13711 qemu-kvm: Qemu: Slirp: use-after-free when sending response [rhel-7.5]
Patch1821: kvm-slirp-Fix-access-to-freed-memory.patch
# For bz#1508745 - CVE-2017-13711 qemu-kvm: Qemu: Slirp: use-after-free when sending response [rhel-7.5]
Patch1822: kvm-slirp-fix-clearing-ifq_so-from-pending-packets.patch
# For bz#1459714 - Throw error if qemu-img rebasing backing file is too long or provide way to fix a "too long" backing file.
Patch1823: kvm-qcow2-Prevent-backing-file-names-longer-than-1023.patch
# For bz#1459725 - Prevent qemu-img resize from causing "Active L1 table too large"
Patch1824: kvm-qemu-img-Use-strerror-for-generic-resize-error.patch
# For bz#1459725 - Prevent qemu-img resize from causing "Active L1 table too large"
Patch1825: kvm-qcow2-Avoid-making-the-L1-table-too-big.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1826: kvm-fw_cfg-remove-support-for-guest-side-data-writes.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1827: kvm-fw_cfg-prevent-selector-key-conflict.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1828: kvm-fw_cfg-prohibit-insertion-of-duplicate-fw_cfg-file-n.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1829: kvm-fw_cfg-factor-out-initialization-of-FW_CFG_ID-rev.-n.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1830: kvm-Implement-fw_cfg-DMA-interface.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1831: kvm-fw_cfg-avoid-calculating-invalid-current-entry-point.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1832: kvm-fw-cfg-support-writeable-blobs.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1833: kvm-Enable-fw_cfg-DMA-interface-for-x86.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1834: kvm-fw_cfg-unbreak-migration-compatibility.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1835: kvm-i386-expose-fw_cfg-QEMU0002-in-SSDT.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1836: kvm-fw_cfg-add-write-callback.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1837: kvm-hw-misc-add-vmcoreinfo-device.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1838: kvm-vmcoreinfo-put-it-in-the-misc-device-category.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1839: kvm-fw_cfg-enable-DMA-if-device-vmcoreinfo.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1840: kvm-build-sys-restrict-vmcoreinfo-to-fw_cfg-dma-capable-.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1841: kvm-dump-Make-DumpState-and-endian-conversion-routines-a.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1842: kvm-dump.c-Fix-memory-leak-issue-in-cleanup-processing-f.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1843: kvm-dump-Propagate-errors-into-qmp_dump_guest_memory.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1844: kvm-dump-Turn-some-functions-to-void-to-make-code-cleane.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1845: kvm-dump-Fix-dump-guest-memory-termination-and-use-after.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1846: kvm-dump-allow-target-to-set-the-page-size.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1847: kvm-dump-allow-target-to-set-the-physical-base.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1848: kvm-dump-guest-memory-cleanup-removing-dump_-error-clean.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1849: kvm-dump-guest-memory-using-static-DumpState-add-DumpSta.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1850: kvm-dump-guest-memory-add-dump_in_progress-helper-functi.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1851: kvm-dump-guest-memory-introduce-dump_process-helper-func.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1852: kvm-dump-guest-memory-disable-dump-when-in-INMIGRATE-sta.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1853: kvm-DumpState-adding-total_size-and-written_size-fields.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1854: kvm-dump-do-not-dump-non-existent-guest-memory.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1855: kvm-dump-add-guest-ELF-note.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1856: kvm-dump-update-phys_base-header-field-based-on-VMCOREIN.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1857: kvm-kdump-set-vmcoreinfo-location.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1858: kvm-scripts-dump-guest-memory.py-Move-constants-to-the-t.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1859: kvm-scripts-dump-guest-memory.py-Make-methods-functions.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1860: kvm-scripts-dump-guest-memory.py-Improve-python-3-compat.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1861: kvm-scripts-dump-guest-memory.py-Cleanup-functions.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1862: kvm-scripts-dump-guest-memory.py-Introduce-multi-arch-su.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1863: kvm-Fix-typo-in-variable-name-found-and-fixed-by-codespe.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1864: kvm-scripts-dump-guest-memory.py-add-vmcoreinfo.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1865: kvm-dump-guest-memory.py-fix-No-symbol-vmcoreinfo_find.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1866: kvm-dump-guest-memory.py-fix-You-can-t-do-that-without-a.patch
# For bz#CVE-2017-5715 
Patch1867: kvm-target-i386-cpu-add-new-CPUID-bits-for-indirect-bran.patch
# For bz#CVE-2017-5715 
Patch1868: kvm-target-i386-add-support-for-SPEC_CTRL-MSR.patch
# For bz#CVE-2017-5715 
Patch1869: kvm-target-i386-cpu-add-new-CPU-models-for-indirect-bran.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1870: kvm-i386-update-ssdt-misc.hex.generated.patch
# For bz#1435432 - Emulated ISA serial port hangs randomly when sending lots of data from guest -> host
# For bz#1473536 - Hangs in serial console under qemu
Patch1871: kvm-main-loop-Acquire-main_context-lock-around-os_host_m.patch
# For bz#1460872 - Aborted(core dumped) when booting guest with "-netdev tap....vhost=on,queues=32"
Patch1872: kvm-virtio-net-validate-backend-queue-numbers-against-bu.patch
# For bz#1411490 - [RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm)
Patch1873: kvm-dump-guest-memory.py-fix-python-2-support.patch
# For bz#1536883 - [abrt] [faf] qemu-kvm: unknown function(): /usr/libexec/qemu-kvm killed by 6
Patch1874: kvm-qxl-add-migration-blocker-to-avoid-pre-save-assert.patch
# For bz#1538866 - qemu will coredump after executing info qtree
Patch1875: kvm-qdev-Fix-assert-in-PCI-address-property-when-used-by.patch
# For bz#1534691 - CVE-2018-5683 qemu-kvm: Qemu: Out-of-bounds read in vga_draw_text routine [rhel-7.5]
Patch1876: kvm-vga-check-the-validation-of-memory-addr-when-draw-te.patch
# For bz#1536883 - [abrt] [faf] qemu-kvm: unknown function(): /usr/libexec/qemu-kvm killed by 6
Patch1877: kvm-savevm-Improve-error-message-for-blocked-migration.patch
# For bz#1536883 - [abrt] [faf] qemu-kvm: unknown function(): /usr/libexec/qemu-kvm killed by 6
Patch1878: kvm-savevm-fail-if-migration-blockers-are-present.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1879: kvm-vnc-Fix-qemu-crashed-when-vnc-client-disconnect-sudd.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1880: kvm-fix-full-frame-updates-for-VNC-clients.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1881: kvm-vnc-update-fix.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1882: kvm-vnc-return-directly-if-no-vnc-client-connected.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1883: kvm-buffer-add-buffer_move_empty.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1884: kvm-buffer-add-buffer_move.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1885: kvm-vnc-kill-jobs-queue-buffer.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1886: kvm-vnc-jobs-move-buffer-reset-use-new-buffer-move.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1887: kvm-vnc-zap-dead-code.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1888: kvm-vnc-add-vnc_width-vnc_height-helpers.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1889: kvm-vnc-factor-out-vnc_update_server_surface.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1890: kvm-vnc-use-vnc_-width-height-in-vnc_set_area_dirty.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1891: kvm-vnc-only-alloc-server-surface-with-clients-connected.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1892: kvm-ui-fix-refresh-of-VNC-server-surface.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1893: kvm-ui-move-disconnecting-check-to-start-of-vnc_update_c.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1894: kvm-ui-remove-redundant-indentation-in-vnc_client_update.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1895: kvm-ui-avoid-pointless-VNC-updates-if-framebuffer-isn-t-.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1896: kvm-ui-track-how-much-decoded-data-we-consumed-when-doin.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1897: kvm-ui-introduce-enum-to-track-VNC-client-framebuffer-up.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1898: kvm-ui-correctly-reset-framebuffer-update-state-after-pr.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1899: kvm-ui-refactor-code-for-determining-if-an-update-should.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1900: kvm-ui-fix-VNC-client-throttling-when-audio-capture-is-a.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1901: kvm-ui-fix-VNC-client-throttling-when-forced-update-is-r.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1902: kvm-ui-place-a-hard-cap-on-VNC-server-output-buffer-size.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1903: kvm-ui-avoid-sign-extension-using-client-width-height.patch
# For bz#1527405 - CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5]
Patch1904: kvm-ui-correctly-advance-output-buffer-when-writing-SASL.patch
# For bz#1518711 - CVE-2017-15268 qemu-kvm: Qemu: I/O: potential memory exhaustion via websock connection to VNC [rhel-7.5]
Patch1905: kvm-io-skip-updates-to-client-if-websocket-output-buffer.patch
# For bz#1567913 - CVE-2018-7858 qemu-kvm: Qemu: cirrus: OOB access when updating vga display [rhel-7] [rhel-7.5.z]
Patch1906: kvm-vga-add-ram_addr_t-cast.patch
# For bz#1567913 - CVE-2018-7858 qemu-kvm: Qemu: cirrus: OOB access when updating vga display [rhel-7] [rhel-7.5.z]
Patch1907: kvm-vga-fix-region-calculation.patch
# For bz#1574075 - EMBARGOED CVE-2018-3639 qemu-kvm: Kernel: omega-4 [rhel-7.5.z]
Patch1908: kvm-i386-define-the-ssbd-CPUID-feature-bit-CVE-2018-3639.patch
# For bz#1584363 - CVE-2018-3639 qemu-kvm: hw: cpu: AMD: speculative store bypass [rhel-7.5.z]
Patch1909: kvm-i386-Define-the-Virt-SSBD-MSR-and-handling-of-it-CVE.patch
# For bz#1584363 - CVE-2018-3639 qemu-kvm: hw: cpu: AMD: speculative store bypass [rhel-7.5.z]
Patch1910: kvm-i386-define-the-AMD-virt-ssbd-CPUID-feature-bit-CVE-.patch


BuildRequires: zlib-devel
BuildRequires: SDL-devel
BuildRequires: which
BuildRequires: gnutls-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libtool
BuildRequires: libaio-devel
BuildRequires: rsync
BuildRequires: python
BuildRequires: pciutils-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libiscsi-devel
BuildRequires: ncurses-devel
BuildRequires: libattr-devel
BuildRequires: libusbx-devel
%if 0%{?have_usbredir:1}
BuildRequires: usbredir-devel >= 0.6
%endif
BuildRequires: texinfo
%if 0%{!?build_only_sub:1}
    %if 0%{?have_spice:1}
BuildRequires: spice-protocol >= 0.12.2
BuildRequires: spice-server-devel >= 0.12.0
    %endif
%endif
%if 0%{?have_seccomp:1}
BuildRequires: libseccomp-devel >= 1.0.0
%endif
%if 0%{?have_tcmalloc:1}
BuildRequires: gperftools-devel
%endif
# For network block driver
BuildRequires: libcurl-devel
%ifarch x86_64
BuildRequires: librados2-devel
BuildRequires: librbd1-devel
%endif
%if 0%{!?build_only_sub:1}
# For gluster block driver
BuildRequires: glusterfs-api-devel >= 3.6.0
BuildRequires: glusterfs-devel
%endif
# We need both because the 'stap' binary is probed for by configure
BuildRequires: systemtap
BuildRequires: systemtap-sdt-devel
# For smartcard NSS support
BuildRequires: nss-devel
# For XFS discard support in raw-posix.c
# For VNC JPEG support
BuildRequires: libjpeg-devel
# For VNC PNG support
BuildRequires: libpng-devel
# For uuid generation
BuildRequires: libuuid-devel
# For BlueZ device support
BuildRequires: bluez-libs-devel
# For Braille device support
BuildRequires: brlapi-devel
# For test suite
BuildRequires: check-devel
# For virtfs
BuildRequires: libcap-devel
# Hard requirement for version >= 1.3
BuildRequires: pixman-devel
# Documentation requirement
BuildRequires: perl-podlators
BuildRequires: texinfo
# For rdma
%if 0%{?have_librdma:1}
BuildRequires: rdma-core-devel
%endif
# cpp for preprocessing option ROM assembly files
%ifarch %{ix86} x86_64
BuildRequires: cpp
%endif
%if 0%{!?build_only_sub:1}
# For compressed guest memory dumps
BuildRequires: lzo-devel snappy-devel
%endif
BuildRequires: libssh2-devel
BuildRequires: libcurl-devel


%if 0%{!?build_only_sub:1}
Requires: qemu-img = %{epoch}:%{version}-%{release}
%endif

# RHEV-specific changes:
# We provide special suffix for qemu-kvm so the conflit is easy
# In addition, RHEV version should obsolete all RHEL version in case both
# RHEL and RHEV channels are used
%rhel_rhev_conflicts qemu-kvm


%define qemudocdir %{_docdir}/%{pkgname}

%description
qemu-kvm%{?pkgsuffix} is an open source virtualizer that provides hardware
emulation for the KVM hypervisor. qemu-kvm%{?pkgsuffix} acts as a virtual
machine monitor together with the KVM kernel modules, and emulates the
hardware for a full system such as a PC and its associated peripherals.

%package -n qemu-img%{?pkgsuffix}
Summary: QEMU command line tool for manipulating disk images
Group: Development/Tools

%rhel_rhev_conflicts qemu-img

%description -n qemu-img%{?pkgsuffix}
This package provides a command line tool for manipulating disk images.

%if 0%{!?build_only_sub:1}
%package -n qemu-kvm-common%{?pkgsuffix}
Summary: QEMU common files needed by all QEMU targets
Group: Development/Tools
Requires(post): /usr/bin/getent
Requires(post): /usr/sbin/groupadd
Requires(post): /usr/sbin/useradd
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%rhel_rhev_conflicts qemu-kvm-common

%description -n qemu-kvm-common%{?pkgsuffix}
qemu-kvm is an open source virtualizer that provides hardware emulation for
the KVM hypervisor. 

This package provides documentation and auxiliary programs used with qemu-kvm.

%endif

%if %{with guest_agent}
%package -n qemu-guest-agent
Summary: QEMU guest agent
Group: System Environment/Daemons
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description -n qemu-guest-agent
qemu-kvm is an open source virtualizer that provides hardware emulation for
the KVM hypervisor. 

This package provides an agent to run inside guests, which communicates
with the host over a virtio-serial channel named "org.qemu.guest_agent.0"

This package does not need to be installed on the host OS.

%post -n qemu-guest-agent
%systemd_post qemu-guest-agent.service

%preun -n qemu-guest-agent
%systemd_preun qemu-guest-agent.service

%postun -n qemu-guest-agent
%systemd_postun_with_restart qemu-guest-agent.service

%endif

%if 0%{!?build_only_sub:1}
%package -n qemu-kvm-tools%{?pkgsuffix}
Summary: KVM debugging and diagnostics tools
Group: Development/Tools

%rhel_rhev_conflicts qemu-kvm-tools

%description -n qemu-kvm-tools%{?pkgsuffix}
This package contains some diagnostics and debugging tools for KVM,
such as kvm_stat.
%endif

%prep
%setup -q -n qemu-%{version}
cp %{SOURCE18} pc-bios # keep "make check" happy
tar -xf %{SOURCE21}
%patch1 -p1
#%%patch2 -p1
#%%patch3 -p1
#%%patch4 -p1
#%%patch5 -p1
#%%patch6 -p1
#%%patch7 -p1
#%%patch8 -p1
#%%patch9 -p1
#%%patch10 -p1
#%%patch11 -p1
#%%patch12 -p1
#%%patch13 -p1
#%%patch14 -p1
#%%patch15 -p1
#%%patch16 -p1
#%%patch17 -p1
#%%patch18 -p1
#%%patch19 -p1
#%%patch20 -p1
#%%patch21 -p1
#%%patch22 -p1
#%%patch23 -p1
#%%patch24 -p1
#%%patch25 -p1
#%%patch26 -p1
#%%patch27 -p1
#%%patch28 -p1
%patch29 -p1
%patch30 -p1
%patch31 -p1
%patch32 -p1
%patch33 -p1
%patch34 -p1
%patch35 -p1
%patch36 -p1
%patch37 -p1

# Fix CPUID model/level values on Conroe/Penryn/Nehalem CPU models
%patch38 -p1
%patch39 -p1
%patch40 -p1

#%patch41 -p1
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
#%%patch62 -p1
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
#%%patch73 -p1
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
#%%patch90 -p1
#%%patch91 -p1
#%%patch92 -p1
%patch93 -p1
%patch94 -p1
#%%patch95 -p1
%patch96 -p1
%patch97 -p1
%patch98 -p1
%patch99 -p1
%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
%patch120 -p1
%patch121 -p1
%patch122 -p1
%patch123 -p1
%patch124 -p1
%patch125 -p1
%patch126 -p1
%patch127 -p1
%patch128 -p1
%patch129 -p1
%patch130 -p1
%patch131 -p1
%patch132 -p1
%patch133 -p1
%patch134 -p1
%patch135 -p1
%patch136 -p1
%patch137 -p1
%patch138 -p1
%patch139 -p1
%patch140 -p1
%patch141 -p1
%patch142 -p1
%patch143 -p1
%patch144 -p1
%patch145 -p1
%patch146 -p1
%patch147 -p1
%patch148 -p1
%patch149 -p1
%patch150 -p1
%patch151 -p1
%patch152 -p1
%patch153 -p1
%patch154 -p1
%patch155 -p1
%patch156 -p1
%patch157 -p1
%patch158 -p1
%patch159 -p1
%patch160 -p1
%patch161 -p1
%patch162 -p1
%patch163 -p1
%patch164 -p1
%patch165 -p1
%patch166 -p1
%patch168 -p1
%patch169 -p1
%patch170 -p1
%patch171 -p1
%patch172 -p1
%patch173 -p1
%patch174 -p1
%patch175 -p1
%patch176 -p1
%patch177 -p1
%patch178 -p1
%patch179 -p1
%patch180 -p1
%patch181 -p1
%patch182 -p1
%patch183 -p1
%patch184 -p1
%patch185 -p1
%patch186 -p1
%patch187 -p1
%patch188 -p1
%patch189 -p1
%patch190 -p1
%patch191 -p1
%patch192 -p1
%patch193 -p1
%patch194 -p1
%patch195 -p1
%patch196 -p1
%patch197 -p1
%patch198 -p1
%patch199 -p1
%patch200 -p1
%patch201 -p1
%patch202 -p1
%patch203 -p1
%patch204 -p1
%patch205 -p1
%patch206 -p1
%patch207 -p1
%patch208 -p1
%patch209 -p1
%patch210 -p1
%patch211 -p1
%patch212 -p1
%patch213 -p1
%patch214 -p1
%patch215 -p1
%patch216 -p1
%patch217 -p1
%patch218 -p1
%patch219 -p1
%patch220 -p1
%patch221 -p1
%patch222 -p1
%patch223 -p1
%patch224 -p1
%patch225 -p1
%patch226 -p1
%patch227 -p1
%patch228 -p1
%patch229 -p1
%patch230 -p1
%patch231 -p1
%patch232 -p1
%patch233 -p1
%patch234 -p1
%patch235 -p1
%patch236 -p1
%patch237 -p1
%patch238 -p1
%patch239 -p1
%patch240 -p1
%patch241 -p1
%patch242 -p1
%patch243 -p1
%patch244 -p1
%patch245 -p1
%patch246 -p1
%patch247 -p1
%patch248 -p1
%patch249 -p1
%patch250 -p1
%patch251 -p1
%patch252 -p1
%patch253 -p1
%patch254 -p1
%patch255 -p1
%patch256 -p1
%patch257 -p1
%patch258 -p1
%patch259 -p1
%patch260 -p1
%patch261 -p1
%patch262 -p1
%patch263 -p1
%patch264 -p1
%patch265 -p1
%patch266 -p1
%patch267 -p1
%patch268 -p1
%patch269 -p1
%patch270 -p1
%patch271 -p1
%patch272 -p1
%patch273 -p1
%patch274 -p1
%patch275 -p1
%patch276 -p1
%patch277 -p1
%patch278 -p1
%patch279 -p1
%patch280 -p1
%patch281 -p1
%patch282 -p1
%patch283 -p1
%patch284 -p1
%patch285 -p1
%patch286 -p1
%patch287 -p1
%patch288 -p1
%patch289 -p1
%patch290 -p1
%patch291 -p1
%patch292 -p1
%patch293 -p1
%patch294 -p1
%patch295 -p1
%patch296 -p1
%patch297 -p1
%patch298 -p1
%patch299 -p1
%patch300 -p1
%patch301 -p1
%patch302 -p1
%patch303 -p1
%patch304 -p1
%patch305 -p1
%patch306 -p1
%patch307 -p1
%patch308 -p1
%patch309 -p1
%patch310 -p1
%patch311 -p1
%patch312 -p1
%patch313 -p1
%patch314 -p1
%patch315 -p1
%patch316 -p1
%patch317 -p1
%patch318 -p1
%patch319 -p1
%patch320 -p1
%patch321 -p1
%patch322 -p1
%patch323 -p1
%patch324 -p1
%patch325 -p1
%patch326 -p1
%patch327 -p1
%patch328 -p1
%patch329 -p1
%patch330 -p1
%patch331 -p1
%patch332 -p1
%patch333 -p1
%patch334 -p1
%patch335 -p1
%patch336 -p1
%patch337 -p1
%patch338 -p1
%patch339 -p1
%patch340 -p1
%patch341 -p1
%patch342 -p1
%patch343 -p1
%patch344 -p1
%patch345 -p1
%patch346 -p1
%patch347 -p1
%patch348 -p1
%patch349 -p1
%patch350 -p1
%patch351 -p1
%patch352 -p1
%patch353 -p1
%patch354 -p1
%patch355 -p1
%patch356 -p1
%patch357 -p1
%patch358 -p1
%patch359 -p1
%patch360 -p1
%patch361 -p1
%patch362 -p1
%patch363 -p1
%patch364 -p1
%patch365 -p1
%patch366 -p1
%patch367 -p1
%patch368 -p1
%patch369 -p1
%patch370 -p1
%patch371 -p1
%patch372 -p1
%patch373 -p1
%patch374 -p1
%patch375 -p1
%patch376 -p1
%patch377 -p1
%patch378 -p1
%patch379 -p1
%patch380 -p1
%patch381 -p1
%patch382 -p1
%patch383 -p1
%patch384 -p1
%patch385 -p1
%patch386 -p1
%patch387 -p1
%patch388 -p1
%patch389 -p1
%patch390 -p1
%patch391 -p1
%patch392 -p1
%patch393 -p1
%patch394 -p1
%patch395 -p1
%patch396 -p1
%patch397 -p1
%patch398 -p1
%patch399 -p1
%patch400 -p1
%patch401 -p1
%patch402 -p1
%patch403 -p1
%patch404 -p1
%patch405 -p1
%patch406 -p1
%patch407 -p1
%patch408 -p1
%patch409 -p1
%patch410 -p1
%patch411 -p1
%patch412 -p1
%patch413 -p1
%patch414 -p1
%patch415 -p1
%patch416 -p1
%patch417 -p1
%patch418 -p1
%patch419 -p1
%patch420 -p1
%patch421 -p1
%patch422 -p1
%patch423 -p1
%patch424 -p1
%patch425 -p1
%patch426 -p1
%patch427 -p1
%patch428 -p1
%patch429 -p1
%patch430 -p1
%patch431 -p1
%patch432 -p1
%patch433 -p1
%patch434 -p1
%patch435 -p1
%patch436 -p1
%patch437 -p1
%patch438 -p1
%patch439 -p1
%patch440 -p1
%patch441 -p1
%patch442 -p1
%patch443 -p1
%patch444 -p1
%patch445 -p1
%patch446 -p1
%patch447 -p1
%patch448 -p1
%patch449 -p1
%patch450 -p1
%patch451 -p1
%patch452 -p1
%patch453 -p1
%patch454 -p1
%patch455 -p1
%patch456 -p1
%patch457 -p1
%patch458 -p1
%patch459 -p1
%patch460 -p1
%patch461 -p1
%patch462 -p1
%patch463 -p1
%patch464 -p1
%patch465 -p1
%patch466 -p1
%patch467 -p1
%patch468 -p1
%patch469 -p1
%patch470 -p1
%patch471 -p1
%patch472 -p1
%patch473 -p1
%patch474 -p1
%patch475 -p1
%patch476 -p1
%patch477 -p1
%patch478 -p1
%patch479 -p1
%patch480 -p1
%patch481 -p1
#%patch482 -p1
%patch483 -p1
%patch484 -p1
%patch485 -p1
%patch486 -p1
%patch487 -p1
%patch488 -p1
%patch489 -p1
%patch490 -p1
%patch491 -p1
%patch492 -p1
%patch493 -p1
%patch494 -p1
%patch495 -p1
%patch496 -p1
%patch497 -p1
%patch498 -p1
%patch499 -p1
%patch500 -p1
%patch501 -p1
%patch502 -p1
%patch503 -p1
%patch504 -p1
%patch505 -p1
%patch506 -p1
%patch507 -p1
%patch508 -p1
%patch509 -p1
%patch510 -p1
%patch511 -p1
%patch512 -p1
%patch513 -p1
%patch514 -p1
%patch515 -p1
%patch516 -p1
%patch517 -p1
%patch518 -p1
%patch519 -p1
%patch520 -p1
%patch521 -p1
%patch522 -p1
%patch523 -p1
%patch524 -p1
%patch525 -p1
%patch526 -p1
%patch527 -p1
%patch528 -p1
%patch529 -p1
%patch530 -p1
%patch531 -p1
%patch532 -p1
%patch533 -p1
%patch534 -p1
%patch535 -p1
%patch536 -p1
%patch537 -p1
%patch538 -p1
%patch539 -p1
%patch540 -p1
%patch541 -p1
%patch542 -p1
%patch543 -p1
%patch544 -p1
%patch545 -p1
%patch546 -p1
%patch547 -p1
%patch548 -p1
%patch549 -p1
%patch550 -p1
%patch551 -p1
%patch552 -p1
%patch553 -p1
%patch554 -p1
%patch555 -p1
%patch556 -p1
%patch557 -p1
%patch558 -p1
%patch559 -p1
%patch560 -p1
%patch561 -p1
%patch562 -p1
%patch563 -p1
%patch564 -p1
%patch565 -p1
%patch566 -p1
%patch567 -p1
%patch568 -p1
%patch569 -p1
%patch570 -p1
%patch571 -p1
%patch572 -p1
%patch573 -p1
%patch574 -p1
%patch575 -p1
%patch576 -p1
%patch577 -p1
%patch578 -p1
%patch579 -p1
%patch580 -p1
%patch581 -p1
%patch582 -p1
%patch583 -p1
%patch584 -p1
%patch585 -p1
%patch586 -p1
%patch587 -p1
%patch588 -p1
%patch589 -p1
%patch590 -p1
%patch591 -p1
%patch592 -p1
%patch593 -p1
%patch594 -p1
%patch595 -p1
%patch596 -p1
%patch597 -p1
%patch598 -p1
%patch599 -p1
%patch600 -p1
%patch601 -p1
%patch602 -p1
%patch603 -p1
%patch604 -p1
%patch605 -p1
%patch606 -p1
%patch607 -p1
%patch608 -p1
%patch609 -p1
%patch610 -p1
%patch611 -p1
%patch612 -p1
%patch613 -p1
%patch614 -p1
%patch615 -p1
%patch616 -p1
%patch617 -p1
%patch618 -p1
%patch619 -p1
%patch620 -p1
%patch621 -p1
%patch622 -p1
%patch623 -p1
%patch624 -p1
%patch625 -p1
%patch626 -p1
%patch627 -p1
%patch628 -p1
%patch629 -p1
%patch630 -p1
%patch631 -p1
%patch632 -p1
%patch633 -p1
%patch634 -p1
%patch635 -p1
%patch636 -p1
%patch637 -p1
%patch638 -p1
%patch639 -p1
%patch640 -p1
%patch641 -p1
%patch642 -p1
%patch643 -p1
%patch644 -p1
%patch645 -p1
%patch646 -p1
%patch647 -p1
%patch648 -p1
%patch649 -p1
%patch650 -p1
%patch651 -p1
%patch652 -p1
%patch653 -p1
%patch654 -p1
%patch655 -p1
%patch656 -p1
%patch657 -p1
%patch658 -p1
%patch659 -p1
%patch660 -p1
%patch661 -p1
%patch662 -p1
%patch663 -p1
%patch664 -p1
%patch665 -p1
%patch666 -p1
%patch667 -p1
%patch668 -p1
%patch669 -p1
%patch670 -p1
%patch671 -p1
%patch672 -p1
%patch673 -p1
%patch674 -p1
%patch675 -p1
%patch676 -p1
%patch677 -p1
%patch678 -p1
%patch679 -p1
%patch680 -p1
%patch681 -p1
%patch682 -p1
%patch683 -p1
%patch684 -p1
%patch685 -p1
%patch686 -p1
%patch687 -p1
%patch688 -p1
%patch689 -p1
%patch690 -p1
%patch691 -p1
%patch692 -p1
%patch693 -p1
%patch694 -p1
%patch695 -p1
%patch696 -p1
%patch697 -p1
%patch698 -p1
%patch699 -p1
%patch700 -p1
%patch701 -p1
%patch702 -p1
%patch703 -p1
%patch704 -p1
%patch705 -p1
%patch706 -p1
%patch707 -p1
%patch708 -p1
%patch709 -p1
%patch710 -p1
%patch711 -p1
%patch712 -p1
%patch713 -p1
%patch714 -p1
%patch715 -p1
%patch716 -p1
%patch717 -p1
%patch718 -p1
%patch719 -p1
%patch720 -p1
%patch721 -p1
%patch722 -p1
%patch723 -p1
%patch724 -p1
%patch725 -p1
%patch726 -p1
%patch727 -p1
%patch728 -p1
%patch729 -p1
%patch730 -p1
%patch731 -p1
%patch732 -p1
%patch733 -p1
%patch734 -p1
%patch735 -p1
%patch736 -p1
%patch737 -p1
%patch738 -p1
%patch739 -p1
%patch740 -p1
%patch741 -p1
%patch742 -p1
%patch743 -p1
%patch744 -p1
%patch745 -p1
%patch746 -p1
%patch747 -p1
%patch748 -p1
%patch749 -p1
%patch750 -p1
%patch751 -p1
%patch752 -p1
%patch753 -p1
%patch754 -p1
%patch755 -p1
%patch756 -p1
%patch757 -p1
%patch758 -p1
%patch759 -p1
%patch760 -p1
%patch761 -p1
%patch762 -p1
%patch763 -p1
%patch764 -p1
%patch765 -p1
%patch766 -p1
%patch767 -p1
%patch768 -p1
%patch769 -p1
%patch770 -p1
%patch771 -p1
%patch772 -p1
%patch773 -p1
%patch774 -p1
%patch775 -p1
%patch776 -p1
%patch777 -p1
%patch778 -p1
%patch779 -p1
%patch780 -p1
%patch781 -p1
%patch782 -p1
%patch783 -p1
%patch784 -p1
%patch785 -p1
%patch786 -p1
%patch787 -p1
%patch788 -p1
%patch789 -p1
%patch790 -p1
%patch791 -p1
%patch792 -p1
%patch793 -p1
%patch794 -p1
%patch795 -p1
%patch796 -p1
%patch797 -p1
%patch798 -p1
%patch799 -p1
%patch800 -p1
%patch801 -p1
%patch802 -p1
%patch803 -p1
%patch804 -p1
%patch805 -p1
%patch806 -p1
%patch807 -p1
%patch808 -p1
%patch809 -p1
%patch810 -p1
%patch811 -p1
%patch812 -p1
%patch813 -p1
%patch814 -p1
%patch815 -p1
%patch816 -p1
%patch817 -p1
%patch818 -p1
%patch819 -p1
%patch820 -p1
%patch821 -p1
%patch822 -p1
%patch823 -p1
%patch824 -p1
%patch825 -p1
%patch826 -p1
%patch827 -p1
%patch828 -p1
%patch829 -p1
%patch830 -p1
%patch831 -p1
%patch832 -p1
%patch833 -p1
%patch834 -p1
%patch835 -p1
%patch836 -p1
%patch837 -p1
%patch838 -p1
%patch839 -p1
%patch840 -p1
%patch841 -p1
%patch842 -p1
%patch843 -p1
%patch844 -p1
%patch845 -p1
%patch846 -p1
%patch847 -p1
%patch848 -p1
%patch849 -p1
%patch850 -p1
%patch851 -p1
%patch852 -p1
%patch853 -p1
%patch854 -p1
%patch855 -p1
%patch856 -p1
%patch857 -p1
%patch858 -p1
%patch859 -p1
%patch860 -p1
%patch861 -p1
%patch862 -p1
%patch863 -p1
%patch864 -p1
%patch865 -p1
%patch866 -p1
%patch867 -p1
%patch868 -p1
%patch869 -p1
%patch870 -p1
%patch871 -p1
%patch872 -p1
%patch873 -p1
%patch874 -p1
%patch875 -p1
%patch876 -p1
%patch877 -p1
%patch878 -p1
%patch879 -p1
%patch880 -p1
%patch881 -p1
%patch882 -p1
%patch883 -p1
%patch884 -p1
%patch885 -p1
%patch886 -p1
%patch887 -p1
%patch888 -p1
%patch889 -p1
%patch890 -p1
%patch891 -p1
%patch892 -p1
%patch893 -p1
%patch894 -p1
%patch895 -p1
%patch896 -p1
%patch897 -p1
%patch898 -p1
%patch899 -p1
%patch900 -p1
%patch901 -p1
%patch902 -p1
%patch903 -p1
%patch904 -p1
%patch905 -p1
%patch906 -p1
%patch907 -p1
%patch908 -p1
%patch909 -p1
%patch910 -p1
%patch911 -p1
%patch912 -p1
%patch913 -p1
%patch914 -p1
%patch915 -p1
%patch916 -p1
%patch917 -p1
%patch918 -p1
%patch919 -p1
%patch920 -p1
%patch921 -p1
%patch922 -p1
%patch923 -p1
%patch924 -p1
%patch925 -p1
%patch926 -p1
%patch927 -p1
%patch928 -p1
%patch929 -p1
%patch930 -p1
%patch931 -p1
%patch932 -p1
%patch933 -p1
%patch934 -p1
%patch935 -p1
%patch936 -p1
%patch937 -p1
%patch938 -p1
%patch939 -p1
%patch940 -p1
%patch941 -p1
%patch942 -p1
%patch943 -p1
%patch944 -p1
%patch945 -p1
%patch946 -p1
%patch947 -p1
%patch948 -p1
%patch949 -p1
%patch950 -p1
%patch951 -p1
%patch952 -p1
%patch953 -p1
%patch954 -p1
%patch955 -p1
%patch956 -p1
%patch957 -p1
%patch958 -p1
%patch959 -p1
%patch960 -p1
%patch961 -p1
%patch962 -p1
%patch963 -p1
%patch964 -p1
%patch965 -p1
%patch966 -p1
%patch967 -p1
%patch968 -p1
%patch969 -p1
%patch970 -p1
%patch971 -p1
%patch972 -p1
%patch973 -p1
%patch974 -p1
%patch975 -p1
%patch976 -p1
%patch977 -p1
%patch978 -p1
%patch979 -p1
%patch980 -p1
%patch981 -p1
%patch982 -p1
%patch983 -p1
%patch984 -p1
%patch985 -p1
%patch986 -p1
%patch987 -p1
%patch988 -p1
%patch989 -p1
%patch990 -p1
%patch991 -p1
%patch992 -p1
%patch993 -p1
%patch994 -p1
%patch995 -p1
%patch996 -p1
%patch997 -p1
%patch998 -p1
%patch999 -p1
%patch1000 -p1
%patch1001 -p1
%patch1002 -p1
%patch1003 -p1
%patch1004 -p1
%patch1005 -p1
%patch1006 -p1
%patch1007 -p1
%patch1008 -p1
%patch1009 -p1
%patch1010 -p1
%patch1011 -p1
%patch1012 -p1
%patch1013 -p1
%patch1014 -p1
%patch1015 -p1
%patch1016 -p1
%patch1017 -p1
%patch1018 -p1
%patch1019 -p1
%patch1020 -p1
%patch1021 -p1
%patch1022 -p1
%patch1023 -p1
%patch1024 -p1
%patch1025 -p1
%patch1026 -p1
%patch1027 -p1
%patch1028 -p1
%patch1029 -p1
%patch1030 -p1
%patch1031 -p1
%patch1032 -p1
%patch1033 -p1
%patch1034 -p1
%patch1035 -p1
%patch1036 -p1
%patch1037 -p1
%patch1038 -p1
%patch1039 -p1
%patch1040 -p1
%patch1041 -p1
%patch1042 -p1
%patch1043 -p1
%patch1044 -p1
%patch1045 -p1
%patch1046 -p1
%patch1047 -p1
%patch1048 -p1
%patch1049 -p1
%patch1050 -p1
%patch1051 -p1
%patch1052 -p1
%patch1053 -p1
%patch1054 -p1
%patch1055 -p1
%patch1056 -p1
%patch1057 -p1
%patch1058 -p1
%patch1059 -p1
%patch1060 -p1
%patch1061 -p1
%patch1062 -p1
%patch1063 -p1
%patch1064 -p1
%patch1065 -p1
%patch1066 -p1
%patch1067 -p1
%patch1068 -p1
%patch1069 -p1
%patch1070 -p1
%patch1071 -p1
%patch1072 -p1
%patch1073 -p1
%patch1074 -p1
%patch1075 -p1
%patch1076 -p1
%patch1077 -p1
%patch1078 -p1
%patch1079 -p1
%patch1080 -p1
%patch1081 -p1
%patch1082 -p1
%patch1083 -p1
%patch1084 -p1
%patch1085 -p1
%patch1086 -p1
%patch1087 -p1
%patch1088 -p1
%patch1089 -p1
%patch1090 -p1
%patch1091 -p1
%patch1092 -p1
%patch1093 -p1
%patch1094 -p1
%patch1095 -p1
%patch1096 -p1
%patch1097 -p1
%patch1098 -p1
%patch1099 -p1
%patch1100 -p1
%patch1101 -p1
%patch1102 -p1
%patch1103 -p1
%patch1104 -p1
%patch1105 -p1
%patch1106 -p1
%patch1107 -p1
%patch1108 -p1
%patch1109 -p1
%patch1110 -p1
%patch1111 -p1
%patch1112 -p1
%patch1113 -p1
%patch1114 -p1
%patch1115 -p1
%patch1116 -p1
%patch1117 -p1
%patch1118 -p1
%patch1119 -p1
%patch1120 -p1
%patch1121 -p1
%patch1122 -p1
%patch1123 -p1
%patch1124 -p1
%patch1125 -p1
%patch1126 -p1
%patch1127 -p1
%patch1128 -p1
%patch1129 -p1
%patch1130 -p1
%patch1131 -p1
%patch1132 -p1
%patch1133 -p1
%patch1134 -p1
%patch1135 -p1
%patch1136 -p1
%patch1137 -p1
%patch1138 -p1
%patch1139 -p1
%patch1140 -p1
%patch1141 -p1
%patch1142 -p1
%patch1143 -p1
%patch1144 -p1
%patch1145 -p1
%patch1146 -p1
%patch1147 -p1
%patch1148 -p1
%patch1149 -p1
%patch1150 -p1
%patch1151 -p1
%patch1152 -p1
%patch1153 -p1
%patch1154 -p1
%patch1155 -p1
%patch1156 -p1
%patch1157 -p1
%patch1158 -p1
%patch1159 -p1
%patch1160 -p1
%patch1161 -p1
%patch1162 -p1
%patch1163 -p1
%patch1164 -p1
%patch1165 -p1
%patch1166 -p1
%patch1167 -p1
%patch1168 -p1
%patch1169 -p1
%patch1170 -p1
%patch1171 -p1
%patch1172 -p1
%patch1173 -p1
%patch1174 -p1
%patch1175 -p1
%patch1176 -p1
%patch1177 -p1
%patch1178 -p1
%patch1179 -p1
%patch1180 -p1
%patch1181 -p1
%patch1182 -p1
%patch1183 -p1
%patch1184 -p1
%patch1185 -p1
%patch1186 -p1
%patch1187 -p1
%patch1189 -p1
%patch1190 -p1
%patch1191 -p1
%patch1192 -p1
%patch1193 -p1
%patch1194 -p1
%patch1195 -p1
%patch1196 -p1
%patch1197 -p1
%patch1198 -p1
%patch1201 -p1
%patch1202 -p1
%patch1203 -p1
%patch1204 -p1
%patch1205 -p1
%patch1206 -p1
%patch1207 -p1
%patch1208 -p1
%patch1209 -p1
%patch1210 -p1
%patch1211 -p1
%patch1212 -p1
%patch1213 -p1
%patch1214 -p1
%patch1215 -p1
%patch1216 -p1
%patch1217 -p1
%patch1218 -p1
%patch1219 -p1
%patch1220 -p1
%patch1221 -p1
%patch1222 -p1
%patch1223 -p1
%patch1224 -p1
%patch1225 -p1
%patch1226 -p1
%patch1227 -p1
%patch1228 -p1
%patch1229 -p1
%patch1230 -p1
%patch1231 -p1
%patch1232 -p1
%patch1233 -p1
%patch1234 -p1
%patch1235 -p1
%patch1236 -p1
%patch1237 -p1
%patch1238 -p1
%patch1239 -p1
%patch1240 -p1
%patch1241 -p1
%patch1242 -p1
%patch1243 -p1
%patch1244 -p1
%patch1245 -p1
%patch1246 -p1
%patch1247 -p1
%patch1248 -p1
%patch1249 -p1
%patch1250 -p1
%patch1251 -p1
%patch1252 -p1
%patch1253 -p1
%patch1254 -p1
%patch1255 -p1
%patch1256 -p1
%patch1257 -p1
%patch1258 -p1
%patch1259 -p1
%patch1260 -p1
%patch1261 -p1
%patch1262 -p1
%patch1263 -p1
%patch1264 -p1
%patch1265 -p1
%patch1266 -p1
%patch1267 -p1
%patch1268 -p1
%patch1269 -p1
%patch1270 -p1
%patch1271 -p1
%patch1272 -p1
%patch1273 -p1
%patch1274 -p1
%patch1275 -p1
%patch1276 -p1
%patch1277 -p1
%patch1278 -p1
%patch1279 -p1
%patch1280 -p1
%patch1281 -p1
%patch1282 -p1
%patch1283 -p1
%patch1284 -p1
%patch1285 -p1
%patch1286 -p1
%patch1287 -p1
%patch1288 -p1
%patch1289 -p1
%patch1290 -p1
%patch1291 -p1
%patch1292 -p1
%patch1293 -p1
%patch1294 -p1
%patch1295 -p1
%patch1296 -p1
%patch1297 -p1
%patch1298 -p1
%patch1299 -p1
%patch1300 -p1
%patch1301 -p1
%patch1302 -p1
%patch1303 -p1
%patch1304 -p1
%patch1305 -p1
%patch1306 -p1
%patch1307 -p1
%patch1308 -p1
%patch1309 -p1
%patch1310 -p1
%patch1311 -p1
%patch1312 -p1
%patch1313 -p1
%patch1314 -p1
%patch1315 -p1
%patch1316 -p1
%patch1317 -p1
%patch1318 -p1
%patch1319 -p1
%patch1320 -p1
%patch1321 -p1
%patch1322 -p1
%patch1323 -p1
%patch1324 -p1
%patch1325 -p1
%patch1326 -p1
%patch1327 -p1
%patch1328 -p1
%patch1329 -p1
%patch1330 -p1
%patch1331 -p1
%patch1332 -p1
%patch1333 -p1
%patch1334 -p1
%patch1335 -p1
%patch1336 -p1
%patch1337 -p1
%patch1338 -p1
%patch1339 -p1
%patch1340 -p1
%patch1341 -p1
%patch1342 -p1
%patch1343 -p1
%patch1344 -p1
%patch1345 -p1
%patch1346 -p1
%patch1347 -p1
%patch1348 -p1
%patch1349 -p1
%patch1350 -p1
%patch1351 -p1
%patch1352 -p1
%patch1353 -p1
%patch1354 -p1
%patch1355 -p1
%patch1356 -p1
%patch1357 -p1
%patch1358 -p1
%patch1359 -p1
%patch1360 -p1
%patch1361 -p1
%patch1362 -p1
%patch1363 -p1
%patch1364 -p1
%patch1365 -p1
%patch1366 -p1
%patch1367 -p1
%patch1368 -p1
%patch1369 -p1
%patch1370 -p1
%patch1371 -p1
%patch1372 -p1
%patch1373 -p1
%patch1374 -p1
%patch1375 -p1
%patch1376 -p1
%patch1377 -p1
%patch1378 -p1
%patch1379 -p1
%patch1380 -p1
%patch1381 -p1
%patch1382 -p1
%patch1383 -p1
%patch1384 -p1
%patch1385 -p1
%patch1386 -p1
%patch1387 -p1
%patch1388 -p1
%patch1389 -p1
%patch1390 -p1
%patch1391 -p1
%patch1392 -p1
%patch1393 -p1
%patch1394 -p1
%patch1395 -p1
%patch1396 -p1
%patch1397 -p1
%patch1398 -p1
%patch1399 -p1
%patch1400 -p1
%patch1401 -p1
%patch1402 -p1
%patch1403 -p1
%patch1404 -p1
%patch1405 -p1
%patch1406 -p1
%patch1407 -p1
%patch1408 -p1
%patch1409 -p1
%patch1410 -p1
%patch1411 -p1
%patch1412 -p1
%patch1413 -p1
%patch1414 -p1
%patch1415 -p1
%patch1416 -p1
%patch1417 -p1
%patch1418 -p1
%patch1419 -p1
%patch1420 -p1
%patch1421 -p1
%patch1422 -p1
%patch1423 -p1
%patch1424 -p1
%patch1425 -p1
%patch1426 -p1
%patch1427 -p1
%patch1428 -p1
%patch1429 -p1
%patch1430 -p1
%patch1431 -p1
%patch1432 -p1
%patch1433 -p1
%patch1434 -p1
%patch1435 -p1
%patch1436 -p1
%patch1437 -p1
%patch1438 -p1
%patch1439 -p1
%patch1440 -p1
%patch1441 -p1
%patch1442 -p1
%patch1443 -p1
%patch1444 -p1
%patch1445 -p1
%patch1446 -p1
%patch1447 -p1
%patch1448 -p1
%patch1449 -p1
%patch1450 -p1
%patch1451 -p1
%patch1452 -p1
%patch1453 -p1
%patch1454 -p1
%patch1455 -p1
%patch1456 -p1
%patch1457 -p1
%patch1458 -p1
%patch1459 -p1
%patch1460 -p1
%patch1461 -p1
%patch1462 -p1
%patch1463 -p1
%patch1464 -p1
%patch1465 -p1
%patch1466 -p1
%patch1467 -p1
%patch1468 -p1
%patch1469 -p1
%patch1470 -p1
%patch1471 -p1
%patch1472 -p1
%patch1473 -p1
%patch1474 -p1
%patch1475 -p1
%patch1476 -p1
%patch1477 -p1
%patch1478 -p1
%patch1479 -p1
%patch1480 -p1
%patch1481 -p1
%patch1482 -p1
%patch1483 -p1
%patch1484 -p1
%patch1485 -p1
%patch1486 -p1
%patch1487 -p1
%patch1488 -p1
%patch1489 -p1
%patch1490 -p1
%patch1491 -p1
%patch1492 -p1
%patch1493 -p1
%patch1494 -p1
%patch1495 -p1
%patch1496 -p1
%patch1497 -p1
%patch1498 -p1
%patch1499 -p1
%patch1500 -p1
%patch1501 -p1
%patch1502 -p1
%patch1503 -p1
%patch1504 -p1
%patch1505 -p1
%patch1506 -p1
%patch1507 -p1
%patch1508 -p1
%patch1509 -p1
%patch1510 -p1
%patch1511 -p1
%patch1512 -p1
%patch1513 -p1
%patch1514 -p1
%patch1515 -p1
%patch1516 -p1
%patch1517 -p1
%patch1518 -p1
%patch1519 -p1
%patch1520 -p1
%patch1521 -p1
%patch1522 -p1
%patch1523 -p1
%patch1524 -p1
%patch1525 -p1
%patch1526 -p1
%patch1527 -p1
%patch1528 -p1
%patch1529 -p1
%patch1530 -p1
%patch1531 -p1
%patch1532 -p1
%patch1533 -p1
%patch1534 -p1
%patch1535 -p1
%patch1536 -p1
%patch1537 -p1
%patch1538 -p1
%patch1539 -p1
%patch1540 -p1
%patch1541 -p1
%patch1542 -p1
%patch1543 -p1
%patch1544 -p1
%patch1545 -p1
%patch1546 -p1
%patch1547 -p1
%patch1548 -p1
%patch1549 -p1
%patch1550 -p1
%patch1551 -p1
%patch1552 -p1
%patch1553 -p1
%patch1554 -p1
%patch1555 -p1
%patch1556 -p1
%patch1557 -p1
%patch1558 -p1
%patch1559 -p1
%patch1560 -p1
%patch1561 -p1
%patch1562 -p1
%patch1563 -p1
%patch1564 -p1
%patch1565 -p1
%patch1566 -p1
%patch1567 -p1
%patch1568 -p1
%patch1569 -p1
%patch1570 -p1
%patch1571 -p1
%patch1572 -p1
%patch1573 -p1
%patch1574 -p1
%patch1575 -p1
%patch1576 -p1
%patch1577 -p1
%patch1578 -p1
%patch1579 -p1
%patch1580 -p1
%patch1581 -p1
%patch1582 -p1
%patch1583 -p1
%patch1584 -p1
%patch1585 -p1
%patch1586 -p1
%patch1587 -p1
%patch1588 -p1
%patch1589 -p1
%patch1590 -p1
%patch1591 -p1
%patch1592 -p1
%patch1593 -p1
%patch1594 -p1
%patch1595 -p1
%patch1596 -p1
%patch1597 -p1
%patch1598 -p1
%patch1599 -p1
%patch1600 -p1
%patch1601 -p1
%patch1602 -p1
%patch1603 -p1
%patch1604 -p1
%patch1605 -p1
%patch1606 -p1
%patch1607 -p1
%patch1608 -p1
%patch1609 -p1
%patch1610 -p1
%patch1611 -p1
%patch1612 -p1
%patch1613 -p1
%patch1614 -p1
%patch1615 -p1
%patch1616 -p1
%patch1617 -p1
%patch1618 -p1
%patch1619 -p1
%patch1620 -p1
%patch1621 -p1
%patch1622 -p1
%patch1623 -p1
%patch1624 -p1
%patch1625 -p1
%patch1626 -p1
%patch1627 -p1
%patch1628 -p1
%patch1629 -p1
%patch1630 -p1
%patch1631 -p1
%patch1632 -p1
%patch1633 -p1
%patch1634 -p1
%patch1635 -p1
%patch1636 -p1
%patch1637 -p1
%patch1638 -p1
%patch1639 -p1
%patch1640 -p1
%patch1641 -p1
%patch1642 -p1
%patch1643 -p1
%patch1644 -p1
%patch1645 -p1
%patch1646 -p1
%patch1647 -p1
%patch1648 -p1
%patch1649 -p1
%patch1650 -p1
%patch1651 -p1
%patch1652 -p1
%patch1653 -p1
%patch1654 -p1
%patch1655 -p1
%patch1656 -p1
%patch1657 -p1
%patch1658 -p1
%patch1659 -p1
%patch1660 -p1
%patch1661 -p1
%patch1662 -p1
%patch1663 -p1
%patch1664 -p1
%patch1665 -p1
%patch1666 -p1
%patch1667 -p1
%patch1668 -p1
%patch1669 -p1
%patch1670 -p1
%patch1671 -p1
%patch1672 -p1
%patch1673 -p1
%patch1674 -p1
%patch1675 -p1
%patch1676 -p1
%patch1677 -p1
%patch1678 -p1
%patch1679 -p1
%patch1680 -p1
%patch1681 -p1
%patch1682 -p1
%patch1683 -p1
%patch1684 -p1
%patch1685 -p1
%patch1686 -p1
%patch1687 -p1
%patch1688 -p1
%patch1689 -p1
%patch1690 -p1
%patch1691 -p1
%patch1692 -p1
%patch1693 -p1
%patch1694 -p1
%patch1695 -p1
%patch1696 -p1
%patch1697 -p1
%patch1698 -p1
%patch1699 -p1
%patch1700 -p1
%patch1701 -p1
%patch1702 -p1
%patch1703 -p1
%patch1704 -p1
%patch1705 -p1
%patch1706 -p1
%patch1707 -p1
%patch1708 -p1
%patch1709 -p1
%patch1710 -p1
%patch1711 -p1
%patch1712 -p1
%patch1713 -p1
%patch1714 -p1
%patch1715 -p1
%patch1716 -p1
%patch1717 -p1
%patch1718 -p1
%patch1719 -p1
%patch1720 -p1
%patch1721 -p1
%patch1722 -p1
%patch1723 -p1
%patch1724 -p1
%patch1725 -p1
%patch1726 -p1
%patch1727 -p1
%patch1728 -p1
%patch1729 -p1
%patch1730 -p1
%patch1731 -p1
%patch1732 -p1
%patch1733 -p1
%patch1734 -p1
%patch1735 -p1
%patch1736 -p1
%patch1737 -p1
%patch1738 -p1
%patch1739 -p1
%patch1740 -p1
%patch1741 -p1
%patch1742 -p1
%patch1743 -p1
%patch1744 -p1
%patch1745 -p1
%patch1746 -p1
%patch1747 -p1
%patch1748 -p1
%patch1749 -p1
%patch1750 -p1
%patch1751 -p1
%patch1752 -p1
%patch1753 -p1
%patch1754 -p1
%patch1755 -p1
%patch1756 -p1
%patch1757 -p1
%patch1758 -p1
%patch1759 -p1
%patch1760 -p1
%patch1761 -p1
%patch1762 -p1
%patch1763 -p1
%patch1764 -p1
%patch1765 -p1
%patch1766 -p1
%patch1767 -p1
%patch1768 -p1
%patch1769 -p1
%patch1770 -p1
%patch1771 -p1
%patch1772 -p1
%patch1773 -p1
%patch1774 -p1
%patch1775 -p1
%patch1776 -p1
%patch1777 -p1
%patch1778 -p1
%patch1779 -p1
%patch1780 -p1
%patch1781 -p1
%patch1782 -p1
%patch1783 -p1
%patch1784 -p1
%patch1785 -p1
%patch1786 -p1
%patch1787 -p1
%patch1788 -p1
%patch1789 -p1
%patch1790 -p1
%patch1791 -p1
%patch1792 -p1
%patch1793 -p1
%patch1794 -p1
%patch1795 -p1
%patch1796 -p1
%patch1797 -p1
%patch1798 -p1
%patch1799 -p1
%patch1800 -p1
%patch1801 -p1
%patch1802 -p1
%patch1803 -p1
%patch1804 -p1
%patch1805 -p1
%patch1806 -p1
%patch1807 -p1
%patch1808 -p1
%patch1809 -p1
%patch1810 -p1
%patch1811 -p1
%patch1812 -p1
%patch1813 -p1
%patch1814 -p1
%patch1815 -p1
%patch1816 -p1
%patch1817 -p1
%patch1818 -p1
%patch1819 -p1
%patch1820 -p1
%patch1821 -p1
%patch1822 -p1
%patch1823 -p1
%patch1824 -p1
%patch1825 -p1
%patch1826 -p1
%patch1827 -p1
%patch1828 -p1
%patch1829 -p1
%patch1830 -p1
%patch1831 -p1
%patch1832 -p1
%patch1833 -p1
%patch1834 -p1
%patch1835 -p1
%patch1836 -p1
%patch1837 -p1
%patch1838 -p1
%patch1839 -p1
%patch1840 -p1
%patch1841 -p1
%patch1842 -p1
%patch1843 -p1
%patch1844 -p1
%patch1845 -p1
%patch1846 -p1
%patch1847 -p1
%patch1848 -p1
%patch1849 -p1
%patch1850 -p1
%patch1851 -p1
%patch1852 -p1
%patch1853 -p1
%patch1854 -p1
%patch1855 -p1
%patch1856 -p1
%patch1857 -p1
%patch1858 -p1
%patch1859 -p1
%patch1860 -p1
%patch1861 -p1
%patch1862 -p1
%patch1863 -p1
%patch1864 -p1
%patch1865 -p1
%patch1866 -p1
%patch1867 -p1
%patch1868 -p1
%patch1869 -p1
%patch1870 -p1
%patch1871 -p1
%patch1872 -p1
%patch1873 -p1
%patch1874 -p1
%patch1875 -p1
%patch1876 -p1
%patch1877 -p1
%patch1878 -p1
%patch1879 -p1
%patch1880 -p1
%patch1881 -p1
%patch1882 -p1
%patch1883 -p1
%patch1884 -p1
%patch1885 -p1
%patch1886 -p1
%patch1887 -p1
%patch1888 -p1
%patch1889 -p1
%patch1890 -p1
%patch1891 -p1
%patch1892 -p1
%patch1893 -p1
%patch1894 -p1
%patch1895 -p1
%patch1896 -p1
%patch1897 -p1
%patch1898 -p1
%patch1899 -p1
%patch1900 -p1
%patch1901 -p1
%patch1902 -p1
%patch1903 -p1
%patch1904 -p1
%patch1905 -p1
%patch1906 -p1
%patch1907 -p1
%patch1908 -p1
%patch1909 -p1
%patch1910 -p1

%build
buildarch="%{kvm_target}-softmmu"

# --build-id option is used for giving info to the debug packages.
extraldflags="-Wl,--build-id";
buildldflags="VL_LDFLAGS=-Wl,--build-id"

# QEMU already knows how to set _FORTIFY_SOURCE
%global optflags %(echo %{optflags} | sed 's/-Wp,-D_FORTIFY_SOURCE=2//')

%ifarch s390
    # drop -g flag to prevent memory exhaustion by linker
    %global optflags %(echo %{optflags} | sed 's/-g//')
    sed -i.debug 's/"-g $CFLAGS"/"$CFLAGS"/g' configure
%endif

dobuild() {
%if 0%{!?build_only_sub:1}
    ./configure \
        --prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --sysconfdir=%{_sysconfdir} \
        --interp-prefix=%{_prefix}/qemu-%%M \
        --audio-drv-list=pa,alsa \
        --with-confsuffix=/%{pkgname} \
        --localstatedir=%{_localstatedir} \
        --libexecdir=%{_libexecdir} \
        --with-pkgversion=%{pkgname}-%{version}-%{release} \
        --disable-strip \
        --disable-qom-cast-debug \
        --extra-ldflags="$extraldflags -pie -Wl,-z,relro -Wl,-z,now" \
        --extra-cflags="%{optflags} -fPIE -DPIE" \
        --enable-trace-backend=dtrace \
        --enable-werror \
        --disable-xen \
        --disable-virtfs \
        --enable-kvm \
        --enable-libusb \
        --enable-spice \
        --enable-seccomp \
        --disable-fdt \
        --enable-docs \
        --disable-sdl \
        --disable-debug-tcg \
        --disable-sparse \
        --disable-brlapi \
        --disable-bluez \
        --disable-vde \
        --disable-curses \
        --enable-curl \
        --enable-libssh2 \
        --enable-vnc-tls \
        --enable-vnc-sasl \
        --enable-linux-aio \
        --enable-smartcard-nss \
        --enable-lzo \
        --enable-snappy \
        --enable-usb-redir \
        --enable-vnc-png \
        --disable-vnc-jpeg \
        --enable-vnc-ws \
        --enable-uuid \
        --disable-vhost-scsi \
%if %{with guest_agent}
        --enable-guest-agent \
%else
        --disable-guest-agent \
%endif
%if %{rhev}
        --enable-live-block-ops \
%else
        --disable-live-block-ops \
%endif
        --disable-live-block-migration \
%ifarch x86_64
        --enable-rbd \
%endif
        --enable-glusterfs \
%if 0%{?have_tcmalloc:1}
        --enable-tcmalloc \
%endif
        --block-drv-rw-whitelist=qcow2,raw,file,host_device,blkdebug,nbd,iscsi,gluster,rbd \
        --block-drv-ro-whitelist=vmdk,vhdx,vpc,ssh,https \
        --iasl=/bin/false \
        "$@"

    echo "config-host.mak contents:"
    echo "==="
    cat config-host.mak
    echo "==="

    make V=1 %{?_smp_mflags} $buildldflags
%else
   ./configure --prefix=%{_prefix} \
               --libdir=%{_libdir} \
               --with-pkgversion=%{pkgname}-%{version}-%{release} \
               --disable-guest-agent \
               "$@"

   make qemu-img %{?_smp_mflags} $buildldflags
   make qemu-io %{?_smp_mflags} $buildldflags
   make qemu-nbd %{?_smp_mflags} $buildldflags
   make qemu-img.1 %{?_smp_mflags} $buildldflags
   make qemu-nbd.8 %{?_smp_mflags} $buildldflags
   %if %{with guest_agent}
      make qemu-ga %{?_smp_mflags} $buildldflags
   %endif
%endif
}

dobuild --target-list="$buildarch"

%if 0%{!?build_only_sub:1}
        # Setup back compat qemu-kvm binary
        ./scripts/tracetool.py --backend dtrace --format stap \
          --binary %{_libexecdir}/qemu-kvm --target-arch %{kvm_target} \
          --target-type system --probe-prefix \
          qemu.kvm < ./trace-events > qemu-kvm.stp

        ./scripts/tracetool.py --backend dtrace --format simpletrace-stap \
          --binary %{_libexecdir}/qemu-kvm --target-arch %{kvm_target} \
          --target-type system --probe-prefix \
          qemu.kvm < ./trace-events > qemu-kvm-simpletrace.stp

        cp -a %{kvm_target}-softmmu/qemu-system-%{kvm_target} qemu-kvm


    gcc %{SOURCE6} -O2 -g -o ksmctl
%endif

%install
%define _udevdir %(pkg-config --variable=udevdir udev)/rules.d

%if 0%{!?build_only_sub:1}
    install -D -p -m 0644 %{SOURCE4} $RPM_BUILD_ROOT%{_unitdir}/ksm.service
    install -D -p -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/ksm
    install -D -p -m 0755 ksmctl $RPM_BUILD_ROOT%{_libexecdir}/ksmctl

    install -D -p -m 0644 %{SOURCE7} $RPM_BUILD_ROOT%{_unitdir}/ksmtuned.service
    install -D -p -m 0755 %{SOURCE8} $RPM_BUILD_ROOT%{_sbindir}/ksmtuned
    install -D -p -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/ksmtuned.conf

    mkdir -p $RPM_BUILD_ROOT%{_bindir}/
    mkdir -p $RPM_BUILD_ROOT%{_udevdir}
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{pkgname}

    install -m 0755 scripts/kvm/kvm_stat $RPM_BUILD_ROOT%{_bindir}/
    install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_udevdir}
    install -m 0644 scripts/dump-guest-memory.py \
                    $RPM_BUILD_ROOT%{_datadir}/%{pkgname}

    make DESTDIR=$RPM_BUILD_ROOT \
        sharedir="%{_datadir}/%{pkgname}" \
        datadir="%{_datadir}/%{pkgname}" \
        install

    mkdir -p $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset

    # Install compatibility roms
    install %{SOURCE14} $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/
    install %{SOURCE15} $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/
    install %{SOURCE16} $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/
    install %{SOURCE17} $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/
    install %{SOURCE20} $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/

    install -m 0755 qemu-kvm $RPM_BUILD_ROOT%{_libexecdir}/
    install -m 0644 qemu-kvm.stp $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/
    install -m 0644 qemu-kvm-simpletrace.stp $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/

    rm $RPM_BUILD_ROOT%{_bindir}/qemu-system-%{kvm_target}
    rm $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/qemu-system-%{kvm_target}.stp
    rm $RPM_BUILD_ROOT%{_datadir}/systemtap/tapset/qemu-system-%{kvm_target}-simpletrace.stp

    # Install simpletrace
    install -m 0755 scripts/simpletrace.py $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/simpletrace.py
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/tracetool
    install -m 0644 -t $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/tracetool scripts/tracetool/*.py
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/tracetool/backend
    install -m 0644 -t $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/tracetool/backend scripts/tracetool/backend/*.py
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/tracetool/format
    install -m 0644 -t $RPM_BUILD_ROOT%{_datadir}/%{pkgname}/tracetool/format scripts/tracetool/format/*.py

    mkdir -p $RPM_BUILD_ROOT%{qemudocdir}
    install -p -m 0644 -t ${RPM_BUILD_ROOT}%{qemudocdir} Changelog README README.systemtap COPYING COPYING.LIB LICENSE %{SOURCE19} QMP/qmp-spec.txt QMP/qmp-events.txt
    mv ${RPM_BUILD_ROOT}%{_docdir}/qemu/qemu-doc.html $RPM_BUILD_ROOT%{qemudocdir}
    mv ${RPM_BUILD_ROOT}%{_docdir}/qemu/qemu-tech.html $RPM_BUILD_ROOT%{qemudocdir}
    mv ${RPM_BUILD_ROOT}%{_docdir}/qemu/qmp-commands.txt $RPM_BUILD_ROOT%{qemudocdir}
    chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
    chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man8/*

    install -D -p -m 0644 qemu.sasl $RPM_BUILD_ROOT%{_sysconfdir}/sasl2/qemu-kvm.conf

    # Provided by package openbios
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/openbios-ppc
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/openbios-sparc32
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/openbios-sparc64
    # Provided by package SLOF
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/slof.bin

    # Remove unpackaged files.
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/palcode-clipper
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/petalogix*.dtb
    rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/bamboo.dtb
    rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/ppc_rom.bin
    rm -f ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/spapr-rtas.bin
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/s390-zipl.rom
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/s390-ccw.img

    # Remove efi roms
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/efi*.rom

    # Provided by package ipxe
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/pxe*rom
    # Provided by package vgabios
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/vgabios*bin
    # Provided by package seabios
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/bios*.bin
    # Provided by package sgabios
    rm -rf ${RPM_BUILD_ROOT}%{_datadir}/%{pkgname}/sgabios.bin

    # the pxe gpxe images will be symlinks to the images on
    # /usr/share/ipxe, as QEMU doesn't know how to look
    # for other paths, yet.
    pxe_link() {
        ln -s ../ipxe/$2.rom %{buildroot}%{_datadir}/%{pkgname}/pxe-$1.rom
    }

    pxe_link e1000 8086100e
    pxe_link ne2k_pci 10ec8029
    pxe_link pcnet 10222000
    pxe_link rtl8139 10ec8139
    pxe_link virtio 1af41000

    rom_link() {
        ln -s $1 %{buildroot}%{_datadir}/%{pkgname}/$2
    }

    rom_link ../seavgabios/vgabios-isavga.bin vgabios.bin
    rom_link ../seavgabios/vgabios-cirrus.bin vgabios-cirrus.bin
    rom_link ../seavgabios/vgabios-qxl.bin vgabios-qxl.bin
    rom_link ../seavgabios/vgabios-stdvga.bin vgabios-stdvga.bin
    rom_link ../seavgabios/vgabios-vmware.bin vgabios-vmware.bin
    rom_link ../seabios/bios.bin bios.bin
    rom_link ../seabios/bios-256k.bin bios-256k.bin
    rom_link ../sgabios/sgabios.bin sgabios.bin
%endif

# Remove libcacard
rm -rf $RPM_BUILD_ROOT%{_bindir}/vscclient
rm -rf $RPM_BUILD_ROOT%{_includedir}/cacard
rm -rf $RPM_BUILD_ROOT%{_libdir}/libcacard.so*
rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libcacard.pc

%if %{with guest_agent}
    # For the qemu-guest-agent subpackage, install:
    # - the systemd service file and the udev rules:
    mkdir -p $RPM_BUILD_ROOT%{_unitdir}
    mkdir -p $RPM_BUILD_ROOT%{_udevdir}
    install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_unitdir}
    install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{_udevdir}

    # - the environment file for the systemd service:
    install -D -p -m 0644 %{SOURCE13} \
      $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/qemu-ga

    # - the fsfreeze hook script:
    install -D --preserve-timestamps \
      scripts/qemu-guest-agent/fsfreeze-hook \
      $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ga/fsfreeze-hook

    # - the directory for user scripts:
    mkdir $RPM_BUILD_ROOT%{_sysconfdir}/qemu-ga/fsfreeze-hook.d

    # - and the fsfreeze script samples:
    mkdir --parents $RPM_BUILD_ROOT%{_datadir}/%{name}/qemu-ga/fsfreeze-hook.d/
    install --preserve-timestamps --mode=0644 \
      scripts/qemu-guest-agent/fsfreeze-hook.d/*.sample \
      $RPM_BUILD_ROOT%{_datadir}/%{name}/qemu-ga/fsfreeze-hook.d/

    # - Install dedicated log directory:
    mkdir -p -v $RPM_BUILD_ROOT%{_localstatedir}/log/qemu-ga/
%endif

%if 0%{!?build_only_sub:1}
    # Install rules to use the bridge helper with libvirt's virbr0
    install -m 0644 %{SOURCE12} $RPM_BUILD_ROOT%{_sysconfdir}/%{pkgname}
%endif


find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f

%if 0%{?build_only_sub}
    mkdir -p $RPM_BUILD_ROOT%{_bindir}
    mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/*
    mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8/*
    install -m 0755 qemu-img $RPM_BUILD_ROOT%{_bindir}/qemu-img
    install -m 0755 qemu-io $RPM_BUILD_ROOT%{_bindir}/qemu-io
    install -m 0755 qemu-nbd $RPM_BUILD_ROOT%{_bindir}/qemu-nbd
    install -c -m 0644 qemu-img.1 ${RPM_BUILD_ROOT}%{_mandir}/man1/qemu-img.1
    install -c -m 0644 qemu-nbd.8 ${RPM_BUILD_ROOT}%{_mandir}/man8/qemu-nbd.8
    %if %{with guest_agent}
        install -c -m 0755  qemu-ga ${RPM_BUILD_ROOT}%{_bindir}/qemu-ga
    %endif
    chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man1/*
    chmod -x ${RPM_BUILD_ROOT}%{_mandir}/man8/*
%endif


%if 0%{!?build_only_sub:1}
%check
    make check
%endif
%post
# load kvm modules now, so we can make sure no reboot is needed.
# If there's already a kvm module installed, we don't mess with it
%udev_rules_update
sh %{_sysconfdir}/sysconfig/modules/kvm.modules &> /dev/null || :
    udevadm trigger --subsystem-match=misc --sysname-match=kvm --action=add || :

%if 0%{!?build_only_sub:1}
%post -n qemu-kvm-common%{?pkgsuffix}
    %systemd_post ksm.service
    %systemd_post ksmtuned.service

    getent group kvm >/dev/null || groupadd -g 36 -r kvm
    getent group qemu >/dev/null || groupadd -g 107 -r qemu
    getent passwd qemu >/dev/null || \
       useradd -r -u 107 -g qemu -G kvm -d / -s /sbin/nologin \
       -c "qemu user" qemu

%preun -n qemu-kvm-common%{?pkgsuffix}
    %systemd_preun ksm.service
    %systemd_preun ksmtuned.service

%postun -n qemu-kvm-common%{?pkgsuffix}
    %systemd_postun_with_restart ksm.service
    %systemd_postun_with_restart ksmtuned.service
%endif

%global kvm_files \
%{_udevdir}/80-kvm.rules

%global qemu_kvm_files \
%{_libexecdir}/qemu-kvm \
%{_datadir}/systemtap/tapset/qemu-kvm.stp \
%{_datadir}/systemtap/tapset/qemu-kvm-simpletrace.stp \
%{_datadir}/%{pkgname}/trace-events \
%{_datadir}/%{pkgname}/systemtap/script.d/qemu_kvm.stp \
%{_datadir}/%{pkgname}/systemtap/conf.d/qemu_kvm.conf

%if 0%{!?build_only_sub:1}
%files -n qemu-kvm-common%{?pkgsuffix}
    %defattr(-,root,root)
    %dir %{qemudocdir}
    %doc %{qemudocdir}/Changelog
    %doc %{qemudocdir}/README
    %doc %{qemudocdir}/qemu-doc.html
    %doc %{qemudocdir}/qemu-tech.html
    %doc %{qemudocdir}/qmp-commands.txt
    %doc %{qemudocdir}/COPYING
    %doc %{qemudocdir}/COPYING.LIB
    %doc %{qemudocdir}/LICENSE
    %doc %{qemudocdir}/README.rhel6-gpxe-source
    %doc %{qemudocdir}/README.systemtap
    %doc %{qemudocdir}/qmp-spec.txt
    %doc %{qemudocdir}/qmp-events.txt
    %dir %{_datadir}/%{pkgname}/
    %{_datadir}/%{pkgname}/keymaps/
    %{_mandir}/man1/%{pkgname}.1*
    %attr(4755, -, -) %{_libexecdir}/qemu-bridge-helper
    %config(noreplace) %{_sysconfdir}/sasl2/%{pkgname}.conf
    %{_unitdir}/ksm.service
    %{_libexecdir}/ksmctl
    %config(noreplace) %{_sysconfdir}/sysconfig/ksm
    %{_unitdir}/ksmtuned.service
    %{_sbindir}/ksmtuned
    %config(noreplace) %{_sysconfdir}/ksmtuned.conf
    %dir %{_sysconfdir}/%{pkgname}
    %config(noreplace) %{_sysconfdir}/%{pkgname}/bridge.conf
    %{_datadir}/%{pkgname}/simpletrace.py*
    %{_datadir}/%{pkgname}/tracetool/*.py*
    %{_datadir}/%{pkgname}/tracetool/backend/*.py*
    %{_datadir}/%{pkgname}/tracetool/format/*.py*
%endif

%if %{with guest_agent}
%files -n qemu-guest-agent
    %defattr(-,root,root,-)
    %doc COPYING README
    %{_bindir}/qemu-ga
    %{_unitdir}/qemu-guest-agent.service
    %{_udevdir}/99-qemu-guest-agent.rules
    %{_sysconfdir}/sysconfig/qemu-ga
    %{_sysconfdir}/qemu-ga
    %{_datadir}/%{name}/qemu-ga
    %dir %{_localstatedir}/log/qemu-ga
%endif

%if 0%{!?build_only_sub:1}
%files
    %defattr(-,root,root)
    %{_datadir}/%{pkgname}/acpi-dsdt.aml
    %{_datadir}/%{pkgname}/q35-acpi-dsdt.aml
    %{_datadir}/%{pkgname}/bios.bin
    %{_datadir}/%{pkgname}/bios-256k.bin
    %{_datadir}/%{pkgname}/sgabios.bin
    %{_datadir}/%{pkgname}/linuxboot.bin
    %{_datadir}/%{pkgname}/multiboot.bin
    %{_datadir}/%{pkgname}/kvmvapic.bin
    %{_datadir}/%{pkgname}/vgabios.bin
    %{_datadir}/%{pkgname}/vgabios-cirrus.bin
    %{_datadir}/%{pkgname}/vgabios-qxl.bin
    %{_datadir}/%{pkgname}/vgabios-stdvga.bin
    %{_datadir}/%{pkgname}/vgabios-vmware.bin
    %{_datadir}/%{pkgname}/pxe-e1000.rom
    %{_datadir}/%{pkgname}/pxe-virtio.rom
    %{_datadir}/%{pkgname}/pxe-pcnet.rom
    %{_datadir}/%{pkgname}/pxe-rtl8139.rom
    %{_datadir}/%{pkgname}/pxe-ne2k_pci.rom
    %{_datadir}/%{pkgname}/qemu-icon.bmp
    %{_datadir}/%{pkgname}/rhel6-virtio.rom
    %{_datadir}/%{pkgname}/rhel6-pcnet.rom
    %{_datadir}/%{pkgname}/rhel6-rtl8139.rom
    %{_datadir}/%{pkgname}/rhel6-ne2k_pci.rom
    %{_datadir}/%{pkgname}/rhel6-e1000.rom
    %{_datadir}/%{pkgname}/dump-guest-memory.py*
    %config(noreplace) %{_sysconfdir}/%{pkgname}/target-x86_64.conf
    %{?kvm_files:}
    %{?qemu_kvm_files:}

%files -n qemu-kvm-tools%{?pkgsuffix}
    %defattr(-,root,root,-)
    %{_bindir}/kvm_stat
%endif

%files -n qemu-img%{?pkgsuffix}
%defattr(-,root,root)
%{_bindir}/qemu-img
%{_bindir}/qemu-io
%{_bindir}/qemu-nbd
%{_mandir}/man1/qemu-img.1*
%{_mandir}/man8/qemu-nbd.8*

%changelog
* Wed Jun 27 2018 Fabian Arrotin <arrfab@centos.org> - 1.5.3-156.el7_5.3
- Added kvm_target arm (Jacco@redsleeve.org)

* Fri Jun 08 2018 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-156.el7_5.3
- kvm-i386-Define-the-Virt-SSBD-MSR-and-handling-of-it-CVE.patch [bz#1584363]
- kvm-i386-define-the-AMD-virt-ssbd-CPUID-feature-bit-CVE-.patch [bz#1584363]
- Resolves: bz#1584363
  (CVE-2018-3639 qemu-kvm: hw: cpu: AMD: speculative store bypass [rhel-7.5.z])

* Fri May 11 2018 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-156.el7_5.2
- kvm-i386-define-the-ssbd-CPUID-feature-bit-CVE-2018-3639.patch [bz#1574075]
- Resolves: bz#1574075
  (EMBARGOED CVE-2018-3639 qemu-kvm: Kernel: omega-4 [rhel-7.5.z])

* Mon Apr 16 2018 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-156.el7_5.1
- kvm-vga-add-ram_addr_t-cast.patch [bz#1567913]
- kvm-vga-fix-region-calculation.patch [bz#1567913]
- Resolves: bz#1567913
  (CVE-2018-7858 qemu-kvm: Qemu: cirrus: OOB access when updating vga display [rhel-7] [rhel-7.5.z])

* Tue Feb 20 2018 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-156.el7
- kvm-vnc-Fix-qemu-crashed-when-vnc-client-disconnect-sudd.patch [bz#1527405]
- kvm-fix-full-frame-updates-for-VNC-clients.patch [bz#1527405]
- kvm-vnc-update-fix.patch [bz#1527405]
- kvm-vnc-return-directly-if-no-vnc-client-connected.patch [bz#1527405]
- kvm-buffer-add-buffer_move_empty.patch [bz#1527405]
- kvm-buffer-add-buffer_move.patch [bz#1527405]
- kvm-vnc-kill-jobs-queue-buffer.patch [bz#1527405]
- kvm-vnc-jobs-move-buffer-reset-use-new-buffer-move.patch [bz#1527405]
- kvm-vnc-zap-dead-code.patch [bz#1527405]
- kvm-vnc-add-vnc_width-vnc_height-helpers.patch [bz#1527405]
- kvm-vnc-factor-out-vnc_update_server_surface.patch [bz#1527405]
- kvm-vnc-use-vnc_-width-height-in-vnc_set_area_dirty.patch [bz#1527405]
- kvm-vnc-only-alloc-server-surface-with-clients-connected.patch [bz#1527405]
- kvm-ui-fix-refresh-of-VNC-server-surface.patch [bz#1527405]
- kvm-ui-move-disconnecting-check-to-start-of-vnc_update_c.patch [bz#1527405]
- kvm-ui-remove-redundant-indentation-in-vnc_client_update.patch [bz#1527405]
- kvm-ui-avoid-pointless-VNC-updates-if-framebuffer-isn-t-.patch [bz#1527405]
- kvm-ui-track-how-much-decoded-data-we-consumed-when-doin.patch [bz#1527405]
- kvm-ui-introduce-enum-to-track-VNC-client-framebuffer-up.patch [bz#1527405]
- kvm-ui-correctly-reset-framebuffer-update-state-after-pr.patch [bz#1527405]
- kvm-ui-refactor-code-for-determining-if-an-update-should.patch [bz#1527405]
- kvm-ui-fix-VNC-client-throttling-when-audio-capture-is-a.patch [bz#1527405]
- kvm-ui-fix-VNC-client-throttling-when-forced-update-is-r.patch [bz#1527405]
- kvm-ui-place-a-hard-cap-on-VNC-server-output-buffer-size.patch [bz#1527405]
- kvm-ui-avoid-sign-extension-using-client-width-height.patch [bz#1527405]
- kvm-ui-correctly-advance-output-buffer-when-writing-SASL.patch [bz#1527405]
- kvm-io-skip-updates-to-client-if-websocket-output-buffer.patch [bz#1518711]
- Resolves: bz#1518711
  (CVE-2017-15268 qemu-kvm: Qemu: I/O: potential memory exhaustion via websock connection to VNC [rhel-7.5])
- Resolves: bz#1527405
  (CVE-2017-15124 qemu-kvm: Qemu: memory exhaustion through framebuffer update request message in VNC server [rhel-7.5])

* Tue Jan 30 2018 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-155.el7
- kvm-qdev-Fix-assert-in-PCI-address-property-when-used-by.patch [bz#1538866]
- kvm-vga-check-the-validation-of-memory-addr-when-draw-te.patch [bz#1534691]
- kvm-savevm-Improve-error-message-for-blocked-migration.patch [bz#1536883]
- kvm-savevm-fail-if-migration-blockers-are-present.patch [bz#1536883]
- Resolves: bz#1534691
  (CVE-2018-5683 qemu-kvm: Qemu: Out-of-bounds read in vga_draw_text routine [rhel-7.5])
- Resolves: bz#1536883
  ([abrt] [faf] qemu-kvm: unknown function(): /usr/libexec/qemu-kvm killed by 6)
- Resolves: bz#1538866
  (qemu will coredump after executing info qtree)

* Wed Jan 24 2018 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-154.el7
- kvm-virtio-net-validate-backend-queue-numbers-against-bu.patch [bz#1460872]
- kvm-dump-guest-memory.py-fix-python-2-support.patch [bz#1411490]
- kvm-qxl-add-migration-blocker-to-avoid-pre-save-assert.patch [bz#1536883]
- Resolves: bz#1411490
  ([RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm))
- Resolves: bz#1460872
  (Aborted(core dumped) when booting guest with "-netdev tap....vhost=on,queues=32")
- Resolves: bz#1536883
  ([abrt] [faf] qemu-kvm: unknown function(): /usr/libexec/qemu-kvm killed by 6)

* Fri Jan 12 2018 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-153.el7
- kvm-i386-update-ssdt-misc.hex.generated.patch [bz#1411490]
- kvm-main-loop-Acquire-main_context-lock-around-os_host_m.patch [bz#1435432 bz#1473536]
- Resolves: bz#1411490
  ([RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm))
- Resolves: bz#1435432
  (Emulated ISA serial port hangs randomly when sending lots of data from guest -> host)
- Resolves: bz#1473536
  (Hangs in serial console under qemu)

* Thu Jan 04 2018 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-152.el7
- kvm-target-i386-cpu-add-new-CPUID-bits-for-indirect-bran.patch [CVE-2017-5715]
- kvm-target-i386-add-support-for-SPEC_CTRL-MSR.patch [CVE-2017-5715]
- kvm-target-i386-cpu-add-new-CPU-models-for-indirect-bran.patch [CVE-2017-5715]

* Tue Dec 19 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-151.el7
- kvm-fw_cfg-remove-support-for-guest-side-data-writes.patch [bz#1411490]
- kvm-fw_cfg-prevent-selector-key-conflict.patch [bz#1411490]
- kvm-fw_cfg-prohibit-insertion-of-duplicate-fw_cfg-file-n.patch [bz#1411490]
- kvm-fw_cfg-factor-out-initialization-of-FW_CFG_ID-rev.-n.patch [bz#1411490]
- kvm-Implement-fw_cfg-DMA-interface.patch [bz#1411490]
- kvm-fw_cfg-avoid-calculating-invalid-current-entry-point.patch [bz#1411490]
- kvm-fw-cfg-support-writeable-blobs.patch [bz#1411490]
- kvm-Enable-fw_cfg-DMA-interface-for-x86.patch [bz#1411490]
- kvm-fw_cfg-unbreak-migration-compatibility.patch [bz#1411490]
- kvm-i386-expose-fw_cfg-QEMU0002-in-SSDT.patch [bz#1411490]
- kvm-fw_cfg-add-write-callback.patch [bz#1411490]
- kvm-hw-misc-add-vmcoreinfo-device.patch [bz#1411490]
- kvm-vmcoreinfo-put-it-in-the-misc-device-category.patch [bz#1411490]
- kvm-fw_cfg-enable-DMA-if-device-vmcoreinfo.patch [bz#1411490]
- kvm-build-sys-restrict-vmcoreinfo-to-fw_cfg-dma-capable-.patch [bz#1411490]
- kvm-dump-Make-DumpState-and-endian-conversion-routines-a.patch [bz#1411490]
- kvm-dump.c-Fix-memory-leak-issue-in-cleanup-processing-f.patch [bz#1411490]
- kvm-dump-Propagate-errors-into-qmp_dump_guest_memory.patch [bz#1411490]
- kvm-dump-Turn-some-functions-to-void-to-make-code-cleane.patch [bz#1411490]
- kvm-dump-Fix-dump-guest-memory-termination-and-use-after.patch [bz#1411490]
- kvm-dump-allow-target-to-set-the-page-size.patch [bz#1411490]
- kvm-dump-allow-target-to-set-the-physical-base.patch [bz#1411490]
- kvm-dump-guest-memory-cleanup-removing-dump_-error-clean.patch [bz#1411490]
- kvm-dump-guest-memory-using-static-DumpState-add-DumpSta.patch [bz#1411490]
- kvm-dump-guest-memory-add-dump_in_progress-helper-functi.patch [bz#1411490]
- kvm-dump-guest-memory-introduce-dump_process-helper-func.patch [bz#1411490]
- kvm-dump-guest-memory-disable-dump-when-in-INMIGRATE-sta.patch [bz#1411490]
- kvm-DumpState-adding-total_size-and-written_size-fields.patch [bz#1411490]
- kvm-dump-do-not-dump-non-existent-guest-memory.patch [bz#1411490]
- kvm-dump-add-guest-ELF-note.patch [bz#1411490]
- kvm-dump-update-phys_base-header-field-based-on-VMCOREIN.patch [bz#1411490]
- kvm-kdump-set-vmcoreinfo-location.patch [bz#1411490]
- kvm-scripts-dump-guest-memory.py-Move-constants-to-the-t.patch [bz#1411490]
- kvm-scripts-dump-guest-memory.py-Make-methods-functions.patch [bz#1411490]
- kvm-scripts-dump-guest-memory.py-Improve-python-3-compat.patch [bz#1411490]
- kvm-scripts-dump-guest-memory.py-Cleanup-functions.patch [bz#1411490]
- kvm-scripts-dump-guest-memory.py-Introduce-multi-arch-su.patch [bz#1411490]
- kvm-Fix-typo-in-variable-name-found-and-fixed-by-codespe.patch [bz#1411490]
- kvm-scripts-dump-guest-memory.py-add-vmcoreinfo.patch [bz#1411490]
- kvm-dump-guest-memory.py-fix-No-symbol-vmcoreinfo_find.patch [bz#1411490]
- kvm-dump-guest-memory.py-fix-You-can-t-do-that-without-a.patch [bz#1411490]
- Resolves: bz#1411490
  ([RFE] Kernel address space layout randomization [KASLR] support (qemu-kvm))

* Tue Dec 12 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-150.el7
- kvm-Build-only-x86_64-packages.patch [bz#1520793]
- Resolves: bz#1520793
  (Do not build non-x86_64 subpackages)

* Wed Nov 29 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-149.el7
- kvm-block-linux-aio-fix-memory-and-fd-leak.patch [bz#1491434]
- kvm-linux-aio-Fix-laio-resource-leak.patch [bz#1491434]
- kvm-slirp-cleanup-leftovers-from-misc.h.patch [bz#1508745]
- kvm-Avoid-embedding-struct-mbuf-in-other-structures.patch [bz#1508745]
- kvm-slirp-Fix-access-to-freed-memory.patch [bz#1508745]
- kvm-slirp-fix-clearing-ifq_so-from-pending-packets.patch [bz#1508745]
- kvm-qcow2-Prevent-backing-file-names-longer-than-1023.patch [bz#1459714]
- kvm-qemu-img-Use-strerror-for-generic-resize-error.patch [bz#1459725]
- kvm-qcow2-Avoid-making-the-L1-table-too-big.patch [bz#1459725]
- Resolves: bz#1459714
  (Throw error if qemu-img rebasing backing file is too long or provide way to fix a "too long" backing file.)
- Resolves: bz#1459725
  (Prevent qemu-img resize from causing "Active L1 table too large")
- Resolves: bz#1491434
  (KVM leaks file descriptors when attaching and detaching virtio-scsi block devices)
- Resolves: bz#1508745
  (CVE-2017-13711 qemu-kvm: Qemu: Slirp: use-after-free when sending response [rhel-7.5])

* Fri Nov 10 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-148.el7
- kvm-multiboot-validate-multiboot-header-address-values.patch [bz#1501121]
- kvm-qemu-option-reject-empty-number-value.patch [bz#1417864]
- Resolves: bz#1417864
  (Qemu-kvm starts with unspecified port)
- Resolves: bz#1501121
  (CVE-2017-14167 qemu-kvm: Qemu: i386: multiboot OOB access while loading kernel image [rhel-7.5])

* Fri Nov 03 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-147.el7
- kvm-vga-drop-line_offset-variable.patch [bz#1501295]
- kvm-vga-Add-mechanism-to-force-the-use-of-a-shadow-surfa.patch [bz#1501295]
- kvm-vga-handle-cirrus-vbe-mode-wraparounds.patch [bz#1501295]
- kvm-cirrus-fix-oob-access-in-mode4and5-write-functions.patch [bz#1501295]
- kvm-i6300esb-Fix-signed-integer-overflow.patch [bz#1470244]
- kvm-i6300esb-fix-timer-overflow.patch [bz#1470244]
- kvm-i6300esb-remove-muldiv64.patch [bz#1470244]
- Resolves: bz#1470244
  (reboot leads to shutoff of qemu-kvm-vm if i6300esb-watchdog set to poweroff)
- Resolves: bz#1501295
  (CVE-2017-15289 qemu-kvm: Qemu: cirrus: OOB access issue in  mode4and5 write functions [rhel-7.5])

* Tue Oct 24 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-146.el7
- kvm-vfio-pass-device-to-vfio_mmap_bar-and-use-it-to-set-.patch [bz#1494181]
- kvm-hw-vfio-pci-Rename-VFIODevice-into-VFIOPCIDevice.patch [bz#1494181]
- kvm-hw-vfio-pci-generalize-mask-unmask-to-any-IRQ-index.patch [bz#1494181]
- kvm-hw-vfio-pci-introduce-minimalist-VFIODevice-with-fd.patch [bz#1494181]
- kvm-hw-vfio-pci-add-type-name-and-group-fields-in-VFIODe.patch [bz#1494181]
- kvm-hw-vfio-pci-handle-reset-at-VFIODevice.patch [bz#1494181]
- kvm-hw-vfio-pci-Introduce-VFIORegion.patch [bz#1494181]
- kvm-hw-vfio-pci-use-name-field-in-format-strings.patch [bz#1494181]
- kvm-vfio-Add-sysfsdev-property-for-pci-platform.patch [bz#1494181]
- kvm-vfio-remove-bootindex-property-from-qdev-to-qom.patch [bz#1494181]
- kvm-vfio-pci-Handle-host-oversight.patch [bz#1494181]
- kvm-vfio-pci-Fix-incorrect-error-message.patch [bz#1494181]
- kvm-vfio-Wrap-VFIO_DEVICE_GET_REGION_INFO.patch [bz#1494181]
- kvm-vfio-Generalize-region-support.patch [bz#1494181]
- kvm-vfio-Enable-sparse-mmap-capability.patch [bz#1494181]
- kvm-vfio-Handle-zero-length-sparse-mmap-ranges.patch [bz#1494181]
- kvm-bswap.h-Remove-cpu_to_32wu.patch [bz#1486642]
- kvm-hw-use-ld_p-st_p-instead-of-ld_raw-st_raw.patch [bz#1486642]
- kvm-vga-Start-cutting-out-non-32bpp-conversion-support.patch [bz#1486642]
- kvm-vga-Remove-remainder-of-old-conversion-cruft.patch [bz#1486642]
- kvm-vga-Separate-LE-and-BE-conversion-functions.patch [bz#1486642]
- kvm-vga-Rename-vga_template.h-to-vga-helpers.h.patch [bz#1486642]
- kvm-vga-stop-passing-pointers-to-vga_draw_line-functions.patch [bz#1486642]
- kvm-target-i386-Add-Intel-SHA_NI-instruction-support.patch [bz#1450396]
- kvm-target-i386-cpu-Add-new-EPYC-CPU-model.patch [bz#1450396]
- kvm-target-i386-Enable-clflushopt-clwb-pcommit-instructi.patch [bz#1501510]
- kvm-i386-add-Skylake-Server-cpu-model.patch [bz#1501510]
- Resolves: bz#1450396
  (Add support for AMD EPYC processors)
- Resolves: bz#1486642
  (CVE-2017-13672 qemu-kvm: Qemu: vga: OOB read access during display update [rhel-7.5])
- Resolves: bz#1494181
  (Backport vGPU support to qemu-kvm)
- Resolves: bz#1501510
  (Add Skylake-Server CPU model (qemu-kvm))

* Fri Oct 06 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-145.el7
- kvm-qemu-char-add-Czech-characters-to-VNC-keysyms.patch [bz#1476641]
- kvm-qemu-char-add-missing-characters-used-in-keymaps.patch [bz#1476641]
- kvm-qemu-char-add-cyrillic-characters-numerosign-to-VNC-.patch [bz#1476641]
- kvm-block-ssh-Use-QemuOpts-for-runtime-options.patch [bz#1461672]
- Resolves: bz#1461672
  (qemu-img core dumped when create external snapshot through ssh protocol without specifying image size)
- Resolves: bz#1476641
  (ui/vnc_keysym.h is very out of date and does not correctly support many Eastern European keyboards)

* Mon Oct 02 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-144.el7
- kvm-qemu-nbd-Ignore-SIGPIPE.patch [bz#1466463]
- Resolves: bz#1466463
  (CVE-2017-10664 qemu-kvm: Qemu: qemu-nbd: server breaks with SIGPIPE upon client abort [rhel-7.5])

* Thu Sep 28 2017 Wainer dos Santos Moschetta <wainersm@redhat.com> - 1.5.3-143.el7
- kvm-block-Limit-multiwrite-merge-downstream-only.patch [bz#1492559]
- Resolves: bz#1492559
  (virtio-blk mutiwrite merge causes too big IO)

* Wed Sep 20 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-142.el7
- kvm-vnc-allow-to-connect-with-add_client-when-vnc-none.patch [bz#1435352]
- kvm-virtio-net-dynamic-network-offloads-configuration.patch [bz#1480428]
- kvm-Workaround-rhel6-ctrl_guest_offloads-machine-type-mi.patch [bz#1480428]
- kvm-target-i386-Add-PKU-and-and-OSPKE-support.patch [bz#1387648]
- Resolves: bz#1387648
  ([Intel 7.5 FEAT] Memory Protection Keys for qemu-kvm)
- Resolves: bz#1435352
  (qemu started with "-vnc none,..." doesn't support any VNC authentication)
- Resolves: bz#1480428
  (KVM: windows guest migration from EL6 to EL7 fails.)

* Tue Jun 13 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-141.el7
- kvm-Fix-memory-slot-page-alignment-logic-bug-1455745.patch [bz#1455745]
- kvm-Do-not-hang-on-full-PTY.patch [bz#1452067]
- kvm-serial-fixing-vmstate-for-save-restore.patch [bz#1452067]
- kvm-serial-reinstate-watch-after-migration.patch [bz#1452067]
- kvm-nbd-Fully-initialize-client-in-case-of-failed-negoti.patch [bz#1451614]
- kvm-nbd-Fix-regression-on-resiliency-to-port-scan.patch [bz#1451614]
- Resolves: bz#1451614
  (CVE-2017-9524 qemu-kvm: segment fault when private user nmap qemu-nbd server [rhel-7.4])
- Resolves: bz#1452067
  (migration can confuse serial port user)
- Resolves: bz#1455745
  (Backport fix for broken logic that's supposed to ensure memory slots are page aligned)

* Tue Jun 06 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-140.el7
- kvm-spice-fix-spice_chr_add_watch-pre-condition.patch [bz#1456983]
- Resolves: bz#1456983
  (Character device regression due to missing patch)

* Wed May 24 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-139.el7
- kvm-char-change-qemu_chr_fe_add_watch-to-return-unsigned.patch [bz#1451470]
- Resolves: bz#1451470
  (RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop)

* Tue May 23 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-138.el7
- kvm-char-serial-cosmetic-fixes.patch [bz#1451470]
- kvm-char-serial-Use-generic-Fifo8.patch [bz#1451470]
- kvm-char-serial-serial_ioport_write-Factor-out-common-co.patch [bz#1451470]
- kvm-char-serial-fix-copy-paste-error-fifo8_is_full-vs-em.patch [bz#1451470]
- kvm-char-serial-Fix-emptyness-check.patch [bz#1451470]
- kvm-char-serial-Fix-emptyness-handling.patch [bz#1451470]
- kvm-serial-poll-the-serial-console-with-G_IO_HUP.patch [bz#1451470]
- kvm-serial-change-retry-logic-to-avoid-concurrency.patch [bz#1451470]
- kvm-qemu-char-ignore-flow-control-if-a-PTY-s-slave-is-no.patch [bz#1451470]
- kvm-serial-check-if-backed-by-a-physical-serial-port-at-.patch [bz#1451470]
- kvm-serial-reset-thri_pending-on-IER-writes-with-THRI-0.patch [bz#1451470]
- kvm-serial-clean-up-THRE-TEMT-handling.patch [bz#1451470]
- kvm-serial-update-LSR-on-enabling-disabling-FIFOs.patch [bz#1451470]
- kvm-serial-only-resample-THR-interrupt-on-rising-edge-of.patch [bz#1451470]
- kvm-serial-make-tsr_retry-unsigned.patch [bz#1451470]
- kvm-serial-simplify-tsr_retry-reset.patch [bz#1451470]
- kvm-serial-separate-serial_xmit-and-serial_watch_cb.patch [bz#1451470]
- kvm-serial-remove-watch-on-reset.patch [bz#1451470]
- Resolves: bz#1451470
  (RHEL 7.2 based VM (Virtual Machine) hung for several hours apparently waiting for lock held by main_loop)

* Fri Apr 28 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-137.el7
- kvm-ide-fix-halted-IO-segfault-at-reset.patch [bz#1299875]
- Resolves: bz#1299875
  (system_reset should clear pending request for error (IDE))

* Tue Apr 18 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-136.el7
- kvm-target-i386-get-set-migrate-XSAVES-state.patch [bz#1327593]
- kvm-Removing-texi2html-from-build-requirements.patch [bz#1440987]
- kvm-Disable-build-of-32bit-packages.patch [bz#1441778]
- kvm-Add-sample-images-to-srpm.patch [bz#1436280]
- Resolves: bz#1327593
  ([Intel 7.4 FEAT] KVM Enable the XSAVEC, XSAVES and XRSTORS instructions)
- Resolves: bz#1436280
  (sample images  for qemu-iotests are missing in the SRPM)
- Resolves: bz#1440987
  (Remove texi2html build dependancy from RPM)
- Resolves: bz#1441778
  (Stop building qemu-img for 32bit architectures.)

* Thu Mar 30 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-135.el7
- kvm-fix-cirrus_vga-fix-OOB-read-case-qemu-Segmentation-f.patch [bz#1430060]
- kvm-cirrus-vnc-zap-bitblit-support-from-console-code.patch [bz#1430060]
- kvm-cirrus-add-option-to-disable-blitter.patch [bz#1430060]
- kvm-cirrus-fix-cirrus_invalidate_region.patch [bz#1430060]
- kvm-cirrus-stop-passing-around-dst-pointers-in-the-blitt.patch [bz#1430060]
- kvm-cirrus-stop-passing-around-src-pointers-in-the-blitt.patch [bz#1430060]
- kvm-cirrus-fix-off-by-one-in-cirrus_bitblt_rop_bkwd_tran.patch [bz#1430060]
- Resolves: bz#1430060
  (CVE-2016-9603 qemu-kvm: Qemu: cirrus: heap buffer overflow via vnc connection [rhel-7.4])

* Tue Mar 21 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-134.el7
- kvm-ui-vnc-introduce-VNC_DIRTY_PIXELS_PER_BIT-macro.patch [bz#1377977]
- kvm-ui-vnc-derive-cmp_bytes-from-VNC_DIRTY_PIXELS_PER_BI.patch [bz#1377977]
- kvm-ui-vnc-optimize-dirty-bitmap-tracking.patch [bz#1377977]
- kvm-ui-vnc-optimize-setting-in-vnc_dpy_update.patch [bz#1377977]
- kvm-ui-vnc-fix-vmware-VGA-incompatiblities.patch [bz#1377977]
- kvm-ui-vnc-fix-potential-memory-corruption-issues.patch [bz#1377977]
- kvm-vnc-fix-memory-corruption-CVE-2015-5225.patch [bz#1377977]
- kvm-vnc-fix-overflow-in-vnc_update_stats.patch [bz#1377977]
- kvm-i386-kvmvapic-initialise-imm32-variable.patch [bz#1335751]
- kvm-qemu-iotests-Filter-out-actual-image-size-in-067.patch [bz#1427176]
- vm-qcow2-Don-t-rely-on-free_cluster_index-in-alloc_ref2.patch [bz#1427176]
- kvm-qemu-iotests-Fix-core-dump-suppression-in-test-039.patch [bz#1427176]
- kvm-qemu-io-Add-sigraise-command.patch [bz#1427176]
- kvm-iotests-Filter-for-Killed-in-qemu-io-output.patch [bz#1427176]
- kvm-iotests-Fix-test-039.patch [bz#1427176]
- kvm-blkdebug-Add-bdrv_truncate.patch [bz#1427176]
- kvm-vhdx-Fix-zero-fill-iov-length.patch [bz#1427176]
- kvm-qemu-iotests-Disable-030-040-041.patch [bz#1427176]
- kvm-x86-add-AVX512_VPOPCNTDQ-features.patch [bz#1415830]
- kvm-usb-ccid-check-ccid-apdu-length.patch [bz#1419818]
- kvm-usb-ccid-better-bulk_out-error-handling.patch [bz#1419818]
- kvm-usb-ccid-move-header-size-check.patch [bz#1419818]
- kvm-usb-ccid-add-check-message-size-checks.patch [bz#1419818]
- kvm-spec-Update-rdma-build-dependency.patch [bz#1433920]
- Resolves: bz#1335751
  (CVE-2016-4020 qemu-kvm: Qemu: i386: leakage of stack memory to guest in kvmvapic.c [rhel-7.4])
- Resolves: bz#1377977
  (qemu-kvm coredump in vnc_raw_send_framebuffer_update [rhel-7.4])
- Resolves: bz#1415830
  ([Intel 7.4 FEAT] Enable vpopcntdq for KNM - qemu/kvm)
- Resolves: bz#1419818
  (CVE-2017-5898 qemu-kvm: Qemu: usb: integer overflow in emulated_apdu_from_guest [rhel-7.4])
- Resolves: bz#1427176
  (test cases of qemu-iotests failed)
- Resolves: bz#1433920
  (Switch from librdmacm-devel to rdma-core-devel)

* Thu Mar 09 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-133.el7
- kvm-target-i386-add-Ivy-Bridge-CPU-model.patch [bz#1368375]
- kvm-x86-add-AVX512_4VNNIW-and-AVX512_4FMAPS-features.patch [bz#1382122]
- kvm-target-i386-kvm_cpu_fill_host-Kill-unused-code.patch [bz#1382122]
- kvm-target-i386-kvm_cpu_fill_host-No-need-to-check-level.patch [bz#1382122]
- kvm-target-i386-kvm_cpu_fill_host-No-need-to-check-CPU-v.patch [bz#1382122]
- kvm-target-i386-kvm_cpu_fill_host-No-need-to-check-xleve.patch [bz#1382122]
- kvm-target-i386-kvm_cpu_fill_host-Set-all-feature-words-.patch [bz#1382122]
- kvm-target-i386-kvm_cpu_fill_host-Fill-feature-words-in-.patch [bz#1382122]
- kvm-target-i386-kvm_check_features_against_host-Kill-fea.patch [bz#1382122]
- kvm-target-i386-Make-TCG-feature-filtering-more-readable.patch [bz#1382122]
- kvm-target-i386-Filter-FEAT_7_0_EBX-TCG-features-too.patch [bz#1382122]
- kvm-target-i386-Filter-KVM-and-0xC0000001-features-on-TC.patch [bz#1382122]
- kvm-target-i386-Define-TCG_-_FEATURES-earlier-in-cpu.c.patch [bz#1382122]
- kvm-target-i386-Loop-based-copying-and-setting-unsetting.patch [bz#1382122]
- kvm-target-i386-Loop-based-feature-word-filtering-in-TCG.patch [bz#1382122]
- kvm-spice-remove-spice-experimental.h-include.patch [bz#1430606]
- kvm-spice-replace-use-of-deprecated-API.patch [bz#1430606]
- Resolves: bz#1368375
  ([Intel 7.4 Bug] qemu-kvm does not support “-cpu IvyBridge”)
- Resolves: bz#1382122
  ([Intel 7.4 FEAT] KVM Enable the avx512_4vnniw, avx512_4fmaps instructions in qemu)
- Resolves: bz#1430606
  (Can't build qemu-kvm with newer spice packages)

* Tue Feb 21 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-132.el7
- kvm-cirrus-fix-patterncopy-checks.patch [bz#1420492]
- kvm-Revert-cirrus-allow-zero-source-pitch-in-pattern-fil.patch [bz#1420492]
- kvm-cirrus-add-blit_is_unsafe-call-to-cirrus_bitblt_cput.patch [bz#1420492]
- Resolves: bz#1420492
  (EMBARGOED CVE-2017-2620 qemu-kvm: Qemu: display: cirrus: potential arbitrary code execution via cirrus_bitblt_cputovideo [rhel-7.4])

* Fri Feb 10 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-131.el7
- kvm-memory-Allow-access-only-upto-the-maximum-alignment-.patch [bz#1342768]
- kvm-virtio-blk-Release-s-rq-queue-at-system_reset.patch [bz#1361488]
- kvm-cirrus_vga-fix-off-by-one-in-blit_region_is_unsafe.patch [bz#1418233]
- kvm-display-cirrus-check-vga-bits-per-pixel-bpp-value.patch [bz#1418233]
- kvm-display-cirrus-ignore-source-pitch-value-as-needed-i.patch [bz#1418233]
- kvm-cirrus-handle-negative-pitch-in-cirrus_invalidate_re.patch [bz#1418233]
- kvm-cirrus-allow-zero-source-pitch-in-pattern-fill-rops.patch [bz#1418233]
- kvm-cirrus-fix-blit-address-mask-handling.patch [bz#1418233]
- kvm-cirrus-fix-oob-access-issue-CVE-2017-2615.patch [bz#1418233]
- kvm-HMP-Fix-user-manual-typo-of-__com.redhat_qxl_screend.patch [bz#1419898]
- kvm-HMP-Fix-documentation-of-__com.redhat.drive_add.patch [bz#1419898]
- Resolves: bz#1342768
  ([Intel 7.4 Bug] qemu-kvm crashes with Linux kernel 4.6.0 or above)
- Resolves: bz#1361488
  (system_reset should clear pending request for error (virtio-blk))
- Resolves: bz#1418233
  (CVE-2017-2615 qemu-kvm: Qemu: display: cirrus: oob access while doing bitblt copy backward mode [rhel-7.4])
- Resolves: bz#1419898
  (Documentation inaccurate for __com.redhat_qxl_screendump and __com.redhat_drive_add)

* Wed Feb 01 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-130.el7
- kvm-gluster-correctly-propagate-errors.patch [bz#1151859]
- kvm-gluster-Correctly-propagate-errors-when-volume-isn-t.patch [bz#1151859]
- kvm-block-gluster-add-support-for-selecting-debug-loggin.patch [bz#1151859]
- Resolves: bz#1151859
  ([RFE] Allow the libgfapi logging level to be controlled.)

* Wed Jan 18 2017 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-129.el7
- kvm-Update-qemu-kvm-package-Summary-and-Description.patch [bz#1378541]
- kvm-vl-Don-t-silently-change-topology-when-all-smp-optio.patch [bz#1375507]
- kvm-net-check-packet-payload-length.patch [bz#1398218]
- kvm-qxl-Only-emit-QXL_INTERRUPT_CLIENT_MONITORS_CONFIG-o.patch [bz#1342489]
- Resolves: bz#1342489
  (Flickering Fedora 24 Login Screen on RHEL 7)
- Resolves: bz#1375507
  ("threads" option is overwritten if both "sockets" and "cores" is set on -smp)
- Resolves: bz#1378541
  (QEMU: update package summary and description)
- Resolves: bz#1398218
  (CVE-2016-2857 qemu-kvm: Qemu: net: out of bounds read in net_checksum_calculate() [rhel-7.4])

* Thu Nov 24 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-128.el7
- kvm-virtio-introduce-virtqueue_unmap_sg.patch [bz#1377968]
- kvm-virtio-introduce-virtqueue_discard.patch [bz#1377968]
- kvm-virtio-decrement-vq-inuse-in-virtqueue_discard.patch [bz#1377968]
- kvm-balloon-fix-segfault-and-harden-the-stats-queue.patch [bz#1377968]
- kvm-virtio-balloon-discard-virtqueue-element-on-reset.patch [bz#1377968]
- kvm-virtio-zero-vq-inuse-in-virtio_reset.patch [bz#1377968]
- kvm-virtio-add-virtqueue_rewind.patch [bz#1377968]
- kvm-virtio-balloon-fix-stats-vq-migration.patch [bz#1377968]
- Resolves: bz#1377968
  ([RHEL7.3] KVM guest shuts itself down after 128th reboot)

* Wed Nov 16 2016 Danilo de Paula <ddepaula@redhat.com> - 1.5.3-127.el7
- kvm-hw-i386-regenerate-checked-in-AML-payload-RHEL-only.patch [bz#1377087]
- kvm-ide-fix-halted-IO-segfault-at-reset.patch [bz#1377087]
- Resolves: bz#1377087
  (shutdown rhel 5.11 guest failed and stop at "system halted")

* Tue Sep 20 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-126.el7
- kvm-virtio-recalculate-vq-inuse-after-migration.patch [bz#1376542]
- Resolves: bz#1376542
  (RHSA-2016-1756 breaks migration of instances)

* Thu Sep 15 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-125.el7
- kvm-nbd-server-Set-O_NONBLOCK-on-client-fd.patch [bz#1285453]
- Resolves: bz#1285453
  (An NBD client can cause QEMU main loop to block when connecting to built-in NBD server)

* Tue Sep 13 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-124.el7
- kvm-target-i386-Add-support-for-FEAT_7_0_ECX.patch [bz#1372459]
- kvm-target-i386-Add-more-Intel-AVX-512-instructions-supp.patch [bz#1372459]
- Resolves: bz#1372459
  ([Intel 7.3 Bug] SKL-SP Guest cpu doesn't support avx512 instruction sets(avx512bw, avx512dq and avx512vl) (qemu-kvm))

* Fri Sep 09 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-123.el7
- kvm-Fix-backport-of-target-i386-add-feature-flags-for-CP.patch [bz#1371619]
- kvm-Add-skip_dump-flag-to-ignore-memory-region-during-du.patch [bz#1373088]
- Resolves: bz#1371619
  (Flags xsaveopt xsavec xgetbv1 are missing on qemu-kvm)
- Resolves: bz#1373088
  ([FJ7.3 Bug]: virsh dump with both --memory-only and --format option fails)

* Fri Aug 26 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-122.el7
- kvm-virtio-validate-the-existence-of-handle_output-befor.patch [bz#1367040]
- Resolves: bz#1367040
  (QEMU crash when guest notifies non-existent virtqueue)

* Tue Aug 02 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-121.el7
- kvm-json-parser-drop-superfluous-assignment-for-token-va.patch [bz#1276036]
- kvm-qjson-Apply-nesting-limit-more-sanely.patch [bz#1276036]
- kvm-qjson-Don-t-crash-when-input-exceeds-nesting-limit.patch [bz#1276036]
- kvm-check-qjson-Add-test-for-JSON-nesting-depth-limit.patch [bz#1276036]
- kvm-qjson-Spell-out-some-silent-assumptions.patch [bz#1276036]
- kvm-qjson-Give-each-of-the-six-structural-chars-its-own-.patch [bz#1276036]
- kvm-qjson-Inline-token_is_keyword-and-simplify.patch [bz#1276036]
- kvm-qjson-Inline-token_is_escape-and-simplify.patch [bz#1276036]
- kvm-qjson-replace-QString-in-JSONLexer-with-GString.patch [bz#1276036]
- kvm-qjson-Convert-to-parser-to-recursive-descent.patch [bz#1276036]
- kvm-qjson-store-tokens-in-a-GQueue.patch [bz#1276036]
- kvm-qjson-surprise-allocating-6-QObjects-per-token-is-ex.patch [bz#1276036]
- kvm-qjson-Limit-number-of-tokens-in-addition-to-total-si.patch [bz#1276036]
- kvm-json-streamer-Don-t-leak-tokens-on-incomplete-parse.patch [bz#1276036]
- kvm-json-streamer-fix-double-free-on-exiting-during-a-pa.patch [bz#1276036]
- kvm-trace-remove-malloc-tracing.patch [bz#1360137]
- Resolves: bz#1276036
  (Crash on QMP input exceeding limits)
- Resolves: bz#1360137
  (GLib-WARNING **: gmem.c:482: custom memory allocation vtable not supported)

* Fri Jul 29 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-120.el7
- kvm-Add-install-dependency-to-newer-libusbx-version.patch [bz#1351106]
- kvm-virtio-error-out-if-guest-exceeds-virtqueue-size.patch [bz#1359729]
- Resolves: bz#1351106
  (symbol lookup error: /usr/libexec/qemu-kvm: undefined symbol: libusb_get_port_numbers)
- Resolves: bz#1359729
  (CVE-2016-5403 qemu-kvm: Qemu: virtio: unbounded memory allocation on host via guest leading to DoS [rhel-7.3])

* Tue Jul 26 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-119.el7
- kvm-qxl-factor-out-qxl_get_check_slot_offset.patch [bz#1355730]
- kvm-qxl-store-memory-region-and-offset-instead-of-pointe.patch [bz#1355730]
- kvm-qxl-fix-surface-migration.patch [bz#1355730]
- kvm-qxl-fix-qxl_set_dirty-call-in-qxl_dirty_one_surface.patch [bz#1355730]
- Resolves: bz#1355730
  (spice-gtk shows outdated screen state after migration [qemu-kvm])

* Tue Jul 19 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-118.el7
- kvm-util-introduce-MIN_NON_ZERO.patch [bz#1318199]
- kvm-BlockLimits-introduce-max_transfer_length.patch [bz#1318199]
- kvm-block-backend-expose-bs-bl.max_transfer_length.patch [bz#1318199]
- kvm-scsi-generic-Merge-block-max-xfer-len-in-INQUIRY-res.patch [bz#1318199]
- kvm-raw-posix-Fetch-max-sectors-for-host-block-device.patch [bz#1318199]
- kvm-scsi-Advertise-limits-by-blocksize-not-512.patch [bz#1318199]
- kvm-util-Fix-MIN_NON_ZERO.patch [bz#1318199]
- Resolves: bz#1318199
  (expose host BLKSECTGET limit in scsi-block (qemu-kvm))

* Tue Jul 12 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-117.el7
- kvm-target-i386-add-feature-flags-for-CPUID-EAX-0xd-ECX-.patch [bz#1327599]
- kvm-target-i386-add-Skylake-Client-cpu-model.patch [bz#1327599]
- Resolves: bz#1327599
  (Add Skylake CPU model)

* Tue Jun 28 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-116.el7
- kvm-block-iscsi-avoid-potential-overflow-of-acb-task-cdb.patch [bz#1340929]
- Resolves: bz#1340929
  (CVE-2016-5126 qemu-kvm: Qemu: block: iscsi: buffer overflow in iscsi_aio_ioctl [rhel-7.3])

* Mon Jun 20 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-115.el7
- kvm-spice-do-not-require-TCP-ports.patch [bz#1336491]
- kvm-vga-add-sr_vbe-register-set.patch [bz#1346982]
- Resolves: bz#1336491
  (Ship FD connection patches qemu-kvm part)
- Resolves: bz#1346982
  (Regression from CVE-2016-3712: windows installer fails to start)

* Wed Jun 15 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-114.el7
- kvm-hw-input-hid.c-Fix-capslock-hid-code.patch [bz#1256741]
- kvm-target-i386-fix-pcmpxstrx-equal-ordered-strstr-mode.patch [bz#1340971]
- kvm-spec-Update-rules-before-triggering-for-kvm-device.patch [bz#1333159]
- Resolves: bz#1256741
  ("CapsLock" will work as "\" when boot a guest with usb-kbd)
- Resolves: bz#1333159
  (qemu-kvm doesn't reload udev rules before triggering for kvm device)
- Resolves: bz#1340971
  (qemu: accel=tcg does not implement SSE 4 properly)

* Sat May 28 2016 Jeff E. Nelson <jen@redhat.com> - 1.5.3-113.el7
- kvm-qxl-allow-to-specify-head-limit-to-qxl-driver.patch [bz#1283198]
- kvm-qxl-Fix-new-function-name-for-spice-server-library.patch [bz#1283198]
- kvm-block-raw-posix-Open-file-descriptor-O_RDWR-to-work-.patch [bz#1268345]
- Resolves: bz#1268345
  (posix_fallocate emulation on NFS fails with Bad file descriptor if fd is opened O_WRONLY)
- Resolves: bz#1283198
  (RFE: backport max monitor limitation from Qemu upstream)

* Mon May 16 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-112.el7
- kvm-virtio-scsi-Prevent-assertion-on-missed-events.patch [bz#1312289]
- kvm-seccomp-adding-sysinfo-system-call-to-whitelist.patch [bz#1177318]
- kvm-acpi-strip-compiler-info-in-built-in-DSDT.patch [bz#1330969]
- kvm-acpi-fix-endian-ness-for-table-ids.patch [bz#1330969]
- kvm-acpi-support-specified-oem-table-id-for-build_header.patch [bz#1330969]
- kvm-acpi-take-oem_id-in-build_header-optionally.patch [bz#1330969]
- kvm-acpi-expose-oem_id-and-oem_table_id-in-build_rsdt.patch [bz#1330969]
- kvm-acpi-add-function-to-extract-oem_id-and-oem_table_id.patch [bz#1330969]
- kvm-pc-set-the-OEM-fields-in-the-RSDT-and-the-FADT-from-.patch [bz#1330969]
- kvm-block-jobs-qemu-kvm-rhel-differentiation.patch [bz#1156635]
- Resolves: bz#1156635
  (Libvirt is confused that qemu-kvm exposes 'block-job-cancel' but not 'block-stream')
- Resolves: bz#1177318
  (Guest using rbd based image as disk failed to start when sandbox was enabled)
- Resolves: bz#1312289
  ("qemu-kvm: /builddir/build/BUILD/qemu-1.5.3/hw/scsi/virtio-scsi.c:533: virtio_scsi_push_event: Assertion `event == 0' failed" after hotplug 20 virtio-scsi disks then hotunplug them)
- Resolves: bz#1330969
  (match the OEM ID and OEM Table ID fields of the FADT and the RSDT to those of the SLIC)

* Thu May 05 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-111.el7
- kvm-vmdk-Leave-bdi-intact-if-ENOTSUP-in-vmdk_get_info.patch [bz#1299250]
- kvm-vmdk-Use-g_random_int-to-generate-CID.patch [bz#1299250]
- kvm-vmdk-Fix-comment-to-match-code-of-extent-lines.patch [bz#1299250]
- kvm-vmdk-Clean-up-descriptor-file-reading.patch [bz#1299250]
- kvm-vmdk-Check-descriptor-file-length-when-reading-it.patch [bz#1299250]
- kvm-vmdk-Remove-unnecessary-initialization.patch [bz#1299250]
- kvm-vmdk-Set-errp-on-failures-in-vmdk_open_vmdk4.patch [bz#1299250]
- kvm-block-vmdk-make-ret-variable-usage-clear.patch [bz#1299250]
- kvm-block-vmdk-move-string-allocations-from-stack-to-the.patch [bz#1299250]
- kvm-block-vmdk-fixed-sizeof-error.patch [bz#1299250]
- kvm-vmdk-Widen-before-shifting-32-bit-header-field.patch [bz#1299250]
- kvm-vmdk-Fix-next_cluster_sector-for-compressed-write.patch [bz#1299250]
- kvm-vmdk-Fix-index_in_cluster-calculation-in-vmdk_co_get.patch [bz#1299250]
- kvm-vmdk-Use-vmdk_find_index_in_cluster-everywhere.patch [bz#1299250]
- kvm-vmdk-Fix-next_cluster_sector-for-compressed-write2.patch [bz#1299250]
- kvm-vmdk-Create-streamOptimized-as-version-3.patch [bz#1299116]
- kvm-vmdk-Fix-converting-to-streamOptimized.patch [bz#1299116]
- kvm-vmdk-Fix-calculation-of-block-status-s-offset.patch [bz#1299116]
- Resolves: bz#1299116
  (qemu-img created VMDK images lead to "Not a supported disk format (sparse VMDK version too old)")
- Resolves: bz#1299250
  (qemu-img created VMDK images are unbootable)

* Wed May 04 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-110.el7
- kvm-qemu-io-Remove-unused-args_command.patch [bz#1272523]
- kvm-cutils-Support-P-and-E-suffixes-in-strtosz.patch [bz#1272523]
- kvm-qemu-io-Make-cvtnum-a-wrapper-around-strtosz_suffix.patch [bz#1272523]
- kvm-qemu-io-Handle-cvtnum-errors-in-alloc.patch [bz#1272523]
- kvm-qemu-io-Don-t-use-global-bs-in-command-implementatio.patch [bz#1272523]
- kvm-qemu-io-Split-off-commands-to-qemu-io-cmds.c.patch [bz#1272523]
- kvm-qemu-io-Factor-out-qemuio_command.patch [bz#1272523]
- kvm-qemu-io-Move-help-function.patch [bz#1272523]
- kvm-qemu-io-Move-quit-function.patch [bz#1272523]
- kvm-qemu-io-Move-qemu_strsep-to-cutils.c.patch [bz#1272523]
- kvm-qemu-io-Move-functions-for-registering-and-running-c.patch [bz#1272523]
- kvm-qemu-io-Move-command_loop-and-friends.patch [bz#1272523]
- kvm-qemu-io-Move-remaining-helpers-from-cmd.c.patch [bz#1272523]
- kvm-qemu-io-Interface-cleanup.patch [bz#1272523]
- kvm-qemu-io-Use-the-qemu-version-for-V.patch [bz#1272523]
- kvm-Make-qemu-io-commands-available-in-HMP.patch [bz#1272523]
- kvm-blkdebug-Add-BLKDBG_FLUSH_TO_OS-DISK-events.patch [bz#1272523]
- kvm-qemu-io-fix-cvtnum-lval-types.patch [bz#1272523]
- kvm-qemu-io-Check-for-trailing-chars.patch [bz#1272523]
- kvm-qemu-io-Correct-error-messages.patch [bz#1272523]
- kvm-ide-test-fix-failure-for-test_flush.patch [bz#1272523]
- kvm-vga-Remove-some-should-be-done-in-BIOS-comments.patch [bz#1331413]
- kvm-vga-fix-banked-access-bounds-checking-CVE-2016-xxxx.patch [bz#1331413]
- kvm-vga-add-vbe_enabled-helper.patch [bz#1331413]
- kvm-vga-factor-out-vga-register-setup.patch [bz#1331413]
- kvm-vga-update-vga-register-setup-on-vbe-changes.patch [bz#1331413]
- kvm-vga-make-sure-vga-register-setup-for-vbe-stays-intac.patch [bz#1331413]
- Resolves: bz#1272523
  (qemu-kvm build failure race condition in tests/ide-test)
- Resolves: bz#1331413
  (EMBARGOED CVE-2016-3710 qemu-kvm: qemu: incorrect banked access bounds checking in vga module [rhel-7.3])

* Mon Mar 14 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-109.el7
- kvm-e1000-eliminate-infinite-loops-on-out-of-bounds-tran.patch [bz#1296044]
- kvm-nbd-Always-call-close_fn-in-nbd_client_new.patch [bz#1285453]
- kvm-nbd-server-Coroutine-based-negotiation.patch [bz#1285453]
- kvm-nbd-client_close-on-error-in-nbd_co_client_start.patch [bz#1285453]
- kvm-Remove-libcacard-build.patch [bz#1314153]
- Resolves: bz#1285453
  (An NBD client can cause QEMU main loop to block when connecting to built-in NBD server)
- Resolves: bz#1296044
  (qemu-kvm: insufficient loop termination conditions in start_xmit() and e1000_receive() [rhel-7.3])
- Resolves: bz#1314153
  (Disable building of libcacard)

* Mon Feb 08 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-108.el7
- kvm-net-Make-qmp_query_rx_filter-with-name-argument-more.patch [bz#1269738]
- kvm-fw_cfg-add-check-to-validate-current-entry-value-CVE.patch [bz#1298048]
- Resolves: bz#1269738
  (Vlan table display repeat four times in qmp when queues=4)
- Resolves: bz#1298048
  (CVE-2016-1714 qemu-kvm: Qemu: nvram: OOB r/w access in processing firmware configurations [rhel-7.3])

* Wed Jan 20 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-107.el7
- kvm-raw-posix-Fix-.bdrv_co_get_block_status-for-unaligne.patch [bz#1283116]
- Resolves: bz#1283116
  ([abrt] qemu-img: get_block_status(): qemu-img killed by SIGABRT)

* Wed Jan 13 2016 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-106.el7
- kvm-ehci-clear-suspend-bit-on-detach.patch [bz#1268879]
- kvm-rbd-make-qemu-s-cache-setting-override-any-ceph-sett.patch [bz#1277248]
- kvm-rbd-fix-ceph-settings-precedence.patch [bz#1277248]
- kvm-target-i386-get-put-MSR_TSC_AUX-across-reset-and-mig.patch [bz#1265427]
- kvm-rtl8139-Fix-receive-buffer-overflow-check.patch [bz#1252757]
- kvm-rtl8139-Do-not-consume-the-packet-during-overflow-in.patch [bz#1252757]
- Resolves: bz#1252757
  ([RHEL-7.2-qmu-kvm] Package is 100% lost when ping from host to Win2012r2 guest with 64000 size)
- Resolves: bz#1265427
  (contents of MSR_TSC_AUX are not migrated)
- Resolves: bz#1268879
  (Camera stops work after remote-viewer re-connection [qemu-kvm])
- Resolves: bz#1277248
  (ceph.conf properties override qemu's command-line properties)

* Fri Oct 16 2015 Jeff E. Nelson <jen@redhat.com> - 1.5.3-105.el7
- kvm-qtest-ide-test-disable-flush-test.patch [bz#1270341]
- Resolves: bz#1270341
  (qemu-kvm build failure race condition in tests/ide-test)

* Wed Sep 23 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-104.el7
- kvm-qemu-iotests-Filter-qemu-io-output-in-025.patch [bz#1170974]
- Resolves: bz#1170974
  (test case 025 of qemu-iotests fail for raw with qemu-kvm-1.5.3-83.el7.x86_64)

* Thu Sep 10 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-103.el7
- kvm-Drop-superfluous-conditionals-around-g_strdup.patch [bz#1218919]
- kvm-util-Drop-superfluous-conditionals-around-g_free.patch [bz#1218919]
- kvm-util-Fuse-g_malloc-memset-into-g_new0.patch [bz#1218919]
- kvm-util-uri-uri_new-can-t-fail-drop-dead-error-handling.patch [bz#1218919]
- kvm-util-uri-realloc2n-can-t-fail-drop-dead-error-handli.patch [bz#1218919]
- kvm-util-uri-URI-member-path-can-be-null-compare-more-ca.patch [bz#1218919]
- kvm-util-uri-Add-overflow-check-to-rfc3986_parse_port.patch [bz#1218919]
- Resolves: bz#1218919
  (Coverity-detected defect: buffer overrun at uri.c:2035)

* Thu Sep 03 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-102.el7
- kvm-mc146818rtc-add-rtc-reset-reinjection-QMP-command.patch [bz#1191226]
- Resolves: bz#1191226
  (libvirt requires rtc-reset-reinjection command, backport it to RHEL7.1)

* Fri Aug 14 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-101.el7
- kvm-serial-reset-state-at-startup.patch [bz#922014]
- kvm-ide-Check-validity-of-logical-block-size.patch [bz#1134670]
- Resolves: bz#1134670
  (fail to specify the physical_block_size/logical_block_size value not 512 for IDE disk)
- Resolves: bz#922014
  (RFE: support hotplugging chardev & serial ports (Windows guests))

* Mon Aug 10 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-100.el7
- kvm-block-update-test-070-for-vhdx.patch [bz#1171576]
- kvm-block-coverity-fix-check-return-value-for-fcntl-in-g.patch [bz#1219217]
- Resolves: bz#1171576
  (test case 064 and 070 of qemu-iotests fail for vhdx with qemu-kvm-1.5.3-83.el7)
- Resolves: bz#1219217
  (Coverity-detected defect: call to fcntl without checking return value)

* Thu Aug 06 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-99.el7
- kvm-usb-ccid-add-missing-wakeup-calls.patch [bz#1243731]
- kvm-vpc-Handle-failure-for-potentially-large-allocations.patch [bz#1217349]
- kvm-block-vpc-prevent-overflow-if-max_table_entries-0x40.patch [bz#1217349]
- kvm-block-qemu-iotests-add-check-for-multiplication-over.patch [bz#1217349]
- kvm-virtio-scsi-use-virtqueue_map_sg-when-loading-reques.patch [bz#1249718]
- kvm-scsi-disk-fix-cmd.mode-field-typo.patch [bz#1249718]
- kvm-rtl8139-avoid-nested-ifs-in-IP-header-parsing-CVE-20.patch [bz#1248766]
- kvm-rtl8139-drop-tautologous-if-ip-.-statement-CVE-2015-.patch [bz#1248766]
- kvm-rtl8139-skip-offload-on-short-Ethernet-IP-header-CVE.patch [bz#1248766]
- kvm-rtl8139-check-IP-Header-Length-field-CVE-2015-5165.patch [bz#1248766]
- kvm-rtl8139-check-IP-Total-Length-field-CVE-2015-5165.patch [bz#1248766]
- kvm-rtl8139-skip-offload-on-short-TCP-header-CVE-2015-51.patch [bz#1248766]
- kvm-rtl8139-check-TCP-Data-Offset-field-CVE-2015-5165.patch [bz#1248766]
- Resolves: bz#1217349
  (qemu-img vpc driver segfault)
- Resolves: bz#1243731
  (smart card emulation doesn't work with USB3 (nec-xhci) controller)
- Resolves: bz#1248766
  (CVE-2015-5165 qemu-kvm: Qemu: rtl8139 uninitialized heap memory information leakage to guest [rhel-7.2])
- Resolves: bz#1249718
  (Segfault occurred at Dst VM while completed migration upon ENOSPC)

* Fri Jul 24 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-98.el7
- kvm-block-curl-Don-t-lose-original-error-when-a-connecti.patch [bz#1235812]
- kvm-vfio-pci-Add-pba_offset-PCI-quirk-for-Chelsio-T5-dev.patch [bz#1244347]
- kvm-block-Print-its-file-name-if-backing-file-opening-fa.patch [bz#1238639]
- kvm-block-Propagate-error-in-bdrv_img_create.patch [bz#1238639]
- kvm-iotests-Add-test-for-non-existing-backing-file.patch [bz#1238639]
- Resolves: bz#1235812
  (block/curl: Fix generic "Input/output error" on failure)
- Resolves: bz#1238639
  (qemu-img shows error message for backing file twice)
- Resolves: bz#1244347
  (Quirk for Chelsio T5 MSI-X PBA)

* Fri Jul 17 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-97.el7
- kvm-ide-Check-array-bounds-before-writing-to-io_buffer-C.patch [bz#1243690]
- kvm-ide-atapi-Fix-START-STOP-UNIT-command-completion.patch [bz#1243690]
- kvm-ide-Clear-DRQ-after-handling-all-expected-accesses.patch [bz#1243690]
- Resolves: bz#1243690
  (EMBARGOED CVE-2015-5154 qemu-kvm: qemu: ide: atapi: heap overflow during I/O buffer memory access [rhel-7.2])

* Thu Jul 16 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-96.el7
- kvm-ahci.c-mask-unused-flags-when-reading-size-PRDT-DBC.patch [bz#1205100]
- kvm-ide-Correct-handling-of-malformed-short-PRDTs.patch [bz#1205100]
- Resolves: bz#1205100
  (qemu-kvm: Qemu: PRDT overflow from guest to host [rhel-7.2])

* Tue Jul 07 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-95.el7
- kvm-i8254-fix-out-of-bounds-memory-access-in-pit_ioport_.patch [bz#1229646]
- kvm-target-i386-fix-cpuid-leaf-0x0d.patch [bz#1233350]
- kvm-target-i386-Intel-MPX.patch [bz#1233350]
- kvm-always-update-the-MPX-model-specific-register.patch [bz#1233350]
- kvm-target-i386-bugfix-of-Intel-MPX.patch [bz#1233350]
- kvm-target-i386-fix-set-of-registers-zeroed-on-reset.patch [bz#1233350]
- kvm-target-i386-Add-mpx-CPU-feature-name.patch [bz#1233350]
- kvm-target-i386-Avoid-shifting-left-into-sign-bit.patch [bz#1233350]
- kvm-target-i386-add-Intel-AVX-512-support.patch [bz#1233350]
- kvm-configure-Add-support-for-tcmalloc.patch [bz#1213881]
- Resolves: bz#1213881
  (enable using tcmalloc for memory allocation in qemu-kvm)
- Resolves: bz#1229646
  (CVE-2015-3214 qemu-kvm: qemu: i8254: out-of-bounds memory access in pit_ioport_read function [rhel-7.2])
- Resolves: bz#1233350
  ([Intel 7.2 FEAT] Expose MPX feature to guest - qemu-kvm)

* Fri Jun 26 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-94.el7
- kvm-qcow2-Put-cache-reference-in-error-case.patch [bz#1129893]
- kvm-qcow2-Catch-bdrv_getlength-error.patch [bz#1129893]
- kvm-block-Introduce-qemu_try_blockalign.patch [bz#1129893]
- kvm-qcow2-Catch-host_offset-for-data-allocation.patch [bz#1129893]
- kvm-iotests-Add-test-for-image-header-overlap.patch [bz#1129893]
- kvm-block-Catch-bs-drv-in-bdrv_check.patch [bz#1129893]
- kvm-qapi-block-Add-fatal-to-BLOCK_IMAGE_CORRUPTED.patch [bz#1129893]
- kvm-qcow2-Add-qcow2_signal_corruption.patch [bz#1129893]
- kvm-qcow2-Use-qcow2_signal_corruption-for-overlaps.patch [bz#1129893]
- kvm-qcow2-Check-L1-L2-reftable-entries-for-alignment.patch [bz#1129893]
- kvm-iotests-Add-more-tests-for-qcow2-corruption.patch [bz#1129893]
- kvm-qcow2-fix-leak-of-Qcow2DiscardRegion-in-update_refco.patch [bz#1129893]
- kvm-qcow2-Do-not-overflow-when-writing-an-L1-sector.patch [bz#1129893]
- kvm-iotests-Add-test-for-qcow2-L1-table-update.patch [bz#1129893]
- kvm-block-Add-qemu_-try_-blockalign0.patch [bz#1129893]
- kvm-qcow2-Calculate-refcount-block-entry-count.patch [bz#1129893]
- kvm-qcow2-Fix-leaks-in-dirty-images.patch [bz#1129893]
- kvm-qcow2-Split-qcow2_check_refcounts.patch [bz#1129893]
- kvm-qcow2-Use-sizeof-refcount_table.patch [bz#1129893]
- kvm-qcow2-Pull-check_refblocks-up.patch [bz#1129893]
- kvm-qcow2-Use-int64_t-for-in-memory-reftable-size.patch [bz#1129893]
- kvm-qcow2-Split-fail-code-in-L1-and-L2-checks.patch [bz#1129893]
- kvm-qcow2-Let-inc_refcounts-return-errno.patch [bz#1129893]
- kvm-qcow2-Let-inc_refcounts-resize-the-reftable.patch [bz#1129893]
- kvm-qcow2-Reuse-refcount-table-in-calculate_refcounts.patch [bz#1129893]
- kvm-qcow2-Fix-refcount-blocks-beyond-image-end.patch [bz#1129893]
- kvm-qcow2-Do-not-perform-potentially-damaging-repairs.patch [bz#1129893]
- kvm-qcow2-Rebuild-refcount-structure-during-check.patch [bz#1129893]
- kvm-qcow2-Clean-up-after-refcount-rebuild.patch [bz#1129893]
- kvm-iotests-Fix-test-outputs.patch [bz#1129893]
- kvm-iotests-Add-test-for-potentially-damaging-repairs.patch [bz#1129893]
- kvm-qcow2-Drop-REFCOUNT_SHIFT.patch [bz#1129893]
- kvm-block-Respect-underlying-file-s-EOF.patch [bz#1129893]
- kvm-qcow2-Fix-header-extension-size-check.patch [bz#1129893]
- kvm-qcow2.py-Add-required-padding-for-header-extensions.patch [bz#1129893]
- kvm-block-Don-t-probe-for-unknown-backing-file-format.patch [bz#1129893]
- kvm-qcow2-Add-two-more-unalignment-checks.patch [bz#1129893]
- kvm-iotests-Add-tests-for-more-corruption-cases.patch [bz#1129893]
- kvm-qcow2-Respect-new_block-in-alloc_refcount_block.patch [bz#1129893]
- kvm-iotests-Add-tests-for-refcount-table-growth.patch [bz#1129893]
- kvm-qcow2-Fix-header-update-with-overridden-backing-file.patch [bz#1129893]
- kvm-qcow2-Flush-pending-discards-before-allocating-clust.patch [bz#1129893]
- Resolves: bz#1129893
  (Backport additional qcow2 corruption prevention and image repair patches)

* Wed Jun 24 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-93.el7
- kvm-atomics-add-explicit-compiler-fence-in-__atomic-memo.patch [bz#1142857 bz#1142857 (aka bz#8*bz#10^bz#6/bz#7)]
- Resolves: bz#1142857
  ([abrt] qemu-kvm: bdrv_error_action(): qemu-kvm killed by SIGABRT)
- Resolves: bz#8*10^6/7)
  (XFree86 apparently sets xhost to ill inital values)
- Resolves: bz#(aka
  ()

* Tue Jun 16 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-92.el7
- kvm-seccomp-add-timerfd_create-and-timerfd_settime-to-th.patch [bz#1185737]
- kvm-qdict-Add-qdict_join.patch [bz#1226697]
- kvm-block-Allow-JSON-filenames.patch [bz#1226697]
- kvm-spice-display-fix-segfault-in-qemu_spice_create_upda.patch [bz#1230808]
- Resolves: bz#1185737
  (qemu-kvm hang when boot with usb-host and sandbox was enabled)
- Resolves: bz#1226697
  ([virt-v2v] Allow json: filenames in qemu-img)
- Resolves: bz#1230808
  ([abrt] qemu-system-x86: __memcmp_sse4_1(): qemu-system-x86_64 killed by SIGSEGV)

* Mon Jun 15 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-91.el7
- kvm-vmdk-Fix-overflow-if-l1_size-is-0x20000000.patch [bz#1217351]
- kvm-block-ssh-Drop-superfluous-libssh2_session_last_errn.patch [bz#1226683]
- kvm-block-ssh-Propagate-errors-through-check_host_key.patch [bz#1226683]
- kvm-block-ssh-Propagate-errors-through-authenticate.patch [bz#1226683]
- kvm-block-ssh-Propagate-errors-through-connect_to_ssh.patch [bz#1226683]
- kvm-block-ssh-Propagate-errors-to-open-and-create-method.patch [bz#1226683]
- kvm-ssh-Don-t-crash-if-either-host-or-path-is-not-specif.patch [bz#1226683]
- kvm-curl-Replaced-old-error-handling-with-error-reportin.patch [bz#1226684]
- kvm-curl-Fix-long-line.patch [bz#1226684]
- kvm-curl-Remove-unnecessary-use-of-goto.patch [bz#1226684]
- kvm-curl-Fix-return-from-curl_read_cb-with-invalid-state.patch [bz#1226684]
- kvm-curl-Remove-erroneous-sleep-waiting-for-curl-complet.patch [bz#1226684]
- kvm-curl-Whitespace-only-changes.patch [bz#1226684]
- kvm-block-curl-Implement-the-libcurl-timer-callback-inte.patch [bz#1226684]
- kvm-curl-Remove-unnecessary-explicit-calls-to-internal-e.patch [bz#1226684]
- kvm-curl-Eliminate-unnecessary-use-of-curl_multi_socket_.patch [bz#1226684]
- kvm-curl-Ensure-all-informationals-are-checked-for-compl.patch [bz#1226684]
- kvm-curl-Fix-hang-reading-from-slow-connections.patch [bz#1226684]
- kvm-curl-Fix-build-when-curl_multi_socket_action-isn-t-a.patch [bz#1226684]
- kvm-curl-Remove-broken-parsing-of-options-from-url.patch [bz#1226684]
- kvm-curl-refuse-to-open-URL-from-HTTP-server-without-ran.patch [bz#1226684]
- kvm-curl-Add-sslverify-option.patch [bz#1226684]
- kvm-block-Drop-superfluous-conditionals-around-g_free.patch [bz#1226684]
- kvm-curl-Handle-failure-for-potentially-large-allocation.patch [bz#1226684]
- kvm-block.curl-adding-timeout-option.patch [bz#1226684]
- kvm-curl-Allow-a-cookie-or-cookies-to-be-sent-with-http-.patch [bz#1226684]
- kvm-curl-The-macro-that-you-have-to-uncomment-to-get-deb.patch [bz#1226684]
- kvm-block-curl-Improve-type-safety-of-s-timeout.patch [bz#1226684]
- kvm-Enable-ssh-driver-read-only.patch [bz#1226683]
- kvm-Enable-curl-driver-read-only.patch [bz#1226684]
- Resolves: bz#1217351
  (Overflow in malloc size calculation in VMDK driver)
- Resolves: bz#1226683
  ([virt-v2v] Backport upstream ssh driver to qemu-kvm)
- Resolves: bz#1226684
  ([virt-v2v] Enable curl driver + upstream features + fixes in qemu-kvm and enable https)

* Thu Jun 04 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-90.el7
- kvm-qcow2-Pass-discard-type-to-qcow2_discard_clusters.patch [bz#1208808]
- kvm-qcow2-Discard-VM-state-in-active-L1-after-creating-s.patch [bz#1208808]
- kvm-configure-Require-libfdt-for-arm-ppc-microblaze-soft.patch [bz#1217850]
- kvm-configure-Add-handling-code-for-AArch64-targets.patch [bz#1217850]
- kvm-configure-permit-compilation-on-arm-aarch64.patch [bz#1217850]
- kvm-spec-Allow-build-on-aarch64.patch [bz#1217850]
- kvm-Remove-redhat-extensions-from-qmp-events.txt.patch [bz#1222833]
- kvm-spec-Add-misssing-QMP-documentation-files.patch [bz#1222833]
- Resolves: bz#1208808
  (creating second and further snapshot takes ages)
- Resolves: bz#1217850
  (qemu-kvm: Enable build on aarch64)
- Resolves: bz#1222833
  (We ship incomplete QMP documentation)

* Wed May 27 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-89.el7
- kvm-CVE-2015-1779-incrementally-decode-websocket-frames.patch [bz#1206497]
- kvm-CVE-2015-1779-limit-size-of-HTTP-headers-from-websoc.patch [bz#1206497]
- kvm-qemu-iotests-Test-unaligned-4k-zero-write.patch [bz#1200295]
- kvm-block-Fix-NULL-deference-for-unaligned-write-if-qiov.patch [bz#1200295]
- kvm-qemu-iotests-Test-unaligned-sub-block-zero-write.patch [bz#1200295]
- kvm-fdc-force-the-fifo-access-to-be-in-bounds-of-the-all.patch [bz#1219270]
- Resolves: bz#1200295
  (QEMU segfault when doing unaligned zero write to non-512 disk)
- Resolves: bz#1206497
  (CVE-2015-1779 qemu-kvm: qemu: vnc: insufficient resource limiting in VNC websockets decoder [rhel-7.2])
- Resolves: bz#1219270
  (CVE-2015-3456 qemu-kvm: qemu: floppy disk controller flaw [rhel-7.2])

* Wed May 06 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-88.el7
- kvm-vfio-warn-if-host-device-rom-can-t-be-read.patch [bz#1210503]
- kvm-vfio-Do-not-reattempt-a-failed-rom-read.patch [bz#1210503]
- kvm-vfio-Correction-in-vfio_rom_read-when-attempting-rom.patch [bz#1210503]
- kvm-vfio-Fix-overrun-after-readlink-fills-buffer-complet.patch [bz#1210504]
- kvm-vfio-use-correct-runstate.patch [bz#1210505]
- kvm-vfio-pci-Fix-BAR-size-overflow.patch [bz#1181267]
- kvm-vfio-Use-vfio-type1-v2-IOMMU-interface.patch [bz#1210508]
- kvm-vfio-pci-Enable-device-request-notification-support.patch [bz#1210509]
- kvm-vfio-pci-Further-fix-BAR-size-overflow.patch [bz#1181267]
- kvm-vfio-pci-Fix-error-path-sign.patch [bz#1210504]
- kvm-x86-Use-common-variable-range-MTRR-counts.patch [bz#1210510]
- kvm-x86-kvm-Add-MTRR-support-for-kvm_get-put_msrs.patch [bz#1210510]
- kvm-x86-Clear-MTRRs-on-vCPU-reset.patch [bz#1210510]
- kvm-spec-Exclude-aarch64.patch [bz#1217850]
- Resolves: bz#1181267
  (vfio-pci: Fix BAR size overflow)
- Resolves: bz#1210503
  (vfio improve PCI ROM loading error handling)
- Resolves: bz#1210504
  (vfio: Fix overrun after readlink() fills buffer completely)
- Resolves: bz#1210505
  (vfio: use correct runstate)
- Resolves: bz#1210508
  (vfio: Use vfio type1 v2 IOMMU interface)
- Resolves: bz#1210509
  (vfio-pci: Enable device request notification support)
- Resolves: bz#1210510
  (Sync MTRRs with KVM and disable on reset)
- Resolves: bz#1217850
  (qemu-kvm: ExcludeArch: aarch64)

* Tue Mar 17 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-87.el7
- kvm-trace-add-qemu_system_powerdown_request-and-qemu_sys.patch [bz#1155671]
- kvm-virtio-net-drop-assert-on-vm-stop.patch [bz#1139562]
- kvm-socket-shutdown.patch [bz#1086168]
- kvm-Handle-bi-directional-communication-for-fd-migration.patch [bz#1086168]
- kvm-migration_cancel-shutdown-migration-socket.patch [bz#1086168]
- kvm-iscsi-Refuse-to-open-as-writable-if-the-LUN-is-write.patch [bz#1032412]
- kvm-main-set-current_machine-before-calling-machine-init.patch [bz#1176283]
- kvm-pc_sysfw-prevent-pflash-and-or-mis-sized-firmware-fo.patch [bz#1176283]
- kvm-Restore-atapi_dma-flag-across-migration.patch [bz#892258]
- kvm-atapi-migration-Throw-recoverable-error-to-avoid-rec.patch [bz#892258]
- kvm-build-reenable-local-builds-to-pass-enable-debug-RHE.patch []
- kvm-raw-posix-Fail-gracefully-if-no-working-alignment-is.patch [bz#1184363]
- kvm-block-Add-Error-argument-to-bdrv_refresh_limits.patch [bz#1184363]
- kvm-Python-lang-gdb-script-to-extract-x86_64-guest-vmcor.patch [bz#828493]
- kvm-RPM-spec-install-dump-guest-memory.py-RHEL-only.patch [bz#828493]
- kvm-spec-Enable-build-of-qemu-img-and-libcacard-for-ppc6.patch [bz#1190086]
- Resolves: bz#1032412
  (opening read-only iscsi lun as read-write should fail)
- Resolves: bz#1086168
  (qemu-kvm can not cancel migration in src host when network of dst host failed)
- Resolves: bz#1139562
  (qemu-kvm with vhost=off and sndbuf=100 crashed when stop it during pktgen test from guest to host)
- Resolves: bz#1155671
  ([Fujitsu 7.2 FEAT]: QEMU: Add tracepoints in system shutdown)
- Resolves: bz#1176283
  ([migration]migration failed when configure guest with OVMF bios + machine type=rhel6.5.0)
- Resolves: bz#1184363
  (Qemu process fails to start with a multipath device with all paths failed)
- Resolves: bz#1190086
  (build qemu-img/libcacard on ppc64le for 7.2)
- Resolves: bz#828493
  ([Hitachi 7.2 FEAT] Extract guest memory dump from qemu-kvm core)
- Resolves: bz#892258
  (ide CDROM io/data errors after migration)

* Thu Mar 05 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-86.el7_1.1
- kvm-pc-add-rhel6.6.0-machine-type.patch [bz#1198958]
- Resolves: bz#1198958
  (Add rhel-6.6.0 machine type to RHEL 7.1.z to support RHEL 6.6 to RHEL 7.1 live migration)

* Sun Jan 25 2015 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-86.el7
- kvm-vfio-pci-Fix-interrupt-disabling.patch [bz#1180942]
- kvm-cirrus-fix-blit-region-check.patch [bz#1169456]
- kvm-cirrus-don-t-overflow-CirrusVGAState-cirrus_bltbuf.patch [bz#1169456]
- Resolves: bz#1169456
  (CVE-2014-8106 qemu-kvm: qemu: cirrus: insufficient blit region checks [rhel-7.1])
- Resolves: bz#1180942
  (qemu core dumped when unhotplug gpu card assigned to guest)

* Wed Jan 07 2015 Jeff E. Nelson <jen@redhat.com> - 1.5.3-85.el7
- kvm-block-delete-cow-block-driver.patch [bz#1175325]
- Resolves: bz#1175325
  (Delete cow block driver)

* Tue Dec 16 2014 Jeff E. Nelson <jen@redhat.com> - 1.5.3-84.el7
- kvm-qemu-iotests-Test-case-for-backing-file-deletion.patch [bz#1002493]
- kvm-qemu-iotests-Add-sample-image-and-test-for-VMDK-vers.patch [bz#1134237]
- kvm-vmdk-Check-VMFS-extent-line-field-number.patch [bz#1134237]
- kvm-qemu-iotests-Introduce-_unsupported_imgopts.patch [bz#1002493]
- kvm-qemu-iotests-Add-_unsupported_imgopts-for-vmdk-subfo.patch [bz#1002493]
- kvm-vmdk-Fix-big-flat-extent-IO.patch [bz#1134241]
- kvm-vmdk-Check-for-overhead-when-opening.patch [bz#1134251]
- kvm-block-vmdk-add-basic-.bdrv_check-support.patch [bz#1134251]
- kvm-qemu-iotest-Make-077-raw-only.patch [bz#1134237]
- kvm-qemu-iotests-Don-t-run-005-on-vmdk-split-formats.patch [bz#1002493]
- kvm-vmdk-extract-vmdk_read_desc.patch [bz#1134251]
- kvm-vmdk-push-vmdk_read_desc-up-to-caller.patch [bz#1134251]
- kvm-vmdk-do-not-try-opening-a-file-as-both-image-and-des.patch [bz#1134251]
- kvm-vmdk-correctly-propagate-errors.patch [bz#1134251]
- kvm-block-vmdk-do-not-report-file-offset-for-compressed-.patch [bz#1134251]
- kvm-vmdk-Fix-d-and-lld-to-PRI-in-format-strings.patch [bz#1134251]
- kvm-vmdk-Fix-x-to-PRIx32-in-format-strings-for-cid.patch [bz#1134251]
- kvm-qemu-img-Convert-by-cluster-size-if-target-is-compre.patch [bz#1134283]
- kvm-vmdk-Implement-.bdrv_write_compressed.patch [bz#1134283]
- kvm-vmdk-Implement-.bdrv_get_info.patch [bz#1134283]
- kvm-qemu-iotests-Test-converting-to-streamOptimized-from.patch [bz#1134283]
- kvm-vmdk-Fix-local_err-in-vmdk_create.patch [bz#1134283]
- kvm-fpu-softfloat-drop-INLINE-macro.patch [bz#1002493]
- kvm-block-New-bdrv_nb_sectors.patch [bz#1002493]
- kvm-vmdk-Optimize-cluster-allocation.patch [bz#1002493]
- kvm-vmdk-Handle-failure-for-potentially-large-allocation.patch [bz#1002493]
- kvm-vmdk-Use-bdrv_nb_sectors-where-sectors-not-bytes-are.patch [bz#1002493]
- kvm-vmdk-fix-vmdk_parse_extents-extent_file-leaks.patch [bz#1002493]
- kvm-vmdk-fix-buf-leak-in-vmdk_parse_extents.patch [bz#1002493]
- kvm-vmdk-Fix-integer-overflow-in-offset-calculation.patch [bz#1002493]
- kvm-migration-fix-parameter-validation-on-ram-load-CVE-2.patch [bz#1163078]
- Resolves: bz#1002493
  (qemu-img convert rate about 100k/second from qcow2/raw to vmdk format on nfs system file)
- Resolves: bz#1134237
  (Opening malformed VMDK description file should fail)
- Resolves: bz#1134241
  (QEMU fails to correctly read/write on VMDK with big flat extent)
- Resolves: bz#1134251
  (Opening an obviously truncated VMDK image should fail)
- Resolves: bz#1134283
  (qemu-img convert from ISO to streamOptimized fails)
- Resolves: bz#1163078
  (CVE-2014-7840 qemu-kvm: qemu: insufficient parameter validation during ram load [rhel-7.1])

* Thu Nov 27 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-83.el7
- kvm-xhci-add-sanity-checks-to-xhci_lookup_uport.patch [bz#1074219]
- kvm-Revert-Build-ceph-rbd-only-for-rhev.patch [bz#1140742]
- kvm-Revert-rbd-Only-look-for-qemu-specific-copy-of-librb.patch [bz#1140742]
- kvm-Revert-rbd-link-and-load-librbd-dynamically.patch [bz#1140742]
- kvm-spec-Enable-rbd-driver-add-dependency.patch [bz#1140742]
- Resolves: bz#1074219
  (qemu core dump when install a RHEL.7 guest(xhci) with migration)
- Resolves: bz#1140742
  (Enable native support for Ceph)

* Tue Nov 25 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-82.el7
- kvm-hw-pci-fixed-error-flow-in-pci_qdev_init.patch [bz#1046007]
- kvm-hw-pci-fixed-hotplug-crash-when-using-rombar-0-with-.patch [bz#1046007]
- Resolves: bz#1046007
  (qemu-kvm aborted when hot plug PCI device to guest with romfile and rombar=0)

* Fri Nov 21 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-81.el7
- kvm-migration-static-variables-will-not-be-reset-at-seco.patch [bz#1071776]
- kvm-vfio-pci-Add-debug-config-options-to-disable-MSI-X-K.patch [bz#1098976]
- kvm-vfio-correct-debug-macro-typo.patch [bz#1098976]
- kvm-vfio-pci-Fix-MSI-X-debug-code.patch [bz#1098976]
- kvm-vfio-pci-Fix-MSI-X-masking-performance.patch [bz#1098976]
- kvm-vfio-Fix-MSI-X-vector-expansion.patch [bz#1098976]
- kvm-vfio-Don-t-cache-MSIMessage.patch [bz#1098976]
- Resolves: bz#1071776
  (Migration "expected downtime" does not refresh after reset to a new value)
- Resolves: bz#1098976
  (2x RHEL 5.10 VM running on RHEL 7 KVM have low TCP_STREAM throughput)

* Fri Nov 21 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-80.el7
- kvm-dump-RHEL-specific-fix-for-CPUState-bug-introduced-b.patch [bz#1161563]
- kvm-dump-guest-memory-Check-for-the-correct-return-value.patch [bz#1157798]
- kvm-dump-const-qualify-the-buf-of-WriteCoreDumpFunction.patch [bz#1157798]
- kvm-dump-add-argument-to-write_elfxx_notes.patch [bz#1157798]
- kvm-dump-add-API-to-write-header-of-flatten-format.patch [bz#1157798]
- kvm-dump-add-API-to-write-vmcore.patch [bz#1157798]
- kvm-dump-add-API-to-write-elf-notes-to-buffer.patch [bz#1157798]
- kvm-dump-add-support-for-lzo-snappy.patch [bz#1157798]
- kvm-RPM-spec-build-qemu-kvm-with-lzo-and-snappy-enabled-.patch [bz#1157798]
- kvm-dump-add-members-to-DumpState-and-init-some-of-them.patch [bz#1157798]
- kvm-dump-add-API-to-write-dump-header.patch [bz#1157798]
- kvm-dump-add-API-to-write-dump_bitmap.patch [bz#1157798]
- kvm-dump-add-APIs-to-operate-DataCache.patch [bz#1157798]
- kvm-dump-add-API-to-write-dump-pages.patch [bz#1157798]
- kvm-dump-Drop-qmp_dump_guest_memory-stub-and-build-for-a.patch [bz#1157798]
- kvm-dump-make-kdump-compressed-format-available-for-dump.patch [bz#1157798]
- kvm-Define-the-architecture-for-compressed-dump-format.patch [bz#1157798]
- kvm-dump-add-query-dump-guest-memory-capability-command.patch [bz#1157798]
- kvm-dump-Drop-pointless-error_is_set-DumpState-member-er.patch [bz#1157798]
- kvm-dump-fill-in-the-flat-header-signature-more-pleasing.patch [bz#1157798]
- kvm-dump-simplify-write_start_flat_header.patch [bz#1157798]
- kvm-dump-eliminate-DumpState.page_shift-guest-s-page-shi.patch [bz#1157798]
- kvm-dump-eliminate-DumpState.page_size-guest-s-page-size.patch [bz#1157798]
- kvm-dump-select-header-bitness-based-on-ELF-class-not-EL.patch [bz#1157798]
- kvm-dump-hoist-lzo_init-from-get_len_buf_out-to-dump_ini.patch [bz#1157798]
- kvm-dump-simplify-get_len_buf_out.patch [bz#1157798]
- kvm-rename-parse_enum_option-to-qapi_enum_parse-and-make.patch [bz#1087724]
- kvm-qapi-introduce-PreallocMode-and-new-PreallocModes-fu.patch [bz#1087724]
- kvm-raw-posix-Add-falloc-and-full-preallocation-option.patch [bz#1087724]
- kvm-qcow2-Add-falloc-and-full-preallocation-option.patch [bz#1087724]
- kvm-vga-fix-invalid-read-after-free.patch [bz#1161890]
- kvm-Use-qemu-kvm-in-documentation-instead-of-qemu-system.patch [bz#1140618]
- kvm-vnc-sanitize-bits_per_pixel-from-the-client.patch [bz#1157645]
- kvm-spice-call-qemu_spice_set_passwd-during-init.patch [bz#1138639]
- kvm-block-raw-posix-Try-both-FIEMAP-and-SEEK_HOLE.patch [bz#1160237]
- kvm-block-raw-posix-Fix-disk-corruption-in-try_fiemap.patch [bz#1160237]
- kvm-block-raw-posix-use-seek_hole-ahead-of-fiemap.patch [bz#1160237]
- kvm-raw-posix-Fix-raw_co_get_block_status-after-EOF.patch [bz#1160237]
- kvm-raw-posix-raw_co_get_block_status-return-value.patch [bz#1160237]
- kvm-raw-posix-SEEK_HOLE-suffices-get-rid-of-FIEMAP.patch [bz#1160237]
- kvm-raw-posix-The-SEEK_HOLE-code-is-flawed-rewrite-it.patch [bz#1160237]
- Resolves: bz#1087724
  ([Fujitsu 7.1 FEAT]: qemu-img should use fallocate() system call for "preallocation=full" option)
- Resolves: bz#1138639
  (fail to login spice session with password + expire time)
- Resolves: bz#1140618
  (Should replace "qemu-system-i386" by "/usr/libexec/qemu-kvm" in manpage of qemu-kvm for our official qemu-kvm build)
- Resolves: bz#1157645
  (CVE-2014-7815 qemu-kvm: qemu: vnc: insufficient bits_per_pixel from the client sanitization [rhel-7.1])
- Resolves: bz#1157798
  ([FEAT RHEL7.1]: qemu: Support compression for dump-guest-memory command)
- Resolves: bz#1160237
  (qemu-img convert intermittently corrupts output images)
- Resolves: bz#1161563
  (invalid QEMU NOTEs in vmcore that is dumped for multi-VCPU guests)
- Resolves: bz#1161890
  ([abrt] qemu-kvm: pixman_image_get_data(): qemu-kvm killed by SIGSEGV)

* Wed Nov 12 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-79.el7
- kvm-libcacard-link-against-qemu-error.o-for-error_report.patch [bz#1088176]
- kvm-error-Add-error_abort.patch [bz#1088176]
- kvm-blockdev-Fail-blockdev-add-with-encrypted-images.patch [bz#1088176]
- kvm-blockdev-Fix-NULL-pointer-dereference-in-blockdev-ad.patch [bz#1088176]
- kvm-qemu-iotests-Test-a-few-blockdev-add-error-cases.patch [bz#1088176]
- kvm-block-Add-errp-to-bdrv_new.patch [bz#1088176]
- kvm-qemu-img-Avoid-duplicate-block-device-IDs.patch [bz#1088176]
- kvm-block-Catch-duplicate-IDs-in-bdrv_new.patch [bz#1088176]
- kvm-qemu-img-Allow-source-cache-mode-specification.patch [bz#1138691]
- kvm-qemu-img-Allow-cache-mode-specification-for-amend.patch [bz#1138691]
- kvm-qemu-img-clarify-src_cache-option-documentation.patch [bz#1138691]
- kvm-qemu-img-fix-rebase-src_cache-option-documentation.patch [bz#1138691]
- kvm-qemu-img-fix-img_compare-flags-error-path.patch [bz#1138691]
- kvm-ac97-register-reset-via-qom.patch [bz#1141667]
- kvm-virtio-blk-Factor-common-checks-out-of-virtio_blk_ha.patch [bz#1085232]
- kvm-virtio-blk-Bypass-error-action-and-I-O-accounting-on.patch [bz#1085232]
- kvm-virtio-blk-Treat-read-write-beyond-end-as-invalid.patch [bz#1085232]
- kvm-ide-Treat-read-write-beyond-end-as-invalid.patch [bz#1085232]
- kvm-ide-only-constrain-read-write-requests-to-drive-size.patch [bz#1085232]
- Resolves: bz#1085232
  (Ilegal guest requests on block devices pause the VM)
- Resolves: bz#1088176
  (QEMU fail to check whether duplicate ID for block device drive using 'blockdev-add' to hotplug)
- Resolves: bz#1138691
  (Allow qemu-img to bypass the host cache (check, compare, convert, rebase, amend))
- Resolves: bz#1141667
  (Qemu crashed if reboot guest after hot remove AC97 sound device)

* Mon Nov 10 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-78.el7
- kvm-slirp-udp-fix-NULL-pointer-dereference-because-of-un.patch [bz#1144820]
- kvm-hw-pci-fix-error-flow-in-pci-multifunction-init.patch [bz#1049734]
- kvm-rhel-Drop-machine-type-pc-q35-rhel7.0.0.patch [bz#1111107]
- kvm-virtio-scsi-Plug-memory-leak-on-virtio_scsi_push_eve.patch [bz#1088822]
- kvm-virtio-scsi-Report-error-if-num_queues-is-0-or-too-l.patch [bz#1089606]
- kvm-virtio-scsi-Fix-memory-leak-when-realize-failed.patch [bz#1089606]
- kvm-virtio-scsi-Fix-num_queue-input-validation.patch [bz#1089606]
- kvm-Revert-linux-aio-use-event-notifiers.patch [bz#1104748]
- kvm-specfile-Require-glusterfs-api-3.6.patch [bz#1155518]
- Resolves: bz#1049734
  (PCI: QEMU crash on illegal operation: attaching a function to a non multi-function device)
- Resolves: bz#1088822
  (hot-plug a virtio-scsi disk via 'blockdev-add' always cause QEMU quit)
- Resolves: bz#1089606
  (QEMU will not reject invalid number of queues (num_queues = 0) specified for virtio-scsi)
- Resolves: bz#1104748
  (48% reduction in IO performance for KVM guest, io=native)
- Resolves: bz#1111107
  (Remove Q35 machine type from qemu-kvm)
- Resolves: bz#1144820
  (CVE-2014-3640 qemu-kvm: qemu: slirp: NULL pointer deref in sosendto() [rhel-7.1])
- Resolves: bz#1155518
  (qemu-kvm: undefined symbol: glfs_discard_async)

* Fri Oct 24 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-77.el7
- kvm-seccomp-add-semctl-to-the-syscall-whitelist.patch [bz#1026314]
- kvm-Revert-kvmclock-Ensure-proper-env-tsc-value-for-kvmc.patch [bz#1098602 bz#1130428]
- kvm-Revert-kvmclock-Ensure-time-in-migration-never-goes-.patch [bz#1098602 bz#1130428]
- kvm-Introduce-cpu_clean_all_dirty.patch [bz#1098602 bz#1130428]
- kvm-kvmclock-Ensure-proper-env-tsc-value-for-kvmclock.v2.patch [bz#1098602 bz#1130428]
- kvm-kvmclock-Ensure-time-in-migration-never-goes-back.v2.patch [bz#1098602 bz#1130428]
- Resolves: bz#1026314
  (BUG: qemu-kvm hang when use '-sandbox on'+'vnc'+'hda')
- Resolves: bz#1098602
  (kvmclock: Ensure time in migration never goes backward (backport))
- Resolves: bz#1130428
  (After migration of RHEL7.1 guest with "-vga qxl", GUI console is hang)

* Tue Oct 21 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-76.el7
- kvm-usb-hcd-xhci-QOM-Upcast-Sweep.patch [bz#980747]
- kvm-usb-hcd-xhci-QOM-parent-field-cleanup.patch [bz#980747]
- kvm-uhci-egsm-fix.patch [bz#1046873]
- kvm-usb-redir-fix-use-after-free.patch [bz#1046574 bz#1088116]
- kvm-xhci-remove-leftover-debug-printf.patch [bz#980833]
- kvm-xhci-add-tracepoint-for-endpoint-state-changes.patch [bz#980833]
- kvm-xhci-add-port-to-slot_address-tracepoint.patch [bz#980833]
- kvm-usb-parallelize-usb3-streams.patch [bz#1075846]
- kvm-xhci-Init-a-transfers-xhci-slotid-and-epid-member-on.patch [bz#1075846]
- kvm-xhci-Add-xhci_epid_to_usbep-helper-function.patch [bz#980833]
- kvm-xhci-Fix-memory-leak-on-xhci_disable_ep.patch [bz#980833]
- kvm-usb-Also-reset-max_packet_size-on-ep_reset.patch [bz#1075846]
- kvm-usb-Fix-iovec-memleak-on-combined-packet-free.patch [bz#1075846]
- kvm-usb-hcd-xhci-Remove-unused-sstreamsm-member-from-XHC.patch [bz#980747]
- kvm-usb-hcd-xhci-Remove-unused-cancelled-member-from-XHC.patch [bz#980747]
- kvm-usb-hcd-xhci-Report-completion-of-active-transfer-wi.patch [bz#980747]
- kvm-usb-hcd-xhci-Update-endpoint-context-dequeue-pointer.patch [bz#980747]
- kvm-xhci-Add-a-few-missing-checks-for-disconnected-devic.patch [bz#980833]
- kvm-usb-Add-max_streams-attribute-to-endpoint-info.patch [bz#1111450]
- kvm-usb-Add-usb_device_alloc-free_streams.patch [bz#1111450]
- kvm-xhci-Call-usb_device_alloc-free_streams.patch [bz#980833]
- kvm-uhci-invalidate-queue-on-device-address-changes.patch [bz#1111450]
- kvm-xhci-iso-fix-time-calculation.patch [bz#949385]
- kvm-xhci-iso-allow-for-some-latency.patch [bz#949385]
- kvm-xhci-switch-debug-printf-to-tracepoint.patch [bz#980747]
- kvm-xhci-use-DPRINTF-instead-of-fprintf-stderr.patch [bz#980833]
- kvm-xhci-child-detach-fix.patch [bz#980833]
- kvm-usb-add-usb_pick_speed.patch [bz#1075846]
- kvm-xhci-make-port-reset-trace-point-more-verbose.patch [bz#980833]
- kvm-usb-initialize-libusb_device-to-avoid-crash.patch [bz#1111450]
- kvm-target-i386-get-CPL-from-SS.DPL.patch [bz#1097363]
- kvm-trace-use-unique-Red-Hat-version-number-in-simpletra.patch [bz#1088112]
- kvm-trace-add-pid-field-to-simpletrace-record.patch [bz#1088112]
- kvm-simpletrace-add-support-for-trace-record-pid-field.patch [bz#1088112]
- kvm-simpletrace-add-simpletrace.py-no-header-option.patch [bz#1088112]
- kvm-trace-extract-stap_escape-function-for-reuse.patch [bz#1088112]
- kvm-trace-add-tracetool-simpletrace_stap-format.patch [bz#1088112]
- kvm-trace-install-simpletrace-SystemTap-tapset.patch [bz#1088112]
- kvm-trace-install-trace-events-file.patch [bz#1088112]
- kvm-trace-add-SystemTap-init-scripts-for-simpletrace-bri.patch [bz#1088112]
- kvm-simpletrace-install-simpletrace.py.patch [bz#1088112]
- kvm-trace-add-systemtap-initscript-README-file-to-RPM.patch [bz#1088112]
- kvm-rdma-Fix-block-during-rdma-migration.patch [bz#1152969]
- Resolves: bz#1046574
  (fail to passthrough the USB speaker redirected from usb-redir with xhci controller)
- Resolves: bz#1046873
  (fail to be recognized the hotpluging usb-storage device with xhci controller in win2012R2 guest)
- Resolves: bz#1075846
  (qemu-kvm core dumped when hotplug/unhotplug USB3.0 device multi times)
- Resolves: bz#1088112
  ([Fujitsu 7.1 FEAT]:QEMU: capturing trace data all the time using ftrace-based tracing)
- Resolves: bz#1088116
  (qemu crash when device_del usb-redir)
- Resolves: bz#1097363
  (qemu ' KVM internal error. Suberror: 1'  when  query cpu frequently during pxe boot in Intel "Q95xx" host)
- Resolves: bz#1111450
  (Guest crash when hotplug usb while disable virt_use_usb)
- Resolves: bz#1152969
  (Qemu-kvm got stuck when migrate to wrong RDMA ip)
- Resolves: bz#949385
  (passthrough USB speaker to win2012 guest fail to work well)
- Resolves: bz#980747
  (flood with 'xhci: wrote doorbell while xHC stopped or paused' when redirected USB Webcam from usb-host with xHCI controller)
- Resolves: bz#980833
  (xhci: FIXME: endpoint stopped w/ xfers running, data might be lost)

* Wed Oct 08 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-75.el7
- kvm-target-i386-Broadwell-CPU-model.patch [bz#1116117]
- kvm-pc-Add-Broadwell-CPUID-compatibility-bits.patch [bz#1116117]
- kvm-virtio-balloon-fix-integer-overflow-in-memory-stats-.patch [bz#1142290]
- Resolves: bz#1116117
  ([Intel 7.1 FEAT] Broadwell new instructions support for KVM - qemu-kvm)
- Resolves: bz#1142290
  (guest is stuck when setting balloon memory with large guest-stats-polling-interval)

* Mon Sep 29 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-74.el7
- kvm-ide-Add-wwn-support-to-IDE-ATAPI-drive.patch [bz#1131316]
- kvm-vmdk-Allow-vmdk_create-to-work-with-protocol.patch [bz#1098086]
- kvm-block-make-vdi-bounds-check-match-upstream.patch [bz#1098086]
- kvm-vdi-say-why-an-image-is-bad.patch [bz#1098086]
- kvm-block-do-not-abuse-EMEDIUMTYPE.patch [bz#1098086]
- kvm-cow-correctly-propagate-errors.patch [bz#1098086]
- kvm-block-Use-correct-width-in-format-strings.patch [bz#1098086]
- kvm-vdi-remove-double-conversion.patch [bz#1098086]
- kvm-block-vdi-Error-out-immediately-in-vdi_create.patch [bz#1098086]
- kvm-vpc-Implement-.bdrv_has_zero_init.patch [bz#1098086]
- kvm-block-vpc-use-QEMU_PACKED-for-on-disk-structures.patch [bz#1098086]
- kvm-block-allow-bdrv_unref-to-be-passed-NULL-pointers.patch [bz#1098086]
- kvm-block-vdi-use-block-layer-ops-in-vdi_create-instead-.patch [bz#1098086]
- kvm-block-use-the-standard-ret-instead-of-result.patch [bz#1098086]
- kvm-block-vpc-use-block-layer-ops-in-vpc_create-instead-.patch [bz#1098086]
- kvm-block-iotest-update-084-to-test-static-VDI-image-cre.patch [bz#1098086]
- kvm-block-add-helper-function-to-determine-if-a-BDS-is-i.patch [bz#1122925]
- kvm-block-extend-block-commit-to-accept-a-string-for-the.patch [bz#1122925]
- kvm-block-add-backing-file-option-to-block-stream.patch [bz#1122925]
- kvm-block-add-__com.redhat_change-backing-file-qmp-comma.patch [bz#1122925]
- Resolves: bz#1098086
  (RFE: Supporting creating vmdk/vdi/vpc format disk with protocols (glusterfs))
- Resolves: bz#1122925
  (Maintain relative path to backing file image during live merge (block-commit))
- Resolves: bz#1131316
  (fail to specify wwn for virtual IDE CD-ROM)

* Tue Sep 23 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-73.el7
- kvm-scsi-disk-fix-bug-in-scsi_block_new_request-introduc.patch [bz#1105880]
- Resolves: bz#1105880
  (bug in scsi_block_new_request() function introduced by upstream commit 137745c5c60f083ec982fe9e861e8c16ebca1ba8)

* Mon Sep 22 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-72.el7
- kvm-vbe-make-bochs-dispi-interface-return-the-correct-me.patch [bz#1139118]
- kvm-vbe-rework-sanity-checks.patch [bz#1139118]
- kvm-spice-display-add-display-channel-id-to-the-debug-me.patch [bz#1139118]
- kvm-spice-make-sure-we-don-t-overflow-ssd-buf.patch [bz#1139118]
- Resolves: bz#1139118
  (CVE-2014-3615 qemu-kvm: Qemu: crash when guest sets high resolution [rhel-7.1])

* Thu Sep 18 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-71.el7
- kvm-spice-move-qemu_spice_display_-from-spice-graphics-t.patch [bz#1054077]
- kvm-spice-move-spice_server_vm_-start-stop-calls-into-qe.patch [bz#1054077]
- kvm-spice-stop-server-for-qxl-hard-reset.patch [bz#1054077]
- kvm-qemu-Adjust-qemu-wakeup.patch [bz#1064156]
- kvm-vmstate_xhci_event-fix-unterminated-field-list.patch [bz#1122147]
- kvm-vmstate_xhci_event-bug-compat-with-RHEL-7.0-RHEL-onl.patch [bz#1122147]
- kvm-pflash_cfi01-write-flash-contents-to-bdrv-on-incomin.patch [bz#1139702]
- kvm-ide-test-Add-enum-value-for-DEV.patch [bz#1123372]
- kvm-ide-test-Add-FLUSH-CACHE-test-case.patch [bz#1123372]
- kvm-ide-Fix-segfault-when-flushing-a-device-that-doesn-t.patch [bz#1123372]
- kvm-IDE-Fill-the-IDENTIFY-request-consistently.patch [bz#852348]
- kvm-ide-Add-resize-callback-to-ide-core.patch [bz#852348]
- Resolves: bz#1054077
  (qemu crash when reboot win7 guest with spice display)
- Resolves: bz#1064156
  ([qxl] The guest show black screen while resumed guest which managedsaved in pmsuspended status.)
- Resolves: bz#1122147
  (CVE-2014-5263 vmstate_xhci_event: fix unterminated field list)
- Resolves: bz#1123372
  (qemu-kvm crashed when doing iofuzz testing)
- Resolves: bz#1139702
  (pflash (UEFI varstore) migration shortcut for libvirt [RHEL])
- Resolves: bz#852348
  (fail to block_resize local data disk with IDE/AHCI disk_interface)

* Fri Sep 12 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-70.el7
- kvm-Enforce-stack-protector-usage.patch [bz#1064260]
- kvm-pc-increase-maximal-VCPU-count-to-240.patch [bz#1134408]
- kvm-gluster-Add-discard-support-for-GlusterFS-block-driv.patch [bz#1136534]
- kvm-gluster-default-scheme-to-gluster-and-host-to-localh.patch [bz#1088150]
- kvm-qdev-properties-system.c-Allow-vlan-or-netdev-for-de.patch [bz#996011]
- kvm-vl-process-object-after-other-backend-options.patch [bz#1128095]
- Resolves: bz#1064260
  (Handle properly --enable-fstack-protector option)
- Resolves: bz#1088150
  (qemu-img coredumpd when try to create a gluster format image)
- Resolves: bz#1128095
  (chardev 'chr0' isn't initialized when we try to open rng backend)
- Resolves: bz#1134408
  ([HP 7.1 FEAT] Increase qemu-kvm's VCPU limit to 240)
- Resolves: bz#1136534
  (glusterfs backend does not support discard)
- Resolves: bz#996011
  (vlan and queues options cause core dumped when qemu-kvm process quit(or ctrl+c))

* Tue Aug 26 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-69.el7
- kvm-rdma-bug-fixes.patch [bz#1107821]
- kvm-virtio-serial-report-frontend-connection-state-via-m.patch [bz#1122151]
- kvm-char-report-frontend-open-closed-state-in-query-char.patch [bz#1122151]
- kvm-acpi-fix-tables-for-no-hpet-configuration.patch [bz#1129552]
- kvm-mirror-Fix-resource-leak-when-bdrv_getlength-fails.patch [bz#1130603]
- kvm-blockjob-Add-block_job_yield.patch [bz#1130603]
- kvm-mirror-Go-through-ready-complete-process-for-0-len-i.patch [bz#1130603]
- kvm-qemu-iotests-Test-BLOCK_JOB_READY-event-for-0Kb-imag.patch [bz#1130603]
- kvm-block-make-top-argument-to-block-commit-optional.patch [bz#1130603]
- kvm-qemu-iotests-Test-0-length-image-for-mirror.patch [bz#1130603]
- kvm-mirror-Fix-qiov-size-for-short-requests.patch [bz#1130603]
- Resolves: bz#1107821
  (rdma migration: seg if destination isn't listening)
- Resolves: bz#1122151
  (Pass close from qemu-ga)
- Resolves: bz#1129552
  (backport "acpi: fix tables for no-hpet configuration")
- Resolves: bz#1130603
  (advertise active commit to libvirt)

* Fri Aug 15 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-68.el7
- kvm-virtio-net-Do-not-filter-VLANs-without-F_CTRL_VLAN.patch [bz#1065724]
- kvm-virtio-net-add-vlan-receive-state-to-RxFilterInfo.patch [bz#1065724]
- kvm-virtio-rng-check-return-value-of-virtio_load.patch [bz#1116941]
- kvm-qapi-treat-all-negative-return-of-strtosz_suffix-as-.patch [bz#1074403]
- Resolves: bz#1065724
  (rx filter incorrect when guest disables VLAN filtering)
- Resolves: bz#1074403
  (qemu-kvm can not give any warning hint when set sndbuf with negative value)
- Resolves: bz#1116941
  (Return value of virtio_load not checked in virtio_rng_load)

* Thu Aug 07 2014 Jeff E. Nelson <jen@redhat.com> - 1.5.3-67.el7
- kvm-vl.c-Output-error-on-invalid-machine-type.patch [bz#990724]
- kvm-migration-dump-vmstate-info-as-a-json-file-for-stati.patch [bz#1118707]
- kvm-vmstate-static-checker-script-to-validate-vmstate-ch.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-add-dump1-and-dump2-fil.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-incompat-machine-types.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-add-version-error-in-ma.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-version-mismatch-inside.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-minimum_version_id-chec.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-remove-a-section.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-remove-a-field.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-remove-last-field-in-a-.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-change-description-name.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-remove-Fields.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-remove-Description.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-remove-Description-insi.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-remove-a-subsection.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-remove-Subsections.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-add-substructure-for-us.patch [bz#1118707]
- kvm-tests-vmstate-static-checker-add-size-mismatch-insid.patch [bz#1118707]
- kvm-aio-fix-qemu_bh_schedule-bh-ctx-race-condition.patch [bz#1116728]
- kvm-block-Improve-driver-whitelist-checks.patch [bz#999789]
- kvm-vmdk-Fix-format-specific-information-create-type-for.patch [bz#1029271]
- kvm-virtio-pci-Report-an-error-when-msix-vectors-init-fa.patch [bz#1095645]
- kvm-scsi-Report-error-when-lun-number-is-in-use.patch [bz#1096576]
- kvm-util-Split-out-exec_dir-from-os_find_datadir.patch [bz#1017685]
- kvm-rules.mak-fix-obj-to-a-real-relative-path.patch [bz#1017685]
- kvm-rules.mak-allow-per-object-cflags-and-libs.patch [bz#1017685]
- kvm-block-use-per-object-cflags-and-libs.patch [bz#1017685]
- kvm-vmdk-Fix-creating-big-description-file.patch [bz#1039791]
- Resolves: bz#1017685
  (Gluster etc. should not be a dependency of vscclient and libcacard)
- Resolves: bz#1029271
  (Format specific information (create type) was wrong when create it specified subformat='streamOptimized')
- Resolves: bz#1039791
  (qemu-img creates truncated VMDK image with subformat=twoGbMaxExtentFlat)
- Resolves: bz#1095645
  (vectors of virtio-scsi-pci will be 0 when set vectors>=129)
- Resolves: bz#1096576
  (QEMU core dumped when boot up two scsi-hd disk on the same virtio-scsi-pci controller in Intel host)
- Resolves: bz#1116728
  (Backport qemu_bh_schedule() race condition fix)
- Resolves: bz#1118707
  (VMstate static checker: backport -dump-vmstate feature to export json-encoded vmstate info)
- Resolves: bz#990724
  (qemu-kvm failing when invalid machine type is provided)
- Resolves: bz#999789
  (qemu should give a more friendly prompt when didn't specify read-only for VMDK format disk)

* Wed Jul 09 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-66.el7
- kvm-xhci-fix-overflow-in-usb_xhci_post_load.patch [bz#1074219]
- kvm-migration-qmp_migrate-keep-working-after-syntax-erro.patch [bz#1086598]
- kvm-seccomp-add-shmctl-mlock-and-munlock-to-the-syscall-.patch [bz#1026314]
- kvm-exit-when-no-kvm-and-vcpu-count-160.patch [bz#1076326]
- kvm-Disallow-outward-migration-while-awaiting-incoming-m.patch [bz#1086987]
- kvm-block-Ignore-duplicate-or-NULL-format_name-in-bdrv_i.patch [bz#1088695 bz#1093983]
- kvm-block-vhdx-account-for-identical-header-sections.patch [bz#1097020]
- kvm-aio-Fix-use-after-free-in-cancellation-path.patch [bz#1095877]
- kvm-scsi-disk-Improve-error-messager-if-can-t-get-versio.patch [bz#1021788]
- kvm-scsi-Improve-error-messages-more.patch [bz#1021788]
- kvm-memory-Don-t-call-memory_region_update_coalesced_ran.patch [bz#1096645]
- kvm-kvmclock-Ensure-time-in-migration-never-goes-backwar.patch [bz#1098602]
- kvm-kvmclock-Ensure-proper-env-tsc-value-for-kvmclock_cu.patch [bz#1098602]
- Resolves: bz#1021788
  (the error message "scsi generic interface too old" is wrong more often than not)
- Resolves: bz#1026314
  (qemu-kvm hang when use '-sandbox on'+'vnc'+'hda')
- Resolves: bz#1074219
  (qemu core dump when install a RHEL.7 guest(xhci) with migration)
- Resolves: bz#1076326
  (qemu-kvm does not quit when booting guest w/ 161 vcpus and "-no-kvm")
- Resolves: bz#1086598
  (migrate_cancel wont take effect on previouly wrong migrate -d cmd)
- Resolves: bz#1086987
  (src qemu crashed when starting migration in inmigrate mode)
- Resolves: bz#1088695
  (there are four "gluster" in qemu-img supported format list)
- Resolves: bz#1093983
  (there are three "nbd" in qemu-img supported format list)
- Resolves: bz#1095877
  (segmentation fault in qemu-kvm due to use-after-free of a SCSIGenericReq (host device pass-through))
- Resolves: bz#1096645
  ([FJ7.0 Bug] RHEL7.0 guest attaching 150 or more virtio-blk disks fails to start up)
- Resolves: bz#1097020
  ([RFE] qemu-img: Add/improve Disk2VHD tools creating VHDX images)
- Resolves: bz#1098602
  (kvmclock: Ensure time in migration never goes backward (backport))

* Wed Jul 02 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-65.el7
- kvm-Allow-mismatched-virtio-config-len.patch [bz#1113009]
- Resolves: bz#1113009
  (Migration failed with virtio-blk from RHEL6.5.0 host to RHEL7.0 host)

* Wed Jun 18 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-64.el7
- kvm-zero-initialize-KVM_SET_GSI_ROUTING-input.patch [bz#1098976]
- kvm-skip-system-call-when-msi-route-is-unchanged.patch [bz#1098976]
- Resolves: bz#1098976
  (2x RHEL 5.10 VM running on RHEL 7 KVM have low TCP_STREAM throughput)

* Tue Jun 17 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-63.el7
- kvm-char-restore-read-callback-on-a-reattached-hotplug-c.patch [bz#1038914]
- kvm-qcow2-Free-preallocated-zero-clusters.patch [bz#1052093]
- kvm-qemu-iotests-Discard-preallocated-zero-clusters.patch [bz#1052093]
- kvm-XBZRLE-Fix-qemu-crash-when-resize-the-xbzrle-cache.patch [bz#1066338]
- kvm-Provide-init-function-for-ram-migration.patch [bz#1066338]
- kvm-Init-the-XBZRLE.lock-in-ram_mig_init.patch [bz#1066338]
- kvm-XBZRLE-Fix-one-XBZRLE-corruption-issues.patch [bz#1066338]
- kvm-Count-used-RAMBlock-pages-for-migration_dirty_pages.patch [bz#1074913]
- kvm-virtio-net-fix-buffer-overflow-on-invalid-state-load.patch [bz#1095678]
- kvm-virtio-net-out-of-bounds-buffer-write-on-invalid-sta.patch [bz#1095690]
- kvm-virtio-net-out-of-bounds-buffer-write-on-load.patch [bz#1095685]
- kvm-virtio-out-of-bounds-buffer-write-on-invalid-state-l.patch [bz#1095695]
- kvm-virtio-avoid-buffer-overrun-on-incoming-migration.patch [bz#1095738]
- kvm-virtio-scsi-fix-buffer-overrun-on-invalid-state-load.patch [bz#1095742]
- kvm-virtio-validate-config_len-on-load.patch [bz#1095783]
- kvm-virtio-validate-num_sg-when-mapping.patch [bz#1095766]
- kvm-virtio-allow-mapping-up-to-max-queue-size.patch [bz#1095766]
- kvm-usb-sanity-check-setup_index-setup_len-in-post_load.patch [bz#1095747]
- kvm-usb-sanity-check-setup_index-setup_len-in-post_l2.patch [bz#1095747]
- kvm-vmstate-reduce-code-duplication.patch [bz#1095716]
- kvm-vmstate-add-VMS_MUST_EXIST.patch [bz#1095716]
- kvm-vmstate-add-VMSTATE_VALIDATE.patch [bz#1095716]
- kvm-hpet-fix-buffer-overrun-on-invalid-state-load.patch [bz#1095707]
- kvm-hw-pci-pcie_aer.c-fix-buffer-overruns-on-invalid-sta.patch [bz#1095716]
- kvm-usb-fix-up-post-load-checks.patch [bz#1096829]
- kvm-qcow-correctly-propagate-errors.patch [bz#1097230]
- kvm-qcow1-Make-padding-in-the-header-explicit.patch [bz#1097230]
- kvm-qcow1-Check-maximum-cluster-size.patch [bz#1097230]
- kvm-qcow1-Validate-L2-table-size-CVE-2014-0222.patch [bz#1097230]
- kvm-qcow1-Validate-image-size-CVE-2014-0223.patch [bz#1097237]
- kvm-qcow1-Stricter-backing-file-length-check.patch [bz#1097237]
- Resolves: bz#1038914
  (Guest can't receive any character transmitted from host after hot unplugging virtserialport then hot plugging again)
- Resolves: bz#1052093
  (qcow2 corruptions (leaked clusters after installing a rhel7 guest using virtio_scsi))
- Resolves: bz#1066338
  (Reduce the migrate cache size during migration causes qemu segment fault)
- Resolves: bz#1074913
  (migration can not finish with 1024k 'remaining ram' left after hotunplug 4 nics)
- Resolves: bz#1095678
  (CVE-2013-4148 qemu-kvm: qemu: virtio-net: buffer overflow on invalid state load [rhel-7.1])
- Resolves: bz#1095685
  (CVE-2013-4149 qemu-kvm: qemu: virtio-net: out-of-bounds buffer write on load [rhel-7.1])
- Resolves: bz#1095690
  (CVE-2013-4150 qemu-kvm: qemu: virtio-net: out-of-bounds buffer write on invalid state load [rhel-7.1])
- Resolves: bz#1095695
  (CVE-2013-4151 qemu-kvm: qemu: virtio: out-of-bounds buffer write on invalid state load [rhel-7.1])
- Resolves: bz#1095707
  (CVE-2013-4527 qemu-kvm: qemu: hpet: buffer overrun on invalid state load [rhel-7.1])
- Resolves: bz#1095716
  (CVE-2013-4529 qemu-kvm: qemu: hw/pci/pcie_aer.c: buffer overrun on invalid state load [rhel-7.1])
- Resolves: bz#1095738
  (CVE-2013-6399 qemu-kvm: qemu: virtio: buffer overrun on incoming migration [rhel-7.1])
- Resolves: bz#1095742
  (CVE-2013-4542 qemu-kvm: qemu: virtio-scsi: buffer overrun on invalid state load [rhel-7.1])
- Resolves: bz#1095747
  (CVE-2013-4541 qemu-kvm: qemu: usb: insufficient sanity checking of setup_index+setup_len in post_load [rhel-7.1])
- Resolves: bz#1095766
  (CVE-2013-4535 CVE-2013-4536 qemu-kvm: qemu: virtio: insufficient validation of num_sg when mapping [rhel-7.1])
- Resolves: bz#1095783
  (CVE-2014-0182 qemu-kvm: qemu: virtio: out-of-bounds buffer write on state load with invalid config_len [rhel-7.1])
- Resolves: bz#1096829
  (CVE-2014-3461 qemu-kvm: Qemu: usb: fix up post load checks [rhel-7.1])
- Resolves: bz#1097230
  (CVE-2014-0222 qemu-kvm: Qemu: qcow1: validate L2 table size to avoid integer overflows [rhel-7.1])
- Resolves: bz#1097237
  (CVE-2014-0223 qemu-kvm: Qemu: qcow1: validate image size to avoid out-of-bounds memory access [rhel-7.1])

* Wed May 07 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-62.el7
- kvm-pc-add-hot_add_cpu-callback-to-all-machine-types.patch [bz#1094285]
- Resolves: bz#1094285
  (Hot plug CPU not working with RHEL6  machine types running on RHEL7 host.)

* Fri May 02 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-61.el7
- kvm-iscsi-fix-indentation.patch [bz#1083413]
- kvm-iscsi-correctly-propagate-errors-in-iscsi_open.patch [bz#1083413]
- kvm-block-iscsi-query-for-supported-VPD-pages.patch [bz#1083413]
- kvm-block-iscsi-fix-segfault-if-writesame-fails.patch [bz#1083413]
- kvm-iscsi-recognize-invalid-field-ASCQ-from-WRITE-SAME-c.patch [bz#1083413]
- kvm-iscsi-ignore-flushes-on-scsi-generic-devices.patch [bz#1083413]
- kvm-iscsi-always-query-max-WRITE-SAME-length.patch [bz#1083413]
- kvm-iscsi-Don-t-set-error-if-already-set-in-iscsi_do_inq.patch [bz#1083413]
- kvm-iscsi-Remember-to-set-ret-for-iscsi_open-in-error-ca.patch [bz#1083413]
- kvm-qemu_loadvm_state-shadow-SeaBIOS-for-VM-incoming-fro.patch [bz#1027565]
- kvm-uhci-UNfix-irq-routing-for-RHEL-6-machtypes-RHEL-onl.patch [bz#1085701]
- kvm-ide-Correct-improper-smart-self-test-counter-reset-i.patch [bz#1087980]
- Resolves: bz#1027565
  (fail to reboot guest after migration from RHEL6.5 host to RHEL7.0 host)
- Resolves: bz#1083413
  (qemu-kvm: iSCSI: Failure. SENSE KEY:ILLEGAL_REQUEST(5) ASCQ:INVALID_FIELD_IN_CDB(0x2400))
- Resolves: bz#1085701
  (Guest hits call trace migrate from RHEL6.5 to RHEL7.0 host with -M 6.1 & balloon & uhci device)
- Resolves: bz#1087980
  (CVE-2014-2894 qemu-kvm: QEMU: out of bounds buffer accesses, guest triggerable via IDE SMART [rhel-7.1])

* Wed Apr 02 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-60.el7
- kvm-qcow2-fix-dangling-refcount-table-entry.patch [bz#1081793]
- kvm-qcow2-link-all-L2-meta-updates-in-preallocate.patch [bz#1081393]
- Resolves: bz#1081393
  (qemu-img will prompt that 'leaked clusters were found' while creating images with '-o preallocation=metadata,cluster_size<=1024')
- Resolves: bz#1081793
  (qemu-img core dumped when creating a qcow2 image base on block device(iscsi or libiscsi))

* Wed Mar 26 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-59.el7
- kvm-qemu-iotests-add-.-check-cloop-support.patch [bz#1066691]
- kvm-qemu-iotests-add-cloop-input-validation-tests.patch [bz#1066691]
- kvm-block-cloop-validate-block_size-header-field-CVE-201.patch [bz#1079455]
- kvm-block-cloop-prevent-offsets_size-integer-overflow-CV.patch [bz#1079320]
- kvm-block-cloop-refuse-images-with-huge-offsets-arrays-C.patch [bz#1079455]
- kvm-block-cloop-refuse-images-with-bogus-offsets-CVE-201.patch [bz#1079455]
- kvm-size-off-by-one.patch [bz#1066691]
- kvm-qemu-iotests-Support-for-bochs-format.patch [bz#1066691]
- kvm-bochs-Unify-header-structs-and-make-them-QEMU_PACKED.patch [bz#1066691]
- kvm-bochs-Use-unsigned-variables-for-offsets-and-sizes-C.patch [bz#1079339]
- kvm-bochs-Check-catalog_size-header-field-CVE-2014-0143.patch [bz#1079320]
- kvm-bochs-Check-extent_size-header-field-CVE-2014-0142.patch [bz#1079315]
- kvm-bochs-Fix-bitmap-offset-calculation.patch [bz#1066691]
- kvm-vpc-vhd-add-bounds-check-for-max_table_entries-and-b.patch [bz#1079455]
- kvm-vpc-Validate-block-size-CVE-2014-0142.patch [bz#1079315]
- kvm-vdi-add-bounds-checks-for-blocks_in_image-and-disk_s.patch [bz#1079455]
- kvm-vhdx-Bounds-checking-for-block_size-and-logical_sect.patch [bz#1079346]
- kvm-curl-check-data-size-before-memcpy-to-local-buffer.-.patch [bz#1079455]
- kvm-qcow2-Check-header_length-CVE-2014-0144.patch [bz#1079455]
- kvm-qcow2-Check-backing_file_offset-CVE-2014-0144.patch [bz#1079455]
- kvm-qcow2-Check-refcount-table-size-CVE-2014-0144.patch [bz#1079455]
- kvm-qcow2-Validate-refcount-table-offset.patch [bz#1066691]
- kvm-qcow2-Validate-snapshot-table-offset-size-CVE-2014-0.patch [bz#1079455]
- kvm-qcow2-Validate-active-L1-table-offset-and-size-CVE-2.patch [bz#1079455]
- kvm-qcow2-Fix-backing-file-name-length-check.patch [bz#1066691]
- kvm-qcow2-Don-t-rely-on-free_cluster_index-in-alloc_refc.patch [bz#1079339]
- kvm-qcow2-Avoid-integer-overflow-in-get_refcount-CVE-201.patch [bz#1079320]
- kvm-qcow2-Check-new-refcount-table-size-on-growth.patch [bz#1066691]
- kvm-qcow2-Fix-types-in-qcow2_alloc_clusters-and-alloc_cl.patch [bz#1066691]
- kvm-qcow2-Protect-against-some-integer-overflows-in-bdrv.patch [bz#1066691]
- kvm-qcow2-Fix-new-L1-table-size-check-CVE-2014-0143.patch [bz#1079320]
- kvm-dmg-coding-style-and-indentation-cleanup.patch [bz#1066691]
- kvm-dmg-prevent-out-of-bounds-array-access-on-terminator.patch [bz#1066691]
- kvm-dmg-drop-broken-bdrv_pread-loop.patch [bz#1066691]
- kvm-dmg-use-appropriate-types-when-reading-chunks.patch [bz#1066691]
- kvm-dmg-sanitize-chunk-length-and-sectorcount-CVE-2014-0.patch [bz#1079325]
- kvm-dmg-use-uint64_t-consistently-for-sectors-and-length.patch [bz#1066691]
- kvm-dmg-prevent-chunk-buffer-overflow-CVE-2014-0145.patch [bz#1079325]
- kvm-block-vdi-bounds-check-qemu-io-tests.patch [bz#1066691]
- kvm-block-Limit-request-size-CVE-2014-0143.patch [bz#1079320]
- kvm-qcow2-Fix-copy_sectors-with-VM-state.patch [bz#1066691]
- kvm-qcow2-Fix-NULL-dereference-in-qcow2_open-error-path-.patch [bz#1079333]
- kvm-qcow2-Fix-L1-allocation-size-in-qcow2_snapshot_load_.patch [bz#1079325]
- kvm-qcow2-Check-maximum-L1-size-in-qcow2_snapshot_load_t.patch [bz#1079320]
- kvm-qcow2-Limit-snapshot-table-size.patch [bz#1066691]
- kvm-parallels-Fix-catalog-size-integer-overflow-CVE-2014.patch [bz#1079320]
- kvm-parallels-Sanity-check-for-s-tracks-CVE-2014-0142.patch [bz#1079315]
- kvm-fix-machine-check-propagation.patch [bz#740107]
- Resolves: bz#1066691
  (qemu-kvm: include leftover patches from block layer security audit)
- Resolves: bz#1079315
  (CVE-2014-0142 qemu-kvm: qemu: crash by possible division by zero [rhel-7.0])
- Resolves: bz#1079320
  (CVE-2014-0143 qemu-kvm: Qemu: block: multiple integer overflow flaws [rhel-7.0])
- Resolves: bz#1079325
  (CVE-2014-0145 qemu-kvm: Qemu: prevent possible buffer overflows [rhel-7.0])
- Resolves: bz#1079333
  (CVE-2014-0146 qemu-kvm: Qemu: qcow2: NULL dereference in qcow2_open() error path [rhel-7.0])
- Resolves: bz#1079339
  (CVE-2014-0147 qemu-kvm: Qemu: block: possible crash due signed types or logic error [rhel-7.0])
- Resolves: bz#1079346
  (CVE-2014-0148 qemu-kvm: Qemu: vhdx: bounds checking for block_size and logical_sector_size [rhel-7.0])
- Resolves: bz#1079455
  (CVE-2014-0144 qemu-kvm: Qemu: block: missing input validation [rhel-7.0])
- Resolves: bz#740107
  ([Hitachi 7.0 FEAT]  KVM: MCA Recovery for KVM guest OS memory)

* Wed Mar 26 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-58.el7
- kvm-pc-Use-cpu64-rhel6-CPU-model-by-default-on-rhel6-mac.patch [bz#1080170]
- kvm-target-i386-Copy-cpu64-rhel6-definition-into-qemu64.patch [bz#1078607 bz#1080170]
- Resolves: bz#1080170
  (intel 82576 VF not work in windows 2008 x86 - Code 12 [TestOnly])
- Resolves: bz#1080170
  (Default CPU model for rhel6.* machine-types is different from RHEL-6)

* Fri Mar 21 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-57.el7
- kvm-virtio-net-fix-guest-triggerable-buffer-overrun.patch [bz#1078308]
- Resolves: bz#1078308
  (EMBARGOED CVE-2014-0150 qemu: virtio-net: fix guest-triggerable buffer overrun [rhel-7.0])

* Fri Mar 21 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-56.el7
- kvm-configure-Fix-bugs-preventing-Ceph-inclusion.patch [bz#1078809]
- Resolves: bz#1078809
  (can not boot qemu-kvm-rhev with rbd image)

* Wed Mar 19 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-55.el7
- kvm-scsi-Change-scsi-sense-buf-size-to-252.patch [bz#1058173]
- kvm-scsi-Fix-migration-of-scsi-sense-data.patch [bz#1058173]
- Resolves: bz#1058173
  (qemu-kvm core dump booting guest with scsi-generic disk attached when using built-in iscsi driver)

* Wed Mar 19 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-54.el7
- kvm-qdev-monitor-Set-properties-after-parent-is-assigned.patch [bz#1046248]
- kvm-block-Update-image-size-in-bdrv_invalidate_cache.patch [bz#1048575]
- kvm-qcow2-Keep-option-in-qcow2_invalidate_cache.patch [bz#1048575]
- kvm-qcow2-Check-bs-drv-in-copy_sectors.patch [bz#1048575]
- kvm-block-bs-drv-may-be-NULL-in-bdrv_debug_resume.patch [bz#1048575]
- kvm-iotests-Test-corruption-during-COW-request.patch [bz#1048575]
- Resolves: bz#1046248
  (qemu-kvm crash when send "info qtree" after hot plug a device with invalid addr)
- Resolves: bz#1048575
  (Segmentation fault occurs after migrate guest(use scsi disk and add stress) to des machine)

* Wed Mar 12 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-53.el7
- kvm-dataplane-Fix-startup-race.patch [bz#1069541]
- kvm-QMP-Relax-__com.redhat_drive_add-parameter-checking.patch [bz#1057471]
- kvm-all-exit-in-case-max-vcpus-exceeded.patch [bz#993429]
- kvm-block-gluster-code-movements-state-storage-changes.patch [bz#1031526]
- kvm-block-gluster-add-reopen-support.patch [bz#1031526]
- kvm-virtio-net-add-feature-bit-for-any-header-s-g.patch [bz#990989]
- kvm-spec-Add-README.rhel6-gpxe-source.patch [bz#1073774]
- kvm-pc-Add-RHEL6-e1000-gPXE-image.patch [bz#1073774]
- kvm-loader-rename-in_ram-has_mr.patch [bz#1064018]
- kvm-pc-avoid-duplicate-names-for-ROM-MRs.patch [bz#1064018]
- kvm-qemu-img-convert-Fix-progress-output.patch [bz#1073728]
- kvm-qemu-iotests-Test-progress-output-for-conversion.patch [bz#1073728]
- kvm-iscsi-Use-bs-sg-for-everything-else-than-disks.patch [bz#1067784]
- kvm-block-Fix-bs-request_alignment-assertion-for-bs-sg-1.patch [bz#1067784]
- kvm-qemu_file-use-fwrite-correctly.patch [bz#1005103]
- kvm-qemu_file-Fix-mismerge-of-use-fwrite-correctly.patch [bz#1005103]
- Resolves: bz#1005103
  (Migration should fail when migrate guest offline to a file which is specified to a readonly directory.)
- Resolves: bz#1031526
  (Can not commit snapshot when disk is using glusterfs:native backend)
- Resolves: bz#1057471
  (fail to do hot-plug with "discard = on" with "Invalid parameter 'discard'" error)
- Resolves: bz#1064018
  (abort from conflicting genroms)
- Resolves: bz#1067784
  (qemu-kvm: block.c:850: bdrv_open_common: Assertion `bs->request_alignment != 0' failed. Aborted (core dumped))
- Resolves: bz#1069541
  (Segmentation fault when boot guest with dataplane=on)
- Resolves: bz#1073728
  (progress bar doesn't display when converting with -p)
- Resolves: bz#1073774
  (e1000 ROM cause migrate fail  from RHEL6.5 host to RHEL7.0 host)
- Resolves: bz#990989
  (backport inline header virtio-net optimization)
- Resolves: bz#993429
  (kvm: test maximum number of vcpus supported (rhel7))

* Wed Mar 05 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-52.el7
- kvm-target-i386-Move-hyperv_-static-globals-to-X86CPU.patch [bz#1004773]
- kvm-Fix-uninitialized-cpuid_data.patch [bz#1057173]
- kvm-fix-coexistence-of-KVM-and-Hyper-V-leaves.patch [bz#1004773]
- kvm-make-availability-of-Hyper-V-enlightenments-depe.patch [bz#1004773]
- kvm-make-hyperv-hypercall-and-guest-os-id-MSRs-migra.patch [bz#1004773]
- kvm-make-hyperv-vapic-assist-page-migratable.patch [bz#1004773]
- kvm-target-i386-Convert-hv_relaxed-to-static-property.patch [bz#1057173]
- kvm-target-i386-Convert-hv_vapic-to-static-property.patch [bz#1057173]
- kvm-target-i386-Convert-hv_spinlocks-to-static-property.patch [bz#1057173]
- kvm-target-i386-Convert-check-and-enforce-to-static-prop.patch [bz#1004773]
- kvm-target-i386-Cleanup-foo-feature-handling.patch [bz#1057173]
- kvm-add-support-for-hyper-v-timers.patch [bz#1057173]
- Resolves: bz#1004773
  (Hyper-V guest OS id and hypercall MSRs not migrated)
- Resolves: bz#1057173
  (KVM Hyper-V Enlightenment - New feature - hv-time (QEMU))

* Wed Mar 05 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-51.el7
- kvm-qmp-access-the-local-QemuOptsLists-for-drive-option.patch [bz#1026184]
- kvm-qxl-add-sanity-check.patch [bz#751937]
- kvm-Fix-two-XBZRLE-corruption-issues.patch [bz#1063417]
- kvm-qdev-monitor-set-DeviceState-opts-before-calling-rea.patch [bz#1037956]
- kvm-vfio-blacklist-loading-of-unstable-roms.patch [bz#1037956]
- kvm-block-Set-block-filename-sizes-to-PATH_MAX-instead-o.patch [bz#1072339]
- Resolves: bz#1026184
  (QMP: querying -drive option returns a NULL parameter list)
- Resolves: bz#1037956
  (bnx2x: boot one guest to do vfio-pci with all PFs assigned in same group meet QEMU segmentation fault (Broadcom BCM57810 card))
- Resolves: bz#1063417
  (google stressapptest vs Migration)
- Resolves: bz#1072339
  (RHEV: Cannot start VMs that have more than 23 snapshots.)
- Resolves: bz#751937
  (qxl triggers assert during iofuzz test)

* Wed Feb 26 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-50.el7
- kvm-mempath-prefault-fix-off-by-one-error.patch [bz#1069039]
- kvm-qemu-option-has_help_option-and-is_valid_option_list.patch [bz#1065873]
- kvm-qemu-img-create-Support-multiple-o-options.patch [bz#1065873]
- kvm-qemu-img-convert-Support-multiple-o-options.patch [bz#1065873]
- kvm-qemu-img-amend-Support-multiple-o-options.patch [bz#1065873]
- kvm-qemu-img-Allow-o-help-with-incomplete-argument-list.patch [bz#1065873]
- kvm-qemu-iotests-Check-qemu-img-command-line-parsing.patch [bz#1065873]
- Resolves: bz#1065873
  (qemu-img silently ignores options with multiple -o parameters)
- Resolves: bz#1069039
  (-mem-prealloc option behaviour is opposite to expected)

* Wed Feb 19 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-49.el7
- kvm-xhci-add-support-for-suspend-resume.patch [bz#1012365]
- kvm-qcow2-remove-n_start-and-n_end-of-qcow2_alloc_cluste.patch [bz#1049176]
- kvm-qcow2-fix-offset-overflow-in-qcow2_alloc_clusters_at.patch [bz#1049176]
- kvm-qcow2-check-for-NULL-l2meta.patch [bz#1055848]
- kvm-qemu-iotests-add-test-for-qcow2-preallocation-with-d.patch [bz#1055848]
- Resolves: bz#1012365
  (xhci usb storage lost in guest after wakeup from S3)
- Resolves: bz#1049176
  (qemu-img core dump when using "-o preallocation=metadata,cluster_size=2048k" to create image of libiscsi lun)
- Resolves: bz#1055848
  (qemu-img core dumped when cluster size is larger than the default value with opreallocation=metadata specified)

* Mon Feb 17 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-48.el7
- kvm-spec-disable-qom-cast-debug.patch [bz#1063942]
- kvm-fix-guest-physical-bits-to-match-host-to-go-beyond-1.patch [bz#989677]
- kvm-monitor-Cleanup-mon-outbuf-on-write-error.patch [bz#1065225]
- Resolves: bz#1063942
  (configure qemu-kvm with --disable-qom-cast-debug)
- Resolves: bz#1065225
  (QMP socket breaks on unexpected close)
- Resolves: bz#989677
  ([HP 7.0 FEAT]: Increase KVM guest supported memory to 4TiB)

* Wed Feb 12 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-47.el7
- kvm-seccomp-add-mkdir-and-fchmod-to-the-whitelist.patch [bz#1026314]
- kvm-seccomp-add-some-basic-shared-memory-syscalls-to-the.patch [bz#1026314]
- kvm-scsi-Support-TEST-UNIT-READY-in-the-dummy-LUN0.patch [bz#1004143]
- kvm-usb-add-vendor-request-defines.patch [bz#1039530]
- kvm-usb-move-usb_-hi-lo-helpers-to-header-file.patch [bz#1039530]
- kvm-usb-add-support-for-microsoft-os-descriptors.patch [bz#1039530]
- kvm-usb-add-microsoft-os-descriptors-compat-property.patch [bz#1039530]
- kvm-usb-hid-add-microsoft-os-descriptor-support.patch [bz#1039530]
- kvm-configure-add-option-to-disable-fstack-protect.patch [bz#1044182]
- kvm-exec-always-use-MADV_DONTFORK.patch [bz#1004197]
- kvm-pc-Save-size-of-RAM-below-4GB.patch [bz#1048080]
- kvm-acpi-Fix-PCI-hole-handling-on-build_srat.patch [bz#1048080]
- kvm-Add-check-for-cache-size-smaller-than-page-size.patch [bz#1017096]
- kvm-XBZRLE-cache-size-should-not-be-larger-than-guest-me.patch [bz#1047448]
- kvm-Don-t-abort-on-out-of-memory-when-creating-page-cach.patch [bz#1047448]
- kvm-Don-t-abort-on-memory-allocation-error.patch [bz#1047448]
- kvm-Set-xbzrle-buffers-to-NULL-after-freeing-them-to-avo.patch [bz#1038540]
- kvm-migration-fix-free-XBZRLE-decoded_buf-wrong.patch [bz#1038540]
- kvm-block-resize-backing-file-image-during-offline-commi.patch [bz#1047254]
- kvm-block-resize-backing-image-during-active-layer-commi.patch [bz#1047254]
- kvm-block-update-block-commit-documentation-regarding-im.patch [bz#1047254]
- kvm-block-Fix-bdrv_commit-return-value.patch [bz#1047254]
- kvm-block-remove-QED-.bdrv_make_empty-implementation.patch [bz#1047254]
- kvm-block-remove-qcow2-.bdrv_make_empty-implementation.patch [bz#1047254]
- kvm-qemu-progress-Drop-unused-include.patch [bz#997878]
- kvm-qemu-progress-Fix-progress-printing-on-SIGUSR1.patch [bz#997878]
- kvm-Documentation-qemu-img-Mention-SIGUSR1-progress-repo.patch [bz#997878]
- Resolves: bz#1004143
  ("test unit ready failed" on LUN 0 delays boot when a virtio-scsi target does not have any disk on LUN 0)
- Resolves: bz#1004197
  (Cannot hot-plug nic in windows VM when the vmem is larger)
- Resolves: bz#1017096
  (Fail to migrate while the size of migrate-compcache less then 4096)
- Resolves: bz#1026314
  (qemu-kvm hang when use '-sandbox on'+'vnc'+'hda')
- Resolves: bz#1038540
  (qemu-kvm aborted while cancel migration then restart it (with page delta compression))
- Resolves: bz#1039530
  (add support for microsoft os descriptors)
- Resolves: bz#1044182
  (Relax qemu-kvm stack protection to -fstack-protector-strong)
- Resolves: bz#1047254
  (qemu-img failed to commit image)
- Resolves: bz#1047448
  (qemu-kvm core  dump in src host when do migration with "migrate_set_capability xbzrle on and migrate_set_cache_size 10000G")
- Resolves: bz#1048080
  (Qemu-kvm NUMA emulation failed)
- Resolves: bz#997878
  (Kill -SIGUSR1 `pidof qemu-img convert` can not get progress of qemu-img)

* Wed Feb 12 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-46.el7
- kvm-block-fix-backing-file-segfault.patch [bz#748906]
- kvm-block-Move-initialisation-of-BlockLimits-to-bdrv_ref.patch [bz#748906]
- kvm-raw-Fix-BlockLimits-passthrough.patch [bz#748906]
- kvm-block-Inherit-opt_transfer_length.patch [bz#748906]
- kvm-block-Update-BlockLimits-when-they-might-have-change.patch [bz#748906]
- kvm-qemu_memalign-Allow-small-alignments.patch [bz#748906]
- kvm-block-Detect-unaligned-length-in-bdrv_qiov_is_aligne.patch [bz#748906]
- kvm-block-Don-t-use-guest-sector-size-for-qemu_blockalig.patch [bz#748906]
- kvm-block-rename-buffer_alignment-to-guest_block_size.patch [bz#748906]
- kvm-raw-Probe-required-direct-I-O-alignment.patch [bz#748906]
- kvm-block-Introduce-bdrv_aligned_preadv.patch [bz#748906]
- kvm-block-Introduce-bdrv_co_do_preadv.patch [bz#748906]
- kvm-block-Introduce-bdrv_aligned_pwritev.patch [bz#748906]
- kvm-block-write-Handle-COR-dependency-after-I-O-throttli.patch [bz#748906]
- kvm-block-Introduce-bdrv_co_do_pwritev.patch [bz#748906]
- kvm-block-Switch-BdrvTrackedRequest-to-byte-granularity.patch [bz#748906]
- kvm-block-Allow-waiting-for-overlapping-requests-between.patch [bz#748906]
- kvm-block-use-DIV_ROUND_UP-in-bdrv_co_do_readv.patch [bz#748906]
- kvm-block-Make-zero-after-EOF-work-with-larger-alignment.patch [bz#748906]
- kvm-block-Generalise-and-optimise-COR-serialisation.patch [bz#748906]
- kvm-block-Make-overlap-range-for-serialisation-dynamic.patch [bz#748906]
- kvm-block-Fix-32-bit-truncation-in-mark_request_serialis.patch [bz#748906]
- kvm-block-Allow-wait_serialising_requests-at-any-point.patch [bz#748906]
- kvm-block-Align-requests-in-bdrv_co_do_pwritev.patch [bz#748906]
- kvm-lock-Fix-memory-leaks-in-bdrv_co_do_pwritev.patch [bz#748906]
- kvm-block-Assert-serialisation-assumptions-in-pwritev.patch [bz#748906]
- kvm-block-Change-coroutine-wrapper-to-byte-granularity.patch [bz#748906]
- kvm-block-Make-bdrv_pread-a-bdrv_prwv_co-wrapper.patch [bz#748906]
- kvm-block-Make-bdrv_pwrite-a-bdrv_prwv_co-wrapper.patch [bz#748906]
- kvm-iscsi-Set-bs-request_alignment.patch [bz#748906]
- kvm-blkdebug-Make-required-alignment-configurable.patch [bz#748906]
- kvm-blkdebug-Don-t-leak-bs-file-on-failure.patch [bz#748906]
- kvm-qemu-io-New-command-sleep.patch [bz#748906]
- kvm-qemu-iotests-Filter-out-qemu-io-prompt.patch [bz#748906]
- kvm-qemu-iotests-Test-pwritev-RMW-logic.patch [bz#748906]
- kvm-block-bdrv_aligned_pwritev-Assert-overlap-range.patch [bz#748906]
- kvm-block-Don-t-call-ROUND_UP-with-negative-values.patch [bz#748906]
- Resolves: bz#748906
  (qemu fails on disk with 4k sectors and cache=off)

* Wed Feb 05 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-45.el7
- kvm-vfio-pci-Fail-initfn-on-DMA-mapping-errors.patch [bz#1044815]
- kvm-vfio-Destroy-memory-regions.patch [bz#1052030]
- kvm-docs-qcow2-compat-1.1-is-now-the-default.patch [bz#1048092]
- kvm-hda-codec-disable-streams-on-reset.patch [bz#947812]
- kvm-QEMUBH-make-AioContext-s-bh-re-entrant.patch [bz#1009297]
- kvm-qxl-replace-pipe-signaling-with-bottom-half.patch [bz#1009297]
- Resolves: bz#1009297
  (RHEL7.0 guest gui can not be used in dest host after migration)
- Resolves: bz#1044815
  (vfio initfn succeeds even if IOMMU mappings fail)
- Resolves: bz#1048092
  (manpage of qemu-img contains error statement about compat option)
- Resolves: bz#1052030
  (src qemu-kvm core dump after hotplug/unhotplug GPU device and do local migration)
- Resolves: bz#947812
  (There's a shot voice after  'system_reset'  during playing music inside rhel6 guest w/ intel-hda device)

* Wed Jan 29 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-44.el7
- kvm-Partially-revert-rhel-Drop-cfi.pflash01-and-isa-ide-.patch [bz#1032346]
- kvm-Revert-pc-Disable-the-use-flash-device-for-BIOS-unle.patch [bz#1032346]
- kvm-memory-Replace-open-coded-memory_region_is_romd.patch [bz#1032346]
- kvm-memory-Rename-readable-flag-to-romd_mode.patch [bz#1032346]
- kvm-isapc-Fix-non-KVM-qemu-boot-read-write-memory-for-is.patch [bz#1032346]
- kvm-add-kvm_readonly_mem_enabled.patch [bz#1032346]
- kvm-support-using-KVM_MEM_READONLY-flag-for-regions.patch [bz#1032346]
- kvm-pc_sysfw-allow-flash-pflash-memory-to-be-used-with-K.patch [bz#1032346]
- kvm-fix-double-free-the-memslot-in-kvm_set_phys_mem.patch [bz#1032346]
- kvm-sysfw-remove-read-only-pc_sysfw_flash_vs_rom_bug_com.patch [bz#1032346]
- kvm-pc_sysfw-remove-the-rom_only-property.patch [bz#1032346]
- kvm-pc_sysfw-do-not-make-it-a-device-anymore.patch [bz#1032346]
- kvm-hw-i386-pc_sysfw-support-two-flash-drives.patch [bz#1032346]
- kvm-i440fx-test-qtest_start-should-be-paired-with-qtest_.patch [bz#1032346]
- kvm-i440fx-test-give-each-GTest-case-its-own-qtest.patch [bz#1032346]
- kvm-i440fx-test-generate-temporary-firmware-blob.patch [bz#1032346]
- kvm-i440fx-test-verify-firmware-under-4G-and-1M-both-bio.patch [bz#1032346]
- kvm-piix-fix-32bit-pci-hole.patch [bz#1032346]
- kvm-qapi-Add-backing-to-BlockStats.patch [bz#1041564]
- kvm-pc-Disable-RDTSCP-unconditionally-on-rhel6.-machine-.patch [bz#918907]
- kvm-pc-Disable-RDTSCP-on-AMD-CPU-models.patch [bz#1056428 bz#874400]
- kvm-block-add-.bdrv_reopen_prepare-stub-for-iscsi.patch [bz#1030301]
- Resolves: bz#1030301
  (qemu-img can not merge live snapshot to backing file(r/w backing file via libiscsi))
- Resolves: bz#1032346
  (basic OVMF support (non-volatile UEFI variables in flash, and fixup for ACPI tables))
- Resolves: bz#1041564
  ([NFR] qemu: Returning the watermark for all the images opened for writing)
- Resolves: bz#1056428
  ("rdtscp" flag defined on Opteron_G5 model and cann't be exposed to guest)
- Resolves: bz#874400
  ("rdtscp" flag defined on Opteron_G5 model and cann't be exposed to guest)
- Resolves: bz#918907
  (provide backwards-compatible RHEL specific machine types in QEMU - CPU features)

* Mon Jan 27 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-43.el7
- kvm-piix-gigabyte-alignment-for-ram.patch [bz#1026548]
- kvm-pc_piix-document-gigabyte_align.patch [bz#1026548]
- kvm-q35-gigabyle-alignment-for-ram.patch [bz#1026548]
- kvm-virtio-bus-remove-vdev-field.patch [bz#983344]
- kvm-virtio-pci-remove-vdev-field.patch [bz#983344]
- kvm-virtio-bus-cleanup-plug-unplug-interface.patch [bz#983344]
- kvm-virtio-blk-switch-exit-callback-to-VirtioDeviceClass.patch [bz#983344]
- kvm-virtio-serial-switch-exit-callback-to-VirtioDeviceCl.patch [bz#983344]
- kvm-virtio-net-switch-exit-callback-to-VirtioDeviceClass.patch [bz#983344]
- kvm-virtio-scsi-switch-exit-callback-to-VirtioDeviceClas.patch [bz#983344]
- kvm-virtio-balloon-switch-exit-callback-to-VirtioDeviceC.patch [bz#983344]
- kvm-virtio-rng-switch-exit-callback-to-VirtioDeviceClass.patch [bz#983344]
- kvm-virtio-pci-add-device_unplugged-callback.patch [bz#983344]
- kvm-block-use-correct-filename-for-error-report.patch [bz#1051438]
- Resolves: bz#1026548
  (i386: pc: align gpa<->hpa on 1GB boundary)
- Resolves: bz#1051438
  (Error message contains garbled characters when unable to open image due to bad permissions (permission denied).)
- Resolves: bz#983344
  (QEMU core dump and host will reboot when do hot-unplug a virtio-blk disk which use  the switch behind switch)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 10:1.5.3-42
- Mass rebuild 2014-01-24

* Wed Jan 22 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-41.el7
- kvm-help-add-id-suboption-to-iscsi.patch [bz#1019221]
- kvm-scsi-disk-add-UNMAP-limits-to-block-limits-VPD-page.patch [bz#1037503]
- kvm-qdev-Fix-32-bit-compilation-in-print_size.patch [bz#1034876]
- kvm-qdev-Use-clz-in-print_size.patch [bz#1034876]
- Resolves: bz#1019221
  (Iscsi miss id sub-option in help output)
- Resolves: bz#1034876
  (export acpi tables to guests)
- Resolves: bz#1037503
  (fix thin provisioning support for block device backends)

* Wed Jan 22 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-40.el7
- kvm-avoid-a-bogus-COMPLETED-CANCELLED-transition.patch [bz#1053699]
- kvm-introduce-MIG_STATE_CANCELLING-state.patch [bz#1053699]
- kvm-vvfat-use-bdrv_new-to-allocate-BlockDriverState.patch [bz#1041301]
- kvm-block-implement-reference-count-for-BlockDriverState.patch [bz#1041301]
- kvm-block-make-bdrv_delete-static.patch [bz#1041301]
- kvm-migration-omit-drive-ref-as-we-have-bdrv_ref-now.patch [bz#1041301]
- kvm-xen_disk-simplify-blk_disconnect-with-refcnt.patch [bz#1041301]
- kvm-nbd-use-BlockDriverState-refcnt.patch [bz#1041301]
- kvm-block-use-BDS-ref-for-block-jobs.patch [bz#1041301]
- kvm-block-Make-BlockJobTypes-const.patch [bz#1041301]
- kvm-blockjob-rename-BlockJobType-to-BlockJobDriver.patch [bz#1041301]
- kvm-qapi-Introduce-enum-BlockJobType.patch [bz#1041301]
- kvm-qapi-make-use-of-new-BlockJobType.patch [bz#1041301]
- kvm-mirror-Don-t-close-target.patch [bz#1041301]
- kvm-mirror-Move-base-to-MirrorBlockJob.patch [bz#1041301]
- kvm-block-Add-commit_active_start.patch [bz#1041301]
- kvm-commit-Support-commit-active-layer.patch [bz#1041301]
- kvm-qemu-iotests-prefill-some-data-to-test-image.patch [bz#1041301]
- kvm-qemu-iotests-Update-test-cases-for-commit-active.patch [bz#1041301]
- kvm-commit-Remove-unused-check.patch [bz#1041301]
- kvm-blockdev-use-bdrv_getlength-in-qmp_drive_mirror.patch [bz#921890]
- kvm-qemu-iotests-make-assert_no_active_block_jobs-common.patch [bz#921890]
- kvm-block-drive-mirror-Check-for-NULL-backing_hd.patch [bz#921890]
- kvm-qemu-iotests-Extend-041-for-unbacked-mirroring.patch [bz#921890]
- kvm-qapi-schema-Update-description-for-NewImageMode.patch [bz#921890]
- kvm-block-drive-mirror-Reuse-backing-HD-for-sync-none.patch [bz#921890]
- kvm-qemu-iotests-Fix-test-041.patch [bz#921890]
- kvm-scsi-bus-fix-transfer-length-and-direction-for-VERIF.patch [bz#1035644]
- kvm-scsi-disk-fix-VERIFY-emulation.patch [bz#1035644]
- kvm-block-ensure-bdrv_drain_all-works-during-bdrv_delete.patch [bz#1041301]
- kvm-use-recommended-max-vcpu-count.patch [bz#998708]
- kvm-pc-Create-pc_compat_rhel-functions.patch [bz#1049706]
- kvm-pc-Enable-x2apic-by-default-on-more-recent-CPU-model.patch [bz#1049706]
- kvm-Build-all-subpackages-for-RHEV.patch [bz#1007204]
- Resolves: bz#1007204
  (qemu-img-rhev  qemu-kvm-rhev-tools are not built for qemu-kvm-1.5.3-3.el7)
- Resolves: bz#1035644
  (rhel7.0host + windows guest + virtio-win + 'chkdsk' in the guest gives qemu assertion in scsi_dma_complete)
- Resolves: bz#1041301
  (live snapshot merge (commit) of the active layer)
- Resolves: bz#1049706
  (MIss CPUID_EXT_X2APIC in Westmere cpu model)
- Resolves: bz#1053699
  (Backport Cancelled race condition fixes)
- Resolves: bz#921890
  (Core dump when block mirror with "sync" is "none" and mode is "absolute-paths")
- Resolves: bz#998708
  (qemu-kvm: maximum vcpu should be recommended maximum)

* Tue Jan 21 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-39.el7
- kvm-Revert-qdev-monitor-Fix-crash-when-device_add-is-cal.patch [bz#669524]
- kvm-Revert-qdev-Do-not-let-the-user-try-to-device_add-wh.patch [bz#669524]
- kvm-qdev-monitor-Clean-up-qdev_device_add-variable-namin.patch [bz#669524]
- kvm-qdev-monitor-Fix-crash-when-device_add-is-called.2.patch.patch [bz#669524]
- kvm-qdev-monitor-Avoid-qdev-as-variable-name.patch [bz#669524]
- kvm-qdev-monitor-Inline-qdev_init-for-device_add.patch [bz#669524]
- kvm-qdev-Do-not-let-the-user-try-to-device_add-when-it.2.patch.patch [bz#669524]
- kvm-qdev-monitor-Avoid-device_add-crashing-on-non-device.patch [bz#669524]
- kvm-qdev-monitor-Improve-error-message-for-device-nonexi.patch [bz#669524]
- kvm-exec-change-well-known-physical-sections-to-macros.patch [bz#1003535]
- kvm-exec-separate-sections-and-nodes-per-address-space.patch [bz#1003535]
- Resolves: bz#1003535
  (qemu-kvm core dump when boot vm with more than 32 virtio disks/nics)
- Resolves: bz#669524
  (Confusing error message from -device <unknown dev>)

* Fri Jan 17 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-38.el7
- kvm-intel-hda-fix-position-buffer.patch [bz#947785]
- kvm-The-calculation-of-bytes_xfer-in-qemu_put_buffer-is-.patch [bz#1003467]
- kvm-migration-Fix-rate-limit.patch [bz#1003467]
- kvm-audio-honor-QEMU_AUDIO_TIMER_PERIOD-instead-of-wakin.patch [bz#1017636]
- kvm-audio-Lower-default-wakeup-rate-to-100-times-second.patch [bz#1017636]
- kvm-audio-adjust-pulse-to-100Hz-wakeup-rate.patch [bz#1017636]
- kvm-pc-Fix-rhel6.-3dnow-3dnowext-compat-bits.patch [bz#918907]
- kvm-add-firmware-to-machine-options.patch [bz#1038603]
- kvm-switch-rhel7-machine-types-to-big-bios.patch [bz#1038603]
- kvm-add-bios-256k.bin-from-seabios-bin-1.7.2.2-10.el7.no.patch [bz#1038603]
- kvm-pci-fix-pci-bridge-fw-path.patch [bz#1034518]
- kvm-hw-cannot_instantiate_with_device_add_yet-due-to-poi.patch [bz#1031098]
- kvm-qdev-Document-that-pointer-properties-kill-device_ad.patch [bz#1031098]
- kvm-Add-back-no-hpet-but-ignore-it.patch [bz#1044742]
- Resolves: bz#1003467
  (Backport migration fixes from post qemu 1.6)
- Resolves: bz#1017636
  (PATCH: fix qemu using 50% host cpu when audio is playing)
- Resolves: bz#1031098
  (Disable device smbus-eeprom)
- Resolves: bz#1034518
  (boot order wrong with q35)
- Resolves: bz#1038603
  (make seabios 256k for rhel7 machine types)
- Resolves: bz#1044742
  (Cannot create guest on remote RHEL7 host using F20 virt-manager, libvirt's qemu -no-hpet detection is broken)
- Resolves: bz#918907
  (provide backwards-compatible RHEL specific machine types in QEMU - CPU features)
- Resolves: bz#947785
  (In rhel6.4 guest  sound recorder doesn't work when  playing audio)

* Wed Jan 15 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-37.el7
- kvm-bitmap-use-long-as-index.patch [bz#997559]
- kvm-memory-cpu_physical_memory_set_dirty_flags-result-is.patch [bz#997559]
- kvm-memory-cpu_physical_memory_set_dirty_range-return-vo.patch [bz#997559]
- kvm-exec-use-accessor-function-to-know-if-memory-is-dirt.patch [bz#997559]
- kvm-memory-create-function-to-set-a-single-dirty-bit.patch [bz#997559]
- kvm-exec-drop-useless-if.patch [bz#997559]
- kvm-exec-create-function-to-get-a-single-dirty-bit.patch [bz#997559]
- kvm-memory-make-cpu_physical_memory_is_dirty-return-bool.patch [bz#997559]
- kvm-memory-all-users-of-cpu_physical_memory_get_dirty-us.patch [bz#997559]
- kvm-memory-set-single-dirty-flags-when-possible.patch [bz#997559]
- kvm-memory-cpu_physical_memory_set_dirty_range-always-di.patch [bz#997559]
- kvm-memory-cpu_physical_memory_mask_dirty_range-always-c.patch [bz#997559]
- kvm-memory-use-bit-2-for-migration.patch [bz#997559]
- kvm-memory-make-sure-that-client-is-always-inside-range.patch [bz#997559]
- kvm-memory-only-resize-dirty-bitmap-when-memory-size-inc.patch [bz#997559]
- kvm-memory-cpu_physical_memory_clear_dirty_flag-result-i.patch [bz#997559]
- kvm-bitmap-Add-bitmap_zero_extend-operation.patch [bz#997559]
- kvm-memory-split-dirty-bitmap-into-three.patch [bz#997559]
- kvm-memory-unfold-cpu_physical_memory_clear_dirty_flag-i.patch [bz#997559]
- kvm-memory-unfold-cpu_physical_memory_set_dirty-in-its-o.patch [bz#997559]
- kvm-memory-unfold-cpu_physical_memory_set_dirty_flag.patch [bz#997559]
- kvm-memory-make-cpu_physical_memory_get_dirty-the-main-f.patch [bz#997559]
- kvm-memory-cpu_physical_memory_get_dirty-is-used-as-retu.patch [bz#997559]
- kvm-memory-s-mask-clear-cpu_physical_memory_mask_dirty_r.patch [bz#997559]
- kvm-memory-use-find_next_bit-to-find-dirty-bits.patch [bz#997559]
- kvm-memory-cpu_physical_memory_set_dirty_range-now-uses-.patch [bz#997559]
- kvm-memory-cpu_physical_memory_clear_dirty_range-now-use.patch [bz#997559]
- kvm-memory-s-dirty-clean-in-cpu_physical_memory_is_dirty.patch [bz#997559]
- kvm-memory-make-cpu_physical_memory_reset_dirty-take-a-l.patch [bz#997559]
- kvm-exec-Remove-unused-global-variable-phys_ram_fd.patch [bz#997559]
- kvm-memory-cpu_physical_memory_set_dirty_tracking-should.patch [bz#997559]
- kvm-memory-move-private-types-to-exec.c.patch [bz#997559]
- kvm-memory-split-cpu_physical_memory_-functions-to-its-o.patch [bz#997559]
- kvm-memory-unfold-memory_region_test_and_clear.patch [bz#997559]
- kvm-use-directly-cpu_physical_memory_-api-for-tracki.patch [bz#997559]
- kvm-refactor-start-address-calculation.patch [bz#997559]
- kvm-memory-move-bitmap-synchronization-to-its-own-functi.patch [bz#997559]
- kvm-memory-syncronize-kvm-bitmap-using-bitmaps-operation.patch [bz#997559]
- kvm-ram-split-function-that-synchronizes-a-range.patch [bz#997559]
- kvm-migration-synchronize-memory-bitmap-64bits-at-a-time.patch [bz#997559]
- Resolves: bz#997559
  (Improve live migration bitmap handling)

* Tue Jan 14 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-36.el7
- kvm-Add-support-statement-to-help-output.patch [bz#972773]
- kvm-__com.redhat_qxl_screendump-add-docs.patch [bz#903910]
- kvm-vl-Round-memory-sizes-below-2MiB-up-to-2MiB.patch [bz#999836]
- kvm-seccomp-exit-if-seccomp_init-fails.patch [bz#1044845]
- kvm-redhat-qemu-kvm.spec-require-python-for-build.patch [bz#1034876]
- kvm-redhat-qemu-kvm.spec-require-iasl.patch [bz#1034876]
- kvm-configure-make-iasl-option-actually-work.patch [bz#1034876]
- kvm-redhat-qemu-kvm.spec-add-cpp-as-build-dependency.patch [bz#1034876]
- kvm-acpi-build-disable-with-no-acpi.patch [bz#1045386]
- kvm-ehci-implement-port-wakeup.patch [bz#1039513]
- kvm-qdev-monitor-Fix-crash-when-device_add-is-called-wit.patch [bz#1026712 bz#1046007]
- kvm-block-vhdx-improve-error-message-and-.bdrv_check-imp.patch [bz#1035001]
- kvm-docs-updated-qemu-img-man-page-and-qemu-doc-to-refle.patch [bz#1017650]
- kvm-enable-pvticketlocks-by-default.patch [bz#1052340]
- kvm-fix-boot-strict-regressed-in-commit-6ef4716.patch [bz#997817]
- kvm-vl-make-boot_strict-variable-static-not-used-outside.patch [bz#997817]
- Resolves: bz#1017650
  (need to update qemu-img man pages on "VHDX" format)
- Resolves: bz#1026712
  (Qemu core dumpd when boot guest with driver name as "virtio-pci")
- Resolves: bz#1034876
  (export acpi tables to guests)
- Resolves: bz#1035001
  (VHDX: journal log should not be replayed by default, but rather via qemu-img check -r all)
- Resolves: bz#1039513
  (backport remote wakeup for ehci)
- Resolves: bz#1044845
  (QEMU seccomp sandbox - exit if seccomp_init() fails)
- Resolves: bz#1045386
  (qemu-kvm: hw/i386/acpi-build.c:135: acpi_get_pm_info: Assertion `obj' failed.)
- Resolves: bz#1046007
  (qemu-kvm aborted when hot plug PCI device to guest with romfile and rombar=0)
- Resolves: bz#1052340
  (pvticketlocks: default on)
- Resolves: bz#903910
  (RHEL7 does not have equivalent functionality for __com.redhat_qxl_screendump)
- Resolves: bz#972773
  (RHEL7: Clarify support statement in KVM help)
- Resolves: bz#997817
  (-boot order and -boot once regressed since RHEL-6)
- Resolves: bz#999836
  (-m 1 crashes)

* Thu Jan 09 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-35.el7
- kvm-option-Add-assigned-flag-to-QEMUOptionParameter.patch [bz#1033490]
- kvm-qcow2-refcount-Snapshot-update-for-zero-clusters.patch [bz#1033490]
- kvm-qemu-iotests-Snapshotting-zero-clusters.patch [bz#1033490]
- kvm-block-Image-file-option-amendment.patch [bz#1033490]
- kvm-qcow2-cache-Empty-cache.patch [bz#1033490]
- kvm-qcow2-cluster-Expand-zero-clusters.patch [bz#1033490]
- kvm-qcow2-Save-refcount-order-in-BDRVQcowState.patch [bz#1033490]
- kvm-qcow2-Implement-bdrv_amend_options.patch [bz#1033490]
- kvm-qcow2-Correct-bitmap-size-in-zero-expansion.patch [bz#1033490]
- kvm-qcow2-Free-only-newly-allocated-clusters-on-error.patch [bz#1033490]
- kvm-qcow2-Add-missing-space-in-error-message.patch [bz#1033490]
- kvm-qemu-iotest-qcow2-image-option-amendment.patch [bz#1033490]
- kvm-qemu-iotests-New-test-case-in-061.patch [bz#1033490]
- kvm-qemu-iotests-Preallocated-zero-clusters-in-061.patch [bz#1033490]
- Resolves: bz#1033490
  (Cannot upgrade/downgrade qcow2 images)

* Wed Jan 08 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-34.el7
- kvm-block-stream-Don-t-stream-unbacked-devices.patch [bz#965636]
- kvm-qemu-io-Let-open-pass-options-to-block-driver.patch [bz#1004347]
- kvm-qcow2.py-Subcommand-for-changing-header-fields.patch [bz#1004347]
- kvm-qemu-iotests-Remaining-error-propagation-adjustments.patch [bz#1004347]
- kvm-qemu-iotests-Add-test-for-inactive-L2-overlap.patch [bz#1004347]
- kvm-qemu-iotests-Adjust-test-result-039.patch [bz#1004347]
- kvm-virtio-net-don-t-update-mac_table-in-error-state.patch [bz#1048671]
- kvm-qcow2-Zero-initialise-first-cluster-for-new-images.patch [bz#1032904]
- Resolves: bz#1004347
  (Backport qcow2 corruption prevention patches)
- Resolves: bz#1032904
  (qemu-img can not create libiscsi qcow2_v3 image)
- Resolves: bz#1048671
  (virtio-net: mac_table change isn't recovered in error state)
- Resolves: bz#965636
  (streaming with no backing file should not do anything)

* Wed Jan 08 2014 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-33.el7
- kvm-block-qemu-iotests-for-vhdx-read-sample-dynamic-imag.patch [bz#879234]
- kvm-block-qemu-iotests-add-quotes-to-TEST_IMG-usage-io-p.patch [bz#879234]
- kvm-block-qemu-iotests-fix-_make_test_img-to-work-with-s.patch [bz#879234]
- kvm-block-qemu-iotests-add-quotes-to-TEST_IMG.base-usage.patch [bz#879234]
- kvm-block-qemu-iotests-add-quotes-to-TEST_IMG-usage-in-0.patch [bz#879234]
- kvm-block-qemu-iotests-removes-duplicate-double-quotes-i.patch [bz#879234]
- kvm-block-vhdx-minor-comments-and-typo-correction.patch [bz#879234]
- kvm-block-vhdx-add-header-update-capability.patch [bz#879234]
- kvm-block-vhdx-code-movement-VHDXMetadataEntries-and-BDR.patch [bz#879234]
- kvm-block-vhdx-log-support-struct-and-defines.patch [bz#879234]
- kvm-block-vhdx-break-endian-translation-functions-out.patch [bz#879234]
- kvm-block-vhdx-update-log-guid-in-header-and-first-write.patch [bz#879234]
- kvm-block-vhdx-code-movement-move-vhdx_close-above-vhdx_.patch [bz#879234]
- kvm-block-vhdx-log-parsing-replay-and-flush-support.patch [bz#879234]
- kvm-block-vhdx-add-region-overlap-detection-for-image-fi.patch [bz#879234]
- kvm-block-vhdx-add-log-write-support.patch [bz#879234]
- kvm-block-vhdx-write-support.patch [bz#879234]
- kvm-block-vhdx-remove-BAT-file-offset-bit-shifting.patch [bz#879234]
- kvm-block-vhdx-move-more-endian-translations-to-vhdx-end.patch [bz#879234]
- kvm-block-vhdx-break-out-code-operations-to-functions.patch [bz#879234]
- kvm-block-vhdx-fix-comment-typos-in-header-fix-incorrect.patch [bz#879234]
- kvm-block-vhdx-add-.bdrv_create-support.patch [bz#879234]
- kvm-block-vhdx-update-_make_test_img-to-filter-out-vhdx-.patch [bz#879234]
- kvm-block-qemu-iotests-for-vhdx-add-write-test-support.patch [bz#879234]
- kvm-block-vhdx-qemu-iotest-log-replay-of-data-sector.patch [bz#879234]
- Resolves: bz#879234
  ([RFE] qemu-img: Add/improve support for VHDX format)

* Mon Jan 06 2014 Michal Novotny <minovotn@redhat.com> - 1.5.3-32.el7
- kvm-block-change-default-of-.has_zero_init-to-0.patch.patch [bz#1007815]
- kvm-iscsi-factor-out-sector-conversions.patch.patch [bz#1007815]
- kvm-iscsi-add-logical-block-provisioning-information-to-.patch.patch [bz#1007815]
- kvm-iscsi-add-.bdrv_get_block_status.patch.patch.patch [bz#1007815]
- kvm-iscsi-split-discard-requests-in-multiple-parts.patch.patch.patch [bz#1007815]
- kvm-block-make-BdrvRequestFlags-public.patch.patch.patch [bz#1007815]
- kvm-block-add-flags-to-bdrv_-_write_zeroes.patch.patch.patch [bz#1007815]
- kvm-block-introduce-BDRV_REQ_MAY_UNMAP-request-flag.patch.patch.patch [bz#1007815]
- kvm-block-add-logical-block-provisioning-info-to-BlockDr.patch.patch.patch [bz#1007815]
- kvm-block-add-wrappers-for-logical-block-provisioning-in.patch.patch.patch [bz#1007815]
- kvm-block-iscsi-add-.bdrv_get_info.patch.patch [bz#1007815]
- kvm-block-add-BlockLimits-structure-to-BlockDriverState.patch.patch.patch [bz#1007815]
- kvm-block-raw-copy-BlockLimits-on-raw_open.patch.patch.patch [bz#1007815]
- kvm-block-honour-BlockLimits-in-bdrv_co_do_write_zeroes.patch.patch.patch [bz#1007815]
- kvm-block-honour-BlockLimits-in-bdrv_co_discard.patch.patch.patch [bz#1007815]
- kvm-iscsi-set-limits-in-BlockDriverState.patch.patch.patch [bz#1007815]
- kvm-iscsi-simplify-iscsi_co_discard.patch.patch.patch [bz#1007815]
- kvm-iscsi-add-bdrv_co_write_zeroes.patch.patch.patch [bz#1007815]
- kvm-block-introduce-bdrv_make_zero.patch.patch.patch [bz#1007815]
- kvm-block-get_block_status-fix-BDRV_BLOCK_ZERO-for-unall.patch.patch.patch [bz#1007815]
- kvm-qemu-img-add-support-for-fully-allocated-images.patch.patch.patch [bz#1007815]
- kvm-qemu-img-conditionally-zero-out-target-on-convert.patch.patch.patch [bz#1007815]
- kvm-block-generalize-BlockLimits-handling-to-cover-bdrv_.patch.patch.patch [bz#1007815]
- kvm-block-add-flags-to-BlockRequest.patch.patch.patch [bz#1007815]
- kvm-block-add-flags-argument-to-bdrv_co_write_zeroes-tra.patch.patch.patch [bz#1007815]
- kvm-block-add-bdrv_aio_write_zeroes.patch.patch.patch [bz#1007815]
- kvm-block-handle-ENOTSUP-from-discard-in-generic-code.patch.patch.patch [bz#1007815]
- kvm-block-make-bdrv_co_do_write_zeroes-stricter-in-produ.patch.patch.patch [bz#1007815]
- kvm-vpc-vhdx-add-get_info.patch.patch.patch [bz#1007815]
- kvm-block-drivers-add-discard-write_zeroes-properties-to.patch.patch.patch [bz#1007815]
- kvm-block-drivers-expose-requirement-for-write-same-alig.patch.patch.patch [bz#1007815]
- kvm-block-iscsi-remove-.bdrv_has_zero_init.patch.patch.patch [bz#1007815]
- kvm-block-iscsi-updated-copyright.patch.patch.patch [bz#1007815]
- kvm-block-iscsi-check-WRITE-SAME-support-differently-dep.patch.patch.patch [bz#1007815]
- kvm-scsi-disk-catch-write-protection-errors-in-UNMAP.patch.patch.patch [bz#1007815]
- kvm-scsi-disk-reject-ANCHOR-1-for-UNMAP-and-WRITE-SAME-c.patch.patch.patch [bz#1007815]
- kvm-scsi-disk-correctly-implement-WRITE-SAME.patch.patch.patch [bz#1007815]
- kvm-scsi-disk-fix-WRITE-SAME-with-large-non-zero-payload.patch.patch.patch [bz#1007815]
- kvm-raw-posix-implement-write_zeroes-with-MAY_UNMAP-for-.patch.patch.patch.patch [bz#1007815]
- kvm-raw-posix-implement-write_zeroes-with-MAY_UNMAP-for-.patch.patch.patch.patch.patch [bz#1007815]
- kvm-raw-posix-add-support-for-write_zeroes-on-XFS-and-bl.patch.patch [bz#1007815]
- kvm-qemu-iotests-033-is-fast.patch.patch [bz#1007815]
- kvm-qemu-img-add-support-for-skipping-zeroes-in-input-du.patch.patch [bz#1007815]
- kvm-qemu-img-fix-usage-instruction-for-qemu-img-convert.patch.patch [bz#1007815]
- kvm-block-iscsi-set-bdi-cluster_size.patch.patch [bz#1007815]
- kvm-block-add-opt_transfer_length-to-BlockLimits.patch.patch [bz#1039557]
- kvm-block-iscsi-set-bs-bl.opt_transfer_length.patch.patch [bz#1039557]
- kvm-qemu-img-dynamically-adjust-iobuffer-size-during-con.patch.patch [bz#1039557]
- kvm-qemu-img-round-down-request-length-to-an-aligned-sec.patch.patch [bz#1039557]
- kvm-qemu-img-decrease-progress-update-interval-on-conver.patch.patch [bz#1039557]
- Resolves: bz#1007815
  (fix WRITE SAME support)
- Resolves: bz#1039557
  (optimize qemu-img for thin provisioned images)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 10:1.5.3-31
- Mass rebuild 2013-12-27

* Wed Dec 18 2013 Michal Novotny <minovotn@redhat.com> - 1.5.3-30.el7
- kvm-Revert-HMP-Disable-drive_add-for-Red-Hat-Enterprise-2.patch.patch [bz#889051]
- Resolves: bz#889051
  (Commands "__com.redhat_drive_add/del" don' t exist in RHEL7.0)

* Wed Dec 18 2013 Michal Novotny <minovotn@redhat.com> - 1.5.3-29.el7
- kvm-QMP-Forward-port-__com.redhat_drive_del-from-RHEL-6.patch [bz#889051]
- kvm-QMP-Forward-port-__com.redhat_drive_add-from-RHEL-6.patch [bz#889051]
- kvm-HMP-Forward-port-__com.redhat_drive_add-from-RHEL-6.patch [bz#889051]
- kvm-QMP-Document-throttling-parameters-of-__com.redhat_d.patch [bz#889051]
- kvm-HMP-Disable-drive_add-for-Red-Hat-Enterprise-Linux.patch [bz#889051]
- Resolves: bz#889051
  (Commands "__com.redhat_drive_add/del" don' t exist in RHEL7.0)

* Wed Dec 18 2013 Michal Novotny <minovotn@redhat.com> - 1.5.3-28.el7
- kvm-virtio_pci-fix-level-interrupts-with-irqfd.patch [bz#1035132]
- Resolves: bz#1035132
  (fail to boot and call trace with x-data-plane=on specified for rhel6.5 guest)

* Wed Dec 18 2013 Michal Novotny <minovotn@redhat.com> - 1.5.3-27.el7
- Change systemd service location [bz#1025217]
- kvm-vmdk-Allow-read-only-open-of-VMDK-version-3.patch [bz#1007710 bz#1029852]
- Resolves: bz#1007710
  ([RFE] Enable qemu-img to support VMDK version 3)
- Resolves: bz#1025217
  (systemd can't control ksm.service and ksmtuned.service)
- Resolves: bz#1029852
  (qemu-img fails to convert vmdk image with "qemu-img: Could not open 'image.vmdk'")

* Wed Dec 18 2013 Michal Novotny <minovotn@redhat.com> - 1.5.3-26.el7
- Add BuildRequires to libRDMAcm-devel for RDMA support [bz#1011720]
- kvm-add-a-header-file-for-atomic-operations.patch [bz#1011720]
- kvm-savevm-Fix-potential-memory-leak.patch [bz#1011720]
- kvm-migration-Fail-migration-on-bdrv_flush_all-error.patch [bz#1011720]
- kvm-rdma-add-documentation.patch [bz#1011720]
- kvm-rdma-introduce-qemu_update_position.patch [bz#1011720]
- kvm-rdma-export-yield_until_fd_readable.patch [bz#1011720]
- kvm-rdma-export-throughput-w-MigrationStats-QMP.patch [bz#1011720]
- kvm-rdma-introduce-qemu_file_mode_is_not_valid.patch [bz#1011720]
- kvm-rdma-introduce-qemu_ram_foreach_block.patch [bz#1011720]
- kvm-rdma-new-QEMUFileOps-hooks.patch [bz#1011720]
- kvm-rdma-introduce-capability-x-rdma-pin-all.patch [bz#1011720]
- kvm-rdma-update-documentation-to-reflect-new-unpin-suppo.patch [bz#1011720]- kvm-rdma-bugfix-ram_control_save_page.patch [bz#1011720]
- kvm-rdma-introduce-ram_handle_compressed.patch [bz#1011720]
- kvm-rdma-core-logic.patch [bz#1011720]
- kvm-rdma-send-pc.ram.patch [bz#1011720]
- kvm-rdma-allow-state-transitions-between-other-states-be.patch [bz#1011720]
- kvm-rdma-introduce-MIG_STATE_NONE-and-change-MIG_STATE_S.patch [bz#1011720]
- kvm-rdma-account-for-the-time-spent-in-MIG_STATE_SETUP-t.patch [bz#1011720]
- kvm-rdma-bugfix-make-IPv6-support-work.patch [bz#1011720]
- kvm-rdma-forgot-to-turn-off-the-debugging-flag.patch [bz#1011720]
- kvm-rdma-correct-newlines-in-error-statements.patch [bz#1011720]
- kvm-rdma-don-t-use-negative-index-to-array.patch [bz#1011720]
- kvm-rdma-qemu_rdma_post_send_control-uses-wrongly-RDMA_W.patch [bz#1011720]
- kvm-rdma-use-DRMA_WRID_READY.patch [bz#1011720]
- kvm-rdma-memory-leak-RDMAContext-host.patch [bz#1011720]
- kvm-rdma-use-resp.len-after-validation-in-qemu_rdma_regi.patch [bz#1011720]
- kvm-rdma-validate-RDMAControlHeader-len.patch [bz#1011720]
- kvm-rdma-check-if-RDMAControlHeader-len-match-transferre.patch [bz#1011720]
- kvm-rdma-proper-getaddrinfo-handling.patch [bz#1011720]
- kvm-rdma-IPv6-over-Ethernet-RoCE-is-broken-in-linux-work.patch [bz#1011720]
- kvm-rdma-remaining-documentation-fixes.patch [bz#1011720]
- kvm-rdma-silly-ipv6-bugfix.patch [bz#1011720]
- kvm-savevm-fix-wrong-initialization-by-ram_control_load_.patch [bz#1011720]
- kvm-arch_init-right-return-for-ram_save_iterate.patch [bz#1011720]
- kvm-rdma-clean-up-of-qemu_rdma_cleanup.patch [bz#1011720]
- kvm-rdma-constify-ram_chunk_-index-start-end.patch [bz#1011720]
- kvm-migration-Fix-debug-print-type.patch [bz#1011720]
- kvm-arch_init-make-is_zero_page-accept-size.patch [bz#1011720]
- kvm-migration-ram_handle_compressed.patch [bz#1011720]
- kvm-migration-fix-spice-migration.patch [bz#1011720]
- kvm-pci-assign-cap-number-of-devices-that-can-be-assigne.patch [bz#678368]
- kvm-vfio-cap-number-of-devices-that-can-be-assigned.patch [bz#678368]
- kvm-Revert-usb-tablet-Don-t-claim-wakeup-capability-for-.patch [bz#1039513]
- kvm-mempath-prefault-pages-manually-v4.patch [bz#1026554]
- Resolves: bz#1011720
  ([HP 7.0 Feat]: Backport RDMA based live guest migration changes from upstream to RHEL7.0 KVM)
- Resolves: bz#1026554
  (qemu: mempath: prefault pages manually)
- Resolves: bz#1039513
  (backport remote wakeup for ehci)
- Resolves: bz#678368
  (RFE: Support more than 8 assigned devices)

* Wed Dec 18 2013 Michal Novotny <minovotn@redhat.com> - 1.5.3-25.el7
- kvm-Change-package-description.patch [bz#1017696]
- kvm-seccomp-add-kill-to-the-syscall-whitelist.patch [bz#1026314]
- kvm-json-parser-fix-handling-of-large-whole-number-value.patch [bz#997915]
- kvm-qapi-add-QMP-input-test-for-large-integers.patch [bz#997915]
- kvm-qapi-fix-visitor-serialization-tests-for-numbers-dou.patch [bz#997915]
- kvm-qapi-add-native-list-coverage-for-visitor-serializat.patch [bz#997915]
- kvm-qapi-add-native-list-coverage-for-QMP-output-visitor.patch [bz#997915]
- kvm-qapi-add-native-list-coverage-for-QMP-input-visitor-.patch [bz#997915]
- kvm-qapi-lack-of-two-commas-in-dict.patch [bz#997915]
- kvm-tests-QAPI-schema-parser-tests.patch [bz#997915]
- kvm-tests-Use-qapi-schema-test.json-as-schema-parser-tes.patch [bz#997915]
- kvm-qapi.py-Restructure-lexer-and-parser.patch [bz#997915]
- kvm-qapi.py-Decent-syntax-error-reporting.patch [bz#997915]
- kvm-qapi.py-Reject-invalid-characters-in-schema-file.patch [bz#997915]
- kvm-qapi.py-Fix-schema-parser-to-check-syntax-systematic.patch [bz#997915]
- kvm-qapi.py-Fix-diagnosing-non-objects-at-a-schema-s-top.patch [bz#997915]
- kvm-qapi.py-Rename-expr_eval-to-expr-in-parse_schema.patch [bz#997915]
- kvm-qapi.py-Permit-comments-starting-anywhere-on-the-lin.patch [bz#997915]
- kvm-scripts-qapi.py-Avoid-syntax-not-supported-by-Python.patch [bz#997915]
- kvm-tests-Fix-schema-parser-test-for-in-tree-build.patch [bz#997915]
- Resolves: bz#1017696
  ([branding] remove references to dynamic translation and user-mode emulation)
- Resolves: bz#1026314
  (qemu-kvm hang when use '-sandbox on'+'vnc'+'hda')
- Resolves: bz#997915
  (Backport new QAPI parser proactively to help developers and avoid silly conflicts)
    
* Tue Dec 17 2013 Michal Novotny <minovotn@redhat.com> - 1.5.3-24.el7
- kvm-range-add-Range-structure.patch [bz#1034876]
- kvm-range-add-Range-to-typedefs.patch [bz#1034876]
- kvm-range-add-min-max-operations-on-ranges.patch [bz#1034876]
- kvm-qdev-Add-SIZE-type-to-qdev-properties.patch [bz#1034876]
- kvm-qapi-make-visit_type_size-fallback-to-type_int.patch [bz#1034876]
- kvm-pc-move-IO_APIC_DEFAULT_ADDRESS-to-include-hw-i386-i.patch [bz#1034876]
- kvm-pci-add-helper-to-retrieve-the-64-bit-range.patch [bz#1034876]
- kvm-pci-fix-up-w64-size-calculation-helper.patch [bz#1034876]
- kvm-refer-to-FWCfgState-explicitly.patch [bz#1034876]
- kvm-fw_cfg-move-typedef-to-qemu-typedefs.h.patch [bz#1034876]
- kvm-arch_init-align-MR-size-to-target-page-size.patch [bz#1034876]
- kvm-loader-store-FW-CFG-ROM-files-in-RAM.patch [bz#1034876]
- kvm-pci-store-PCI-hole-ranges-in-guestinfo-structure.patch [bz#1034876]
- kvm-pc-pass-PCI-hole-ranges-to-Guests.patch [bz#1034876]
- kvm-pc-replace-i440fx_common_init-with-i440fx_init.patch [bz#1034876]
- kvm-pc-don-t-access-fw-cfg-if-NULL.patch [bz#1034876]
- kvm-pc-add-I440FX-QOM-cast-macro.patch [bz#1034876]
- kvm-pc-limit-64-bit-hole-to-2G-by-default.patch [bz#1034876]
- kvm-q35-make-pci-window-address-size-match-guest-cfg.patch [bz#1034876]
- kvm-q35-use-64-bit-window-programmed-by-guest.patch [bz#1034876]
- kvm-piix-use-64-bit-window-programmed-by-guest.patch [bz#1034876]
- kvm-pc-fix-regression-for-64-bit-PCI-memory.patch [bz#1034876]
- kvm-cleanup-object.h-include-error.h-directly.patch [bz#1034876]
- kvm-qom-cleanup-struct-Error-references.patch [bz#1034876]
- kvm-qom-add-pointer-to-int-property-helpers.patch [bz#1034876]
- kvm-fw_cfg-interface-to-trigger-callback-on-read.patch [bz#1034876]
- kvm-loader-support-for-unmapped-ROM-blobs.patch [bz#1034876]
- kvm-pcie_host-expose-UNMAPPED-macro.patch [bz#1034876]
- kvm-pcie_host-expose-address-format.patch [bz#1034876]
- kvm-q35-use-macro-for-MCFG-property-name.patch [bz#1034876]
- kvm-q35-expose-mmcfg-size-as-a-property.patch [bz#1034876]
- kvm-i386-add-ACPI-table-files-from-seabios.patch [bz#1034876]
- kvm-acpi-add-rules-to-compile-ASL-source.patch [bz#1034876]
- kvm-acpi-pre-compiled-ASL-files.patch [bz#1034876]
- kvm-acpi-ssdt-pcihp-updat-generated-file.patch [bz#1034876]
- kvm-loader-use-file-path-size-from-fw_cfg.h.patch [bz#1034876]
- kvm-i386-add-bios-linker-loader.patch [bz#1034876]
- kvm-loader-allow-adding-ROMs-in-done-callbacks.patch [bz#1034876]
- kvm-i386-define-pc-guest-info.patch [bz#1034876]
- kvm-acpi-piix-add-macros-for-acpi-property-names.patch [bz#1034876]
- kvm-piix-APIs-for-pc-guest-info.patch [bz#1034876]
- kvm-ich9-APIs-for-pc-guest-info.patch [bz#1034876]
- kvm-pvpanic-add-API-to-access-io-port.patch [bz#1034876]
- kvm-hpet-add-API-to-find-it.patch [bz#1034876]
- kvm-hpet-fix-build-with-CONFIG_HPET-off.patch [bz#1034876]
- kvm-acpi-add-interface-to-access-user-installed-tables.patch [bz#1034876]
- kvm-pc-use-new-api-to-add-builtin-tables.patch [bz#1034876]
- kvm-i386-ACPI-table-generation-code-from-seabios.patch [bz#1034876]
- kvm-ssdt-fix-PBLK-length.patch [bz#1034876]
- kvm-ssdt-proc-update-generated-file.patch [bz#1034876]
- kvm-pc-disable-pci-info.patch [bz#1034876]
- kvm-acpi-build-fix-build-on-glib-2.22.patch [bz#1034876]
- kvm-acpi-build-fix-build-on-glib-2.14.patch [bz#1034876]
- kvm-acpi-build-fix-support-for-glib-2.22.patch [bz#1034876]
- kvm-acpi-build-Fix-compiler-warning-missing-gnu_printf-f.patch [bz#1034876]
- kvm-exec-Fix-prototype-of-phys_mem_set_alloc-and-related.patch [bz#1034876]
- Resolves: bz#1034876
  (export acpi tables to guests)

* Tue Dec 17 2013 Michal Novotny <minovotn@redhat.com> - 1.5.3-23.el7
- kvm-qdev-monitor-Unref-device-when-device_add-fails.patch [bz#1003773]
- kvm-qdev-Drop-misleading-qdev_free-function.patch [bz#1003773]
- kvm-blockdev-fix-drive_init-opts-and-bs_opts-leaks.patch [bz#1003773]
- kvm-libqtest-rename-qmp-to-qmp_discard_response.patch [bz#1003773]
- kvm-libqtest-add-qmp-fmt-.-QDict-function.patch [bz#1003773]
- kvm-blockdev-test-add-test-case-for-drive_add-duplicate-.patch [bz#1003773]
- kvm-qdev-monitor-test-add-device_add-leak-test-cases.patch [bz#1003773]
- kvm-qtest-Use-display-none-by-default.patch [bz#1003773]
- Resolves: bz#1003773
  (When virtio-blk-pci device with dataplane is failed to be added, the drive cannot be released.)

* Tue Dec 17 2013 Michal Novotny <minovotn@redhat.com> - 1.5.3-22.el7
- Fix ksmtuned with set_process_name=1 [bz#1027420]
- Fix committed memory when no qemu-kvm running [bz#1027418]
- kvm-virtio-net-fix-the-memory-leak-in-rxfilter_notify.patch [bz#1033810]
- kvm-qom-Fix-memory-leak-in-object_property_set_link.patch [bz#1033810]
- kvm-fix-intel-hda-live-migration.patch [bz#1036537]
- kvm-vfio-pci-Release-all-MSI-X-vectors-when-disabled.patch [bz#1029743]
- kvm-Query-KVM-for-available-memory-slots.patch [bz#921490]
- kvm-block-Dont-ignore-previously-set-bdrv_flags.patch [bz#1039501]
- kvm-cleanup-trace-events.pl-New.patch [bz#997832]
- kvm-slavio_misc-Fix-slavio_led_mem_readw-_writew-tracepo.patch [bz#997832]
- kvm-milkymist-minimac2-Fix-minimac2_read-_write-tracepoi.patch [bz#997832]
- kvm-trace-events-Drop-unused-events.patch [bz#997832]
- kvm-trace-events-Fix-up-source-file-comments.patch [bz#997832]
- kvm-trace-events-Clean-up-with-scripts-cleanup-trace-eve.patch [bz#997832]
- kvm-trace-events-Clean-up-after-removal-of-old-usb-host-.patch [bz#997832]
- kvm-net-Update-netdev-peer-on-link-change.patch [bz#1027571]
- Resolves: bz#1027418
  (ksmtuned committed_memory() still returns "", not 0, when no qemu running)
- Resolves: bz#1027420
  (ksmtuned can’t handle libvirt WITH set_process_name=1)
- Resolves: bz#1027571
  ([virtio-win]win8.1 guest network can not resume automatically after do "set_link tap1 on")
- Resolves: bz#1029743
  (qemu-kvm core dump after hot plug/unplug 82576 PF about 100 times)
- Resolves: bz#1033810
  (memory leak in using object_get_canonical_path())
- Resolves: bz#1036537
  (Cross version migration from RHEL6.5 host to RHEL7.0 host with sound device failed.)
- Resolves: bz#1039501
  ([provisioning] discard=on broken)
- Resolves: bz#921490
  (qemu-kvm core dumped after hot plugging more than 11 VF through vfio-pci)
- Resolves: bz#997832
  (Backport trace fixes proactively to avoid confusion and silly conflicts)

* Tue Dec 03 2013 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-21.el7
- kvm-scsi-Allocate-SCSITargetReq-r-buf-dynamically-CVE-20.patch [bz#1007334]
- Resolves: bz#1007334
  (CVE-2013-4344 qemu-kvm: qemu: buffer overflow in scsi_target_emulate_report_luns [rhel-7.0])

* Thu Nov 28 2013 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-20.el7
- kvm-pc-drop-virtio-balloon-pci-event_idx-compat-property.patch [bz#1029539]
- kvm-virtio-net-only-delete-bh-that-existed.patch [bz#922463]
- kvm-virtio-net-broken-RX-filtering-logic-fixed.patch [bz#1029370]
- kvm-block-Avoid-unecessary-drv-bdrv_getlength-calls.patch [bz#1025138]
- kvm-block-Round-up-total_sectors.patch [bz#1025138]
- kvm-doc-fix-hardcoded-helper-path.patch [bz#1016952]
- kvm-introduce-RFQDN_REDHAT-RHEL-6-7-fwd.patch [bz#971933]
- kvm-error-reason-in-BLOCK_IO_ERROR-BLOCK_JOB_ERROR-event.patch [bz#971938]
- kvm-improve-debuggability-of-BLOCK_IO_ERROR-BLOCK_JOB_ER.patch [bz#895041]
- kvm-vfio-pci-Fix-multifunction-on.patch [bz#1029275]
- kvm-qcow2-Change-default-for-new-images-to-compat-1.1.patch [bz#1026739]
- kvm-qcow2-change-default-for-new-images-to-compat-1.1-pa.patch [bz#1026739]
- kvm-rng-egd-offset-the-point-when-repeatedly-read-from-t.patch [bz#1032862]
- kvm-Fix-rhel-rhev-conflict-for-qemu-kvm-common.patch [bz#1033463]
- Resolves: bz#1016952
  (qemu-kvm man page guide wrong path for qemu-bridge-helper)
- Resolves: bz#1025138
  (Read/Randread/Randrw performance regression)
- Resolves: bz#1026739
  (qcow2: Switch to compat=1.1 default for new images)
- Resolves: bz#1029275
  (Guest only find one 82576 VF(function 0) while use multifunction)
- Resolves: bz#1029370
  ([whql][netkvm][wlk] Virtio-net device handles RX multicast filtering improperly)
- Resolves: bz#1029539
  (Machine type rhel6.1.0 and  balloon device cause migration fail from RHEL6.5 host to RHEL7.0 host)
- Resolves: bz#1032862
  (virtio-rng-egd: repeatedly read same random data-block w/o considering the buffer offset)
- Resolves: bz#1033463
  (can not upgrade qemu-kvm-common to qemu-kvm-common-rhev due to conflicts)
- Resolves: bz#895041
  (QMP: forward port I/O error debug messages)
- Resolves: bz#922463
  (qemu-kvm core dump when virtio-net multi queue guest hot-unpluging vNIC)
- Resolves: bz#971933
  (QMP: add RHEL's vendor extension prefix)
- Resolves: bz#971938
  (QMP: Add error reason to BLOCK_IO_ERROR event)

* Mon Nov 11 2013 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-19.el7
- kvm-qapi-qapi-visit.py-fix-list-handling-for-union-types.patch [bz#848203]
- kvm-qapi-qapi-visit.py-native-list-support.patch [bz#848203]
- kvm-qapi-enable-generation-of-native-list-code.patch [bz#848203]
- kvm-net-add-support-of-mac-programming-over-macvtap-in-Q.patch [bz#848203]
- Resolves: bz#848203
  (MAC Programming for virtio over macvtap - qemu-kvm support)

* Fri Nov 08 2013 Michal Novotny <minovotn@redhat.com> - 1.5.3-18.el7
- Removing leaked patch kvm-e1000-rtl8139-update-HMP-NIC-when-every-bit-is-writt.patch

* Thu Nov 07 2013 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-17.el7
- kvm-pci-assign-Add-MSI-affinity-support.patch [bz#1025877]
- kvm-Fix-potential-resource-leak-missing-fclose.patch [bz#1025877]
- kvm-pci-assign-remove-the-duplicate-function-name-in-deb.patch [bz#1025877]
- kvm-Remove-s390-ccw-img-loader.patch [bz#1017682]
- kvm-Fix-vscclient-installation.patch [bz#1017681]
- kvm-Change-qemu-bridge-helper-permissions-to-4755.patch [bz#1017689]
- kvm-net-update-nic-info-during-device-reset.patch [bz#922589]
- kvm-net-e1000-update-network-information-when-macaddr-is.patch [bz#922589]
- kvm-net-rtl8139-update-network-information-when-macaddr-.patch [bz#922589]
- kvm-virtio-net-fix-up-HMP-NIC-info-string-on-reset.patch [bz#1026689]
- kvm-vfio-pci-VGA-quirk-update.patch [bz#1025477]
- kvm-vfio-pci-Add-support-for-MSI-affinity.patch [bz#1025477]
- kvm-vfio-pci-Test-device-reset-capabilities.patch [bz#1026550]
- kvm-vfio-pci-Lazy-PCI-option-ROM-loading.patch [bz#1026550]
- kvm-vfio-pci-Cleanup-error_reports.patch [bz#1026550]
- kvm-vfio-pci-Add-dummy-PCI-ROM-write-accessor.patch [bz#1026550]
- kvm-vfio-pci-Fix-endian-issues-in-vfio_pci_size_rom.patch [bz#1026550]
- kvm-linux-headers-Update-to-include-vfio-pci-hot-reset-s.patch [bz#1025472]
- kvm-vfio-pci-Implement-PCI-hot-reset.patch [bz#1025472]
- kvm-linux-headers-Update-for-KVM-VFIO-device.patch [bz#1025474]
- kvm-vfio-pci-Make-use-of-new-KVM-VFIO-device.patch [bz#1025474]
- kvm-vmdk-Fix-vmdk_parse_extents.patch [bz#995866]
- kvm-vmdk-fix-VMFS-extent-parsing.patch [bz#995866]
- kvm-e1000-rtl8139-update-HMP-NIC-when-every-bit-is-writt.patch [bz#922589]
- kvm-don-t-disable-ctrl_mac_addr-feature-for-6.5-machine-.patch [bz#1005039]
- Resolves: bz#1005039
  (add compat property to disable ctrl_mac_addr feature)
- Resolves: bz#1017681
  (rpmdiff test "Multilib regressions": vscclient is a libtool script on s390/s390x/ppc/ppc64)
- Resolves: bz#1017682
  (/usr/share/qemu-kvm/s390-ccw.img need not be distributed)
- Resolves: bz#1017689
  (/usr/libexec/qemu-bridge-helper permissions should be 4755)
- Resolves: bz#1025472
  (Nvidia GPU device assignment - qemu-kvm - bus reset support)
- Resolves: bz#1025474
  (Nvidia GPU device assignment - qemu-kvm - NoSnoop support)
- Resolves: bz#1025477
  (VFIO MSI affinity)
- Resolves: bz#1025877
  (pci-assign lacks MSI affinity support)
- Resolves: bz#1026550
  (QEMU VFIO update ROM loading code)
- Resolves: bz#1026689
  (virtio-net: macaddr is reset but network info of monitor isn't updated)
- Resolves: bz#922589
  (e1000/rtl8139: qemu mac address can not be changed via set the hardware address in guest)
- Resolves: bz#995866
  (fix vmdk support to ESX images)

* Thu Nov 07 2013 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-16.el7
- kvm-block-drop-bs_snapshots-global-variable.patch [bz#1026524]
- kvm-block-move-snapshot-code-in-block.c-to-block-snapsho.patch [bz#1026524]
- kvm-block-fix-vvfat-error-path-for-enable_write_target.patch [bz#1026524]
- kvm-block-Bugfix-format-and-snapshot-used-in-drive-optio.patch [bz#1026524]
- kvm-iscsi-use-bdrv_new-instead-of-stack-structure.patch [bz#1026524]
- kvm-qcow2-Add-corrupt-bit.patch [bz#1004347]
- kvm-qcow2-Metadata-overlap-checks.patch [bz#1004347]
- kvm-qcow2-Employ-metadata-overlap-checks.patch [bz#1004347]
- kvm-qcow2-refcount-Move-OFLAG_COPIED-checks.patch [bz#1004347]
- kvm-qcow2-refcount-Repair-OFLAG_COPIED-errors.patch [bz#1004347]
- kvm-qcow2-refcount-Repair-shared-refcount-blocks.patch [bz#1004347]
- kvm-qcow2_check-Mark-image-consistent.patch [bz#1004347]
- kvm-qemu-iotests-Overlapping-cluster-allocations.patch [bz#1004347]
- kvm-w32-Fix-access-to-host-devices-regression.patch [bz#1026524]
- kvm-add-qemu-img-convert-n-option-skip-target-volume-cre.patch [bz#1026524]
- kvm-bdrv-Use-Error-for-opening-images.patch [bz#1026524]
- kvm-bdrv-Use-Error-for-creating-images.patch [bz#1026524]
- kvm-block-Error-parameter-for-open-functions.patch [bz#1026524]
- kvm-block-Error-parameter-for-create-functions.patch [bz#1026524]
- kvm-qemu-img-create-Emit-filename-on-error.patch [bz#1026524]
- kvm-qcow2-Use-Error-parameter.patch [bz#1026524]
- kvm-qemu-iotests-Adjustments-due-to-error-propagation.patch [bz#1026524]
- kvm-block-raw-Employ-error-parameter.patch [bz#1026524]
- kvm-block-raw-win32-Employ-error-parameter.patch [bz#1026524]
- kvm-blkdebug-Employ-error-parameter.patch [bz#1026524]
- kvm-blkverify-Employ-error-parameter.patch [bz#1026524]
- kvm-block-raw-posix-Employ-error-parameter.patch [bz#1026524]
- kvm-block-raw-win32-Always-use-errno-in-hdev_open.patch [bz#1026524]
- kvm-qmp-Documentation-for-BLOCK_IMAGE_CORRUPTED.patch [bz#1004347]
- kvm-qcow2-Correct-snapshots-size-for-overlap-check.patch [bz#1004347]
- kvm-qcow2-CHECK_OFLAG_COPIED-is-obsolete.patch [bz#1004347]
- kvm-qcow2-Correct-endianness-in-overlap-check.patch [bz#1004347]
- kvm-qcow2-Switch-L1-table-in-a-single-sequence.patch [bz#1004347]
- kvm-qcow2-Use-pread-for-inactive-L1-in-overlap-check.patch [bz#1004347]
- kvm-qcow2-Remove-wrong-metadata-overlap-check.patch [bz#1004347]
- kvm-qcow2-Use-negated-overflow-check-mask.patch [bz#1004347]
- kvm-qcow2-Make-overlap-check-mask-variable.patch [bz#1004347]
- kvm-qcow2-Add-overlap-check-options.patch [bz#1004347]
- kvm-qcow2-Array-assigning-options-to-OL-check-bits.patch [bz#1004347]
- kvm-qcow2-Add-more-overlap-check-bitmask-macros.patch [bz#1004347]
- kvm-qcow2-Evaluate-overlap-check-options.patch [bz#1004347]
- kvm-qapi-types.py-Split-off-generate_struct_fields.patch [bz#978402]
- kvm-qapi-types.py-Fix-enum-struct-sizes-on-i686.patch [bz#978402]
- kvm-qapi-types-visit.py-Pass-whole-expr-dict-for-structs.patch [bz#978402]
- kvm-qapi-types-visit.py-Inheritance-for-structs.patch [bz#978402]
- kvm-blockdev-Introduce-DriveInfo.enable_auto_del.patch [bz#978402]
- kvm-Implement-qdict_flatten.patch [bz#978402]
- kvm-blockdev-blockdev-add-QMP-command.patch [bz#978402]
- kvm-blockdev-Separate-ID-generation-from-DriveInfo-creat.patch [bz#978402]
- kvm-blockdev-Pass-QDict-to-blockdev_init.patch [bz#978402]
- kvm-blockdev-Move-parsing-of-media-option-to-drive_init.patch [bz#978402]
- kvm-blockdev-Move-parsing-of-if-option-to-drive_init.patch [bz#978402]
- kvm-blockdev-Moving-parsing-of-geometry-options-to-drive.patch [bz#978402]
- kvm-blockdev-Move-parsing-of-boot-option-to-drive_init.patch [bz#978402]
- kvm-blockdev-Move-bus-unit-index-processing-to-drive_ini.patch [bz#978402]
- kvm-blockdev-Move-virtio-blk-device-creation-to-drive_in.patch [bz#978402]
- kvm-blockdev-Remove-IF_-check-for-read-only-blockdev_ini.patch [bz#978402]
- kvm-qemu-iotests-Check-autodel-behaviour-for-device_del.patch [bz#978402]
- kvm-blockdev-Remove-media-parameter-from-blockdev_init.patch [bz#978402]
- kvm-blockdev-Don-t-disable-COR-automatically-with-blockd.patch [bz#978402]
- kvm-blockdev-blockdev_init-error-conversion.patch [bz#978402]
- kvm-sd-Avoid-access-to-NULL-BlockDriverState.patch [bz#978402]
- kvm-blockdev-fix-cdrom-read_only-flag.patch [bz#978402]
- kvm-block-fix-backing-file-overriding.patch [bz#978402]
- kvm-block-Disable-BDRV_O_COPY_ON_READ-for-the-backing-fi.patch [bz#978402]
- kvm-block-Don-t-copy-backing-file-name-on-error.patch [bz#978402]
- kvm-qemu-iotests-Try-creating-huge-qcow2-image.patch [bz#980771]
- kvm-block-move-qmp-and-info-dump-related-code-to-block-q.patch [bz#980771]
- kvm-block-dump-snapshot-and-image-info-to-specified-outp.patch [bz#980771]
- kvm-block-add-snapshot-info-query-function-bdrv_query_sn.patch [bz#980771]
- kvm-block-add-image-info-query-function-bdrv_query_image.patch [bz#980771]
- kvm-qmp-add-ImageInfo-in-BlockDeviceInfo-used-by-query-b.patch [bz#980771]
- kvm-vmdk-Implement-.bdrv_has_zero_init.patch [bz#980771]
- kvm-qemu-iotests-Add-basic-ability-to-use-binary-sample-.patch [bz#980771]
- kvm-qemu-iotests-Quote-TEST_IMG-and-TEST_DIR-usage.patch [bz#980771]
- kvm-qemu-iotests-fix-test-case-059.patch [bz#980771]
- kvm-qapi-Add-ImageInfoSpecific-type.patch [bz#980771]
- kvm-block-Add-bdrv_get_specific_info.patch [bz#980771]
- kvm-block-qapi-Human-readable-ImageInfoSpecific-dump.patch [bz#980771]
- kvm-qcow2-Add-support-for-ImageInfoSpecific.patch [bz#980771]
- kvm-qemu-iotests-Discard-specific-info-in-_img_info.patch [bz#980771]
- kvm-qemu-iotests-Additional-info-from-qemu-img-info.patch [bz#980771]
- kvm-vmdk-convert-error-code-to-use-errp.patch [bz#980771]
- kvm-vmdk-refuse-enabling-zeroed-grain-with-flat-images.patch [bz#980771]
- kvm-qapi-Add-optional-field-compressed-to-ImageInfo.patch [bz#980771]
- kvm-vmdk-Only-read-cid-from-image-file-when-opening.patch [bz#980771]
- kvm-vmdk-Implment-bdrv_get_specific_info.patch [bz#980771]
- Resolves: bz#1004347
  (Backport qcow2 corruption prevention patches)
- Resolves: bz#1026524
  (Backport block layer error parameter patches)
- Resolves: bz#978402
  ([RFE] Add discard support to qemu-kvm layer)
- Resolves: bz#980771
  ([RFE]  qemu-img should be able to tell the compat version of a qcow2 image)

* Thu Nov 07 2013 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-15.el7
- kvm-cow-make-reads-go-at-a-decent-speed.patch [bz#989646]
- kvm-cow-make-writes-go-at-a-less-indecent-speed.patch [bz#989646]
- kvm-cow-do-not-call-bdrv_co_is_allocated.patch [bz#989646]
- kvm-block-keep-bs-total_sectors-up-to-date-even-for-grow.patch [bz#989646]
- kvm-block-make-bdrv_co_is_allocated-static.patch [bz#989646]
- kvm-block-do-not-use-total_sectors-in-bdrv_co_is_allocat.patch [bz#989646]
- kvm-block-remove-bdrv_is_allocated_above-bdrv_co_is_allo.patch [bz#989646]
- kvm-block-expect-errors-from-bdrv_co_is_allocated.patch [bz#989646]
- kvm-block-Fix-compiler-warning-Werror-uninitialized.patch [bz#989646]
- kvm-qemu-img-always-probe-the-input-image-for-allocated-.patch [bz#989646]
- kvm-block-make-bdrv_has_zero_init-return-false-for-copy-.patch [bz#989646]
- kvm-block-introduce-bdrv_get_block_status-API.patch [bz#989646]
- kvm-block-define-get_block_status-return-value.patch [bz#989646]
- kvm-block-return-get_block_status-data-and-flags-for-for.patch [bz#989646]
- kvm-block-use-bdrv_has_zero_init-to-return-BDRV_BLOCK_ZE.patch [bz#989646]
- kvm-block-return-BDRV_BLOCK_ZERO-past-end-of-backing-fil.patch [bz#989646]
- kvm-qemu-img-add-a-map-subcommand.patch [bz#989646]
- kvm-docs-qapi-document-qemu-img-map.patch [bz#989646]
- kvm-raw-posix-return-get_block_status-data-and-flags.patch [bz#989646]
- kvm-raw-posix-report-unwritten-extents-as-zero.patch [bz#989646]
- kvm-block-add-default-get_block_status-implementation-fo.patch [bz#989646]
- kvm-block-look-for-zero-blocks-in-bs-file.patch [bz#989646]
- kvm-qemu-img-fix-invalid-JSON.patch [bz#989646]
- kvm-block-get_block_status-set-pnum-0-on-error.patch [bz#989646]
- kvm-block-get_block_status-avoid-segfault-if-there-is-no.patch [bz#989646]
- kvm-block-get_block_status-avoid-redundant-callouts-on-r.patch [bz#989646]
- kvm-qcow2-Restore-total_sectors-value-in-save_vmstate.patch [bz#1025740]
- kvm-qcow2-Unset-zero_beyond_eof-in-save_vmstate.patch [bz#1025740]
- kvm-qemu-iotests-Test-for-loading-VM-state-from-qcow2.patch [bz#1025740]
- kvm-apic-rename-apic-specific-bitopts.patch [bz#1001216]
- kvm-hw-import-bitmap-operations-in-qdev-core-header.patch [bz#1001216]
- kvm-qemu-help-Sort-devices-by-logical-functionality.patch [bz#1001216]
- kvm-devices-Associate-devices-to-their-logical-category.patch [bz#1001216]
- kvm-Mostly-revert-qemu-help-Sort-devices-by-logical-func.patch [bz#1001216]
- kvm-qdev-monitor-Group-device_add-help-and-info-qdm-by-c.patch [bz#1001216]
- kvm-qdev-Replace-no_user-by-cannot_instantiate_with_devi.patch [bz#1001216]
- kvm-sysbus-Set-cannot_instantiate_with_device_add_yet.patch [bz#1001216]
- kvm-cpu-Document-why-cannot_instantiate_with_device_add_.patch [bz#1001216]
- kvm-apic-Document-why-cannot_instantiate_with_device_add.patch [bz#1001216]
- kvm-pci-host-Consistently-set-cannot_instantiate_with_de.patch [bz#1001216]
- kvm-ich9-Document-why-cannot_instantiate_with_device_add.patch [bz#1001216]
- kvm-piix3-piix4-Clean-up-use-of-cannot_instantiate_with_.patch [bz#1001216]
- kvm-vt82c686-Clean-up-use-of-cannot_instantiate_with_dev.patch [bz#1001216]
- kvm-isa-Clean-up-use-of-cannot_instantiate_with_device_a.patch [bz#1001216]
- kvm-qdev-Do-not-let-the-user-try-to-device_add-when-it-c.patch [bz#1001216]
- kvm-rhel-Revert-unwanted-cannot_instantiate_with_device_.patch [bz#1001216]
- kvm-rhel-Revert-downstream-changes-to-unused-default-con.patch [bz#1001076]
- kvm-rhel-Drop-cfi.pflash01-and-isa-ide-device.patch [bz#1001076]
- kvm-rhel-Drop-isa-vga-device.patch [bz#1001088]
- kvm-rhel-Make-isa-cirrus-vga-device-unavailable.patch [bz#1001088]
- kvm-rhel-Make-ccid-card-emulated-device-unavailable.patch [bz#1001123]
- kvm-x86-fix-migration-from-pre-version-12.patch [bz#1005695]
- kvm-x86-cpuid-reconstruct-leaf-0Dh-data.patch [bz#1005695]
- kvm-kvmvapic-Catch-invalid-ROM-size.patch [bz#920021]
- kvm-kvmvapic-Enter-inactive-state-on-hardware-reset.patch [bz#920021]
- kvm-kvmvapic-Clear-also-physical-ROM-address-when-enteri.patch [bz#920021]
- kvm-block-optionally-disable-live-block-jobs.patch [bz#987582]
- kvm-rpm-spec-template-disable-live-block-ops-for-rhel-en.patch [bz#987582]
- kvm-migration-disable-live-block-migration-b-i-for-rhel-.patch [bz#1022392]
- kvm-Build-ceph-rbd-only-for-rhev.patch [bz#987583]
- kvm-spec-Disable-host-cdrom-RHEL-only.patch [bz#760885]
- kvm-rhel-Make-pci-serial-2x-and-pci-serial-4x-device-una.patch [bz#1001180]
- kvm-usb-host-libusb-Fix-reset-handling.patch [bz#980415]
- kvm-usb-host-libusb-Configuration-0-may-be-a-valid-confi.patch [bz#980383]
- kvm-usb-host-libusb-Detach-kernel-drivers-earlier.patch [bz#980383]
- kvm-monitor-Remove-pci_add-command-for-Red-Hat-Enterpris.patch [bz#1010858]
- kvm-monitor-Remove-pci_del-command-for-Red-Hat-Enterpris.patch [bz#1010858]
- kvm-monitor-Remove-usb_add-del-commands-for-Red-Hat-Ente.patch [bz#1010858]
- kvm-monitor-Remove-host_net_add-remove-for-Red-Hat-Enter.patch [bz#1010858]
- kvm-fw_cfg-add-API-to-find-FW-cfg-object.patch [bz#990601]
- kvm-pvpanic-use-FWCfgState-explicitly.patch [bz#990601]
- kvm-pvpanic-initialization-cleanup.patch [bz#990601]
- kvm-pvpanic-fix-fwcfg-for-big-endian-hosts.patch [bz#990601]
- kvm-hw-misc-make-pvpanic-known-to-user.patch [bz#990601]
- kvm-gdbstub-do-not-restart-crashed-guest.patch [bz#990601]
- kvm-gdbstub-fix-for-commit-87f25c12bfeaaa0c41fb857713bbc.patch [bz#990601]
- kvm-vl-allow-cont-from-panicked-state.patch [bz#990601]
- kvm-hw-misc-don-t-create-pvpanic-device-by-default.patch [bz#990601]
- kvm-block-vhdx-add-migration-blocker.patch [bz#1007176]
- kvm-qemu-kvm.spec-add-vhdx-to-the-read-only-block-driver.patch [bz#1007176]
- kvm-qemu-kvm.spec-Add-VPC-VHD-driver-to-the-block-read-o.patch [bz#1007176]
- Resolves: bz#1001076
  (Disable or remove other block devices we won't support)
- Resolves: bz#1001088
  (Disable or remove display devices we won't support)
- Resolves: bz#1001123
  (Disable or remove device ccid-card-emulated)
- Resolves: bz#1001180
  (Disable or remove devices pci-serial-2x, pci-serial-4x)
- Resolves: bz#1001216
  (Fix no_user or provide another way make devices unavailable with -device / device_add)
- Resolves: bz#1005695
  (QEMU should hide CPUID.0Dh values that it does not support)
- Resolves: bz#1007176
  (Add VPC and VHDX file formats as supported in qemu-kvm (read-only))
- Resolves: bz#1010858
  (Disable unused human monitor commands)
- Resolves: bz#1022392
  (Disable live-storage-migration in qemu-kvm (migrate -b/-i))
- Resolves: bz#1025740
  (Saving VM state on qcow2 images results in VM state corruption)
- Resolves: bz#760885
  (Disable host cdrom passthrough)
- Resolves: bz#920021
  (qemu-kvm segment fault when reboot guest after hot unplug device with option ROM)
- Resolves: bz#980383
  (The usb3.0 stick can't be returned back to host after shutdown guest with usb3.0 pass-through)
- Resolves: bz#980415
  (libusbx: error [_open_sysfs_attr] open /sys/bus/usb/devices/4-1/bConfigurationValue failed ret=-1 errno=2)
- Resolves: bz#987582
  (Initial Virtualization Differentiation for RHEL7 (Live snapshots))
- Resolves: bz#987583
  (Initial Virtualization Differentiation for RHEL7 (Ceph enablement))
- Resolves: bz#989646
  (Support backup vendors in qemu to access qcow disk readonly)
- Resolves: bz#990601
  (pvpanic device triggers guest bugs when present by default)

* Wed Nov 06 2013 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-14.el7
- kvm-target-i386-remove-tabs-from-target-i386-cpu.h.patch [bz#928867]
- kvm-migrate-vPMU-state.patch [bz#928867]
- kvm-blockdev-do-not-default-cache.no-flush-to-true.patch [bz#1009993]
- kvm-virtio-blk-do-not-relay-a-previous-driver-s-WCE-conf.patch [bz#1009993]
- kvm-rng-random-use-error_setg_file_open.patch [bz#907743]
- kvm-block-mirror_complete-use-error_setg_file_open.patch [bz#907743]
- kvm-blockdev-use-error_setg_file_open.patch [bz#907743]
- kvm-cpus-use-error_setg_file_open.patch [bz#907743]
- kvm-dump-qmp_dump_guest_memory-use-error_setg_file_open.patch [bz#907743]
- kvm-savevm-qmp_xen_save_devices_state-use-error_setg_fil.patch [bz#907743]
- kvm-block-bdrv_reopen_prepare-don-t-use-QERR_OPEN_FILE_F.patch [bz#907743]
- kvm-qerror-drop-QERR_OPEN_FILE_FAILED-macro.patch [bz#907743]
- kvm-rhel-Drop-ivshmem-device.patch [bz#787463]
- kvm-usb-remove-old-usb-host-code.patch [bz#1001144]
- kvm-Add-rhel6-pxe-roms-files.patch [bz#997702]
- kvm-Add-rhel6-pxe-rom-to-redhat-rpm.patch [bz#997702]
- kvm-Fix-migration-from-rhel6.5-to-rhel7-with-ipxe.patch [bz#997702]
- kvm-pc-Don-t-prematurely-explode-QEMUMachineInitArgs.patch [bz#994490]
- kvm-pc-Don-t-explode-QEMUMachineInitArgs-into-local-vari.patch [bz#994490]
- kvm-smbios-Normalize-smbios_entry_add-s-error-handling-t.patch [bz#994490]
- kvm-smbios-Convert-to-QemuOpts.patch [bz#994490]
- kvm-smbios-Improve-diagnostics-for-conflicting-entries.patch [bz#994490]
- kvm-smbios-Make-multiple-smbios-type-accumulate-sanely.patch [bz#994490]
- kvm-smbios-Factor-out-smbios_maybe_add_str.patch [bz#994490]
- kvm-hw-Pass-QEMUMachine-to-its-init-method.patch [bz#994490]
- kvm-smbios-Set-system-manufacturer-product-version-by-de.patch [bz#994490]
- kvm-smbios-Decouple-system-product-from-QEMUMachine.patch [bz#994490]
- kvm-rhel-SMBIOS-type-1-branding.patch [bz#994490]
- kvm-Add-disable-rhev-features-option-to-configure.patch []
- Resolves: bz#1001144
  (Disable or remove device usb-host-linux)
- Resolves: bz#1009993
  (RHEL7 guests do not issue fdatasyncs on virtio-blk)
- Resolves: bz#787463
  (disable ivshmem (was: [Hitachi 7.0 FEAT] Support ivshmem (Inter-VM Shared Memory)))
- Resolves: bz#907743
  (qemu-ga: empty reason string for OpenFileFailed error)
- Resolves: bz#928867
  (Virtual PMU support during live migration - qemu-kvm)
- Resolves: bz#994490
  (Set per-machine-type SMBIOS strings)
- Resolves: bz#997702
  (Migration from RHEL6.5 host to RHEL7.0 host is failed with virtio-net device)

* Tue Nov 05 2013 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-13.el7
- kvm-seabios-paravirt-allow-more-than-1TB-in-x86-guest.patch [bz#989677]
- kvm-scsi-prefer-UUID-to-VM-name-for-the-initiator-name.patch [bz#1006468]
- kvm-Fix-incorrect-rhel_rhev_conflicts-macro-usage.patch [bz#1017693]
- Resolves: bz#1006468
  (libiscsi initiator name should use vm UUID)
- Resolves: bz#1017693
  (incorrect use of rhel_rhev_conflicts)
- Resolves: bz#989677
  ([HP 7.0 FEAT]: Increase KVM guest supported memory to 4TiB)

* Mon Nov 04 2013 Michal Novotny <minovotn@redhat.com> - 1.5.3-12.el7
- kvm-vl-Clean-up-parsing-of-boot-option-argument.patch [bz#997817]
- kvm-qemu-option-check_params-is-now-unused-drop-it.patch [bz#997817]
- kvm-vl-Fix-boot-order-and-once-regressions-and-related-b.patch [bz#997817]
- kvm-vl-Rename-boot_devices-to-boot_order-for-consistency.patch [bz#997817]
- kvm-pc-Make-no-fd-bootchk-stick-across-boot-order-change.patch [bz#997817]
- kvm-doc-Drop-ref-to-Bochs-from-no-fd-bootchk-documentati.patch [bz#997817]
- kvm-libqtest-Plug-fd-and-memory-leaks-in-qtest_quit.patch [bz#997817]
- kvm-libqtest-New-qtest_end-to-go-with-qtest_start.patch [bz#997817]
- kvm-qtest-Don-t-reset-on-qtest-chardev-connect.patch [bz#997817]
- kvm-boot-order-test-New-covering-just-PC-for-now.patch [bz#997817]
- kvm-qemu-ga-execute-fsfreeze-freeze-in-reverse-order-of-.patch [bz#1019352]
- kvm-rbd-link-and-load-librbd-dynamically.patch [bz#989608]
- kvm-rbd-Only-look-for-qemu-specific-copy-of-librbd.so.1.patch [bz#989608]
- kvm-spec-Whitelist-rbd-block-driver.patch [bz#989608]
- Resolves: bz#1019352
  (qemu-guest-agent: "guest-fsfreeze-freeze" deadlocks if the guest have mounted disk images)
- Resolves: bz#989608
  ([7.0 FEAT] qemu runtime support for librbd backend (ceph))
- Resolves: bz#997817
  (-boot order and -boot once regressed since RHEL-6)

* Thu Oct 31 2013 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-11.el7
- kvm-chardev-fix-pty_chr_timer.patch [bz#994414]
- kvm-qemu-socket-zero-initialize-SocketAddress.patch [bz#922010]
- kvm-qemu-socket-drop-pointless-allocation.patch [bz#922010]
- kvm-qemu-socket-catch-monitor_get_fd-failures.patch [bz#922010]
- kvm-qemu-char-check-optional-fields-using-has_.patch [bz#922010]
- kvm-error-add-error_setg_file_open-helper.patch [bz#922010]
- kvm-qemu-char-use-more-specific-error_setg_-variants.patch [bz#922010]
- kvm-qemu-char-print-notification-to-stderr.patch [bz#922010]
- kvm-qemu-char-fix-documentation-for-telnet-wait-socket-f.patch [bz#922010]
- kvm-qemu-char-don-t-leak-opts-on-error.patch [bz#922010]
- kvm-qemu-char-use-ChardevBackendKind-in-CharDriver.patch [bz#922010]
- kvm-qemu-char-minor-mux-chardev-fixes.patch [bz#922010]
- kvm-qemu-char-add-chardev-mux-support.patch [bz#922010]
- kvm-qemu-char-report-udp-backend-errors.patch [bz#922010]
- kvm-qemu-socket-don-t-leak-opts-on-error.patch [bz#922010]
- kvm-chardev-handle-qmp_chardev_add-KIND_MUX-failure.patch [bz#922010]
- kvm-acpi-piix4-Enable-qemu-kvm-compatibility-mode.patch [bz#1019474]
- kvm-target-i386-support-loading-of-cpu-xsave-subsection.patch [bz#1004743]
- Resolves: bz#1004743
  (XSAVE migration format not compatible between RHEL6 and RHEL7)
- Resolves: bz#1019474
  (RHEL-7 can't load piix4_pm migration section from RHEL-6.5)
- Resolves: bz#922010
  (RFE: support hotplugging chardev & serial ports)
- Resolves: bz#994414
  (hot-unplug chardev with pty backend caused qemu Segmentation fault)

* Thu Oct 17 2013 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-10.el7
- kvm-xhci-fix-endpoint-interval-calculation.patch [bz#1001604]
- kvm-xhci-emulate-intr-endpoint-intervals-correctly.patch [bz#1001604]
- kvm-xhci-reset-port-when-disabling-slot.patch [bz#1001604]
- kvm-Revert-usb-hub-report-status-changes-only-once.patch [bz#1001604]
- kvm-target-i386-Set-model-6-on-qemu64-qemu32-CPU-models.patch [bz#1004290]
- kvm-pc-rhel6-doesn-t-have-APIC-on-pentium-CPU-models.patch [bz#918907]
- kvm-pc-RHEL-6-had-x2apic-set-on-Opteron_G-123.patch [bz#918907]
- kvm-pc-RHEL-6-don-t-have-RDTSCP.patch [bz#918907]
- kvm-scsi-Fix-scsi_bus_legacy_add_drive-scsi-generic-with.patch [bz#1009285]
- kvm-seccomp-fine-tuning-whitelist-by-adding-times.patch [bz#1004175]
- kvm-block-add-bdrv_write_zeroes.patch [bz#921465]
- kvm-block-raw-add-bdrv_co_write_zeroes.patch [bz#921465]
- kvm-rdma-export-qemu_fflush.patch [bz#921465]
- kvm-block-migration-efficiently-encode-zero-blocks.patch [bz#921465]
- kvm-Fix-real-mode-guest-migration.patch [bz#921465]
- kvm-Fix-real-mode-guest-segments-dpl-value-in-savevm.patch [bz#921465]
- kvm-migration-add-autoconvergence-documentation.patch [bz#921465]
- kvm-migration-send-total-time-in-QMP-at-completed-stage.patch [bz#921465]
- kvm-migration-don-t-use-uninitialized-variables.patch [bz#921465]
- kvm-pc-drop-external-DSDT-loading.patch [bz#921465]
- kvm-hda-codec-refactor-common-definitions-into-a-header-.patch [bz#954195]
- kvm-hda-codec-make-mixemu-selectable-at-runtime.patch [bz#954195]
- kvm-audio-remove-CONFIG_MIXEMU-configure-option.patch [bz#954195]
- kvm-pc_piix-disable-mixer-for-6.4.0-machine-types-and-be.patch [bz#954195]
- kvm-spec-mixemu-config-option-is-no-longer-supported-and.patch [bz#954195]
- Resolves: bz#1001604
  (usb hub doesn't work properly (win7 sees downstream port #1 only).)
- Resolves: bz#1004175
  ('-sandbox on'  option  cause  qemu-kvm process hang)
- Resolves: bz#1004290
  (Use model 6 for qemu64 and intel cpus)
- Resolves: bz#1009285
  (-device usb-storage,serial=... crashes with SCSI generic drive)
- Resolves: bz#918907
  (provide backwards-compatible RHEL specific machine types in QEMU - CPU features)
- Resolves: bz#921465
  (Migration can not finished even the "remaining ram" is already 0 kb)
- Resolves: bz#954195
  (RHEL machines <=6.4 should not use mixemu)

* Thu Oct 10 2013 Miroslav Rezanina <mrezanin@redhat.com> - 1.5.3-9.el7
- kvm-qxl-fix-local-renderer.patch [bz#1005036]
- kvm-spec-include-userspace-iSCSI-initiator-in-block-driv.patch [bz#923843]
- kvm-linux-headers-update-to-kernel-3.10.0-26.el7.patch [bz#1008987]
- kvm-target-i386-add-feature-kvm_pv_unhalt.patch [bz#1008987]
- kvm-warn-if-num-cpus-is-greater-than-num-recommended.patch [bz#1010881]
- kvm-char-move-backends-io-watch-tag-to-CharDriverState.patch [bz#1007222]
- kvm-char-use-common-function-to-disable-callbacks-on-cha.patch [bz#1007222]
- kvm-char-remove-watch-callback-on-chardev-detach-from-fr.patch [bz#1007222]
- kvm-block-don-t-lose-data-from-last-incomplete-sector.patch [bz#1017049]
- kvm-vmdk-fix-cluster-size-check-for-flat-extents.patch [bz#1017049]
- kvm-qemu-iotests-add-monolithicFlat-creation-test-to-059.patch [bz#1017049]
- Resolves: bz#1005036
  (When using “-vga qxl” together with “-display vnc=:5” or “-display  sdl” qemu displays  pixel garbage)
- Resolves: bz#1007222
  (QEMU core dumped when do hot-unplug virtio serial port during transfer file between host to guest with virtio serial through TCP socket)
- Resolves: bz#1008987
  (pvticketlocks: add kvm feature kvm_pv_unhalt)
- Resolves: bz#1010881
  (backport vcpu soft limit warning)
- Resolves: bz#1017049
  (qemu-img refuses to open the vmdk format image its created)
- Resolves: bz#923843
  (include userspace iSCSI initiator in block driver whitelist)

* Wed Oct 09 2013 Miroslav Rezanina <mrezanin@redhat.com> - qemu-kvm-1.5.3-8.el7
- kvm-vmdk-Make-VMDK3Header-and-VmdkGrainMarker-QEMU_PACKE.patch [bz#995866]
- kvm-vmdk-use-unsigned-values-for-on-disk-header-fields.patch [bz#995866]
- kvm-qemu-iotests-add-poke_file-utility-function.patch [bz#995866]
- kvm-qemu-iotests-add-empty-test-case-for-vmdk.patch [bz#995866]
- kvm-vmdk-check-granularity-field-in-opening.patch [bz#995866]
- kvm-vmdk-check-l2-table-size-when-opening.patch [bz#995866]
- kvm-vmdk-check-l1-size-before-opening-image.patch [bz#995866]
- kvm-vmdk-use-heap-allocation-for-whole_grain.patch [bz#995866]
- kvm-vmdk-rename-num_gtes_per_gte-to-num_gtes_per_gt.patch [bz#995866]
- kvm-vmdk-Move-l1_size-check-into-vmdk_add_extent.patch [bz#995866]
- kvm-vmdk-fix-L1-and-L2-table-size-in-vmdk3-open.patch [bz#995866]
- kvm-vmdk-support-vmfsSparse-files.patch [bz#995866]
- kvm-vmdk-support-vmfs-files.patch [bz#995866]
- Resolves: bz#995866
  (fix vmdk support to ESX images)

* Thu Sep 26 2013 Miroslav Rezanina <mrezanin@redhat.com> - qemu-kvm-1.5.3-7.el7
- kvm-spice-fix-display-initialization.patch [bz#974887]
- kvm-Remove-i82550-network-card-emulation.patch [bz#921983]
- kvm-Remove-usb-wacom-tablet.patch [bz#903914]
- kvm-Disable-usb-uas.patch [bz#903914]
- kvm-Disable-vhost-scsi.patch [bz#994642]
- kvm-Remove-no-hpet-option.patch [bz#947441]
- kvm-Disable-isa-parallel.patch [bz#1002286]
- kvm-xhci-implement-warm-port-reset.patch [bz#949514]
- kvm-usb-add-serial-bus-property.patch [bz#953304]
- kvm-rhel6-compat-usb-serial-numbers.patch [bz#953304]
- kvm-vmdk-fix-comment-for-vmdk_co_write_zeroes.patch [bz#995866]
- kvm-gluster-Add-image-resize-support.patch [bz#1007226]
- kvm-block-Introduce-bs-zero_beyond_eof.patch [bz#1007226]
- kvm-block-Produce-zeros-when-protocols-reading-beyond-en.patch [bz#1007226]
- kvm-gluster-Abort-on-AIO-completion-failure.patch [bz#1007226]
- kvm-Preparation-for-usb-bt-dongle-conditional-build.patch [bz#1001131]
- kvm-Remove-dev-bluetooth.c-dependency-from-vl.c.patch [bz#1001131]
- kvm-exec-Fix-Xen-RAM-allocation-with-unusual-options.patch [bz#1009328]
- kvm-exec-Clean-up-fall-back-when-mem-path-allocation-fai.patch [bz#1009328]
- kvm-exec-Reduce-ifdeffery-around-mem-path.patch [bz#1009328]
- kvm-exec-Simplify-the-guest-physical-memory-allocation-h.patch [bz#1009328]
- kvm-exec-Drop-incorrect-dead-S390-code-in-qemu_ram_remap.patch [bz#1009328]
- kvm-exec-Clean-up-unnecessary-S390-ifdeffery.patch [bz#1009328]
- kvm-exec-Don-t-abort-when-we-can-t-allocate-guest-memory.patch [bz#1009328]
- kvm-pc_sysfw-Fix-ISA-BIOS-init-for-ridiculously-big-flas.patch [bz#1009328]
- kvm-virtio-scsi-Make-type-virtio-scsi-common-abstract.patch [bz#903918]
- kvm-qga-move-logfiles-to-new-directory-for-easier-SELinu.patch [bz#1009491]
- kvm-target-i386-add-cpu64-rhel6-CPU-model.patch [bz#918907]
- kvm-fix-steal-time-MSR-vmsd-callback-to-proper-opaque-ty.patch [bz#903889]
- Resolves: bz#1001131
  (Disable or remove device usb-bt-dongle)
- Resolves: bz#1002286
  (Disable or remove device isa-parallel)
- Resolves: bz#1007226
  (Introduce bs->zero_beyond_eof)
- Resolves: bz#1009328
  ([RFE] Nicer error report when qemu-kvm can't allocate guest RAM)
- Resolves: bz#1009491
  (move qga logfiles to new /var/log/qemu-ga/ directory [RHEL-7])
- Resolves: bz#903889
  (The value of steal time in "top" command always is "0.0% st" after guest migration)
- Resolves: bz#903914
  (Disable or remove usb related devices that we will not support)
- Resolves: bz#903918
  (Disable or remove emulated SCSI devices we will not support)
- Resolves: bz#918907
  (provide backwards-compatible RHEL specific machine types in QEMU - CPU features)
- Resolves: bz#921983
  (Disable or remove emulated network devices that we will not support)
- Resolves: bz#947441
  (HPET device must be disabled)
- Resolves: bz#949514
  (fail to passthrough the USB3.0 stick to windows guest with xHCI controller under pc-i440fx-1.4)
- Resolves: bz#953304
  (Serial number of some USB devices must be fixed for older RHEL machine types)
- Resolves: bz#974887
  (the screen of guest fail to display correctly when use spice + qxl driver)
- Resolves: bz#994642
  (should disable vhost-scsi)
- Resolves: bz#995866
  (fix vmdk support to ESX images)

* Mon Sep 23 2013 Paolo Bonzini <pbonzini@redhat.com> - qemu-kvm-1.5.3-6.el7
- re-enable spice
- Related: #979953

* Mon Sep 23 2013 Paolo Bonzini <pbonzini@redhat.com> - qemu-kvm-1.5.3-5.el7
- temporarily disable spice until libiscsi rebase is complete
- Related: #979953

* Thu Sep 19 2013 Michal Novotny <minovotn@redhat.com> - qemu-kvm-1.5.3-4.el7
- kvm-block-package-preparation-code-in-qmp_transaction.patch [bz#1005818]
- kvm-block-move-input-parsing-code-in-qmp_transaction.patch [bz#1005818]
- kvm-block-package-committing-code-in-qmp_transaction.patch [bz#1005818]
- kvm-block-package-rollback-code-in-qmp_transaction.patch [bz#1005818]
- kvm-block-make-all-steps-in-qmp_transaction-as-callback.patch [bz#1005818]
- kvm-blockdev-drop-redundant-proto_drv-check.patch [bz#1005818]
- kvm-block-Don-t-parse-protocol-from-file.filename.patch [bz#1005818]
- kvm-Revert-block-Disable-driver-specific-options-for-1.5.patch [bz#1005818]
- kvm-qcow2-Add-refcount-update-reason-to-all-callers.patch [bz#1005818]
- kvm-qcow2-Options-to-enable-discard-for-freed-clusters.patch [bz#1005818]
- kvm-qcow2-Batch-discards.patch [bz#1005818]
- kvm-block-Always-enable-discard-on-the-protocol-level.patch [bz#1005818]
- kvm-qapi.py-Avoid-code-duplication.patch [bz#1005818]
- kvm-qapi.py-Allow-top-level-type-reference-for-command-d.patch [bz#1005818]
- kvm-qapi-schema-Use-BlockdevSnapshot-type-for-blockdev-s.patch [bz#1005818]
- kvm-qapi-types.py-Implement-base-for-unions.patch [bz#1005818]
- kvm-qapi-visit.py-Split-off-generate_visit_struct_fields.patch [bz#1005818]
- kvm-qapi-visit.py-Implement-base-for-unions.patch [bz#1005818]
- kvm-docs-Document-QAPI-union-types.patch [bz#1005818]
- kvm-qapi-Add-visitor-for-implicit-structs.patch [bz#1005818]
- kvm-qapi-Flat-unions-with-arbitrary-discriminator.patch [bz#1005818]
- kvm-qapi-Add-consume-argument-to-qmp_input_get_object.patch [bz#1005818]
- kvm-qapi.py-Maintain-a-list-of-union-types.patch [bz#1005818]
- kvm-qapi-qapi-types.py-native-list-support.patch [bz#1005818]
- kvm-qapi-Anonymous-unions.patch [bz#1005818]
- kvm-block-Allow-driver-option-on-the-top-level.patch [bz#1005818]
- kvm-QemuOpts-Add-qemu_opt_unset.patch [bz#1005818]
- kvm-blockdev-Rename-I-O-throttling-options-for-QMP.patch [bz#1005818]
- kvm-qemu-iotests-Update-051-reference-output.patch [bz#1005818]
- kvm-blockdev-Rename-readonly-option-to-read-only.patch [bz#1005818]
- kvm-blockdev-Split-up-cache-option.patch [bz#1005818]
- kvm-qcow2-Use-dashes-instead-of-underscores-in-options.patch [bz#1005818]
- kvm-qemu-iotests-filter-QEMU-version-in-monitor-banner.patch [bz#1006959]
- kvm-tests-set-MALLOC_PERTURB_-to-expose-memory-bugs.patch [bz#1006959]
- kvm-qemu-iotests-Whitespace-cleanup.patch [bz#1006959]
- kvm-qemu-iotests-Fixed-test-case-026.patch [bz#1006959]
- kvm-qemu-iotests-Fix-test-038.patch [bz#1006959]
- kvm-qemu-iotests-Remove-lsi53c895a-tests-from-051.patch [bz#1006959]
- Resolves: bz#1005818
  (qcow2: Backport discard command line options)
- Resolves: bz#1006959
  (qemu-iotests false positives)

* Thu Aug 29 2013 Miroslav Rezanina <mrezanin@redhat.com> - qemu-kvm-1.5.3-3.el7
- Fix rhel/rhev split

* Thu Aug 29 2013 Miroslav Rezanina <mrezanin@redhat.com> - qemu-kvm-1.5.3-2.el7
- kvm-osdep-add-qemu_get_local_state_pathname.patch [bz#964304]
- kvm-qga-determine-default-state-dir-and-pidfile-dynamica.patch [bz#964304]
- kvm-configure-don-t-save-any-fixed-local_statedir-for-wi.patch [bz#964304]
- kvm-qga-create-state-directory-on-win32.patch [bz#964304]
- kvm-qga-save-state-directory-in-ga_install_service-RHEL-.patch [bz#964304]
- kvm-Makefile-create-.-var-run-when-installing-the-POSIX-.patch [bz#964304]
- kvm-qemu-option-Fix-qemu_opts_find-for-null-id-arguments.patch [bz#980782]
- kvm-qemu-option-Fix-qemu_opts_set_defaults-for-corner-ca.patch [bz#980782]
- kvm-vl-New-qemu_get_machine_opts.patch [bz#980782]
- kvm-Fix-machine-options-accel-kernel_irqchip-kvm_shadow_.patch [bz#980782]
- kvm-microblaze-Fix-latent-bug-with-default-DTB-lookup.patch [bz#980782]
- kvm-Simplify-machine-option-queries-with-qemu_get_machin.patch [bz#980782]
- kvm-pci-add-VMSTATE_MSIX.patch [bz#838170]
- kvm-xhci-add-XHCISlot-addressed.patch [bz#838170]
- kvm-xhci-add-xhci_alloc_epctx.patch [bz#838170]
- kvm-xhci-add-xhci_init_epctx.patch [bz#838170]
- kvm-xhci-add-live-migration-support.patch [bz#838170]
- kvm-pc-set-level-xlevel-correctly-on-486-qemu32-CPU-mode.patch [bz#918907]
- kvm-pc-Remove-incorrect-rhel6.x-compat-model-value-for-C.patch [bz#918907]
- kvm-pc-rhel6.x-has-x2apic-present-on-Conroe-Penryn-Nehal.patch [bz#918907]
- kvm-pc-set-compat-CPUID-0x80000001-.EDX-bits-on-Westmere.patch [bz#918907]
- kvm-pc-Remove-PCLMULQDQ-from-Westmere-on-rhel6.x-machine.patch [bz#918907]
- kvm-pc-SandyBridge-rhel6.x-compat-fixes.patch [bz#918907]
- kvm-pc-Haswell-doesn-t-have-rdtscp-on-rhel6.x.patch [bz#918907]
- kvm-i386-fix-LAPIC-TSC-deadline-timer-save-restore.patch [bz#972433]
- kvm-all.c-max_cpus-should-not-exceed-KVM-vcpu-limit.patch [bz#996258]
- kvm-add-timestamp-to-error_report.patch [bz#906937]
- kvm-Convert-stderr-message-calling-error_get_pretty-to-e.patch [bz#906937]
- Resolves: bz#838170
  (Add live migration support for USB [xhci, usb-uas])
- Resolves: bz#906937
  ([Hitachi 7.0 FEAT][QEMU]Add a time stamp to error message (*))
- Resolves: bz#918907
  (provide backwards-compatible RHEL specific machine types in QEMU - CPU features)
- Resolves: bz#964304
  (Windows guest agent service failed to be started)
- Resolves: bz#972433
  ("INFO: rcu_sched detected stalls" after RHEL7 kvm vm migrated)
- Resolves: bz#980782
  (kernel_irqchip defaults to off instead of on without -machine)
- Resolves: bz#996258
  (boot guest with maxcpu=255 successfully but actually max number of vcpu is 160)

* Wed Aug 28 2013 Miroslav Rezanina <mrezanin@redhat.com> - 10:1.5.3-1
- Rebase to qemu 1.5.3

* Tue Aug 20 2013 Miroslav Rezanina <mrezanin@redhat.com> - 10:1.5.2-4
- qemu: guest agent creates files with insecure permissions in deamon mode [rhel-7.0] (rhbz 974444)
- update qemu-ga config & init script in RHEL7 wrt. fsfreeze hook (rhbz 969942)
- RHEL7 does not have equivalent functionality for __com.redhat_qxl_screendump (rhbz 903910)
- SEP flag behavior for CPU models of RHEL6 machine types should be compatible (rhbz 960216)
- crash command can not read the dump-guest-memory file when paging=false [RHEL-7] (rhbz 981582)
- RHEL 7 qemu-kvm fails to build on F19 host due to libusb deprecated API (rhbz 996469)
- Live migration support in virtio-blk-data-plane (rhbz 995030)
- qemu-img resize can execute successfully even input invalid syntax (rhbz 992935)

* Fri Aug 09 2013 Miroslav Rezanina <mrezanin@redhat.com> - 10:1.5.2-3
- query mem info from monitor would cause qemu-kvm hang [RHEL-7] (rhbz #970047)
- Throttle-down guest to help with live migration convergence (backport to RHEL7.0) (rhbz #985958)
- disable (for now) EFI-enabled roms (rhbz #962563)
- qemu-kvm "vPMU passthrough" mode breaks migration, shouldn't be enabled by default (rhbz #853101)
- Remove pending watches after virtserialport unplug (rhbz #992900)
- Containment of error when an SR-IOV device encounters an error... (rhbz #984604)

* Wed Jul 31 2013 Miroslav Rezanina <mrezanin@redhat.com> - 10:1.5.2-2
- SPEC file prepared for RHEL/RHEV split (rhbz #987165)
- RHEL guest( sata disk ) can not boot up (rhbz #981723)
- Kill the "use flash device for BIOS unless KVM" misfeature (rhbz #963280)
- Provide RHEL-6 machine types (rhbz #983991)
- Change s3/s4 default to "disable". (rhbz #980840)  
- Support Virtual Memory Disk Format in qemu (rhbz #836675)
- Glusterfs backend for QEMU (rhbz #805139)

* Tue Jul 02 2013 Miroslav Rezanina <mrezanin@redhat.com> - 10:1.5.2-1
- Rebase to 1.5.2

* Tue Jul 02 2013 Miroslav Rezanina <mrezanin@redhat.com> - 10:1.5.1-2
- Fix package package version info (bz #952996)
- pc: Replace upstream machine types by RHEL-7 types (bz #977864)
- target-i386: Update model values on Conroe/Penryn/Nehalem CPU model (bz #861210)
- target-i386: Set level=4 on Conroe/Penryn/Nehalem (bz #861210)

* Fri Jun 28 2013 Miroslav Rezanina <mrezanin@redhat.com> - 10:1.5.1-1
- Rebase to 1.5.1
- Change epoch to 10 to obsolete RHEL-6 qemu-kvm-rhev package (bz #818626)

* Fri May 24 2013 Miroslav Rezanina <mrezanin@redhat.com> - 3:1.5.0-2
- Enable werror (bz #948290)
- Enable nbd driver (bz #875871)
- Fix udev rules file location (bz #958860)
- Remove +x bit from systemd unit files (bz #965000)
- Drop unneeded kvm.modules on x86 (bz #963642)
- Fix build flags
- Enable libusb

* Thu May 23 2013 Miroslav Rezanina <mrezanin@redhat.com> - 3:1.5.0-1
- Rebase to 1.5.0

* Tue Apr 23 2013 Miroslav Rezanina <mrezanin@redhat.com> - 3:1.4.0-4
- Enable build of libcacard subpackage for non-x86_64 archs (bz #873174)
- Enable build of qemu-img subpackage for non-x86_64 archs (bz #873174)
- Enable build of qemu-guest-agent subpackage for non-x86_64 archs (bz #873174)

* Tue Apr 23 2013 Miroslav Rezanina <mrezanin@redhat.com> - 3:1.4.0-3
- Enable/disable features supported by rhel7
- Use qemu-kvm instead of qemu in filenames and pathes

* Fri Apr 19 2013 Daniel Mach <dmach@redhat.com> - 3:1.4.0-2.1
- Rebuild for cyrus-sasl

* Fri Apr 05 2013 Miroslav Rezanina <mrezanin@redhat.com> - 3:1.4.0-2
- Synchronization with Fedora 19 package version 2:1.4.0-8

* Wed Apr 03 2013 Daniel Mach <dmach@redhat.com> - 3:1.4.0-1.1
- Rebuild for libseccomp

* Thu Mar 07 2013 Miroslav Rezanina <mrezanin@redhat.com> - 3:1.4.0-1
- Rebase to 1.4.0

* Mon Feb 25 2013 Michal Novotny <minovotn@redhat.com> - 3:1.3.0-8
- Missing package qemu-system-x86 in hardware certification kvm testing (bz#912433)
- Resolves: bz#912433
  (Missing package qemu-system-x86 in hardware certification kvm testing)

* Fri Feb 22 2013 Alon Levy <alevy@redhat.com> - 3:1.3.0-6
- Bump epoch back to 3 since there has already been a 3 package release:
  3:1.2.0-20.el7 https://brewweb.devel.redhat.com/buildinfo?buildID=244866
- Mark explicit libcacard dependency on new enough qemu-img to avoid conflict
  since /usr/bin/vscclient was moved from qemu-img to libcacard subpackage.

* Wed Feb 13 2013 Michal Novotny <minovotn@redhat.com> - 2:1.3.0-5
- Fix patch contents for usb-redir (bz#895491)
- Resolves: bz#895491
  (PATCH: 0110-usb-redir-Add-flow-control-support.patch has been mangled on rebase !!)

* Wed Feb 06 2013 Alon Levy <alevy@redhat.com> - 2:1.3.0-4
- Add patch from f19 package for libcacard missing error_set symbol.
- Resolves: bz#891552

* Mon Jan 07 2013 Michal Novotny <minovotn@redhat.com> - 2:1.3.0-3
- Remove dependency on bogus qemu-kvm-kvm package [bz#870343]
- Resolves: bz#870343
  (qemu-kvm-1.2.0-16.el7 cant be installed)

* Tue Dec 18 2012 Michal Novotny <minovotn@redhat.com> - 2:1.3.0-2
- Rename qemu to qemu-kvm
- Move qemu-kvm to libexecdir

* Fri Dec 07 2012 Cole Robinson <crobinso@redhat.com> - 2:1.3.0-1
- Switch base tarball from qemu-kvm to qemu
- qemu 1.3 release
- Option to use linux VFIO driver to assign PCI devices
- Many USB3 improvements
- New paravirtualized hardware random number generator device.
- Support for Glusterfs volumes with "gluster://" -drive URI
- Block job commands for live block commit and storage migration

* Wed Nov 28 2012 Alon Levy <alevy@redhat.com> - 2:1.2.0-25
* Merge libcacard into qemu, since they both use the same sources now.

* Thu Nov 22 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-24
- Move vscclient to qemu-common, qemu-nbd to qemu-img

* Tue Nov 20 2012 Alon Levy <alevy@redhat.com> - 2:1.2.0-23
- Rewrite fix for bz #725965 based on fix for bz #867366
- Resolve bz #867366

* Fri Nov 16 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-23
- Backport --with separate_kvm support from EPEL branch

* Fri Nov 16 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-22
- Fix previous commit

* Fri Nov 16 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-21
- Backport commit 38f419f (configure: Fix CONFIG_QEMU_HELPERDIR generation,
  2012-10-17)

* Thu Nov 15 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-20
- Install qemu-bridge-helper as suid root
- Distribute a sample /etc/qemu/bridge.conf file

* Thu Nov  1 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-19
- Sync spice patches with upstream, minor bugfixes and set the qxl pci
  device revision to 4 by default, so that guests know they can use
  the new features

* Tue Oct 30 2012 Cole Robinson <crobinso@redhat.com> - 2:1.2.0-18
- Fix loading arm initrd if kernel is very large (bz #862766)
- Don't use reserved word 'function' in systemtap files (bz #870972)
- Drop assertion that was triggering when pausing guests w/ qxl (bz
  #870972)

* Sun Oct 28 2012 Cole Robinson <crobinso@redhat.com> - 2:1.2.0-17
- Pull patches queued for qemu 1.2.1

* Fri Oct 19 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-16
- add s390x KVM support
- distribute pre-built firmware or device trees for Alpha, Microblaze, S390
- add missing system targets
- add missing linux-user targets
- fix previous commit

* Thu Oct 18 2012 Dan Horák <dan[at]danny.cz> - 2:1.2.0-15
- fix build on non-kvm arches like s390(x)

* Wed Oct 17 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-14
- Change SLOF Requires for the new version number

* Thu Oct 11 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-13
- Add ppc support to kvm.modules (original patch by David Gibson)
- Replace x86only build with kvmonly build: add separate defines and
  conditionals for all packages, so that they can be chosen and
  renamed in kvmonly builds and so that qemu has the appropriate requires
- Automatically pick libfdt dependancy
- Add knob to disable spice+seccomp

* Fri Sep 28 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-12
- Call udevadm on post, fixing bug 860658

* Fri Sep 28 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-11
- Rebuild against latest spice-server and spice-protocol
- Fix non-seamless migration failing with vms with usb-redir devices,
  to allow boxes to load such vms from disk

* Tue Sep 25 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-10
- Sync Spice patchsets with upstream (rhbz#860238)
- Fix building with usbredir >= 0.5.2

* Thu Sep 20 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-9
- Sync USB and Spice patchsets with upstream

* Sun Sep 16 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.2.0-8
- Use 'global' instead of 'define', and underscore in definition name,
  n-v-r, and 'dist' tag of SLOF, all to fix RHBZ#855252.

* Fri Sep 14 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.2.0-4
- add versioned dependency from qemu-system-ppc to SLOF (BZ#855252)

* Wed Sep 12 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.2.0-3
- Fix RHBZ#853408 which causes libguestfs failure.

* Sat Sep  8 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-2
- Fix crash on (seamless) migration
- Sync usbredir live migration patches with upstream

* Fri Sep  7 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.2.0-1
- New upstream release 1.2.0 final
- Add support for Spice seamless migration
- Add support for Spice dynamic monitors
- Add support for usb-redir live migration

* Tue Sep 04 2012 Adam Jackson <ajax@redhat.com> 1.2.0-0.5.rc1
- Flip Requires: ceph >= foo to Conflicts: ceph < foo, so we pull in only the
  libraries which we need and not the rest of ceph which we don't.

* Tue Aug 28 2012 Cole Robinson <crobinso@redhat.com> 1.2.0-0.4.rc1
- Update to 1.2.0-rc1

* Mon Aug 20 2012 Richard W.M. Jones <rjones@redhat.com> - 1.2-0.3.20120806git3e430569
- Backport Bonzini's vhost-net fix (RHBZ#848400).

* Tue Aug 14 2012 Cole Robinson <crobinso@redhat.com> - 1.2-0.2.20120806git3e430569
- Bump release number, previous build forgot but the dist bump helped us out

* Tue Aug 14 2012 Cole Robinson <crobinso@redhat.com> - 1.2-0.1.20120806git3e430569
- Revive qemu-system-{ppc*, sparc*} (bz 844502)
- Enable KVM support for all targets (bz 844503)

* Mon Aug 06 2012 Cole Robinson <crobinso@redhat.com> - 1.2-0.1.20120806git3e430569.fc18
- Update to git snapshot

* Sun Jul 29 2012 Cole Robinson <crobinso@redhat.com> - 1.1.1-1
- Upstream stable release 1.1.1
- Fix systemtap tapsets (bz 831763)
- Fix VNC audio tunnelling (bz 840653)
- Don't renable ksm on update (bz 815156)
- Bump usbredir dep (bz 812097)
- Fix RPM install error on non-virt machines (bz 660629)
- Obsolete openbios to fix upgrade dependency issues (bz 694802)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.1.0-8
- Re-diff previous patch so that it applies and actually apply it

* Tue Jul 10 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.1.0-7
- Add patch to fix default machine options.  This fixes libvirt
  detection of qemu.
- Back out patch 1 which conflicts.

* Fri Jul  6 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.1.0-5
- Fix qemu crashing (on an assert) whenever USB-2.0 isoc transfers are used

* Thu Jul  5 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.1.0-4
- Disable tests since they hang intermittently.
- Add kvmvapic.bin (replaces vapic.bin).
- Add cpus-x86_64.conf.  qemu now creates /etc/qemu/target-x86_64.conf
  as an empty file.
- Add qemu-icon.bmp.
- Add qemu-bridge-helper.
- Build and include virtfs-proxy-helper + man page (thanks Hans de Goede).

* Wed Jul  4 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.1.0-1
- New upstream release 1.1.0
- Drop about a 100 spice + USB patches, which are all upstream

* Mon Apr 23 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.0-17
- Fix install failure due to set -e (rhbz #815272)

* Mon Apr 23 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.0-16
- Fix kvm.modules to exit successfully on non-KVM capable systems (rhbz #814932)

* Thu Apr 19 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.0-15
- Add a couple of backported QXL/Spice bugfixes
- Add spice volume control patches

* Fri Apr 6 2012 Paolo Bonzini <pbonzini@redhat.com> - 2:1.0-12
- Add back PPC and SPARC user emulators
- Update binfmt rules from upstream

* Mon Apr  2 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.0-11
- Some more USB bugfixes from upstream

* Thu Mar 29 2012 Eduardo Habkost <ehabkost@redhat.com> - 2:1.0-12
- Fix ExclusiveArch mistake that disabled all non-x86_64 builds on Fedora

* Wed Mar 28 2012 Eduardo Habkost <ehabkost@redhat.com> - 2:1.0-11
- Use --with variables for build-time settings

* Wed Mar 28 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-10
- Switch to use iPXE for netboot ROMs

* Thu Mar 22 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-9
- Remove O_NOATIME for 9p filesystems

* Mon Mar 19 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-8
- Move udev rules to /lib/udev/rules.d (rhbz #748207)

* Fri Mar  9 2012 Hans de Goede <hdegoede@redhat.com> - 2:1.0-7
- Add a whole bunch of USB bugfixes from upstream

* Mon Feb 13 2012 Daniel P. Berrange <berrange@redhat.com> - 2:1.0-6
- Add many more missing BRs for misc QEMU features
- Enable running of test suite during build

* Tue Feb 07 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-5
- Add support for virtio-scsi

* Sun Feb  5 2012 Richard W.M. Jones <rjones@redhat.com> - 2:1.0-4
- Require updated ceph for latest librbd with rbd_flush symbol.

* Tue Jan 24 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-3
- Add support for vPMU
- e1000: bounds packet size against buffer size CVE-2012-0029

* Fri Jan 13 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-2
- Add patches for USB redirect bits
- Remove palcode-clipper, we don't build it

* Wed Jan 11 2012 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-1
- Add patches from 1.0.1 queue

* Fri Dec 16 2011 Justin M. Forbes <jforbes@redhat.com> - 2:1.0-1
- Update to qemu 1.0

* Tue Nov 15 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.1-3
- Enable spice for i686 users as well

* Thu Nov 03 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.1-2
- Fix POSTIN scriplet failure (#748281)

* Fri Oct 21 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.1-1
- Require seabios-bin >= 0.6.0-2 (#741992)
- Replace init scripts with systemd units (#741920)
- Update to 0.15.1 stable upstream
  
* Fri Oct 21 2011 Paul Moore <pmoore@redhat.com>
- Enable full relro and PIE (rhbz #738812)

* Wed Oct 12 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-6
- Add BR on ceph-devel to enable RBD block device

* Wed Oct  5 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-5
- Create a qemu-guest-agent sub-RPM for guest installation

* Tue Sep 13 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-4
- Enable DTrace tracing backend for SystemTAP (rhbz #737763)
- Enable build with curl (rhbz #737006)

* Thu Aug 18 2011 Hans de Goede <hdegoede@redhat.com> - 2:0.15.0-3
- Add missing BuildRequires: usbredir-devel, so that the usbredir code
  actually gets build

* Thu Aug 18 2011 Richard W.M. Jones <rjones@redhat.com> - 2:0.15.0-2
- Add upstream qemu patch 'Allow to leave type on default in -machine'
  (2645c6dcaf6ea2a51a3b6dfa407dd203004e4d11).

* Sun Aug 14 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-1
- Update to 0.15.0 stable release.

* Thu Aug 04 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-0.3.201108040af4922
- Update to 0.15.0-rc1 as we prepare for 0.15.0 release

* Thu Aug  4 2011 Daniel P. Berrange <berrange@redhat.com> - 2:0.15.0-0.3.2011072859fadcc
- Fix default accelerator for non-KVM builds (rhbz #724814)

* Thu Jul 28 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-0.1.2011072859fadcc
- Update to 0.15.0-rc0 as we prepare for 0.15.0 release

* Tue Jul 19 2011 Hans de Goede <hdegoede@redhat.com> - 2:0.15.0-0.2.20110718525e3df
- Add support usb redirection over the network, see:
  http://fedoraproject.org/wiki/Features/UsbNetworkRedirection
- Restore chardev flow control patches

* Mon Jul 18 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.15.0-0.1.20110718525e3df
- Update to git snapshot as we prepare for 0.15.0 release

* Wed Jun 22 2011 Richard W.M. Jones <rjones@redhat.com> - 2:0.14.0-9
- Add BR libattr-devel.  This caused the -fstype option to be disabled.
  https://www.redhat.com/archives/libvir-list/2011-June/thread.html#01017

* Mon May  2 2011 Hans de Goede <hdegoede@redhat.com> - 2:0.14.0-8
- Fix a bug in the spice flow control patches which breaks the tcp chardev

* Tue Mar 29 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-7
- Disable qemu-ppc and qemu-sparc packages (#679179)

* Mon Mar 28 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-6
- Spice fixes for flow control.

* Tue Mar 22 2011 Dan Horák <dan[at]danny.cz> - 2:0.14.0-5
- be more careful when removing the -g flag on s390

* Fri Mar 18 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-4
- Fix thinko on adding the most recent patches.

* Wed Mar 16 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-3
- Fix migration issue with vhost
- Fix qxl locking issues for spice

* Wed Mar 02 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-2
- Re-enable sparc and cris builds

* Thu Feb 24 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-1
- Update to 0.14.0 release

* Fri Feb 11 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-0.1.20110210git7aa8c46
- Update git snapshot
- Temporarily disable qemu-cris and qemu-sparc due to build errors (to be resolved shorly)

* Tue Feb 08 2011 Justin M. Forbes <jforbes@redhat.com> - 2:0.14.0-0.1.20110208git3593e6b
- Update to 0.14.0 rc git snapshot
- Add virtio-net to modules

* Wed Nov  3 2010 Daniel P. Berrange <berrange@redhat.com> - 2:0.13.0-2
- Revert previous change
- Make qemu-common own the /etc/qemu directory
- Add /etc/qemu/target-x86_64.conf to qemu-system-x86 regardless
  of host architecture.

* Wed Nov 03 2010 Dan Horák <dan[at]danny.cz> - 2:0.13.0-2
- Remove kvm config file on non-x86 arches (part of #639471)
- Own the /etc/qemu directory

* Mon Oct 18 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-1
- Update to 0.13.0 upstream release
- Fixes for vhost
- Fix mouse in certain guests (#636887)
- Fix issues with WinXP guest install (#579348)
- Resolve build issues with S390 (#639471)
- Fix Windows XP on Raw Devices (#631591)

* Tue Oct 05 2010 jkeating - 2:0.13.0-0.7.rc1.1
- Rebuilt for gcc bug 634757

* Tue Sep 21 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.7.rc1
- Flip qxl pci id from unstable to stable (#634535)
- KSM Fixes from upstream (#558281)

* Tue Sep 14 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.6.rc1
- Move away from git snapshots as 0.13 is close to release
- Updates for spice 0.6

* Tue Aug 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.5.20100809git25fdf4a
- Fix typo in e1000 gpxe rom requires.
- Add links to newer vgabios

* Tue Aug 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.4.20100809git25fdf4a
- Disable spice on 32bit, it is not supported and buildreqs don't exist.

* Mon Aug 9 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.3.20100809git25fdf4a
- Updates from upstream towards 0.13 stable
- Fix requires on gpxe
- enable spice now that buildreqs are in the repository.
- ksmtrace has moved to a separate upstream package

* Tue Jul 27 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.2.20100727gitb81fe95
- add texinfo buildreq for manpages.

* Tue Jul 27 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.13.0-0.1.20100727gitb81fe95
- Update to 0.13.0 upstream snapshot
- ksm init fixes from upstream

* Tue Jul 20 2010 Dan Horák <dan[at]danny.cz> - 2:0.12.3-8
- Add avoid-llseek patch from upstream needed for building on s390(x)
- Don't use parallel make on s390(x)

* Tue Jun 22 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.3-7
- Add vvfat hardening patch from upstream (#605202)

* Fri Apr 23 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-6
- Change requires to the noarch seabios-bin
- Add ownership of docdir to qemu-common (#572110)
- Fix "Cannot boot from non-existent NIC" error when using virt-install (#577851)

* Thu Apr 15 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-5
- Update virtio console patches from upstream

* Thu Mar 11 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-4
- Detect cdrom via ioctl (#473154)
- re add increased buffer for USB control requests (#546483)

* Wed Mar 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-3
- Migration clear the fd in error cases (#518032)

* Tue Mar 09 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-2
- Allow builds --with x86only
- Add libaio-devel buildreq for aio support

* Fri Feb 26 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.3-1
- Update to 0.12.3 upstream
- vhost-net migration/restart fixes
- Add F-13 machine type
- virtio-serial fixes

* Tue Feb 09 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.2-6
- Add vhost net support.

* Thu Feb 04 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.2-5
- Avoid creating too large iovecs in multiwrite merge (#559717)
- Don't try to set max_kernel_pages during ksm init on newer kernels (#558281)
- Add logfile options for ksmtuned debug.

* Wed Jan 27 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.2-4
- Remove build dependency on iasl now that we have seabios

* Wed Jan 27 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.2-3
- Remove source target for 0.12.1.2

* Wed Jan 27 2010 Amit Shah <amit.shah@redhat.com> - 2:0.12.2-2
- Add virtio-console patches from upstream for the F13 VirtioSerial feature

* Mon Jan 25 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.2-1
- Update to 0.12.2 upstream

* Sun Jan 10 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.1.2-3
- Point to seabios instead of bochs, and add a requires for seabios

* Mon Jan  4 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.1.2-2
- Remove qcow2 virtio backing file patch

* Mon Jan  4 2010 Justin M. Forbes <jforbes@redhat.com> - 2:0.12.1.2-1
- Update to 0.12.1.2 upstream
- Remove patches included in upstream

* Fri Nov 20 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-12
- Fix a use-after-free crasher in the slirp code (#539583)
- Fix overflow in the parallels image format support (#533573)

* Wed Nov  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-11
- Temporarily disable preadv/pwritev support to fix data corruption (#526549)

* Tue Nov  3 2009 Justin M. Forbes <jforbes@redhat.com> - 2:0.11.0-10
- Default ksm and ksmtuned services on.

* Thu Oct 29 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-9
- Fix dropped packets with non-virtio NICs (#531419)

* Wed Oct 21 2009 Glauber Costa <gcosta@redhat.com> - 2:0.11.0-8
- Properly save kvm time registers (#524229)

* Mon Oct 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-7
- Fix potential segfault from too small MSR_COUNT (#528901)

* Fri Oct  9 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-6
- Fix fs errors with virtio and qcow2 backing file (#524734)
- Fix ksm initscript errors on kernel missing ksm (#527653)
- Add missing Requires(post): getent, useradd, groupadd (#527087)

* Tue Oct  6 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-5
- Add 'retune' verb to ksmtuned init script

* Mon Oct  5 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-4
- Use rtl8029 PXE rom for ne2k_pci, not ne (#526777)
- Also, replace the gpxe-roms-qemu pkg requires with file-based requires

* Thu Oct  1 2009 Justin M. Forbes <jmforbes@redhat.com> - 2:0.11.0-3
- Improve error reporting on file access (#524695)

* Mon Sep 28 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-2
- Fix pci hotplug to not exit if supplied an invalid NIC model (#524022)

* Mon Sep 28 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.11.0-1
- Update to 0.11.0 release
- Drop a couple of upstreamed patches

* Wed Sep 23 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-5
- Fix issue causing NIC hotplug confusion when no model is specified (#524022)

* Wed Sep 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-4
- Fix for KSM patch from Justin Forbes

* Wed Sep 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-3
- Add ksmtuned, also from Dan Kenigsberg
- Use %%_initddir macro

* Wed Sep 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-2
- Add ksm control script from Dan Kenigsberg

* Mon Sep  7 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.92-1
- Update to qemu-kvm-0.11.0-rc2
- Drop upstreamed patches
- extboot install now fixed upstream
- Re-place TCG init fix (#516543) with the one gone upstream

* Mon Sep  7 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.10.rc1
- Fix MSI-X error handling on older kernels (#519787)

* Fri Sep  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.9.rc1
- Make pulseaudio the default audio backend (#519540, #495964, #496627)

* Thu Aug 20 2009 Richard W.M. Jones <rjones@redhat.com> - 2:0.10.91-0.8.rc1
- Fix segfault when qemu-kvm is invoked inside a VM (#516543)

* Tue Aug 18 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.7.rc1
- Fix permissions on udev rules (#517571)

* Mon Aug 17 2009 Lubomir Rintel <lkundrak@v3.sk> - 2:0.10.91-0.6.rc1
- Allow blacklisting of kvm modules (#517866)

* Fri Aug  7 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.5.rc1
- Fix virtio_net with -net user (#516022)

* Tue Aug  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.4.rc1
- Update to qemu-kvm-0.11-rc1; no changes from rc1-rc0

* Tue Aug  4 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.3.rc1.rc0
- Fix extboot checksum (bug #514899)

* Fri Jul 31 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.2.rc1.rc0
- Add KSM support
- Require bochs-bios >= 2.3.8-0.8 for latest kvm bios updates

* Thu Jul 30 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.91-0.1.rc1.rc0
- Update to qemu-kvm-0.11.0-rc1-rc0
- This is a pre-release of the official -rc1
- A vista installer regression is blocking the official -rc1 release
- Drop qemu-prefer-sysfs-for-usb-host-devices.patch
- Drop qemu-fix-build-for-esd-audio.patch
- Drop qemu-slirp-Fix-guestfwd-for-incoming-data.patch
- Add patch to ensure extboot.bin is installed

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:0.10.50-14.kvm88
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 23 2009 Glauber Costa <glommer@redhat.com> - 2:0.10.50-13.kvm88
- Fix bug 513249, -net channel option is broken

* Thu Jul 16 2009 Daniel P. Berrange <berrange@redhat.com> - 2:0.10.50-12.kvm88
- Add 'qemu' user and group accounts
- Force disable xen until it can be made to build

* Thu Jul 16 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-11.kvm88
- Update to kvm-88, see http://www.linux-kvm.org/page/ChangeLog
- Package mutiboot.bin
- Update for how extboot is built
- Fix sf.net source URL
- Drop qemu-fix-ppc-softmmu-kvm-disabled-build.patch
- Drop qemu-fix-pcspk-build-with-kvm-disabled.patch
- Cherry-pick fix for esound support build failure

* Wed Jul 15 2009 Daniel Berrange <berrange@lettuce.camlab.fab.redhat.com> - 2:0.10.50-10.kvm87
- Add udev rules to make /dev/kvm world accessible & group=kvm (rhbz #497341)
- Create a kvm group if it doesn't exist (rhbz #346151)

* Tue Jul 07 2009 Glauber Costa <glommer@redhat.com> - 2:0.10.50-9.kvm87
- use pxe roms from gpxe, instead of etherboot package.

* Fri Jul  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-8.kvm87
- Prefer sysfs over usbfs for usb passthrough (#508326)

* Sat Jun 27 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-7.kvm87
- Update to kvm-87
- Drop upstreamed patches
- Cherry-pick new ppc build fix from upstream
- Work around broken linux-user build on ppc
- Fix hw/pcspk.c build with --disable-kvm
- Re-enable preadv()/pwritev() since #497429 is long since fixed
- Kill petalogix-s3adsp1800.dtb, since we don't ship the microblaze target

* Fri Jun  5 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-6.kvm86
- Fix 'kernel requires an x86-64 CPU' error
- BuildRequires ncurses-devel to enable '-curses' option (#504226)

* Wed Jun  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-5.kvm86
- Prevent locked cdrom eject - fixes hang at end of anaconda installs (#501412)
- Avoid harmless 'unhandled wrmsr' warnings (#499712)

* Thu May 21 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-4.kvm86
- Update to kvm-86 release
- ChangeLog here: http://marc.info/?l=kvm&m=124282885729710

* Fri May  1 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-3.kvm85
- Really provide qemu-kvm as a metapackage for comps

* Tue Apr 28 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-2.kvm85
- Provide qemu-kvm as a metapackage for comps

* Mon Apr 27 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10.50-1.kvm85
- Update to qemu-kvm-devel-85
- kvm-85 is based on qemu development branch, currently version 0.10.50
- Include new qemu-io utility in qemu-img package
- Re-instate -help string for boot=on to fix virtio booting with libvirt
- Drop upstreamed patches
- Fix missing kernel/include/asm symlink in upstream tarball
- Fix target-arm build
- Fix build on ppc
- Disable preadv()/pwritev() until bug #497429 is fixed
- Kill more .kernelrelease uselessness
- Make non-kvm qemu build verbose

* Fri Apr 24 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-15
- Fix source numbering typos caused by make-release addition

* Thu Apr 23 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-14
- Improve instructions for generating the tarball

* Tue Apr 21 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-13
- Enable pulseaudio driver to fix qemu lockup at shutdown (#495964)

* Tue Apr 21 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-12
- Another qcow2 image corruption fix (#496642)

* Mon Apr 20 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-11
- Fix qcow2 image corruption (#496642)

* Sun Apr 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-10
- Run sysconfig.modules from %%post on x86_64 too (#494739)

* Sun Apr 19 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-9
- Align VGA ROM to 4k boundary - fixes 'qemu-kvm -std vga' (#494376)

* Tue Apr  14 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-8
- Provide qemu-kvm conditional on the architecture.

* Thu Apr  9 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-7
- Add a much cleaner fix for vga segfault (#494002)

* Sun Apr  5 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-6
- Fixed qcow2 segfault creating disks over 2TB. #491943

* Fri Apr  3 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-5
- Fix vga segfault under kvm-autotest (#494002)
- Kill kernelrelease hack; it's not needed
- Build with "make V=1" for more verbose logs

* Thu Apr 02 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-4
- Support botting gpxe roms.

* Wed Apr 01 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-2
- added missing patch. love for CVS.

* Wed Apr 01 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-1
- Include debuginfo for qemu-img
- Do not require qemu-common for qemu-img
- Explicitly own each of the firmware files
- remove firmwares for ppc and sparc. They should be provided by an external package.
  Not that the packages exists for sparc in the secondary arch repo as noarch, but they
  don't automatically get into main repos. Unfortunately it's the best we can do right
  now.
- rollback a bit in time. Snapshot from avi's maint/2.6.30
  - this requires the sasl patches to come back.
  - with-patched-kernel comes back.

* Wed Mar 25 2009 Mark McLoughlin <markmc@redhat.com> - 2:0.10-0.12.kvm20090323git
- BuildRequires pciutils-devel for device assignment (#492076)

* Mon Mar 23 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.11.kvm20090323git
- Update to snapshot kvm20090323.
- Removed patch2 (upstream).
- use upstream's new split package.
- --with-patched-kernel flag not needed anymore
- Tell how to get the sources.

* Wed Mar 18 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.10.kvm20090310git
- Added extboot to files list.

* Wed Mar 11 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.9.kvm20090310git
- Fix wrong reference to bochs bios.

* Wed Mar 11 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.8.kvm20090310git
- fix Obsolete/Provides pair
- Use kvm bios from bochs-bios package.
- Using RPM_OPT_FLAGS in configure
- Picked back audio-drv-list from kvm package

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.7.kvm20090310git
- modify ppc patch

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.6.kvm20090310git
- updated to kvm20090310git
- removed sasl patches (already in this release)

* Tue Mar 10 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.5.kvm20090303git
- kvm.modules were being wrongly mentioned at %%install.
- update description for the x86 system package to include kvm support
- build kvm's own bios. It is still necessary while kvm uses a slightly different
  irq routing mechanism

* Thu Mar 05 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.4.kvm20090303git
- seems Epoch does not go into the tags. So start back here.

* Thu Mar 05 2009 Glauber Costa <glommer@redhat.com> - 2:0.10-0.1.kvm20090303git
- Use bochs-bios instead of bochs-bios-data
- It's official: upstream set on 0.10

* Thu Mar  5 2009 Daniel P. Berrange <berrange@redhat.com> - 2:0.9.2-0.2.kvm20090303git
- Added BSD to license list, since many files are covered by BSD

* Wed Mar 04 2009 Glauber Costa <glommer@redhat.com> - 0.9.2-0.1.kvm20090303git
- missing a dot. shame on me

* Wed Mar 04 2009 Glauber Costa <glommer@redhat.com> - 0.92-0.1.kvm20090303git
- Set Epoch to 2
- Set version to 0.92. It seems upstream keep changing minds here, so pick the lowest
- Provides KVM, Obsoletes KVM
- Only install qemu-kvm in ix86 and x86_64
- Remove pkgdesc macros, as they were generating bogus output for rpm -qi.
- fix ppc and ppc64 builds

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.3.kvm20090303git
- only execute post scripts for user package.
- added kvm tools.

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.2.kvm20090303git
- put kvm.modules into cvs

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 0.10-0.1.kvm20090303git
- Set Epoch to 1
- Build KVM (basic build, no tools yet)
- Set ppc in ExcludeArch. This is temporary, just to fix one issue at a time.
  ppc users (IBM ? ;-)) please wait a little bit.

* Tue Mar  3 2009 Daniel P. Berrange <berrange@redhat.com> - 1.0-0.5.svn6666
- Support VNC SASL authentication protocol
- Fix dep on bochs-bios-data

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.4.svn6666
- use bios from bochs-bios package.

* Tue Mar 03 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.3.svn6666
- use vgabios from vgabios package.

* Mon Mar 02 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.2.svn6666
- use pxe roms from etherboot package.

* Mon Mar 02 2009 Glauber Costa <glommer@redhat.com> - 1.0-0.1.svn6666
- Updated to tip svn (release 6666). Featuring split packages for qemu.
  Unfortunately, still using binary blobs for the bioses.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 11 2009 Debarshi Ray <rishi@fedoraproject.org> - 0.9.1-12
- Updated build patch. Closes Red Hat Bugzilla bug #465041.

* Wed Dec 31 2008 Dennis Gilmore <dennis@ausil.us> - 0.9.1-11
- add sparcv9 and sparc64 support

* Fri Jul 25 2008 Bill Nottingham <notting@redhat.com>
- Fix qemu-img summary (#456344)

* Wed Jun 25 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-10.fc10
- Rebuild for GNU TLS ABI change

* Wed Jun 11 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-9.fc10
- Remove bogus wildcard from files list (rhbz #450701)

* Sat May 17 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.9.1-8
- Register binary handlers also for shared libraries

* Mon May  5 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-7.fc10
- Fix text console PTYs to be in rawmode

* Sun Apr 27 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.9.1-6
- Register binary handler for SuperH-4 CPU

* Wed Mar 19 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-5.fc9
- Split qemu-img tool into sub-package for smaller footprint installs

* Wed Feb 27 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-4.fc9
- Fix block device checks for extendable disk formats (rhbz #435139)

* Sat Feb 23 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-3.fc9
- Fix block device extents check (rhbz #433560)

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.9.1-2
- Autorebuild for GCC 4.3

* Tue Jan  8 2008 Daniel P. Berrange <berrange@redhat.com> - 0.9.1-1.fc9
- Updated to 0.9.1 release
- Fix license tag syntax
- Don't mark init script as a config file

* Wed Sep 26 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-5.fc8
- Fix rtl8139 checksum calculation for Vista (rhbz #308201)

* Tue Aug 28 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-4.fc8
- Fix debuginfo by passing -Wl,--build-id to linker

* Tue Aug 28 2007 David Woodhouse <dwmw2@infradead.org> 0.9.0-4
- Update licence
- Fix CDROM emulation (#253542)

* Tue Aug 28 2007 Daniel P. Berrange <berrange@redhat.com> - 0.9.0-3.fc8
- Added backport of VNC password auth, and TLS+x509 cert auth
- Switch to rtl8139 NIC by default for linkstate reporting
- Fix rtl8139 mmio region mappings with multiple NICs

* Sun Apr  1 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.9.0-2
- Fix direct loading of a linux kernel with -kernel & -initrd (bz 234681)
- Remove spurious execute bits from manpages (bz 222573)

* Tue Feb  6 2007 David Woodhouse <dwmw2@infradead.org> 0.9.0-1
- Update to 0.9.0

* Wed Jan 31 2007 David Woodhouse <dwmw2@infradead.org> 0.8.2-5
- Include licences

* Mon Nov 13 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.8.2-4
- Backport patch to make FC6 guests work by Kevin Kofler
  <Kevin@tigcc.ticalc.org> (bz 207843).

* Mon Sep 11 2006 David Woodhouse <dwmw2@infradead.org> 0.8.2-3
- Rebuild

* Thu Aug 24 2006 Matthias Saou <http://freshrpms.net/> 0.8.2-2
- Remove the target-list iteration for x86_64 since they all build again.
- Make gcc32 vs. gcc34 conditional on %%{fedora} to share the same spec for
  FC5 and FC6.

* Wed Aug 23 2006 Matthias Saou <http://freshrpms.net/> 0.8.2-1
- Update to 0.8.2 (#200065).
- Drop upstreamed syscall-macros patch2.
- Put correct scriplet dependencies.
- Force install mode for the init script to avoid umask problems.
- Add %%postun condrestart for changes to the init script to be applied if any.
- Update description with the latest "about" from the web page (more current).
- Update URL to qemu.org one like the Source.
- Add which build requirement.
- Don't include texi files in %%doc since we ship them in html.
- Switch to using gcc34 on devel, FC5 still has gcc32.
- Add kernheaders patch to fix linux/compiler.h inclusion.
- Add target-sparc patch to fix compiling on ppc (some int32 to float).

* Thu Jun  8 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-3
- More header abuse in modify_ldt(), change BuildRoot:

* Wed Jun  7 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-2
- Fix up kernel header abuse

* Tue May 30 2006 David Woodhouse <dwmw2@infradead.org> 0.8.1-1
- Update to 0.8.1

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-6
- Update linker script for PPC

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-5
- Just drop $RPM_OPT_FLAGS. They're too much of a PITA

* Sat Mar 18 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-4
- Disable stack-protector options which gcc 3.2 doesn't like

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-3
- Use -mcpu= instead of -mtune= on x86_64 too
- Disable SPARC targets on x86_64, because dyngen doesn't like fnegs

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-2
- Don't use -mtune=pentium4 on i386. GCC 3.2 doesn't like it

* Fri Mar 17 2006 David Woodhouse <dwmw2@infradead.org> 0.8.0-1
- Update to 0.8.0
- Resort to using compat-gcc-32
- Enable ALSA

* Mon May 16 2005 David Woodhouse <dwmw2@infradead.org> 0.7.0-2
- Proper fix for GCC 4 putting 'blr' or 'ret' in the middle of the function,
  for i386, x86_64 and PPC.

* Sat Apr 30 2005 David Woodhouse <dwmw2@infradead.org> 0.7.0-1
- Update to 0.7.0
- Fix dyngen for PPC functions which end in unconditional branch

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sun Feb 13 2005 David Woodhouse <dwmw2@infradead.org> 0.6.1-2
- Package cleanup

* Sun Nov 21 2004 David Woodhouse <dwmw2@redhat.com> 0.6.1-1
- Update to 0.6.1

* Tue Jul 20 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-2
- Compile fix from qemu CVS, add x86_64 host support

* Wed May 12 2004 David Woodhouse <dwmw2@redhat.com> 0.6.0-1
- Update to 0.6.0.

* Sat May 8 2004 David Woodhouse <dwmw2@redhat.com> 0.5.5-1
- Update to 0.5.5.

* Sun May 2 2004 David Woodhouse <dwmw2@redhat.com> 0.5.4-1
- Update to 0.5.4.

* Thu Apr 22 2004 David Woodhouse <dwmw2@redhat.com> 0.5.3-1
- Update to 0.5.3. Add init script.

* Thu Jul 17 2003 Jeff Johnson <jbj@redhat.com> 0.4.3-1
- Create.
