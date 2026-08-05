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

    stateEl.textContent = `${data.decision} (Dummy Mode)`;
    emgEl.textContent = data.details?.emg_rms ?? "-";
    hrvEl.textContent = data.details?.hrv_sdnn ?? "-";
    gsrEl.textContent = data.details?.gsr_tonic ?? "-";
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
        biosignal: { emg_rms: 0.24, hrv_sdnn: 0.12, gsr_tonic: 0.22 },
        text_features: { text_vector: { stress: 0.1, anxious: 0.2 } }
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
