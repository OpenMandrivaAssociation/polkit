%define api 1
%define major 0
%define gir_major 1.0
%define libname %mklibname %{name} %{api} %{major}
%define girname %mklibname %{name}-gir %{gir_major}
%define develname %mklibname -d %{name} %{api}

Summary:	PolicyKit Authorization Framework
Name:		polkit
Version:	0.109
Release:	1
License:	LGPLv2+
Group:		System/Libraries
URL:		http://www.freedesktop.org/wiki/Software/PolicyKit
Source0:	http://www.freedesktop.org/software/polkit/releases/%{name}-%{version}.tar.gz
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	expat-devel
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(mozjs185)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(systemd)
# (cg) Only needed due to patches+autoconf
BuildRequires:	gettext-devel
Requires:	dbus

Obsoletes: PolicyKit <= 0.10
Provides: PolicyKit = 0.11

# polkit saw some API/ABI changes from 0.96 to 0.97 so require a
# sufficiently new polkit-gnome package
Conflicts: polkit-gnome < 0.97

Obsoletes: polkit-desktop-policy < 0.103
Provides: polkit-desktop-policy = 0.103

%description
PolicyKit is a toolkit for defining and handling authorizations.
It is used for allowing unprivileged processes to speak to privileged
processes.

%package -n %{libname}
Group:		System/Libraries
Summary:	PolicyKit Authorization Framework

%description -n %{libname}
This package contains the shared libraries of %{name}.

%package -n %{girname}
Group:		System/Libraries
Summary:	GObject Introspection interface library for %{name}
Conflicts:	polkit < 0.104-3

%description -n %{girname}
GObject Introspection interface library for %{name}.

%package -n %{develname}
Summary:	Development files for PolicyKit
Group:		Development/C
Requires:	%{libname} = %{version}-%{release}
Provides:	polkit-%{api}-devel = %{version}-%{release}
Requires: pkgconfig(glib-2.0)
Obsoletes: PolicyKit-devel <= 0.10
Provides: PolicyKit-devel = 0.11

%description -n %{develname}
Development files for PolicyKit.

%prep
%setup -q

%build
libtoolize --copy --force; aclocal; autoheader; automake --add-missing --force-missing; autoconf
%configure2_5x \
	--enable-gtk-doc \
	--disable-static \
	--libexecdir=%{_libexecdir}/polkit-1 \
    --enable-introspection \
    --enable-systemd=yes

%make LIBS="-lgmodule-2.0"

%install
%makeinstall_std
# (cg) Make the rules dir (this is where other packages should ship their rules)
mkdir -p %{buildroot}%{_datadir}/polkit-1/rules.d

%find_lang polkit-1 polkit-1.lang

# remove unpackaged files
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%pre
%_pre_useradd polkitd %{_prefix}/lib/polkit-1 /sbin/nologin

%post
# (cg) Previous package enabled this but it's now purely dbus activated
rm -f %{_sysconfdir}/systemd/system/graphical.target.wants/polkitd.service

%postun
%_postun_userdel polkitd

