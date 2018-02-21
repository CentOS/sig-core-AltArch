%if 0%{?fedora}
%global with_devel 1
%global with_bundled 1
%global with_debug 1
%else
%global with_devel 0
%global with_bundled 1
%global with_debug 1
%endif

%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif
%global provider        github
%global provider_tld    com
%global project	        openshift
%global repo            ose
# https://github.com/openshift/ose
%global provider_prefix	%{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     k8s.io/kubernetes
%global commit		269f928217957e7126dc87e6adfa82242bfe5b1e
%global shortcommit	%(c=%{commit}; echo ${c:0:7})

%global openshift_ip    github.com/openshift/origin

%global k8s_provider        github
%global k8s_provider_tld    com
%global k8s_project         kubernetes
%global k8s_repo            kubernetes
# https://github.com/kubernetes/kubernetes
%global k8s_provider_prefix %{k8s_provider}.%{k8s_provider_tld}/%{k8s_project}/%{k8s_repo}
%global k8s_commit      43a9be421799afb8a9c02d3541212a6e623c9053
%global k8s_shortcommit %(c=%{k8s_commit}; echo ${c:0:7})
%global k8s_src_dir     Godeps/_workspace/src/k8s.io/kubernetes/
%global k8s_src_dir_sed Godeps\\/_workspace\\/src\\/k8s\\.io\\/kubernetes\\/

%global con_provider        github
%global con_provider_tld    com
%global con_project         kubernetes
%global con_repo            contrib
# https://github.com/kubernetes/kubernetes
%global con_provider_prefix %{con_provider}.%{con_provider_tld}/%{con_project}/%{con_repo}
%global con_commit      7fbd2520863b3c6a1d4a2e503cd76497f3ebc0e2
%global con_shortcommit %(c=%{con_commit}; echo ${c:0:7})

%global bindata_provider        github
%global bindata_provider_tld    com
%global bindata_project         jteeuwen
%global bindata_repo            go-bindata
# https://github.com/jteeuwen/go-bindata
%global bindata_provider_prefix %{bindata_provider}.%{bindata_provider_tld}/%{bindata_project}/%{bindata_repo}
%global bindata_commit      a0ff2567cfb70903282db057e799fd826784d41d
%global bindata_shortcommit %(c=%{bindata_commit}; echo ${c:0:7})

%global O4N_GIT_MAJOR_VERSION 3
%global O4N_GIT_MINOR_VERSION 4+
%global O4N_GIT_VERSION       v3.5.5.23
%global K8S_GIT_VERSION       v1.5.2-47-g43a9be4
%global kube_version          1.5.2
%global kube_git_version      v%{kube_version}

#I really need this, otherwise "version_ldflags=$(kube::version_ldflags)"
# does not work
%global _buildshell	/bin/bash
%global _checkshell	/bin/bash

Name:		kubernetes
Version:	%{kube_version}
Release:	0.7.git%{shortcommit}%{?dist}
Summary:        Container cluster management
License:        ASL 2.0
URL:            %{import_path}
ExclusiveArch:  x86_64
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1:        https://%{k8s_provider_prefix}/archive/%{k8s_commit}/%{k8s_repo}-%{k8s_shortcommit}.tar.gz
Source2:        https://%{con_provider_prefix}/archive/%{con_commit}/%{con_repo}-%{con_shortcommit}.tar.gz
Source3:        kubernetes-accounting.conf
Source4:        https://%{bindata_provider_prefix}/archive/%{bindata_commit}/%{bindata_repo}-%{bindata_shortcommit}.tar.gz

Source33:       genmanpages.sh
Patch0:         build-with-debug-info.patch
Patch1:         add-pod-infrastructure-container.patch
Patch2:         Change-etcd-server-port.patch

Patch9:         hack-test-cmd.sh.patch

# Drop apiserver command from hyperkube as apiserver has different permisions and capabilities
# Add kube-prefix for controller-manager, proxy and scheduler
Patch13:        remove-apiserver-backport-kubectl-add-kube-prefix-fo.patch
Patch17:        Hyperkube-remove-federation-cmds.patch

Patch18:        fix-rootScopeNaming-generate-selfLink-issue-37686.patch

# It obsoletes cadvisor but needs its source code (literally integrated)
Obsoletes:      cadvisor

# kubernetes is decomposed into master and node subpackages
# require both of them for updates
Requires: kubernetes-master = %{version}-%{release}
Requires: kubernetes-node = %{version}-%{release}

%description
%{summary}

%package unit-test
Summary: %{summary} - for running unit tests

# below Rs used for testing
Requires: golang >= 1.2-7
Requires: etcd >= 2.0.9
Requires: hostname
Requires: rsync
Requires: NetworkManager

%description unit-test
%{summary} - for running unit tests

%package master
Summary: Kubernetes services for master host

BuildRequires: golang >= 1.2-7
BuildRequires: systemd
BuildRequires: rsync
BuildRequires: golang-github-cpuguy83-go-md2man

Requires(pre): shadow-utils
Requires: kubernetes-client = %{version}-%{release}

# if node is installed with node, version and release must be the same
Conflicts: kubernetes-node < %{version}-%{release}
Conflicts: kubernetes-node > %{version}-%{release}

%description master
Kubernetes services for master host

%package node
Summary: Kubernetes services for node host

%if 0%{?fedora} >= 21 || 0%{?rhel}
Requires: docker
%else
Requires: docker-io
%endif

BuildRequires: golang >= 1.2-7
BuildRequires: systemd
BuildRequires: rsync
BuildRequires: golang-github-cpuguy83-go-md2man

Requires(pre): shadow-utils
Requires: socat
Requires: kubernetes-client = %{version}-%{release}
Requires: conntrack-tools

# if master is installed with node, version and release must be the same
Conflicts: kubernetes-master < %{version}-%{release}
Conflicts: kubernetes-master > %{version}-%{release}

%description node
Kubernetes services for node host

%package client
Summary: Kubernetes client tools

BuildRequires: golang >= 1.2-7

%description client
Kubernetes client tools like kubectl

%prep
%setup -q -n %{k8s_repo}-%{k8s_commit} -T -b 1
%if 0%{?with_debug}
%patch0 -p1
%endif

# Hack test-cmd.sh to be run with os binaries
#%patch9 -p1

%setup -q -n %{bindata_repo}-%{bindata_commit} -T -b 4

%setup -q -n %{con_repo}-%{con_commit} -T -b 2
%patch1 -p1

%setup -q -n %{repo}-%{commit}

# clean the directory up to Godeps
dirs=$(ls | grep -v "^vendor")
rm -rf $dirs

# move k8s code from Godeps
mv vendor/k8s.io/kubernetes/* .
# copy missing source code
cp ../%{k8s_repo}-%{k8s_commit}/cmd/kube-apiserver/apiserver.go cmd/kube-apiserver/.
cp ../%{k8s_repo}-%{k8s_commit}/cmd/kube-controller-manager/controller-manager.go cmd/kube-controller-manager/.
cp ../%{k8s_repo}-%{k8s_commit}/cmd/kubelet/kubelet.go cmd/kubelet/.
cp ../%{k8s_repo}-%{k8s_commit}/cmd/kube-proxy/proxy.go cmd/kube-proxy/.
cp ../%{k8s_repo}-%{k8s_commit}/plugin/cmd/kube-scheduler/scheduler.go plugin/cmd/kube-scheduler/.
cp -r ../%{k8s_repo}-%{k8s_commit}/cmd/kubectl cmd/.
# copy hack directory
cp -r ../%{k8s_repo}-%{k8s_commit}/hack .
cp -r ../%{k8s_repo}-%{k8s_commit}/cluster .
# copy contrib folder
mkdir -p contrib
cp -r ../%{con_repo}-%{con_commit}/init contrib/.
# copy docs
mkdir docs
cp -r ../%{k8s_repo}-%{k8s_commit}/docs/admin docs/.
cp -r ../%{k8s_repo}-%{k8s_commit}/docs/man docs/.
cp -r ../%{k8s_repo}-%{k8s_commit}/cmd/{gendocs,genkubedocs,genman,genyaml} cmd/.
mkdir -p federation/cmd
cp -r ../%{k8s_repo}-%{k8s_commit}/federation .
#github.com/spf13/cobra/doc
mkdir -p vendor/github.com/spf13
cp -r ../%{k8s_repo}-%{k8s_commit}/vendor/github.com/spf13/cobra vendor/github.com/spf13/.
#github.com/cpuguy83/go-md2man/md2man
mkdir -p vendor/github.com/cpuguy83
cp -r ../%{k8s_repo}-%{k8s_commit}/vendor/github.com/cpuguy83/go-md2man vendor/github.com/cpuguy83/.
#github.com/aws/aws-sdk-go/service/route53
mkdir -p vendor/github.com/aws
cp -r ../%{k8s_repo}-%{k8s_commit}/vendor/github.com/aws/aws-sdk-go vendor/github.com/aws/.
#google.golang.org/api/dns/v1
mkdir -p vendor/google.golang.org
cp -r ../%{k8s_repo}-%{k8s_commit}/vendor/google.golang.org/api vendor/google.golang.org/.
# copy LICENSE and *.md
cp ../%{k8s_repo}-%{k8s_commit}/LICENSE .
cp ../%{k8s_repo}-%{k8s_commit}/*.md .
# copy hyperkube
cp -r ../%{k8s_repo}-%{k8s_commit}/cmd/hyperkube cmd/.
# copy swagger
#cp -r ../%{k8s_repo}-%{k8s_commit}/pkg/ui/data/swagger pkg/ui/data/.
# copy Makefiles
cp -r ../%{k8s_repo}-%{k8s_commit}/Makefile .
cp -r ../%{k8s_repo}-%{k8s_commit}/Makefile.generated_files .
cp -r ../%{k8s_repo}-%{k8s_commit}/test .
# cmd/libs/go2idl/deepcopy-gen/
cp -r ../%{k8s_repo}-%{k8s_commit}/cmd/libs/go2idl/{deepcopy-gen,conversion-gen,defaulter-gen,openapi-gen} cmd/libs/go2idl/.
# missing vendored deps
# - k8s.io/kubernetes/pkg/client/metrics/prometheus
# - k8s.io/kubernetes/pkg/version/prometheus
# - k8s.io/kubernetes/pkg/version/verflag
mkdir -p vendor/k8s.io/kubernetes/pkg/client/metrics/
cp -r ../%{k8s_repo}-%{k8s_commit}/pkg/client/metrics/prometheus vendor/k8s.io/kubernetes/pkg/client/metrics/.
mkdir -p vendor/k8s.io/kubernetes/pkg/version
cp -r ../%{k8s_repo}-%{k8s_commit}/pkg/version/prometheus vendor/k8s.io/kubernetes/pkg/version/.
cp -r ../%{k8s_repo}-%{k8s_commit}/pkg/version/verflag vendor/k8s.io/kubernetes/pkg/version/.

%patch2 -p1

# Drop apiserver from hyperkube
%patch13 -p1
%patch17 -p1

# Move all the code under src/k8s.io/kubernetes directory
mkdir -p src/k8s.io/kubernetes
mv $(ls | grep -v "^src$") src/k8s.io/kubernetes/.

%patch18 -p1

mkdir -p src/%{bindata_provider_prefix}
cp -r ../%{bindata_repo}-%{bindata_commit}/* src/%{bindata_provider_prefix}/.

%build
export GOPATH=$(pwd)
go build -o go-bindata %{bindata_provider_prefix}/go-bindata
export PATH=${PATH}:$(pwd)

pushd src/k8s.io/kubernetes/
export KUBE_GIT_TREE_STATE="clean"
export KUBE_GIT_COMMIT=%{commit}
export KUBE_GIT_VERSION=%{kube_git_version}
export KUBE_EXTRA_GOPATH=$(pwd)/Godeps/_workspace

# https://bugzilla.redhat.com/show_bug.cgi?id=1392922#c1
%ifarch ppc64le
export GOLDFLAGS='-linkmode=external'
%endif
make WHAT="--use_go_build cmd/hyperkube cmd/kube-apiserver"

# convert md to man
./hack/generate-docs.sh || true
pushd docs
pushd admin
cp kube-apiserver.md kube-controller-manager.md kube-proxy.md kube-scheduler.md kubelet.md ..
popd
cp %{SOURCE33} genmanpages.sh
bash genmanpages.sh
popd

%install
pushd src/k8s.io/kubernetes/
. hack/lib/init.sh
kube::golang::setup_env

%ifarch ppc64le
output_path="${KUBE_OUTPUT_BINPATH}"
%else
output_path="${KUBE_OUTPUT_BINPATH}/$(kube::golang::current_platform)"
%endif

install -m 755 -d %{buildroot}%{_bindir}

echo "+++ INSTALLING hyperkube"
install -p -m 755 -t %{buildroot}%{_bindir} ${output_path}/hyperkube

echo "+++ INSTALLING kube-apiserver"
install -p -m 754 -t %{buildroot}%{_bindir} ${output_path}/kube-apiserver

binaries=(kube-controller-manager kube-scheduler kube-proxy kubelet kubectl)
for bin in "${binaries[@]}"; do
  echo "+++ HARDLINKING ${bin} to hyperkube"
  ln %{buildroot}%{_bindir}/hyperkube %{buildroot}%{_bindir}/${bin}
done

# install the bash completion
install -d -m 0755 %{buildroot}%{_datadir}/bash-completion/completions/
%{buildroot}%{_bindir}/kubectl completion bash > %{buildroot}%{_datadir}/bash-completion/completions/kubectl

# install config files
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -m 644 -t %{buildroot}%{_sysconfdir}/%{name} contrib/init/systemd/environ/*

# install service files
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 -t %{buildroot}%{_unitdir} contrib/init/systemd/*.service

# install manpages
install -d %{buildroot}%{_mandir}/man1
install -p -m 644 docs/man/man1/* %{buildroot}%{_mandir}/man1
# from k8s tarball copied docs/man/man1/*.1

# install the place the kubelet defaults to put volumes
install -d %{buildroot}%{_sharedstatedir}/kubelet

# place contrib/init/systemd/tmpfiles.d/kubernetes.conf to /usr/lib/tmpfiles.d/kubernetes.conf
install -d -m 0755 %{buildroot}%{_tmpfilesdir}
install -p -m 0644 -t %{buildroot}/%{_tmpfilesdir} contrib/init/systemd/tmpfiles.d/kubernetes.conf
mkdir -p %{buildroot}/run
install -d -m 0755 %{buildroot}/run/%{name}/

# enable CPU and Memory accounting
install -d -m 0755 %{buildroot}/%{_sysconfdir}/systemd/system.conf.d
install -p -m 0644 -t %{buildroot}/%{_sysconfdir}/systemd/system.conf.d %{SOURCE3}

# rpmdiff issues
#chmod 0755 %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/hack/build-ui.sh
#chmod 0644 %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/hack/lib/util.sh
chmod 0755 %{buildroot}%{_datadir}/bash-completion/completions/kubectl
popd

mv src/k8s.io/kubernetes/*.md .
mv src/k8s.io/kubernetes/LICENSE .

# place files for unit-test rpm
install -d -m 0755 %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/
# basically, everything from the root directory is needed
# unit-tests needs source code
# integration tests needs docs and other files
# test-cmd.sh atm needs cluster, examples and other
cp -a src %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/
rm -rf %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/src/k8s.io/kubernetes/_output
cp -a *.md %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/src/k8s.io/kubernetes/

# rpmdiff issues
chmod 0644 %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/src/k8s.io/kubernetes/vendor/github.com/openshift/source-to-image/pkg/scripts/install.go
chmod 0755 %{buildroot}%{_sharedstatedir}/kubernetes-unit-test/src/k8s.io/kubernetes/plugin/pkg/scheduler/algorithm/predicates/predicates_test.go

%check
# Fedora, RHEL7 and CentOS are tested via unit-test subpackage
if [ 1 != 1 ]; then
echo "******Testing the commands*****"
hack/test-cmd.sh
echo "******Benchmarking kube********"
hack/benchmark-go.sh

# In Fedora 20 and RHEL7 the go cover tools isn't available correctly
%if 0%{?fedora} >= 21
echo "******Testing the go code******"
hack/test-go.sh
echo "******Testing integration******"
hack/test-integration.sh --use_go_build
%endif
fi

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
# empty as it depends on master and node

%files master
%license LICENSE
%doc *.md
%{_mandir}/man1/kube-apiserver.1*
%{_mandir}/man1/kube-controller-manager.1*
%{_mandir}/man1/kube-scheduler.1*
%attr(754, -, kube) %caps(cap_net_bind_service=ep) %{_bindir}/kube-apiserver
%{_bindir}/kube-controller-manager
%{_bindir}/kube-scheduler
%{_bindir}/hyperkube
%{_unitdir}/kube-apiserver.service
%{_unitdir}/kube-controller-manager.service
%{_unitdir}/kube-scheduler.service
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/apiserver
%config(noreplace) %{_sysconfdir}/%{name}/scheduler
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/controller-manager
%{_tmpfilesdir}/kubernetes.conf
%verify(not size mtime md5) %attr(755, kube,kube) %dir /run/%{name}

%files node
%license LICENSE
%doc *.md
%{_mandir}/man1/kubelet.1*
%{_mandir}/man1/kube-proxy.1*
%{_bindir}/kubelet
%{_bindir}/kube-proxy
%{_bindir}/hyperkube
%{_unitdir}/kube-proxy.service
%{_unitdir}/kubelet.service
%dir %{_sharedstatedir}/kubelet
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config
%config(noreplace) %{_sysconfdir}/%{name}/kubelet
%config(noreplace) %{_sysconfdir}/%{name}/proxy
%config(noreplace) %{_sysconfdir}/systemd/system.conf.d/kubernetes-accounting.conf
%{_tmpfilesdir}/kubernetes.conf
%verify(not size mtime md5) %attr(755, kube,kube) %dir /run/%{name}

%files client
%license LICENSE
%doc *.md
%{_mandir}/man1/kubectl.1*
%{_mandir}/man1/kubectl-*
%{_bindir}/kubectl
%{_bindir}/hyperkube
%{_datadir}/bash-completion/completions/kubectl

%files unit-test
%{_sharedstatedir}/kubernetes-unit-test/

%pre master
getent group kube >/dev/null || groupadd -r kube
getent passwd kube >/dev/null || useradd -r -g kube -d / -s /sbin/nologin \
        -c "Kubernetes user" kube

%post master
%systemd_post kube-apiserver kube-scheduler kube-controller-manager

%preun master
%systemd_preun kube-apiserver kube-scheduler kube-controller-manager

%postun master
%systemd_postun


%pre node
getent group kube >/dev/null || groupadd -r kube
getent passwd kube >/dev/null || useradd -r -g kube -d / -s /sbin/nologin \
        -c "Kubernetes user" kube

%post node
%systemd_post kubelet kube-proxy
# If accounting is not currently enabled systemd reexec
if [[ `systemctl show docker kubelet | grep -q -e CPUAccounting=no -e MemoryAccounting=no; echo $?` -eq 0 ]]; then
  systemctl daemon-reexec
fi

%preun node
%systemd_preun kubelet kube-proxy

%postun node
%systemd_postun

%changelog
* Tue Jun 06 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.5.2-0.7.git269f928
- Update to ose v3.5.5.23
  resolves: #1459174

* Tue May 02 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.5.2-0.6.gita552679
- Update to ose v3.5.5.11
  resolves: #1447353

* Tue Mar 21 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.5.2-0.5.gita552679
- Re-generate man pages
  related: #1434371

* Tue Mar 21 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.5.2-0.4.gita552679
- Update to ose v3.5.0.55
  resolves: #1434371

* Thu Mar 09 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.5.2-0.3.gitc55cf2b
- fix rootScopeNaming generate selfLink
  resolves: #1430427

* Mon Feb 06 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.5.2-0.2.gitc55cf2b
- Fix rpmdiff issues
  related: #1419726

* Mon Feb 06 2017 Jan Chaloupka <jchaloup@redhat.com> - 1.5.2-0.1.gitc55cf2b
- Update to ose v3.5.0.17
  resolves: #1419726

* Mon Dec 12 2016 Jan Chaloupka <jchaloup@redhat.com> - 1.4.0-0.1.git87d9d8d
- Update to ose v3.4.0.34
  resolves: #1403892
- Add missing dependency of kube-proxy on conntrack-tools
  resolves: #1403196

* Tue Nov 01 2016 jchaloup <jchaloup@redhat.com> - 1.3.0-0.3.git86dc49a
- Update to ose v3.3.1.3
  resolves: #1390548

* Wed Sep 07 2016 jchaloup <jchaloup@redhat.com> - 1.3.0-0.2.gitc5ee292
- Fix permissions
  related: #1373884

* Wed Sep 07 2016 jchaloup <jchaloup@redhat.com> - 1.3.0-0.1.gitc5ee292
- Update to ose v3.3.0.30
  resolves: #1373884

* Wed Jul 13 2016 jchaloup <jchaloup@redhat.com> - 1.2.0-0.14.gitec7364b
- Own /run/kubernetes directory

* Mon Jul 11 2016 jchaloup <jchaloup@redhat.com> - 1.2.0-0.13.gitec7364b
- Update to ose v3.2.1.6
  Enable CPU and Memory accounting on a node
  resolves: #1354340

* Sun May 29 2016 jchaloup <jchaloup@redhat.com> - 1.2.0-0.12.gita4463d9
- Update to ose v3.2.0.44
  resolves: #1340646

* Tue Apr 19 2016 jchaloup <jchaloup@redhat.com> - 1.2.0-0.11.git738b760
- Set correct permissions for kubernetes-unit-test/docs/user-guide/ui.md (not shipped)
  related: #1327666

* Fri Apr 15 2016 jchaloup <jchaloup@redhat.com> - 1.2.0-0.10.gite88b10d
- Rebase to ose v3.2.0.16, kubernetes v1.2.0
  resolves: #1327666

* Tue Mar 08 2016 jchaloup <jchaloup@redhat.com> - 1.2.0-0.9.alpha1.gitb57e8bd
- hyperkube.server: don't parse args for any command
  related: #1314728

* Mon Mar 07 2016 jchaloup <jchaloup@redhat.com> - 1.2.0-0.8.alpha1.git8574601
- Rebase to ose 3.1.1.6
  related: #1314728

* Fri Mar 04 2016 jchaloup <jchaloup@redhat.com> - 1.2.0-0.7.alpha7.git8632732
- Bump to upstream 125f050150ef45b31e6b671d269bb69dc93541e5
  Disable extensions/v1beta1 implicitly
  resolves: #1314728

* Tue Jan 05 2016 jchaloup <jchaloup@redhat.com> - 1.2.0-0.6.alpha1.git8632732
- Move definition of all version, git and commit macros at one place

* Mon Jan 04 2016 jchaloup <jchaloup@redhat.com> - 1.2.0-0.5.alpha1.git8632732
- Set kube-apiserver's group to kube
  resolves: #1295545

* Mon Jan 04 2016 jchaloup <jchaloup@redhat.com> - 1.2.0-0.4.alpha1.git8632732
- Set kube-apiserver permission to 754

* Mon Jan 04 2016 jchaloup <jchaloup@redhat.com> - 1.2.0-0.3.alpha1.git8632732
- Fix rpmdiff complaint

* Tue Dec 01 2015 jchaloup <jchaloup@redhat.com> - 1.2.0-0.2.alpha1.git0e71938
- Build kubernetes from ose's Godeps using hack/build-go.sh
  ose's Godeps = kubernetes upstream + additional patches
- Build with debug info
- Use internal pod infrastructure container
- Set CAP_NET_BIND_SERVICE on the kube-apiserver so it can use 443, set 0 permission for others
- Rebase to ose-3.1.1.0 (19 Dec 2015)

* Thu Nov 05 2015 jchaloup <jchaloup@redhat.com> - 1.2.0-0.1.alpha1.git0e71938
- Rebase to ose 3.1.0.0
- Remove Ceph and FC volume patch as they are already merged in k8s tarball

* Fri Oct 23 2015 Colin Walters <walters@redhat.com> - 1.1.0-0.41.alpha1.git6de3e85
- Add patch to support FC volumes
  Resolves: #1274443

* Fri Oct 23 2015 Colin Walters <walters@redhat.com> - 1.1.0-0.40.alpha1.git6de3e85
- Add patch to drop dependency on Ceph server side
  Resolves: #1274421

* Mon Oct 12 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.39.alpha1.git6de3e85
- Add missing short option for --server of kubectl
- Update unit-test-subpackage (only test-cmd.sh atm)
  related: #1211266

* Fri Oct 09 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.38.alpha1.git6de3e85
- Add normalization of flags
  related: #1211266

* Wed Sep 30 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.37.alpha1.git5f38cb0
- Do not unset default cluster, otherwise k8s ends with error when no cluster set
- Built k8s from o7t/ose 6de3e8543699213f0cdb28032be82b4dae408dfe
  related: #1211266

* Wed Sep 30 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.36.alpha0.git5f38cb0
- Bump to o4n 5f38cb0e98c9e854cafba9c7f98dafd51e955ad8
  related: #1211266

* Tue Sep 29 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.35.alpha1.git2695cdc
- Update git version of k8s and o4n, add macros
  related: #1211266

* Tue Sep 29 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.34.alpha1.git2695cdc
- Built k8s from o4n tarball
- Bump to upstream 2695cdcd29a8f11ef60278758e11f4817daf3c7c
  related: #1211266

* Tue Sep 22 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.33.alpha1.git09cf38e
- Bump to upstream 09cf38e9a80327e2d41654db277d00f19e2c84d0
  related: #1211266

* Thu Sep 17 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.32.alpha1.git400e685
- Bump to upstream 400e6856b082ecf4b295568acda68d630fc000f1
  related: #1211266

* Wed Sep 16 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.31.gitd549fc4
- Bump to upstream d549fc400ac3e5901bd089b40168e1e6fb17341d
  related: #1211266

* Tue Sep 15 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.30.gitc9570e3
- Bump to upstream c9570e34d03c6700d83f796c0125d17c5064e57d
  related: #1211266

* Mon Sep 14 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.29.git86b4e77
- Bump to upstream 86b4e777e1947c1bc00e422306a3ca74cbd54dbe
  related: #1211266

* Thu Sep 10 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.28.gitf867ba3
- Bump to upstream f867ba3ba13e3dad422efd21c74f52b9762de37e
  related: #1211266

* Wed Sep 09 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.27.git0f4fa4e
- Bump to upstream 0f4fa4ed25ae9a9d1824fe55aeefb4d4ebfecdfd
  related: #1211266

* Tue Sep 08 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.26.git196f58b
- Bump to upstream 196f58b9cb25a2222c7f9aacd624737910b03acb
  related: #1211266

* Mon Sep 07 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.25.git96e0ed5
- Bump to upstream 96e0ed5749608d4cc32f61b3674deb04c8fa90ad
  related: #1211266

* Sat Sep 05 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.24.git2e2def3
- Bump to upstream 2e2def36a904fe9a197da5fc70e433e2e884442f
  related: #1211266

* Fri Sep 04 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.23.gite724a52
- Bump to upstream e724a5210adf717f62a72162621ace1e08730c75
  related: #1211266

* Thu Sep 03 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.22.gitb6f2f39
- Bump to upstream b6f2f396baec5105ff928cf61903c2c368259b21
  related: #1211266

* Wed Sep 02 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.21.gitb4a3698
- Bump to upstream b4a3698faed81410468eccf9f328ca6df3d0cca3
  related: #1211266

* Tue Sep 01 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.20.git2f9652c
- Bump to upstream 2f9652c7f1d4b8f333c0b5c8c1270db83b913436
  related: #1211266

* Mon Aug 31 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.19.git66a644b
- Bump to upstream 66a644b275ede9ddb98eb3f76e8d1840cafc2147
  related: #1211266

* Thu Aug 27 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.18.gitab73849
- Bump to upstream ab7384943748312f5e9294f42d42ed3983c7c96c
  related: #1211266

* Wed Aug 26 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.17.git00e3442
- Bump to upstream 00e34429e0242323ed34347cf0ab65b3d62b21f7
  related: #1211266

* Tue Aug 25 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.16.gita945785
- Bump to upstream a945785409d5b68f3a2721d2209300edb5abf1ce
  related: #1211266

* Mon Aug 24 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.15.git5fe7029
- Bump to upstream 5fe7029e688e1e5873a0b95a622edda5b5156d2b
  related: #1211266

* Fri Aug 21 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.14.gitb6f18c7
- Bump to upstream b6f18c7ce08714c8d4f6019463879a164a41750e
  related: #1211266

* Thu Aug 20 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.13.git44fa48e
- Bump to upstream 44fa48e5af44d3e988fa943d96a2de732d8cc666
  related: #1211266

* Wed Aug 19 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.12.gitb5a4a54
- Bump to upstream b5a4a548df0cffb99bdcc3b9b9e48d4025d0541c
  related: #1211266

* Tue Aug 18 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.11.git919c7e9
- Bump to upstream 919c7e94e23d2dcd5bdd96896e0a7990f9ae3338
  related: #1211266

* Tue Aug 18 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.10.git280b66c
- Bump to upstream 280b66c9012c21e253acd4e730f8684c39ca08ec
  related: #1211266

* Mon Aug 17 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.9.git081d9c6
- Bump to upstream 081d9c64d25c20ec16035036536511811118173d
  related: #1211266

* Fri Aug 14 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.8.git8dcbeba
- Bump to upstream 8dcbebae5ef6a7191d9dfb65c68833c6852a21ad
  related: #1211266

* Thu Aug 13 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.7.git968cbbe
- Bump to upstream 968cbbee5d4964bd916ba379904c469abb53d623
  related: #1211266

* Wed Aug 12 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.6.gitc91950f
- Bump to upstream c91950f01cb14ad47486dfcd2fdfb4be3ee7f36b
  related: #1211266

* Tue Aug 11 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.5.gite44c8e6
- Bump to upstream e44c8e6661c931f7fd434911b0d3bca140e1df3a
  related: #1211266

* Mon Aug 10 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.4.git2bfa9a1
- Bump to upstream 2bfa9a1f98147cfdc2e9f4cf50e2c430518d91eb
  related: #1243827

* Thu Aug 06 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.3.git4c42e13
- Bump to upstream 4c42e1302d3b351f3cb6074d32aa420bbd45e07d
- Change import path prefix to k8s.io/kubernetes
  related: #1243827

* Wed Aug 05 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.2.git159ba48
- Bump to upstream 159ba489329e9f6ce422541e13f97e1166090ec8
  related: #1243827

* Sat Aug 01 2015 jchaloup <jchaloup@redhat.com> - 1.1.0-0.1.git6129d3d
- Bump to upstream 6129d3d4eb80714286650818081a64ce2699afed
  related: #1243827

* Fri Jul 31 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.18.gitff058a1
- Bump to upstream ff058a1afeb63474f7a35805941f3b07c27aae0f
  related: #1243827

* Thu Jul 30 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.17.git769230e
- Bump to upstream 769230e735993bb0bf924279a40593c147c9a6ab
  related: #1243827

* Wed Jul 29 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.16.gitdde7222
- Bump to upstream dde72229dc9cbbdacfb2e44b22d9d5b357027020
  related: #1243827

* Tue Jul 28 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.15.gitc5bffaa
- Bump to upstream c5bffaaf3166513da6259c44a5d1ba8e86bea5ce
  related: #1243827

* Sat Jul 25 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.14.git5bd82ff
- Bump to upstream 5bd82ffe6da8f4e72e71b362635e558bfc412106
  related: #1243827

* Fri Jul 24 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.13.git291acd1
- Bump to upstream 291acd1a09ac836ec7524b060a19a6498d9878dd
  related: #1243827

* Thu Jul 23 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.12.gitfbed349
- Bump to upstream fbed3492bfa09e59b1c423fdd7c1ecad333a06ef
  related: #1243827

* Tue Jul 21 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.11.gitfbc85e9
- Add runtime dependency of kubernetes-node on socat (so kubectl port-forward works on AH)

* Tue Jul 21 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.10.gitfbc85e9
- Update the build script for go1.5 as well
- Bump to upstream fbc85e9838f25547be94fbffeeb92a756d908ca0
  related: #1243827

* Mon Jul 20 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.9.git2d88675
- Bump to upstream 2d88675f2203d316d4bac312c7ccad12991b56c2
- Change KUBE_ETCD_SERVERS to listen on 2379 ports instead of 4001
  resolves: #1243827
- Add kubernetes-client to provide kubectl command
  resolves: #1241469

* Mon Jul 20 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.8.gitb2dafda
- Fix dependency and tests for go-1.5
- with_debug off as the builds ends with error "ELFRESERVE too small: ..."

* Sat Jul 18 2015 Eric Paris <eparis@redhat.com> - 1.0.0-0.7.gitb2dafda
- Update apiserver binary gid

* Fri Jul 17 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.6.gitb2dafda
- Bump to upstream b2dafdaef5aceafad503ab56254b60f80da9e980
  related: #1211266

* Thu Jul 16 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.5.git596a8a4
- Bump to upstream 596a8a40d12498b5335140f50753980bfaea4f6b
  related: #1211266

* Wed Jul 15 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.4.git6ba532b
- Bump to upstream 6ba532b218cb5f5ea3f0e8dce5395182f388536c
  related: #1211266

* Tue Jul 14 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.3.gitc616182
- Bump to upstream c6161824db3784e6156131307a5e94647e5557fd
  related: #1211266

* Mon Jul 13 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.2.git2c27b1f
- Bump to upstream 2c27b1fa64f4e70f04575d1b217494f49332390e
  related: #1211266

* Sat Jul 11 2015 jchaloup <jchaloup@redhat.com> - 1.0.0-0.1.git1b37059
- Bump to upstream 1b370599ccf271741e657335c4943cb8c7dba28b
  related: #1211266

* Fri Jul 10 2015 jchaloup <jchaloup@redhat.com> - 0.21.1-0.2.gitccc4cfc
- Bump to upstream ccc4cfc7e11e0f127ac1cea045017dd799be3c63
  related: #1211266

* Thu Jul 09 2015 jchaloup <jchaloup@redhat.com> - 0.21.1-0.1.git41f8907
- Update generating of man pages from md (add genmanpages.sh)
- Bump to upstream 41f89075396329cd46c58495c7d3f7e13adcaa96
  related: #1211266

* Wed Jul 08 2015 jchaloup <jchaloup@redhat.com> - 0.20.2-0.5.git77be29e
- Bump to upstream 77be29e3da71f0a136b6aa4048b2f0575c2598e4
  related: #1211266

* Tue Jul 07 2015 jchaloup <jchaloup@redhat.com> - 0.20.2-0.4.git639a7da
- Bump to upstream 639a7dac50a331414cc6c47083323388da0d8756
  related: #1211266

* Mon Jul 06 2015 jchaloup <jchaloup@redhat.com> - 0.20.2-0.3.gitbb6f2f7
- Bump to upstream bb6f2f7ad90596d624d84cc691eec0f518e90cc8
  related: #1211266

* Fri Jul 03 2015 jchaloup <jchaloup@redhat.com> - 0.20.2-0.2.git974377b
- Bump to upstream 974377b3064ac59b6e5694bfa568d67128026171
  related: #1211266

* Thu Jul 02 2015 jchaloup <jchaloup@redhat.com> - 0.20.2-0.1.gitef41ceb
- Bump to upstream ef41ceb3e477ceada84c5522f429f02ab0f5948e
  related: #1211266

* Tue Jun 30 2015 jchaloup <jchaloup@redhat.com> - 0.20.0-0.3.git835eded
- Bump to upstream 835eded2943dfcf13a89518715e4be842a6a3ac0
- Generate missing man pages
  related: #1211266

* Mon Jun 29 2015 jchaloup <jchaloup@redhat.com> - 0.20.0-0.2.git1c0b765
- Bump to upstream 1c0b765df6dabfe9bd0e20489ed3bd18e6b3bda8
  Comment out missing man pages
  related: #1211266

* Fri Jun 26 2015 jchaloup <jchaloup@redhat.com> - 0.20.0-0.1.git8ebd896
- Bump to upstream 8ebd896351513d446d56bc5785c070d2909226a3
  related: #1211266

* Fri Jun 26 2015 jchaloup <jchaloup@redhat.com> - 0.19.3-0.6.git712f303
- Bump to upstream 712f303350b35e70a573f3cb19193c8ec7ee7544
  related: #1211266

* Thu Jun 25 2015 jchaloup <jchaloup@redhat.com> - 0.19.3-0.5.git2803b86
- Bump to upstream 2803b86a42bf187afa816a7ce14fec754cc2af51
  related: #1211266

* Wed Jun 24 2015 Eric Paris <eparis@redhat.com> - 0.19.3-0.4.git5b4dc4e
- Set CAP_NET_BIND_SERVICE on the kube-apiserver so it can use 443

* Wed Jun 24 2015 jchaloup <jchaloup@redhat.com> - 0.19.3-0.3.git5b4dc4e
- Bump to upstream 5b4dc4edaa14e1ab4e3baa19df0388fa54dab344
  pkg/cloudprovider/* packages does not conform to golang language specification
  related: #1211266

* Tue Jun 23 2015 jchaloup <jchaloup@redhat.com> - 0.19.3-0.2.gita2ce3ea
- Bump to upstream a2ce3ea5293553b1fe0db3cbc6d53bdafe061d79
  related: #1211266

* Mon Jun 22 2015 jchaloup <jchaloup@redhat.com> - 0.19.1-0.1.gitff0546d
- Bump to upstream ff0546da4fc23598de59db9f747c535545036463
  related: #1211266

* Fri Jun 19 2015 jchaloup <jchaloup@redhat.com> - 0.19.0-0.7.gitb2e9fed
- Bump to upstream b2e9fed3490274509506285bdba309c50afb5c39
  related: #1211266

* Thu Jun 18 2015 jchaloup <jchaloup@redhat.com> - 0.19.0-0.6.gitf660940
- Bump to upstream f660940dceb3fe6ffb1b14ba495a47d91b5cd910
  related: #1211266

* Wed Jun 17 2015 jchaloup <jchaloup@redhat.com> - 0.19.0-0.5.git43889c6
- Bump to upstream 43889c612c4d396dcd8fbf3fbd217e106eaf5bce
  related: #1211266

* Tue Jun 16 2015 jchaloup <jchaloup@redhat.com> - 0.19.0-0.4.gita8269e3
- Bump to upstream a8269e38c9e2bf81ba18cd6420e2309745d5b0b9
  related: #1211266

* Sun Jun 14 2015 jchaloup <jchaloup@redhat.com> - 0.19.0-0.3.git5e5c1d1
- Bump to upstream 5e5c1d10976f2f26d356ca60ef7d0d715c9f00a2
  related: #1211266

* Fri Jun 12 2015 jchaloup <jchaloup@redhat.com> - 0.19.0-0.2.git0ca96c3
- Bump to upstream 0ca96c3ac8b47114169f3b716ae4521ed8c7657c
  related: #1211266

* Thu Jun 11 2015 jchaloup <jchaloup@redhat.com> - 0.19.0-0.1.git5a02fc0
- Bump to upstream 5a02fc07d8a943132b9e68fe7169778253318487
  related: #1211266

* Wed Jun 10 2015 jchaloup <jchaloup@redhat.com> - 0.18.2-0.3.git0dfb681
- Bump to upstream 0dfb681ba5d5dba535895ace9d650667904b5df7
  related: #1211266

* Tue Jun 09 2015 jchaloup <jchaloup@redhat.com> - 0.18.2-0.2.gitb68e08f
- golang-cover is not needed

* Tue Jun 09 2015 jchaloup <jchaloup@redhat.com> - 0.18.2-0.1.gitb68e08f
- Bump to upstream b68e08f55f5ae566c4ea3905d0993a8735d6d34f
  related: #1211266

* Sat Jun 06 2015 jchaloup <jchaloup@redhat.com> - 0.18.1-0.3.git0f1c4c2
- Bump to upstream 0f1c4c25c344f70c3592040b2ef092ccdce0244f
  related: #1211266

* Fri Jun 05 2015 jchaloup <jchaloup@redhat.com> - 0.18.1-0.2.git7309e1f
- Bump to upstream 7309e1f707ea5dd08c51f803037d7d22c20e2b92
  related: #1211266

* Thu Jun 04 2015 jchaloup <jchaloup@redhat.com> - 0.18.1-0.1.gita161edb
- Bump to upstream a161edb3960c01ff6e14813858c2eeb85910009b
  related: #1211266

* Wed Jun 03 2015 jchaloup <jchaloup@redhat.com> - 0.18.0-0.3.gitb5a91bd
- Bump to upstream b5a91bda103ed2459f933959241a2b57331747ba
- Don't run %check section (kept only for local run). Tests are now handled via CI.
  related: #1211266

* Tue Jun 02 2015 jchaloup <jchaloup@redhat.com> - 0.18.0-0.2.git5520386
- Bump to upstream 5520386b180d3ddc4fa7b7dfe6f52642cc0c25f3
  related: #1211266

* Mon Jun 01 2015 jchaloup <jchaloup@redhat.com> - 0.18.0-0.1.git0bb78fe
- Bump to upstream 0bb78fe6c53ce38198cc3805c78308cdd4805ac8
  related: #1211266

* Fri May 29 2015 jchaloup <jchaloup@redhat.com> - 0.17.1-6
- Bump to upstream ed4898d98c46869e9cbdb44186dfdeda9ff80cc2
  related: #1211266

* Thu May 28 2015 jchaloup <jchaloup@redhat.com> - 0.17.1-5
- Bump to upstream 6fa2777e26559fc008eacac83eb165d25bd9a7de
  related: #1211266

* Tue May 26 2015 jchaloup <jchaloup@redhat.com> - 0.17.1-4
- Bump to upstream 01fcb58673001e56c69e128ab57e0c3f701aeea5
  related: #1211266

* Mon May 25 2015 jchaloup <jchaloup@redhat.com> - 0.17.1-3
- Decompose package into master and node subpackage.
  Thanks to Avesh for testing and patience.
  related: #1211266

* Mon May 25 2015 jchaloup <jchaloup@redhat.com> - 0.17.1-2
- Bump to upstream cf7b0bdc2a41d38613ac7f8eeea91cae23553fa2
  related: #1211266

* Fri May 22 2015 jchaloup <jchaloup@redhat.com> - 0.17.1-1
- Bump to upstream d9d12fd3f7036c92606fc3ba9046b365212fcd70
  related: #1211266

* Wed May 20 2015 jchaloup <jchaloup@redhat.com> - 0.17.0-12
- Bump to upstream a76bdd97100c66a46e2b49288540dcec58a954c4
  related: #1211266

* Tue May 19 2015 jchaloup <jchaloup@redhat.com> - 0.17.0-11
- Bump to upstream 10339d72b66a31592f73797a9983e7c207481b22
  related: #1211266

* Mon May 18 2015 jchaloup <jchaloup@redhat.com> - 0.17.0-10
- Bump to upstream efb42b302d871f7217394205d84e5ae82335d786
  related: #1211266

* Sat May 16 2015 jchaloup <jchaloup@redhat.com> - 0.17.0-9
- Bump to upstream d51e131726b925e7088b90915e99042459b628e0
  related: #1211266

* Fri May 15 2015 jchaloup <jchaloup@redhat.com> - 0.17.0-8
- Bump to upstream 1ee33ac481a14db7b90e3bbac8cec4ceea822bfb
  related: #1211266

* Fri May 15 2015 jchaloup <jchaloup@redhat.com> - 0.17.0-7
- Bump to upstream d3c6fb0d6a13c0177dcd67556d72963c959234ea
  related: #1211266

* Fri May 15 2015 jchaloup <jchaloup@redhat.com> - 0.17.0-6
- Bump to upstream f57f31783089f41c0bdca8cb87a1001ca94e1a45
  related: #1211266

* Thu May 14 2015 jchaloup <jchaloup@redhat.com> - 0.17.0-5
- Bump to upstream c90d381d0d5cf8ab7b8412106f5a6991d7e13c7d
  related: #1211266

* Thu May 14 2015 jchaloup <jchaloup@redhat.com> - 0.17.0-4
- Bump to upstream 5010b2dde0f9b9eb820fe047e3b34bc9fa6324de
- Add debug info
  related: #1211266

* Wed May 13 2015 jchaloup <jchaloup@redhat.com> - 0.17.0-3
- Bump to upstream ec19d41b63f5fe7b2c939e7738a41c0fbe65d796
  related: #1211266

* Tue May 12 2015 jchaloup <jchaloup@redhat.com> - 0.17.0-2
- Provide /usr/bin/kube-version-change binary
  related: #1211266

* Tue May 12 2015 jchaloup <jchaloup@redhat.com> - 0.17.0-1
- Bump to upstream 962f10ee580eea30e5f4ea725c4e9e3743408a58
  related: #1211266

* Mon May 11 2015 jchaloup <jchaloup@redhat.com> - 0.16.2-7
- Bump to upstream 63182318c5876b94ac9b264d1224813b2b2ab541
  related: #1211266

* Fri May 08 2015 jchaloup <jchaloup@redhat.com> - 0.16.2-6
- Bump to upstream d136728df7e2694df9e082902f6239c11b0f2b00
- Add NetworkManager as dependency for /etc/resolv.conf
  related: #1211266

* Thu May 07 2015 jchaloup <jchaloup@redhat.com> - 0.16.2-5
- Bump to upstream ca0f678b9a0a6dc795ac7a595350d0dbe9d0ac3b
  related: #1211266

* Wed May 06 2015 jchaloup <jchaloup@redhat.com> - 0.16.2-4
- Add docs to kubernetes-unit-test
  related: #1211266

* Wed May 06 2015 jchaloup <jchaloup@redhat.com> - 0.16.2-3
- Bump to upstream 3a24c0e898cb3060d7905af6df275a3be562451d
  related: #1211266

* Tue May 05 2015 jchaloup <jchaloup@redhat.com> - 0.16.2-2
- Add api and README.md to kubernetes-unit-test
  related: #1211266

* Tue May 05 2015 jchaloup <jchaloup@redhat.com> - 0.16.2-1
- Bump to upstream 72048a824ca16c3921354197953fabecede5af47
  related: #1211266

* Mon May 04 2015 jchaloup <jchaloup@redhat.com> - 0.16.1-2
- Bump to upstream 1dcd80cdf3f00409d55cea1ef0e7faef0ae1d656
  related: #1211266

* Sun May 03 2015 jchaloup <jchaloup@redhat.com> - 0.16.1-1
- Bump to upstream 86751e8c90a3c0e852afb78d26cb6ba8cdbc37ba
  related: #1211266

* Fri May 01 2015 jchaloup <jchaloup@redhat.com> - 0.16.0-2
- Bump to upstream 72708d74b9801989ddbdc8403fc5ba4aafb7c1ef
  related: #1211266

* Wed Apr 29 2015 jchaloup <jchaloup@redhat.com> - 0.16.0-1
- Bump to upstream 7dcce2eeb7f28643d599c8b6a244523670d17c93
  related: #1211266

* Tue Apr 28 2015 jchaloup <jchaloup@redhat.com> - 0.15.0-10
- Add unit-test subpackage
  related: #1211266

* Tue Apr 28 2015 jchaloup <jchaloup@redhat.com> - 0.15.0-9
- Bump to upstream 99fc906f78cd2bcb08536c262867fa6803f816d5
  related: #1211266

* Mon Apr 27 2015 jchaloup <jchaloup@redhat.com> - 0.15.0-8
- Bump to upstream 051dd96c542799dfab39184d2a7c8bacf9e88d85
  related: #1211266

* Fri Apr 24 2015 jchaloup <jchaloup@redhat.com> - 0.15.0-7
- Bump to upstream 9f753c2592481a226d72cea91648db8fb97f0da8
  related: #1211266

* Thu Apr 23 2015 jchaloup <jchaloup@redhat.com> - 0.15.0-6
- Bump to upstream cf824ae5e07965ba0b4b15ee88e08e2679f36978
  related: #1211266

* Tue Apr 21 2015 jchaloup <jchaloup@redhat.com> - 0.15.0-5
- Bump to upstream 21788d8e6606038a0a465c97f5240b4e66970fbb
  related: #1211266

* Mon Apr 20 2015 jchaloup <jchaloup@redhat.com> - 0.15.0-4
- Bump to upstream eb1ea269954da2ce557f3305fa88d42e3ade7975
  related: #1211266

* Fri Apr 17 2015 jchaloup <jchaloup@redhat.com> - 0.15.0-3
- Obsolete cadvisor as it is integrated in kubelet
  related: #1211266

* Wed Apr 15 2015 jchaloup <jchaloup@redhat.com> - 0.15.0-0.2.git0ea87e4
- Bump to upstream 0ea87e486407298dc1e3126c47f4076b9022fb09
  related: #1211266

* Tue Apr 14 2015 jchaloup <jchaloup@redhat.com> - 0.15.0-0.1.gitd02139d
- Bump to upstream d02139d2b454ecc5730cc535d415c1963a7fb2aa
  related: #1211266

* Sun Apr 12 2015 jchaloup <jchaloup@redhat.com> - 0.14.2-0.2.gitd577db9
- Bump to upstream d577db99873cbf04b8e17b78f17ec8f3a27eca30

* Wed Apr 08 2015 jchaloup <jchaloup@redhat.com> - 0.14.2-0.1.git2719194
- Bump to upstream 2719194154ffd38fd1613699a9dd10a00909957e
  Use etcd-2.0.8 and higher

* Tue Apr 07 2015 jchaloup <jchaloup@redhat.com> - 0.14.1-0.2.gitd2f4734
- Bump to upstream d2f473465738e6b6f7935aa704319577f5e890ba

* Thu Apr 02 2015 jchaloup <jchaloup@redhat.com> - 0.14.1-0.1.gita94ffc8
- Bump to upstream a94ffc8625beb5e2a39edb01edc839cb8e59c444

* Wed Apr 01 2015 jchaloup <jchaloup@redhat.com> - 0.14.0-0.2.git8168344
- Bump to upstream 81683441b96537d4b51d146e39929b7003401cd5

* Tue Mar 31 2015 jchaloup <jchaloup@redhat.com> - 0.14.0-0.1.git9ed8761
- Bump to upstream 9ed87612d07f75143ac96ad90ff1ff68f13a2c67
- Remove [B]R from devel branch until the package has stable API

* Mon Mar 30 2015 jchaloup <jchaloup@redhat.com> - 0.13.2-0.6.git8a7a127
- Bump to upstream 8a7a127352263439e22253a58628d37a93fdaeb2

* Fri Mar 27 2015 jchaloup <jchaloup@redhat.com> - 0.13.2-0.5.git8d94c43
- Bump to upstream 8d94c43e705824f23791b66ad5de4ea095d5bb32
  resolves: #1205362

* Wed Mar 25 2015 jchaloup <jchaloup@redhat.com> - 0.13.2-0.4.git455fe82
- Bump to upstream 455fe8235be8fd9ba0ce21bf4f50a69d42e18693

* Mon Mar 23 2015 jchaloup <jchaloup@redhat.com> - 0.13.2-0.3.gitef75888
- Remove runtime dependency on etcd
  resolves: #1202923

* Sun Mar 22 2015 jchaloup <jchaloup@redhat.com> - 0.13.2-0.2.gitef75888
- Bump to upstream ef758881d108bb53a128126c503689104d17f477

* Fri Mar 20 2015 jchaloup <jchaloup@redhat.com> - 0.13.2-0.1.gita8f2cee
- Bump to upstream a8f2cee8c5418676ee33a311fad57d6821d3d29a

* Fri Mar 13 2015 jchaloup <jchaloup@redhat.com> - 0.12.0-0.9.git53b25a7
- Bump to upstream 53b25a7890e31bdec6f2a95b32200d6cc27ae2ca
  fix kube-proxy.service and kubelet
  resolves: #1200919 #1200924

* Fri Mar 13 2015 jchaloup <jchaloup@redhat.com> - 0.12.0-0.8.git39dceb1
- Bump to upstream 39dceb13a511a83963a766a439cb386d10764310

* Thu Mar 12 2015 Eric Paris <eparis@redhat.com> - 0.12.0-0.7.gita3fd0a9
- Move from /etc/tmpfiles.d to %{_tmpfilesdir}
  resolves: #1200969

* Thu Mar 12 2015 jchaloup <jchaloup@redhat.com> - 0.12.0-0.6.gita3fd0a9
- Place contrib/init/systemd/tmpfiles.d/kubernetes.conf to /etc/tmpfiles.d/kubernetes.conf

* Thu Mar 12 2015 jchaloup <jchaloup@redhat.com> - 0.12.0-0.5.gita3fd0a9
- Bump to upstream a3fd0a9fd516bb6033f32196ae97aaecf8c096b1

* Tue Mar 10 2015 jchaloup <jchaloup@redhat.com> - 0.12.0-0.4.gita4d871a
- Bump to upstream a4d871a10086436557f804930812f2566c9d4d39

* Fri Mar 06 2015 jchaloup <jchaloup@redhat.com> - 0.12.0-0.3.git2700871
- Bump to upstream 2700871b049d5498167671cea6de8317099ad406

* Thu Mar 05 2015 jchaloup <jchaloup@redhat.com> - 0.12.0-0.2.git8b627f5
- Bump to upstream 8b627f516fd3e4f62da90d401ceb3d38de6f8077

* Tue Mar 03 2015 jchaloup <jchaloup@redhat.com> - 0.12.0-0.1.gitecca426
- Bump to upstream ecca42643b91a7117de8cd385b64e6bafecefd65

* Mon Mar 02 2015 jchaloup <jchaloup@redhat.com> - 0.11.0-0.5.git6c5b390
- Bump to upstream 6c5b390160856cd8334043344ef6e08568b0a5c9

* Sat Feb 28 2015 jchaloup <jchaloup@redhat.com> - 0.11.0-0.4.git0fec31a
- Bump to upstream 0fec31a11edff14715a1efb27f77262a7c3770f4

* Fri Feb 27 2015 jchaloup <jchaloup@redhat.com> - 0.11.0-0.3.git08402d7
- Bump to upstream 08402d798c8f207a2e093de5a670c5e8e673e2de

* Wed Feb 25 2015 jchaloup <jchaloup@redhat.com> - 0.11.0-0.2.git86434b4
- Bump to upstream 86434b4038ab87ac40219562ad420c3cc58c7c6b

* Tue Feb 24 2015 jchaloup <jchaloup@redhat.com> - 0.11.0-0.1.git754a2a8
- Bump to upstream 754a2a8305c812121c3845d8293efdd819b6a704
  turn off integration tests until "FAILED: unexpected endpoints:
  timed out waiting for the condition" problem is resolved
  Adding back devel subpackage ([B]R list outdated)

* Fri Feb 20 2015 jchaloup <jchaloup@redhat.com> - 0.10.1-0.3.git4c87805
- Bump to upstream 4c87805870b1b22e463c4bd711238ef68c77f0af

* Tue Feb 17 2015 jchaloup <jchaloup@redhat.com> - 0.10.1-0.2.git6f84bda
- Bump to upstream 6f84bdaba853872dbac69c84d3ab4b6964e85d8c

* Tue Feb 17 2015 jchaloup <jchaloup@redhat.com> - 0.10.1-0.1.git7d6130e
- Bump to upstream 7d6130edcdfabd7dd2e6a06fdc8fe5e333f07f5c

* Sat Feb 07 2015 jchaloup <jchaloup@redhat.com> - 0.9.1-0.7.gitc9c98ab
- Bump to upstream c9c98ab19eaa6f0b2ea17152c9a455338853f4d0
  Since some dependencies are broken, we can not build Kubernetes from Fedora deps.
  Switching to vendored source codes until Go draft is resolved

* Wed Feb 04 2015 jchaloup <jchaloup@redhat.com> - 0.9.1-0.6.git7f5ed54
- Bump to upstream 7f5ed541f794348ae6279414cf70523a4d5133cc

* Tue Feb 03 2015 jchaloup <jchaloup@redhat.com> - 0.9.1-0.5.git2ac6bbb
- Bump to upstream 2ac6bbb7eba7e69eac71bd9acd192cda97e67641

* Mon Feb 02 2015 jchaloup <jchaloup@redhat.com> - 0.9.1-0.4.gite335e2d
- Bump to upstream e335e2d3e26a9a58d3b189ccf41ceb3770d1bfa9

* Fri Jan 30 2015 jchaloup <jchaloup@redhat.com> - 0.9.1-0.3.git55793ac
- Bump to upstream 55793ac2066745f7243c666316499e1a8cf074f0

* Thu Jan 29 2015 jchaloup <jchaloup@redhat.com> - 0.9.1-0.2.gitca6de16
- Bump to upstream ca6de16df7762d4fc9b4ad44baa78d22e3f30742

* Tue Jan 27 2015 jchaloup <jchaloup@redhat.com> - 0.9.1-0.1.git3623a01
- Bump to upstream 3623a01bf0e90de6345147eef62894057fe04b29
- update tests for etcd-2.0

* Thu Jan 22 2015 jchaloup <jchaloup@redhat.com> - 0.8.2-571.gitb2f287c
+- Bump to upstream b2f287c259d856f4c08052a51cd7772c563aff77

* Thu Jan 22 2015 Eric Paris <eparis@redhat.com> - 0.8.2-570.gitb2f287c
- patch kubelet service file to use docker.service not docker.socket

* Wed Jan 21 2015 jchaloup <jchaloup@redhat.com> - 0.8.2-0.1.git5b04640
- Bump to upstream 5b046406a957a1e7eda7c0c86dd7a89e9c94fc5f

* Sun Jan 18 2015 jchaloup <jchaloup@redhat.com> - 0.8.0-126.0.git68298f0
- Add some missing dependencies
- Add devel subpackage

* Fri Jan 09 2015 Eric Paris <eparis@redhat.com> - 0.8.0-125.0.git68298f0
- Bump to upstream 68298f08a4980f95dfbf7b9f58bfec1808fb2670

* Tue Dec 16 2014 Eric Paris <eparis@redhat.com> - 0.7.0-18.0.git52e165a
- Bump to upstream 52e165a4fd720d1703ebc31bd6660e01334227b8

* Mon Dec 15 2014 Eric Paris <eparis@redhat.com> - 0.6-297.0.git5ef34bf
- Bump to upstream 5ef34bf52311901b997119cc49eff944c610081b

* Wed Dec 03 2014 Eric Paris <eparis@redhat.com>
- Replace patch to use old googlecode/go.net/ with BuildRequires on golang.org/x/net/

* Tue Dec 02 2014 Eric Paris <eparis@redhat.com> - 0.6-4.0.git993ef88
- Bump to upstream 993ef88eec9012b221f79abe8f2932ee97997d28

* Mon Dec 01 2014 Eric Paris <eparis@redhat.com> - 0.5-235.0.git6aabd98
- Bump to upstream 6aabd9804fb75764b70e9172774002d4febcae34

* Wed Nov 26 2014 Eric Paris <eparis@redhat.com> - 0.5-210.0.gitff1e9f4
- Bump to upstream ff1e9f4c191342c24974c030e82aceaff8ea9c24

* Tue Nov 25 2014 Eric Paris <eparis@redhat.com> - 0.5-174.0.git64e07f7
- Bump to upstream 64e07f7fe03d8692c685b09770c45f364967a119

* Mon Nov 24 2014 Eric Paris <eparis@redhat.com> - 0.5-125.0.git162e498
- Bump to upstream 162e4983b947d2f6f858ca7607869d70627f5dff

* Fri Nov 21 2014 Eric Paris <eparis@redhat.com> - 0.5-105.0.git3f74a1e
- Bump to upstream 3f74a1e9f56b3c3502762930c0c551ccab0557ea

* Thu Nov 20 2014 Eric Paris <eparis@redhat.com> - 0.5-65.0.gitc6158b8
- Bump to upstream c6158b8aa9c40fbf1732650a8611429536466b21
- include go-restful build requirement

* Tue Nov 18 2014 Eric Paris <eparis@redhat.com> - 0.5-14.0.gitdf0981b
- Bump to upstream df0981bc01c5782ad30fc45cb6f510f365737fc1

* Tue Nov 11 2014 Eric Paris <eparis@redhat.com> - 0.4-680.0.git30fcf24
- Bump to upstream 30fcf241312f6d0767c7d9305b4c462f1655f790

* Mon Nov 10 2014 Eric Paris <eparis@redhat.com> - 0.4-633.0.git6c70227
- Bump to upstream 6c70227a2eccc23966d32ea6d558ee05df46e400

* Fri Nov 07 2014 Eric Paris <eparis@redhat.com> - 0.4-595.0.gitb695650
- Bump to upstream b6956506fa2682afa93770a58ea8c7ba4b4caec1

* Thu Nov 06 2014 Eric Paris <eparis@redhat.com> - 0.4-567.0.git3b1ef73
- Bump to upstream 3b1ef739d1fb32a822a22216fb965e22cdd28e7f

* Thu Nov 06 2014 Eric Paris <eparis@redhat.com> - 0.4-561.0.git06633bf
- Bump to upstream 06633bf4cdc1ebd4fc848f85025e14a794b017b4
- Make spec file more RHEL/CentOS friendly

* Tue Nov 04 2014 Eric Paris <eparis@redhat.com - 0.4-510.0.git5a649f2
- Bump to upstream 5a649f2b9360a756fc8124897d3453a5fa9473a6

* Mon Nov 03 2014 Eric Paris <eparis@redhat.com - 0.4-477.0.gita4abafe
- Bump to upstream a4abafea02babc529c9b5b9c825ba0bb3eec74c6

* Mon Nov 03 2014 Eric Paris <eparis@redhat.com - 0.4-453.0.git808be2d
- Bump to upstream 808be2d13b7bf14a3cf6985bc7c9d02f48a3d1e0
- Includes upstream change to remove --machines from the APIServer
- Port to new build system
- Start running %check tests again

* Fri Oct 31 2014 Eric Paris <eparis@redhat.com - 0.4+-426.0.gita18cdac
- Bump to upstream a18cdac616962a2c486feb22afa3538fc3cf3a3a

* Thu Oct 30 2014 Eric Paris <eparis@redhat.com - 0.4+-397.0.git78df011
- Bump to upstream 78df01172af5cc132b7276afb668d31e91e61c11

* Wed Oct 29 2014 Eric Paris <eparis@redhat.com - 0.4+-0.9.git8e1d416
- Bump to upstream 8e1d41670783cb75cf0c5088f199961a7d8e05e5

* Tue Oct 28 2014 Eric Paris <eparis@redhat.com - 0.4-0.8.git1c61486
- Bump to upstream 1c61486ec343246a81f62b4297671217c9576df7

* Mon Oct 27 2014 Eric Paris <eparis@redhat.com - 0.4-0.7.gitdc7e3d6
- Bump to upstream dc7e3d6601a89e9017ca9db42c09fd0ecb36bb36

* Fri Oct 24 2014 Eric Paris <eparis@redhat.com - 0.4-0.6.gite46af6e
- Bump to upstream e46af6e37f6e6965a63edb8eb8f115ae8ef41482

* Thu Oct 23 2014 Eric Paris <eparis@redhat.com - 0.4-0.5.git77d2815
- Bump to upstream 77d2815b86e9581393d7de4379759c536df89edc

* Wed Oct 22 2014 Eric Paris <eparis@redhat.com - 0.4-0.4.git97dd730
- Bump to upstream 97dd7302ac2c2b9458a9348462a614ebf394b1ed
- Use upstream kubectl bash completion instead of in-repo
- Fix systemd_post and systemd_preun since we are using upstream service files

* Tue Oct 21 2014 Eric Paris <eparis@redhat.com - 0.4-0.3.gite868642
- Bump to upstream e8686429c4aa63fc73401259c8818da168a7b85e

* Mon Oct 20 2014 Eric Paris <eparis@redhat.com - 0.4-0.2.gitd5377e4
- Bump to upstream d5377e4a394b4fc6e3088634729b538eac124b1b
- Use in tree systemd unit and Environment files
- Include kubectl bash completion from outside tree

* Fri Oct 17 2014 Eric Paris <eparis@redhat.com - 0.4-0.1.gitb011263
- Bump to upstream b01126322b826a15db06f6eeefeeb56dc06db7af
- This is a major non backward compatible change.

* Thu Oct 16 2014 Eric Paris <eparis@redhat.com> - 0.4-0.0.git4452163
- rebase to v0.4
- include man pages

* Tue Oct 14 2014 jchaloup <jchaloup@redhat.com> - 0.3-0.3.git98ac8e1
- create /var/lib/kubelet
- Use bash completions from upstream
- Bump to upstream 98ac8e178fcf1627399d659889bcb5fe25abdca4
- all by Eric Paris

* Mon Sep 29 2014 Jan Chaloupka <jchaloup@redhat.com> - 0.3-0.2.git88fdb65
- replace * with coresponding files
- remove dependency on gcc

* Wed Sep 24 2014 Eric Paris <eparis@redhat.com - 0.3-0.1.git88fdb65
- Bump to upstream 88fdb659bc44cf2d1895c03f8838d36f4d890796

* Tue Sep 23 2014 Eric Paris <eparis@redhat.com - 0.3-0.0.gitbab5082
- Bump to upstream bab5082a852218bb65aaacb91bdf599f9dd1b3ac

* Fri Sep 19 2014 Eric Paris <eparis@redhat.com - 0.2-0.10.git06316f4
- Bump to upstream 06316f486127697d5c2f5f4c82963dec272926cf

* Thu Sep 18 2014 Eric Paris <eparis@redhat.com - 0.2-0.9.gitf7a5ec3
- Bump to upstream f7a5ec3c36bd40cc2216c1da331ab647733769dd

* Wed Sep 17 2014 Eric Paris <eparis@redhat.com - 0.2-0.8.gitac8ee45
- Try to intelligently determine the deps

* Wed Sep 17 2014 Eric Paris <eparis@redhat.com - 0.2-0.7.gitac8ee45
- Bump to upstream ac8ee45f4fc4579b3ed65faafa618de9c0f8fb26

* Mon Sep 15 2014 Eric Paris <eparis@redhat.com - 0.2-0.5.git24b5b7e
- Bump to upstream 24b5b7e8d3a8af1eecf4db40c204e3c15ae955ba

* Thu Sep 11 2014 Eric Paris <eparis@redhat.com - 0.2-0.3.gitcc7999c
- Bump to upstream cc7999c00a40df21bd3b5e85ecea3b817377b231

* Wed Sep 10 2014 Eric Paris <eparis@redhat.com - 0.2-0.2.git60d4770
- Add bash completions

* Wed Sep 10 2014 Eric Paris <eparis@redhat.com - 0.2-0.1.git60d4770
- Bump to upstream 60d4770127d22e51c53e74ca94c3639702924bd2

* Mon Sep 08 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-0.4.git6ebe69a
- prefer autosetup instead of setup (revert setup change in 0-0.3.git)
https://fedoraproject.org/wiki/Autosetup_packaging_draft
- revert version number to 0.1

* Mon Sep 08 2014 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.3.git6ebe69a
- gopath defined in golang package already
- package owns /etc/kubernetes
- bash dependency implicit
- keep buildroot/$RPM_BUILD_ROOT macros consistent
- replace with macros wherever possible
- set version, release and source tarball prep as per
https://fedoraproject.org/wiki/Packaging:SourceURL#Github

* Mon Sep 08 2014 Eric Paris <eparis@redhat.com>
- make services restart automatically on error

* Sat Sep 06 2014 Eric Paris <eparis@redhat.com - 0.1-0.1.0.git6ebe69a8
- Bump to upstream 6ebe69a8751508c11d0db4dceb8ecab0c2c7314a

* Wed Aug 13 2014 Eric Paris <eparis@redhat.com>
- update to upstream
- redo build to use project scripts
- use project scripts in %check
- rework deletion of third_party packages to easily detect changes
- run apiserver and controller-manager as non-root

* Mon Aug 11 2014 Adam Miller <maxamillion@redhat.com>
- update to upstream
- decouple the rest of third_party

* Thu Aug 7 2014 Eric Paris <eparis@redhat.com>
- update to head
- update package to include config files

* Wed Jul 16 2014 Colin Walters <walters@redhat.com>
- Initial package
