# Ro-ASD Kernel Policy v1

Bu belge `ro-asd-kernel-policy 0.1.0` için güvenli foundation sınırını
tanımlar.

## Kanal modeli

Politika üç kavramsal kanal tanımlar:

- **standard**: normal kullanım için desteklenen varsayılan kanal.
- **experimental**: yalnız açık kullanıcı tercihiyle seçilebilen test kanalı.
- **fallback**: bilinen-çalışan kurtarma çekirdeği.

0.1.0 bu kanallardan hiçbirini etkinleştirmez veya paket adıyla bağlamaz.

## Ownership

- Ro Installer kernel seçimi yapmaz.
- Plasma Setup kernel seçimi yapmaz.
- Gelecekte kullanıcıya açık seçim ve yönetim Ro-Assist'e aittir.
- Compose katmanı, internet olmadan dahi boot edebilen başlangıç kernelini
  image içine koymakla sorumludur.
- Gerçek kernel paketlerinin producer'ı daha sonra ayrı güven zinciriyle
  tanımlanacaktır.

## Güvenlik invariantları

Sistem aktif kernel yönetimine geçtiğinde:

1. En az bir bilinen-çalışan boot edilebilir kernel korunmalıdır.
2. Experimental kanal hiçbir zaman otomatik seçilmemelidir.
3. Offline kurulum boot edilebilir baseline kernel ile tamamlanmalıdır.
4. Ro kernel enforcement başlamadan önce Secure Boot signing zinciri
   doğrulanmalıdır.

## 0.1.0'da özellikle yapılmayanlar

Paket Fedora kernel RPM'lerini kaldırmaz veya exclude etmez, harici repository
açmaz, bootloader default'unu değiştirmez, kernel command line yazmaz, Secure
Boot state değiştirmez ve herhangi bir kernel channel zorlamaz.

Bu sınır, kernel altyapısı tamamlanmadan bir policy RPM'inin sistemi boot
edilemez hale getirmesini engeller.
