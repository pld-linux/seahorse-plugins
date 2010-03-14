Summary:	Plugins and utilities for encryption in GNOME
Name:		seahorse-plugins
Version:	2.28.1
Release:	1
License:	GPL v2
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/seahorse-plugins/2.28/%{name}-%{version}.tar.bz2
# Source0-md5:	cec5ef8b94c16798f53a5876d3718b91
URL:		http://www.gnome.org/projects/seahorse/
BuildRequires:	GConf2-devel >= 2.24.0
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.71
BuildRequires:	evolution-data-server-devel >= 2.26.0
BuildRequires:	gedit2-devel >= 2.24.0
BuildRequires:	gettext-devel
BuildRequires:	gnome-doc-utils >= 0.14.0
BuildRequires:	gnome-keyring-devel >= 2.26.0
BuildRequires:	gnome-panel-devel >= 2.26.0
BuildRequires:	gnupg >= 1.4.5
BuildRequires:	gpgme-devel >= 1:1.1.2
BuildRequires:	gtk+2-devel >= 2:2.14.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libcryptui-devel >= 2.28.0
BuildRequires:	libglade2-devel >= 1:2.6.2
BuildRequires:	libnotify-devel >= 0.4.2
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.6.31
BuildRequires:	nautilus-devel >= 2.26.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
Requires(post,postun):	desktop-file-utils
Requires(post,preun):	GConf2
Requires:	seahorse >= 2.28.0
Obsoletes:	epiphany-extension-seahorse
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The plugins and utilities in this package integrate seahorse into the
GNOME desktop environment and allow users to perform operations from
applications like nautilus or gedit.

%package -n gedit-plugin-seahorse
Summary:	Seahorse plugin for Gedit
Summary(pl.UTF-8):	Wtyczka Seahorse dla Gedit
Group:		X11/Applications
Requires(post,preun):	GConf2
Requires:	%{name} = %{version}-%{release}
Requires:	gedit2 >= 2.26.0

%description -n gedit-plugin-seahorse
This plugin performs encryption operations on text.

%description -n gedit-plugin-seahorse -l pl.UTF-8
Wtyczka wykonująca operacje szyfrujące na tekście.

%package -n nautilus-extension-seahorse
Summary:	Seahorse extension for Nautilus
Summary(pl.UTF-8):	Rozszerzenie Seahorse dla Nautilusa
Group:		X11/Applications
Requires(post,postun):	shared-mime-info
Requires:	%{name} = %{version}-%{release}
Requires:	nautilus >= 2.26.0

%description -n nautilus-extension-seahorse
Extension for signing and encrypting files.

%description -n nautilus-extension-seahorse -l pl.UTF-8
Rozszerzenie do podpisywania i szyfrowania plików.

%package -n gnome-applet-seahorse
Summary:	Seahorse applet
Summary(pl.UTF-8):	Aplet Seahorse
Group:		X11/Applications
Requires(post,postun):	gtk+2
Requires:	%{name} = %{version}-%{release}
Requires:	gnome-panel >= 2.26.0

%description -n gnome-applet-seahorse
Applet for signing and encrypting files.

%description -n gnome-applet-seahorse -l pl.UTF-8
Aplet Seahorse.

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
	--disable-update-mime-database \
	--disable-schemas-install \
	--disable-epiphany
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/epiphany/2.*/extensions/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/gedit-2/plugins/*.{a,la}
rm -f $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-2.0/*.{a,la}

%find_lang seahorse-applet --with-gnome --with-omf
%find_lang %{name} --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install seahorse-plugins.schemas
%update_desktop_database

%preun
%gconf_schema_uninstall seahorse-plugins.schemas

%postun
%update_desktop_database_postun

%post -n gedit-plugin-seahorse
%gconf_schema_install seahorse-gedit.schemas

%preun -n gedit-plugin-seahorse
%gconf_schema_uninstall seahorse-gedit.schemas

%post -n nautilus-extension-seahorse
%update_mime_database

%postun -n nautilus-extension-seahorse
%update_mime_database

%post -n gnome-applet-seahorse
%update_icon_cache hicolor

%postun -n gnome-applet-seahorse
%update_icon_cache hicolor

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README THANKS
%attr(755,root,root) %{_bindir}/seahorse-agent
%attr(755,root,root) %{_bindir}/seahorse-preferences
%attr(755,root,root) %{_bindir}/seahorse-tool
%{_sysconfdir}/gconf/schemas/seahorse-plugins.schemas
%{_desktopdir}/seahorse-pgp-encrypted.desktop
%{_desktopdir}/seahorse-pgp-keys.desktop
%{_desktopdir}/seahorse-pgp-preferences.desktop
%{_desktopdir}/seahorse-pgp-signature.desktop
%{_datadir}/seahorse-plugins
%{_pixmapsdir}/seahorse-plugins
%exclude %{_pixmapsdir}/seahorse-plugins/*/seahorse-applet*
%{_mandir}/man1/seahorse-agent.1*
%{_mandir}/man1/seahorse-tool.1*

%files -n gedit-plugin-seahorse
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gedit-2/plugins/libseahorse-pgp.so
%{_libdir}/gedit-2/plugins/seahorse-pgp.gedit-plugin
%{_sysconfdir}/gconf/schemas/seahorse-gedit.schemas

%files -n nautilus-extension-seahorse
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/nautilus/extensions-2.0/libnautilus-seahorse.so
%{_datadir}/mime/packages/seahorse.xml

%files -n gnome-applet-seahorse -f seahorse-applet.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/seahorse/seahorse-applet
%{_libdir}/bonobo/servers/GNOME_SeahorseApplet.server
%{_datadir}/gnome-2.0/ui/GNOME_SeahorseApplet.xml
%{_datadir}/seahorse-plugins/glade/seahorse-applet-preferences.glade
%{_iconsdir}/hicolor/*/*/seahorse-applet*
%{_pixmapsdir}/seahorse-plugins/*/seahorse-applet*
%{_pixmapsdir}/seahorse-applet.svg
