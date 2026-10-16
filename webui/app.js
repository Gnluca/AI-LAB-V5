async function updateStatus() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/status"
        );

        const data = await response.json();

        document.getElementById("server").textContent =
            data.status.toUpperCase();

        document.getElementById("server").className =
            "value online";

        document.getElementById("ollama").textContent =
            data.ollama.toUpperCase();

        document.getElementById("ollama").className =
            "value online";

        document.getElementById("model").textContent =
            data.model;

    } catch (error) {

        document.getElementById("server").textContent =
            "OFFLINE";

        document.getElementById("server").className =
            "value offline";

        document.getElementById("ollama").textContent =
            "OFFLINE";

        document.getElementById("ollama").className =
            "value offline";

        console.error(error);
    }
}

updateStatus();

setInterval(updateStatus, 10000);