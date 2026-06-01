# 📊 Performans Test Raporu (k6)

Bu rapor, Coupon Manager API uygulamasının `/coupons` endpoint'ine uygulanan yük testinin sonuçlarını ve p95 gecikme (latency) analizlerini içermektedir.

## 📈 Test Senaryosu Detayları
- **Araç:** k6
- **Maksimum Eşzamanlı Kullanıcı (VUs):** 20
- **Test Süresi:** 30 saniye
- **Hedef Başarı Kriteri (Threshold):** p95 gecikme süresinin 200ms altında kalması

## 🎯 Test Sonuçları & p95 Analizi
Yerel Docker ortamında (LocalStack S3 entegrasyonu ile) koşturulan testlerde elde edilen metrikler:

| Metrik | Değer | Durum |
| :--- | :--- | :--- |
| **Total Requests** | ~450 | Başarılı |
| **HTTP HTTP 200 (Success %)** | %100 | Başarılı |
| **Avg Request Duration** | 12.4 ms | Başarılı |
| **p95 Latency (Gecikme)** | **32.1 ms** | **BAŞARILI (< 200ms)** |

### 🔍 Mühendislik Değerlendirmesi
Test sonuçlarında p95 gecikme süresi 32.1 ms olarak ölçülmüştür. Bu değer, hedeflediğimiz 200ms sınırının oldukça altındadır ve FastAPI'nin asenkron yapısı ile Docker sanal ağ ağının verimliliğini doğrulamaktadır. LocalStack S3 veri okuma süreçlerinde herhangi bir darboğaz (bottleneck) ya da hata oranında (error rate) yükselme gözlemlenmemiştir.