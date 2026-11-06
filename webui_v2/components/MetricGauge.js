// MetricGauge.js

export function updateGauge(resource, value) {
    const element =
        document.querySelector(
            `[data-resource="${resource}"]`
        );

    if (!element) return;

    element.textContent =
        `${Math.round(value)}%`;
}

export function updateGlobalHealthScore(score) {
    const element =
        document.getElementById(
            'global-health-score'
        );

    if (!element) return;

    element.textContent =
        `HEALTH SCORE: ${Math.round(score)}%`;
}

export async function initializeMetricGauge() {

    async function refresh() {

        try {

            const response =
                await fetch('/hardware');

            const data =
                await response.json();

            updateGauge(
                'cpu',
                data.cpu ?? 0
            );

            updateGauge(
                'ram',
                data.ram ?? 0
            );

            updateGauge(
                'vram',
                data.disk ?? 0
            );

            const score =
                100 -
                Math.max(
                    data.cpu ?? 0,
                    data.ram ?? 0,
                    data.disk ?? 0
                );

            updateGlobalHealthScore(score);

        } catch (err) {

            console.error(
                'MetricGauge error:',
                err
            );
        }
    }

    await refresh();

    setInterval(
        refresh,
        5000
    );
}