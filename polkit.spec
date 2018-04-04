%define api 1
%define major 0
%define girmaj 1.0
%define libagent %mklibname %{name}-agent %{api} %{major}
%define libgobject %mklibname %{name}-gobject %{api} %{major}
%define girname %mklibname %{name}-gir %{girmaj}
%define giragent %mklibname polkitagent-gir %{girmaj}
%define devname %mklibname -d %{name} %{api}

Summary:	PolicyKit Authorization Framework
Name:		polkit
Version:	0.114
Release:	1
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.freedesktop.org/wiki/Software/PolicyKit
Source0:	http://www.freedesktop.org/software/polkit/releases/%{name}-%{version}.tar.gz
Patch0:		polkit-0.113-ABF-workaround.patch
# (tpg) export environemt vars
Patch20:	x11vars.patch
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(mozjs185)
BuildRequires:	pkgconfig(libsystemd)
# (cg) Only needed due to patches+autoconf
BuildRequires:	gettext-devel
Requires:	dbus
Requires(pre,post,preun):	rpm-helper
# polkit saw some API/ABI changes from 0.96 to 0.97 so require a
# sufficiently new polkit-gnome package
Conflicts:	polkit-gnome < 0.97
%rename		PolicyKit
%rename		polkit-desktop-policy

%description
PolicyKit is a toolkit for defining and handling authorizations.
It is used for allowing unprivileged processes to speak to privileged
processes.

%package -n %{libagent}
Group:		System/Libraries
Summary:	PolicyKit Authorization Framework
Obsoletes:	%{_lib}polkit1_0 < 0.112-2

%description -n %{libagent}
This package contains a shared library for %{name}.

%package -n %{libgobject}
Group:		System/Libraries
Summary:	PolicyKit Authorization Framework
Conflicts:	%{_lib}polkit1_0 < 0.112-2

%description -n %{libgobject}
This package contains a shared library for %{name}.

%package -n %{girname}
Group:		System/Libraries
Summary:	GObject Introspection interface library for %{name}
Conflicts:	polkit < 0.104-3

%description -n %{girname}
GObject Introspection interface library for %{name}.

%package -n %{giragent}
Group:		System/Libraries
Summary:	GObject Introspection interface library for %{name}
Conflicts:	polkit < 0.104-3
Conflicts:	%{_lib}polkit-gir-1.0 < 0.112-2

%description -n %{giragent}
GObject Introspection interface library for %{name}.

%package -n %{devname}
Summary:	Development files for PolicyKit
Group:		Development/C
Provides:	polkit-%{api}-devel = %{version}-%{release}
Requires:	%{libagent} = %{version}-%{release}
Requires:	%{libgobject} = %{version}-%{release}
Requires:	%{girname} = %{version}-%{release}
Requires:	%{giragent} = %{version}-%{release}

%description -n %{devname}
Development files for PolicyKit.

%prep
%setup -q
%autopatch -p1

%build
autoreconf -fiv

%configure \
	--enable-gtk-doc \
	--disable-static \
	--libexecdir=%{_libexecdir}/polkit-1 \
	--enable-introspection \
	--enable-libsystemd-login=yes

%make_build LIBS="-lgmodule-2.0"

%install
%make_install
# (cg) Make the rules dir (this is where other packages should ship their rules)
mkdir -p %{buildroot}%{_datadir}/polkit-1/rules.d

%find_lang polkit-1 polkit-1.lang

%pre
%_pre_useradd polkitd %{_prefix}/lib/polkit-1 /sbin/nologin

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

%files -n %{libagent}
%{_libdir}/libpolkit-agent-%{api}.so.%{major}*

%files -n %{libgobject}
%{_libdir}/libpolkit-gobject-%{api}.so.%{major}*

%files -n %{girname}
%{_libdir}/girepository-1.0/Polkit-%{girmaj}.typelib

%files -n %{giragent}
%{_libdir}/girepository-1.0/PolkitAgent-%{girmaj}.typelib

%files -n %{devname}
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/*.gir
%{_datadir}/gtk-doc/html/*
