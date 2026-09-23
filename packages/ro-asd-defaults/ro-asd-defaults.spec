Name:           ro-asd-defaults
Version:        0.1.0
Release:        1%{?dist}
Summary:        Ro-ASD distribution defaults policy contract

License:        GPL-3.0-only
URL:            https://github.com/Project-Ro-ASD/Ro-ASD-release
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Machine-readable ownership and safety policy for Ro-ASD distribution defaults.
The initial version intentionally changes no user or desktop configuration.

%prep
%autosetup

%build

%install
install -Dpm 0644 defaults-policy-v1.json \
  %{buildroot}%{_datadir}/ro-asd/defaults/defaults-policy-v1.json

%files
%license LICENSE
%doc README.md DEFAULTS-OWNERSHIP-V1.md
%dir %{_datadir}/ro-asd
%dir %{_datadir}/ro-asd/defaults
%{_datadir}/ro-asd/defaults/defaults-policy-v1.json

%changelog
* Wed Sep 23 2026 Project Ro-ASD <contact@roasd.org> - 0.1.0-1
- Establish the Ro-ASD defaults ownership and safety contract
