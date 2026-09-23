# ro-asd-desktop-standard

Ro-ASD standard desktop profilinin meta-paketidir.

0.1.0 sürümü yalnız güven zinciri tamamlanmış foundation bileşenlerini hard
dependency olarak bağlar:

- ro-asd-release >= 0.1.2
- ro-asd-keyring >= 0.1.0
- ro-asd-repos >= 0.1.0
- ro-asd-defaults >= 0.1.0
- ro-asd-branding >= 0.1.0

Fedora KDE paket seçimi bu RPM'in işi değildir. Plasma ve temel Fedora masaüstü
paketleri gelecekteki compose tanımı tarafından seçilecektir.

Ro-Theme, Ro-Assist, Ro-ASD Plasma Setup downstream ve diğer Ro uygulamaları
mimarileri netleşene kadar 0.1.0 hard dependency setine dahil değildir.
