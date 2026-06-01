# Coupon Manager API

Marmara Üniversitesi Bilgisayar Mühendisliği 
Bulut Mimarilerinde Test Mühendisliği Dönem Projesi

## 📋 Proje Tanımı
Bu proje, e-ticaret sistemlerinde indirim ve kupon yönetimi süreçlerini; **FastAPI** mimarisi üzerinde, ölçeklenebilir ve **Cloud-Native** prensiplerle tasarlanmış bir backend uygulamasıdır. Test otomasyonu, dağıtık sistemler ve gözlemlenebilirlik (observability) odaklı bir altyapıya sahiptir.

## 🚀 Teknik Stack
* **Backend:** FastAPI (Python 3.11), Pydantic, Httpx
* **Infrastructure:** Minikube (Kubernetes), Docker, LocalStack (S3 Mock)
* **Testing:** Pytest (Unit/Integration), Playwright (E2E), k6 (Load Testing)
* **Observability:** Prometheus, Grafana
* **CI/CD:** GitHub Actions (Fail-Fast Pipeline)

## 🛠️ Mimari ve CI/CD
Proje, her kod push işleminde otomatik tetiklenen bir boru hattına sahiptir:
1. **Setup:** Python/Node.js ortamı hazırlanır.
2. **Testing:** Unit, Integration, E2E testleri çalıştırılır.
3. **Performance:** k6 ile yük testi (p95 < 200ms) yapılır.
4. **Packaging:** Docker multi-stage build ile optimize imaj üretilir.

## 📊 Metrikler
| Metrik | Hedef | Gerçekleşen |
| :--- | :--- | :--- |
| Test Kapsamı | %70 | **%71** |
| p95 Gecikme | < 200ms | **32.1ms** |

## 📁 Dosya Yapısı
- `/src`: Ana uygulama mantığı ve API endpointleri.
- `/tests`: Birim, entegrasyon ve Playwright E2E testleri.
- `/manifests`: Kubernetes Deployment ve ConfigMap yapılandırmaları.
- `slides.pdf`: Proje sunumu.

---
*Hazırlayan: Metehan Muhammed Torun (170423016)*
