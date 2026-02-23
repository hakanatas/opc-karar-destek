# Orofaringeal Kanser (OPC) Karar Destek Sistemi

Bu proje, yapılandırılmış hasta verilerini alarak, Hibrit Topluluk Öğrenme (Ensemble Learning) yöntemleri ve XAI (Açıklanabilir Yapay Zeka - SHAP) ile tümör risk analizi yapan profesyonel bir web uygulamasıdır. 

Müşteri-Sunucu (Client-Server) mimarisi kullanılarak geliştirilmiştir.

## Teknolojiler
- **Arka Uç (Backend):** Python, FastAPI, Uvicorn, Pydantic (Model entegrasyonuna hazır API)
- **Ön Yüz (Frontend):** Vanilla HTML5, CSS3, JavaScript, Chart.js

## Kurulum ve Çalıştırma

### 1) Python Sanal Ortamı ve Kütüphaneler
Proje dizininde bir sanal ortam oluşturup aktif ettikten sonra gerekli kütüphaneleri indirin:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r api/requirements_api.txt
```

### 2) Sunucuyu Başlatma
Arka uç sunucusunu başlatmak için proje dizininden `api` klasörüne girip `uvicorn` komutunu çalıştırın:

```bash
cd api
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3) Uygulamayı Görüntüleme
Tarayıcınızdan http://localhost:8000 adresine giderek sistemi kullanabilirsiniz.
