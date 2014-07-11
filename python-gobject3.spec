%define url_ver %(echo %{version}|cut -d. -f1,2)

%define oname pygobject

%if %{_use_internal_dependency_generator}
%define __noautoprovfiles %{py_platsitedir}/gi/_gobject/__init__.py
%else
%define _exclude_files_from_autoreq ^%{py_platsitedir}/gi/_gobject/__init__.py
%endif

Summary:	Python bindings for GObject Introspection
Name:		python-gobject3
Version:	3.12.2
Release:	2
License:	LGPLv2+ and MIT
Group:		Development/Python
Url:		http://www.gnome.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{oname}/%{url_ver}/%{oname}-%{version}.tar.xz
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(glib-2.0) >= 2.24.0
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.10.2
BuildRequires:	pkgconfig(libffi) >= 3.0
BuildRequires:	pkgconfig(python3)
BuildRequires:	pkgconfig(py3cairo)
BuildRequires:	gnome-common

%description
The %{name} package provides a convenient wrapper for the GObject 
library for use in Python programs.

%package -n python-gi
Summary:	Python bindings for GObject Introspection
Group:		Development/Python
Provides:	python-gobject-introspection = %{version}-%{release}
Provides:	%{name} = %{version}-%{release}
Conflicts:	python-gobject < 2.28.6-3
Obsoletes:	python3-gi

%description -n python-gi
This package contains the Python GObject Introspection bindings.

%package -n python-gi-cairo
Summary:	Python-gi bindings for Cairo
Group:		Development/Python
Requires:	python-gi = %{version}-%{release}
Requires:	typelib(PangoCairo)
Requires:	python-cairo >= 1.10.0
Provides:	python-gobject-cairo = %{version}-%{release}
Obsoletes:	ptyhon3-gi-cairo

%description -n python-gi-cairo
This package contains the Python-gi Cairo bindings.

%package devel
Group:		Development/C
Summary:	Python-gobject development files
Obsoletes:	python3-gobject3-devel

%description devel
This contains the python-gobject development files, including C
header, pkg-config file.

%prep
%setup -qn %{oname}-%{version}

%build
%configure2_5x PYTHON=%__python3
%make  LDFLAGS="`python3-config --ldflags`"

%install
PYTHON=%__python3 %makeinstall_std
rm -rf %{buildroot}%{python3_sitearch}/pygobject-*

# dsextra stuff is for windows installs so remove it
rm -fr %{buildroot}%{python_sitearch}/gtk-2.0

# docs are out of date and are being reworked upstream
# so remove them
rm -rf %{buildroot}%{_datadir}/gtk-doc
rm -rf %{buildroot}%{_datadir}/pygobject

%files -n python-gi
%doc README NEWS AUTHORS ChangeLog
%{py3_platsitedir}/gi
%{py3_platsitedir}/pygtkcompat
%exclude %{py3_platsitedir}/gi/_gi_cairo.*.so

%files -n python-gi-cairo
%{py3_platsitedir}/gi/_gi_cairo.*.so

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

