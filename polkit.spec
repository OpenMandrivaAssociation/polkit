%define api 1
%define major 0
%define girmaj 1.0
%define libagent %mklibname %{name}-agent %{api} %{major}
%define libgobject %mklibname %{name}-gobject %{api} %{major}
%define girname %mklibname %{name}-gir %{girmaj}
%define giragent %mklibname polkitagent-gir %{girmaj}
%define devname %mklibname -d %{name} %{api}

# (tpg) reduce size a bit
%global optflags %{optflags} -Oz

Summary:	PolicyKit Authorization Framework
Name:		polkit
Version:	0.119
Release:	5
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.freedesktop.org/wiki/Software/PolicyKit
Source0:	http://www.freedesktop.org/software/polkit/releases/%{name}-%{version}.tar.gz
Source1:	%{name}.sysusers
Patch0:		polkit-0.113-ABF-workaround.patch
Patch1:		polkit-0.119-fix-polkit-agent-helper-1-search-path.patch
# (tpg) export environemt vars
Patch20:	x11vars.patch
Patch21:	https://raw.githubusercontent.com/clearlinux-pkgs/polkit/master/more-gc.patch

BuildRequires:	meson
BuildRequires:	intltool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(mozjs-78)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(dbus-1)
Requires:	dbus
# polkit saw some API/ABI changes from 0.96 to 0.97 so require a
# sufficiently new polkit-gnome package
Conflicts:	polkit-gnome < 0.97
%rename		PolicyKit
%rename		polkit-desktop-policy
Requires(pre):	systemd
%systemd_ordering

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
%autosetup -p1

%build
# (tpg) this script is bogus
sed -i -e 's,meson_post_install.py,/bin/true,g' meson.build

%meson \
    -Dsession_tracking=libsystemd-login \
    -Dsystemdsystemunitdir=%{_unitdir} \
    -Dpolkitd_user=polkitd \
    -Dauthfw=pam

%meson_build

%install
%meson_install
# (cg) Make the rules dir (this is where other packages should ship their rules)
mkdir -p %{buildroot}%{_datadir}/polkit-1/rules.d

install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/%{name}.conf
sed -i -e 's,@LIBDIR@,%{_libdir},g' %{buildroot}%{_sysusersdir}/%{name}.conf

%find_lang polkit-1 polkit-1.lang

%pre
%sysusers_create_package %{name} %{SOURCE1}

%post
# The implied (systemctl preset) will fail and complain, but the macro hides
# and ignores the fact.  This is in fact what we want, polkit.service does not
# have an [Install] section and it is always started on demand.
%systemd_post polkit.service

%preun
%systemd_preun polkit.service

%postun
%systemd_postun_with_restart polkit.service

# (tpg) update /etc/passwd for new libdir for polkitd user
%triggerpostun -- %{name} < 0.119-5
systemctl stop polkit.service
usermod -d %{_libdir}/polkit-1 polkitd
systemctl start polkit.service

%files -f polkit-1.lang
%{_sysconfdir}/pam.d/polkit-1
%{_sysusersdir}/%{name}.conf
%{_bindir}/pkaction
%{_bindir}/pkcheck
%{_bindir}/pkttyagent
%{_unitdir}/polkit.service
%dir %{_libdir}/polkit-1
%{_libdir}/polkit-1/polkitd
%{_datadir}/dbus-1/system.d/org.freedesktop.PolicyKit1.conf
%{_datadir}/dbus-1/system-services/*
%dir %{_datadir}/polkit-1/
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/org.freedesktop.policykit.policy
%attr(700,polkitd,root) %dir %{_datadir}/polkit-1/rules.d
%attr(700,polkitd,root) %{_sysconfdir}/polkit-1/rules.d
%dir %{_sysconfdir}/polkit-1

# see upstream docs for why these permissions are necessary
%attr(4755,root,root) %{_bindir}/pkexec
%attr(4755,root,root) %{_libdir}/polkit-1/polkit-agent-helper-1

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
%{_datadir}/gettext/its/polkit.its
%{_datadir}/gettext/its/polkit.loc
