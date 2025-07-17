# VentoAI Canlı Hava Durumu Uygulaması 🌤️

Bu Python terminal uygulaması, Google Gemini API (örneğin Gemini 2.5 Flash) ve kendi yazdığım `weather_api` fonksiyonları kullanarak kullanıcıların istedikleri şehirlerin güncel hava durumunu gösterir.

---

## Özellikler

- Kullanıcıdan şehir ismi alır
- Gemini modelini kullanarak fonksiyon çağrısı ile hava durumu bilgisi getirir
- Sıcaklık, hava durumu açıklaması ve nem yüzdesi gösterir
- Kullanıcı “çıkış” yazana kadar çalışır

---

## Gereksinimler

- Python 3.8+
- Google Gemini API anahtarı
- Weather API anahtarı (kendi `weather_api.py` fonksiyonun kullanıyor)
- `dotenv` kütüphanesi (.env dosyasını okumak için)
- `google-generativeai` kütüphanesi

---

## Kurulum

1. Depoyu klonla veya indir:
   ```bash
   git clone https://github.com/kullaniciadi/ventoai-weather.git
   cd ventoai-weather
