# Coupon Manager API

**Marmara Üniversitesi Bilgisayar Mühendisliği**
**Bulut Mimarilerinde Test Mühendisliği — Dönem Projesi**

> **Hazırlayan:** Metehan Muhammed Torun — Öğrenci ID: `170423016`

---

## 📋 Proje Tanımı

Bu proje, e-commerce sistemlerinde indirim ve kupon yönetimi süreçlerini **FastAPI** mimarisi üzerinde, ölçeklenebilir ve **Cloud-Native** prensiplerle tasarlanmış bir backend uygulamasıdır. Test otomasyonu, dağıtık sistemler ve gözlemlenebilirlik (observability) odaklı bir altyapıya sahiptir.

---

## 🚀 Teknik Stack

| Katman | Teknolojiler |
| :--- | :--- |
| **Backend** | FastAPI (Python 3.11), Pydantic |
| **Infrastructure** | Minikube (Kubernetes), Docker (Multi-stage build), LocalStack (AWS S3 Emülasyonu) |
| **Testing** | Pytest (Unit/Integration), Playwright (Headless E2E), Factory Boy & Faker, Postman/Newman |
| **Performance** | k6 (Load Testing) |
| **Observability** | Prometheus & Grafana (Real-time monitoring) |
| **CI/CD** | GitHub Actions (Fail-Fast Pipeline) |

---

## 🏗️ Bulut Yerlisi (Cloud-Native) Mimari Tasarımı

Proje, mikroservis bağımlılıklarını yerel ortamda simüle ederken ağ izolasyonunu ve zaman aşımı (timeout) sorunlarını sıfıra indirmek amacıyla endüstri standardı olan **Sidecar Pattern** mimarisiyle kurgulanmıştır.

- Ana API konteyneri (`coupon-manager-api`) ile AWS S3 emülatörü (`localstack`), Kubernetes katmanında aynı **Pod** içerisinde konumlandırılmıştır.
- Servisler birbirleriyle `localhost` köprüsü üzerinden ultra hızlı ve izole bir şekilde haberleşmektedir.

---

## 🛠️ CI/CD Pipeline Akışı

Proje, her `push` ve `pull_request` işleminde otomatik tetiklenen endüstri standardı bir boru hattına sahiptir:

1. **Linting & Formatting** — Kod standartlarının kontrolü
2. **Testing** — Birim (Unit), Testcontainers destekli entegrasyon ve Playwright tabanlı E2E testleri
3. **Coverage Enforcement** — Kod kalitesini garantileyen zorunlu **%70+** coverage eşik kontrolü
4. **Packaging** — Docker Buildx ile optimize edilmiş, üretime hazır multi-stage container imajı derleme
5. **Deployment & Smoke Test** — Minikube deployment doğrulama ve duman testleri

---

## 📊 Başarı Metrikleri

Sistem, belirlenen tüm mühendislik hedeflerini başarıyla aşmıştır:

| Metrik | Hedef | Gerçekleşen |
| :--- | :---: | :---: |
| **Kod Kapsama (Coverage)** | > %70 | **%85** |
| **p95 Gecikme (Latency)** | < 200ms | **32.1ms** |
| **Test Senaryoları** | — | **17 Kararlı Senaryo** |
| **Hata Oranı** | %0 | **%0** |

---

## 💻 Yerel Kurulum ve Canlı Demo

Sunum ve jüri demosu esnasında uygulamanın yerel cluster üzerinde ayağa kaldırılması için aşağıdaki adımları sırayla takip edin.

### 1. Minikube ve Docker Ortamının Hazırlanması

```powershell
# Minikube cluster'ını başlatın
minikube start

# Docker terminal ortamını Minikube ağına bağlayın
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

### 2. Multi-Stage Container İmajının Derlenmesi

```powershell
# Proje kök dizininde imajı build edin
docker build -t coupon-manager:latest .
```

### 3. Kubernetes Manifestolarının Dağıtımı

```powershell
# Konfigürasyon, Service ve Sidecar Deployment bileşenlerini uygulayın
kubectl apply -f k8s/

# Eski podları temizleyerek yeni imajın kararlı yüklenmesini sağlayın
kubectl delete pods --all

# Podların hazır ve Running (READY 2/2) olduğunu doğrulayın
kubectl get pods
```

### 4. Ağ Tünelinin Kurulması (Port-Forwarding)

```powershell
# Dış dünyadan pod servis katmanına tünel açın (Bu terminali kapatmayınız)
kubectl port-forward service/coupon-manager-service 8000:8000
```

### 5. Tarayıcı Üzerinden API ve UI Kontrolü

| Arayüz | URL |
| :--- | :--- |
| **Canlı HTML Kontrol Paneli** | http://127.0.0.1:8000/ui/index.html |
| **OpenAPI Swagger UI Dokümantasyonu** | http://127.0.0.1:8000/docs |

---

## 🎬 Canlı Demo ve Sunum Yedek Videosu

Canlı demo sırasında oluşabilecek olası altyapı veya yerel ağ kesintilerine karşı hazırlanan kesintisiz sistem akış videosuna aşağıdaki linkten erişebilirsiniz:

🔗 **[Metehan Muhammed Torun — Coupon Manager E2E Canlı Demo Videosu]()**
*https://drive.google.com/file/d/1tiaq71QqgjrLij7UyvKaDA2zfIa6WRw9/view?usp=sharing*

---

## 📁 Dosya Yapısı

```
.
├── .github/workflows/   # GitHub Actions CI/CD iş akışları ve pipeline yapılandırmaları
├── src/                 # Ana uygulama mantığı, API endpointleri, statik web arayüzü ve S3 servis katmanı
├── tests/               # Birim, entegrasyon ve Playwright E2E test senaryoları ile model factory yapıları
├── postman/             # API istek senaryoları ve Newman otomasyon koleksiyonları
├── perf/                # k6 yük testi scriptleri ve performans senaryoları
├── monitoring/          # Prometheus konfigürasyonları ve Grafana dashboard metrik panelleri
├── docs/                # Mimari diyagramı (architecture.png), sunum slaytları (slides.pdf) ve final raporu (final-report.pdf)
├── k8s/                 # Kubernetes Deployment (Sidecar), Service ve ConfigMap manifestoları
├── Dockerfile           # Uygulamanın optimize edilmiş multi-stage container imaj yapılandırması
└── LICENSE              # MIT Lisans belgesi
```

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) ile lisanslanmıştır.

---

> Bu proje, Marmara Üniversitesi Bilgisayar Mühendisliği Bölümü **MTH3018** kodlu *"Bulut Mimarilerinde Test Mühendisliği"* dersi jüri değerlendirmesi için üretilmiştir.
