// components/apiHelper.js

const API = {
    STATUS: "/status",
    MASTER_LOOP: "/runtime/master-loop",
    COGNITIVE_REPORT: "/runtime/cognitive-report",
    FEEDBACK: "/runtime/feedback"
};

async function request(url) {
    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(
                `HTTP ${response.status} ${response.statusText}`
            );
        }

        return await response.json();

    } catch (error) {
        console.error(`[API ERROR] ${url}`, error);

        return {
            error: true,
            message: error.message
        };
    }
}

export async function getStatus() {
    return request(API.STATUS);
}

export async function getMasterLoop() {
    return request(API.MASTER_LOOP);
}

export async function getCognitiveReport() {
    return request(API.COGNITIVE_REPORT);
}