// ── State ─────────────────────────────────────────────────
let weatherData = { temperature: 30.0, is_rainy: 0, weather_description: "Default" };
let currentLang = 'en';

// ── Translations ──────────────────────────────────────────
const T = {
    en: {
        heroTitle: "Hospital OPD <span style='color:var(--primary)'>Wait Time</span> Predictor",
        heroSub: "Predict waiting times at Indian government hospitals before you visit",
        details: "Select Visit Details",
        hospital: "Hospital",
        dept: "Department",
        date: "Visit Date",
        time: "Arrival Time",
        weather: "Weather",
        btnWeather: "Fetch Live Weather",
        btnPredict: "Predict Wait Time",
        linkHeatmap: "View Weekly Heatmap →",
        linkCompare: "View Model Comparison →",
        placeholder: "Fill in the details and click Predict",
        statusLow: "Short wait — great time to visit!",
        statusMod: "Moderate wait — plan accordingly.",
        statusHigh: "Long wait — consider a different time.",
        minsWait: "minutes wait",
        festival: "Festival Day",
        rainy: "Rainy Day",
        normal: "Normal Day",
        bestWeek: "Best Time This Week",
        bestDay: (d) => `Best Time on ${d}`,
        feedback: "Was this accurate? Give Feedback",
        feedbackPrompt: "How many minutes did you actually wait?",
        feedbackThanks: "Thank you! Feedback saved.",
        fetching: "Fetching...",
        predicting: "Predicting...",
    },
    ml: {
        heroTitle: "ആശുപത്രി OPD <span style='color:var(--primary)'>കാത്തിരിക്കൽ സമയം</span> പ്രവചനം",
        heroSub: "സന്ദർശനത്തിന് മുമ്പ് ആശുപത്രി കാത്തിരിക്കൽ സമയം അറിയൂ",
        details: "സന്ദർശന വിവരങ്ങൾ",
        hospital: "ആശുപത്രി",
        dept: "വിഭാഗം",
        date: "സന്ദർശന തീയതി",
        time: "എത്തിച്ചേരുന്ന സമയം",
        weather: "കാലാവസ്ഥ",
        btnWeather: "തത്സമയ കാലാവസ്ഥ",
        btnPredict: "കാത്തിരിക്കൽ സമയം പ്രവചിക്കൂ",
        linkHeatmap: "വാരാന്ത ഹീറ്റ്മാപ്പ് കാണൂ →",
        linkCompare: "മോഡൽ താരതമ്യം കാണൂ →",
        placeholder: "വിവരങ്ങൾ നൽകി പ്രവചിക്കൂ",
        statusLow: "ഹ്രസ്വ കാത്തിരിപ്പ് — സന്ദർശിക്കാൻ നല്ല സമയം!",
        statusMod: "മിതമായ കാത്തിരിപ്പ് — ആസൂത്രണം ചെയ്യൂ.",
        statusHigh: "ദീർഘ കാത്തിരിപ്പ് — വേറൊരു സമയം നോക്കൂ.",
        minsWait: "മിനിറ്റ് കാത്തിരിക്കൽ",
        festival: "ഉത്സവ ദിവസം",
        rainy: "മഴ ദിവസം",
        normal: "സാധാരണ ദിവസം",
        bestWeek: "ഈ ആഴ്ചയിലെ ഏറ്റവും നല്ല സമയം",
        bestDay: (d) => `${d} ലെ ഏറ്റവും നല്ല സമയം`,
        feedback: "പ്രവചനം ശരിയായിരുന്നോ? അഭിപ്രായം നൽകൂ",
        feedbackPrompt: "യഥാർത്ഥ കാത്തിരിക്കൽ സമയം എത്ര മിനിറ്റായിരുന്നു?",
        feedbackThanks: "നന്ദി! നിങ്ങളുടെ അഭിപ്രായം ലഭിച്ചു.",
        fetching: "ലഭ്യമാക്കുന്നു...",
        predicting: "പ്രവചിക്കുന്നു...",
    },
    hi: {
        heroTitle: "अस्पताल OPD <span style='color:var(--primary)'>प्रतीक्षा समय</span> भविष्यवाणी",
        heroSub: "सरकारी अस्पताल जाने से पहले प्रतीक्षा समय जानें",
        details: "यात्रा विवरण चुनें",
        hospital: "अस्पताल",
        dept: "विभाग",
        date: "यात्रा तिथि",
        time: "आगमन समय",
        weather: "मौसम",
        btnWeather: "लाइव मौसम देखें",
        btnPredict: "प्रतीक्षा समय जानें",
        linkHeatmap: "साप्ताहिक हीटमैप देखें →",
        linkCompare: "मॉडल तुलना देखें →",
        placeholder: "विवरण भरें और भविष्यवाणी करें",
        statusLow: "कम प्रतीक्षा — जाने का अच्छा समय!",
        statusMod: "मध्यम प्रतीक्षा — योजना बनाएं।",
        statusHigh: "लंबी प्रतीक्षा — दूसरा समय चुनें।",
        minsWait: "मिनट प्रतीक्षा",
        festival: "त्योहार का दिन",
        rainy: "बारिश का दिन",
        normal: "सामान्य दिन",
        bestWeek: "इस सप्ताह का सबसे अच्छा समय",
        bestDay: (d) => `${d} का सबसे अच्छा समय`,
        feedback: "क्या यह सटीक था? प्रतिक्रिया दें",
        feedbackPrompt: "आपने वास्तव में कितने मिनट प्रतीक्षा की?",
        feedbackThanks: "धन्यवाद! प्रतिक्रिया सहेजी गई।",
        fetching: "प्राप्त हो रहा है...",
        predicting: "भविष्यवाणी हो रही है...",
    }
};

