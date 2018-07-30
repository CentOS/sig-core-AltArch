# adwaita-icon-theme
touch --no-create %{gtk3_install_path}/share/icons/Adwaita &>/dev/null || :
touch --no-create %{gtk3_install_path}/share/icons/hicolor &>/dev/null || :
%{gtk3_install_path}/bin/gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :

# glib2
%{gtk3_install_path}/bin/gio-querymodules-%{__isa_bits} %{gtk3_install_path}/%{_lib}/gio/modules

# gtk3
%{gtk3_install_path}/bin/gtk-query-immodules-3.0-%{__isa_bits} --update-cache
%{gtk3_install_path}/bin/glib-compile-schemas %{gtk3_install_path}/share/glib-2.0/schemas &> /dev/null || :

# fontconfig
umask 0022

# Force regeneration of all fontconfig cache files
# The check for existance is needed on dual-arch installs (the second
#  copy of fontconfig might install the binary instead of the first)
# The HOME setting is to avoid problems if HOME hasn't been reset
# FIXME hardcoded version !
if [ -x %{gtk3_install_path}/bin/fc-cache ] && %{gtk3_install_path}/bin/fc-cache --version 2>&1 | grep -q 2.10.95 ; then
  HOME=/root %{gtk3_install_path}/bin/fc-cache -f
fi
