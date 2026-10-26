const API_BASE = "";

async function loadHardware() {
    try {
        const res = await fetch(`${API_BASE}/hardware`);
        const data = await res.json();

        document.getElementById("cpu").textContent =
            `${data.cpu ?? "--"}%`;

        document.getElementById("ram").textContent =
            `${data.ram ?? "--"}%`;

        document.getElementById("disk").textContent =
            `${data.disk ?? "--"}%`;

        document.getElementById("node-status").textContent =
            data.status || "ONLINE";

        document.getElementById("ollama").textContent =
            data.ollama || "ONLINE";

        document.getElementById("model").textContent =
            data.model || "llama3.1";

    } catch (err) {
        console.error("Hardware Error:", err);
    }
}

async function loadMasterLoop() {

    try {

        const res = await fetch(
            `${API_BASE}/runtime/master-loop`
        );

        const data = await res.json();

        document.getElementById("loop-status").textContent =
            data.status;

        document.getElementById("loop-cycles").textContent =
            data.cycles;

        document.getElementById("loop-time").textContent =
            data.last_cycle;

    } catch {

        document.getElementById("loop-status")
            .textContent = "OFFLINE";
    }
}

async function loadMemoryAudit() {
    try {
        const res = await fetch(`${API_BASE}/agent/memory/audit`);
        const data = await res.json();

        document.getElementById("memory-audit").innerHTML = `
            Write: ${data.write_test}<br>
            Read: ${data.read_test}<br>
            Consistency: ${data.consistency}<br>
            GC: ${data.garbage_collection}
        `;
    } catch (err) {
        console.error("Memory Error:", err);

        document.getElementById("memory-audit").innerHTML =
            "Memory OFFLINE";
    }
}

async function loadInventory() {
    try {
        const res = await fetch(`${API_BASE}/agent/inventory/status`);
        const data = await res.json();

        document.getElementById("inventory-status").innerHTML = `
            Files: ${data.files}<br>
            Modules: ${data.modules}<br>
            Status: ${data.status}
        `;
    } catch (err) {
        console.error("Inventory Error:", err);

        document.getElementById("inventory-status").innerHTML =
            "Inventory OFFLINE";
    }
}

async function loadKnowledge() {
    try {
        const res = await fetch(`${API_BASE}/agent/knowledge/status`);
        const data = await res.json();

        document.getElementById("knowledge-status").innerHTML = `
            Coverage: ${data.coverage}%<br>
            Documents: ${data.documents}<br>
            Agents: ${data.agents}<br>
            Status: ${data.status}
        `;
    } catch (err) {
        console.error("Knowledge Error:", err);

        document.getElementById("knowledge-status").innerHTML =
            "Knowledge OFFLINE";
    }
}

async function loadFactory() {
    try {
        const res = await fetch(`${API_BASE}/factory/status`);
        const data = await res.json();

        document.getElementById("factory-status").innerHTML = `
            Agents: ${data.agents}<br>
            Memory: ${data.memory_records}<br>
            Ollama: ${data.ollama}<br>
            Model: ${data.model}
        `;
    } catch (err) {
        console.error("Factory Error:", err);

        document.getElementById("factory-status").innerHTML =
            "Factory OFFLINE";
    }
}

async function loadNetwork() {
    try {
        const res = await fetch(`${API_BASE}/agent/network/discover`);
        const data = await res.json();

        const nodeCount = Array.isArray(data.nodes)
            ? data.nodes.length
            : 0;

        document.getElementById("network-status").innerHTML = `
            Nodes: ${nodeCount}<br>
            Status: ONLINE
        `;
    } catch (err) {
        console.error("Network Error:", err);

        document.getElementById("network-status").innerHTML =
            "Network OFFLINE";
    }
}

async function loadRegistry() {
    try {
        const res = await fetch(`${API_BASE}/registry/nodes`);
        const data = await res.json();

        let html = "";

        for (const [name, info] of Object.entries(data.nodes)) {
            html += `
                <strong>${name}</strong><br>
                IP: ${info.ip}<br>
                Status: ${info.status}<br>
                Role: ${info.role}<br><br>
            `;
        }

        document.getElementById("node-registry").innerHTML = html;

    } catch (err) {
        console.error("Registry Error:", err);

        document.getElementById("node-registry").innerHTML =
            "Registry OFFLINE";
    }
}

async function loadRuntimeHealth() {
    try {
        const res = await fetch(`${API_BASE}/runtime/health`);
        const data = await res.json();

        document.getElementById("runtime-health").innerHTML = `
            Runtime: ${data.runtime}<br>
            Server: ${data.server}<br>
            Dashboard: ${data.dashboard}<br>
            Status: ${data.status}
        `;
    } catch (err) {
        document.getElementById("runtime-health").innerHTML =
            "Runtime OFFLINE";
    }
}

async function loadEvents() {
    try {
        const res = await fetch(`${API_BASE}/agent/labmanager/events`);
        const data = await res.json();

        document.getElementById("events").innerHTML =
            data.events.map(e => `<li>${e}</li>`).join("");
    } catch (err) {
        document.getElementById("events").innerHTML =
            "<li>Events OFFLINE</li>";
    }
}

async function refreshDashboard() {
    await loadHardware();
    await loadMemoryAudit();
    await loadInventory();
    await loadKnowledge();
    await loadFactory();
    await loadNetwork();
    await loadRegistry();
    await loadRuntimeHealth();
    await loadEvents();
	await loadMasterLoop();
}

document.addEventListener("DOMContentLoaded", () => {
    refreshDashboard();
    setInterval(refreshDashboard, 10000);
});