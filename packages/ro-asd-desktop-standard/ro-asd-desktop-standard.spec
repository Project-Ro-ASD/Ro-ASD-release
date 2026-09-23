Name:           ro-asd-desktop-standard
Version:        0.1.0
Release:        1%{?dist}
Summary:        Ro-ASD standard desktop profile meta-package

License:        GPL-3.0-only
URL:            https://github.com/Project-Ro-ASD/Ro-ASD-release
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

Requires:       ro-asd-release >= 0.1.2
Requires:       ro-asd-keyring >= 0.1.0
Requires:       ro-asd-repos >= 0.1.0
Requires:       ro-asd-defaults >= 0.1.0
Requires:       ro-asd-branding >= 0.1.0

Provides:       ro-asd-desktop-profile = 44

%description
Meta-package and machine-readable contract for the Ro-ASD standard desktop
profile. Fedora KDE composition remains owned by the image compose layer.

%prep
%autosetup

%build

%install
install -Dpm 0644 desktop-standard-profile-v1.json \
  %{buildroot}%{_datadir}/ro-asd/profiles/desktop-standard-profile-v1.json

%files
%license LICENSE
%doc README.md DESKTOP-STANDARD-PROFILE-V1.md
%dir %{_datadir}/ro-asd
%dir %{_datadir}/ro-asd/profiles
%{_datadir}/ro-asd/profiles/desktop-standard-profile-v1.json

%changelog
* Wed Sep 23 2026 Project Ro-ASD <contact@roasd.org> - 0.1.0-1
- Establish the Ro-ASD standard desktop profile contract
- Require the trusted Ro-ASD foundation packages
