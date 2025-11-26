from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    image_url = None
    error = None

    if request.method == 'POST':
        target_url = request.form.get('url')
        if not target_url:
            error = "Masukkan link dulu dong!"
        else:
            try:
                # Menyamar jadi browser biasa agar tidak langsung diblokir
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                }
                response = requests.get(target_url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # Mencari meta tag og:image (link foto asli)
                    meta_image = soup.find("meta", property="og:image")

                    if meta_image:
                        image_url = meta_image["content"]
                    else:
                        error = "Foto tidak ditemukan. Pastikan akun tidak diprivate!"
                else:
                    error = "Gagal akses ke Instagram. Coba lagi nanti."
            except Exception as e:
                error = f"Terjadi kesalahan: {e}"

    return render_template('index.html', image_url=image_url, error=error)

if __name__ == '__main__':
    app.run(debug=True)
