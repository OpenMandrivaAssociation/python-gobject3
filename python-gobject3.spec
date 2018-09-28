%define _disable_ld_no_undefined 1
%define _disable_rebuild_configure 1
%define url_ver %(echo %{version}|cut -d. -f1,2)

%define oname pygobject
%define api 2.0
%define major 0
%define libname %mklibname pyglib-gi %{api} %{major}
%define libname2 %mklibname py2glib-gi %{api} %{major}

%global __provides_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/(pygtkcompat|gi/pygtkcompat.py|gi/_gobject/__init__.py|gi/module.py|gi/__init__.py|gi/overrides/GIMarshallingTests.py)
%global __requires_exclude_from ^(%{python2_sitearch}|%{python3_sitearch})/(pygtkcompat|gi/pygtkcompat.py|gi/_gobject/__init__.py|gi/module.py|gi/__init__.py|gi/overrides/GIMarshallingTests.py)
%global __requires_exclude typelib\\(%%namespaces

Summary:	Python bindings for GObject Introspection
Name:		python-gobject3
Version:	3.30.1
Release:	1
License:	LGPLv2+ and MIT
Group:		Development/Python
Url:		http://www.gnome.org
Source0:	https://download.gnome.org/sources/pygobject/%url_ver/pygobject-%{version}.tar.xz
BuildRequires:	gtk-doc
BuildRequires:	pkgconfig(glib-2.0) >= 2.24.0
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.10.2
BuildRequires:	pkgconfig(libffi) >= 3.0
BuildRequires:	pkgconfig(pycairo) >= 1.2.0
BuildRequires:	pkgconfig(python2) >= 2.5.2
BuildRequires:	pkgconfig(python)
BuildRequires:	pkgconfig(py3cairo)
BuildRequires:	meson

%description
The %{name} package provides a convenient wrapper for the GObject
library for use in Python programs.

%package -n python-gi
Summary:	Python bindings for GObject Introspection
Group:		Development/Python
Provides:	python-gobject-introspection = %{version}-%{release}
Provides:	%{name} = %{version}-%{release}
Conflicts:	python-gobject < 2.28.6-3
Requires:	gobject-introspection
%rename python3-gi

%description -n python-gi
This package contains the Python GObject Introspection bindings.

%package -n python2-gi
Summary:	Python 2 bindings for GObject Introspection
Group:		Development/Python
Provides:	python2-gobject-introspection = %{version}-%{release}
Provides:	python2-gobject3 = %{version}-%{release}
Conflicts:	python2-gobject < 2.28.6-3

%description -n python2-gi
This package contains the Python 3 GObject Introspection bindings.

%package -n python-gi-cairo
Summary:	Python-gi bindings for Cairo
Group:		Development/Python
Requires:	python-gi = %{version}-%{release}
Requires:	typelib(PangoCairo)
Requires:	python-cairo >= 1.10.0
Provides:	python-gobject-cairo = %{version}-%{release}

%description -n python-gi-cairo
This package contains the Python-gi Cairo bindings.

%package -n python2-gi-cairo
Summary:	Python2-gi bindings for Cairo
Group:		Development/Python
Requires:	python2-gi = %{version}-%{release}
Requires:	typelib(PangoCairo)
Requires:	python2-cairo >= 1.10.0
Provides:	python2-gobject-cairo = %{version}-%{release}

%description -n python2-gi-cairo
This package contains the Python-gi Cairo bindings.

%package devel
Group:		Development/C
Summary:	Python-gobject development files
Requires:	pkgconfig(gobject-introspection-1.0)

%description devel
This contains the python-gobject development files, including C
header, pkg-config file.

%prep
%setup -q -c -T

# Python 2
tar xf %{SOURCE0}
mv pygobject-%{version} python2

# Python 3
cp -ar python2 python3

%build
# Python 2
pushd python2
%meson -Dpython=%{__python2}
%meson_build
popd

# Python 3
pushd python3
%meson -Dpython=%{__python3}
%meson_build
popd

%install
# Python 2
pushd python2
%meson_install
popd

# Python 3
pushd python3
%meson_install
popd

# dsextra stuff is for windows installs so remove it
rm -fr %{buildroot}%{py_platsitedir}/gtk-2.0

# docs are out of date and are being reworked upstream
# so remove them
rm -rf %{buildroot}%{_datadir}/gtk-doc
rm -rf %{buildroot}%{_datadir}/pygobject

%files -n python-gi
%{py_platsitedir}/gi
%{py_platsitedir}/pygtkcompat
%exclude %{py_platsitedir}/gi/_gi_cairo.*.so
%{py_sitelib}/*.egg-info

%files -n python2-gi
%{py2_platsitedir}/gi
%{py2_platsitedir}/pygtkcompat
%exclude %{py2_platsitedir}/gi/_gi_cairo.so
%{py2_platsitedir}/*.egg-info

%files -n python-gi-cairo
%{py_platsitedir}/gi/_gi_cairo.*.so

%files -n python2-gi-cairo
%{py2_platsitedir}/gi/_gi_cairo.so

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
