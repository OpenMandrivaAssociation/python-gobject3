%define url_ver %(echo %{version}|cut -d. -f1,2)

%define oname pygobject
%define api 2.0
%define major 0
%define libname %mklibname pyglib-gi %{api} %{major}
%define libname3 %mklibname py3glib-gi %{api} %{major}

%if %{_use_internal_dependency_generator}
%define __noautoprovfiles %{py_platsitedir}/gi/_gobject/__init__.py
%else
%define _exclude_files_from_autoreq ^%{py_platsitedir}/gi/_gobject/__init__.py
%endif

Summary:	Python bindings for GObject Introspection
Name:		python-gobject3
Version:	3.10.1
Release:	1
License:	LGPLv2+ and MIT
Group:		Development/Python
Url:		http://www.gnome.org
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{oname}/%{url_ver}/%{oname}-%{version}.tar.xz
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

%description -n python-gi
This package contains the Python GObject Introspection bindings.

%package -n python3-gi
Summary:	Python 3 bindings for GObject Introspection
Group:		Development/Python
Provides:	python3-gobject-introspection = %{version}-%{release}
Provides:	python3-gobject3 = %{version}-%{release}
Conflicts:	python3-gobject < 2.28.6-3

%description -n python3-gi
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

%package -n python3-gi-cairo
Summary:	Python3-gi bindings for Cairo
Group:		Development/Python
Requires:	python3-gi = %{version}-%{release}
Requires:	typelib(PangoCairo)
Requires:	python3-cairo >= 1.10.0
Provides:	python3-gobject-cairo = %{version}-%{release}

%description -n python3-gi-cairo
This package contains the Python-gi Cairo bindings.

%package -n %{libname}
Group:		System/Libraries
Summary:	Python GObject Introspection bindings shared library

%description -n %{libname}
This archive contains bindings for the GObject, to be used in Python
It is a fairly complete set of bindings, it's already rather useful, 
and is usable to write moderately complex programs.

%package -n %{libname3}
Group:		System/Libraries
Summary:	Python 3 GObject Introspection bindings shared library

%description -n %{libname3}
This archive contains bindings for the GObject, to be used in Python 3
It is a fairly complete set of bindings, it's already rather useful, 
and is usable to write moderately complex programs.

%package devel
Group:		Development/C
Summary:	Python-gobject development files
Requires:	%{libname} = %{version}-%{release}

%description devel
This contains the python-gobject development files, including C
header, pkg-config file.

%package -n python3-gobject3-devel
Group:		Development/C
Summary:	Python-gobject development files
Requires:	%{libname} = %{version}-%{release}

%description -n python3-gobject3-devel
This contains the python3-gobject development files, including C
header, pkg-config file.

%prep
%setup -qn %{oname}-%{version} -c
mv %{oname}-%{version} python2
cp -r python2 python3

%build
pushd python3
sed -i -e 's/AM_CONFIG_HEADER/AC_CONFIG_HEADERS/g' configure*
sed -i -e 's/AM_PROG_CC_STDC/AC_PROG_CC/g' configure*
autoreconf -fi
%configure2_5x PYTHON=%__python3
%make  LDFLAGS="`python3-config --ldflags`"
popd

pushd python2
sed -i -e 's/AM_CONFIG_HEADER/AC_CONFIG_HEADERS/g' configure*
sed -i -e 's/AM_PROG_CC_STDC/AC_PROG_CC/g' configure*
autoreconf -fi
%configure2_5x
%make LIBS="-lpython%{py_ver}"
popd

%install
pushd python3
PYTHON=%__python3 %makeinstall_std
rm -rf %{buildroot}%{python3_sitearch}/pygobject-*
popd

pushd python2
%makeinstall_std
rm -rf %{buildroot}%{python_sitearch}/pygobject-*
popd

# dsextra stuff is for windows installs so remove it
rm -fr %{buildroot}%{python_sitearch}/gtk-2.0

# docs are out of date and are being reworked upstream
# so remove them
rm -rf %{buildroot}%{_datadir}/gtk-doc
rm -rf %{buildroot}%{_datadir}/pygobject

%files -n python-gi
%doc python2/README python2/NEWS python2/AUTHORS python2/ChangeLog
%{py_platsitedir}/gi
%exclude %{py_platsitedir}/gi/_gi_cairo.so

%files -n python3-gi
%doc python3/README python3/NEWS python3/AUTHORS python3/ChangeLog
%{py3_platsitedir}/gi
%exclude %{py3_platsitedir}/gi/_gi_cairo.so

%files -n python-gi-cairo
%{py_platsitedir}/gi/_gi_cairo.so

%files -n python3-gi-cairo
%{py3_platsitedir}/gi/_gi_cairo.so

%files -n %{libname}
%{_libdir}/libpyglib-gi-%{api}-python.so.%{major}*

%files -n %{libname3}
%{_libdir}/libpyglib-gi-%{api}-python3.so.%{major}*

%files devel
%{_includedir}/*
%{_libdir}/*python.so
%{_libdir}/pkgconfig/*.pc

%files -n python3-gobject3-devel
%{_libdir}/*python3.so

