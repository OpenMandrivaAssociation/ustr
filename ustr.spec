%define major 1
%define api 1.0
%define libname %{mklibname %{name} %{api} %{major}}
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
Release: 4
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
%{makeinstall} LDCONFIG=/bin/true HIDE=

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



%changelog
* Wed Sep 09 2009 Thierry Vignaud <tvignaud@mandriva.com> 1.0.4-3mdv2010.0
+ Revision: 434591
- rebuild

  + Götz Waschk <waschk@mandriva.org>
    - fix devel deps

* Fri Aug 08 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.0.4-2mdv2009.0
+ Revision: 269452
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Mon Apr 21 2008 David Walluck <walluck@mandriva.org> 1.0.4-1mdv2009.0
+ Revision: 196077
- 1.0.4

* Wed Jan 16 2008 David Walluck <walluck@mandriva.org> 1.0.3-1mdv2008.1
+ Revision: 153835
- 1.0.3

* Wed Jan 02 2008 David Walluck <walluck@mandriva.org> 1.0.2-2mdv2008.1
+ Revision: 140296
- build with -fPIC

* Wed Jan 02 2008 David Walluck <walluck@mandriva.org> 1.0.2-1mdv2008.1
+ Revision: 140274
- import ustr


* Tue Oct 30 2007 James Antill <james@and.org> - 1.0.2-2
- Build new upstream in Fedora

* Mon Oct 29 2007 James Antill <james@and.org> - 1.0.2-1
- New release

* Tue Aug 28 2007 James Antill <jantill@redhat.com> - 1.0.1-6
- Add options for fedora policy brokeness, so it's easy to undo.
- Rebuild for buildid.

* Wed Aug  8 2007 James Antill <james@and.org> - 1.0.1-5
- Import fix for ustr-import, wrt. repl <=> replace

* Sun Aug  5 2007 James Antill <james@and.org> - 1.0.1-4
- Patches for minor GIT HEAD documentation fixes.
- Install mkdir_p and fgrep examples.

* Sat Aug  4 2007 James Antill <james@and.org> - 1.0.1-2
- First upload to Fedora repos.

* Fri Aug  3 2007 James Antill <james@and.org> - 1.0.1-0.10.fc7
- Re-fix dups in -devel and -debug file lists.
- Change license to new format

* Thu Aug  2 2007 James Antill <james@and.org> - 1.0.1-0.9.fc7
- Fix dups in -devel and -debug file lists.

* Wed Aug  1 2007 James Antill <james@and.org> - 1.0.1-0.8.fc7
- Required to make DBG_ONLY_BAD_POLICIES_HAVE_THIS_EMPTY_CFLAGS empty
- due to so called "review"

* Fri Jul 27 2007 James Antill <james@and.org> - 1.0.1-0.2.fc7
- Next test release of 1.0.1, lots of fixes from Fedora review.

* Wed Jul 25 2007 James Antill <james@and.org> - 1.0.1-0
- Test release of 1.0.1.

* Wed Jul 11 2007 James Antill <james@and.org> - 1.0.0-1
- Upgrade to 1.0.0
- Minor fixes on specfile

* Sun Jun  3 2007 James Antill <james@and.org> - 0.99.2-1
- Upgrade to 0.99.2

* Thu May 24 2007 James Antill <james@and.org> - 0.99.1-2
- Fix ver typo to be version.

* Fri May 18 2007 James Antill <james@and.org> - 0.99.1-1
- Use all-shared to get GCC-ish specific shared libs.

* Mon May 14 2007 James Antill <james@and.org> - 0.98.1-0
- Initial spec

