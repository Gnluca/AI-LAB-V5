// components/TaskCenter.js

import { getMasterLoop } from './apiHelper.js';

function renderMasterLoop(data) {

    const cycleElement =
        document.getElementById('current-cycle');

    const uptimeElement =
        document.getElementById('uptime-display');

    const runtimeState =
        document.querySelector(
            '#runtime-status .runtime-value'
        );

    if (!data || typeof data !== 'object') {
        console.warn(
            '[TaskCenter] Dati master loop non validi'
        );
        return;
    }

    if (runtimeState) {
        runtimeState.textContent =
            data.status || 'UNKNOWN';
    }

    if (cycleElement) {
        cycleElement.textContent =
            data.cycle ?? '-';
    }

    if (uptimeElement) {
        uptimeElement.textContent =
            data.uptime_seconds ?? '-';
    }
}

export async function refreshTaskCenter() {

    const data = await getMasterLoop();

    if (!data.error) {
        renderMasterLoop(data);
    }
}

export async function initializeTaskCenter() {
    startTaskCenter();
}

export function startTaskCenter() {

    refreshTaskCenter();

    setInterval(
        refreshTaskCenter,
        5000
    );
}