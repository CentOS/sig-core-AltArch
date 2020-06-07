# Basic setup information
%include "../ks.include/repo_armhfp.ksi"

%include "../ks.include/common.ksi"
%include "../ks.include/RaspberryPI.ksi"
%include "../ks.include/wifi.ksi"
%include "../ks.include/pkgs_common_7.ksi"
%include "../ks.include/pkgs_exclude_7.ksi"
%include "../ks.include/pkgs_kde_7.ksi"

# Repositories to use
repo --name="instKern" --baseurl=http://mirror.centos.org/altarch/7/kernel/armhfp/kernel-rpi2/ --cost=100

# Disk setup
clearpart --initlabel --all
part /boot --asprimary --fstype=vfat --size=300 --label=boot
part swap --asprimary --fstype=swap --size=512 --label=swap
part / --asprimary --fstype=ext4 --size=4000 --label=rootfs

# Package setup
%packages
raspberrypi-vc-utils
raspberrypi2-firmware
raspberrypi2-kernel

%end

%post
# Generating initrd
export kvr=$(rpm -q --queryformat '%{version}-%{release}' $(rpm -q raspberrypi2-kernel|tail -n 1))
dracut --force /boot/initramfs-$kvr.armv7hl.img $kvr.armv7hl

%end
