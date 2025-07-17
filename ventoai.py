import os                                # Ortam değişkenlerini okumak için
from dotenv import load_dotenv           # .env dosyasındaki API key'leri okumak için
import google.generativeai as genai      # Gemini API'si için Google kütüphanesi
from weather_api import get_weather      # Kendi yazdığımız hava durumu fonksiyonu
from gemini_functions import functions   # Gemini Function Calling fonksiyon tanımları
import sys                               # Sistem fonksiyonları için

# .env dosyasını yükle (.env içinde GOOGLE_API_KEY, WEATHER_API_KEY ve GEMINI_MODEL olacak)
load_dotenv()

# API anahtarlarını ortamdan al
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL")  # Örn: "models/gemini-1.5-flash"

# Gemini API'yi başlat
genai.configure(api_key=GOOGLE_API_KEY)

# Gemini modelini tanımla ve fonksiyonları bağla
model = genai.GenerativeModel(
    model_name=MODEL_NAME,  # Artık model adını .env dosyasından okuyoruz
    tools=[{"function_declarations": functions}]
)

# Chat başlat
chat = model.start_chat()

def clear_input_buffer():
    """Input buffer'ını temizle"""
    if hasattr(sys.stdin, 'flush'):
        sys.stdin.flush()

def get_user_input():
    """Güvenli kullanıcı girişi al"""
    try:
        clear_input_buffer()
        user_input = input("\nHava durumu öğrenmek istediğiniz şehri yazınız (Çıkmak için 'çıkış' yazın): ").strip()
        return user_input
    except (EOFError, KeyboardInterrupt):
        return "çıkış"

def handle_gemini_response(response, user_input):
    """Gemini yanıtını işle"""
    try:
        # Response'un yapısını kontrol et
        if not response.candidates:
            print("\n🤖 Üzgünüm, bir yanıt alamadım. Lütfen tekrar deneyin.")
            return
        
        candidate = response.candidates[0]
        
        # Content kontrolü
        if not candidate.content or not candidate.content.parts:
            print("\n🤖 Üzgünüm, bir yanıt alamadım. Lütfen tekrar deneyin.")
            return
        
        first_part = candidate.content.parts[0]
        
        # Fonksiyon çağrısı kontrolü
        if hasattr(first_part, 'function_call') and first_part.function_call:
            function_call = first_part.function_call
            
            if function_call.name == "get_weather":
                city = function_call.args.get("city", user_input)
                result = get_weather(city)
                
                if "error" not in result:
                    print(f"\n📍 {city} için hava durumu:")
                    print(f"🌡️ Sıcaklık: {result['sıcaklık']}°C")
                    print(f"🌤️ Durum: {result['açıklama']}")
                    print(f"💧 Nem: %{result['nem']}")
                else:
                    print(f"\n⚠️ Hata: {result['error']}")
            else:
                print(f"\n🤖 Bilinmeyen fonksiyon çağrısı: {function_call.name}")
        
        # Metin yanıtı kontrolü
        elif hasattr(first_part, 'text') and first_part.text:
            response_text = first_part.text.strip()
            if response_text:
                print(f"\n🤖 {response_text}")
        
        else:
            print("\n🤖 Hangi şehrin hava durumunu öğrenmek istiyorsunuz?")
            
    except Exception as e:
        print(f"\n🚨 Yanıt işlenirken hata: {e}")

def main():
    print("VentoAI Canlı Hava Durumu Uygulamasına Hoşgeldiniz! 🌤️")
    print(" Şehir adının başına 'Hava durumu' yazın (örn: 'Hava durumu İstanbul')")
    
    request_count = 0  # Talep sayacı
    
    while True:
        try:
            # Kullanıcıdan şehir ismini al
            user_input = get_user_input()
            
            # Çıkış kontrolü
            if user_input.lower() in ["çıkış", "exit", "quit", "q"]:
                print("Görüşmek üzere! 👋")
                break
            
            # Boş giriş kontrolü
            if not user_input:
                print("\n⚠️ Lütfen bir şehir adı girin.")
                continue
            
            # Çok uzun giriş kontrolü
            if len(user_input) > 100:
                print("\n⚠️ Lütfen daha kısa bir şehir adı girin.")
                continue
            
            request_count += 1
            print(f"\n🔄 İşleniyor... (Talep #{request_count})")
            
            # Kullanıcının mesajını Gemini'ye gönder
            response = chat.send_message(user_input)
            
            # Yanıtı işle
            handle_gemini_response(response, user_input)
            
        except KeyboardInterrupt:
            print("\n\nProgram kullanıcı tarafından durduruldu. Görüşmek üzere! 👋")
            break
        except Exception as e:
            print(f"\n🚨 Beklenmeyen hata: {e}")
            print("Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
