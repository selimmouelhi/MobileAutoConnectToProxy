#!/usr/bin/env python3
"""
Proxy Auto-Setup Tool for Android Test Devices
Automates Proxyman proxy configuration on Android devices via ADB.

Requirements:
  - adb (Android platform-tools)
"""

import os
import shutil
import socket
import subprocess
import textwrap


# ── Config ───────────────────────────────────────────────────────────────────

DEFAULT_PROXY_PORT = 9090


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
        model = "unknown"
        for part in parts[1:]:
            if part.startswith("model:"):
                model = part.split(":", 1)[1]
                break
        devices.append((serial, model))
    return devices


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


# ── Main menu ────────────────────────────────────────────────────────────────

def print_header(proxy_host, proxy_port):
    print("\n" + "=" * 56)
    print("   Proxy Auto-Setup Tool for Android Test Devices")
    print("=" * 56)
    print(f"   Mac IP      : {proxy_host}")
    print(f"   Proxy Port  : {proxy_port}")
    print("-" * 56)


def main():
    proxy_host = get_local_ip()
    proxy_port = DEFAULT_PROXY_PORT

    if os.environ.get("PROXY_HOST"):
        proxy_host = os.environ["PROXY_HOST"]
    if os.environ.get("PROXY_PORT"):
        proxy_port = int(os.environ["PROXY_PORT"])

    while True:
        print_header(proxy_host, proxy_port)
        print("""
   1) Set Proxy              (fully automated via adb)
   2) Clear Proxy            (fully automated via adb)
   3) ADB Wireless Connect   (pair & connect devices over Wi-Fi)

   4) Change proxy IP
   5) Change proxy port
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
            try:
                new_ip = input(f"  Enter new proxy IP [{proxy_host}]: ").strip()
                if new_ip:
                    proxy_host = new_ip
                    print(f"  Proxy IP updated to {proxy_host}")
                else:
                    print("  Keeping current IP.")
            except (KeyboardInterrupt, EOFError):
                print("  Keeping current IP.")
        elif choice == "5":
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
