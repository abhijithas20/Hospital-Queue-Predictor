// ── State ─────────────────────────────────────────────────
let weatherData = { temperature: 30.0, is_rainy: 0, weather_description: "Default" };
let isML = false; // language toggle

// ── On Load ───────────────────────────────────────────────
window.onload = () => {
    // Set today's date as default
    const today = new Date().toISOString().split("T")[0];
    document.getElementById("visitDate").value = today;
    updateSlider(10);
};

// ── Slider ────────────────────────────────────────────────
function updateSlider(val) {
    val = parseInt(val);
    const ampm = val < 12 ? "AM" : "PM";
    const display = val <= 12 ? val : val - 12;
    document.getElementById("sliderLabel").textContent = `${display}:00 ${ampm}`;
}

// ── Fetch Weather ─────────────────────────────────────────
async function fetchWeather() {
    const hospital = document.getElementById("hospital").value;
    const btn = document.querySelector(".btn-outline");
    btn.textContent = "Fetching...";

    try {
        const res = await fetch("/weather", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ hospital })
        });
        weatherData = await res.json();
        document.getElementById("weatherTemp").textContent = `${weatherData.temperature}°C`;
        document.getElementById("weatherDesc").textContent = weatherData.weather_description;
        btn.textContent = isML ? "തത്സമയ കാലാവസ്ഥ" : "Fetch Live Weather";
    } catch (e) {
        btn.textContent = "Failed — using defaults";
    }
}

// ── Predict ───────────────────────────────────────────────
async function predict() {
    const hospital   = document.getElementById("hospital").value;
    const department = document.getElementById("department").value;
    const dateStr    = document.getElementById("visitDate").value;
    const hour       = parseInt(document.getElementById("hourSlider").value);

    if (!dateStr) {
        alert("Please select a visit date!");
        return;
    }

    const date  = new Date(dateStr);
    const days  = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const day   = days[date.getDay()];
    const month = date.getMonth() + 1;

    const btn = document.querySelector(".btn-primary");
    btn.textContent = "Predicting...";

    try {
        const res = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                hospital, department, day, hour, month,
                temperature: weatherData.temperature,
                is_rainy: weatherData.is_rainy,
                date: dateStr
            })
        });

        const data = await res.json();
        showResult(data, day, hour, hospital, department, month);
    } catch (e) {
        alert("Prediction failed. Is Flask running?");
    }

    btn.textContent = isML ? "കാത്തിരിക്കൽ സമയം പ്രവചിക്കൂ" : "Predict Wait Time";
}

// ── Show Result ───────────────────────────────────────────
function showResult(data, day, hour, hospital, department, month) {
    const ampm   = hour < 12 ? "AM" : "PM";
    const dispHr = hour <= 12 ? hour : hour - 12;

    const statusText = {
        low:      isML ? "ഹ്രസ്വ കാത്തിരിപ്പ് — സന്ദർശിക്കാൻ നല്ല സമയം!" : "Short wait — great time to visit!",
        moderate: isML ? "മിതമായ കാത്തിരിപ്പ് — ആസൂത്രണം ചെയ്യൂ." : "Moderate wait — plan accordingly.",
        high:     isML ? "ദീർഘ കാത്തിരിപ്പ് — വേറൊരു സമയം നോക്കൂ." : "Long wait — consider a different time."
    };

    const festivalBadge = data.is_festival
        ? `<div class="pill">🎉 ${isML ? "ഉത്സവ ദിവസം" : "Festival Day"}</div>`
        : "";

    const rainyBadge = weatherData.is_rainy
        ? `<div class="pill">🌧️ ${isML ? "മഴ ദിവസം" : "Rainy Day"}</div>`
        : `<div class="pill">☀️ ${isML ? "സാധാരണ ദിവസം" : "Normal Day"}</div>`;

    document.getElementById("resultArea").innerHTML = `
        <div class="result-box ${data.level}">
            <div class="wait-time">${data.wait_time}</div>
            <div class="wait-label">${isML ? "മിനിറ്റ് കാത്തിരിക്കൽ" : "minutes wait"}</div>
            <div class="wait-status">${statusText[data.level]}</div>
        </div>

        <div class="info-pills">
            <div class="pill">📅 ${day} ${isML ? "at" : "at"} ${dispHr}:00 ${ampm}</div>
            ${festivalBadge}
            ${rainyBadge}
        </div>

        <div class="best-time-grid" id="bestTimeGrid">
            <div class="best-time-card">
                <div class="bt-label">${isML ? "ഈ ആഴ്ചയിലെ ഏറ്റവും നല്ല സമയം" : "Best Time This Week"}</div>
                <div class="bt-value">Loading...</div>
            </div>
            <div class="best-time-card">
                <div class="bt-label">${isML ? `${day} ലെ ഏറ്റവും നല്ല സമയം` : `Best Time on ${day}`}</div>
                <div class="bt-value">Loading...</div>
            </div>
        </div>

        <div style="margin-bottom:12px">
            <button class="btn-outline" onclick="submitFeedback(${data.wait_time}, '${hospital}', '${department}')">
                ${isML ? "പ്രവചനം ശരിയായിരുന്നോ? അഭിപ്രായം നൽകൂ" : "Was this accurate? Give Feedback"}
            </button>
        </div>
    `;

    // Load heatmap data for best time
    loadBestTime(hospital, department, month, day);
}

