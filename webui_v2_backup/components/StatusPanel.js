// StatusPanel.js - Popola gli stati vitali utilizzando data-role per la mappatura sicura.

import { getStatus } from './apiHelper.js'; // Assumiamo che questo sia l'unico modo valido per ottenere i dati.

/**
 * Helper: Tenta di trovare un elemento nel DOM in base al suo ruolo (data-role) 
 * e ne aggiorna il contenuto, gestendo eventuali fallimenti senza bloccare lo script.
 * @param {string} key - La chiave del dato che deve corrispondere a data-role (es: 'primary_node').
 * @param {*} value - Il valore da visualizzare nello stato.
 */
 
 
function updateStatusByRole(key, value) {
    // 1. Costruisce il selettore per trovare l'elemento tramite attributo "data-role"
    const selector = `[data-role="${key}"]`;
    const element = document.querySelector(selector);

    if (element) {
        let displayValue;
        if (typeof value === 'string') {
            // Tratta tutte le stringhe in maiuscolo per coerenza con lo stato "online" / "offline"
            displayValue = value.toUpperCase(); 
        } else if (value && typeof value !== 'undefined') {
             // Gestisce numeri, booleani o altri tipi di dati validi
             displayValue = String(value).toUpperCase(); 
        } else {
            // Valore mancante o nullo
            displayValue = 'N/A';
        }

        element.textContent = displayValue;
    } else {
		
        // NON lancia un errore, ma avvisa lo sviluppatore che il data-role manca nell'HTML.
		
        if (!element) {
    return;
}
    }
}


/**
 * Inizializza e popola il pannello di stato utilizzando i dati caricati da API/JSON.
 */
 
 
export async function initStatusPanel() {
    console.log("Inizializzazione Status Panel...");

    try {
        // 1. Ottiene i dati in modo pulito, usando l'import corretto.
        const statusData = await getStatus(); 
        
        if (!statusData || typeof statusData !== 'object') {
             throw new Error("Dati dello stato non disponibili o formato JSON errato.");
        }

        // 2. Itera su ogni chiave (servizio) nel JSON ricevuto.
        for (const key in statusData) {
            if (Object.hasOwnProperty.call(statusData, key)) {
                const value = statusData[key];
                
                // Utilizziamo la funzione helper che mappa il dato al ruolo corretto.
                updateStatusByRole(key, value); 
            }
        }			

    } catch (error) {
        // Blocco principale: gestisce errori di rete o problemi critici ai dati.
        console.error("FATALE - Errore nel caricamento dello Status Panel:", error);
        // Se non c'è un container specifico, potresti voler fare nulla per non fallire l'intera pagina.
    }
}

export async function initializeStatusPanel() {
    return initStatusPanel();
}

export async function startStatusPanel() {
    return initStatusPanel();
}


