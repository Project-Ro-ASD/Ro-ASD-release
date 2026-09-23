Name:           ro-asd-branding
Version:        0.1.0
Release:        1%{?dist}
Summary:        Ro-ASD branding ownership contract

License:        GPL-3.0-only
URL:            https://github.com/Project-Ro-ASD/Ro-ASD-release
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Machine-readable ownership and safety contract for Ro-ASD distribution
branding. The initial version intentionally replaces no Fedora identity files.

%prep
%autosetup

%build

%install
install -Dpm 0644 branding-contract-v1.json \
  %{buildroot}%{_datadir}/ro-asd/branding/branding-contract-v1.json

%files
%license LICENSE
%doc README.md BRANDING-CONTRACT-V1.md
%dir %{_datadir}/ro-asd
%dir %{_datadir}/ro-asd/branding
%{_datadir}/ro-asd/branding/branding-contract-v1.json

%changelog
* Wed Sep 23 2026 Project Ro-ASD <contact@roasd.org> - 0.1.0-1
- Establish the Ro-ASD branding ownership and safety contract
