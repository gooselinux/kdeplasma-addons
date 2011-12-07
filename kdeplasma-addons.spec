Name: kdeplasma-addons
Version: 4.3.4
Release: 5%{?dist}
Summary: Additional plasmoids for KDE

Group: User Interface/Desktops
License: GPLv2
URL: http://www.kde.org/
Source0: ftp://ftp.kde.org/pub/kde/stable/%{version}/src/kdeplasma-addons-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

## upstreamable patches
# disable contacts krunner that induces mostly needless kres-migrator and
# akonadi launch on first login
Patch51: kdeplasma-addons-4.2.2-krunner_contacts_not_enabledbydefault.patch

# disable webkit
Patch52: kdeplasma-addons-4.3.4-webkit.patch

# 4.3 upstream patches
Patch100: kdeplasma-addons-4.3.5.patch

BuildRequires: boost-devel
BuildRequires: gettext
BuildRequires: kdepimlibs-devel >= %{version}
BuildRequires: kdebase-workspace-devel >= %{version}
BuildRequires: kdegraphics-devel >= %{version}
BuildRequires: libXcomposite-devel libXrender-devel libXdamage-devel
BuildRequires: qimageblitz-devel
BuildRequires: soprano-devel

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }

%description
Additional plasmoids for KDE.

%package libs
Summary: Runtime libraries for %{name}
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: kdelibs4%{?_isa} >= %{version}

%description libs
%{summary}.

%package devel
Summary: Developer files for %{name}
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: plasma-devel

%description devel
Files for developing applications using %{name}.


%prep
%setup -q

%patch51 -p1 -b .krunner_contacts_not_enabledbydefault 
%patch52 -p1 -b .nowebkit

