%define libname %{mklibname %{name} 1}
%define libnamedevel %{mklibname %{name} -d}
%define libnamestaticdevel %{mklibname %{name} -d -s}

%define show_all_cmds       1
%define broken_fed_dbg_opts 1

%if %{show_all_cmds}
%define policy_cflags_hide HIDE=
%else
%define policy_cflags_hide %{nil}
%endif

%if %{broken_fed_dbg_opts}
# Variable name explains itself.
%define policy_cflags_broken DBG_ONLY_BAD_POLICIES_HAVE_THIS_EMPTY_CFLAGS=
%else
%define policy_cflags_broken %{nil}
%endif

%define policy_cflags %{policy_cflags_hide} %{policy_cflags_broken}

Name: ustr
Version: 1.0.4
Release: %mkrel 2
Summary: String library, very low memory overhead, simple to import
Group: System/Libraries
License: MIT or LGPLv2+ or BSD
URL: http://www.and.org/ustr/
Source0: http://www.and.org/ustr/%{version}/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# BuildRequires: make gcc sed

%description
Micro string library, very low overhead from plain strdup() (Ave. 44% for
0-20B strings). Very easy to use in existing C code. At it's simplest you can
just include a single header file into your .c and start using it.
This package also distributes pre-built shared libraries.

%package -n %{libname}
Summary: String library, very low memory overhead, simple to import
Group: System/Libraries
Provides: %{name} = %{version}-%{release}

%description -n %{libname}
Micro string library, very low overhead from plain strdup() (Ave. 44% for
0-20B strings). Very easy to use in existing C code. At it's simplest you can
just include a single header file into your .c and start using it.
This package also distributes pre-built shared libraries.

%package -n %{libnamedevel}
Summary: Development files for %{name}
Group: Development/C
Provides: %{name}-devel = %{version}-%{release}
Requires: %libname = %version-%release

%description -n %{libnamedevel}
Header files for the Ustr string library, and the .so to link with.
Also includes a %{name}.pc file for pkg-config usage.
Includes the ustr-import tool, for if you jsut want to include
the code in your projects ... you don't have to link to the shared lib.

%package -n %{libnamestaticdevel}
Summary: Static development files for %{name}
Group: Development/C
Provides: %{name}-static-devel = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: %libnamedevel = %version-%release

%description -n %{libnamestaticdevel}
Static library for the Ustr string library.

%package -n %{libname}-debug
Summary: Development files for %{name}, with debugging options turned on
Group: Development/C
Provides:  %{name}-debug = %{version}-%{release}

%description -n %{libname}-debug
Dynamic libraries for a debug build of the Ustr string
library.

%package -n %{mklibname %{name}}-debug-devel
Summary: Development files for %{name}, with debugging options turned on
Group: Development/C
Provides: %{name}-debug-devel = %{version}-%{release}
Requires: %{name}-devel = %{version}-%{release}
Requires: %{name}-debug = %{version}-%{release}

%description -n %{mklibname %{name}}-debug-devel
Header files and dynamic libraries for a debug build of the Ustr string
library. Also includes a %{name}-debug.pc file for pkg-config usage.

%package -n %{mklibname %{name}}-debug-static-devel
Summary: Static development files for %{name}, with debugging options turned on
Group: Development/C
Provides: %{name}-debug-static = %{version}-%{release}
Requires: %{name}-debug-devel = %{version}-%{release}
Requires: %{name}-static-devel = %{version}-%{release}

%description -n %{mklibname %{name}}-debug-static-devel
Static library for the debug build of the Ustr string library.

%prep
%setup -q

%build
%{make} all-shared CFLAGS="%{optflags} -fPIC" %{policy_cflags}

%check
%{make} check %{policy_cflags}

%install
rm -rf $RPM_BUILD_ROOT
%{makeinstall} LDCONFIG=/bin/true HIDE=

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libname}-debug -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname}-debug -p /sbin/ldconfig
%endif

%files -n %{libname}
%defattr(-,root,root,-)
%doc ChangeLog LICENSE* README NEWS
%{_libdir}/libustr-1.0.so.*

%files -n %{libnamedevel}
%defattr(-,root,root,-)
%{_datadir}/ustr-%{version}
%{_bindir}/ustr-import
%{_includedir}/ustr.h
%{_includedir}/ustr-*.h
%exclude %{_includedir}/ustr*debug.h
%{_libdir}/pkgconfig/ustr.pc
%{_libdir}/libustr.so
%{_datadir}/doc/ustr-devel-%{version}
%{_mandir}/man1/*
%{_mandir}/man3/*

%files -n %{libnamestaticdevel}
%{_libdir}/libustr.a

%files -n %{libname}-debug
%defattr(-,root,root,-)
%{_libdir}/libustr-debug-1.0.so.*

%files -n %{mklibname %{name}}-debug-devel
%{_libdir}/libustr-debug.so
%{_includedir}/ustr-debug.h
%{_includedir}/ustr-conf-debug.h
%{_libdir}/pkgconfig/ustr-debug.pc

%files -n %{mklibname %{name}}-debug-static-devel
%{_libdir}/libustr-debug.a

