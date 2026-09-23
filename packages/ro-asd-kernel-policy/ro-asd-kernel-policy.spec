Name:           ro-asd-kernel-policy
Version:        0.1.0
Release:        1%{?dist}
Summary:        Ro-ASD kernel lifecycle policy contract

License:        GPL-3.0-only
URL:            https://github.com/Project-Ro-ASD/Ro-ASD-release
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Machine-readable kernel lifecycle, ownership and safety contract for Ro-ASD.
The initial release intentionally installs, removes, selects, excludes or
configures no kernel package.

%prep
%autosetup

%build

%install
install -Dpm 0644 kernel-policy-v1.json \
  %{buildroot}%{_datadir}/ro-asd/kernel/kernel-policy-v1.json

%files
%license LICENSE
%doc README.md KERNEL-POLICY-V1.md
%dir %{_datadir}/ro-asd
%dir %{_datadir}/ro-asd/kernel
%{_datadir}/ro-asd/kernel/kernel-policy-v1.json

%changelog
* Wed Sep 23 2026 Project Ro-ASD <contact@roasd.org> - 0.1.0-1
- Establish the Ro-ASD kernel lifecycle and safety contract
