Summary:	System daemon for managing color devices
Name:		colord
Version:	0.1.24
Release:	6
License:	GPL v2+ and LGPL v2+
Group:		Daemons
Source0:	http://www.freedesktop.org/software/colord/releases/%{name}-%{version}.tar.xz
# Source0-md5:	1e7c4164c35b8415af108fb2a0db7e1f
URL:		http://www.freedesktop.org/software/colord/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-devel
BuildRequires:	gettext-devel
BuildRequires:	glib-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	lcms2-devel
BuildRequires:	libgusb-devel
BuildRequires:	libtool
BuildRequires:	pkg-config
BuildRequires:	polkit-devel
BuildRequires:	sane-backends-devel
BuildRequires:	sqlite3-devel
BuildRequires:	udev-glib-devel
BuildRequires:	vala-vapigen
Requires(pre,postun):	pwdutils
Provides:	group(colord)
Provides:	user(colord)
Requires:	%{name}-libs = %{version}-%{release}
Suggests:	shared-color-profiles
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/colord

%description
colord is a low level system activated daemon that maps color devices
to color profiles in the system context.

%package libs
Summary:	colord library
Group:		Libraries

%description libs
colord library.

%package devel
Summary:	Header files for colord library
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for colord library.

%package apidocs
Summary:	colord API documentation
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
colord API documentation.

%prep
%setup -q

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules		\
	--disable-static		\
	--enable-vala			\
	--with-daemon-user=colord	\
	--with-html-dir=%{_gtkdocdir} 	\
	--with-systemdsystemunitdir=%{systemdunitdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/colord-*/*.la
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/locale/it_IT

%find_lang %{name}

:> $RPM_BUILD_ROOT/var/lib/colord/mapping.db
:> $RPM_BUILD_ROOT/var/lib/colord/storage.db

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 108 -r -f colord
%useradd -u 108 -r -d /usr/share/empty -s /bin/false -c "colord daemon" -g colord colord

%postun
if [ "$1" = "0" ]; then
    %userremove colord
    %groupremove colord
fi

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/cd-create-profile
%attr(755,root,root) %{_bindir}/cd-fix-profile
%attr(755,root,root) %{_bindir}/colormgr
%dir %{_libexecdir}
%attr(755,root,root) %{_libexecdir}/colord

%dir %{_libdir}/colord-sensors
%attr(755,root,root) %{_libdir}/colord-sensors/libcolord_sensor_colorhug.so
%attr(755,root,root) %{_libdir}/colord-sensors/libcolord_sensor_dummy.so
%attr(755,root,root) %{_libdir}/colord-sensors/libcolord_sensor_huey.so

%dir %{_libdir}/colord-plugins
%attr(755,root,root) %{_libdir}/colord-plugins/libcd_plugin_camera.so
%attr(755,root,root) %{_libdir}/colord-plugins/libcd_plugin_scanner.so

%dir %{_datadir}/color/icc/colord
%{_datadir}/color/icc/colord/*.icc

%{_datadir}/dbus-1/system-services/org.freedesktop.ColorManager.service
%{_datadir}/polkit-1/actions/org.freedesktop.color.policy
%{systemdunitdir}/colord.service
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/colord.conf
/etc/dbus-1/system.d/org.freedesktop.ColorManager.conf
%{_prefix}/lib/udev/rules.d/69-cd-sensors.rules
%{_prefix}/lib/udev/rules.d/95-cd-devices.rules

%attr(755,colord,colord) %dir /var/lib/colord
%attr(755,colord,colord) %dir /var/lib/colord/icc
%ghost /var/lib/colord/mapping.db
%ghost /var/lib/colord/storage.db

%{_datadir}/dbus-1/interfaces/org.freedesktop.ColorManager.Device.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.ColorManager.Profile.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.ColorManager.Sensor.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.ColorManager.xml

%if 0
%{_mandir}/man1/cd-create-profile.1*
%{_mandir}/man1/cd-fix-profile.1*
%{_mandir}/man1/colormgr.1*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libcolord*.so.?
%attr(755,root,root) %{_libdir}/libcolord*.so.*.*.*
%{_libdir}/girepository-1.0/*.typelib

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcolord*.so
%{_includedir}/colord-1
%{_pkgconfigdir}/colord*.pc
%{_datadir}/gir-1.0/*.gir
%{_datadir}/vala/vapi/colord.vapi

%if 0
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/colord
%endif

