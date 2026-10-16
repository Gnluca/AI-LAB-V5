async function checkSecurity() {

    try {

        console.log("Tentativo connessione...");

        const response = await fetch(
            "http://127.0.0.1:8000/status"
        );

        console.log("Response:", response);

        const data = await response.json();

        console.log("Data:", data);

        document.getElementById("fastapi").textContent =
            data.status;

        document.getElementById("ollama").textContent =
            data.ollama;

        document.getElementById("model").textContent =
            data.model;

    }
    catch(error) {

        console.error("ERRORE FETCH:", error);

        document.getElementById("fastapi").textContent =
            "OFFLINE";
    }
}

checkSecurity();