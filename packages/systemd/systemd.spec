Name: %{_cross_os}systemd
Version: 241
Release: 1%{?dist}
Summary: System and Service Manager
License: LGPLv2+ and MIT and GPLv2+
URL: https://www.freedesktop.org/wiki/Software/systemd
Source0: https://github.com/systemd/systemd/archive/v%{version}/systemd-%{version}.tar.gz
BuildRequires: gperf
BuildRequires: intltool
BuildRequires: meson
BuildRequires: gcc-%{_cross_target}
BuildRequires: %{_cross_os}glibc-devel
BuildRequires: %{_cross_os}kmod-devel
BuildRequires: %{_cross_os}libacl-devel
BuildRequires: %{_cross_os}libattr-devel
BuildRequires: %{_cross_os}libblkid-devel
BuildRequires: %{_cross_os}libcap-devel
BuildRequires: %{_cross_os}libmount-devel
BuildRequires: %{_cross_os}libuuid-devel
BuildRequires: %{_cross_os}libxcrypt-devel
Requires: %{_cross_os}glibc
Requires: %{_cross_os}kmod
Requires: %{_cross_os}libacl
Requires: %{_cross_os}libattr
Requires: %{_cross_os}libblkid
Requires: %{_cross_os}libcap
Requires: %{_cross_os}libmount
Requires: %{_cross_os}libuuid
Requires: %{_cross_os}libxcrypt

%description
%{summary}.

%package devel
Summary: Files for development using the System and Service Manager
Requires: %{name}

%description devel
%{summary}.

%prep
%autosetup -n systemd-%{version} -p1

%build
CONFIGURE_OPTS=(
 -Dsplit-usr=false
 -Dsplit-bin=true
 -Drootprefix='%{_cross_prefix}'
 -Drootlibdir='%{_cross_libdir}'
 -Dlink-udev-shared=true
 -Dlink-systemctl-shared=true
 -Dstatic-libsystemd=false
 -Dstatic-libudev=false

 -Dsysvinit-path='%{_cross_sysconfdir}/init.d'
 -Dsysvrcnd-path='%{_cross_sysconfdir}/rc.d'

 -Dutmp=false
 -Dhibernate=false
 -Dldconfig=true
 -Dresolve=true
 -Defi=false
 -Dtpm=false
 -Denvironment-d=false
 -Dbinfmt=false
 -Dcoredump=false
 -Dlogind=false
 -Dhostnamed=true
 -Dlocaled=false
 -Dmachined=false
 -Dportabled=false
 -Dnetworkd=true
 -Dtimedated=false
 -Dtimesyncd=false
 -Dremote=false
 -Dnss-myhostname=false
 -Dnss-mymachines=false
 -Dnss-resolve=false
 -Dnss-systemd=false
 -Dfirstboot=false
 -Drandomseed=true
 -Dbacklight=false
 -Dvconsole=false
 -Dquotacheck=false
 -Dsysusers=true
 -Dtmpfiles=true
 -Dimportd=false
 -Dhwdb=false
 -Drfkill=false
 -Dman=false
 -Dhtml=false

 -Dcertificate-root='%{_cross_sysconfdir}/ssl'
 -Dpkgconfigdatadir='%{_cross_pkgconfigdir}'
 -Dpkgconfiglibdir='%{_cross_pkgconfigdir}'

 -Dseccomp=auto
 -Dselinux=auto
 -Dapparmor=false
 -Dsmack=false
 -Dpolkit=false
 -Dima=false

 -Dacl=true
 -Daudit=false
 -Dblkid=true
 -Dkmod=true
 -Dpam=false
 -Dmicrohttpd=false
 -Dlibcryptsetup=false
 -Dlibcurl=false
 -Didn=false
 -Dlibidn2=false
 -Dlibidn=false
 -Dlibiptc=false
 -Dqrencode=false
 -Dgcrypt=false
 -Dgnutls=false
 -Dopenssl=false
 -Delfutils=false
 -Dzlib=false
 -Dbzip2=false
 -Dxz=false
 -Dlz4=false
 -Dxkbcommon=false
 -Dpcre2=false
 -Dglib=false
 -Ddbus=false

 -Dgnu-efi=false

 -Dbashcompletiondir=no
 -Dzshcompletiondir=no

 -Dtests=false
 -Dslow-tests=false
 -Dinstall-tests=false

 -Doss-fuzz=false
 -Dllvm-fuzz=false
)

