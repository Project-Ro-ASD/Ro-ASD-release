# ro-asd-repos — beklemede

İstemci makinelerde sürüme özel Ro-ASD repo tanımlarını ve yalnızca kamuya açık
GPG anahtarını kuracak ayrı `noarch` paket olacaktır. Kanal adları, repo kimliği,
base URL yapısı, anahtar dosya adları ve snapshot biçimi Ro-Repo V2 yayın
sözleşmesinde kesinleşmeden spec eklenmeyecektir.

## Kanallar (0.1.5)

| Repo | Varsayılan | Kimler için |
|---|---|---|
| `ro-asd-dev` | kapalı | Release Engineering ekibi: yeni release'ler önce buraya gelir |
| `ro-asd-beta` | açık | Gönüllü test kullanıcıları |
| `ro-asd-stable` | kapalı | Herkes, ekibin onayladığı sürümler |

Ekip üyesi dev kanalını şöyle açar:

```bash
sudo dnf config-manager setopt ro-asd-dev.enabled=1
sudo dnf upgrade --refresh
```

Kapatmak için `ro-asd-dev.enabled=0`. Aynı paketin dev ve beta'da farklı sürümü varsa DNF yeni olanı seçer.
