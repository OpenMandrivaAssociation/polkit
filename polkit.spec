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
Version:	0.112
Release:	15
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.freedesktop.org/wiki/Software/PolicyKit
Source0:	http://www.freedesktop.org/software/polkit/releases/%{name}-%{version}.tar.gz
Patch0:		0001-Post-release-version-bump-to-0.113.patch
Patch1:		0002-PolkitSystemBusName-Add-public-API-to-retrieve-Unix-.patch
Patch2:		0003-examples-cancel-Fix-to-securely-lookup-subject.patch
Patch3:		0004-Fixed-compilation-problem-in-the-backend.patch
Patch4:		0005-Don-t-discard-error-data-returned-by-polkit_system_b.patch
Patch5:		0006-sessionmonitor-systemd-Deduplicate-code-paths.patch
Patch6:		0007-PolkitSystemBusName-Retrieve-both-pid-and-uid.patch
Patch7:		0008-Port-internals-non-deprecated-PolkitProcess-API-wher.patch
Patch8:		0009-Use-G_GNUC_BEGIN_IGNORE_DEPRECATIONS-to-avoid-warnin.patch
Patch9:		0010-pkexec-Work-around-systemd-injecting-broken-XDG_RUNT.patch
Patch10:	0011-Fix-a-memory-leak.patch
Patch11:	0012-PolkitAgentSession-fix-race-between-child-and-io-wat.patch
Patch12:	0013-pkexec-Support-just-plain-pkexec-to-run-shell.patch
Patch13:	0014-build-Fix-several-issues-on-FreeBSD.patch
Patch14:	0015-polkitd-Fix-problem-with-removing-non-existent-sourc.patch
Patch15:	0016-sessionmonitor-systemd-prepare-for-D-Bus-user-bus-mo.patch
Patch16:	0017-Refuse-duplicate-user-arguments-to-pkexec.patch
Patch17:	0018-authority-Fix-memory-leak-in-EnumerateActions-call-r.patch
Patch18:	0019-Use-libsystemd-instead-of-older-libsystemd-login-if-.patch
Patch19:	0020-.dir-locals-Style-for-Emacs-we-don-t-use-tabs.patch
Patch20:	0021-authority-Avoid-cookie-wrapping-by-using-u64-counter.patch
Patch21:	0022-CVE-2015-3218-backend-Handle-invalid-object-paths-in.patch
Patch22:	0024-sessionmonitor-systemd-Use-sd_uid_get_state-to-check.patch
Patch23:	0025-Revert-authority-Avoid-cookie-wrapping-by-using-u64-.patch

# (tpg) https://bugs.freedesktop.org/show_bug.cgi?id=83590
Patch100:	polkit-0.112-do-not-insert-again-same-action_id.patch
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	pam-devel
BuildRequires:	pkgconfig(expat)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(mozjs185)
BuildRequires:	pkgconfig(libsystemd-login)
# (cg) Only needed due to patches+autoconf
BuildRequires:	gettext-devel
Requires:	dbus
Requires(pre,post,preun):	rpm-helper
# polkit saw some API/ABI changes from 0.96 to 0.97 so require a
# sufficiently new polkit-gnome package
Conflicts:	polkit-gnome < 0.97
%rename		PolicyKit
%rename		polkit-desktop-policy

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
%apply_patches

%build
autoreconf -fiv

%configure \
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
