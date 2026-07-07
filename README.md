# LİNGO — TDK Kelimeleriyle Türkçe Kelime Oyunu

TRT Lingo mantığında, Streamlit ile yazılmış kelime oyunu. 5 / 6 / 7 harfli
TDK kelimeleri, ilk harf ipucu, 5 tahmin hakkı, puan ve seri takibi.

## Dosyalar
- `app.py` — oyunun tamamı
- `kelimeler_5.txt` / `kelimeler_6.txt` / `kelimeler_7.txt` — TDK tabanlı kelime listeleri (özel isimler ve çok kelimeli girişler ayıklandı)
- `requirements.txt` — sadece `streamlit`

## Bilgisayarda çalıştırma
```bash
pip install streamlit
streamlit run app.py
```
Tarayıcıda `http://localhost:8501` açılır.

## İnternette yayınlama (babanın telefonundan oynaması için)
1. GitHub'da yeni bir **public** repo aç (ör. `lingo-tdk`), bu klasördeki 5 dosyayı yükle.
2. https://share.streamlit.io adresine GitHub hesabınla gir.
3. **New app** → repo: `kullaniciadin/lingo-tdk`, branch: `main`, main file: `app.py` → **Deploy**.
4. 1-2 dakika içinde `https://....streamlit.app` gibi bir link verir. Linki babana at, telefon tarayıcısından direkt oynar — kurulum gerekmez.

## Kurallar
- Gizli kelimenin **ilk harfi** kırmızı kutuda gösterilir.
- Her tahmin, seçilen uzunlukta ve TDK listesinde geçerli bir kelime olmalı.
- 🟥 kırmızı kare: harf doğru + yer doğru · 🟡 sarı yuvarlak: harf var, yer yanlış · 🟦 koyu: harf yok.
- Puan: doğru bilince 50 + kalan her hak × 25. Üst üste bilmek seriyi büyütür.
