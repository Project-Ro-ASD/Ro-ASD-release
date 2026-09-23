Name:           ro-asd-repos
Version:        0.1.0
Release:        1%{?dist}
Summary:        Ro-ASD DNF repository definitions

License:        GPL-3.0-only
URL:            https://github.com/Project-Ro-ASD/Ro-ASD-release
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
Requires:       ro-asd-keyring >= 0.1.0

%description
DNF repository definitions for Ro-ASD Fedora 44 beta and stable channels.
Repository metadata and RPM signature verification are enabled. The initial
0.1.0 package enables beta because no public stable channel exists yet.

%prep
%autosetup

%build

%install
install -Dpm 0644 ro-asd.repo \
  %{buildroot}%{_sysconfdir}/yum.repos.d/ro-asd.repo

%files
%license LICENSE
%doc README.md
%config(noreplace) %{_sysconfdir}/yum.repos.d/ro-asd.repo

%changelog
* Wed Sep 23 2026 Project Ro-ASD <dev@ro-asd.invalid> - 0.1.0-1
- Add signed Ro-ASD beta and stable DNF repository definitions
