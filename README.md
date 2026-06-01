# Coupon Manager API

Marmara Üniversitesi Bilgisayar Mühendisliği 
Bulut Mimarilerinde Test Mühendisliği Dönem Projesi

## 📋 Proje Tanımı
Bu proje, e-ticaret sistemlerinde indirim ve kupon yönetimi süreçlerini; **FastAPI** mimarisi üzerinde, ölçeklenebilir ve **Cloud-Native** prensiplerle tasarlanmış bir backend uygulamasıdır. Test otomasyonu, dağıtık sistemler ve gözlemlenebilirlik (observability) odaklı bir altyapıya sahiptir.

## 🚀 Teknik Stack
* **Backend:** FastAPI (Python 3.11), Pydantic
* **Infrastructure:** Minikube (Kubernetes), Docker (Multi-stage build), LocalStack (AWS S3 Emülasyonu)
* **Testing:** Pytest (Unit/Integration), Playwright (Headless E2E), Factory Boy & Faker
* **Performance:** k6 (Load Testing)
* **Observability:** Prometheus & Grafana (Real-time monitoring)
* **CI/CD:** GitHub Actions (Fail-Fast Pipeline)

## 🛠️ Mimari ve CI/CD
Proje, her `push` işleminde otomatik tetiklenen endüstri standardı bir boru hattına sahiptir:
1.  **Setup:** Sanallaştırılmış ortam hazırlığı.
2.  **Testing:** Birim, entegrasyon ve Playwright tabanlı E2E testleri (Fail-Fast mekanizması).
3.  **Performance:** k6 ile yük testi (Threshold: p95 < 200ms).
4.  **Coverage Enforcement:** Kod kalitesini garantileyen zorunlu %70+ coverage eşik kontrolü.
5.  **Packaging:** Docker Buildx ile optimize edilmiş, üretime hazır konteyner imajı derleme.

## 📊 Başarı Metrikleri
Sistem, belirlenen tüm mühendislik hedeflerini başarıyla aşmıştır:

| Metrik | Hedef | Gerçekleşen |
| :--- | :--- | :--- |
| **Kod Kapsama (Coverage)** | > %70  | **%85** |
| **p95 Gecikme (Latency)** | < 200ms | **32.1ms** |
| **Test Senaryoları** | - | **17 Kararlı Senaryo** |
| **Hata Oranı** | %0 | **%0** |

## 📁 Dosya Yapısı
- `/.github`: GitHub Actions CI/CD iş akışları ve boru hattı yapılandırmaları.
- `/src`: Ana uygulama mantığı, API endpointleri ve S3 servis katmanı.
- `/tests`: Birim, entegrasyon ve Playwright E2E testleri.
- `/postman`: API istek senaryoları ve Newman otomasyon koleksiyonları.
- `/perf`: k6 yük testi scriptleri ve performans senaryoları.
- `/docs`: Proje raporu ve sunum dosyaları.
- `/k8s`: Kubernetes Deployment, Service ve ConfigMap manifestoları.
- `Dockerfile`: Uygulamanın optimize edilmiş container imaj yapılandırması.
---
*Hazırlayan: Metehan Muhammed Torun (170423016)*
