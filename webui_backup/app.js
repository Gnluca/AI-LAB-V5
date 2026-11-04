async function loadData() {

    try {
        const r = await fetch("/status");

        if (r.ok) {
            const data = await r.json();

            document.getElementById("status").textContent =
                JSON.stringify(data, null, 2);
        } else {
            document.getElementById("status").textContent =
                "Endpoint /status non trovato";
        }
    } catch (e) {
        document.getElementById("status").textContent = e.message;
    }

    try {
        const r = await fetch("/runtime/cognitive-report");

        if (r.ok) {
            const data = await r.json();

            document.getElementById("report").textContent =
                JSON.stringify(data, null, 2);
        } else {
            document.getElementById("report").textContent =
                "Endpoint non trovato";
        }
    } catch (e) {
        document.getElementById("report").textContent = e.message;
    }

    try {
        const r = await fetch("/runtime/feedback");

        if (r.ok) {
            const data = await r.json();

            document.getElementById("feedback").textContent =
                JSON.stringify(data, null, 2);
        } else {
            document.getElementById("feedback").textContent =
                "Endpoint non trovato";
        }
    } catch (e) {
        document.getElementById("feedback").textContent = e.message;
    }
}

loadData();
setInterval(loadData, 5000);