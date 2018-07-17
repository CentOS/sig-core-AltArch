# sig-core-AltArch
Repository that will contain specific needed patches to build upstream packages on specific cpu arch (mostly armhfp/armv7hl, as such arch doesn't exist "upstream")

Worth knowing that each package here has only the .spec and .patch from existing pkg, and for which you can open a PR if you want to provide a patch.
The real source (aka Source0 , or other binary blobs) should come from either :
 * git.centos.org (for most of the pkgs here, so use [get_sources.sh](https://wiki.centos.org/Sources) to download the needed Sources)
 * $upstream project (like kernel.org for vanilla/upstream kernel)


This repository also hosts the kickstarts used to build the armhfp images. Those are located under image_build directory

