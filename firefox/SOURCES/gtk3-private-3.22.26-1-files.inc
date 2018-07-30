%dir %{gtk3_install_path}/bin
%{gtk3_install_path}/bin/gdk-pixbuf-query-loaders-%{__isa_bits}
%{gtk3_install_path}/bin/gdk-pixbuf-thumbnailer
%{gtk3_install_path}/bin/gio-querymodules-%{__isa_bits}
%{gtk3_install_path}/bin/glib-compile-schemas
%{gtk3_install_path}/bin/gtk-query-immodules-3.0-%{__isa_bits}
%{gtk3_install_path}/bin/gtk-update-icon-cache
%{gtk3_install_path}/bin/fc-cache

%{gtk3_install_path}/etc

%dir %{gtk3_install_path}/%{_lib}
%{gtk3_install_path}/%{_lib}/libatk-1.0.so.*
%{gtk3_install_path}/%{_lib}/libatk-bridge-2.0.so.*
%{gtk3_install_path}/%{_lib}/libatspi.so.*
%{gtk3_install_path}/%{_lib}/libcairo.so.*
%{gtk3_install_path}/%{_lib}/libcairo-gobject.so.*
%{gtk3_install_path}/%{_lib}/libfontconfig.so.*
%{gtk3_install_path}/%{_lib}/libfreetype.so.*
%{gtk3_install_path}/%{_lib}/libgdk-3.so.*
%{gtk3_install_path}/%{_lib}/libgdk_pixbuf-2.0.so.*
%{gtk3_install_path}/%{_lib}/libgio-2.0.so.*
%{gtk3_install_path}/%{_lib}/libglib-2.0.so.*
%{gtk3_install_path}/%{_lib}/libgmodule-2.0.so.*
%{gtk3_install_path}/%{_lib}/libgobject-2.0.so.*
%{gtk3_install_path}/%{_lib}/libgthread-2.0.so.*
%{gtk3_install_path}/%{_lib}/libgtk-3.so.*
%{gtk3_install_path}/%{_lib}/libharfbuzz.so.*
%{gtk3_install_path}/%{_lib}/libpango-1.0.so.*
%{gtk3_install_path}/%{_lib}/libpangocairo-1.0.so.*
%{gtk3_install_path}/%{_lib}/libpangoft2-1.0.so.*
%{gtk3_install_path}/%{_lib}/libpcre.so.*
%{gtk3_install_path}/%{_lib}/librsvg-2.so.*
%dir %{gtk3_install_path}/%{_lib}/cairo
%{gtk3_install_path}/%{_lib}/cairo/cairo-fdr.so.*
%{gtk3_install_path}/%{_lib}/cairo/cairo-sphinx.so.*
%{gtk3_install_path}/%{_lib}/cairo/libcairo-trace.so.*
%{gtk3_install_path}/%{_lib}/gdk-pixbuf-2.0
%ghost %attr(644, root, root) %{gtk3_install_path}/%{_lib}/gdk-pixbuf-2.0/2.10.0/loaders.cache
%{gtk3_install_path}/%{_lib}/gio
%ghost %attr(644, root, root) %{gtk3_install_path}/%{_lib}/gio/modules/giomodule.cache
%{gtk3_install_path}/%{_lib}/gtk-3.0

%{gtk3_install_path}/libexec

%{gtk3_install_path}/share
%ghost %attr(644, root, root) %{gtk3_install_path}/share/icons/Adwaita/icon-theme.cache
%ghost %attr(644, root, root) %{gtk3_install_path}/share/icons/hicolor/icon-theme.cache
%ghost %attr(644, root, root) %{gtk3_install_path}/share/glib-2.0/schemas/gschemas.compiled

%{gtk3_install_path}/var
%dir %{gtk3_install_path}/var/cache/fontconfig

