Summary: A library of functions for manipulating TIFF format image files.
Name: libtiff
Version: 3.5.7
Release: 7
Copyright: distributable
Group: System Environment/Libraries
Source0: http://www.libtiff.org/tiff-v%{version}.tar.gz
Patch0: tiff-v3.5-shlib.patch
Patch1: libtiff-v3.4-arm.patch
Patch2: libtiff-v3.5.4-codecs.patch
Patch3: libtiff-v3.5.4-mandir.patch
Patch4: libtiff-v3.5.5-buildroot.patch
Patch5: libtiff-v3.5.5-64bit.patch
Patch6: libtiff-v3.5.7-seek.patch
Patch7: libtiff-v3.5.7-exit.patch
Patch8: libtiff-v3.5.7-largefile.patch
URL: http://www.libtiff.org/
BuildRoot: %{_tmppath}/%{name}-root
BuildRequires: zlib-devel zlib libjpeg-devel libjpeg
Requires: zlib libjpeg 
%define LIBVER %(echo %{version} | cut -f-2 -d.)

%description
The libtiff package contains a library of functions for manipulating 
TIFF (Tagged Image File Format) image format files.  TIFF is a widely
used file format for bitmapped images.  TIFF files usually end in the
.tif extension and they are often quite large.

The libtiff package should be installed if you need to manipulate TIFF
format image files.

%package devel
Summary: Development tools for programs which will use the libtiff library.
Group: Development/Libraries
Requires: libtiff = %{version}

%description devel
This package contains the header files and static libraries for
developing programs which will manipulate TIFF format image files
using the libtiff library.

If you need to develop programs which will manipulate TIFF format
image files, you should install this package.  You'll also need to
install the libtiff package.

%prep
%setup -q -n tiff-v%{version}
%patch0 -p1 -b .shlib
%patch1 -p1 -b .arm
%patch2 -p1 -b .codecs
%patch3 -p1 -b .mandir
%patch4 -p1 -b .buildroot
%patch5 -p1 -b .64bit
%patch6 -p1 -b .seek
%patch7 -p1 -b .exit
%patch8 -p1 -b .largefile
find . -type d -name CVS | xargs -r rm -frv

%build

# Fixes problem with newer bash versions and doesn't hurt older ones.
CDPATH=""
unset CDPATH
./configure --target=%{_target_platform} << EOF
no
%{_bindir}
%{_libdir}
%{_includedir}
%{_mandir}
$RPM_DOC_DIR/%{name}-%{version}
bsd-source-cat
yes
EOF
cd libtiff
ln -s libtiff.so.%{LIBVER} libtiff.so
cd ..
export LDOPTS=-s
make

%install
[ "$RPM_BUILD_DIR" ] && rm -fr $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/{%{_bindir},%{_includedir},%{_mandir}}
make install
rm -f $RPM_BUILD_ROOT%{_libdir}/libtiff.so*
install -m755 libtiff/libtiff.so.%{LIBVER} $RPM_BUILD_ROOT%{_libdir}
ln -sf libtiff.so.%{LIBVER} $RPM_BUILD_ROOT%{_libdir}/libtiff.so

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYRIGHT README VERSION
%{_bindir}/*
%{_libdir}/libtiff.so.*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%doc TODO html
%{_includedir}/*
%{_libdir}/libtiff.so
%{_libdir}/libtiff.a
%{_mandir}/man3/*

%changelog
* Mon Aug 19 2002 Phil Knirsch <pknirsch@redhat.com> 3.5.7-7
- Added LFS support (#71593)

* Tue Jun 25 2002 Phil Knirsch <pknirsch@redhat.com> 3.5.7-6
- Fixed wrong exit code of tiffcp app (#67240)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 15 2002 Phil Knirsch <pknirsch@redhat.com>
- Fixed segfault in fax2tiff tool (#64708).

* Mon Feb 25 2002 Phil Knirsch <pknirsch@redhat.com>
- Fixed problem with newer bash versions setting CDPATH (#59741)

* Tue Feb 19 2002 Phil Knirsch <pknirsch@redhat.com>
- Update to current release 3.5.7

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Aug 28 2001 Phil Knirsch <phil@redhat.de>
- Fixed ia64 problem with tiffinfo. Was general 64 bit arch problem where s390x
  and ia64 were missing (#52129).

* Tue Jun 26 2001 Philipp Knirsch <pknirsch@redhat.de>
- Hopefully final symlink fix

* Thu Jun 21 2001 Than Ngo <than@redhat.com>
- add missing libtiff symlink

* Fri Mar 16 2001 Crutcher Dunnavant <crutcher@redhat.com>
- killed tiff-to-ps.fpi filter

* Wed Feb 28 2001 Philipp Knirsch <pknirsch@redhat.de>
- Fixed missing devel version dependancy.

* Tue Dec 19 2000 Philipp Knirsch <pknirsch@redhat.de>
- rebuild

* Tue Aug  7 2000 Crutcher Dunnavant <crutcher@redhat.com>
- added a tiff-to-ps.fpi filter for printing

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul 13 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply Peter Skarpetis's fix for the 32-bit conversion

* Mon Jul  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- make man pages non-executable (#12811)

* Mon Jun 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- remove CVS repo info from data directories

* Thu May 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix build rooting
- fix syntax error in configure script
- move man pages to %{_mandir}

* Wed May 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild for an errata release

* Wed Mar 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.5.5, which integrates our fax2ps fixes and the glibc fix

* Tue Mar 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix fax2ps swapping height and width in the bounding box

* Mon Mar 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- move man pages from devel package to the regular one
- integrate Frank Warmerdam's fixed .fax handling code (keep until next release
  of libtiff)
- fix fax2ps breakage (bug #8345)

* Sat Feb 05 2000 Nalin Dahyabhai <nalin@redhat.com>
- set MANDIR=man3 to make multifunction man pages friendlier

* Mon Jan 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix URLs

* Fri Jan 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- link shared library against libjpeg and libz

* Tue Jan 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable zip and jpeg codecs
- change defattr in normal package to 0755
- add defattr to -devel package

* Wed Dec 22 1999 Bill Nottingham <notting@redhat.com>
- update to 3.5.4

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 6)

* Wed Jan 13 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Wed Jun 10 1998 Prospector System <bugs@redhat.com>
- translations modified for de

* Wed Jun 10 1998 Michael Fulbright <msf@redhat.com>
- rebuilt against fixed jpeg libs (libjpeg-6b)

* Thu May 07 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Oct 13 1997 Donnie Barnes <djb@redhat.com>
- new version to replace the one from libgr
- patched for glibc
- added shlib support
