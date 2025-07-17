import os                               # İşletim sistemi ile ilgili işlemler için (env değişkenleri için)
import requests                         # HTTP istekleri yapmak için (API çağrısı için)
from dotenv import load_dotenv          # .env dosyasını okuyup çevresel değişkenleri yüklemek için

load_dotenv()                          # Proje klasöründeki .env dosyasını yükle, API keyleri çevre değişkenlerine aktarılır

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")  # .env içinden WEATHER_API_KEY anahtarını al ve değişkene ata

def get_weather(city: str) -> dict:   # 'city' isimli şehir parametresi alan ve sözlük (dict) döndüren fonksiyon tanımı
    """
    OpenWeatherMap API üzerinden verilen şehir için hava durumu bilgilerini çeker.
    """
    # OpenWeatherMap API URL'sini oluşturuyoruz, şehir ismi, API key, birim metrik (°C) ve dil Türkçe olarak parametrelenmiş
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=tr"
    
    response = requests.get(url)       # Hazırlanan URL'ye GET isteği atıyoruz, API'den cevap alıyoruz
    
    data = response.json()              # Gelen cevabı JSON formatına çeviriyoruz (Python sözlüğüne)
    
    # Eğer API çağrısı başarılıysa (HTTP durum kodu 200 ise)
    if response.status_code == 200:
        return {                       # Hava durumu bilgilerini sözlük olarak döndürüyoruz
            "şehir": city,             # İstenen şehir ismi
            "sıcaklık": data["main"]["temp"],          # Sıcaklık (°C)
            "açıklama": data["weather"][0]["description"], # Hava durumu açıklaması (ör: "açık", "bulutlu")
            "nem": data["main"]["humidity"]            # Nem yüzdesi
        }
    else:
        # API hatalıysa veya şehir bulunamadıysa hata mesajı içeren sözlük döndür
        return {"error": f"{city} için hava durumu bulunamadı."}
