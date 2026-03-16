let polling = null;

// Load current settings on page load
fetch('/settings').then(r => r.json()).then(data => {
    document.getElementById('pathInput').value = data.download_path;
    document.getElementById('subtitle').textContent = `YouTube → MP3 · ${data.download_path}`;
});

function toggleSettings() {
    document.getElementById('settingsPanel').classList.toggle('open');
}

async function savePath() {
    const path = document.getElementById('pathInput').value.trim();
    if (!path) return;
    const res = await fetch('/settings', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ download_path: path })
    });
    const data = await res.json();
    const fb = document.getElementById('settingsFeedback');
    fb.textContent = data.message || data.error;
    if (res.ok) {
        document.getElementById('subtitle').textContent = `YouTube → MP3 · ${path}`;
        setTimeout(() => { fb.textContent = ''; }, 3000);
    }
}

async function startDownload() {
    const url = document.getElementById('url').value.trim();
    if (!url) return;

    setLoading(true);

    const res = await fetch('/download', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
    });

    const data = await res.json();
    setStatus(data.message || data.error);

    if (res.ok) {
        polling = setInterval(pollStatus, 1500);
    } else {
        setLoading(false);
    }
}

async function pollStatus() {
    const res = await fetch('/status');
    const data = await res.json();
    setStatus(data.message);
    if (!data.running) {
        clearInterval(polling);
        setLoading(false);
        if (!data.message.startsWith('Error')) {
            document.getElementById('url').value = '';
        }
    }
}

function setLoading(on) {
    document.getElementById('btn').disabled = on;
    document.getElementById('progress').classList.toggle('active', on);
}

function setStatus(msg) {
    document.getElementById('status').textContent = msg;
}