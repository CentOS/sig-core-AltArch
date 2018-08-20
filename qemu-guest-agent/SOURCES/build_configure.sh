#!/bin/sh

_prefix=$1
shift
_libdir=$1
shift
_sysconfdir=$1
shift
_localstatedir=$1
shift
_libexecdir=$1
shift
pkgname=$1
shift
arch=$1
shift
nvr=$1
shift
optflags=$1
shift
have_fdt=$1
shift
have_tcmalloc=$1
shift

./configure \
    --prefix=${_prefix} \
    --libdir=${_libdir} \
    --sysconfdir=${_sysconfdir} \
    --interp-prefix=${_prefix}/qemu-%M \
    --localstatedir=${_localstatedir} \
    --libexecdir=${_libexecdir} \
    --extra-ldflags="$extraldflags -pie -Wl,-z,relro -Wl,-z,now" \
    --extra-cflags="${optflags} -fPIE -DPIE" \
    --with-pkgversion=${nvr} \
    --with-confsuffix=/${pkgname} \
    --with-coroutine=ucontext \
    --disable-archipelago \
    --disable-bluez \
    --disable-brlapi \
    --disable-cap-ng \
    --enable-coroutine-pool \
    --disable-curl \
    --disable-curses \
    --disable-debug-tcg \
    --enable-docs \
    --disable-gtk \
    --enable-kvm \
    --disable-libiscsi \
    --disable-libnfs \
    --disable-libssh2 \
    --disable-libusb \
    --disable-bzip2 \
    --disable-linux-aio \
    --disable-lzo \
    --disable-opengl \
    --enable-pie \
    --disable-qom-cast-debug \
    --disable-sdl \
    --disable-smartcard \
    --disable-snappy \
    --disable-sparse \
    --disable-strip \
    --disable-tpm \
    --enable-trace-backend=dtrace \
    --disable-vde \
    --disable-vhdx \
    --disable-vhost-scsi \
    --disable-virtfs \
    --disable-vnc-jpeg \
    --disable-vte \
    --disable-vnc-png \
    --disable-vnc-sasl \
    --enable-werror \
    --disable-xen \
    --disable-xfsctl \
    --${have_fdt}-fdt \
    --disable-glusterfs \
    --enable-guest-agent \
    --disable-numa \
    --disable-rbd \
    --disable-rdma \
    --disable-seccomp \
    --disable-spice \
    --disable-usb-redir \
    --${have_tcmalloc}-tcmalloc \
    --disable-system \
    --disable-tools \
    "$@"
