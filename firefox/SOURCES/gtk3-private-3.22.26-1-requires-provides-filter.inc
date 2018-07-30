%filter_provides_in %{gtk3_install_path}/%{_lib}
%filter_requires_in %{gtk3_install_path}/%{_lib}

%filter_from_requires /libgdk-3.*/d
%filter_from_requires /libatk-1.0.so.*/d
%filter_from_requires /libatk-bridge-2.0.so.*/d
%filter_from_requires /libatspi.so.*/d
%filter_from_requires /libcairo.so.*/d
%filter_from_requires /libcairo-gobject.so.*/d
%filter_from_requires /libfontconfig.so.*/d
%filter_from_requires /libfreetype.so.*/d
%filter_from_requires /libgdk-3.so.*/d
%filter_from_requires /libgdk_pixbuf-2.0.so.*/d
%filter_from_requires /libgio-2.0.so.*/d
%filter_from_requires /libglib-2.0.so.*/d
%filter_from_requires /libgmodule-2.0.so.*/d
%filter_from_requires /libgobject-2.0.so.*/d
%filter_from_requires /libgthread-2.0.so.*/d
%filter_from_requires /libgtk-3.so.*/d
%filter_from_requires /libharfbuzz.so.*/d
%filter_from_requires /libpango-1.0.so.*/d
%filter_from_requires /libpangocairo-1.0.so.*/d
%filter_from_requires /libpangoft2-1.0.so.*/d
%filter_from_requires /libpcre.so.*/d

# Don't forget to call %%filter_setup from the consumer!
