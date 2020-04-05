# Basic setup information
%include "../ks.include/repo_armhfp.ksi"

%include "../ks.include/common.ksi"
%include "../ks.include/generic.ksi"
%include "../ks.include/wifi.ksi"
%include "../ks.include/pkgs_common_7.ksi"
%include "../ks.include/pkgs_exclude_7.ksi"
%include "../ks.include/pkgs_gnome_7.ksi"
%include "../ks.include/uboot32.ksi"

# Repositories to use
repo --name="instKern" --baseurl=http://mirror.centos.org/altarch/7/kernel/armhfp/kernel-generic/ --cost=100

# Disk setup
clearpart --initlabel --all
part /boot/fw --asprimary --fstype=vfat --size=30
part /boot --asprimary --fstype=ext3 --size=700 --label=boot
part swap --asprimary --fstype=swap --size=512 --label=swap
part / --asprimary --fstype=ext4 --size=4000 --label=rootfs
