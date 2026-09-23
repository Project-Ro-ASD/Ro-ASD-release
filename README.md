# Ro-ASD release policy packages

Bu depo, Ro-ASD dağıtım kimliğini ve sistem politikasını kurulum aracından
bağımsız RPM paketlerine taşır. Fedora 44 ilk yayın tabanıdır.

## Kapsam

Depoda bağımsız kaynak RPM aileleri planlanır:

| Paket ailesi | Sahip olduğu alan | Bugünkü durum |
| --- | --- | --- |
| `ro-asd-release` | Makinece okunabilir Ro-ASD/Fedora sürüm metadatası | İlk çalışan RPM iskeleti |
| `ro-asd-keyring` | Ro-ASD public trust anahtarları | İlk çalışan RPM iskeleti |
| `ro-asd-repos` | İstemci repo dosyaları | İlk çalışan RPM iskeleti |
| `ro-asd-branding` | Logo, ad ve dağıtım kimliği varlıkları | Branding contract v1 + ilk RPM iskeleti |
| `ro-asd-defaults` | Paketlenmiş masaüstü ve sistem varsayılanları | Ownership contract v1 + ilk RPM iskeleti |
| `ro-asd-kernel-policy` | Kararlı/deneysel/fallback çekirdek kanal politikası | Fedora 44 çekirdek kaynağını bekliyor |
| `ro-asd-desktop-standard` | Standart profil meta-paketi | Profile contract v1 + foundation meta-package |

Bu paket aileleri tek spec içinde birleştirilmeyecektir. Aynı Git deposunda
yaşayabilirler ancak bağımsız sürümlenir ve bağımsız SRPM üretirler.

## İlk çalışan parça

`packages/ro-asd-release`, `packages/ro-asd-keyring`, `packages/ro-asd-repos`, `packages/ro-asd-defaults`, `packages/ro-asd-branding` ve `packages/ro-asd-desktop-standard` bugün gerçek spec içerir. Paket şu güvenli
dosyaları kurar:

- `/usr/lib/ro-asd/release.json`
- `/usr/lib/ro-asd/release`
- `/etc/ro-asd-release` sembolik bağı

Bu aşamada `/usr/lib/os-release`, Fedora logo/marka dosyaları, çekirdek
politikası veya `system-release` provides/obsoletes değiştirilmez.

`ro-asd-repos` şu DNF kanallarını tanımlar:

- `ro-asd-beta`: varsayılan açık
- `ro-asd-beta-source`: kapalı
- `ro-asd-stable`: kapalı
- `ro-asd-stable-source`: kapalı

İlk sürümde beta kanalının açık olmasının nedeni, public Ro-Repo V2 ağacında
henüz stable kanalının bulunmamasıdır. Tüm tanımlar hem RPM hem repository
metadata signature doğrulamasını zorunlu tutar ve `ro-asd-keyring >= 0.1.0`
bağımlılığı ile trust material'i paket üzerinden alır.

`VERSION.yaml` ürün sürümü için tek kaynaktır. Ro-ASD görünür ürün sürümü
Fedora tabanıyla birlikte `44` iken bu RPM'in bileşen sürümü bağımsız olarak
`0.1.0-1.fc44` değeridir.

## Yerel doğrulama

Fedora 44 üzerinde:

```bash
./scripts/check-version.py
./scripts/build-rpm.sh
./scripts/verify-build.py dist
```

Normal PR/main CI çıktısı RPM, SRPM, `SHA256SUMS` ve
`build-manifest-v1.json` üretir. Bu manifest yalnız derleme kanıtıdır ve bir
Ro-Repo producer release kimliği değildir.

## Trusted release modeli

Gerçek `ro-asd-release` yayını yalnız component-scoped tag ile tetiklenir:

```text
ro-asd-release-v0.1.0
```

Trusted `.github/workflows/release.yml` şu zinciri uygular:

1. tag sürümünü `VERSION.yaml` ve RPM spec ile eşleştirir,
2. tag commit'inin `main` geçmişinde olduğunu doğrular,
3. Fedora 44 ortamında RPM ve SRPM üretir,
4. draft GitHub Release oluşturup numeric release ID alır,
5. canonical `component-artifact-manifest-v1.json` üretir,
6. release bundle için GitHub attestation üretir,
7. asset kümesini doğrular,
8. yalnız tüm kontroller geçtiğinde draft release'i publish eder.

Producer RPM'leri production anahtarıyla imzalamaz. Production RPM/repository
imzası Ro-Repo tarafından merkezi olarak uygulanır.

Monorepo içindeki paket aileleri kendi component-scoped tag alanlarını kullanır.
Örneğin `ro-asd-release-vX.Y.Z`, `ro-asd-keyring-vX.Y.Z` ve ileride
`ro-asd-repos-vX.Y.Z`.

`ro-asd-keyring`, yalnız public OpenPGP trust material taşır. İlk keyring
sürümündeki RPM ve repository-metadata anahtarları Ro-Repo'nun immutable
`repo-f44-20260920-001` snapshot'ından vendörlenmiştir. Beklenen signing
subkey fingerprint'leri package contract içinde pinlenir:

- RPM: `38CB87F6FBD645309432A6E22E02DEE8828B769B`
- repository metadata: `1715DDA529B9ADB46D47CB389A62B8F9026E75E5`

Private signing key hiçbir zaman bu depoya veya keyring RPM'ine girmez.

## Bilinçli olarak bekletilen işler

- Fedora kimlik dosyalarının değiştirilmesi
- KIWI compose ve ISO üretimi
- Diğer paket ailelerinin production producer workflow'a bağlanması


## Defaults ownership modeli

`ro-asd-defaults` kullanıcı home dizinlerine yazmaz, `/etc/skel/.config`
üzerinden kullanıcı ayarı kopyalamaz ve normal distro varsayılanlarını KConfig
immutable hale getirmez. İlk `0.1.0` sürümü yalnız machine-readable ownership
contract taşır ve masaüstü davranışını değiştirmez.

Tema, wallpaper, icon/cursor, Plymouth ve mevcut tema KConfig dosyaları
`ro-theme` sahipliğinde kalır. Ayrıntılı sınırlar
`docs/DEFAULTS-OWNERSHIP-V1.md` ve
`packages/ro-asd-defaults/defaults-policy-v1.json` içindedir.


## Branding ownership modeli

`ro-asd-branding` Ro-ASD'ye özgü görünür dağıtım kimliğinin sahibi olarak
ayrılır. İlk `0.1.0` sürümü yalnız machine-readable branding contract taşır;
Fedora release dosyalarını veya Fedora-owned logo yollarını değiştirmez.

Mevcut Ro-Theme logosu v1'de Ro-Theme sahipliğinde kalır. Logo asset'leri
branding paketine ancak tek canonical source-of-truth belirlendikten sonra
taşınacaktır. Ayrıntılı sınırlar `docs/BRANDING-CONTRACT-V1.md` ve
`packages/ro-asd-branding/branding-contract-v1.json` içindedir.


## Desktop standard profile modeli

`ro-asd-desktop-standard` Fedora KDE paket listesini kopyalamaz. İlk 0.1.0
sürümü yalnız güven zinciri tamamlanmış Ro-ASD foundation bileşenlerini
dependency olarak bağlar ve standard desktop profile contract'ını taşır.

Ro-Theme, Ro-Assist ve olası Ro-ASD Plasma Setup downstream entegrasyonu
mimarileri tamamlanana kadar hard dependency değildir. Fedora KDE temel paket
seçimi gelecekteki compose katmanının sorumluluğundadır.
