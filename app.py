from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

if not os.path.exists('downloads'):
    os.makedirs('downloads')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    if not url:
        return "URL kosong", 400

    # hapus file lama
    for f in os.listdir('downloads'):
        try:
            os.remove(os.path.join('downloads', f))
        except:
            pass

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'quiet': True,
            'no_warnings': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            title = info.get('title', 'video')

        return f"""
        <h3>{title}</h3>
        <video width="100%" controls autoplay>
            <source src="/get_video" type="video/mp4">
        </video>
        <br><br>
        <a href="/get_video" download style="display:block;padding:12px;background:#fe2c55;color:white;text-align:center;text-decoration:none;border-radius:8px">DOWNLOAD VIDEO</a>
        <br><a href="/">Kembali</a>
        """
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/get_video')
def get_video():
    files = os.listdir('downloads')
    if not files:
        return "File tidak ada", 404
    filepath = os.path.join('downloads', files[0])
    return send_file(filepath, as_attachment=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
