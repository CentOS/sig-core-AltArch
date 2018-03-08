#global candidate rc3

Name:      uboot-tools
Version:   2018.01
Release:   1%{?candidate:.%{candidate}}%{?dist}
Summary:   U-Boot utilities
License:   GPLv2+ BSD LGPL-2.1+ LGPL-2.0+
URL:       http://www.denx.de/wiki/U-Boot

Source0:   ftp://ftp.denx.de/pub/u-boot/u-boot-%{version}%{?candidate:-%{candidate}}.tar.bz2
Source1:   arm-boards
Source2:   arm-chromebooks
Source3:   aarch64-boards
Source4:   aarch64-chromebooks
Source5:   10-devicetree.install

# Fedoraisms patches
Patch1:    uefi-use-Fedora-specific-path-name.patch

# general fixes
Patch2:    uefi-distro-load-FDT-from-any-partition-on-boot-device.patch
Patch3:    usb-kbd-fixes.patch

# Board fixes and enablement
Patch10:   db-generic-fixes.patch
Patch11:   db410c-fixes.patch
Patch12:   db820c-support.patch
Patch13:   dragonboard-fixes.patch
# Patch14:   mvebu-enable-generic-distro-boot-config.patch
# Patch15:   mx6-Initial-Hummingboard-2-support.patch

BuildRequires:  bc
BuildRequires:  dtc
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  openssl-devel
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-libfdt
BuildRequires:  SDL-devel
BuildRequires:  swig
%ifarch %{arm} aarch64
BuildRequires:  vboot-utils
%endif
%ifarch aarch64
BuildRequires:  arm-trusted-firmware-armv8
%endif

Requires:       dtc
Requires:       systemd

%description
This package contains a few U-Boot utilities - mkimage for creating boot images
and fw_printenv/fw_setenv for manipulating the boot environment variables.

%ifarch aarch64
%package     -n uboot-images-armv8
Summary:     u-boot bootloader images for aarch64 boards
Requires:    uboot-tools
BuildArch:   noarch

%description -n uboot-images-armv8
u-boot bootloader binaries for aarch64 boards
%endif

%ifarch %{arm}
%package     -n uboot-images-armv7
Summary:     u-boot bootloader images for armv7 boards
Requires:    uboot-tools
BuildArch:   noarch

%description -n uboot-images-armv7
u-boot bootloader binaries for armv7 boards
%endif

%ifarch %{arm} aarch64
%package     -n uboot-images-elf
Summary:     u-boot bootloader images for armv7 boards
Requires:    uboot-tools
Obsoletes:   uboot-images-qemu
Provides:    uboot-images-qemu

%description -n uboot-images-elf
u-boot bootloader ELF binaries for use with qemu and other platforms
%endif

%prep
%setup -q -n u-boot-%{version}%{?candidate:-%{candidate}}

git init
git config --global gc.auto 0
git config user.email "noone@example.com" 
git config user.name "no one" 
git add . 
git commit -a -q -m "%{version} baseline" 
git am %{patches} </dev/null 
git config --unset user.email 
git config --unset user.name 
rm -rf .git

cp %SOURCE1 %SOURCE2 %SOURCE3 %SOURCE4 .

%build
mkdir builds

