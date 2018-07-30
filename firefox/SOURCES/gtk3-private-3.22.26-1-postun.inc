# adwaita
if [ $1 -eq 0 ] ; then
    touch --no-create %{gtk3_install_path}/share/icons/Adwaita &>/dev/null
    touch --no-create %{gtk3_install_path}/share/icons/hicolor &>/dev/null
    %{gtk3_install_path}/bin/gtk-update-icon-cache %{gtk3_install_path}/share/icons/Adwaita &>/dev/null || :
    %{gtk3_install_path}/bin/gtk-update-icon-cache %{gtk3_install_path}/share/icons/hicolor &>/dev/null || :
fi

# gdk-pixbuf2
if [ $1 -gt 0 ]; then
  %{gtk3_install_path}/bin/gdk-pixbuf-query-loaders-%{__isa_bits} --update-cache || :
fi

# glib2
[ ! -x %{gtk3_install_path}/bin/gio-querymodules-%{__isa_bits} ] || \
%{gtk3_install_path}/bin/gio-querymodules-%{__isa_bits} %{gtk3_install_path}/%{_lib}/gio/modules

# gtk3
if [ $1 -gt 0 ]; then
  %{gtk3_install_path}/bin/gtk-query-immodules-3.0-%{__isa_bits} --update-cache
fi

if [ $1 -eq 0 ] ; then
    rm -rf %{gtk3_install_path}/var/cache/fontconfig/* &>/dev/null || :
fi

%{gtk3_install_path}/bin/glib-compile-schemas %{gtk3_install_path}/share/glib-2.0/schemas &> /dev/null || :
