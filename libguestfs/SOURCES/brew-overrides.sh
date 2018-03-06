#!/bin/bash -

# This script is used when we build libguestfs from brew, as sometimes
# we require packages which are not available in the current version
# of RHEL.  Normally these updated packages would be released along
# with libguestfs in the next RHEL, although unfortunately sometimes
# that doesn't happen (eg. RHBZ#1199605).

set -x

# The kernel package doesn't install unless xfsprogs >= 4.3.0
# is installed.
xfsprogs="$(brew -q latest-pkg rhel-7.4-candidate xfsprogs |
            awk '{print $1}')"

# linux-firmware is for virt-p2v, see RHBZ#1364419
linux_firmware="$(brew -q latest-pkg rhel-7.4-candidate linux-firmware |
                  awk '{print $1}')"

pkgs="
  hivex-1.3.10-5.8.el7
  libvirt-3.1.0-2.el7
  libselinux-2.5-9.el7
  $linux_firmware
  ocaml-findlib-1.3.3-7.el7
  policycoreutils-2.5-12.el7
  rdma-core-13-1.el7
  $xfsprogs
"

for pkg in $pkgs ; do
    brew tag-pkg rhel-7.4-temp-override $pkg
done

for pkg in $pkgs ; do
    brew wait-repo rhel-7.4-build --build=$pkg
done
