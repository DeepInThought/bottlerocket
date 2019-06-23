%global goproject github.com/kubernetes
%global gorepo kubernetes
%global goimport %{goproject}/%{gorepo}

%global gover 1.12.9
%global rpmver %{gover}

%global _dwz_low_mem_die_limit 0

Name: %{_cross_os}%{gorepo}
Version: %{rpmver}
Release: 1%{?dist}
Summary: Container cluster management
License: ASL 2.0
URL: https://%{goimport}
Source0: https://%{goimport}/archive/v%{gover}/%{gorepo}-%{gover}.tar.gz
Source1: kubelet.service
Source2: kubelet-config
Source3: kubelet-kubeconfig
Source4: cluster-ca.crt
Source5: kubelet-tmpfiles.conf
Patch1: 0001-always-set-relevant-variables-for-cross-compiling.patch

BuildRequires: git
BuildRequires: rsync
BuildRequires: gcc-%{_cross_target}
BuildRequires: %{_cross_os}glibc-devel
BuildRequires: %{_cross_os}golang
Requires: %{_cross_os}conntrack-tools
Requires: %{_cross_os}containerd
Requires: %{_cross_os}glibc

%description
%{summary}.

%prep
%autosetup -Sgit -n %{gorepo}-%{gover} -p1
mkdir -p GOPATH/src/%{goproject}
ln -s %{_builddir}/%{gorepo}-%{gover} GOPATH/src/%{goimport}

%build
cd GOPATH/src/%{goimport}
export GOPATH="${PWD}/GOPATH"
export KUBE_BUILD_PLATFORMS="linux/%{_cross_go_arch}"
make WHAT="cmd/hyperkube"

%install
output="./_output/local/bin/linux/%{_cross_go_arch}"
install -d %{buildroot}%{_cross_bindir}
install -p -m 0755 ${output}/hyperkube %{buildroot}%{_cross_bindir}

for bin in \
  kube-apiserver kube-controller-manager \
  kube-proxy kube-scheduler kubectl kubelet ;
do
  ln -s hyperkube  %{buildroot}%{_cross_bindir}/${bin}
done

install -d %{buildroot}%{_cross_unitdir}
install -p -m 0644 %{S:1} %{buildroot}%{_cross_unitdir}/kubelet.service

install -d %{buildroot}%{_cross_unitdir}/multi-user.target.wants
ln -s ../kubelet.service %{buildroot}%{_cross_unitdir}/multi-user.target.wants

install -d %{buildroot}%{_cross_factorydir}%{_cross_sysconfdir}/kubernetes/kubelet
install -p -m 0644 %{S:2} %{buildroot}%{_cross_factorydir}%{_cross_sysconfdir}/kubernetes/kubelet/config
install -p -m 0644 %{S:3} %{buildroot}%{_cross_factorydir}%{_cross_sysconfdir}/kubernetes/kubelet/kubeconfig

install -d %{buildroot}%{_cross_factorydir}%{_cross_sysconfdir}/kubernetes/pki
install -p -m 0644 %{S:4} %{buildroot}%{_cross_factorydir}%{_cross_sysconfdir}/kubernetes/pki/ca.crt

install -d %{buildroot}%{_cross_tmpfilesdir}
install -p -m 0644 %{S:5} %{buildroot}%{_cross_tmpfilesdir}/kubelet.conf

%files
%{_cross_bindir}/hyperkube
%{_cross_bindir}/kube-apiserver
%{_cross_bindir}/kube-controller-manager
%{_cross_bindir}/kube-proxy
%{_cross_bindir}/kube-scheduler
%{_cross_bindir}/kubectl
%{_cross_bindir}/kubelet
%{_cross_unitdir}/kubelet.service
%{_cross_unitdir}/multi-user.target.wants/kubelet.service
%dir %{_cross_factorydir}%{_cross_sysconfdir}/kubernetes
%dir %{_cross_factorydir}%{_cross_sysconfdir}/kubernetes/kubelet
%{_cross_factorydir}%{_cross_sysconfdir}/kubernetes/kubelet/config
%{_cross_factorydir}%{_cross_sysconfdir}/kubernetes/kubelet/kubeconfig
%dir %{_cross_factorydir}%{_cross_sysconfdir}/kubernetes/pki
%{_cross_factorydir}%{_cross_sysconfdir}/kubernetes/pki/ca.crt
%{_cross_tmpfilesdir}/kubelet.conf

%changelog
