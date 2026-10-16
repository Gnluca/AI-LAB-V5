async function updateStatus() {
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/status",
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        );

        if (!response.ok) {
            throw new Error("Server non raggiungibile");
        }

        const data = await response.json();

        document.getElementById("server").textContent =
            (data.status || "ONLINE").toUpperCase();

        document.getElementById("server").className =
            "value online";

        document.getElementById("ollama").textContent =
            (data.ollama || "ONLINE").toUpperCase();

        document.getElementById("ollama").className =
            "value online";

        document.getElementById("model").textContent =
            data.model || "llama3.1";

    } catch (error) {

        document.getElementById("server").textContent =
            "OFFLINE";

        document.getElementById("server").className =
            "value offline";

        document.getElementById("ollama").textContent =
            "OFFLINE";

        document.getElementById("ollama").className =
            "value offline";

        document.getElementById("model").textContent =
            "Non disponibile";

        console.error("Errore API:", error);
    }
}

function updateClock() {
    const now = new Date();

    document.getElementById("clock").textContent =
        now.toLocaleString("it-IT");
}

updateStatus();
updateClock();

setInterval(updateStatus, 10000);
setInterval(updateClock, 1000);