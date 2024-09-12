%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1
%define url_ver %(echo %{version}|cut -d. -f1,2)

%define oname pygobject
%define api 2.0
%define major 0
%define libname %mklibname pyglib-gi %{api} %{major}
%define libname2 %mklibname py2glib-gi %{api} %{major}

%global __provides_exclude_from ^(%{python_sitelib}|%{python_sitearch})/(pygtkcompat|gi/pygtkcompat.py|gi/_gobject/__init__.py|gi/module.py|gi/__init__.py|gi/overrides/GIMarshallingTests.py)
%global __requires_exclude_from ^(%{python_sitelib}|%{python_sitearch})/(pygtkcompat|gi/pygtkcompat.py|gi/_gobject/__init__.py|gi/module.py|gi/__init__.py|gi/overrides/GIMarshallingTests.py)
%global __requires_exclude typelib\\(%%namespaces

Summary:	Python bindings for GObject Introspection
Name:		python-gobject3
Version:	3.50.0
Release:	1
License:	LGPLv2+ and MIT
Group:		Development/Python
Url:		https://www.gnome.org
Source0:	https://download.gnome.org/sources/pygobject/%url_ver/pygobject-%{version}.tar.xz
# (bero) FIXME is this the right thing to do? GstInterfaces looks to me
# like it's obsolete crap from gstreamer 0.x days, but who really knows...
#Patch0:		pygobject-3.40.1-no-GstInterfaces.patch
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(glib-2.0) >= 2.24.0
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.10.2
BuildRequires:	pkgconfig(libffi) >= 3.0
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(py3cairo)
BuildRequires:	meson
Requires:	typelib(PangoCairo)
Requires:	python-cairo >= 1.10.0
%rename python-gi-cairo
%rename python-gobject-cairo

%description
The %{name} package provides a convenient wrapper for the GObject
library for use in Python programs.

%package -n python-gi
Summary:	Python bindings for GObject Introspection
Group:		Development/Python
Provides:	python-gobject-introspection = %{EVRD}
Conflicts:	python-gobject < 2.28.6-3
Requires:	gobject-introspection
Provides:	%{name}-base = %{EVRD}
%rename python3-gi

%description -n python-gi
This package contains the Python GObject Introspection bindings,
without non-cairo bits.

%package devel
Group:		Development/C
Summary:	Python-gobject development files
Requires:	pkgconfig(gobject-introspection-1.0)
Requires:	%{name} = %{EVRD}

%description devel
This contains the python-gobject development files, including C
header, pkg-config file.

%prep
%autosetup -p1 -n %{oname}-%{version}

%build
%meson -Dpython=%{__python3}
%meson_build

%install
%meson_install

# dsextra stuff is for windows installs so remove it
#rm -fr %{buildroot}%{py_platsitedir}/gtk-2.0

# docs are out of date and are being reworked upstream
# so remove them
rm -rf %{buildroot}%{_datadir}/gtk-doc
#rm -rf %{buildroot}%{_datadir}/pygobject

%files
%{python_sitearch}/gi/_gi_cairo*.so
%{python_sitearch}/gi/_gtktemplate.py
%{python_sitearch}/gi/pygtkcompat.py
%{python_sitearch}/pygtkcompat/
%{python_sitearch}/gi/__pycache__/pygtkcompat.*

%files -n python-gi

%{python_sitearch}/gi/
%{python_sitearch}/PyGObject-%{version}.egg-info
# (tpg) do not remove these
%exclude %{python_sitearch}/gi/pygtkcompat.py
%exclude %{python_sitearch}/gi/_gi_cairo*.so
%exclude %{python_sitearch}/gi/__pycache__/pygtkcompat.*
%exclude %{python_sitearch}/gi/_gtktemplate.py

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
