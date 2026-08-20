const apiUrl = "http://localhost:8000/api/fuse";

async function fetchStressData(payload) {
    const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });
    return response.json();
}

function renderState(data) {
    const stateEl = document.getElementById("stressState");
    const emgEl = document.getElementById("emgValue");
    const hrvEl = document.getElementById("hrvValue");
    const gsrEl = document.getElementById("gsrValue");

    const fusion = data.details || {};
    const input = fusion.details?.input || fusion.input || {};
    const label = fusion.color
        ? `${fusion.color} / ${fusion.level}`
        : `${data.decision}`;
    stateEl.textContent = `${label} (Dummy Mode)`;
    emgEl.textContent = input.emg ?? "-";
    hrvEl.textContent = input.hrv ?? "-";
    gsrEl.textContent = input.gsr ?? "-";
}

function renderDummyState() {
    renderState({
        decision: "NORMAL",
        details: {
            emg_rms: 0.25,
            hrv_sdnn: 0.16,
            gsr_tonic: 0.18
        }
    });
}

async function initDashboard() {
    const demoPayload = {
        biosignal: { emg: 0.24, hrv: 72.0, gsr: 3.1 },
        text_features: { text_post: "belajar dengan tenang" }
    };

    try {
        const result = await fetchStressData(demoPayload);
        renderState(result);
    } catch (error) {
        console.warn("Backend unavailable; showing dummy data.", error);
        renderDummyState();
    }
}

initDashboard();
