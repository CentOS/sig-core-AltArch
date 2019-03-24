# Basic setup information
url --url="http://mirror.centos.org/altarch/7/os/armhfp/"
install
keyboard us --xlayouts=us --vckeymap=us
rootpw centos
timezone --isUtc --nontp UTC
selinux --enforcing
firewall --enabled --port=22
network --bootproto=dhcp --device=link --activate --onboot=on
shutdown
bootloader --location=mbr
lang en_US.UTF-8

# Repositories to use
repo --name="instCentOS" --baseurl=http://mirror.centos.org/altarch/7/os/armhfp/ --cost=100
repo --name="instUpdates" --baseurl=http://mirror.centos.org/altarch/7/updates/armhfp/ --cost=100
repo --name="instExtras" --baseurl=http://mirror.centos.org/altarch/7/extras/armhfp/ --cost=100
repo --name="instKern" --baseurl=http://mirror.centos.org/altarch/7/kernel/armhfp/kernel-generic/ --cost=100

# Disk setup
clearpart --initlabel --all
part /boot/fw --asprimary --fstype=vfat --size=30
part /boot  --fstype=ext3   --size=700  --label=boot --asprimary
part swap --fstype=swap --size=512 --label=swap --asprimary
part / --fstype=ext4 --size=3600 --label=rootfs --asprimary

# Package setup
%packages
@core
@x11
@kde
net-tools
cloud-utils-growpart
chrony
kernel
dracut-config-generic
-dracut-config-rescue
extlinux-bootloader
bcm283x-firmware
uboot-images-armv7

%end

%pre

#End of Pre script for partitions
%end

%post

# Mandatory README file
cat >/root/README << EOF
== CentOS 7 userland ==

If you want to automatically resize your / partition, just type the following (as root user):
rootfs-expand

EOF

# Enabling chronyd on boot
systemctl enable chronyd

# Setting correct yum variable to use mainline kernel repo
echo "generic" > /etc/yum/vars/kvariant

# For cubietruck WiFi : kernel module works and linux-firmware has the needed file
# But it just needs a .txt config file

cat > /lib/firmware/brcm/brcmfmac43362-sdio.txt << EOF

AP6210_NVRAM_V1.2_03192013
manfid=0x2d0
prodid=0x492
vendid=0x14e4
devid=0x4343
boardtype=0x0598

# Board Revision is P307, same nvram file can be used for P304, P305, P306 and P307 as the tssi pa params used are same
#Please force the automatic RX PER data to the respective board directory if not using P307 board, for e.g. for P305 boards force the data into the following directory /projects/BCM43362/a1_labdata/boardtests/results/sdg_rev0305
boardrev=0x1307
boardnum=777
xtalfreq=26000
boardflags=0x80201
boardflags2=0x80
sromrev=3
wl0id=0x431b
macaddr=00:90:4c:07:71:12
aa2g=1
ag0=2
maxp2ga0=74
cck2gpo=0x2222
ofdm2gpo=0x44444444
mcs2gpo0=0x6666
mcs2gpo1=0x6666
pa0maxpwr=56

#P207 PA params
#pa0b0=5447
#pa0b1=-658
#pa0b2=-175<div></div>

#Same PA params for P304,P305, P306, P307

pa0b0=5447
pa0b1=-607
pa0b2=-160
pa0itssit=62
pa1itssit=62


cckPwrOffset=5
ccode=0
rssismf2g=0xa
rssismc2g=0x3
rssisav2g=0x7
triso2g=0
noise_cal_enable_2g=0
noise_cal_po_2g=0
swctrlmap_2g=0x04040404,0x02020202,0x02020202,0x010101,0x1ff
temp_add=29767
temp_mult=425

btc_flags=0x6
btc_params0=5000
btc_params1=1000
btc_params6=63

EOF

# For RaspberryPi 2 and 3 (firmware)
# depends on uboot-images-armv7 and bcm283x-firmware pkgs
cp -Pr /usr/share/bcm283x-firmware/* /boot/fw/
cp -P /usr/share/uboot/rpi_2/u-boot.bin /boot/fw/rpi2-u-boot.bin
cp -P /usr/share/uboot/rpi_3_32b/u-boot.bin /boot/fw/rpi3-u-boot.bin

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




# Remove ifcfg-link on pre generated images
rm -f /etc/sysconfig/network-scripts/ifcfg-link

# Remove machine-id on pre generated images
rm -f /etc/machine-id
touch /etc/machine-id

%end
