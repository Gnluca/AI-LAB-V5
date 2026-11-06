// MetricGauge.js: Gestisce i gauge di utilizzo risorse e il punteggio generale.

/**
 * Aggiorna un singolo widget Gauge (CPU, RAM, VRAM).
 * @param {string} resource - La risorsa (cpu, ram, vram).
 * @param {number} value - Percentuale di utilizzo.
 */
export function updateGauge(resource, value) {
    const element = document.querySelector(`[data-resource="${resource}"]`);
    if (element) {
        element.textContent = `${Math.round(value)}%`;

        // Reset e assegnazione classe colore per il Gauge principale
        const gaugeCard = document.closest('.gauge-card');
        gaugeCard.querySelectorAll('.status-indicator, .status-ok, .status-warning, .status-down').forEach(el => el.classList.remove('status-ok', 'status-warning', 'status-down'));

        let statusClass;
        if (value >= 90) {
            statusClass = 'danger'; // Rosso critico
        } else if (value >= 75) {
            statusClass = 'warning'; // Giallo avviso
        } else {
            statusClass = 'success'; // Verde OK
        }

        // Aggiunge la classe di stato al gauge container o alla risorsa
        document.querySelector(`[data-resource="${resource}"]`).style.color = '';
        gaugeCard.style.boxShadow = `0 0 ${Math.max(5, value/2)}px rgba(0, ${170 - (value*1.5)}, 255, 0.3)`;

    }
}

/**
 * Aggiorna il punteggio di salute complessivo del sistema.
 * @param {number} score - Punteggio da 0 a 100.
 */
export function updateGlobalHealthScore(score) {
    const element = document.getElementById('global-health-score');
    if (element) {
        element.textContent = `${Math.round(score)}%`;
    }
}
