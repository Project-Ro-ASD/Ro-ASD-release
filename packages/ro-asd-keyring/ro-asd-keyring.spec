Name:           ro-asd-keyring
Version:        0.1.0
Release:        1%{?dist}
Summary:        Ro-ASD repository public trust keys

License:        GPL-3.0-only
URL:            https://github.com/Project-Ro-ASD/Ro-ASD-release
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Public OpenPGP keys used to verify Ro-ASD RPM packages and repository metadata.
This package contains public trust material only and never contains private
signing keys.

%prep
%autosetup

%build

%install
install -Dpm 0644 RPM-GPG-KEY-ro-asd \
  %{buildroot}%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-ro-asd
install -Dpm 0644 REPODATA-GPG-KEY-ro-asd \
  %{buildroot}%{_sysconfdir}/pki/rpm-gpg/REPODATA-GPG-KEY-ro-asd

%files
%license LICENSE
%doc README.md
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-ro-asd
%{_sysconfdir}/pki/rpm-gpg/REPODATA-GPG-KEY-ro-asd

%changelog
* Tue Sep 22 2026 Project Ro-ASD <dev@ro-asd.invalid> - 0.1.0-1
- Add initial Ro-ASD RPM and repository metadata public trust keys
