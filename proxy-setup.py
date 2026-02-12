#!/usr/bin/env python3
"""
Proxy Auto-Setup Tool for Test Devices
Automates Proxyman proxy configuration on Android & iOS devices.
No external dependencies - stdlib only.
"""

import http.server
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import textwrap
import threading
import uuid


# ── Config ───────────────────────────────────────────────────────────────────

DEFAULT_PROXY_PORT = 9090
MOBILECONFIG_SERVER_PORT = 8888


# ── Utility helpers ──────────────────────────────────────────────────────────

def get_local_ip():
    """Return the Mac's local IP on the active interface."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except OSError:
        return "127.0.0.1"


def check_adb():
    """Return True if adb is available on PATH."""
    return shutil.which("adb") is not None


def get_connected_android_devices():
    """Return list of (serial, model_name) for connected Android devices."""
    try:
        result = subprocess.run(
            ["adb", "devices", "-l"],
            capture_output=True, text=True, timeout=10,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return []

    devices = []
    for line in result.stdout.strip().splitlines()[1:]:
        line = line.strip()
        if not line or "offline" in line or "unauthorized" in line:
            continue
        parts = line.split()
        serial = parts[0]
        # Try to extract model name from the device descriptor
        model = "unknown"
        for part in parts[1:]:
            if part.startswith("model:"):
                model = part.split(":", 1)[1]
                break
        devices.append((serial, model))
    return devices


# ── ASCII QR code generator (no dependencies) ───────────────────────────────

def _qr_encode_numeric(data):
    """Minimal QR-like encoding – we generate a simple visual QR using
    box-drawing characters.  For a real QR code we'd need a full encoder,
    so instead we produce a framed ASCII art block that *looks* like a QR
    code but actually just displays the URL prominently.  iOS users will
    type the short URL or copy-paste it.
    """
    # We'll generate a genuine (minimal) QR Code using the standard algorithm
    # for alphanumeric mode – but that's 800+ lines.  Instead, generate a
    # simple framed text block that is easy to scan visually.
    return None  # signal caller to use the simple display


def generate_ascii_qr(url):
    """Generate an ASCII QR code for *url* using only stdlib.

    Uses a compact binary matrix approach implementing QR Code Model 2,
    Version 2 (25x25), with alphanumeric encoding.  Since a full QR encoder
    is complex, we take a pragmatic shortcut: use the `qrcode` library if
    available, otherwise fall back to a clear visual frame with the URL.
    """
    # Try the optional qrcode lib first (pip install qrcode)
    try:
        import qrcode  # type: ignore
        qr = qrcode.QRCode(box_size=1, border=1)
        qr.add_data(url)
        qr.make(fit=True)
        matrix = qr.get_matrix()
        lines = []
        for row in matrix:
            line = ""
            for cell in row:
                line += "\u2588\u2588" if cell else "  "
            lines.append(line)
        return "\n".join(lines)
    except ImportError:
        pass

    # Fallback: framed URL display
    width = max(len(url) + 4, 40)
    border = "\u2588" * width
    empty = "\u2588" + " " * (width - 2) + "\u2588"
    pad = (width - 2 - len(url)) // 2
    url_line = "\u2588" + " " * pad + url + " " * (width - 2 - pad - len(url)) + "\u2588"
    return "\n".join([
        border, empty, url_line, empty, border,
        "",
        "  (Install 'pip install qrcode' for a real QR code)",
    ])


# ── .mobileconfig profile generation ────────────────────────────────────────

def generate_mobileconfig(proxy_host, proxy_port):
    """Return XML string for a .mobileconfig profile that sets HTTP/HTTPS proxy."""
    payload_uuid = str(uuid.uuid4()).upper()
    profile_uuid = str(uuid.uuid4()).upper()

    return textwrap.dedent(f"""\
        <?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
          "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
        <plist version="1.0">
        <dict>
            <key>PayloadContent</key>
            <array>
                <dict>
                    <key>PayloadType</key>
                    <string>com.apple.wifi.managed</string>
                    <key>PayloadVersion</key>
                    <integer>1</integer>
                    <key>PayloadIdentifier</key>
                    <string>com.proxyman.proxy.wifi.{payload_uuid}</string>
                    <key>PayloadUUID</key>
                    <string>{payload_uuid}</string>
                    <key>PayloadDisplayName</key>
                    <string>Proxyman Wi-Fi Proxy</string>
                    <key>ProxyType</key>
                    <string>Manual</string>
                    <key>ProxyServer</key>
                    <string>{proxy_host}</string>
                    <key>ProxyServerPort</key>
                    <integer>{proxy_port}</integer>
                    <key>ProxyPACFallbackAllowed</key>
                    <false/>
                </dict>
            </array>
            <key>PayloadDisplayName</key>
            <string>Proxyman Proxy ({proxy_host}:{proxy_port})</string>
            <key>PayloadIdentifier</key>
            <string>com.proxyman.proxy.profile.{profile_uuid}</string>
            <key>PayloadUUID</key>
            <string>{profile_uuid}</string>
            <key>PayloadType</key>
            <string>Configuration</string>
            <key>PayloadVersion</key>
            <integer>1</integer>
            <key>PayloadRemovalDisallowed</key>
            <false/>
            <key>PayloadDescription</key>
            <string>Sets HTTP proxy to {proxy_host}:{proxy_port} for Proxyman interception.</string>
        </dict>
        </plist>
    """)


# ── Temporary HTTP server for .mobileconfig ─────────────────────────────────

class MobileConfigHandler(http.server.BaseHTTPRequestHandler):
    """Serves the .mobileconfig file at any path."""

    profile_data = b""

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/x-apple-aspen-config")
        self.send_header("Content-Disposition", 'attachment; filename="proxyman-proxy.mobileconfig"')
        self.send_header("Content-Length", str(len(self.profile_data)))
        self.end_headers()
        self.wfile.write(self.profile_data)

    def log_message(self, format, *args):
        # Suppress default logging to keep output clean
        pass


def start_profile_server(proxy_host, proxy_port):
    """Start a temporary HTTP server serving the .mobileconfig profile.
    Returns (server, thread) so caller can shut it down.
    """
    profile_xml = generate_mobileconfig(proxy_host, proxy_port)
    MobileConfigHandler.profile_data = profile_xml.encode("utf-8")

    server = http.server.HTTPServer(("0.0.0.0", MOBILECONFIG_SERVER_PORT), MobileConfigHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


# ── ADB wireless connect ─────────────────────────────────────────────────────

def adb_wireless_connect():
    """Interactively pair and/or connect Android devices over Wi-Fi (ADB wireless)."""
    if not check_adb():
        print("\n  [!] adb not found on PATH. Install Android platform-tools first.")
        return

    print(textwrap.dedent("""
      ADB Wireless Connect
      --------------------
      Prerequisites:
        - Device and Mac must be on the same Wi-Fi network
        - On the device: Settings > Developer Options > Wireless debugging > ON

      Options:
        a) Pair a new device   (first time only — needs pairing code)
        b) Connect to a device (already paired — just needs IP:port)
        c) List connected devices
        d) Back to main menu
    """))

    try:
        sub = input("  Select: ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        return

    if sub == "a":
        _adb_pair()
    elif sub == "b":
        _adb_connect()
    elif sub == "c":
        _adb_list()
    elif sub == "d":
        return
    else:
        print("  Invalid option.")


def _adb_pair():
    """Pair with a new device using ADB wireless pairing."""
    print(textwrap.dedent("""
      On the device, go to:
        Settings > Developer Options > Wireless debugging > Pair device with pairing code

      You'll see an IP:port and a 6-digit pairing code.
    """))
    try:
        addr = input("  Enter pairing IP:port (e.g. 192.168.4.50:37123): ").strip()
        if not addr:
            print("  Cancelled.")
            return
        code = input("  Enter 6-digit pairing code: ").strip()
        if not code:
            print("  Cancelled.")
            return
    except (KeyboardInterrupt, EOFError):
        return

    print(f"\n  Pairing with {addr}...")
    try:
        result = subprocess.run(
            ["adb", "pair", addr, code],
            capture_output=True, text=True, timeout=15,
        )
        output = (result.stdout + result.stderr).strip()
        if result.returncode == 0 and "Successfully" in output:
            print(f"  [OK] {output}")
            print("\n  Now use option (b) to connect to the device's wireless debugging port.")
        else:
            print(f"  [FAIL] {output}")
    except subprocess.TimeoutExpired:
        print("  [FAIL] Pairing timed out.")


def _adb_connect():
    """Connect to an already-paired device."""
    print(textwrap.dedent("""
      On the device, check the IP:port shown under:
        Settings > Developer Options > Wireless debugging
      (This is the *connection* port, NOT the pairing port.)
    """))
    try:
        addr = input("  Enter device IP:port (e.g. 192.168.4.50:41567): ").strip()
        if not addr:
            print("  Cancelled.")
            return
    except (KeyboardInterrupt, EOFError):
        return

    print(f"\n  Connecting to {addr}...")
    try:
        result = subprocess.run(
            ["adb", "connect", addr],
            capture_output=True, text=True, timeout=10,
        )
        output = (result.stdout + result.stderr).strip()
        if "connected" in output.lower():
            print(f"  [OK] {output}")
        else:
            print(f"  [FAIL] {output}")
    except subprocess.TimeoutExpired:
        print("  [FAIL] Connection timed out.")


def _adb_list():
    """List all currently connected ADB devices."""
    devices = get_connected_android_devices()
    if not devices:
        print("\n  No devices connected.")
    else:
        print(f"\n  Connected devices ({len(devices)}):\n")
        for serial, model in devices:
            print(f"    - {model} ({serial})")


# ── Android actions ──────────────────────────────────────────────────────────

def android_set_proxy(proxy_host, proxy_port):
    """Set HTTP proxy on all connected Android devices via adb."""
    if not check_adb():
        print("\n  [!] adb not found on PATH. Install Android platform-tools first.")
        return

    devices = get_connected_android_devices()
    if not devices:
        print("\n  [!] No connected Android devices found.")
        print("      Make sure USB debugging is enabled and the device is connected.")
        return

    print(f"\n  Found {len(devices)} device(s):\n")
    proxy_value = f"{proxy_host}:{proxy_port}"

    for serial, model in devices:
        try:
            result = subprocess.run(
                ["adb", "-s", serial, "shell", "settings", "put", "global", "http_proxy", proxy_value],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                print(f"    [OK] {model} ({serial}) -> proxy set to {proxy_value}")
            else:
                print(f"    [FAIL] {model} ({serial}) -> {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            print(f"    [FAIL] {model} ({serial}) -> timed out")


def android_clear_proxy():
    """Clear HTTP proxy on all connected Android devices."""
    if not check_adb():
        print("\n  [!] adb not found on PATH. Install Android platform-tools first.")
        return

    devices = get_connected_android_devices()
    if not devices:
        print("\n  [!] No connected Android devices found.")
        return

    print(f"\n  Clearing proxy on {len(devices)} device(s):\n")

    for serial, model in devices:
        try:
            # Delete then set to :0 for a thorough cleanup
            subprocess.run(
                ["adb", "-s", serial, "shell", "settings", "delete", "global", "http_proxy"],
                capture_output=True, text=True, timeout=10,
            )
            result = subprocess.run(
                ["adb", "-s", serial, "shell", "settings", "put", "global", "http_proxy", ":0"],
                capture_output=True, text=True, timeout=10,
            )
            if result.returncode == 0:
                print(f"    [OK] {model} ({serial}) -> proxy cleared")
                print(f"         (toggle Wi-Fi on the device if proxy still shows in Wi-Fi settings)")
            else:
                print(f"    [FAIL] {model} ({serial}) -> {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            print(f"    [FAIL] {model} ({serial}) -> timed out")


# ── iOS actions ──────────────────────────────────────────────────────────────

def ios_set_proxy(proxy_host, proxy_port):
    """Generate .mobileconfig profile and serve it via temporary HTTP server."""
    url = f"http://{proxy_host}:{MOBILECONFIG_SERVER_PORT}"

    print(f"\n  Starting profile server on port {MOBILECONFIG_SERVER_PORT}...")

    try:
        server, thread = start_profile_server(proxy_host, proxy_port)
    except OSError as e:
        print(f"\n  [!] Could not start server: {e}")
        print(f"      Is port {MOBILECONFIG_SERVER_PORT} already in use?")
        return

    print(f"\n  Profile server is running!\n")
    print(f"  On each iOS device, open Safari and visit:\n")
    print(f"    {url}\n")

    # Show QR code
    qr = generate_ascii_qr(url)
    for line in qr.split("\n"):
        print(f"    {line}")

    print(f"\n  Then go to: Settings > General > VPN & Device Management")
    print(f"  Tap the 'Proxyman Proxy' profile and tap Install.\n")

    try:
        input("  Press Enter to stop the server when done... ")
    except (KeyboardInterrupt, EOFError):
        pass

    server.shutdown()
    print("  Server stopped.")


def ios_remove_proxy():
    """Print instructions for removing the proxy profile on iOS."""
    print(textwrap.dedent("""
      To remove the proxy on each iOS device:

        1. Open Settings
        2. Go to General > VPN & Device Management
        3. Tap "Proxyman Proxy" profile
        4. Tap "Remove Profile"
        5. Enter passcode if prompted

      Note: iOS does not support remote profile removal without MDM.
      Each device must be manually cleared using the steps above.
    """))


# ── Main menu ────────────────────────────────────────────────────────────────

def print_header(proxy_host, proxy_port):
    print("\n" + "=" * 56)
    print("   Proxy Auto-Setup Tool for Test Devices")
    print("=" * 56)
    print(f"   Mac IP      : {proxy_host}")
    print(f"   Proxy Port  : {proxy_port}")
    print("-" * 56)


def main():
    proxy_host = get_local_ip()
    proxy_port = DEFAULT_PROXY_PORT

    # Allow overriding via env vars
    if os.environ.get("PROXY_HOST"):
        proxy_host = os.environ["PROXY_HOST"]
    if os.environ.get("PROXY_PORT"):
        proxy_port = int(os.environ["PROXY_PORT"])

    while True:
        print_header(proxy_host, proxy_port)
        print("""
   1) Android: Set Proxy       (fully automated via adb)
   2) Android: Clear Proxy     (fully automated via adb)
   3) Android: ADB Wireless    (pair & connect devices over Wi-Fi)
   4) iOS: Set Proxy            (install .mobileconfig profile)
   5) iOS: Remove Proxy         (manual instructions)

   6) Change proxy IP
   7) Change proxy port
   q) Quit
        """)

        try:
            choice = input("  Select an option: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Bye!")
            break

        if choice == "1":
            android_set_proxy(proxy_host, proxy_port)
        elif choice == "2":
            android_clear_proxy()
        elif choice == "3":
            adb_wireless_connect()
        elif choice == "4":
            ios_set_proxy(proxy_host, proxy_port)
        elif choice == "5":
            ios_remove_proxy()
        elif choice == "6":
            try:
                new_ip = input(f"  Enter new proxy IP [{proxy_host}]: ").strip()
                if new_ip:
                    proxy_host = new_ip
                    print(f"  Proxy IP updated to {proxy_host}")
                else:
                    print("  Keeping current IP.")
            except (KeyboardInterrupt, EOFError):
                print("  Keeping current IP.")
        elif choice == "7":
            try:
                new_port = input("  Enter new proxy port: ").strip()
                proxy_port = int(new_port)
                print(f"  Proxy port updated to {proxy_port}")
            except (ValueError, KeyboardInterrupt, EOFError):
                print("  Invalid port, keeping current value.")
        elif choice == "q":
            print("\n  Bye!")
            break
        else:
            print("\n  Invalid option. Try again.")

        print()


if __name__ == "__main__":
    main()
