# Ro-ASD release policy packages

Bu depo, Ro-ASD dağıtım kimliğini ve sistem politikasını kurulum aracından
bağımsız RPM paketlerine taşır. Fedora 44 ilk yayın tabanıdır.

## Kapsam

Depoda altı ayrı kaynak RPM ailesi planlanır:

| Paket ailesi | Sahip olduğu alan | Bugünkü durum |
| --- | --- | --- |
| `ro-asd-release` | Makinece okunabilir Ro-ASD/Fedora sürüm metadatası | İlk çalışan RPM iskeleti |
| `ro-asd-repos` | İstemci repo dosyaları ve kamu anahtarı | Ro-Repo V2 sözleşmesini bekliyor |
| `ro-asd-branding` | Logo, ad ve dağıtım kimliği varlıkları | Fedora marka incelemesini bekliyor |
| `ro-asd-defaults` | Paketlenmiş masaüstü ve sistem varsayılanları | Sahiplik matrisi hazırlanacak |
| `ro-asd-kernel-policy` | Kararlı/deneysel/fallback çekirdek kanal politikası | Fedora 44 çekirdek kaynağını bekliyor |
| `ro-asd-desktop-standard` | Standart profil meta-paketi | Theme ve Assist teslimlerini bekliyor |

Bu paketler tek spec içinde birleştirilmeyecektir. Her aile bağımsız sürümlenir
ve bağımsız SRPM üretir.

## İlk çalışan parça

Yalnızca `packages/ro-asd-release` bugün gerçek spec içerir. Paket şu güvenli
dosyaları kurar:

- `/usr/lib/ro-asd/release.json`
- `/usr/lib/ro-asd/release`
- `/etc/ro-asd-release` sembolik bağı

Bu aşamada `/usr/lib/os-release`, Fedora logo/marka dosyaları, repo URL'leri,
GPG anahtarları, çekirdek politikası veya `system-release` provides/obsoletes
değiştirilmez.

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

Çıktılar `dist/` altında ikili/noarch RPM, eşleşen SRPM, `SHA256SUMS` ve
geliştirme manifesti olarak oluşur. Bunlar CI kanıtıdır; tag, GitHub Release,
imza veya Ro-Repo yayını değildir.

## Bilinçli olarak bekletilen işler

- Canlı alan adı ve repo URL'lerinin pakete yazılması
- Resmî RPM/repodata imzası ve anahtar dağıtımı
- Fedora kimlik dosyalarının değiştirilmesi
- KIWI compose ve ISO üretimi
- Tag tabanlı GitHub Release ve Ro-Repo alım otomasyonu

Bu adımlar Ro-Repo V2 yayın sözleşmesi, proje anahtar kimliği ve marka kararı
kesinleşmeden eklenmemelidir.
