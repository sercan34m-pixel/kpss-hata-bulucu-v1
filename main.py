import flet as ft
import json
import os
import traceback # Hatayı ekrana basmak için gerekli

# --- DOSYA İSİMLERİ ---
SORU_DOSYASI = "sorular.json" 
BILGI_DOSYASI = "pratik_bilgiler.json"

def main(page: ft.Page):
    # 1. GÜVENLİK AĞI: Tüm kod try-except içinde
    try:
        page.title = "Hata Avcısı Modu"
        page.theme_mode = ft.ThemeMode.LIGHT
        page.padding = 20
        page.scroll = "AUTO"

        # Ekrana bir başlık atalım ki çalıştığını görelim
        page.add(ft.Text("🚀 Uygulama Başlatılıyor...", size=20, weight="bold", color="blue"))
        page.update()

        # --- TEST 1: Dosyalar Yanımızda mı? ---
        # Bulunduğumuz klasördeki dosyaları listele
        mevcut_konum = os.getcwd()
        dosyalar = os.listdir(mevcut_konum)
        
        page.add(ft.Text(f"📂 Konum: {mevcut_konum}", size=12))
        page.add(ft.Text(f"📄 Dosyalar: {str(dosyalar)}", size=12, color="grey"))
        page.update()

        # --- TEST 2: Soru Dosyasını Okuma ---
        tum_sorular = []
        if SORU_DOSYASI in dosyalar:
            page.add(ft.Text(f"✅ {SORU_DOSYASI} bulundu, okunuyor...", color="green"))
            try:
                with open(SORU_DOSYASI, "r", encoding="utf-8") as f:
                    tum_sorular = json.load(f)
                page.add(ft.Text(f"🎉 Başarılı! {len(tum_sorular)} soru yüklendi.", color="green", weight="bold"))
            except Exception as e:
                page.add(ft.Text(f"❌ Dosya var ama okunamadı: {e}", color="red"))
        else:
            page.add(ft.Text(f"❌ {SORU_DOSYASI} BULUNAMADI!", color="red", weight="bold"))
            # Kritik hata olsa bile devam et, çökme.

        page.update()

        # ====================================================
        # BURADA NORMAL UYGULAMAYI BAŞLATIYORUZ (SADELEŞTİRİLMİŞ)
        # ====================================================
        
        # Eğer soru yoksa uyarı ver
        if not tum_sorular:
            page.add(ft.Container(content=ft.Text("Veritabanı boş olduğu için uygulama başlatılamadı.", color="white"), bgcolor="red", padding=10))
            return

        # Basit bir giriş ekranı çizelim (Hata yoksa burası görünecek)
        def giris_yap(e):
            page.snack_bar = ft.SnackBar(ft.Text("Giriş Başarılı!"))
            page.snack_bar.open = True
            page.update()

        page.add(ft.Divider())
        page.add(ft.Text("✅ SİSTEM TESTİ GEÇİLDİ", size=20, color="green"))
        page.add(ft.TextField(label="Adınız"))
        page.add(ft.ElevatedButton("Teste Başla", on_click=giris_yap))
        
    except Exception as e:
        # EĞER BİR HATA OLURSA BEYAZ EKRAN YERİNE BUNU GÖSTER
        hata_mesaji = traceback.format_exc()
        page.clean()
        page.add(ft.Column([
            ft.Icon("error", color="red", size=50),
            ft.Text("UYGULAMA ÇÖKTÜ!", size=30, color="red", weight="bold"),
            ft.Container(height=20),
            ft.Text("Lütfen bu ekranın görüntüsünü al:", weight="bold"),
            ft.Container(
                content=ft.Text(hata_mesaji, color="white", size=10, font_family="monospace"),
                bgcolor="black",
                padding=10,
                border_radius=10
            )
        ], scroll="AUTO"))
        page.update()

# --- GİRİŞ KAPISI ---
if __name__ == "__main__":
    ft.app(target=main)