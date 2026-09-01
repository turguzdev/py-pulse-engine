// Polling Intervals & State
let pollInterval = null;

async function fetchTelemetry() {
  try {
    const [healthRes, sysRes, analyticsRes] = await Promise.all([
      fetch("/api/health"),
      fetch("/api/system"),
      fetch("/api/analytics/summary")
    ]);

    if (healthRes.ok) {
      const health = await healthRes.json();
      document.getElementById("health-status").textContent = "Operational";
      document.getElementById("uptime-val").textContent = `${health.uptime_seconds}s`;
    }

    if (sysRes.ok) {
      const sys = await sysRes.json();
      document.getElementById("cpu-val").textContent = `${sys.cpu_percent}%`;
      document.getElementById("cpu-bar").style.width = `${Math.min(sys.cpu_percent, 100)}%`;
      document.getElementById("cpu-foot").textContent = `Cores: ${sys.cpu_count} (${sys.platform})`;

      document.getElementById("ram-val").textContent = `${sys.memory_percent}%`;
      document.getElementById("ram-bar").style.width = `${sys.memory_percent}%`;
      document.getElementById("ram-foot").textContent = `Available: ${sys.memory_available_mb} MB / ${sys.memory_total_mb} MB`;
    }

    if (analyticsRes.ok) {
      const a = await analyticsRes.json();
      document.getElementById("rps-val").textContent = `${a.requests_per_second}`;
      document.getElementById("latency-foot").textContent = `Avg Latency: ${a.avg_latency_ms} ms`;
    }
  } catch (err) {
    document.getElementById("health-status").textContent = "Offline";
  }
}

async function loadNodes() {
  const listEl = document.getElementById("node-list");
  try {
    const res = await fetch("/api/nodes");
    const nodes = await res.json();

    if (!nodes || nodes.length === 0) {
      listEl.innerHTML = '<div class="empty-state">No active cluster nodes.</div>';
      return;
    }

    listEl.innerHTML = nodes.map(n => `
      <div class="node-item">
        <div class="node-info">
          <h4>${n.name} <span class="node-role-badge">${n.role}</span></h4>
          <div class="node-meta">
            <span>📍 ${n.region}</span>
            <span>⚡ ${n.cpu_cores} Cores / ${n.memory_gb} GB</span>
            <span>⏱️ ${n.uptime_hours}h</span>
          </div>
        </div>
        <button class="btn btn-danger" onclick="decommissionNode('${n.id}')">Decommission</button>
      </div>
    `).join("");
  } catch (err) {
    listEl.innerHTML = `<div class="empty-state">Failed to load nodes: ${err.message}</div>`;
  }
}

async function callApi(endpoint) {
  const consoleEl = document.getElementById("console-output");
  consoleEl.textContent = `// Sending GET ${endpoint}...`;
  try {
    const res = await fetch(endpoint);
    const data = await res.json();
    consoleEl.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    consoleEl.textContent = `// Error: ${err.message}`;
  }
}

function clearConsole() {
  document.getElementById("console-output").textContent = "// Console cleared. Ready for next query.";
}

function openAddNodeModal() {
  document.getElementById("node-modal").classList.add("active");
}

function closeAddNodeModal() {
  document.getElementById("node-modal").classList.remove("active");
}

async function handleCreateNode(event) {
  event.preventDefault();
  const name = document.getElementById("node-name").value;
  const region = document.getElementById("node-region").value;
  const role = document.getElementById("node-role").value;

  try {
    const res = await fetch("/api/nodes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, region, role, tags: ["user-provisioned"] })
    });
    if (res.ok) {
      closeAddNodeModal();
      document.getElementById("node-form").reset();
      loadNodes();
    }
  } catch (err) {
    alert(`Failed to create node: ${err.message}`);
  }
}

async function decommissionNode(nodeId) {
  if (!confirm(`Are you sure you want to decommission node ${nodeId}?`)) return;
  try {
    const res = await fetch(`/api/nodes/${nodeId}`, { method: "DELETE" });
    if (res.ok) {
      loadNodes();
    }
  } catch (err) {
    alert(`Failed to delete node: ${err.message}`);
  }
}

// Initial Boot
document.addEventListener("DOMContentLoaded", () => {
  fetchTelemetry();
  loadNodes();
  pollInterval = setInterval(fetchTelemetry, 3000);
});
