%define api 1
%define major 0
%define gir_major 1.0
%define libname %mklibname %{name} %{api} %{major}
%define girname %mklibname %{name}-gir %{gir_major}
%define develname %mklibname -d %{name} %{api}

Summary: PolicyKit Authorization Framework
Name: polkit
Version: 0.104
Release: 5
License: LGPLv2+
Group: System/Libraries
URL: http://www.freedesktop.org/wiki/Software/PolicyKit
Source0: http://hal.freedesktop.org/releases/%{name}-%{version}.tar.gz
Patch0: polkit-0.104-fix-linking.patch

BuildRequires: gtk-doc
BuildRequires: intltool
BuildRequires: expat-devel
BuildRequires: pam-devel
BuildRequires: pkgconfig(eggdbus-1)
BuildRequires: pkgconfig(gobject-introspection-1.0)
Requires: consolekit

%description
PolicyKit is a toolkit for defining and handling authorizations.
It is used for allowing unprivileged processes to speak to privileged
processes.

%package -n %{libname}
Group: System/Libraries
Summary: PolicyKit Authorization Framework

%description -n %{libname}
This package contains the shared libraries of %{name}.

%package -n %{girname}
Group:		System/Libraries
Summary:	GObject Introspection interface library for %{name}
Conflicts:	polkit < 0.104-3

%description -n %{girname}
GObject Introspection interface library for %{name}.

%package -n %{develname}
Summary: Development files for PolicyKit
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: polkit-%{api}-devel = %{version}-%{release}

%description -n %{develname}
Development files for PolicyKit.

%prep
%setup -q
%apply_patches
autoreconf -fi

%build
%configure2_5x \
	--enable-gtk-doc \
	--disable-static \
	--libexecdir=%{_libexecdir}/polkit-1

%make

%install
%makeinstall_std

%find_lang polkit-1 polkit-1.lang

# remove unpackaged files
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%files -f polkit-1.lang
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%{_sysconfdir}/pam.d/polkit-1
%{_sysconfdir}/polkit-1
%{_bindir}/pkaction
%{_bindir}/pkcheck
%{_bindir}/pk-example-frobnicate
%dir %{_libdir}/polkit-1
%dir %{_libdir}/polkit-1/extensions
%{_libdir}/polkit-1/extensions/*.so
%{_libexecdir}/polkit-1/polkitd
%{_datadir}/dbus-1/system-services/*
%dir %{_datadir}/polkit-1/
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.policy
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.examples.pkexec.policy
%{_mandir}/man1/*
%{_mandir}/man8/*

# see upstream docs for why these permissions are necessary
%attr(0700,root,root) %dir %{_var}/lib/polkit-1/
%attr(4755,root,root) %{_bindir}/pkexec
%attr(4755,root,root) %{_libexecdir}/polkit-1/polkit-agent-helper-1

%dir %{_localstatedir}/lib/polkit-1/localauthority
%dir %{_localstatedir}/lib/polkit-1/localauthority/10-vendor.d
%dir %{_localstatedir}/lib/polkit-1/localauthority/20-org.d
%dir %{_localstatedir}/lib/polkit-1/localauthority/30-site.d
%dir %{_localstatedir}/lib/polkit-1/localauthority/50-local.d
%dir %{_localstatedir}/lib/polkit-1/localauthority/90-mandatory.d

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

