(() => {
  "use strict";
  const POLL_MS = 5000;
  const ENDPOINTS = { status: "/status", report: "/runtime/cognitive-report", feedback: "/runtime/feedback" };
  const $ = (id) => document.getElementById(id);
  const state = { status: null, report: null, feedback: [], lastSuccess: 0, busy: false };
  const text = (id, value) => { const el = $(id); if (el) el.textContent = value == null || value === "" ? "—" : String(value); };
  const first = (...values) => values.find(v => v !== undefined && v !== null && v !== "");
  const norm = value => String(value ?? "unknown").toLowerCase();
  const online = value => ["online", "active", "healthy", "ok", "true", "connected"].includes(norm(value));
  const num = value => { const n = Number(value); return Number.isFinite(n) ? Math.max(0, Math.min(100, n)) : null; };
  const fmt = value => value == null ? "—" : `${Number(value).toFixed(1)}%`;
  const esc = value => String(value ?? "").replace(/[&<>"']/g, c => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[c]));
  function setOrb(id, value) { const el = $(id); el.className = `status-orb ${online(value) ? "online" : "offline"}`; }
  function setDot(id, value) { const el = $(id); el.className = `service-dot ${online(value) ? "good" : ""}`; }
  function setBar(id, value) { $(id).style.width = value == null ? "0%" : `${value}%`; }
  function gauge(id, value) { $(id).style.setProperty("--value", value == null ? 0 : value); }
  function showToast(message) { const el=$("toast"); el.textContent=message; el.classList.add("show"); setTimeout(()=>el.classList.remove("show"),2200); }
  async function getJSON(url) {
    const response = await fetch(url, { cache: "no-store", headers: { "Accept": "application/json" } });
    if (!response.ok) throw new Error(`${url}: HTTP ${response.status}`);
    return response.json();
  }
  function renderStatus(data, report) {
    const obs = report?.observation || {};
    const cpu = num(first(obs.cpu?.usage, obs.cpu, data?.cpu?.usage, data?.cpu));
    const ram = num(first(obs.memory?.usage, obs.memory?.percent, data?.memory?.usage, data?.ram, data?.memory));
    const n41 = first(obs.node41, data?.node41, data?.primary_node_status, data?.status);
    const n56 = first(obs.node56, obs.node_details?.status, data?.node56, data?.secondary_node_status);
    const ollama = first(obs.ollama?.status, data?.ollama?.status, data?.ollama);
    const runtime = first(data?.runtime, data?.status, "unknown");
    if (cpu !== null) { text("cpu-value", cpu.toFixed(1)); text("cpu-state", cpu > 85 ? "Elevato" : "Operativo"); gauge("cpu-gauge",cpu); setBar("cpu-bar",cpu); text("cpu-inline",fmt(cpu)); }
    if (ram !== null) { text("ram-value",ram.toFixed(1)); text("ram-detail",ram > 85 ? "Memoria sotto pressione" : "RAM di sistema"); gauge("ram-gauge",ram); setBar("ram-bar",ram); text("ram-inline",fmt(ram)); }
    const total = first(obs.memory?.total_gb, data?.memory?.total_gb);
    text("ram-total", total ? `${Number(total).toFixed(1)} GB total` : "Sistema");
    text("node41-status", n41); text("node56-status", n56);
    setOrb("node41-orb",n41); setOrb("node56-orb",n56);
    text("runtime-status",runtime); text("node56-detail",first(obs.node_details?.version, "Worker"));
    text("topo-node41",online(n41)?"ONLINE":"OFFLINE"); text("topo-node56",online(n56)?"ONLINE":"OFFLINE");
    text("api-status",online(runtime)?"Connected":"Degraded");
    text("ollama-status",ollama); setDot("ollama-dot",ollama);
    const registry=first(obs.node_details?.details?.registry,data?.registry,"unknown");
    text("registry-status",registry); setDot("registry-dot",registry);
    const models=first(obs.ollama?.models,data?.ollama?.models,[]);
    $("model-list").innerHTML = Array.isArray(models)&&models.length ? models.map(m=>`<span class="model-chip">${esc(m)}</span>`).join("") : '<span class="muted">Nessun modello riportato</span>';
    const n41ok=online(n41), n56ok=online(n56);
    setBar("node41-bar",n41ok?100:0); setBar("node56-bar",n56ok?100:0);
    text("node41-inline",n41ok?"Online":"Offline"); text("node56-inline",n56ok?"Online":"Offline");
  }
  function renderReport(report) {
    const obs=report?.observation||{}, context=report?.context||{};
    const goals=Array.isArray(report?.goals)?report.goals:[];
    const recs=Array.isArray(context.recommendations)?context.recommendations:[];
    const problems=Array.isArray(context.problems)?context.problems:[];
    text("goal-count",goals.length); text("pending-count",goals.filter(g=>norm(g.status)==="pending").length);
    text("recommendation-count",recs.length);
    text("cognitive-health",first(context.status,"Unknown"));
    text("runtime-health",first(context.status,obs.cpu?.status,"Unknown"));
    text("report-time",first(report?.timestamp,obs.timestamp,"—"));
    $("goals-list").innerHTML=goals.length?goals.map(g=>`<div class="goal-item"><span class="goal-symbol">◈</span><div class="goal-copy"><b>${esc(g.goal||g.name||"Goal senza nome")}</b><small>Priorità ${esc(g.priority??"—")}</small></div><span class="goal-state">${esc(g.status||"unknown")}</span></div>`).join(""):'<div class="empty-state">Nessun goal nel report corrente</div>';
    text("context-note", problems.length ? `Problemi rilevati: ${problems.join(" · ")}` : recs.length ? `Raccomandazioni: ${recs.join(" · ")}` : "Nessun problema o suggerimento segnalato dal Cognitive Core.");
    const alerts=Array.isArray(obs.alerts)?obs.alerts:[];
    const combined=[...problems.map(p=>({title:p,detail:"Cognitive Core"})),...alerts.map(a=>typeof a==="string"?{title:a,detail:"Runtime"}:({title:a.title||a.message||a.name||"Runtime alert",detail:a.detail||a.severity||"Runtime"}))];
    text("alert-count",combined.length);
    $("alerts-list").innerHTML=combined.length?combined.map(a=>`<div class="alert-item"><span class="alert-mark">⚠</span><div><b>${esc(a.title)}</b><small>${esc(a.detail)}</small></div></div>`).join(""):'<div class="empty-state">✓ Nessun alert segnalato dal report</div>';
    if (state.status) renderStatus(state.status,report);
  }
  function normalizeFeedback(data) {
    if(Array.isArray(data)) return data;
    if(Array.isArray(data?.events)) return data.events;
    if(Array.isArray(data?.feedback)) return data.feedback;
    return [];
  }
  function renderFeedback(data) {
    const events=normalizeFeedback(data).slice().reverse();
    text("feedback-total",`${events.length} eventi`);
    const rows=[];
    events.forEach(event=>{
      const results=Array.isArray(event?.results)?event.results:[event];
      results.forEach(item=>rows.push({timestamp:first(item.timestamp,event.timestamp),task:first(item.task,item.agent,item.event,"Runtime feedback"),node:item.node,status:first(item.status,"recorded"),detail:first(item.error,item.detail,item.worker_response?.detail,item.worker_response?.status)}));
    });
    const recent=rows.slice(0,12);
    $("feedback-list").innerHTML=recent.length?recent.map(e=>{
      const failed=norm(e.status).includes("fail")||norm(e.status).includes("error")||Boolean(e.error);
      let time="Ora non disponibile"; try{if(e.timestamp)time=new Date(e.timestamp).toLocaleString("it-IT",{month:"short",day:"2-digit",hour:"2-digit",minute:"2-digit"});}catch(_){}
      return `<div class="timeline-item"><div class="timeline-head"><b>${esc(e.task)}</b><time>${esc(time)}</time></div><p>${esc([e.node,e.detail].filter(Boolean).join(" · ")||"Nessun dettaglio aggiuntivo")}</p><span class="event-status ${failed?"failed":""}">${esc(e.status)}</span></div>`;
    }).join(""):'<div class="empty-state">Il feed feedback è vuoto o ha un formato non riconosciuto</div>';
  }
  async function refresh() {
    if(state.busy)return; state.busy=true; $("refresh-btn").classList.add("spinning");
    const results=await Promise.allSettled([getJSON(ENDPOINTS.status),getJSON(ENDPOINTS.report),getJSON(ENDPOINTS.feedback)]);
    let failures=0;
    results.forEach((result,index)=>{
      if(result.status==="rejected"){failures++;return;}
      const value=result.value;
      if(index===0){state.status=value;renderStatus(value,state.report);}
      if(index===1){state.report=value;renderReport(value);}
      if(index===2){state.feedback=value;renderFeedback(value);}
    });
    const success=results.length-failures;
    if(success){state.lastSuccess=Date.now();text("last-update",`Aggiornato ${new Date().toLocaleTimeString("it-IT",{hour:"2-digit",minute:"2-digit",second:"2-digit"})}`);text("sidebar-connection",failures?`${success}/3 endpoint attivi`:"API raggiungibile");}
    else {text("last-update","Connessione non disponibile");text("sidebar-connection","API non raggiungibile");}
    if(failures===3) showToast("Impossibile raggiungere gli endpoint AI-LAB");
    state.busy=false;$("refresh-btn").classList.remove("spinning");
  }
  $("refresh-btn").addEventListener("click",refresh);
  refresh(); setInterval(refresh,POLL_MS);
})();