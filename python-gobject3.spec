%define oname pygobject

%define api 2.0
%define major 0
%define libname %mklibname pyglib-gi %{api} %{major}

%if %{_use_internal_dependency_generator}
%define __noautoprovfiles %{py_platsitedir}/gi/_gobject/__init__.py
%else
%define _exclude_files_from_autoreq ^%{py_platsitedir}/gi/_gobject/__init__.py
%endif

Summary:	Python bindings for GObject Introspection
Name:		python-gobject3
Version:	3.4.0
Release:	2
License:	LGPLv2+ and MIT
Group:		Development/Python
Url:		http://www.gnome.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{oname}/3.4/%{oname}-%{version}.tar.xz

BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(glib-2.0) >= 2.24.0
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.10.2
BuildRequires:	pkgconfig(libffi) >= 3.0
BuildRequires:	pkgconfig(pycairo) >= 1.2.0
BuildRequires:	pkgconfig(python) >= 2.5.2

%description
The %{name} package provides a convenient wrapper for the GObject 
library for use in Python programs.

%package -n python-gi
Summary:	Python bindings for GObject Introspection
Group:		Development/Python
Provides:	python-gobject-introspection = %{version}-%{release}
Provides:	%{name} = %{version}-%{release}
Conflicts:	python-gobject < 2.28.6-3

%description -n python-gi
This package contains the Python GObject Introspection bindings.

%package -n python-gi-cairo
Summary:	Python-gi bindings for Cairo
Group:		Development/Python
Requires:	python-gi = %{version}-%{release}
Requires:	typelib(PangoCairo)
Requires:	python-cairo >= 1.2.0
Obsoletes:	python-gobject-cairo < 2.28.6-3
Provides:	python-gobject-cairo = %{version}-%{release}

%description -n python-gi-cairo
This package contains the Python-gi Cairo bindings.

%package -n %{libname}
Group:		System/Libraries
Summary:	Python GObject Introspection bindings shared library

%description -n %{libname}
This archive contains bindings for the GObject, to be used in Python
It is a fairly complete set of bindings, it's already rather useful, 
and is usable to write moderately complex programs.

%package devel
Group:		Development/C
Summary:	Python-gobject development files
Requires:	%{libname} = %{version}-%{release}

%description devel
This contains the python-gobject development files, including C
header, pkg-config file.

%prep
%setup -qn %{oname}-%{version}

%build
%configure2_5x
%make LIBS="-lpython%{py_ver}"

%install
%makeinstall_std

# dsextra stuff is for windows installs so remove it
rm -fr %{buildroot}%{python_sitearch}/gtk-2.0

# docs are out of date and are being reworked upstream
# so remove them
rm -rf %{buildroot}%{_datadir}/gtk-doc
rm -rf %{buildroot}%{_datadir}/pygobject

%files -n python-gi
%doc README NEWS AUTHORS ChangeLog
%{py_platsitedir}/gi
%exclude %{py_platsitedir}/gi/_gi_cairo.so

%files -n python-gi-cairo
%{py_platsitedir}/gi/_gi_cairo.so

%files -n %{libname}
%{_libdir}/libpyglib-gi-%{api}-python.so.%{major}*

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Oct  2 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.4.0-1
- 3.4.0

* Thu May 17 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.2.2-1
+ Revision: 799303
- update to new version 3.2.2

* Sun May 13 2012 Alexander Khrukin <akhrukin@mandriva.org> 3.2.1-1
+ Revision: 798544
- version update 3.2.1

* Sun Apr 29 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.2.0-1
+ Revision: 794486
- new version 3.2.0

* Sat Mar 17 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.0.4-1
+ Revision: 785442
- new version 3.0.4
- corrected Conflicts for older pythob-gobject

* Mon Nov 21 2011 Matthew Dawkins <mattydaw@mandriva.org> 3.0.2-1
+ Revision: 732233
- imported package python-gobject3

