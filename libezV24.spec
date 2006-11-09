Summary:	An easy to use programming interface for Linux serial ports
Summary(pl):	Prosty w u¿yciu interfejs programowy do linuksowych portów szeregowych
Name:		libezV24
Version:	0.1.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/ezv24/%{name}-%{version}.tar.gz
# Source0-md5:	59a682a6ba5cce142760f7309dea44f9
URL:		http://libezV24.sourceforge.net/
BuildRequires:	sed >= 4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An easy to use programming interface for Linux serial ports.

%description -l pl
Prosty w u¿yciu interfejs programowy do linuksowych portów
szeregowych.

%package devel
Summary:	Header files for libezV24 library
Summary(pl):	Pliki nag³ówkowe biblioteki libezV24
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains include files and other resources you can use to
incorporate %{name} into applications.

%description devel -l pl
Ten pakiet zawiera pliki nag³ówkowe i inne zasoby przydatne przy
u¿ywaniu libezV24 w aplikacjach.

%package static
Summary:	Static libezV24 library
Summary(pl):	Statyczna biblioteka libezV24
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static libezV24 library.

%description static -l pl
Ten pakiet zawiera statyczn± bibliotekê libezV24.

%prep
%setup -q

%build
sed -i -e 's#ldconfig##g' Makefile*
sed -i -e 's#-W1,soname#-Wl,-soname#g' Makefile*
sed -i -e 's#gcc#%{__cc}#g' Makefile*
sed -i -e 's#LIBNAME = .*#LIBNAME = lib$(SOBASE).a#g' Makefile*
%{__make} shared static \
	C_FLAG="-c %{rpmcflags} -Wall -fPIC -D\$(PLATFORM) \$(INCDIR)" \
	LFLAGS="%{rpmldflags} \$(LIBDIR)"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}/ezV24}

%{__make} install \
	PREFIX=$RPM_BUILD_ROOT%{_prefix}

LINKS=$(cd $RPM_BUILD_ROOT%{_libdir}; ls -1 lib*.so)
LINKD=$(cd $RPM_BUILD_ROOT%{_libdir}; ls -1 lib*.so.*.*)
ln -sf $LINKD $RPM_BUILD_ROOT%{_libdir}/$LINKS

%clean
rm -rf $RPM_BUILD_ROOT

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS ChangeLog HISTORY
%attr(755,root,root) %{_libdir}/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%doc api-html/*
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/ezV24

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
