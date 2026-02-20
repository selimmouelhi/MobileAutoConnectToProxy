let refreshTimer;
let connectionMode = 'wifi';
let currentMacIp = '';
let currentMacPort = 9090;

function esc(s) {
  const d = document.createElement('div');
  d.textContent = s;
  return d.innerHTML;
}

function setMode(mode) {
  connectionMode = mode;
  document.getElementById('mode-wifi').className = 'toggle-btn' + (mode === 'wifi' ? ' active' : '');
  document.getElementById('mode-usb').className = 'toggle-btn' + (mode === 'usb' ? ' active' : '');
  document.getElementById('mode-hint').textContent =
    mode === 'usb' ? 'Routes traffic over USB cable (adb reverse)' : 'Routes traffic over Wi-Fi network';
  document.getElementById('ip-row').style.display = mode === 'usb' ? 'none' : 'flex';
}

function updateBanner(devices, macIp, macPort) {
  const banner = document.getElementById('state-banner');
  if (!devices || devices.length === 0) {
    banner.className = 'state-banner state-nodevices';
    banner.innerHTML = '<span class="emoji">\u{1F4F1}</span><span class="label">No devices connected</span>';
    return;
  }

  // Check for unhealthy devices first (stale IP or missing tunnel)
  const sick = devices.filter(d => d.health === 'stale' || d.health === 'no_tunnel');
  if (sick.length > 0) {
    const d = sick[0];
    banner.className = 'state-banner state-stale';
    banner.innerHTML =
      `<span class="emoji">\u26A0\uFE0F</span>` +
      `<span class="label">Stale Proxy <span class="detail">${esc(d.issue)}</span></span>` +
      `<button class="banner-fix-btn" onclick="autoFixProxy()">Fix Now</button>`;
    return;
  }

  const states = devices.map(d => {
    if (d.proxy === null) return 'clean';
    if (d.proxy === ':0') return 'disabled';
    return 'enabled';
  });

  const unique = [...new Set(states)];

  if (unique.length === 1) {
    const s = unique[0];
    if (s === 'enabled') {
      const proxyVal = devices[0].proxy;
      const isUsb = proxyVal && proxyVal.startsWith('127.0.0.1');
      banner.className = 'state-banner state-enabled';
      banner.innerHTML = `<span class="emoji pulse">\u{1F6E1}\uFE0F</span><span class="label">Proxy Enabled${isUsb ? ' (USB)' : ''} <span class="detail">${esc(proxyVal)}</span></span>`;
    } else if (s === 'disabled') {
      banner.className = 'state-banner state-disabled';
      banner.innerHTML = '<span class="emoji">\u{1F6D1}</span><span class="label">Proxy Disabled <span class="detail">setting exists as :0</span></span>';
    } else {
      banner.className = 'state-banner state-clean';
      banner.innerHTML = '<span class="emoji">\u2705</span><span class="label">No Proxy Set <span class="detail">clean state</span></span>';
    }
  } else {
    banner.className = 'state-banner state-mixed';
    banner.innerHTML = '<span class="emoji">\u26A0\uFE0F</span><span class="label">Mixed State <span class="detail">devices have different proxy settings</span></span>';
  }
}

function proxyBadge(device) {
  if (device.proxy === null) {
    return '<span class="device-badge badge-clean">no proxy</span>';
  }
  if (device.proxy === ':0') {
    return '<span class="device-badge badge-disabled">disabled</span>';
  }
  if (device.health === 'stale' || device.health === 'no_tunnel') {
    return `<span class="device-badge badge-stale">${esc(device.proxy)} — stale</span>`;
  }
  return `<span class="device-badge badge-enabled">${esc(device.proxy)}</span>`;
}

async function fetchStatus() {
  try {
    const resp = await fetch('/api/status');
    const data = await resp.json();

    currentMacIp = data.ip;
    currentMacPort = data.port;

    document.getElementById('mac-ip').textContent = data.ip;
    document.getElementById('proxy-port').placeholder = data.port;

    const adbEl = document.getElementById('adb-status');
    if (data.adb) { adbEl.textContent = 'Connected'; adbEl.className = ''; }
    else { adbEl.textContent = 'Not found'; adbEl.className = 'warn'; }

    document.getElementById('device-count').textContent = data.devices.length;

    updateBanner(data.devices, data.ip, data.port);

    const list = document.getElementById('device-list');
    if (data.devices.length === 0) {
      list.innerHTML = '<div class="no-devices">No devices connected</div>';
    } else {
      list.innerHTML = data.devices.map(d =>
        `<div class="device-row">
          <div class="device-dot ${d.health === 'stale' || d.health === 'no_tunnel' ? 'dot-warn' : ''}"></div>
          <div class="device-info">
            <span class="device-model">${esc(d.model)}</span>
            <span class="device-serial">${esc(d.serial)}</span>
          </div>
          ${proxyBadge(d)}
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
  const port = parseInt(document.getElementById('proxy-port').value) || 9090;
  if (connectionMode === 'usb') {
    await doAction('/api/proxy/enable', { usb: true, port }, 'Enable Proxy (USB)');
  } else {
    const ip = document.getElementById('proxy-ip').value.trim();
    if (!ip) { alert('Please enter a proxy IP address.'); return; }
    await doAction('/api/proxy/enable', { ip, port }, 'Enable Proxy');
  }
}

async function autoFixProxy() {
  // Re-apply proxy with the Mac's current IP and port
  const port = parseInt(document.getElementById('proxy-port').value) || currentMacPort;
  if (connectionMode === 'usb') {
    await doAction('/api/proxy/enable', { usb: true, port }, 'Auto-Fix Proxy (USB)');
  } else {
    await doAction('/api/proxy/enable', { ip: currentMacIp, port }, 'Auto-Fix Proxy');
  }
}

async function disableProxy() {
  await doAction('/api/proxy/disable', {}, 'Disable Proxy');
}

async function deleteProxy() {
  await doAction('/api/proxy/delete', {}, 'Delete Proxy');
}

async function doAction(url, body, label) {
  const btnEn = document.getElementById('btn-enable');
  const btnDis = document.getElementById('btn-disable');
  const btnDel = document.getElementById('btn-delete');
  btnEn.disabled = btnDis.disabled = btnDel.disabled = true;

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
      const rows = data.results.map(r => {
        const cls = r.ok ? 'ok' : 'fail';
        const tag = r.ok ? 'OK' : 'FAIL';
        return `<div class="result-row ${cls}">[${tag}] ${esc(r.model)} (${esc(r.serial)}) \u2014 ${esc(r.message)}</div>`;
      }).join('');
      const anyOk = data.results.some(r => r.ok);
      const usbHint = (label.includes('USB') && anyOk)
        ? '<div class="usb-hint">\u{1F50C} To remove proxy, just unplug the USB cable. Every time you unplug and replug, you need to enable again.</div>'
        : '';
      resBody.innerHTML = rows + usbHint;
    }
  } catch (e) {
    resBody.innerHTML = `<div class="result-row error">Request failed: ${esc(e.message)}</div>`;
  }

  btnEn.disabled = btnDis.disabled = btnDel.disabled = false;
  fetchStatus();
}

// Initial load + auto-refresh every 5s
fetchStatus();
refreshTimer = setInterval(fetchStatus, 5000);
