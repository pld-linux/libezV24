Summary:	an easy to use programming interface for Linux serial ports
Name:		libezV24
Version:	0.1.1
Release:	1
License:	LGPL
Group:		Libraries
Source0:	http://dl.sourceforge.net/ezv24/%{name}-%{version}.tar.gz
# Source0-md5:	59a682a6ba5cce142760f7309dea44f9
URL:		http://libezV24.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
An easy to use programming interface for Linux serial ports.

%package devel
Summary:	%{name} library headers
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
This package contains include files and other resources you can use to
incorporate %{name} into applications.

%package static
Summary:	libezV24 static libraries
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}

%description static
This is package with static libezV24 libraries.

%prep
%setup -q

%build
sed -i -e 's#ldconfig##g' Makefile*
sed -i -e 's#-W1,soname#-Wl,-soname#g' Makefile*
sed -i -e 's#gcc#%{__cc}#g' Makefile*
sed -i -e 's#LIBNAME = .*#LIBNAME = lib$(SOBASE).a#g' Makefile*
%{__make} shared static

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
