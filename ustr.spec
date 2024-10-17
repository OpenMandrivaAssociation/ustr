%define api 1.0
%define major 1
%define libname %mklibname %{name} %{api} %{major}
%define libnamedevel %mklibname %{name} -d

%define show_all_cmds       1
%define broken_fed_dbg_opts 0
%define multilib_inst       1

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

%define policy_cflags %{policy_cflags_hide}  %{policy_cflags_broken}

%if %{multilib_inst}
%define ustr_make_install install-multilib-linux
%else
%define ustr_make_install install
%endif

Name: ustr
Version: 1.0.4
Release: 11
Summary: String library, very low memory overhead, simple to import
Group: System/Libraries
License: MIT or LGPLv2+ or BSD
URL: https://www.and.org/ustr/
Source0: http://www.and.org/ustr/%{version}/%{name}-%{version}.tar.bz2
## Everybody uses this patch.
Patch0: ustr-1.0.4-c99-inline.patch
Patch1: ustr-1.0.4-ustrp_utf8_valid.patch
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
Obsoletes: %{name} < 1.0.4-13
Obsoletes: %{_lib}ustr1 < 1.0.4-13

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
Obsoletes: %{_lib}ustr-static-devel < 1.0.4-13

%description -n %{libnamedevel}
Header files for the Ustr string library, and the .so to link with.
Also includes a %{name}.pc file for pkg-config usage.
Includes the ustr-import tool, for if you jsut want to include
the code in your projects ... you don't have to link to the shared lib.


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
Obsoletes: %{_lib}ustr-debug-static-devel < 1.0.4-13

%description -n %{mklibname %{name}}-debug-devel
Header files and dynamic libraries for a debug build of the Ustr string
library. Also includes a %{name}-debug.pc file for pkg-config usage.

%prep
%setup -q
%autopatch -p1

%build
%make  all-shared CFLAGS="${CFLAGS:-%optflags}  -fgnu89-inline" %{policy_cflags}

%check
%if %{?chk}%{!?chk:1}
%make check CFLAGS="${CFLAGS:-%optflags}  -fgnu89-inline" %{policy_cflags}
%endif

%install
make $@ %{ustr_make_install} prefix=%{_prefix} \
                bindir=%{_bindir}         mandir=%{_mandir} \
                datadir=%{_datadir}       libdir=%{_libdir} \
                includedir=%{_includedir} libexecdir=%{_libexecdir} \
                DOCSHRDIR=%{_datadir}/doc/ustr-devel \
                DESTDIR=$RPM_BUILD_ROOT LDCONFIG=/bin/true HIDE=

# drop static build
find %{buildroot} -name "*.a" -delete

%files -n %{libname}
%license LICENSE*
%doc ChangeLog README NEWS
%{_libdir}/libustr-%{api}.so.%{major}{,.*}

%files -n %{libnamedevel}
%{_datadir}/ustr-%{version}
%{_bindir}/ustr-import
%if %{multilib_inst}
%{_libexecdir}/ustr-%{version}
%endif
%{_includedir}/ustr.h
%{_includedir}/ustr-*.h
%exclude %{_includedir}/ustr*debug.h
%{_libdir}/pkgconfig/ustr.pc
%{_libdir}/libustr.so
%{_docdir}/ustr-devel
%{_mandir}/man1/*.*
%{_mandir}/man3/*.*

%files -n %{libname}-debug
%{_libdir}/libustr-debug-1.0.so.*

%files -n %{mklibname %{name}}-debug-devel
%{_libdir}/libustr-debug-1.0.so.*
%{_libdir}/libustr-debug.so
%{_includedir}/ustr*-debug*.h
%{_libdir}/pkgconfig/ustr-debug.pc