// ── On Load ───────────────────────────────────────────────
window.onload = () => {
    const today = new Date().toISOString().split("T")[0];
    document.getElementById("visitDate").value = today;
    updateSlider(10);
};

// ── Set Language ──────────────────────────────────────────
function setLang(lang) {
    currentLang = lang;
    const t = T[lang];

    // Update active button
    ['en','ml','hi'].forEach(l => {
        document.getElementById(`btn-${l}`).classList.toggle('active', l === lang);
    });

    // Update all text
    document.getElementById("hero-title").innerHTML   = t.heroTitle;
    document.getElementById("hero-sub").textContent   = t.heroSub;
    document.getElementById("label-details").textContent = t.details;
    document.getElementById("label-hospital").textContent = t.hospital;
    document.getElementById("label-dept").textContent = t.dept;
    document.getElementById("label-date").textContent = t.date;
    document.getElementById("label-time").textContent = t.time;
    document.getElementById("label-weather").textContent = t.weather;
    document.getElementById("btn-weather").textContent = t.btnWeather;
    document.getElementById("btn-predict").textContent = t.btnPredict;
    document.getElementById("link-heatmap").textContent = t.linkHeatmap;
    document.getElementById("link-compare").textContent = t.linkCompare;
    document.getElementById("placeholder-text").textContent = t.placeholder;
}

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
    const btn = document.getElementById("btn-weather");
    btn.textContent = T[currentLang].fetching;
    try {
        const res = await fetch("/weather", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ hospital })
        });
        weatherData = await res.json();
        document.getElementById("weatherTemp").textContent = `${weatherData.temperature}°C`;
        document.getElementById("weatherDesc").textContent = weatherData.weather_description;
        document.getElementById("weatherRain").textContent = 
           weatherData.is_rainy ? "🌧️ Rainy — wait times may be higher" : "☀️ Clear conditions";
        btn.textContent = T[currentLang].btnWeather;
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

    if (!dateStr) { alert("Please select a visit date!"); return; }

    const date  = new Date(dateStr);
    const days  = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const day   = days[date.getDay()];
    const month = date.getMonth() + 1;

    const btn = document.getElementById("btn-predict");
    btn.textContent = T[currentLang].predicting;

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
        alert("Prediction failed. Please try again.");
    }

    btn.textContent = T[currentLang].btnPredict;
}

// ── Show Result ───────────────────────────────────────────
function showResult(data, day, hour, hospital, department, month) {
    const t = T[currentLang];
    const ampm   = hour < 12 ? "AM" : "PM";
    const dispHr = hour <= 12 ? hour : hour - 12;

    const statusText = {
        low: t.statusLow, moderate: t.statusMod, high: t.statusHigh
    };

    const festivalBadge = data.is_festival
        ? `<div class="pill">🎉 ${t.festival}</div>` : "";
    const weatherBadge = weatherData.is_rainy
        ? `<div class="pill">🌧️ ${t.rainy}</div>`
        : `<div class="pill">☀️ ${t.normal}</div>`;

    document.getElementById("resultArea").innerHTML = `
        <div class="result-box ${data.level}">
            <div class="wait-time">${data.wait_time}</div>
            <div class="wait-label">${t.minsWait}</div>
            <div class="wait-status">${statusText[data.level]}</div>
        </div>
        <div class="info-pills">
            <div class="pill">📅 ${day} at ${dispHr}:00 ${ampm}</div>
            ${festivalBadge}
            ${weatherBadge}
        </div>
        <div class="best-time-grid" id="bestTimeGrid">
            <div class="best-time-card">
                <div class="bt-label">${t.bestWeek}</div>
                <div class="bt-value" id="best-week-val">Loading...</div>
            </div>
            <div class="best-time-card">
                <div class="bt-label">${t.bestDay(day)}</div>
                <div class="bt-value" id="best-day-val">Loading...</div>
            </div>
        </div>
        <div style="margin-bottom:12px">
            <button class="btn-outline" 
                onclick="submitFeedback(${data.wait_time}, '${hospital}', '${department}')">
                ${t.feedback}
            </button>
        </div>
    `;

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

        let bestWait = 999, bestDay = "", bestHourIdx = 0;
        matrix.forEach((row, i) => {
            row.forEach((val, j) => {
                if (val < bestWait) {
                    bestWait = val; bestDay = days[i]; bestHourIdx = j;
                }
            });
        });

        const dayIdx = days.indexOf(selectedDay) >= 0 ? days.indexOf(selectedDay) : 0;
        let bestDayWait = 999, bestDayHourIdx = 0;
        matrix[dayIdx].forEach((val, j) => {
            if (val < bestDayWait) { bestDayWait = val; bestDayHourIdx = j; }
        });

        document.getElementById("best-week-val").innerHTML =
            `${bestDay}<br><small style="color:var(--muted)">${data.hours[bestHourIdx]} · ~${bestWait} min</small>`;
        document.getElementById("best-day-val").innerHTML =
            `${data.hours[bestDayHourIdx]}<br><small style="color:var(--muted)">~${bestDayWait} min</small>`;

    } catch(e) { console.log("Best time load failed", e); }
}

// ── Feedback ──────────────────────────────────────────────
async function submitFeedback(predicted, hospital, department) {
    const t = T[currentLang];
    const actual = prompt(t.feedbackPrompt);
    if (!actual) return;

    const accurate = Math.abs(parseInt(actual) - predicted) <= 10 ? "yes" : "no";
    await fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ hospital, department, predicted, actual, accurate })
    });
    alert(t.feedbackThanks);
}
