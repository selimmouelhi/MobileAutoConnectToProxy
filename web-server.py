#!/usr/bin/env python3
"""
Web UI for Android Proxy Setup.
Serves a browser-based frontend and JSON API on localhost:8080.

Reuses proxy logic from proxy-setup.py.
"""

import importlib
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# Import proxy-setup.py as a module (hyphen in filename requires importlib)
proxy_setup = importlib.import_module("proxy-setup")

get_local_ip = proxy_setup.get_local_ip
check_adb = proxy_setup.check_adb
get_connected_android_devices = proxy_setup.get_connected_android_devices
android_set_proxy = proxy_setup.android_set_proxy
android_clear_proxy = proxy_setup.android_clear_proxy
DEFAULT_PROXY_PORT = proxy_setup.DEFAULT_PROXY_PORT

HOST = "0.0.0.0"
PORT = 8080

# ── HTML Frontend ────────────────────────────────────────────────────────────

HTML_PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Proxy Setup - Android Devices</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, sans-serif;
    background: #1a1a2e; color: #e0e0e0; min-height: 100vh;
    display: flex; justify-content: center; padding: 2rem 1rem;
  }
  .container { max-width: 640px; width: 100%; }
  h1 { font-size: 1.5rem; margin-bottom: .25rem; color: #fff; }
  .subtitle { color: #888; font-size: .85rem; margin-bottom: 1.5rem; }

  /* Info bar */
  .info-bar {
    background: #16213e; border-radius: 10px; padding: 1rem 1.25rem;
    display: flex; gap: 2rem; margin-bottom: 1.25rem; flex-wrap: wrap;
  }
  .info-item label { display: block; font-size: .7rem; text-transform: uppercase;
    letter-spacing: .05em; color: #888; margin-bottom: .2rem; }
  .info-item span { font-size: 1rem; color: #00d2ff; font-weight: 600; }
  .info-item span.warn { color: #ff6b6b; }

  /* Devices */
  .section-title { font-size: .85rem; color: #888; margin-bottom: .5rem; }
  .devices {
    background: #16213e; border-radius: 10px; padding: 1rem 1.25rem;
    margin-bottom: 1.25rem; min-height: 56px;
  }
  .device-row {
    display: flex; align-items: center; gap: .75rem;
    padding: .5rem 0; border-bottom: 1px solid #1a1a3e;
  }
  .device-row:last-child { border-bottom: none; }
  .device-dot { width: 8px; height: 8px; border-radius: 50%; background: #00e676; flex-shrink: 0; }
  .device-model { font-weight: 600; color: #fff; }
  .device-serial { font-size: .75rem; color: #666; margin-left: auto; font-family: monospace; }
  .no-devices { color: #666; font-style: italic; padding: .5rem 0; }

  /* Form */
  .form-row { display: flex; gap: .75rem; margin-bottom: 1.25rem; }
  .field { flex: 1; }
  .field.port { flex: 0 0 100px; }
  .field label { display: block; font-size: .75rem; color: #888; margin-bottom: .3rem; }
  .field input {
    width: 100%; padding: .6rem .75rem; border-radius: 8px; border: 1px solid #2a2a4a;
    background: #16213e; color: #fff; font-size: .95rem; outline: none;
  }
  .field input:focus { border-color: #00d2ff; }

  /* Buttons */
  .btn-row { display: flex; gap: .75rem; margin-bottom: 1.25rem; }
  .btn {
    flex: 1; padding: .85rem; border: none; border-radius: 10px;
    font-size: 1rem; font-weight: 700; cursor: pointer; transition: opacity .15s;
    color: #fff;
  }
  .btn:hover { opacity: .85; }
  .btn:disabled { opacity: .4; cursor: not-allowed; }
  .btn-enable { background: #00c853; }
  .btn-disable { background: #ff1744; }

  /* Results */
  .results {
    background: #16213e; border-radius: 10px; padding: 1rem 1.25rem;
    display: none;
  }
  .results.show { display: block; }
  .result-row { padding: .35rem 0; font-size: .85rem; font-family: monospace; }
  .result-row.ok { color: #69f0ae; }
  .result-row.fail { color: #ff6b6b; }
  .result-row.error { color: #ff6b6b; }

  .spinner { display: inline-block; width: 14px; height: 14px; border: 2px solid #444;
    border-top-color: #00d2ff; border-radius: 50%; animation: spin .6s linear infinite;
    vertical-align: middle; margin-right: .4rem; }
  @keyframes spin { to { transform: rotate(360deg); } }
</style>
</head>
<body>
<div class="container">
  <h1>Proxy Setup</h1>
  <p class="subtitle">Android Test Devices via ADB</p>

  <div class="info-bar">
    <div class="info-item">
      <label>Mac IP</label>
      <span id="mac-ip">...</span>
    </div>
    <div class="info-item">
      <label>ADB Status</label>
      <span id="adb-status">...</span>
    </div>
    <div class="info-item">
      <label>Devices</label>
      <span id="device-count">...</span>
    </div>
  </div>

  <p class="section-title">Connected Devices</p>
  <div class="devices" id="device-list">
    <div class="no-devices">Loading...</div>
  </div>

  <div class="form-row">
    <div class="field">
      <label>Proxy IP Address</label>
      <input type="text" id="proxy-ip" placeholder="192.168.x.x">
    </div>
    <div class="field port">
      <label>Port</label>
      <input type="number" id="proxy-port" value="" placeholder="9090">
    </div>
  </div>

  <div class="btn-row">
    <button class="btn btn-enable" id="btn-enable" onclick="enableProxy()">Enable Proxy</button>
    <button class="btn btn-disable" id="btn-disable" onclick="disableProxy()">Disable Proxy</button>
  </div>

  <div class="results" id="results">
    <p class="section-title" id="results-title">Results</p>
    <div id="results-body"></div>
  </div>
</div>

<script>
  let refreshTimer;

  async function fetchStatus() {
    try {
      const resp = await fetch('/api/status');
      const data = await resp.json();

      document.getElementById('mac-ip').textContent = data.ip;
      document.getElementById('proxy-port').placeholder = data.port;

      const adbEl = document.getElementById('adb-status');
      if (data.adb) { adbEl.textContent = 'Connected'; adbEl.className = ''; }
      else { adbEl.textContent = 'Not found'; adbEl.className = 'warn'; }

      document.getElementById('device-count').textContent = data.devices.length;

      const list = document.getElementById('device-list');
      if (data.devices.length === 0) {
        list.innerHTML = '<div class="no-devices">No devices connected</div>';
      } else {
        list.innerHTML = data.devices.map(d =>
          `<div class="device-row">
            <div class="device-dot"></div>
            <span class="device-model">${esc(d.model)}</span>
            <span class="device-serial">${esc(d.serial)}</span>
          </div>`
        ).join('');
      }

      // Pre-fill IP only if user hasn't typed anything
      const ipInput = document.getElementById('proxy-ip');
      if (!ipInput.dataset.touched) {
        ipInput.value = data.ip;
      }
      const portInput = document.getElementById('proxy-port');
      if (!portInput.value) {
        portInput.value = data.port;
      }
    } catch (e) {
      console.error('Status fetch failed', e);
    }
  }

  document.getElementById('proxy-ip').addEventListener('input', function() {
    this.dataset.touched = '1';
  });

  async function enableProxy() {
    const ip = document.getElementById('proxy-ip').value.trim();
    const port = parseInt(document.getElementById('proxy-port').value) || 9090;
    if (!ip) { alert('Please enter a proxy IP address.'); return; }
    await doAction('/api/proxy/enable', { ip, port }, 'Enable Proxy');
  }

  async function disableProxy() {
    await doAction('/api/proxy/disable', {}, 'Disable Proxy');
  }

  async function doAction(url, body, label) {
    const btnEn = document.getElementById('btn-enable');
    const btnDis = document.getElementById('btn-disable');
    btnEn.disabled = btnDis.disabled = true;

    const resDiv = document.getElementById('results');
    const resBody = document.getElementById('results-body');
    const resTitle = document.getElementById('results-title');
    resTitle.textContent = label;
    resBody.innerHTML = '<span class="spinner"></span> Working...';
    resDiv.classList.add('show');

    try {
      const resp = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      });
      const data = await resp.json();

      if (data.error) {
        resBody.innerHTML = `<div class="result-row error">${esc(data.error)}</div>`;
      } else if (data.results) {
        resBody.innerHTML = data.results.map(r => {
          const cls = r.ok ? 'ok' : 'fail';
          const tag = r.ok ? 'OK' : 'FAIL';
          return `<div class="result-row ${cls}">[${tag}] ${esc(r.model)} (${esc(r.serial)}) — ${esc(r.message)}</div>`;
        }).join('');
      }
    } catch (e) {
      resBody.innerHTML = `<div class="result-row error">Request failed: ${esc(e.message)}</div>`;
    }

    btnEn.disabled = btnDis.disabled = false;
    fetchStatus();
  }

  function esc(s) {
    const d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }

  // Initial load + auto-refresh every 5s
  fetchStatus();
  refreshTimer = setInterval(fetchStatus, 5000);
</script>
</body>
</html>
"""

# ── HTTP Handler ─────────────────────────────────────────────────────────────

class ProxyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self._serve_html()
        elif self.path == "/api/status":
            self._handle_status()
        else:
            self._send_json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path == "/api/proxy/enable":
            self._handle_enable()
        elif self.path == "/api/proxy/disable":
            self._handle_disable()
        else:
            self._send_json({"error": "not found"}, 404)

    # ── Routes ───────────────────────────────────────────────────────────

    def _serve_html(self):
        body = HTML_PAGE.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _handle_status(self):
        devices = get_connected_android_devices()
        self._send_json({
            "ip": get_local_ip(),
            "port": DEFAULT_PROXY_PORT,
            "adb": check_adb(),
            "devices": [{"serial": s, "model": m} for s, m in devices],
        })

    def _handle_enable(self):
        data = self._read_json()
        if data is None:
            return
        ip = data.get("ip", "").strip()
        port = data.get("port", DEFAULT_PROXY_PORT)
        if not ip:
            self._send_json({"error": "Missing 'ip' field"}, 400)
            return
        try:
            port = int(port)
        except (TypeError, ValueError):
            self._send_json({"error": "Invalid port"}, 400)
            return

        results = android_set_proxy(ip, port)
        if results is None:
            if not check_adb():
                self._send_json({"error": "adb not found on PATH"})
            else:
                self._send_json({"error": "No connected Android devices"})
            return
        self._send_json({"results": results})

    def _handle_disable(self):
        results = android_clear_proxy()
        if results is None:
            if not check_adb():
                self._send_json({"error": "adb not found on PATH"})
            else:
                self._send_json({"error": "No connected Android devices"})
            return
        self._send_json({"results": results})

    # ── Helpers ──────────────────────────────────────────────────────────

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length)
            return json.loads(raw) if raw else {}
        except (json.JSONDecodeError, ValueError):
            self._send_json({"error": "Invalid JSON"}, 400)
            return None

    def _send_json(self, obj, status=200):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Quieter log: just method + path
        sys.stderr.write(f"  {args[0]}\n")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    ip = get_local_ip()
    print(f"\n  Proxy Setup Web UI")
    print(f"  ──────────────────")
    print(f"  Mac IP : {ip}")
    print(f"  ADB    : {'available' if check_adb() else 'NOT FOUND'}")
    print(f"  Server : http://localhost:{PORT}")
    print(f"\n  Press Ctrl+C to stop.\n")

    server = HTTPServer((HOST, PORT), ProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
