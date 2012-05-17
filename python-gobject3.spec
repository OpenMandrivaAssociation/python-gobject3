%define oname pygobject

%define api 2.0
%define major 0
%define libname %mklibname pyglib-gi %{api} %major

%define _exclude_files_from_autoreq ^%{py_platsitedir}/gi/_gobject/__init__.py 

Summary:	Python bindings for GObject Introspection
Name:		python-gobject3
Version:	3.2.2
Release:	1
License:	LGPLv2+ and MIT
Group:		Development/Python
Url:		http://www.gnome.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{oname}/%{oname}-%{version}.tar.xz
Patch0:		pygobject-2.90.2-link.patch

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

find %{buildroot} -name *.la | xargs rm

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

