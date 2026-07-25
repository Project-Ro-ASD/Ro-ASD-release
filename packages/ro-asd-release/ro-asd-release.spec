Name:           ro-asd-release
Version:        0.1.0
Release:        1%{?dist}
Summary:        Ro-ASD release metadata

License:        GPL-3.0-only
URL:            https://github.com/Project-Ro-ASD/Ro-ASD-release
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

%description
Machine-readable Ro-ASD product and Fedora base release metadata. This initial
package intentionally does not replace Fedora os-release or branding files.

%prep
%autosetup

%build

%install
install -Dpm 0644 release.json %{buildroot}%{_prefix}/lib/ro-asd/release.json
install -Dpm 0644 release %{buildroot}%{_prefix}/lib/ro-asd/release
mkdir -p %{buildroot}%{_sysconfdir}
ln -s ../usr/lib/ro-asd/release %{buildroot}%{_sysconfdir}/ro-asd-release

%files
%license LICENSE
%doc README.md
%dir %{_prefix}/lib/ro-asd
%{_prefix}/lib/ro-asd/release.json
%{_prefix}/lib/ro-asd/release
%{_sysconfdir}/ro-asd-release

%changelog
* Sat Jul 25 2026 Project Ro-ASD <dev@ro-asd.invalid> - 0.1.0-1
- Add initial safe Ro-ASD release metadata package
