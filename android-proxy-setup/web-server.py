#!/usr/bin/env python3
"""
Web UI for Android Proxy Setup.
Serves a browser-based frontend and JSON API on localhost:8080.

Reuses proxy logic from proxy-setup.py.
"""

import importlib
import json
import logging
import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

# Import proxy-setup.py as a module (hyphen in filename requires importlib)
proxy_setup = importlib.import_module("proxy-setup")

get_local_ip = proxy_setup.get_local_ip
check_adb = proxy_setup.check_adb
get_connected_android_devices = proxy_setup.get_connected_android_devices
android_set_proxy = proxy_setup.android_set_proxy
android_set_proxy_usb = proxy_setup.android_set_proxy_usb
android_clear_proxy = proxy_setup.android_clear_proxy
android_delete_proxy = proxy_setup.android_delete_proxy
android_get_proxy_state = proxy_setup.android_get_proxy_state
check_proxy_health = proxy_setup.check_proxy_health
DEFAULT_PROXY_PORT = proxy_setup.DEFAULT_PROXY_PORT

HOST = "0.0.0.0"
PORT = 8081

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css":  "text/css; charset=utf-8",
    ".js":   "application/javascript; charset=utf-8",
}

# ── Logging ───────────────────────────────────────────────────────────────────

log = logging.getLogger("proxy-web")
log.setLevel(logging.INFO)
_handler = logging.StreamHandler(sys.stderr)
_handler.setFormatter(logging.Formatter("  %(asctime)s  %(message)s", datefmt="%H:%M:%S"))
log.addHandler(_handler)

# ── HTTP Handler ─────────────────────────────────────────────────────────────

class ProxyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self._serve_static("index.html")
        elif self.path.startswith("/static/"):
            filename = self.path[len("/static/"):]
            self._serve_static(filename)
        elif self.path == "/api/status":
            self._handle_status()
        else:
            self._send_json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path == "/api/proxy/enable":
            self._handle_enable()
        elif self.path == "/api/proxy/disable":
            self._handle_disable()
        elif self.path == "/api/proxy/delete":
            self._handle_delete()
        else:
            self._send_json({"error": "not found"}, 404)

    # ── Static file serving ───────────────────────────────────────────────

    def _serve_static(self, filename):
        # Block path traversal
        if ".." in filename or filename.startswith("/"):
            self._send_json({"error": "forbidden"}, 403)
            return

        filepath = os.path.join(STATIC_DIR, filename)
        if not os.path.isfile(filepath):
            self._send_json({"error": "not found"}, 404)
            return

        ext = os.path.splitext(filename)[1].lower()
        content_type = CONTENT_TYPES.get(ext, "application/octet-stream")

        with open(filepath, "rb") as f:
            body = f.read()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # ── API Routes ────────────────────────────────────────────────────────

    def _handle_status(self):
        devices = get_connected_android_devices()
        mac_ip = get_local_ip()
        device_list = []
        for serial, model in devices:
            health = check_proxy_health(serial, mac_ip)
            device_list.append({
                "serial": serial,
                "model": model,
                "proxy": health["proxy"],
                "health": health["status"],
                "issue": health["issue"],
            })
        self._send_json({
            "ip": mac_ip,
            "port": DEFAULT_PROXY_PORT,
            "adb": check_adb(),
            "devices": device_list,
        })

    def _handle_enable(self):
        data = self._read_json()
        if data is None:
            return
        usb = data.get("usb", False)
        port = data.get("port", DEFAULT_PROXY_PORT)
        try:
            port = int(port)
        except (TypeError, ValueError):
            self._send_json({"error": "Invalid port"}, 400)
            return

        if usb:
            log.info("ENABLE PROXY (USB)  ->  127.0.0.1:%d", port)
            results = android_set_proxy_usb(port)
        else:
            ip = data.get("ip", "").strip()
            if not ip:
                self._send_json({"error": "Missing 'ip' field"}, 400)
                return
            log.info("ENABLE PROXY  ->  %s:%d", ip, port)
            results = android_set_proxy(ip, port)
        if results is None:
            if not check_adb():
                self._send_json({"error": "adb not found on PATH"})
            else:
                self._send_json({"error": "No connected Android devices"})
            return
        for r in results:
            tag = "OK" if r["ok"] else "FAIL"
            log.info("  [%s] %s (%s) - %s", tag, r["model"], r["serial"], r["message"])
        self._send_json({"results": results})

    def _handle_disable(self):
        log.info("DISABLE PROXY  (set to :0)")
        results = android_clear_proxy()
        if results is None:
            if not check_adb():
                self._send_json({"error": "adb not found on PATH"})
            else:
                self._send_json({"error": "No connected Android devices"})
            return
        for r in results:
            tag = "OK" if r["ok"] else "FAIL"
            log.info("  [%s] %s (%s) - %s", tag, r["model"], r["serial"], r["message"])
        self._send_json({"results": results})

    def _handle_delete(self):
        log.info("DELETE PROXY  (full removal)")
        results = android_delete_proxy()
        if results is None:
            if not check_adb():
                self._send_json({"error": "adb not found on PATH"})
            else:
                self._send_json({"error": "No connected Android devices"})
            return
        for r in results:
            tag = "OK" if r["ok"] else "FAIL"
            log.info("  [%s] %s (%s) - %s", tag, r["model"], r["serial"], r["message"])
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
        # Suppress default HTTP request logs (noisy status polls every 5s)
        pass


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    ip = get_local_ip()
    devices = get_connected_android_devices()
    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║       📱  Proxy Setup Web UI  📱        ║")
    print("  ╠══════════════════════════════════════════╣")
    print(f"  ║  Mac IP   : {ip:<28s}║")
    print(f"  ║  ADB      : {'✅ available' if check_adb() else '❌ NOT FOUND':<28s}║")
    print(f"  ║  Devices  : {str(len(devices)) + ' connected':<28s}║")
    print(f"  ║  Server   : {'http://localhost:' + str(PORT):<28s}║")
    print("  ╚══════════════════════════════════════════╝")
    print()
    log.info("Server started — press Ctrl+C to stop")
    print()

    server = HTTPServer((HOST, PORT), ProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("Server stopped")
        server.server_close()


if __name__ == "__main__":
    main()
