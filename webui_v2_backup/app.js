// app.js

import { startStatusPanel }
    from './components/StatusPanel.js';
import { initializeTaskCenter }
    from './components/TaskCenter.js';
import { initializeEventLogger } from './components/EventLogger.js';

/**
 * Inizializza l'intera interfaccia utente AI Lab, 
 * gestendo il caricamento asincrono e l'interdipendenza dei componenti.
 */
 
 
async function initializeApplication() {
    console.log("🤖 WebUI: Avvio inizializzazione del pannello principale...");

    // Inizializza i componenti in parallelo per migliorare le performance di caricamento iniziale.
	
	
    await Promise.all([
    startStatusPanel(),
    initializeTaskCenter(),
    initializeEventLogger()
]);

    console.log("✅ WebUI: Tutti i componenti sono stati inizializzati con successo.");
}


// Controllo per assicurare che la funzione venga eseguita solo dopo il caricamento completo del DOM.
document.addEventListener('DOMContentLoaded', () => {
    initializeApplication();
});

/* 
 * Nota di architettura: 
 * Il master loop (setInterval) è stato delegato all'interno dei componenti stessi 
 * per garantire che l'aggiornamento periodico cada nel contesto specifico del dato (stato, task).
 */
