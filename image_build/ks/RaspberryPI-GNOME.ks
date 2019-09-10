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
repo --name="instCentOS" --baseurl=http://mirror.centos.org/altarch/7/os/armhfp/ --cost=100
repo --name="instUpdates" --baseurl=http://mirror.centos.org/altarch/7/updates/armhfp/ --cost=100
repo --name="instCentCR" --baseurl=http://mirror.centos.org/altarch/7/cr/armhfp/ --cost=100
repo --name="instExtras" --baseurl=http://mirror.centos.org/altarch/7/extras/armhfp/ --cost=100
repo --name="instKern" --baseurl=http://mirror.centos.org/altarch/7/kernel/armhfp/kernel-rpi2/ --cost=100

# Disk setup
clearpart --initlabel --all
part /boot --asprimary --fstype=vfat --size=300 --label=boot
part swap --asprimary --fstype=swap --size=512 --label=swap
part / --asprimary --fstype=ext4 --size=4000 --label=rootfs

# Package setup
%packages
@core
@gnome-desktop
@x11
chrony
cloud-utils-growpart
firefox
net-tools
raspberrypi-vc-utils
raspberrypi2-firmware
raspberrypi2-kernel
uboot-images-armv7
-caribou*
-gnome-shell-browser-plugin
-java-1.6.0-*
-java-1.7.0-*
-java-11-*
-python*-caribou*

%end

%pre

#End of Pre script for partitions
%end

%post
# Generating initrd
export kvr=$(rpm -q --queryformat '%{version}-%{release}' $(rpm -q raspberrypi2-kernel|tail -n 1))
dracut --force /boot/initramfs-$kvr.armv7hl.img $kvr.armv7hl


# Mandatory README file
cat >/root/README << EOF
== CentOS 7 userland ==

If you want to automatically resize your / partition, just type the following (as root user):
rootfs-expand

EOF

# Enabling chronyd on boot
systemctl enable chronyd


# Specific cmdline.txt files needed for raspberrypi2/3
cat > /boot/cmdline.txt << EOF
console=ttyAMA0,115200 console=tty1 root=/dev/mmcblk0p3 rootfstype=ext4 elevator=deadline rootwait
EOF

# Setting correct yum variable to use raspberrypi kernel repo
echo "rpi2" > /etc/yum/vars/kvariant


# RaspberryPi 3 config for wifi
cat > /usr/lib/firmware/brcm/brcmfmac43430-sdio.txt << EOF
# NVRAM file for BCM943430WLPTH
# 2.4 GHz, 20 MHz BW mode

# The following parameter values are just placeholders, need to be updated.
manfid=0x2d0
prodid=0x0727
vendid=0x14e4
devid=0x43e2
boardtype=0x0727
boardrev=0x1101
boardnum=22
#macaddr=00:90:4c:c5:12:38
sromrev=11
boardflags=0x00404201
boardflags3=0x08000000
xtalfreq=37400
nocrc=1
ag0=255
aa2g=1
ccode=ALL

pa0itssit=0x20
extpagain2g=0
#PA parameters for 2.4GHz, measured at CHIP OUTPUT
pa2ga0=-168,7161,-820
AvVmid_c0=0x0,0xc8
cckpwroffset0=5

# PPR params
maxp2ga0=84
txpwrbckof=6
cckbw202gpo=0
legofdmbw202gpo=0x66111111
mcsbw202gpo=0x77711111
propbw202gpo=0xdd

# OFDM IIR :
ofdmdigfilttype=18
ofdmdigfilttypebe=18
# PAPD mode:
papdmode=1
papdvalidtest=1
pacalidx2g=42
papdepsoffset=-22
papdendidx=58

# LTECX flags
ltecxmux=0
ltecxpadnum=0x0102
ltecxfnsel=0x44
ltecxgcigpio=0x01

il0macaddr=00:90:4c:c5:12:38
wl0id=0x431b

deadman_to=0xffffffff
# muxenab: 0x1 for UART enable, 0x2 for GPIOs, 0x8 for JTAG
muxenab=0x1
# CLDO PWM voltage settings - 0x4 - 1.1 volt
#cldo_pwm=0x4