%files -f polkit-1.lang
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%{_sysconfdir}/pam.d/polkit-1
%{_bindir}/pkaction
%{_bindir}/pkcheck
%{_bindir}/pkttyagent
%{_bindir}/pk-example-frobnicate
%{_systemunitdir}/polkit.service
%dir %{_prefix}/lib/polkit-1
%{_prefix}/lib/polkit-1/polkitd
%{_datadir}/dbus-1/system-services/*
%dir %{_datadir}/polkit-1/
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.policy
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.examples.pkexec.policy
%attr(700,polkitd,root) %dir %{_datadir}/polkit-1/rules.d
%attr(700,polkitd,root) %{_sysconfdir}/polkit-1/rules.d
%dir %{_sysconfdir}/polkit-1
#%{_sysconfdir}/polkit-1/rules.d/50-default.rules
%{_mandir}/man1/*
%{_mandir}/man8/*

# see upstream docs for why these permissions are necessary
%attr(4755,root,root) %{_bindir}/pkexec
%attr(4755,root,root) %{_prefix}/lib/polkit-1/polkit-agent-helper-1

%files -n %{libname}
%{_libdir}/lib*-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Polkit*-%{gir_major}.typelib

%files -n %{develname}
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%{_datadir}/gtk-doc/html/*


%changelog
* Sun Jul 22 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.107-1
+ Revision: 810588
- update to new version 0.107

* Sat Jun 30 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.106-2
+ Revision: 807612
- add buildrequires in pkgconfig style for systemd stuff
- spec file clean
- sjip rules dir (form Mageia)
- adjust %%pre and %%postun scriplets (from Mageia)
- drop useles autoreconf

* Tue Jun 26 2012 Guilherme Moro <guilherme@mandriva.com> 0.106-1
+ Revision: 806932
- Update to version .106
  no more pkla files, use .rules files instead

* Tue May 08 2012 Guilherme Moro <guilherme@mandriva.com> 0.105-1
+ Revision: 797370
- Updated to version .105
  Dropped patch for linking

* Wed Apr 25 2012 Matthew Dawkins <mattydaw@mandriva.org> 0.104-5
+ Revision: 793439
- bump
- rebuild with rpm+g-i typelib auto prov/reqs generation

* Sun Feb 19 2012 Tomasz Pawel Gajc <tpg@mandriva.org> 0.104-2
+ Revision: 777317
- fix file list
- disable systemd support

* Thu Jan 05 2012 Götz Waschk <waschk@mandriva.org> 0.104-1
+ Revision: 757867
- new version
- fix linking

* Thu Dec 08 2011 Götz Waschk <waschk@mandriva.org> 0.103-1
+ Revision: 738860
- new version

* Fri Nov 18 2011 Matthew Dawkins <mattydaw@mandriva.org> 0.102-11
+ Revision: 731596
- bump to overcome stuck pkg in BS
- rebuild
  cleaned up spec
  removed defattr
  removed clean section
  removed .la files
  converted RPM_BUILD_ROOT to buildroot
  removed reqs in lib pkg for main pkg
  converted BRs to pkgconfig provides
  removed BuildRoot
  removed mkrel

* Sat Nov 05 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.102-9
+ Revision: 719991
- rebuild for glib2

* Wed Nov 02 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.102-8
+ Revision: 712302
- fix scriplets for good

* Sat Oct 29 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.102-7
+ Revision: 707784
- fix scriplets

* Fri Oct 28 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.102-6
+ Revision: 707762
- fix service script

* Fri Oct 28 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.102-5
+ Revision: 707759
- fix sed script

* Sun Oct 23 2011 Michael Scherer <misc@mandriva.org> 0.102-4
+ Revision: 705702
- fix %%post script

* Wed Oct 12 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 0.102-3
+ Revision: 704480
- fix scriplets
- enable systemd support to start polkitd early

* Sat Aug 06 2011 Götz Waschk <waschk@mandriva.org> 0.102-1
+ Revision: 693469
- update to new version 0.102

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.101-2
+ Revision: 667799
- mass rebuild

* Sun Mar 06 2011 Götz Waschk <waschk@mandriva.org> 0.101-1
+ Revision: 642324
- new version
- add example program

* Wed Feb 23 2011 Götz Waschk <waschk@mandriva.org> 0.100-1
+ Revision: 639421
- update to new version 0.100

* Mon Sep 20 2010 Götz Waschk <waschk@mandriva.org> 0.99-1mdv2011.0
+ Revision: 579953
- update to new version 0.99

* Tue Aug 24 2010 Götz Waschk <waschk@mandriva.org> 0.98-1mdv2011.0
+ Revision: 572587
- new version
- drop patch

* Fri Aug 20 2010 Götz Waschk <waschk@mandriva.org> 0.97-2mdv2011.0
+ Revision: 571424
- add fix for bug #60617

* Wed Aug 11 2010 Götz Waschk <waschk@mandriva.org> 0.97-1mdv2011.0
+ Revision: 568931
- new version
- drop patch 0

* Fri Jul 30 2010 Funda Wang <fwang@mandriva.org> 0.96-3mdv2011.0
+ Revision: 563242
- rebuild for new gobject-introspection

* Wed Apr 28 2010 Frederic Crozat <fcrozat@mandriva.com> 0.96-2mdv2010.1
+ Revision: 540125
- Patch0 (GIT): fix polkit information disclosure (fdo bug #26982)

* Mon Jan 18 2010 Frederic Crozat <fcrozat@mandriva.com> 0.96-1mdv2010.1
+ Revision: 493024
- Release 0.96

* Mon Nov 30 2009 Nicolas Lécureuil <nlecureuil@mandriva.com> 0.95-1mdv2010.1
+ Revision: 471660
- Update to version 0.95

* Thu Aug 13 2009 Frederic Crozat <fcrozat@mandriva.com> 0.94-1mdv2010.0
+ Revision: 415982
- Release 0.94

* Fri Jul 24 2009 Götz Waschk <waschk@mandriva.org> 0.93-2mdv2010.0
+ Revision: 399254
- fix libexecdir

* Fri Jul 24 2009 Götz Waschk <waschk@mandriva.org> 0.93-1mdv2010.0
+ Revision: 399185
- new version
- update file list

* Tue Jul 14 2009 Götz Waschk <waschk@mandriva.org> 0.92-2mdv2010.0
+ Revision: 395849
- update deps

* Tue Jul 14 2009 Götz Waschk <waschk@mandriva.org> 0.92-1mdv2010.0
+ Revision: 395832
- import polkit


* Tue Jul 14 2009 Götz Waschk <waschk@mandriva.org> 0.92-1mdv2010.0
- port to Mandriva

* Tue Jun 09 2009 David Zeuthen <davidz@redhat.com> - 0.92-3
- Don't make docs noarch (I *heart* multilib)
- Change license to LGPLv2+

* Mon Jun 08 2009 David Zeuthen <davidz@redhat.com> - 0.92-2
- Rebuild

* Mon Jun 08 2009 David Zeuthen <davidz@redhat.com> - 0.92-1
- Update to 0.92 release

* Wed May 27 2009 David Zeuthen <davidz@redhat.com> - 0.92-0.git20090527
- Update to 0.92 snapshot

* Mon Feb  9 2009 David Zeuthen <davidz@redhat.com> - 0.91-1
- Initial spec file.
