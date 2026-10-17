const API_URL = "http://127.0.0.1:8000";

async function loadStatus() {

    try {

        const response = await fetch(
            `${API_URL}/status`
        );

        const data = await response.json();

        const serverStatus =
            document.getElementById("server-status");

        const ollamaStatus =
            document.getElementById("ollama-status");

        const modelName =
            document.getElementById("model-name");

        if (serverStatus) {
            serverStatus.textContent =
                data.status || "ONLINE";
        }

        if (ollamaStatus) {
            ollamaStatus.textContent =
                data.ollama || "ONLINE";
        }

        if (modelName) {
            modelName.textContent =
                data.model || "llama3.1";
        }

    } catch (error) {

        console.error("Errore status:", error);

        const serverStatus =
            document.getElementById("server-status");

        if (serverStatus) {
            serverStatus.textContent =
                "OFFLINE";
        }
    }
}

async function loadNetwork() {

    const panel =
        document.getElementById(
            "network-panel"
        );

    if (!panel) return;

    try {

        const response = await fetch(
            `${API_URL}/network/scan`
        );

        const data = await response.json();

        let html = "";

        data.results.forEach(node => {

            const online =
                typeof node.status === "object";

            const badge =
                online
                    ? "🟢 ONLINE"
                    : "🔴 OFFLINE";

            const model =
                online
                    ? (node.status.model || "N/A")
                    : "N/A";

            html += `
                <div class="network-node">

                    <h3>${node.name}</h3>

                    <p>
                        <b>IP:</b>
                        ${node.ip}
                    </p>

                    <p>
                        <b>Role:</b>
                        ${node.role}
                    </p>

                    <p>
                        <b>Status:</b>
                        ${badge}
                    </p>

                    <p>
                        <b>Model:</b>
                        ${model}
                    </p>

                    ${
                        !online
                        ? `
                        <p style="color:red">
                            ${node.error || ""}
                        </p>
                        `
                        : ""
                    }

                </div>

                <hr>
            `;
        });

                html += `
            <p>
                <b>Administrator:</b>
                ${data.administrator}
            </p>

            <p>
                <b>Connected Nodes:</b>
                ${data.connected_nodes}
            </p>

            <p>
                <b>Online Nodes:</b>
                ${data.online_nodes || 0}
            </p>
        `;

        panel.innerHTML = html;

    } catch (error) {

        console.error(error);

        panel.innerHTML =
            "Errore caricamento rete";
    }
}

async function loadDevelopmentAgent() {

    const panel =
        document.getElementById(
            "development-agent"
        );

    if (!panel) return;

    try {

        const response = await fetch(
            `${API_URL}/agent/development/status`
        );

        const data = await response.json();

        panel.innerHTML = `
            <p>
                <b>Agent:</b>
                ${data.agent}
            </p>

            <p>
                <b>Status:</b>
                ${data.status}
            </p>
        `;

    } catch (error) {

        console.error(
            "Errore DevelopmentAgent:",
            error
        );

        panel.innerHTML = `
            <p style="color:red">
                ❌ DevelopmentAgent non disponibile
            </p>
        `;
    }
}

async function init() {

    await loadStatus();
    await loadDevelopmentAgent();
    await loadNetwork();

}

window.onload = init;