%cross_meson "${CONFIGURE_OPTS[@]}"
%cross_meson_build

%install
%cross_meson_install

%files
%{_cross_bindir}/busctl
%{_cross_bindir}/hostnamectl
%{_cross_bindir}/journalctl
%{_cross_bindir}/networkctl
%{_cross_bindir}/resolvectl
%{_cross_bindir}/systemctl
%{_cross_bindir}/systemd-analyze
%{_cross_bindir}/systemd-ask-password
%{_cross_bindir}/systemd-cat
%{_cross_bindir}/systemd-cgls
%{_cross_bindir}/systemd-cgtop
%{_cross_bindir}/systemd-delta
%{_cross_bindir}/systemd-detect-virt
%{_cross_bindir}/systemd-escape
%{_cross_bindir}/systemd-id128
%{_cross_bindir}/systemd-machine-id-setup
%{_cross_bindir}/systemd-mount
%{_cross_bindir}/systemd-notify
%{_cross_bindir}/systemd-nspawn
%{_cross_bindir}/systemd-path
%{_cross_bindir}/systemd-resolve
%{_cross_bindir}/systemd-run
%{_cross_bindir}/systemd-socket-activate
%{_cross_bindir}/systemd-stdio-bridge
%{_cross_bindir}/systemd-sysusers
%{_cross_bindir}/systemd-tmpfiles
%{_cross_bindir}/systemd-tty-ask-password-agent
%{_cross_bindir}/systemd-umount
%{_cross_bindir}/udevadm
%exclude %{_cross_bindir}/kernel-install

%{_cross_sbindir}/halt
%{_cross_sbindir}/init
%{_cross_sbindir}/poweroff
%{_cross_sbindir}/reboot
%{_cross_sbindir}/runlevel
%{_cross_sbindir}/shutdown
%{_cross_sbindir}/telinit
%{_cross_sbindir}/resolvconf

%{_cross_libdir}/libsystemd.so.*
%{_cross_libdir}/libudev.so.*
%dir %{_cross_libdir}/modprobe.d
%dir %{_cross_libdir}/sysctl.d
%dir %{_cross_libdir}/sysusers.d
%dir %{_cross_libdir}/tmpfiles.d
%dir %{_cross_libdir}/systemd
%dir %{_cross_libdir}/udev
%{_cross_libdir}/modprobe.d/*
%{_cross_libdir}/sysctl.d/*
%{_cross_libdir}/sysusers.d/*
%{_cross_libdir}/tmpfiles.d/*
%{_cross_libdir}/systemd/*
%{_cross_libdir}/udev/*
%exclude %{_cross_libdir}/kernel/install.d

%exclude %{_cross_sysconfdir}/systemd/
%exclude %{_cross_sysconfdir}/udev/
%exclude %{_cross_sysconfdir}/X11
%exclude %{_cross_sysconfdir}/init.d
%exclude %{_cross_sysconfdir}/xdg

%exclude %{_cross_datadir}/dbus-1
%exclude %{_cross_datadir}/polkit-1

%dir %{_cross_factorydir}
%exclude %{_cross_factorydir}%{_cross_sysconfdir}/nsswitch.conf
%exclude %{_cross_factorydir}%{_cross_sysconfdir}/pam.d
%exclude %{_cross_factorydir}%{_cross_sysconfdir}/pam.d/other
%exclude %{_cross_factorydir}%{_cross_sysconfdir}/pam.d/system-auth

%exclude %{_cross_docdir}
%exclude %{_cross_localedir}
%exclude %{_cross_localstatedir}

%files devel
%{_cross_libdir}/libsystemd.so
%{_cross_libdir}/libudev.so
%{_cross_pkgconfigdir}/systemd.pc
%{_cross_pkgconfigdir}/udev.pc
%{_cross_pkgconfigdir}/libsystemd.pc
%{_cross_pkgconfigdir}/libudev.pc
%{_cross_includedir}/libudev.h
%dir %{_cross_includedir}/systemd
%{_cross_includedir}/systemd/*.h
%exclude %{_cross_libdir}/rpm/macros.d

%changelog
