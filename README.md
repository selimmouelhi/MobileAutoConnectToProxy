# Android Proxy Auto-Setup Tool

Automates Proxyman proxy configuration on Android devices via ADB. Available as a **CLI tool** and a **Web UI**.

## Prerequisites

- **Python 3.8+**
- **ADB** (Android Debug Bridge) installed and on your PATH
  ```bash
  brew install android-platform-tools
  ```
- **Android device** with Developer Options and USB/Wireless debugging enabled

## Setup: Connect a Device via Wireless ADB

1. On your Android device, go to **Settings > Developer Options > Wireless debugging** and turn it **ON**.

2. Make sure your Mac and Android device are on the **same Wi-Fi network**.

3. **Pair the device** (first time only):
   - On the device, tap **Pair device with pairing code** — note the IP:port and 6-digit code.
   - On your Mac:
     ```bash
     adb pair <IP>:<PAIRING_PORT>
     ```
     Enter the 6-digit code when prompted.

4. **Connect to the device**:
   - On the device, note the IP:port shown under **Wireless debugging** (this is the *connection* port, not the pairing port).
   - On your Mac:
     ```bash
     adb connect <IP>:<CONNECTION_PORT>
     ```

5. **Verify the connection**:
   ```bash
   adb devices -l
   ```
   You should see your device listed.

> You can also use the CLI tool's **ADB Wireless Connect** menu (option 3) to do the pairing and connection interactively.

## Option A: Web UI (Recommended)

A browser-based interface for enabling/disabling proxy on connected devices.

### Run the server

```bash
python3 web-server.py
```

### Open the UI

Go to **http://localhost:8080** in your browser.

### Usage

1. The UI auto-detects your Mac's IP, connected devices, and ADB status.
2. Adjust the **Proxy IP** and **Port** if needed (defaults to your Mac's IP and port 9090).
3. Click **Enable Proxy** to set the proxy on all connected devices.
4. Click **Disable Proxy** to clear the proxy from all devices.
5. Results are shown per-device after each action.

> The device list auto-refreshes every 5 seconds.

## Option B: CLI Tool

A terminal-based menu for the same functionality plus interactive ADB wireless connect.

### Run

```bash
python3 proxy-setup.py
```

### Menu options

| Option | Description |
|--------|-------------|
| 1 | Set proxy on all connected Android devices |
| 2 | Clear proxy on all connected Android devices |
| 3 | ADB Wireless Connect (pair & connect over Wi-Fi) |
| 4 | Change proxy IP |
| 5 | Change proxy port |
| q | Quit |

### Environment variables (optional)

Override the default proxy IP or port:

```bash
PROXY_HOST=192.168.1.100 PROXY_PORT=8888 python3 proxy-setup.py
```

## Troubleshooting

- **"adb not found"** — Install Android platform-tools: `brew install android-platform-tools`
- **No devices showing** — Make sure USB/wireless debugging is enabled and the device is connected (`adb devices -l`)
- **Proxy still showing in Wi-Fi settings after clearing** — Toggle Wi-Fi off and on on the device
- **Wireless pairing fails** — Ensure both devices are on the same network and the pairing code hasn't expired (it refreshes every ~30 seconds)
