// =====================================
// AI LAB V6.2 Dashboard
// =====================================

const API_BASE = "http://127.0.0.1:8000";

// -------------------------------------
// CLOCK
// -------------------------------------

function updateClock() {
    const clock = document.getElementById("clock");

    if (clock) {
        const now = new Date();

        clock.textContent =
            now.toLocaleDateString("it-IT") +
            " " +
            now.toLocaleTimeString("it-IT");
    }
}

// -------------------------------------
// HARDWARE STATUS
// -------------------------------------

async function loadHardwareStatus() {

    try {

        const response =
            await fetch(`${API_BASE}/agent/hardware/status`);

        const data = await response.json();

        document.getElementById("cpu").textContent =
            data.cpu_cores ?? "--";

        document.getElementById("ram").textContent =
            data.ram_gb + " GB";

        document.getElementById("disk").textContent =
            data.disk_free_gb + " GB";

    }
    catch (error) {

        console.error(error);

        document.getElementById("cpu").textContent = "OFFLINE";
        document.getElementById("ram").textContent = "OFFLINE";
        document.getElementById("disk").textContent = "OFFLINE";
    }

}

// -------------------------------------
// SERVER STATUS
// -------------------------------------

async function loadServerStatus() {

    try {

        const response =
            await fetch(`${API_BASE}/status`);

        const data = await response.json();

        console.log("Server Status:", data);

    }
    catch (err) {

        console.error("Server offline", err);

    }

}

// -------------------------------------
// NETWORK STATUS
// -------------------------------------

async function loadNetworkStatus() {

    try {

        const response =
            await fetch(`${API_BASE}/network/scan`);

        const data = await response.json();

        console.log("Network:", data);

    }
    catch (err) {

        console.error(err);

    }

}

// -------------------------------------
// DASHBOARD START
// -------------------------------------

async function refreshDashboard() {

    await loadHardwareStatus();
    await loadServerStatus();
    await loadNetworkStatus();

}

document.addEventListener("DOMContentLoaded", () => {

    updateClock();

    refreshDashboard();

    setInterval(updateClock, 1000);

    setInterval(refreshDashboard, 30000);

    console.log("AI LAB Dashboard Online");

});