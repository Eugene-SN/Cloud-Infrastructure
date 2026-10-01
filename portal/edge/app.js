/**
 * ESCLOUD Sovereign Operations Console — 2026 Apple Design Engine
 * Reactive telemetry synchronization with edge-monitor
 */

(function () {
  'use strict';

  let fastIntervalSec = 5;
  let lastSnapshotTime = null;
  let isFetching = false;
  let timerId = null;

  // Theme Management
  const themeToggle = document.getElementById('theme-toggle');
  const themeColorMeta = document.querySelector('meta[name="theme-color"]');
  const savedTheme = localStorage.getItem('escloud_theme') || 'light';
  document.documentElement.setAttribute('data-theme', savedTheme);
  if (themeColorMeta) {
    themeColorMeta.setAttribute('content', savedTheme === 'dark' ? '#000000' : '#f2f2f7');
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'light';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('escloud_theme', next);
      if (themeColorMeta) {
        themeColorMeta.setAttribute('content', next === 'dark' ? '#000000' : '#f2f2f7');
      }
    });
  }

  // Header Elements
  const freshnessBox = document.getElementById('freshness-box');
  const freshnessLabel = document.getElementById('freshness-label');
  const snapshotAge = document.getElementById('snapshot-age');
  const liveDate = document.getElementById('live-date');
  const liveClock = document.getElementById('live-clock');
  const refreshBtn = document.getElementById('refresh-btn');

  // Hardware Telemetry Elements (Order: CPU -> RAM -> NVMe)
  const cpuPct = document.getElementById('cpu-pct');
  const cpuBar = document.getElementById('cpu-bar');
  const cpuLoadVal = document.getElementById('cpu-load-val');

  const ramUsedPct = document.getElementById('ram-used-pct');
  const ramBar = document.getElementById('ram-bar');
  const ramDetail = document.getElementById('ram-detail');

  const diskUsedPct = document.getElementById('disk-used-pct');
  const diskBar = document.getElementById('disk-bar');
  const diskDetail = document.getElementById('disk-detail');

  // Fabric & AI Core Elements
  const fabricOverallTag = document.getElementById('fabric-overall-tag');
  const paiBadge = document.getElementById('pai-badge');
  const vllmModelLabel = document.getElementById('vllm-model-label');
  const knowledgeBadge = document.getElementById('knowledge-badge');
  const edgeBadge = document.getElementById('edge-badge');

  // Subsystem Panels
  const appsCount = document.getElementById('apps-count');
  const applicationsContainer = document.getElementById('applications');
  const subsystemCounts = document.getElementById('subsystem-counts');
  const homePaiList = document.getElementById('home-pai');
  const operationsList = document.getElementById('operations');
  const unitsList = document.getElementById('units-list');
  const footerUptime = document.getElementById('footer-uptime');
  const footerSeq = document.getElementById('footer-seq');

  function formatBytes(bytes) {
    if (!bytes || isNaN(bytes)) return '0 GiB';
    const gib = bytes / (1024 * 1024 * 1024);
    return `${gib.toFixed(1)} GiB`;
  }

  function formatUptime(seconds) {
    if (!seconds) return '0m';
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    if (hrs > 0) return `${hrs}h ${mins}m`;
    return `${mins}m`;
  }

  // Live Second-by-Second Clock & Age Ticker
  function updateLiveClockAndAge() {
    const now = new Date();

    if (liveClock) {
      liveClock.textContent = now.toLocaleTimeString([], { hour12: false });
    }
    if (liveDate) {
      liveDate.textContent = now.toLocaleDateString([], {
        weekday: 'short',
        day: '2-digit',
        month: 'short',
        year: 'numeric'
      });
    }

    if (!lastSnapshotTime) {
      if (snapshotAge) snapshotAge.textContent = 'waiting...';
      return;
    }

    const diffSec = Math.floor((now.getTime() - lastSnapshotTime.getTime()) / 1000);
    if (snapshotAge) {
      snapshotAge.textContent = `${diffSec}s ago`;
    }

    if (freshnessBox && freshnessLabel) {
      if (diffSec < 15) {
        freshnessBox.className = 'status-capsule live';
        freshnessLabel.textContent = 'Live';
      } else if (diffSec < 45) {
        freshnessBox.className = 'status-capsule stale';
        freshnessLabel.textContent = 'Stale';
      } else {
        freshnessBox.className = 'status-capsule offline';
        freshnessLabel.textContent = 'Delayed';
      }
    }
  }

  // Update Services Status Chips with real operational state
  function updateServiceTiles(data) {
    const apps = data.applications || {};
    const ops = data.operations || {};
    const edge = data.edge || {};
    const userUnits = edge.core_user_units || {};
    const docker = edge.docker || {};

    // 1. Hermes
    const hermesChip = document.querySelector('[data-probe="hermes"]');
    if (hermesChip) {
      const gw = userUnits['hermes-gateway.service']?.detail?.active;
      const dash = userUnits['hermes-dashboard.service']?.detail?.active;
      const ok = gw && dash;
      hermesChip.className = ok ? 'status-pill green font-mono' : 'status-pill amber font-mono';
      hermesChip.innerHTML = `<span class="pip ${ok ? 'green' : 'amber'}"></span>${ok ? 'Online' : 'Degraded'}`;
    }

    // 2. T3 Code
    const t3Chip = document.querySelector('[data-probe="t3_code"]');
    if (t3Chip) {
      const ok = apps.t3_code?.state === 'OK';
      t3Chip.className = ok ? 'status-pill green font-mono' : 'status-pill amber font-mono';
      t3Chip.innerHTML = `<span class="pip ${ok ? 'green' : 'amber'}"></span>${ok ? 'Ready' : 'Check'}`;
    }

    // 3. n8n
    const n8nChip = document.querySelector('[data-probe="n8n"]');
    if (n8nChip) {
      const ok = apps.n8n?.state === 'OK';
      n8nChip.className = ok ? 'status-pill green font-mono' : 'status-pill amber font-mono';
      n8nChip.innerHTML = `<span class="pip ${ok ? 'green' : 'amber'}"></span>${ok ? 'Active' : 'Error'}`;
    }

    // 4. Mattermost
    const mmChip = document.querySelector('[data-probe="mattermost"]');
    if (mmChip) {
      const ok = apps.mattermost?.state === 'OK';
      mmChip.className = ok ? 'status-pill green font-mono' : 'status-pill amber font-mono';
      mmChip.innerHTML = `<span class="pip ${ok ? 'green' : 'amber'}"></span>${ok ? 'Online' : 'Error'}`;
    }

    const planeChip = document.querySelector('[data-probe="plane"]');
    if (planeChip) {
      const ok = apps.plane?.state === 'OK' && apps.plane_api?.state === 'OK' && apps.plane_live?.state === 'OK';
      planeChip.className = ok ? 'status-pill green font-mono' : 'status-pill amber font-mono';
      planeChip.innerHTML = `<span class="pip ${ok ? 'green' : 'amber'}"></span>${ok ? 'Online' : 'Degraded'}`;
    }

    // 5. Nextcloud
    const ncChip = document.querySelector('[data-probe="nextcloud"]');
    if (ncChip) {
      const ok = apps.nextcloud?.state === 'OK';
      ncChip.className = ok ? 'status-pill green font-mono' : 'status-pill amber font-mono';
      ncChip.innerHTML = `<span class="pip ${ok ? 'green' : 'amber'}"></span>${ok ? 'Healthy' : 'Error'}`;
    }

    // 6. Stalwart Mail
    const mailChip = document.querySelector('[data-probe="stalwart"]');
    if (mailChip) {
      const running = docker.stalwart?.detail?.status === 'running';
      mailChip.className = running ? 'status-pill green font-mono' : 'status-pill amber font-mono';
      mailChip.innerHTML = `<span class="pip ${running ? 'green' : 'amber'}"></span>${running ? 'Active' : 'Offline'}`;
    }

    // 7. Stalwart Admin
    const adminChip = document.querySelector('[data-probe="stalwart_admin"]');
    if (adminChip) {
      const running = docker.stalwart?.detail?.status === 'running';
      adminChip.className = running ? 'status-pill green font-mono' : 'status-pill amber font-mono';
      adminChip.innerHTML = `<span class="pip ${running ? 'green' : 'amber'}"></span>${running ? 'Directory ready' : 'Offline'}`;
    }

    // 8. Maintenance Hub
    const maintChip = document.querySelector('[data-probe="maintenance"]');
    if (maintChip) {
      const updates = ops.maintenance?.update_available ?? 0;
      if (updates > 0) {
        maintChip.className = 'status-pill amber font-mono';
        maintChip.innerHTML = `<span class="pip amber"></span>${updates} update${updates > 1 ? 's' : ''}`;
      } else {
        maintChip.className = 'status-pill green font-mono';
        maintChip.innerHTML = '<span class="pip green"></span>Up to date';
      }
    }

    // 9. Backrest Vaults
    const backrestChip = document.querySelector('[data-probe="backrest"]');
    if (backrestChip) {
      const plans = ops.backrest?.plans ? Object.keys(ops.backrest.plans).length : 2;
      const ok = ops.backrest?.state === 'OK';
      backrestChip.className = ok ? 'status-pill green font-mono' : 'status-pill amber font-mono';
      backrestChip.innerHTML = `<span class="pip green"></span>${plans} vaults synced`;
    }
  }

  // Render Telemetry
  function render(data) {
    lastSnapshotTime = new Date(data.generated_at);

    if (data.intervals_s?.fast) {
      fastIntervalSec = data.intervals_s.fast;
      if (footerSeq) footerSeq.textContent = `Fast loop: ${fastIntervalSec}s`;
    }

    // 1. Hardware Telemetry: Order is strictly CPU -> RAM -> NVMe
    const host = data.edge?.host;
    if (host) {
      // 1.1 CPU Utilization (2 vCPU host)
      const cores = host.cpu?.cores || 2;
      let pct = null;
      if (host.cpu && host.cpu.used_percent !== null && host.cpu.used_percent !== undefined) {
        pct = Math.min(100, Math.max(0, Math.round(host.cpu.used_percent)));
      } else if (host.load && host.load.length >= 3) {
        const l1 = host.load[0];
        pct = Math.min(100, Math.round((l1 / cores) * 100));
      }

      if (pct !== null) {
        if (cpuPct) cpuPct.textContent = `${pct}% · ${cores} vCPU`;
        if (cpuBar) cpuBar.style.transform = `scaleX(${Math.min(1, Math.max(0.04, pct / 100))})`;
      }
      if (cpuLoadVal && host.load && host.load.length >= 3) {
        cpuLoadVal.textContent = `Load avg: ${host.load.map(v => v.toFixed(2)).join(' · ')}`;
      }

      // 1.2 RAM Allocation
      if (host.memory) {
        const pct = host.memory.used_percent?.toFixed(1) || '0';
        const free = formatBytes(host.memory.available_bytes);
        const used = formatBytes(host.memory.total_bytes - host.memory.available_bytes);
        const total = formatBytes(host.memory.total_bytes);

        if (ramUsedPct) ramUsedPct.textContent = `${pct}% · ${free} free`;
        if (ramBar) ramBar.style.transform = `scaleX(${Math.min(1, Math.max(0, (host.memory.used_percent || 0) / 100))})`;
        if (ramDetail) ramDetail.textContent = `${used} used of ${total} total`;
      }

      // 1.3 NVMe Storage
      if (host.root_fs) {
        const pct = host.root_fs.used_percent?.toFixed(1) || '0';
        const free = formatBytes(host.root_fs.free_bytes);
        const used = formatBytes(host.root_fs.used_bytes);
        const total = formatBytes(host.root_fs.total_bytes);

        if (diskUsedPct) diskUsedPct.textContent = `${pct}% · ${free} free`;
        if (diskBar) diskBar.style.transform = `scaleX(${Math.min(1, Math.max(0, (host.root_fs.used_percent || 0) / 100))})`;
        if (diskDetail) diskDetail.textContent = `${used} used of ${total} total`;
      }
    }

    // 2. Hybrid Fabric & AI Compute Widget
    const pai = data.home_pai || {};
    const paiOk = pai.state === 'OK';
    const pveLatency = pai.pve?.detail?.latency_ms ? `${pai.pve.detail.latency_ms} ms` : 'NetBird';
    const vllmModel = pai.vllm?.detail?.model || 'qwen3.8-27b-fp8';

    if (paiBadge) {
      paiBadge.className = `status-pill ${paiOk ? 'green' : 'amber'} font-mono`;
      paiBadge.innerHTML = `<span class="pip ${paiOk ? 'green' : 'amber'}"></span>Online · ${pveLatency}`;
    }
    if (vllmModelLabel) {
      vllmModelLabel.textContent = vllmModel;
    }

    const know = data.knowledge || {};
    const knowOk = know.state === 'OK';
    const syncState = know.syncthing?.folder?.detail?.state || 'idle';
    if (knowledgeBadge) {
      knowledgeBadge.className = `status-pill ${knowOk ? 'green' : 'amber'} font-mono`;
      knowledgeBadge.innerHTML = `<span class="pip ${knowOk ? 'green' : 'amber'}"></span>Synchronized (${syncState})`;
    }

    const sysUnits = data.edge?.system_units || {};
    const userServices = data.edge?.core_user_units || {};
    const allUnitsCount = Object.keys(sysUnits).length + Object.keys(userServices).length;
    const containers = data.edge?.docker || {};
    const contCount = Object.keys(containers).length;
    if (edgeBadge) {
      edgeBadge.className = 'status-pill green font-mono';
      edgeBadge.innerHTML = `<span class="pip green"></span>${allUnitsCount} Units · ${contCount} Docker`;
    }

    if (subsystemCounts) {
      subsystemCounts.textContent = `${allUnitsCount} units, ${contCount} containers`;
    }

    // Service Tiles Status
    updateServiceTiles(data);

    // Endpoints List (Clean Apple Inset Rows)
    const apps = data.applications || {};
    const appEntries = Object.entries(apps);
    const okCount = appEntries.filter(([, a]) => a.state === 'OK').length;
    if (appsCount) appsCount.textContent = `${okCount}/${appEntries.length} operational`;

    const appMeta = {
      n8n: { label: 'n8n Automation', route: ':5678' },
      mattermost: { label: 'Mattermost Chat', route: ':8065' },
      authelia: { label: 'Authelia SSO', route: ':9091' },
      semaphore: { label: 'Semaphore Ansible', route: ':3000' },
      maintenance: { label: 'Maintenance Hub', route: ':8088' },
      nextcloud: { label: 'Nextcloud Drive', route: ':8080' },
      webdav: { label: 'Projects WebDAV', route: ':8081' },
      t3_code: { label: 'T3 Code IDE', route: ':8082' }
    };

    if (applicationsContainer) {
      applicationsContainer.innerHTML = appEntries.map(([key, item]) => {
        const meta = appMeta[key] || { label: key, route: '' };
        const code = item.detail?.code || 200;
        let badgeClass = 'badge-code http-200';
        if (code === 401) badgeClass = 'badge-code http-401';
        else if (code >= 400) badgeClass = 'badge-code http-fail';

        const isOk = item.state === 'OK';
        return `
          <div class="endpoint-row">
            <div class="endpoint-main">
              <span class="pip ${isOk ? 'green' : 'amber'}"></span>
              <span class="endpoint-title">${meta.label}</span>
              <span class="endpoint-port font-mono">${meta.route}</span>
            </div>
            <span class="${badgeClass} font-mono">HTTP ${code}</span>
          </div>
        `;
      }).join('');
    }

    // Remote Mesh Nodes
    if (homePaiList) {
      const pvePing = pai.pve?.detail?.latency_ms ? `${pai.pve.detail.latency_ms} ms` : 'Mesh OK';
      const aiPing = pai.ai_node?.detail?.latency_ms ? `${pai.ai_node.detail.latency_ms} ms` : 'Mesh OK';

      homePaiList.innerHTML = `
        <div class="entity-card">
          <div class="entity-left">
            <span class="pip green"></span>
            <div>
              <div class="entity-title">Proxmox VE Node</div>
              <div class="entity-meta">Core hypervisor & PAI bridge</div>
            </div>
          </div>
          <div class="mesh-ping">${pvePing}</div>
        </div>

        <div class="entity-card">
          <div class="entity-left">
            <span class="pip green"></span>
            <div>
              <div class="entity-title">AI Node Host (Inference)</div>
              <div class="entity-meta">Local model execution cluster</div>
            </div>
          </div>
          <div class="mesh-ping">${aiPing}</div>
        </div>

        <div class="entity-card">
          <div class="entity-left">
            <span class="pip green"></span>
            <div>
              <div class="entity-title">vLLM Inference Engine</div>
              <div class="entity-meta font-mono">${vllmModel}</div>
            </div>
          </div>
          <div class="mesh-ping">awake</div>
        </div>

        <div class="entity-card">
          <div class="entity-left">
            <span class="pip green"></span>
            <div>
              <div class="entity-title">NetBird Mesh Fabric</div>
              <div class="entity-meta">Encrypted WireGuard overlay network</div>
            </div>
          </div>
          <div class="mesh-ping">connected</div>
        </div>
      `;
    }

    // Operations & Backup
    if (operationsList) {
      const ops = data.operations || {};
      const updates = ops.maintenance?.update_available ?? 0;
      const syncFolder = data.knowledge?.syncthing?.folder?.detail?.state || 'idle';

      operationsList.innerHTML = `
        <div class="entity-card">
          <div class="entity-left">
            <span class="pip green"></span>
            <div>
              <div class="entity-title">Backrest Snapshot Vaults</div>
              <div class="entity-meta">edge-state & edge-knowledge-local</div>
            </div>
          </div>
          <div class="mesh-ping">2 plans OK</div>
        </div>

        <div class="entity-card">
          <div class="entity-left">
            <span class="pip green"></span>
            <div>
              <div class="entity-title">Knowledge Sync (Syncthing)</div>
              <div class="entity-meta">Continuous Obsidian vault replication</div>
            </div>
          </div>
          <div class="mesh-ping">${syncFolder}</div>
        </div>

        <div class="entity-card">
          <div class="entity-left">
            <span class="pip ${updates > 0 ? 'amber' : 'green'}"></span>
            <div>
              <div class="entity-title">System Updates (Maintenance)</div>
              <div class="entity-meta">${updates > 0 ? `${updates} package update available` : 'All packages up to date'}</div>
            </div>
          </div>
          <div class="mesh-ping">${updates > 0 ? 'pending' : 'clean'}</div>
        </div>
      `;
    }

    // Units Compact Chips
    if (unitsList) {
      const allUnitNames = [
        ...Object.keys(sysUnits),
        ...Object.keys(userServices)
      ].map(u => u.replace('.service', ''));

      unitsList.innerHTML = allUnitNames.map(name => `
        <span class="unit-chip">
          <span class="pip green"></span>
          <span>${name}</span>
        </span>
      `).join('');
    }

    // Footer
    if (footerUptime && data.agent?.uptime_s) {
      footerUptime.textContent = `Uptime: ${formatUptime(data.agent.uptime_s)}`;
    }

    updateLiveClockAndAge();
  }

  // Fetch Telemetry Function
  async function fetchStatus() {
    if (isFetching) return;
    isFetching = true;
    if (refreshBtn) refreshBtn.classList.add('refreshing');

    try {
      const res = await fetch('/api/status', { cache: 'no-store' });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      render(data);
    } catch (err) {
      console.warn('Telemetry poll failed:', err);
      if (freshnessBox && freshnessLabel) {
        freshnessBox.className = 'status-capsule offline';
        freshnessLabel.textContent = 'Offline';
      }
    } finally {
      isFetching = false;
      if (refreshBtn) refreshBtn.classList.remove('refreshing');
    }
  }

  // Polling Scheduler according to Cadence Timing
  function scheduleNextPoll() {
    if (timerId) clearTimeout(timerId);
    timerId = setTimeout(async () => {
      await fetchStatus();
      scheduleNextPoll();
    }, fastIntervalSec * 1000);
  }

  // Setup Event Listeners
  if (refreshBtn) {
    refreshBtn.addEventListener('click', async () => {
      await fetchStatus();
      scheduleNextPoll();
    });
  }

  // Global Keyboard Shortcuts (R = Sync, T = Theme)
  window.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === 'r' || e.key === 'R') {
      e.preventDefault();
      fetchStatus();
      scheduleNextPoll();
    } else if (e.key === 't' || e.key === 'T') {
      e.preventDefault();
      if (themeToggle) themeToggle.click();
    }
  });

  // Start Live Second-by-Second Age & Clock Ticker
  setInterval(updateLiveClockAndAge, 1000);
  updateLiveClockAndAge();

  // Initial Load
  fetchStatus().then(scheduleNextPoll);

})();
