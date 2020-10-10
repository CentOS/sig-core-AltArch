#!/bin/bash

for i in x86_64 i686 ppc ppc64 ppc64le aarch64 armv7hl power9;do
    filename=centos-release-7/$i/CentOS-Vault.repo
    echo "# CentOS Vault contains rpms from older releases in the CentOS-7">$filename
    echo "# tree." >>$filename

    versions=""
    if [ "$i" == "x86_64" ];then
        baseurl=""
    else
        baseurl='altarch/'
    fi
    if [ "$i" == "x86_64" -o "$i" == "i686" ];then
        altkey=""
    elif [ "$i" == "armv7hl" ];then
        altkey="
       file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-AltArch-7-Arm32"
    elif [ "$i" == "aarch64" ];then
        altkey="
       file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7-\$basearch"
    else
        altkey="
       file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-SIG-AltArch-7-\$basearch"
    fi
    if [ "$i" == "x86_64" ];then
        versions+="7.0.1406"
    fi
    if [ "$i" == "x86_64" -o "$i" == "i686" -o "$i" == "aarch64" ];then
        versions+=" 7.1.1503"
    fi
    versions+=" 7.2.1511"
    if [ "$i" == "aarch64" ];then
        versions+=" 7.2.1603"
    fi
    versions+=" 7.3.1611 7.4.1708"
    versions+=" 7.5.1804 7.6.1810"
    versions+=" 7.7.1908 7.8.2003"
    for j in $versions ;do
        if [ "$i" == "power9" ] && [[ "$j" > "7.4.1708" ]];then
            basearch=$i
        else
            basearch='$basearch'
        fi
       cat >>$filename <<__EOF__

# C$j
[C$j-base]
name=CentOS-$j - Base
baseurl=http://vault.centos.org/$baseurl$j/os/$basearch/
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7$altkey
enabled=0

[C$j-updates]
name=CentOS-$j - Updates
baseurl=http://vault.centos.org/$baseurl$j/updates/$basearch/
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7$altkey
enabled=0

[C$j-extras]
name=CentOS-$j - Extras
baseurl=http://vault.centos.org/$baseurl$j/extras/$basearch/
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7$altkey
enabled=0

[C$j-centosplus]
name=CentOS-$j - CentOSPlus
baseurl=http://vault.centos.org/$baseurl$j/centosplus/$basearch/
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7$altkey
enabled=0

[C$j-fasttrack]
name=CentOS-$j - Fasttrack
baseurl=http://vault.centos.org/$baseurl$j/fasttrack/$basearch/
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7$altkey
enabled=0
__EOF__
    done
done