%ifarch aarch64 %{arm}
for board in $(cat %{_arch}-boards)
do
  echo "Building board: $board"
  mkdir builds/$(echo $board)/
  # ATF selection, needs improving, suggestions of ATF SoC to Board matrix welcome
  sun50i=(pine64_plus a64-olinuxino bananapi_m64 nanopi_a64 nanopi_neo2 orangepi_pc2 orangepi_prime orangepi_win orangepi_zero_plus2 sopine_baseboard)
  if [[ " ${sun50i[*]} " == *" $board "* ]]; then
    echo "Board: $board using sun50iw1p1"
    cp /usr/share/arm-trusted-firmware/sun50iw1p1/bl31.bin builds/$(echo $board)/
  fi
  rk3368=(geekbox sheep-rk3368)
  if [[ " ${rk3368[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3368"
    cp /usr/share/arm-trusted-firmware/rk3368/bl31.bin builds/$(echo $board)/
  fi
  rk3399=(evb-rk3399 firefly-rk3399 puma-rk3399)
  if [[ " ${rk3399[*]} " == *" $board "* ]]; then
    echo "Board: $board using rk3399"
    cp /usr/share/arm-trusted-firmware/rk3399/bl31.bin builds/$(echo $board)/
  fi
  # End ATF
  make $(echo $board)_defconfig O=builds/$(echo $board)/
  make HOSTCC="gcc $RPM_OPT_FLAGS" CROSS_COMPILE="" %{?_smp_mflags} V=1 O=builds/$(echo $board)/
done

%endif

make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" defconfig V=1 O=builds/
make HOSTCC="gcc $RPM_OPT_FLAGS" %{?_smp_mflags} CROSS_COMPILE="" tools-all V=1 O=builds/

%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/

%ifarch aarch64
for board in $(cat %{_arch}-boards)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in spl/*spl.bin u-boot.bin u-boot.dtb u-boot-dtb.img u-boot.img u-boot.itb spl/sunxi-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
  fi
 done
done
%endif

%ifarch %{arm}
for board in $(cat %{_arch}-boards)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in MLO SPL spl/arndale-spl.bin spl/origen-spl.bin spl/smdkv310-spl.bin spl/*spl.bin u-boot.bin u-boot.dtb u-boot-dtb-tegra.bin u-boot.img u-boot.imx u-boot-nodtb-tegra.bin u-boot-spl.kwb u-boot-sunxi-with-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
  fi
 done

done

# Bit of a hack to remove binaries we don't use as they're large
for board in $(cat %{_arch}-boards)
do
  if [ -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot-sunxi-with-spl.bin ]; then
    rm -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.*
  fi
  if [ -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/MLO ]; then
    rm -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
  if [ -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/SPL ]; then
    rm -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
  if [ -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.imx ]; then
    rm -f $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/u-boot.bin
  fi
done
%endif

%ifarch aarch64
for board in $(cat %{_arch}-boards)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
 for file in MLO SPL spl/arndale-spl.bin spl/origen-spl.bin spl/smdkv310-spl.bin u-boot.bin u-boot.dtb u-boot-dtb-tegra.bin u-boot.img u-boot.imx u-boot-nodtb-tegra.bin u-boot-spl.kwb u-boot-sunxi-with-spl.bin
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/$(echo $board)/
  fi
 done
done
%endif

# ELF binaries
%ifarch %{arm}
for board in vexpress_ca15_tc2 vexpress_ca9x4
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/elf/$(echo $board)/
 for file in u-boot
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/elf/$(echo $board)/
  fi
 done
done
%endif

%ifarch aarch64
for board in $(cat %{_arch}-boards)
do
mkdir -p $RPM_BUILD_ROOT%{_datadir}/uboot/elf/$(echo $board)/
 for file in u-boot
 do
  if [ -f builds/$(echo $board)/$(echo $file) ]; then
    install -p -m 0644 builds/$(echo $board)/$(echo $file) $RPM_BUILD_ROOT%{_datadir}/uboot/elf/$(echo $board)/
  fi
 done
done
%endif

for tool in bmp_logo dumpimage easylogo/easylogo env/fw_printenv fit_check_sign fit_info gdb/gdbcont gdb/gdbsend gen_eth_addr gen_ethaddr_crc img2srec mkenvimage mkimage mksunxiboot ncb proftool sunxi-spl-image-builder ubsha1 xway-swap-bytes
do
install -p -m 0755 builds/tools/$tool $RPM_BUILD_ROOT%{_bindir}
done
install -p -m 0644 doc/mkimage.1 $RPM_BUILD_ROOT%{_mandir}/man1

install -p -m 0755 builds/tools/env/fw_printenv $RPM_BUILD_ROOT%{_bindir}
( cd $RPM_BUILD_ROOT%{_bindir}; ln -sf fw_printenv fw_setenv )

install -p -m 0644 tools/env/fw_env.config $RPM_BUILD_ROOT%{_sysconfdir}

# systemd kernel-install script for device tree
mkdir -p $RPM_BUILD_ROOT/lib/kernel/install.d/
install -p -m 0755 %{SOURCE5} $RPM_BUILD_ROOT/lib/kernel/install.d/

# Copy sone useful docs over
mkdir -p builds/docs
cp -p board/amlogic/odroid-c2/README builds/docs/README.odroid-c2
cp -p board/hisilicon/hikey/README builds/docs/README.hikey
cp -p board/hisilicon/hikey/README builds/docs/README.hikey
cp -p board/Marvell/db-88f6820-gp/README builds/docs/README.mvebu-db-88f6820
cp -p board/rockchip/evb_rk3399/README builds/docs/README.evb_rk3399
cp -p board/solidrun/clearfog/README builds/docs/README.clearfog
cp -p board/solidrun/mx6cuboxi/README builds/docs/README.mx6cuboxi
cp -p board/sunxi/README.sunxi64 builds/docs/README.sunxi64
cp -p board/sunxi/README.nand builds/docs/README.sunxi-nand
cp -p board/ti/am335x/README builds/docs/README.am335x
cp -p board/ti/omap5_uevm/README builds/docs/README.omap5_uevm
cp -p board/udoo/README builds/docs/README.udoo
cp -p board/wandboard/README builds/docs/README.wandboard
cp -p board/warp/README builds/docs/README.warp
cp -p board/warp7/README builds/docs/README.warp7

%files
%doc README doc/README.imximage doc/README.kwbimage doc/README.distro doc/README.gpt
%doc doc/README.odroid doc/README.rockchip doc/README.efi doc/uImage.FIT doc/README.arm64
%doc doc/README.chromium builds/docs/*
%{_bindir}/*
%{_mandir}/man1/mkimage.1*
/lib/kernel/install.d/10-devicetree.install
%dir %{_datadir}/uboot/
%config(noreplace) %{_sysconfdir}/fw_env.config

%ifarch aarch64
%files -n uboot-images-armv8
%{_datadir}/uboot/*
%exclude %{_datadir}/uboot/elf
%endif

%ifarch %{arm}
%files -n uboot-images-armv7
%{_datadir}/uboot/*
%exclude %{_datadir}/uboot/elf
%endif

%ifarch %{arm} aarch64
%files -n uboot-images-elf
%{_datadir}/uboot/elf
%endif

%changelog
* Tue Jan  9 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.01-1
- 2018.01

* Tue Jan  2 2018 Peter Robinson <pbrobinson@fedoraproject.org> 2018.01-0.2.rc3
- 2018.01 RC3

* Tue Dec 19 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2018.01-0.1.rc2
- 2018.01 RC2

* Thu Nov 23 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.11-3
- Newer EFI loader fix patch
- Fix static MAC on omap3/omap4 devices

* Tue Nov 21 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.11-2
- Add EFI loader fix

* Wed Nov 15 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.11-1
- 2017.11

* Tue Nov  7 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.11-0.4.rc4
- 2017.11 RC4

* Sat Nov  4 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.11-0.3.rc3
- 2017.11 RC3

* Tue Oct 17 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.11-0.2.rc2
- Update / rebase a couple of patches

* Tue Oct 17 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.11-0.1.rc2
- 2017.11 RC2

* Tue Oct 10 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.09-4
- Improve uEFI partition detection for some devices

* Thu Oct  5 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.09-3
- Fix regression in i.MX6 and omap4 devices
- Improve DT detection support on aarch64
- uEFI fixes and improvements
- ENable Sinovoip BPI devices

* Wed Sep 27 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.09-2
- Add patch to fix some uEFI console output
- Minor other tweaks

* Mon Sep 18 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.09-1
- 2017.09

* Tue Sep 12 2017 Than Ngo <than@redhat.com> - 2017.09-0.6.rc4
- fixed the check for rockchip rk3368 boards

* Tue Sep  5 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.09-0.5.rc4
- 2017.09 RC4
- Add qemu arm target config

* Fri Aug 25 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.09-0.4.rc2
- Raspberry Pi and Allwinner fixes
- Enable some new devices

* Tue Aug 15 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.09-0.3.rc2
- 2017.09 RC2

* Thu Aug  3 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.09-0.2.rc1
- uEFI fixes
- DragonBoard 410c fixes

* Tue Aug  1 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.09-0.1.rc1
- 2017.09 RC1
- Initial patch rebase

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.07-1
- 2017.07

* Thu Jul  6 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.07-0.3.rc3
- 2017.07 RC3

* Tue Jun 20 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.07-0.2.rc2
- 2017.07 RC2
- Enable AllWinner: NanoPi M1+, NanoPi Neo2, SoPine baseboard, OrangePi Zero+2, OrangePi Win
- Enable Rockchips: GeekBox, Sheep
- Dragonboard fixes
- uEFI fixes

* Tue Jun  6 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.07-0.1.rc1
- 2017.07 RC1
- Build BananaPi m64, OrangePi pc2, OrangePi Prime with ATF

* Mon May 29 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-02
- Add distro-boot support for ClearFog
- Add support for building a chained u-boot for nyan-big

* Tue May  9 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-01
- 2017.05

* Wed May  3 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.7.rc7
- 2017.05 RC3

* Mon Apr 24 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.6.rc2
- Add SPL/ATF support for AllWinner A64 SoCs
- Ship u-boot elf binaries for all aarch64 devices
- Cleanups and spec updates
- Add some more docs/tools

* Mon Apr 17 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.5.rc2
- Ship the elf u-boot binaries for aarch64

* Mon Apr 17 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.4.rc2
- 2017.05 RC2

* Tue Apr 11 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.3.rc1
- Add support for STi STiH410

* Wed Apr  5 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.2.rc1
- Build am335x_evm

* Wed Apr  5 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.05-0.1.rc1
- 2017.05 RC1
- Enable TinkerBoard and MacchiatoBIN

* Mon Mar 20 2017 Jon Disnard <parasense@fedoraproject.org> 2017.03-2
- Pass --no-dynamic-linker for linkers newer than 2.26 
- Add build dependency on gcc

* Mon Mar 13 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-1
- 2017.03

* Mon Mar  6 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-0.7.rc3
- Add support for SATA on Cubox-i and Hummingboard
- Add initial Hummingboard 2 (Gate/Edge) support
- Add initial Marvell ESPRESSOBin board support

* Tue Feb 28 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-0.6.rc3
- 2017.03 RC3

* Wed Feb 15 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-0.5.rc2
- Rebase OpenSSL 1.1 patches

* Mon Feb 13 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-0.4.rc2
- 2017.03 RC2
- Temporarily drop OpenSSL 1.1 patches (need rebase)
- Add fix for UDOO Neo distro boot

* Mon Feb 13 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-0.3.rc1
- Add patches to fix build against OpenSSL 1.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2017.03-0.2.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.03-0.1.rc1
- 2017.03 RC1

* Tue Jan 10 2017 Peter Robinson <pbrobinson@fedoraproject.org> 2017.01-1
- 2017.01
