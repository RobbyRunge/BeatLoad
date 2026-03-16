from flask import Flask, request, jsonify, render_template
import yt_dlp
import threading
import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
DOWNLOAD_PATH = os.environ.get("DOWNLOAD_PATH", "")

status = {"message": "⚠ No download path set. Open Settings and enter a path." if not DOWNLOAD_PATH else "Ready.", "running": False}
settings = {"download_path": DOWNLOAD_PATH}


def do_download(url):
    status["running"] = True
    status["message"] = "Downloading..."

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{settings["download_path"]}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        status["message"] = f"Done! Saved to {settings['download_path']}"
    except Exception as e:
        status["message"] = f"Error: {e}"
    finally:
        status["running"] = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download():
    if status["running"]:
        return jsonify({"error": "Download already running."}), 429
    url = request.json.get("url", "").strip()
    if not url:
        return jsonify({"error": "No URL provided."}), 400
    threading.Thread(target=do_download, args=(url,), daemon=True).start()
    return jsonify({"message": "Download started."})


@app.route("/settings", methods=["GET", "POST"])
def handle_settings():
    if request.method == "POST":
        path = request.json.get("download_path", "").strip()
        if not path:
            return jsonify({"error": "No path provided."}), 400
        settings["download_path"] = path
        return jsonify({"message": "Saved.", "download_path": path})
    return jsonify(settings)


@app.route("/status")
def get_status():
    return jsonify(status)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
