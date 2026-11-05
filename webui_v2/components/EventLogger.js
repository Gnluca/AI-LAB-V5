// components/EventLogger.js

import { renderComponent } from './utils.js';

const loggerContainer = document.getElementById("event-stream");

/**
 * Ottiene un report cognitivo (log degli eventi) dall'AI Lab.
 */
 
async function fetchCognitiveReport() {

    console.log("Attempting to fetch cognitive report from /runtime/cognitive-report...");

    try {
        const response = await fetch('/runtime/cognitive-report');

        if (!response.ok) {
            throw new Error(`HTTP error! Status code: ${response.status}`);
        }

        return await response.json();

    } catch (error) {

        console.warn("Could not fetch cognitive report:", error);
        return [];
    }
}

/**
 * Invia l'eventuale feedback utente al sistema AI Lab.
 */
 
async function sendUserFeedback(feedbackText) {
    if (!feedbackText || typeof feedbackText !== 'string') {
        alert("Per favore, inserisci un feedback valido.");
        return;
    }

    console.log(`Sending user feedback: ${feedbackText}...`);
    try {
        const response = await fetch('/runtime/feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: feedbackText, source: "WebUI" })
        });

        if (response.ok) {
             alert("Feedback inviato con successo!");
        } else {
            const errorBody = await response.text();
            console.error("Failed to send feedback:", errorBody);
            alert(`Errore nell'invio del feedback: ${errorBody}`);
        }
    } catch (error) {
        console.error("Network error while sending feedback:", error);
        alert("Errore di rete durante l'invio del feedback.");
    }
}

/**
 * Renderizza gli eventi nel logger.
 * @param {Array<Object>} events Array di oggetti evento/log.
 */
 
function renderLogs(report) {

    if (!loggerContainer) return;

    let html = "";

    if (report.context?.problems) {
        html += report.context.problems.map(problem => `
            <div class="log-entry log-warning">
                [WARNING] ${problem}
            </div>
        `).join("");
    }

    if (report.goals) {
        html += report.goals.map(goal => `
            <div class="log-entry log-info">
                [GOAL] ${goal.goal}
                (Priority ${goal.priority})
            </div>
        `).join("");
    }

    if (!html) {
        html = `
            <div class="log-info">
                Nessun evento disponibile
            </div>
        `;
    }

    loggerContainer.innerHTML = html;
}


/**
 * Funzione principale di inizializzazione del componente Event Logger.
 */
export async function initializeEventLogger() {
    if (!loggerContainer) {
        console.error("Elemento HTML #event-logger non trovato.");
        return;
    }

    // Esegue il fetch iniziale del report cognitivo
    const initialLogs = await fetchCognitiveReport();
    renderLogs(initialLogs);
}
