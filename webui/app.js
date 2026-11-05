(() => {
  "use strict";
  const POLL_MS = 5000;
  const API_BASE = String(window.AI_LAB_API_BASE || "").replace(/\/$/, "");
  const ENDPOINTS = { status: `${API_BASE}/status`, report: `${API_BASE}/runtime/master-loop`, feedback: `${API_BASE}/mpc/tasks` };
  const state = { status: null, report: null, busy: false };
  const $ = id => document.getElementById(id);
  const first = (...values) => values.find(v => v !== undefined && v !== null && v !== "");
  const norm = value => String(value ?? "unknown").toLowerCase();
  const online = value => ["online", "active", "healthy", "ok", "true", "connected", "running", "up"].includes(norm(value));
  const num = value => { const n = Number(value); return Number.isFinite(n) ? Math.max(0, Math.min(100, n)) : null; };
  const fmt = value => value == null ? "—" : `${Number(value).toFixed(1)}%`;
  const esc = value => String(value ?? "").replace(/[&<>"']/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;" }[c]));
  const text = (id, value) => { const el = $(id); if (el) el.textContent = value == null || value === "" ? "—" : String(value); };
  const statusValue = value => value && typeof value === "object" ? first(value.status, value.state, value.health, value.online, value.value, "unknown") : first(value, "unknown");
  const arr = value => Array.isArray(value) ? value : [];
  const setOrb = (id, value) => { const el = $(id); if (el) el.className = `status-orb ${online(value) ? "online" : "offline"}`; };
  const setDot = (id, value) => { const el = $(id); if (el) el.className = `service-dot ${online(value) ? "good" : ""}`; };
  const setBar = (id, value) => { const el = $(id); if (el) el.style.width = value == null ? "0%" : `${value}%`; };
  const gauge = (id, value) => { const el = $(id); if (el) el.style.setProperty("--value", value == null ? 0 : value); };
  function showToast(message) { const el = $("toast"); if (!el) return; el.textContent = message; el.classList.add("show"); setTimeout(() => el.classList.remove("show"), 2200); }
  async function getJSON(url) { const response = await fetch(url, { cache: "no-store", headers: { Accept: "application/json" } }); if (!response.ok) throw new Error(`${url}: HTTP ${response.status}`); if (!(response.headers.get("content-type") || "").includes("json")) throw new Error(`${url}: risposta non JSON`); return response.json(); }

  function renderStatus(data = {}, report = {}) {
    const obs = report.observation || {};
    const cpu = num(first(obs.cpu?.usage, obs.cpu?.percent, obs.cpu, data.cpu?.usage, data.cpu?.percent, data.cpu));
    const ram = num(first(obs.memory?.usage, obs.memory?.percent, obs.memory, data.memory?.usage, data.memory?.percent, data.ram, data.memory));
    const n41 = statusValue(first(obs.node41, data.node41, data.primary_node_status, data.status));
    const n56 = statusValue(first(obs.node56, obs.node_details?.status, data.node56, data.secondary_node_status));
    const ollama = statusValue(first(obs.ollama?.status, data.ollama?.status, data.ollama));
    const runtime = statusValue(first(data.runtime, data.runtime_status, data.status));
    if (cpu !== null) { text("cpu-value", cpu.toFixed(1)); text("cpu-state", cpu > 85 ? "Elevato" : "Operativo"); gauge("cpu-gauge", cpu); setBar("cpu-bar", cpu); text("cpu-inline", fmt(cpu)); }
    if (ram !== null) { text("ram-value", ram.toFixed(1)); text("ram-detail", ram > 85 ? "Memoria sotto pressione" : "RAM di sistema"); gauge("ram-gauge", ram); setBar("ram-bar", ram); text("ram-inline", fmt(ram)); }
    const total = first(obs.memory?.total_gb, data.memory?.total_gb);
    text("ram-total", total != null && Number.isFinite(Number(total)) ? `${Number(total).toFixed(1)} GB total` : "Sistema");
    text("node41-status", n41); text("node56-status", n56); setOrb("node41-orb", n41); setOrb("node56-orb", n56);
    text("runtime-status", runtime); text("node56-detail", first(obs.node_details?.version, "Worker"));
    text("topo-node41", online(n41) ? "ONLINE" : "OFFLINE"); text("topo-node56", online(n56) ? "ONLINE" : "OFFLINE"); text("api-status", online(runtime) ? "Connected" : "Degraded");
    text("ollama-status", ollama); setDot("ollama-dot", ollama);
    const registry = statusValue(first(obs.node_details?.details?.registry, data.registry)); text("registry-status", registry); setDot("registry-dot", registry);
    const models = arr(first(obs.ollama?.models, data.ollama?.models)); const list = $("model-list");
    if (list) list.innerHTML = models.length ? models.map(m => `<span class="model-chip">${esc(typeof m === "object" ? first(m.name, m.model, "model") : m)}</span>`).join("") : '<span class="muted">Nessun modello riportato</span>';
    setBar("node41-bar", online(n41) ? 100 : 0); setBar("node56-bar", online(n56) ? 100 : 0); text("node41-inline", online(n41) ? "Online" : "Offline"); text("node56-inline", online(n56) ? "Online" : "Offline");
  }

  function renderReport(report = {}) {
    const obs = report.observation || {}, context = report.context || {}, goals = arr(report.goals), recs = arr(context.recommendations), problems = arr(context.problems);
    text("goal-count", goals.length); text("pending-count", goals.filter(g => norm(typeof g === "object" ? g.status : "").includes("pending")).length); text("recommendation-count", recs.length);
    text("cognitive-health", first(context.status, "Unknown")); text("runtime-health", first(context.status, obs.cpu?.status, "Unknown")); text("report-time", first(report.timestamp, obs.timestamp, "—"));
    const goalsList = $("goals-list");
    if (goalsList) goalsList.innerHTML = goals.length ? goals.map(g => { const item = typeof g === "object" ? g : { goal: g }; return `<div class="goal-item"><span class="goal-symbol">◈</span><div class="goal-copy"><b>${esc(item.goal || item.name || "Goal senza nome")}</b><small>Priorità ${esc(item.priority ?? "—")}</small></div><span class="goal-state">${esc(item.status || "unknown")}</span></div>`; }).join("") : '<div class="empty-state">Nessun goal nel report corrente</div>';
    text("context-note", problems.length ? `Problemi rilevati: ${problems.join(" · ")}` : recs.length ? `Raccomandazioni: ${recs.join(" · ")}` : "Nessun problema o suggerimento segnalato dal Cognitive Core.");
    const alerts = arr(obs.alerts), combined = [...problems.map(p => ({ title: p, detail: "Cognitive Core" })), ...alerts.map(a => typeof a === "string" ? { title: a, detail: "Runtime" } : ({ title: a.title || a.message || a.name || "Runtime alert", detail: a.detail || a.severity || "Runtime" }))];
    text("alert-count", combined.length); const alertsList = $("alerts-list");
    if (alertsList) alertsList.innerHTML = combined.length ? combined.map(a => `<div class="alert-item"><span class="alert-mark">⚠</span><div><b>${esc(a.title)}</b><small>${esc(a.detail)}</small></div></div>`).join("") : '<div class="empty-state">✓ Nessun alert segnalato dal report</div>';
    if (state.status) renderStatus(state.status, report);
  }

  function normalizeFeedback(data) { return Array.isArray(data) ? data : arr(data?.events).length ? data.events : arr(data?.feedback); }
  function renderFeedback(data) {
    const events = normalizeFeedback(data).slice().reverse(), rows = []; text("feedback-total", `${events.length} eventi`);
    events.forEach(event => (arr(event?.results).length ? event.results : [event]).forEach(item => rows.push({ timestamp: first(item.timestamp, event.timestamp), task: first(item.task, item.agent, item.event, "Runtime feedback"), node: item.node, status: first(item.status, "recorded"), detail: first(item.error, item.detail, item.worker_response?.detail, item.worker_response?.status) })));
    const recent = rows.slice(0, 12), list = $("feedback-list");
    if (list) list.innerHTML = recent.length ? recent.map(e => { const failed = norm(e.status).includes("fail") || norm(e.status).includes("error"); let time = "Ora non disponibile"; const d = e.timestamp && new Date(e.timestamp); if (d && !Number.isNaN(d.valueOf())) time = d.toLocaleString("it-IT", { month: "short", day: "2-digit", hour: "2-digit", minute: "2-digit" }); return `<div class="timeline-item"><div class="timeline-head"><b>${esc(e.task)}</b><time>${esc(time)}</time></div><p>${esc([e.node, e.detail].filter(Boolean).join(" · ") || "Nessun dettaglio aggiuntivo")}</p><span class="event-status ${failed ? "failed" : ""}">${esc(e.status)}</span></div>`; }).join("") : '<div class="empty-state">Il feed feedback è vuoto o ha un formato non riconosciuto</div>';
  }

  async function refresh() {
    if (state.busy) return; state.busy = true; $("refresh-btn")?.classList.add("spinning");
    const results = await Promise.allSettled(Object.values(ENDPOINTS).map(getJSON)); let failures = 0;
    results.forEach((result, index) => { if (result.status === "rejected") { failures++; return; } if (index === 0) { state.status = result.value; renderStatus(state.status, state.report || {}); } if (index === 1) { state.report = result.value; renderReport(state.report); } if (index === 2) renderFeedback(result.value); });
    const success = results.length - failures; text("last-update", success ? `Aggiornato ${new Date().toLocaleTimeString("it-IT", { hour: "2-digit", minute: "2-digit", second: "2-digit" })}` : "Connessione non disponibile"); text("sidebar-connection", success ? `${success}/3 endpoint attivi` : "API non raggiungibile"); if (failures === 3) showToast("Impossibile raggiungere gli endpoint AI-LAB"); state.busy = false; $("refresh-btn")?.classList.remove("spinning");
  }
  $("refresh-btn")?.addEventListener("click", refresh); refresh(); setInterval(refresh, POLL_MS);
})();
