%global debug_package %{nil}

Name:           ro-asd-repos
Version:        0.1.2
Release:        1%{?dist}
Summary:        Ro-ASD DNF repository definitions

License:        GPL-3.0-only
URL:            https://github.com/Project-Ro-ASD/Ro-ASD-release
Source0:        %{name}-%{version}.tar.gz

BuildArch:      x86_64
ExclusiveArch:  x86_64
Requires:       ro-asd-keyring >= 0.1.0

%description
DNF repository definitions for Ro-ASD Fedora 44 x86_64. The active beta
repository uses R2 and keeps signed RPM and metadata verification enabled.
The legacy beta remains available as an explicit recovery repository.

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
* Thu Nov 19 2026 Project Ro-ASD <dev@ro-asd.invalid> - 0.1.2-1
- Migrate Fedora 44 x86_64 beta clients to the signed R2 channel
* Fri Oct 09 2026 Project Ro-ASD <dev@ro-asd.invalid> - 0.1.1-1
- Prefer Ro-ASD binary repositories for reviewed Fedora package overrides
* Wed Sep 23 2026 Project Ro-ASD <dev@ro-asd.invalid> - 0.1.0-1
- Add signed Ro-ASD beta and stable DNF repository definitions
