%define api 1
%define major 0
%define gir_major 1.0
%define libname %mklibname %{name} %{api} %{major}
%define girname %mklibname %{name}-gir %{gir_major}
%define develname %mklibname -d %{name} %{api}

Summary:		PolicyKit Authorization Framework
Name:			polkit
Version:		0.112
Release:		6.1
License:		LGPLv2+
Group:			System/Libraries
URL:			http://www.freedesktop.org/wiki/Software/PolicyKit
Source0:		http://www.freedesktop.org/software/polkit/releases/%{name}-%{version}.tar.gz
# (tpg) https://bugs.freedesktop.org/show_bug.cgi?id=88288
Patch0:         0000-polkit-0.112-authority-Fix-memory-leak-in-EnumerateActions.patch
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
Requires(pre):	rpm-helper
Requires(post):	rpm-helper
Requires(preun):	rpm-helper
# polkit saw some API/ABI changes from 0.96 to 0.97 so require a
# sufficiently new polkit-gnome package
Conflicts:		polkit-gnome < 0.97
%rename			PolicyKit
%rename			polkit-desktop-policy

%track
prog %name = {
	url = http://www.freedesktop.org/software/polkit/releases
	regex = %name-(__VER__)\.tar\.gz
	version = %version
}

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
Requires:	pkgconfig(glib-2.0)
Obsoletes:	PolicyKit-devel <= 0.10
Provides:	PolicyKit-devel = 0.11

%description -n %{develname}
Development files for PolicyKit.

%prep
%setup -q
%apply_patches

%build
%serverbuild_hardened

%configure2_5x \
	--enable-gtk-doc \
	--disable-static \
	--libexecdir=%{_libexecdir}/polkit-1 \
    --enable-introspection \
    --enable-libsystemd-login=yes

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
%systemd_post polkit.service

%preun
%systemd_preun polkit.service

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
