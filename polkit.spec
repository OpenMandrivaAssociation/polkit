%define api 1
%define major 0
%define libname %mklibname %name %api %major
%define develname %mklibname -d %name %api
Summary: PolicyKit Authorization Framework
Name: polkit
Version: 0.93
Release: %mkrel 2
License: LGPLv2+
URL: http://www.freedesktop.org/wiki/Software/PolicyKit
Source0: http://hal.freedesktop.org/releases/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Group: System/Libraries
BuildRequires: expat-devel
BuildRequires: pam-devel
BuildRequires: eggdbus-devel
BuildRequires: gtk-doc
BuildRequires: intltool
Requires: consolekit

%description
PolicyKit is a toolkit for defining and handling authorizations.
It is used for allowing unprivileged processes to speak to privileged
processes.

%package -n %libname
Group: System/Libraries
Summary: PolicyKit Authorization Framework
Requires: %name >= %version

%description -n %libname
PolicyKit is a toolkit for defining and handling authorizations.
It is used for allowing unprivileged processes to speak to privileged
processes.

This package contains the shared libraries of %{name}.

%package -n %develname
Summary: Development files for PolicyKit
Group: Development/C
Requires: %libname = %{version}-%{release}
Provides: polkit-%api-devel = %{version}-%{release}

%description -n %develname
Development files for PolicyKit.


%prep
%setup -q

%build
%configure2_5x --enable-gtk-doc --disable-static --libexecdir=%{_libexecdir}/polkit-1

make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%find_lang polkit-1

%clean
rm -rf $RPM_BUILD_ROOT

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/lib*-%api.so.%{major}*

%files -f polkit-1.lang
%defattr(-,root,root,-)
%dir %{_libdir}/polkit-1
%dir %{_libdir}/polkit-1/extensions
%{_libdir}/polkit-1/extensions/*.so
%{_libdir}/polkit-1/extensions/*.la
%{_datadir}/man/man1/pkexec.1*
%{_datadir}/man/man1/pkaction.1*
%{_datadir}/man/man1/pkcheck.1*
%_mandir/man8/pklocalauthority.8*
%_mandir/man8/polkit.8*
%_mandir/man8/polkitd.8*
%{_datadir}/dbus-1/system-services/*
%dir %{_datadir}/polkit-1/
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.policy
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%{_sysconfdir}/pam.d/polkit-1
%{_sysconfdir}/polkit-1
%{_bindir}/pkaction
%{_bindir}/pkcheck
%_libexecdir/polkit-1/polkitd

# see upstream docs for why these permissions are necessary
%attr(0700,root,root) %dir %{_localstatedir}/lib/polkit-1/
%attr(4755,root,root) %{_bindir}/pkexec
%attr(4755,root,root) %{_libexecdir}/polkit-1/polkit-agent-helper-1

%files -n %develname
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*
%{_bindir}/pk-example-frobnicate
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.examples.pkexec.policy
%{_datadir}/gtk-doc/html/*

