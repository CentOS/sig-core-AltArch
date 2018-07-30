%if "%{name}" == "gtk3-private"
    function prepend_buildroot_include_path_to_compiler_flags() {
        export CFLAGS="-I%{_buildrootdir}%{gtk3_install_path}/$@ $CFLAGS" \
        export CXXFLAGS="-I%{_buildrootdir}%{gtk3_install_path}/$@ $CXXFLAGS"
    }
    
    prepend_buildroot_include_path_to_compiler_flags include
    prepend_buildroot_include_path_to_compiler_flags include/glib-2.0
    prepend_buildroot_include_path_to_compiler_flags include/glib-2.0
    prepend_buildroot_include_path_to_compiler_flags include/gio-unix-2.0
    prepend_buildroot_include_path_to_compiler_flags %{_lib}/glib-2.0/include
    prepend_buildroot_include_path_to_compiler_flags include/freetype2
    prepend_buildroot_include_path_to_compiler_flags include/fontconfig
    prepend_buildroot_include_path_to_compiler_flags include/harfbuzz
    prepend_buildroot_include_path_to_compiler_flags include/gdk-pixbuf-2.0
    prepend_buildroot_include_path_to_compiler_flags include/atk-1.0
    prepend_buildroot_include_path_to_compiler_flags include/at-spi-2.0
    prepend_buildroot_include_path_to_compiler_flags include/at-spi2-atk/2.0
    prepend_buildroot_include_path_to_compiler_flags include/cairo
    prepend_buildroot_include_path_to_compiler_flags include/pango-1.0
    prepend_buildroot_include_path_to_compiler_flags include/librsvg-2.0
    prepend_buildroot_include_path_to_compiler_flags include/cairo
    prepend_buildroot_include_path_to_compiler_flags include/gtk-3.0
    prepend_buildroot_include_path_to_compiler_flags include/gtk-3.0/unix-print
    prepend_buildroot_include_path_to_compiler_flags include/librsvg-2.0
%else
    sed -i 's@%{gtk3_install_path}@%{_buildrootdir}%{gtk3_install_path}@g' %{_buildrootdir}%{gtk3_install_path}/%{_lib}/pkgconfig/*.pc
%endif

export LDFLAGS="-L%{_buildrootdir}%{gtk3_install_path}/%{_lib} $LDFLAGS"
export LDFLAGS="-Wl,-rpath,%{gtk3_install_path}/%{_lib} $LDFLAGS"
export LDFLAGS="-Wl,-rpath-link,%{_buildrootdir}%{gtk3_install_path}/%{_lib} $LDFLAGS"

export PKG_CONFIG_PATH=%{_buildrootdir}%{gtk3_install_path}/%{_lib}/pkgconfig
