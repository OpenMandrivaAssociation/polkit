%define _with_systemd 1

%define api 1
%define major 0
%define libname %mklibname %name %api %major
%define develname %mklibname -d %name %api
Summary: PolicyKit Authorization Framework
Name: polkit
Version: 0.102
Release: %mkrel 6
License: LGPLv2+
URL: http://www.freedesktop.org/wiki/Software/PolicyKit
Source0: http://hal.freedesktop.org/releases/%{name}-%{version}.tar.gz
Source1: polkitd.service
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Group: System/Libraries
BuildRequires: expat-devel
BuildRequires: pam-devel
BuildRequires: eggdbus-devel
BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires: libgirepository-devel
%if %{_with_systemd}
BuildRequires: systemd-units >= 37
Requires(post): systemd-units
Requires(post): systemd-sysvinit
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif
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
%apply_patches

%build
%configure2_5x --enable-gtk-doc --disable-static --libexecdir=%{_libexecdir}/polkit-1

%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std

%if %{_with_systemd}
install -m 0644 -D %{SOURCE1} %{buildroot}%{_unitdir}/polkitd.service
sed -i -e 's#/usr/lib#%{_libdir}#g' %{buildroot}%{_unitdir}/polkitd.service
%endif

%find_lang polkit-1

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/polkit-1/extensions/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%if %{_with_systemd}
%post
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 -o $2 -ge 2 ]; then
/bin/systemctl enable polkitd.service >/dev/null 2>&1 || :
/bin/systemctl try-restart polkitd.service >/dev/null 2>&1 || :
fi

%postun
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
/bin/systemctl try-restart polkitd.service >/dev/null 2>&1 || :
fi

%preun
if [ $1 = 0 ]; then
/bin/systemctl --no-reload polkitd.service > /dev/null 2>&1 || :
/bin/systemctl stop polkitd.service > /dev/null 2>&1 || :
fi

%endif

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/lib*-%api.so.%{major}*

%files -f polkit-1.lang
%defattr(-,root,root,-)
%dir %{_libdir}/polkit-1
%dir %{_libdir}/polkit-1/extensions
%{_libdir}/polkit-1/extensions/*.so
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_datadir}/dbus-1/system-services/*
%dir %{_datadir}/polkit-1/
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.policy
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.examples.pkexec.policy
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%{_sysconfdir}/pam.d/polkit-1
%{_sysconfdir}/polkit-1
%{_bindir}/pkaction
%{_bindir}/pkcheck
%{_bindir}/pk-example-frobnicate
%{_libexecdir}/polkit-1/polkitd
%{_libdir}/girepository-1.0/*.typelib

# see upstream docs for why these permissions are necessary
%attr(0700,root,root) %dir %{_var}/lib/polkit-1/
%attr(4755,root,root) %{_bindir}/pkexec
%attr(4755,root,root) %{_libexecdir}/polkit-1/polkit-agent-helper-1

%attr(0700,root,root) %dir %{_localstatedir}/lib/polkit-1/
%dir %{_localstatedir}/lib/polkit-1/localauthority
%dir %{_localstatedir}/lib/polkit-1/localauthority/10-vendor.d
%dir %{_localstatedir}/lib/polkit-1/localauthority/20-org.d
%dir %{_localstatedir}/lib/polkit-1/localauthority/30-site.d
%dir %{_localstatedir}/lib/polkit-1/localauthority/50-local.d
%dir %{_localstatedir}/lib/polkit-1/localauthority/90-mandatory.d
%if %{_with_systemd}
%{_unitdir}/polkitd.service
%endif

%files -n %develname
%defattr(-,root,root,-)
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%{_includedir}/*
%{_datadir}/gtk-doc/html/*

