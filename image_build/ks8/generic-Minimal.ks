# Basic setup information
url --url="http://mirror.centos.org/altarch/7/os/armhfp/"
install
keyboard us --xlayouts=us --vckeymap=us
rootpw --plaintext centos
timezone --isUtc --nontp UTC
selinux --enforcing
firewall --enabled --port=22:tcp
network --bootproto=dhcp --device=link --activate --onboot=on
services --enabled=sshd,NetworkManager,chronyd
shutdown
bootloader --location=mbr
lang en_US.UTF-8

# Repositories to use
%include repos.ksi

# Disk setup
clearpart --initlabel --all
part /boot/efi --asprimary --fstype=vfat --size=80
part /boot --asprimary --fstype=ext4 --size=700 --label=boot
part swap --asprimary --fstype=swap --size=512 --label=swap
part / --asprimary --fstype=ext4 --size=2000 --label=rootfs

# Package setup
%packages
@core
bcm283x-firmware
chrony
cloud-utils-growpart
dracut-config-generic
efi-filesystem
efibootmgr
extlinux-bootloader
grub2-common
grub2-efi-arm
grub2-efi-modules
-grubby
grubby-deprecated
kernel
net-tools
NetworkManager-wifi
uboot-images-armv7
-caribou*
-dracut-config-rescue
-gnome-shell-browser-plugin
-java-1.6.0-*
-java-1.7.0-*
-java-11-*
-python*-caribou*

%end

%pre

#End of Pre script for partitions
%end

%include readme.ksi
%include firmware_txt.ksi

%post
cat << EOF > /etc/default/grub
GRUB_ENABLE_BLSCFG=false
EOF
chmod 644 /etc/default/grub

# Enabling chronyd on boot
systemctl enable chronyd

# For RaspberryPi 2 and 3 (firmware)
# depends on uboot-images-armv7
cp -P /usr/share/uboot/rpi_2/u-boot.bin /boot/efi/rpi2-u-boot.bin
cp -P /usr/share/uboot/rpi_3_32b/u-boot.bin /boot/efi/rpi3-u-boot.bin
cp -P /usr/share/uboot/rpi_4_32b/u-boot.bin /boot/efi/rpi4-u-boot.bin

dnf -y remove dracut-config-generic

# Remove ifcfg-link on pre generated images
rm -f /etc/sysconfig/network-scripts/ifcfg-link

# Remove machine-id on pre generated images
rm -f /etc/machine-id
touch /etc/machine-id

%end
