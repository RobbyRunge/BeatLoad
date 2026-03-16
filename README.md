# Beatload

A simple web-based YouTube to MP3 downloader with a clean dark UI. Paste a YouTube URL, hit Download, and the audio gets saved as an MP3 to a folder of your choice.

---

## Features

- Download audio from YouTube as high-quality MP3 (192kbps)
- Clean dark web interface — runs locally in your browser
- Configurable download path via the Settings panel
- Live download status with animated progress bar
- URL field clears automatically after a successful download

---

## Requirements

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/) (required for audio conversion)

---

## Installation

**1. Clone or download the project**

```bash
git clone https://github.com/yourname/beatload.git
cd beatload
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

On Linux / macOS:
```bash
source .venv/bin/activate
```

On Windows:
```cmd
.venv\Scripts\activate
```

**3. Install Python dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure your download path**

Copy the example env file and set your path:

```bash
cp .env.example .env
```

Then edit `.env`:

```
DOWNLOAD_PATH=/your/download/path
```

**5. Install ffmpeg**

On Fedora / Nobara:
```bash
sudo dnf install ffmpeg
```

On Ubuntu / Debian:
```bash
sudo apt install ffmpeg
```

On Arch:
```bash
sudo pacman -S ffmpeg
```

On Windows:

1. Download the latest ffmpeg build from [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/) (choose `ffmpeg-release-essentials.zip`)
2. Extract the zip and copy the `bin` folder contents (ffmpeg.exe, ffprobe.exe, ffplay.exe) to a folder like `C:\ffmpeg\bin`
3. Add `C:\ffmpeg\bin` to your system PATH:
   - Open **Start** → search **"Environment Variables"**
   - Under **System Variables**, select **Path** → click **Edit**
   - Click **New** and add `C:\ffmpeg\bin`
   - Click **OK** and restart your terminal
4. Verify with:
```cmd
ffmpeg -version
```

---

## Usage

**Start the server:**

```bash
source .venv/bin/activate   # skip if already active
python app.py
```

**Open in your browser:**

```
http://localhost:5001
```

Paste a YouTube URL into the input field and click **Download**. The MP3 file will be saved to the configured download path.

---

## Configuration

The download path is read from the `.env` file on startup. You can also change it at any time directly in the UI without restarting:

1. Click **⚙ Settings** in the top right corner
2. Enter a new path in the **Download Path** field
3. Click **Save**

The new path is applied immediately to all subsequent downloads.

> **Note:** Changes made in the UI are not written back to `.env` — they only last until the server restarts.

---

## Project Structure

```
beatload/
├── app.py                  # Flask backend
├── .env                    # Your local config (not committed)
├── .env.example            # Example config for new users
├── requirements.txt        # Python dependencies
├── static/
│   ├── css/
│   │   └── style.css       # Stylesheet
│   └── js/
│       └── app.js          # Frontend logic
└── templates/
    └── index.html          # Main UI
```

---

## Desktop Shortcut

### Linux

To launch Beatload with a double-click, create a `.desktop` file:

```ini
[Desktop Entry]
Name=Beatload
Comment=YouTube to MP3 Downloader
Exec=bash -c "cd /path/to/beatload && source .venv/bin/activate && python app.py & sleep 2 && xdg-open http://localhost:5001"
Icon=audio-x-generic
Terminal=false
Type=Application
Categories=Audio;
```

Save it to `~/Desktop/Beatload.desktop` and make it executable:

```bash
chmod +x ~/Desktop/Beatload.desktop
```

### Windows

Create a file called `Beatload.bat` on your Desktop with the following content:

```bat
@echo off
cd /d "C:\path\to\beatload"
call .venv\Scripts\activate
start /B python app.py
timeout /t 2 >nul
start http://localhost:5001
```

Double-click the `.bat` file to start the server and open the browser automatically.

> **Note:** On Windows, use backslashes for the download path in `.env`, e.g. `DOWNLOAD_PATH=C:\Users\YourName\Music`.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Serves the web UI |
| `POST` | `/download` | Starts a download (`{ "url": "..." }`) |
| `GET` | `/status` | Returns current download status |
| `GET` | `/settings` | Returns current settings |
| `POST` | `/settings` | Updates settings (`{ "download_path": "..." }`) |

---

## Notes

- Only one download can run at a time. Starting a new one while another is in progress will return a `429` error.
- The server runs in debug mode by default. For production use, consider running it behind a proper WSGI server like Gunicorn.