# 4.3 upstream patches
%patch100 -p1 -b .kde435

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LIB
%{_kde4_bindir}/lancelot
%{_kde4_appsdir}/bball/
%{_kde4_appsdir}/desktoptheme/*
%{_kde4_appsdir}/lancelot/
%{_kde4_appsdir}/plasma/services/*
%{_kde4_appsdir}/plasma-applet-frame/
#{_kde4_appsdir}/plasma-applet-opendesktop/
%{_kde4_appsdir}/plasma_pastebin/
%{_kde4_appsdir}/plasma_wallpaper_pattern/
%{_kde4_appsdir}/rssnow/
%{_kde4_configdir}/*.knsrc
%{_kde4_datadir}/kde4/services/*.desktop
%{_kde4_datadir}/kde4/services/ServiceMenus/*.desktop
%{_kde4_datadir}/kde4/servicetypes/*.desktop
%{_kde4_datadir}/mime/packages/lancelotpart-mime.xml
%{_kde4_datadir}/dbus-1/services/org.kde.lancelot.service
%{_kde4_libdir}/kde4/*.so
%{_kde4_iconsdir}/hicolor/*/*/*

%files libs
%defattr(-,root,root,-)
%{_kde4_libdir}/libconversion.so.*
%{_kde4_libdir}/libocsclient.so.*
%{_kde4_libdir}/liblancelot.so.*
%{_kde4_libdir}/libplasmapotdprovidercore.so.*
%{_kde4_libdir}/libplasmacomicprovidercore.so.*
%{_kde4_libdir}/libplasmaweather.so.*
#{_kde4_libdir}/librtm.so.*

%files devel
%defattr(-,root,root,-)
%{_kde4_includedir}/conversion/
%{_kde4_includedir}/lancelot/
%{_kde4_libdir}/libconversion.so
%{_kde4_libdir}/libocsclient.so
%{_kde4_libdir}/liblancelot.so
%{_kde4_libdir}/libplasma*.so
#%{_kde4_libdir}/librtm.so
%{_kde4_appsdir}/cmake/modules/FindConversion.cmake


%changelog
* Sat Jun 05 2010 Than Ngo <than@redhat.com> - 4.3.4-5
- Resolves: bz#597271, drop WebKit support in Qt

* Tue Mar 30 2010 Than Ngo <than@redhat.com> - 4.3.4-4
- rebuilt against qt-4.6.2

* Fri Jan 22 2010 Than Ngo <than@redhat.com> - 4.3.4-3
- backport 4.3.5 fixes

* Sat Dec 12 2009 Than Ngo <than@redhat.com> - 4.3.4-2
- cleanup

* Tue Dec 01 2009 Than Ngo <than@redhat.com> - 4.3.4-1
- 4.3.4

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Mon Oct 26 2009 Than Ngo <than@redhat.com> - 4.3.2-5
- remove duplicate BR on eigen2-devel

* Tue Oct 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.2-4
- rebuild (eigen2)

* Fri Oct 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.2-3
- rev microblog/twitter patch (kde#200475#c36)

* Sat Oct 10 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.2-2
- microblog/twitter fix (kde#209891)

* Mon Oct 05 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Sat Oct 03 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.1-3
- Ship -devel subpackage (#527011)

* Wed Sep 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-2
- Microblogging Widget Does Not Fetch Tweets (#526524)

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1

* Thu Aug 13 2009 Than Ngo <than@redhat.com> - 4.3.0-9
- omit BR on kdeedu-devel/eigen2-devel for rhel

* Fri Aug 07 2009 Ben Boeckel <MathStuf@gmail.com> - 4.3.0-8
- Waited for newRepo task

* Fri Aug 07 2009 Ben Boeckel <MathStuf@gmail.com> - 4.3.0-7
- Rebuild for mising rawhide oxygen-icon-theme
- Fix patch comments

* Fri Aug 07 2009 Ben Boeckel <MathStuf@gmail.com> - 4.3.0-6
- Add patch to fix kde#196809

* Tue Aug 04 2009 Than Ngo <than@redhat.com> - 4.3.0-5
- respin

* Mon Aug 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-4
- fix microblog post crasher (kdebug#202364)

* Mon Aug 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-3
- -libs subpkg to sanitize multilib

* Sun Aug 02 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.0-2
- fix to allow updating of status via microblog plasmoid 

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Wed Jul 22 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Thu Jul 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.96-2
- BR: libXcomposite-devel (lancelot eye-candy)

* Sun Jul 12 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Fri Jun 26 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3rc1

* Thu Jun 04 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.90-1
- KDE-4.3 beta2 (4.2.90)

* Mon May 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.85-4
- BR: eigen2-devel soprano-devel

* Tue May 19 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.85-3
- BR kdeedu-devel (for Marble)

* Sun May 17 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.85-2
- Obsoletes/Provides: kde-plasma-weather

* Wed May 13 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.85-1
- KDE 4.3 beta 1

* Thu Apr 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-3
- disable contacts krunner by default

* Wed Apr 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-2
- optimize scriptlets

* Tue Mar 31 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Mon Mar 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.1-3
- make bball applet work, ship .svg instead of .svgz (kdebug#185568)
- use new %%_qt45 macro
- spec housecleaning

* Fri Mar 13 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2.1-2
- fix Lancelot rendering issues with Qt 4.5 (F11+ only, as the effect of that
  patch with 4.4.3 is unknown)

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Wed Jan 07 2009 Than Ngo <than@redhat.com> - 4.1.96-1
- 4.2rc1

* Tue Dec 16 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.85-2
- saner versioned Obsoletes

* Fri Dec 12 2008 Than Ngo <than@redhat.com> 4.1.85-1
- 4.2beta2

* Tue Dec 02 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.80-3
- BR plasma-devel
- add Provides: kde-plasma-lancelot
- fix file list
- BR libkexiv2-devel >= 0.4.0 on F10+

* Thu Nov 20 2008 Than Ngo <than@redhat.com> 4.1.80-2
- merged
- add Obsoletes: kde-plasma-lancelot

* Thu Nov 20 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 4.1.80-1
- 4.1.80
- BR cmake >= 2.6.2
- make install/fast

* Wed Nov 12 2008 Than Ngo <than@redhat.com> 4.1.3-1
- 4.1.3

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-2
- make VERBOSE=1
- respin against new(er) kde-filesystem

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- 4.1.2

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-1
- 4.0.99

* Thu Jul 17 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-2
- kdeplasma-addons rename

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98

* Thu Jul 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-2
- Provides: kdeplasma-addons

* Sun Jul 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-1
- 4.0.85

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Fri Jun 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.83-2
- add ldconfig to scriptlets

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.82-1
- kdeplasmoids-4.0.82

* Tue May 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.80-2
- add missing BR openldap-devel
- update file list, add icon scriptlets

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta 1

* Wed May 07 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-0.1.20080506svn804581
- update to revision 804581 from KDE SVN (to match KDE 4.0.72)
- add COPYING and COPYING.LIB as %%doc
- update file list

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.1-5
- rebuild (again) for the fixed %%{_kde4_buildtype}

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.1-4
- rebuild for NDEBUG and _kde4_libexecdir

* Tue Mar 04 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.1-3
- disable broken bluemarble applet (crashes Plasma when no OpenGL, #435656)

* Tue Mar 04 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.1-2
- rebuild against KDE 4.0.2 (mainly to make sure it still builds)

* Thu Jan 31 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.1-1
- kde-4.0.1

* Tue Jan 08 2008 Sebastian Vahl <fedora@deadbabylon.de> 4.0.0-1
- kde-4.0.0

* Tue Dec 11 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.97.0-3
- add versioned obsolete kdeaddons

* Tue Dec 11 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.97.0-2
- package language files properly (by RexDieter)
- Obsolete: kdeaddons

* Tue Dec 11 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.97.0-1
- kde 3.97.0
- removed some BRs which are in kdelibs4-devel now
- BR: gettext

* Sun Dec 02 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.2-2
- update %%summary and %%description
- cleanup spec
- removed unneeded Requires

* Sun Dec 02 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.2-1
- kde-3.96.2

* Tue Nov 27 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.1-1
- kde-3.96.1

* Mon Nov 19 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.0-3
- BR: kde-filesystem >= 4

* Mon Nov 19 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.0-2
- BR: libxkbfile-devel
- BR: libXpm-devel
- BR: libXv-devel
- BR: libXxf86misc-devel
- BR: libXScrnSaver-devel
- BR: libXtst-devel
- BR: kdepimlibs-devel
- BR: qimageblitz-devel
- explicit require kdelibs, kdepimlibs and kdeworkspace >= version
- add require kde4-macro scriplet

* Thu Nov 15 2007 Sebastian Vahl <fedora@deadbabylon.de> 3.96.0-1
- Initial version for Fedora