// ── Best Time ─────────────────────────────────────────────
async function loadBestTime(hospital, department, month, selectedDay) {
    try {
        const res = await fetch("/heatmap_data", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                hospital, department, month,
                temperature: weatherData.temperature,
                is_rainy: weatherData.is_rainy,
                is_festival: 0
            })
        });
        const data = await res.json();
        const matrix = data.matrix;
        const days   = data.days;
        const hours  = list => list;

        // Best overall
        let bestWait = 999, bestDay = "", bestHourIdx = 0;
        matrix.forEach((row, i) => {
            row.forEach((val, j) => {
                if (val < bestWait) {
                    bestWait = val; bestDay = days[i]; bestHourIdx = j;
                }
            });
        });

        // Best on selected day
        const dayIdx = days.indexOf(selectedDay) >= 0 ? days.indexOf(selectedDay) : 0;
        let bestDayWait = 999, bestDayHourIdx = 0;
        matrix[dayIdx].forEach((val, j) => {
            if (val < bestDayWait) { bestDayWait = val; bestDayHourIdx = j; }
        });

        const cards = document.querySelectorAll(".best-time-card .bt-value");
        cards[0].innerHTML = `${bestDay}<br><small style="color:var(--muted)">${data.hours[bestHourIdx]} · ~${bestWait} min</small>`;
        cards[1].innerHTML = `${data.hours[bestDayHourIdx]}<br><small style="color:var(--muted)">~${bestDayWait} min</small>`;

    } catch(e) {
        console.log("Best time load failed", e);
    }
}

// ── Feedback ──────────────────────────────────────────────
async function submitFeedback(predicted, hospital, department) {
    const actual = prompt(isML 
        ? "യഥാർത്ഥ കാത്തിരിക്കൽ സമയം എത്ര മിനിറ്റായിരുന്നു?" 
        : "How many minutes did you actually wait?");
    if (!actual) return;

    const accurate = Math.abs(parseInt(actual) - predicted) <= 10 ? "yes" : "no";

    await fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ hospital, department, predicted, actual, accurate })
    });

    alert(isML ? "നന്ദി! നിങ്ങളുടെ അഭിപ്രായം ലഭിച്ചു." : "Thank you! Feedback saved.");
}

// ── Language Toggle ────────────────────────────────────────
function toggleLang() {
    isML = !isML;
    document.getElementById("langBtn").textContent = isML ? "English" : "മലയാളം";

    document.querySelectorAll("[data-en]").forEach(el => {
        if (isML) {
            el.innerHTML = el.getAttribute("data-ml");
        } else {
            el.innerHTML = el.getAttribute("data-en");
        }
    });
}