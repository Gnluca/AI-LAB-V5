const API_BASE = "http://127.0.0.1:8000";

async function fetchJson(url) {
    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error(error);
        return null;
    }
}

async function loadFrameworkStatus() {
    const data = await fetchJson(`${API_BASE}/status`);

    if (!data) return;

    document.getElementById("status").textContent =
        (data.status || "offline").toUpperCase();

    const ollama = document.getElementById("ollama");
    if (ollama) {
        ollama.textContent =
            (data.ollama || "offline").toUpperCase();
    }

    const model = document.getElementById("model");
    if (model) {
        model.textContent =
            data.model || "--";
    }
}

async function loadHardwareStatus() {
    const data = await fetchJson(
        `${API_BASE}/hardware/status`
    );

    if (!data) {
        document.getElementById("cpu").textContent = "--";
        document.getElementById("ram").textContent = "--";
        document.getElementById("disk").textContent = "--";
        return;
    }

    document.getElementById("cpu").textContent =
        `${data.cpu}%`;

    document.getElementById("ram").textContent =
        `${data.ram}%`;

    document.getElementById("disk").textContent =
        `${data.disk}%`;
}

async function loadRegistry() {
    const data = await fetchJson(`${API_BASE}/registry`);

    if (!data) return;

    const registry = document.getElementById("registry");

    if (registry) {
        registry.innerHTML =
            "<pre>" +
            JSON.stringify(data, null, 2) +
            "</pre>";
    }
}

async function loadFingerprint() {
    const data = await fetchJson(`${API_BASE}/fingerprint`);

    if (!data) return;

    const fingerprint =
        document.getElementById("fingerprint");

    if (fingerprint) {
        fingerprint.innerHTML =
            "<pre>" +
            JSON.stringify(data, null, 2) +
            "</pre>";
    }
}

async function loadPassport() {
    const data = await fetchJson(`${API_BASE}/passport`);

    if (!data) return;

    const passport =
        document.getElementById("passport");

    if (passport) {
        passport.innerHTML =
            "<pre>" +
            JSON.stringify(data, null, 2) +
            "</pre>";
    }
}

async function refreshDashboard() {
    await loadFrameworkStatus();
    await loadHardwareStatus();
    await loadRegistry();
    await loadFingerprint();
    await loadPassport();
}

document.addEventListener("DOMContentLoaded", () => {

    refreshDashboard();

    setInterval(() => {
        loadFrameworkStatus();
        loadHardwareStatus();
    }, 5000);

});

function updateClock() {
    const now = new Date();

    const time =
        now.toLocaleDateString("it-IT") +
        " " +
        now.toLocaleTimeString("it-IT");

    document.getElementById("clock").textContent = time;
}

setInterval(updateClock, 1000);
updateClock();

async function loadHardwareStatus() {
    try {
        const response = await fetch(`${API_BASE}/hardware/status`);
        const data = await response.json();

        document.getElementById("cpu").textContent =
            data.cpu.toFixed(1) + "%";

        document.getElementById("ram").textContent =
            data.ram.toFixed(1) + "%";

        document.getElementById("disk").textContent =
            data.disk.toFixed(1) + "%";

    } catch (error) {
        console.error("Hardware Status Error:", error);

        document.getElementById("cpu").textContent = "--";
        document.getElementById("ram").textContent = "--";
        document.getElementById("disk").textContent = "--";
    }
}

async function loadStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();

        const statusEl = document.getElementById("status");
        if (statusEl) {
            statusEl.textContent =
                (data.status || "offline").toUpperCase();
        }

        const ollamaEl = document.getElementById("ollama");
        if (ollamaEl) {
            ollamaEl.textContent =
                (data.ollama || "offline").toUpperCase();
        }

        const modelEl = document.getElementById("model");
        if (modelEl) {
            modelEl.textContent =
                data.model || "--";
        }

    } catch (error) {
        console.error("Status Error:", error);
    }
}

function updateClock() {
    const now = new Date();

    const text =
        now.toLocaleDateString("it-IT") +
        " " +
        now.toLocaleTimeString("it-IT");

    const clock = document.getElementById("clock");

    if (clock) {
        clock.textContent = text;
    }
}

async function refresh() {
    await loadStatus();
    await loadHardwareStatus();
}

document.addEventListener("DOMContentLoaded", () => {

    refresh();
    updateClock();

    setInterval(refresh, 5000);
    setInterval(updateClock, 1000);

});
