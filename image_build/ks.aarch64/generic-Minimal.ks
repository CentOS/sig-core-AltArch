# Basic setup information
%include "../ks.include/repo_aarch64.ksi"

%include "../ks.include/common.ksi"
%include "../ks.include/generic.ksi"
%include "../ks.include/wifi.ksi"
%include "../ks.include/pkgs_common_7.ksi"
%include "../ks.include/pkgs_exclude_7.ksi"
%include "../ks.include/uboot64.ksi"

# Repositories to use
repo --name="instKern" --baseurl=http://mirror.centos.org/altarch/7/kernel/aarch64/kernel-generic/ --cost=100

# Disk setup
#clearpart --initlabel --all --disklabel=gpt
clearpart --initlabel --all
part /boot/efi --asprimary --fstype=efi --size=100
part /boot --asprimary --fstype=ext3 --size=700 --label=boot
part swap --asprimary --fstype=swap --size=512 --label=swap
part / --asprimary --fstype=ext4 --size=2200 --label=rootfs

%packages
dracut-config-extradrivers
-extlinux-bootloader
grub2
grub2-common
grub2-efi-aa64
grub2-efi-aa64-modules
efibootmgr
shim-aa64
uboot-images-armv8

%end

%post
# Generic efi filename for VMs
mkdir -p /boot/efi/EFI/BOOT
if [ -f /boot/efi/EFI/centos/grubaa64.efi ];then
    cp -f /boot/efi/EFI/centos/grubaa64.efi /boot/efi/EFI/BOOT/BOOTAA64.EFI
fi
#setup dtb link
if [ -x /lib/kernel/install.d/10-devicetree.install ];then
    /lib/kernel/install.d/10-devicetree.install remove
fi

cat << EOF > /etc/sysconfig/kernel
# Written by image installer
# UPDATEDEFAULT specifies if new-kernel-pkg should make new kernels the default
UPDATEDEFAULT=yes

# DEFAULTKERNEL specifies the default kernel package type
DEFAULTKERNEL=kernel
EOF
chmod 644 /etc/sysconfig/kernel

%end

%post --nochroot --erroronfail
/usr/bin/mount --bind /dev $INSTALL_ROOT/dev
cd $INSTALL_ROOT
/usr/sbin/chroot . /usr/sbin/grub2-mkconfig -o /etc/grub2-efi.cfg
/usr/bin/umount $INSTALL_ROOT/dev

%end