#VCO freq 326.4MHz
spurconfig=0x3

edonthd20l=-75
edoffthd20ul=-80

EOF

# RaspberryPI 3 model+ wifi
cat > /usr/lib/firmware/brcm/brcmfmac43455-sdio.txt << EOF
# Cloned from bcm94345wlpagb_p2xx.txt
NVRAMRev=$Rev: 498373 $
sromrev=11
vendid=0x14e4
devid=0x43ab
manfid=0x2d0
prodid=0x06e4
#macaddr=00:90:4c:c5:12:38
macaddr=b8:27:eb:74:f2:6c
nocrc=1
boardtype=0x6e4
boardrev=0x1304

#XTAL 37.4MHz
xtalfreq=37400

btc_mode=1
#------------------------------------------------------
#boardflags: 5GHz eTR switch by default
#            2.4GHz eTR switch by default
#            bit1 for btcoex
boardflags=0x00480201
boardflags2=0x40800000
boardflags3=0x44200100
phycal_tempdelta=15
rxchain=1
txchain=1
aa2g=1
aa5g=1
tssipos5g=1
tssipos2g=1
femctrl=0
AvVmid_c0=1,165,2,100,2,100,2,100,2,100
pa2ga0=-129,6525,-718
pa2ga1=-149,4408,-601
pa5ga0=-185,6836,-815,-186,6838,-815,-184,6859,-815,-184,6882,-818
pa5ga1=-202,4285,-574,-201,4312,-578,-196,4391,-586,-201,4294,-575
itrsw=1
pdoffsetcckma0=2
pdoffset2gperchan=0,-2,1,0,1,0,1,1,1,0,0,-1,-1,0
pdoffset2g40ma0=16
pdoffset40ma0=0x8888
pdoffset80ma0=0x8888
extpagain5g=2
extpagain2g=2
tworangetssi2g=1
tworangetssi5g=1
# LTECX flags
# WCI2
ltecxmux=0
ltecxpadnum=0x0504
ltecxfnsel=0x22
ltecxgcigpio=0x32

maxp2ga0=80
ofdmlrbw202gpo=0x0022
dot11agofdmhrbw202gpo=0x4442
mcsbw202gpo=0x98444422
mcsbw402gpo=0x98444422
maxp5ga0=82,82,82,82
mcsbw205glpo=0xb9555000
mcsbw205gmpo=0xb9555000
mcsbw205ghpo=0xb9555000
mcsbw405glpo=0xb9555000
mcsbw405gmpo=0xb9555000
mcsbw405ghpo=0xb9555000
mcsbw805glpo=0xb9555000
mcsbw805gmpo=0xb9555000
mcsbw805ghpo=0xb9555000

swctrlmap_2g=0x00000000,0x00000000,0x00000000,0x010000,0x3ff
swctrlmap_5g=0x00100010,0x00200020,0x00200020,0x010000,0x3fe
swctrlmapext_5g=0x00000000,0x00000000,0x00000000,0x000000,0x3
swctrlmapext_2g=0x00000000,0x00000000,0x00000000,0x000000,0x3

vcodivmode=1
deadman_to=481500000

ed_thresh2g=-54
ed_thresh5g=-54
eu_edthresh2g=-54
eu_edthresh5g=-54
ldo1=4
rawtempsense=0x1ff
cckPwrIdxCorr=3
cckTssiDelay=150
ofdmTssiDelay=150
txpwr2gAdcScale=1
txpwr5gAdcScale=1
dot11b_opts=0x3aa85
cbfilttype=1
fdsslevel_ch11=6

# Improved Bluetooth coexistence parameters from Cypress
btc_mode=1
btc_params8=0x4e20
btc_params1=0x7530

EOF


# Remove ifcfg-link on pre generated images
rm -f /etc/sysconfig/network-scripts/ifcfg-link

# Remove machine-id on pre generated images
rm -f /etc/machine-id
touch /etc/machine-id

%end
