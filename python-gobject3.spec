%define _disable_rebuild_configure 1
%define url_ver %(echo %{version}|cut -d. -f1,2)

%define oname pygobject
%define api 2.0
%define major 0
%define libname %mklibname pyglib-gi %{api} %{major}
%define libname2 %mklibname py2glib-gi %{api} %{major}

%if %{_use_internal_dependency_generator}
%define __noautoprovfiles %{py_platsitedir}/gi/_gobject/__init__.py
%else
%define _exclude_files_from_autoreq ^%{py_platsitedir}/gi/_gobject/__init__.py
%endif

Summary:	Python bindings for GObject Introspection
Name:		python-gobject3
Version:	3.18.2
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
BuildRequires:	pkgconfig(python) >= 2.5.2
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

%description devel
This contains the python-gobject development files, including C
header, pkg-config file.

%prep
%setup -qn %{oname}-%{version} -c
mv %{oname}-%{version} python2
cp -r python2 python3

%build
pushd python3
%configure2_5x PYTHON=%__python3
%make LDFLAGS="`python3-config --ldflags`"
popd

pushd python2
%configure2_5x PYTHON=%__python2
%make LDFLAGS="`python2-config --ldflags`"
popd

%install
pushd python3
PYTHON=%__python3 %makeinstall_std
rm -rf %{buildroot}%{py3_sitearch}/pygobject-*
popd

pushd python2
PYTHON=%__python2 %makeinstall_std
rm -rf %{buildroot}%{py2_sitearch}/pygobject-*
popd

# dsextra stuff is for windows installs so remove it
rm -fr %{buildroot}%{py_platsitedir}/gtk-2.0

# docs are out of date and are being reworked upstream
# so remove them
rm -rf %{buildroot}%{_datadir}/gtk-doc
rm -rf %{buildroot}%{_datadir}/pygobject

%files -n python-gi
%doc python3/README python3/NEWS python3/AUTHORS python3/ChangeLog
%{py_platsitedir}/gi
%{py_platsitedir}/pygtkcompat
%exclude %{py_platsitedir}/gi/_gi_cairo.*.so
%{py_platsitedir}/pygobject-*-py%{py3_ver}-*.egg-info

%files -n python2-gi
%doc python2/README python2/NEWS python2/AUTHORS python2/ChangeLog
%{py2_platsitedir}/gi
%{py2_platsitedir}/pygtkcompat
%exclude %{py2_platsitedir}/gi/_gi_cairo.so
%{py2_platsitedir}/pygobject-*-py%{py2_ver}-*.egg-info

%files -n python-gi-cairo
%{py_platsitedir}/gi/_gi_cairo.*.so

%files -n python2-gi-cairo
%{py2_platsitedir}/gi/_gi_cairo.so

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
