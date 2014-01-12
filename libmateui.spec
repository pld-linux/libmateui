# NOTE: this package is deprecated, meant for MATE <= 1.4 compatibility only
#
# Conditional build:
%bcond_with	gtk3		# use GTK+ 3.x instead of 2.x
%bcond_with	static_libs	# static library
#
Summary:	MATE base GUI library
Summary(pl.UTF-8):	Podstawowa biblioteka GUI MATE
Name:		libmateui
Version:	1.4.0
Release:	1
License:	LGPL v2+
Group:		X11/Libraries
Source0:	http://pub.mate-desktop.org/releases/1.4/%{name}-%{version}.tar.xz
# Source0-md5:	c48f2213a0511c60c8811af503c60337
URL:		http://mate-desktop.org
BuildRequires:	autoconf >= 2.54
BuildRequires:	automake >= 1:1.9
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gdk-pixbuf2-devel >= 2.12.0
BuildRequires:	gettext-devel >= 0.10.40
BuildRequires:	glib2-devel >= 1:2.16.0
%{!?with_gtk3:BuildRequires:	gtk+2-devel >= 2:2.12.0}
%{?with_gtk3:BuildRequires:	gtk+3-devel >= 3.0.0}
BuildRequires:	gtk-doc >= 1.0
BuildRequires:	intltool >= 0.40.0
BuildRequires:	libglade2-devel >= 2.0.0
BuildRequires:	libmate-devel >= 1.1.0
BuildRequires:	libmatecanvas-devel >= 1.1.0
BuildRequires:	libmatecomponentui-devel >= 1.1.0
BuildRequires:	libmatekeyring-devel >= 1.1.0
BuildRequires:	libtool >= 1:1.4.3
BuildRequires:	libxml2-devel >= 1:2.4.20
BuildRequires:	mate-common
BuildRequires:	mate-conf-devel >= 1.1.0
BuildRequires:	mate-vfs-devel >= 1.1.0
BuildRequires:	pango-devel >= 1:1.1.2
BuildRequires:	perl-base
BuildRequires:	pkgconfig
BuildRequires:	popt-devel >= 1.5
BuildRequires:	rpmbuild(macros) >= 1.197
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
Requires:	gdk-pixbuf2 >= 2.12.0
Requires:	glib2 >= 1:2.16.0
%{!?with_gtk3:Requires:	gtk+2 >= 2:2.12.0}
%{?with_gtk3:Requires:	gtk+3 >= 3.0.0}
Requires:	libmate-libs >= 1.1.0
Requires:	libmatecomponentui >= 1.1.0
Requires:	libmatekeyring >= 1.1.0
Requires:	mate-conf-libs >= 1.1.0
Requires:	mate-vfs-libs >= 1.1.0
Requires:	popt >= 1.5
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libmateui is the GUI part of base MATE libraries. It's a fork of
libgnomeui.

%description -l pl.UTF-8
libmateui to związana z graficznym interfejsem użytkownika (GUI) część
podstawowych bibliotek MATE. Jest to odgałęzienie libgnomeui.

%package devel
Summary:	Header files for libmateui
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libmateui
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	gdk-pixbuf2-devel >= 2.12.0
Requires:	glib2-devel >= 1:2.16.0
%{!?with_gtk3:Requires:	gtk+2-devel >= 2:2.12.0}
%{?with_gtk3:Requires:	gtk+3-devel >= 3.0.0}
Requires:	libglade2-devel >= 2.0.0
Requires:	libmate-devel >= 1.1.0
Requires:	libmatecanvas-devel >= 1.1.0
Requires:	libmatecomponentui-devel >= 1.1.0
Requires:	libmatekeyring-devel >= 1.1.0
Requires:	mate-conf-devel >= 1.1.0
Requires:	mate-vfs-devel >= 1.1.0
Requires:	popt-devel >= 1.5
Requires:	xorg-lib-libICE-devel
Requires:	xorg-lib-libSM-devel

%description devel
This package includes the header files that you will need for
libmateui applications development.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe potrzebne do kompilacji programów
używających biblioteki libmateui.

%package static
Summary:	Static libmateui library
Summary(pl.UTF-8):	Statyczna biblioteka libmateui
Group:		X11/Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static version of libmateui library.

%description static -l pl.UTF-8
Statyczna wersja biblioteki libmateui.

%package apidocs
Summary:	libmateui API documentation
Summary(pl.UTF-8):	Dokumentacja API libmateui
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
libmateui API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API libmateui.

%prep
%setup -q

%build
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	MATECONFTOOL=/usr/bin/mateconftool-2 \
	--enable-gtk-doc \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	%{?with_gtk3:--with-gtk=3.0} \
	--with-html-dir=%{_gtkdocdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# no static modules and *.la for libglade
# libraries .la obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la \
	$RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.la
%if %{with static_libs}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.a
%endif

%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{sr@ije,sr@ijekavian}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_libdir}/libmateui-2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libmateui-2.so.0
%attr(755,root,root) %{_libdir}/libglade/2.0/libmate.so
%{_pixmapsdir}/mate-about-logo.png

%files devel
%defattr(644,root,root,755)
%{_includedir}/libmateui-2.0
%attr(755,root,root) %{_libdir}/libmateui-2.so
%{_pkgconfigdir}/libmateui-2.0.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libmateui-2.a
%endif

%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/libmateui
