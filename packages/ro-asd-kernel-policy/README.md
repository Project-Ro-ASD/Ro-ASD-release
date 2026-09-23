# ro-asd-kernel-policy

Ro-ASD kernel lifecycle ve güvenlik politikasının machine-readable temel
paketidir.

İlk `0.1.0` sürümü **aktif kernel yönetimi yapmaz**. Paket yalnız
`/usr/share/ro-asd/kernel/kernel-policy-v1.json` sözleşmesini taşır.

Bu sürümde:

- kernel paketi kurulmaz veya kaldırılmaz,
- Fedora kernel paketleri exclude edilmez,
- harici kernel deposu etkinleştirilmez,
- bootloader varsayılanı değiştirilmez,
- kernel command line yeniden yazılmaz,
- Secure Boot durumu değiştirilmez,
- standard/experimental/fallback kanallarından biri zorla seçilmez.

Kernel seçimi Ro Installer veya Plasma Setup'ın işi değildir. Gelecekte
kullanıcıya açık kernel seçimi ve yönetimi Ro-Assist üzerinden yapılacaktır.
Compose katmanı ise image'ın boot edilebilir başlangıç kernelini sağlamakla
sorumludur.

Aktif kernel politikası ancak trusted kernel producer, Secure Boot signing
zinciri, fallback boot testi, rollback/upgrade kanıtı ve Ro-Assist kernel
yönetimi hazır olduğunda ayrı bir sürümle açılacaktır.
