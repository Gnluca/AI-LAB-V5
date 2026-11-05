// utils.js

/**
 * Funzione helper che aggiorna il contenuto HTML di un contenitore specificato, 
 * evitando manipolazioni dirette e garantendo l'uso di template string ES6.
 * @param {HTMLElement} element Il contenitore DOM su cui renderizzare i contenuti.
 * @param {string} htmlString La stringa HTML da iniettare.
 */
export function renderComponent(element, htmlString) {
    if (element instanceof HTMLElement && typeof htmlString === 'string') {
        // Usa innerHTML per iniettare il contenuto completo dei componenti.
        element.innerHTML = htmlString; 
    } else {
        console.error("Errore: Elemento DOM o stringa HTML non validi forniti a renderComponent.");
    }
}
