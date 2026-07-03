// ============================================================
// AI Claim Verifier
// popup.js
// Part 1/8
// Initialization
// Theme
// Backend Connection
// Main Controller
// ============================================================

const BACKEND_URL = "http://127.0.0.1:8000";

const RING_RADIUS = 60;
const RING_CIRCUMFERENCE = 2 * Math.PI * RING_RADIUS;

const analyzeButton =
    document.getElementById("analyzeBtn");

const resultsContainer =
    document.getElementById("results");

const backendStatus =
    document.getElementById("backendStatus");

const themeToggle =
    document.getElementById("themeToggle");

let loadingTimer = null;

const LOADING_STEPS = [

    {
        icon: "🤖",
        label: "Running AI Detection"
    },

    {
        icon: "📝",
        label: "Extracting Claims"
    },

    {
        icon: "🌐",
        label: "Searching Trusted Sources"
    },

    {
        icon: "🧠",
        label: "Semantic Matching"
    },

    {
        icon: "⚖️",
        label: "Verifying Evidence"
    },

    {
        icon: "📊",
        label: "Calculating Credibility"
    },

    {
        icon: "✅",
        label: "Preparing Report"
    }

];



// ============================================================
// Initialize Extension
// ============================================================

initialize();

function initialize() {

    initializeTheme();

    checkBackendHealth();

    analyzeButton.addEventListener(

        "click",

        analyzeSelectedText

    );

    themeToggle.addEventListener(

        "click",

        toggleTheme

    );

}



// ============================================================
// Theme Handling
// ============================================================

function initializeTheme() {

    if (!chrome.storage?.local) {

        applyTheme("light");

        return;

    }

    chrome.storage.local.get(

        ["theme"],

        (data) => {

            const prefersDark =

                window.matchMedia(

                    "(prefers-color-scheme: dark)"

                ).matches;

            const theme =

                data.theme ||

                (prefersDark

                    ? "dark"

                    : "light");

            applyTheme(theme);

        }

    );

}



function toggleTheme() {

    const current =

        document.documentElement.getAttribute(

            "data-theme"

        ) || "light";

    const next =

        current === "dark"

            ? "light"

            : "dark";

    applyTheme(next);

    if (chrome.storage?.local) {

        chrome.storage.local.set({

            theme: next

        });

    }

}



function applyTheme(theme) {

    document.documentElement.setAttribute(
        "data-theme",
        theme
    );

    const dark = theme === "dark";

    themeToggle.textContent = dark ? "☀️" : "🌙";

    themeToggle.setAttribute(
        "aria-label",
        dark
            ? "Switch to Light Mode"
            : "Switch to Dark Mode"
    );

}



// ============================================================
// Backend Health Check
// ============================================================

async function checkBackendHealth() {

    try {

        const response =

            await fetch(

                `${BACKEND_URL}/health`

            );

        backendStatus.classList.toggle(

            "offline",

            !response.ok

        );

    }

    catch {

        backendStatus.classList.add(

            "offline"

        );

    }

}



// ============================================================
// Analyze Selected Text
// ============================================================

async function analyzeSelectedText() {

    try {

        const selectedText =

            await getSelectedText();

        if (!selectedText) {

            showMessage(

                "Please select some text on the webpage."

            );

            return;

        }

        analyzeButton.disabled = true;

        analyzeButton.querySelector(

            ".btn-label"

        ).textContent =

            "Analyzing...";

        showLoading();

        const response =

            await fetch(

                `${BACKEND_URL}/analyze`,

                {

                    method: "POST",

                    headers: {

                        "Content-Type":

                            "application/json"

                    },

                    body: JSON.stringify({

                        text: selectedText

                    })

                }

            );

        if (!response.ok) {

            throw new Error(

                "Backend request failed."

            );

        }

        const data =

            await response.json();

        stopLoadingAnimation();

        renderDashboard(data);

    }

    catch (error) {

        stopLoadingAnimation();

        showError(

            error.message

        );

    }

    finally {

        analyzeButton.disabled = false;

        analyzeButton.querySelector(

            ".btn-label"

        ).textContent =

            "Analyze Selected Text";

    }

}



// ============================================================
// Get Highlighted Text
// ============================================================

async function getSelectedText() {

    const [tab] =

        await chrome.tabs.query({

            active: true,

            currentWindow: true

        });

    const result =

        await chrome.scripting.executeScript({

            target: {

                tabId: tab.id

            },

            func: () =>

                window

                    .getSelection()

                    .toString()

        });

    return result[0].result.trim();

}
// ============================================================
// Dashboard Renderer
// ============================================================

function renderDashboard(data) {

    const ai =
        data.ai_detection || {};

    const verificationResults =
        data.verification_results || [];

    let html = "";

    html += renderHeroCard(
        data,
        verificationResults
    );

    html += renderAIDetectionCard(
        ai
    );

    html += renderClaimsSummaryCard(
        data
    );

    verificationResults.forEach(

        (claim, index) => {

            html += renderClaim(

                claim,

                index

            );

        }

    );

    resultsContainer.innerHTML = html;

    runEntranceAnimations(

        data,

        verificationResults

    );

    attachEvidenceHandlers();

}



// ============================================================
// Hero Card
// ============================================================

function renderHeroCard(

    data,

    verificationResults

) {

    const score =

        Math.round(

            data.overall_credibility || 0

        );

    let details = "";
    let heroCardClass = "";

    if (

        verificationResults.length > 0

    ) {

        const credibility =

            verificationResults[0]

                .credibility || {};
        
        heroCardClass =
          getHeroRiskClass(
              credibility.risk_level
          );

        details = `

        <div class="grade-row">

            <span class="grade-pill">

                Grade ${credibility.grade || "-"}

            </span>

            <span class="risk-pill ${getRiskClass(

                credibility.risk_level

            )}">

                <span class="risk-dot"></span>

                ${credibility.risk_level || "Unknown"}

            </span>

        </div>

        <div class="verdict-summary">

            <strong>Summary</strong>

            <br>

            ${credibility.verification_summary || ""}

        </div>

        `;

    }

    else {

        details = `

        <div class="no-claims-note">

            No factual claims detected.

        </div>

        `;

    }

    return `

    <div class="card hero-card ${heroCardClass}">

        <div class="ring-wrap">

            <svg

                width="148"

                height="148"

                viewBox="0 0 140 140"

            >

                <circle

                    class="ring-track"

                    cx="70"

                    cy="70"

                    r="${RING_RADIUS}"

                    stroke-width="12"

                    fill="none"

                ></circle>

                <circle

                    id="scoreRing"

                    class="ring-progress"

                    cx="70"

                    cy="70"

                    r="${RING_RADIUS}"

                    stroke-width="12"

                    fill="none"

                    stroke-dasharray="${RING_CIRCUMFERENCE}"

                    stroke-dashoffset="${RING_CIRCUMFERENCE}"

                ></circle>

            </svg>

            <div class="ring-center">

                <div

                    id="scoreNumber"

                    class="ring-score"

                >

                    0

                </div>

                <div class="ring-score-label">

                    Credibility

                </div>

            </div>

        </div>

        <div

            id="scoreTarget"

            data-score="${score}"

            hidden

        ></div>

        ${details}

    </div>

    `;

}



// ============================================================
// AI Detection Card
// ============================================================

function renderAIDetectionCard(ai) {

    const probability =

        Number(

            ai.ai_probability || 0

        );

    const isAI =

        ai.classification ===

        "AI Generated";

    return `

    <div class="card">

        <div class="card-title">

            🤖 AI Detection

        </div>

        <div class="detect-row">

            <span class="detect-label">

                Classification

            </span>

            <span

                class="detect-classification

                ${

                    isAI

                        ? "ai"

                        : "human"

                }"

            >

                ${

                    isAI

                        ? "🤖"

                        : "🧑"

                }

                ${

                    ai.classification ||

                    "Unknown"

                }

            </span>

        </div>

        <div class="detect-label">

            AI Probability

        </div>

        <div class="gauge-track">

            <div

                id="aiGauge"

                class="gauge-fill

                ${

                    isAI

                        ? ""

                        : "human"

                }"

                data-value="${probability}"

            ></div>

        </div>

        <div

            id="aiGaugeValue"

            class="gauge-value"

        >

            0%

        </div>

    </div>

    `;

}



// ============================================================
// Claims Summary Card
// ============================================================

function renderClaimsSummaryCard(data) {

    return `

    <div class="card">

        <div class="card-title">

            📋 Claims Summary

        </div>

        <div class="stat-grid">

            <div class="stat-box supported">

                <div class="stat-num">

                    ${data.supported_claims}

                </div>

                <div class="stat-label">

                    Supported

                </div>

            </div>

            <div class="stat-box contradicted">

                <div class="stat-num">

                    ${data.contradicted_claims}

                </div>

                <div class="stat-label">

                    Contradicted

                </div>

            </div>

            <div class="stat-box unknown">

                <div class="stat-num">

                    ${data.unknown_claims}

                </div>

                <div class="stat-label">

                    Unknown

                </div>

            </div>

            <div class="stat-box total">

                <div class="stat-num">

                    ${data.claims_found}

                </div>

                <div class="stat-label">

                    Total

                </div>

            </div>

        </div>

    </div>

    `;

}
// ============================================================
// Individual Claim Card
// ============================================================

function renderClaim(
    result,
    index
) {

    const statusClass =
        getStatusClass(
            result.status
        );

    const confidence =
        Math.round(
            result.confidence || 0
        );

    let evidenceHTML = "";

    if (
        result.evidence &&
        result.evidence.length > 0
    ) {

        evidenceHTML =
            result.evidence
                .map(renderEvidence)
                .join("");

    }

    else {

        evidenceHTML =

        `<p class="no-evidence">

            No supporting evidence found.

        </p>`;

    }

    return `

    <div class="card claim-card">

        <div class="claim-head">

            <div>

                <div class="claim-index">

                    Claim ${index + 1}

                </div>

                <div class="claim-text">

                    ${escapeHTML(result.claim)}

                </div>

            </div>

            <span
                class="status-badge ${statusClass}"
            >

                ${result.status}

            </span>

        </div>

        <div class="confidence-row">

            <span class="confidence-label">

                Confidence

            </span>

            <div class="confidence-track">

                <div

                    id="confidenceFill-${index}"

                    class="confidence-fill"

                    data-value="${confidence}"

                ></div>

            </div>

            <span

                id="confidenceValue-${index}"

                class="confidence-value"

            >

                0%

            </span>

        </div>

        <button

            class="evidence-btn"

            data-target="evidence-${index}"

            aria-expanded="false"

        >

            <span>

                View Evidence

            </span>

        </button>

        <div

            id="evidence-${index}"

            class="evidence-container"

        >

            ${evidenceHTML}

        </div>

    </div>

    `;

}



// ============================================================
// Evidence Card
// ============================================================

function renderEvidence(
    evidence
) {

    const domain =
        evidence.domain || "";

    const favicon =

        domain

        ?

        `https://www.google.com/s2/favicons?sz=64&domain=${encodeURIComponent(domain)}`

        :

        "";

    const statusClass =
        getStatusClass(
            evidence.nli_status
        );

    return `

    <div class="evidence-card">

        <div class="favicon">

            ${

                favicon

                ?

                `<img

                    src="${favicon}"

                    alt=""

                    loading="lazy"

                >`

                :

                ""

            }

        </div>

        <div class="evidence-body">

            <div class="evidence-title">

                ${escapeHTML(
                    evidence.title
                )}

            </div>

            <div class="evidence-domain">

                🌐 ${escapeHTML(domain)}

            </div>

            <div class="evidence-meta">

                <span class="chip tier">

                    Tier ${evidence.tier}

                </span>

                <span class="chip trust">

                    Trust ${evidence.source_trust}

                </span>

                <span class="chip sim">

                    Similarity ${Math.round(
                        evidence.similarity
                    )}%

                </span>

                <span class="chip">

                    NLI ${Math.round(
                        evidence.nli_confidence
                    )}%

                </span>

            </div>

            <div class="evidence-footer">

                <span

                    class="nli-badge ${statusClass}"

                >

                    ${evidence.nli_status}

                </span>

                <a

                    href="${escapeAttr(
                        evidence.url
                    )}"

                    target="_blank"

                    rel="noopener"

                    class="source-link"

                >

                    Open Source ↗

                </a>

            </div>

        </div>

    </div>

    `;

}
// ============================================================
// Loading Screen
// ============================================================

function showLoading() {

    resultsContainer.innerHTML = `

    <div class="card loading-card">

        <div class="loading-title">

            <span class="spinner"></span>

            Analyzing Content

        </div>

        <div class="progress-track">

            <div

                id="progressFill"

                class="progress-fill"

            ></div>

        </div>

        <div class="loading-stage">

            <span

                id="stageIcon"

                class="stage-icon"

            >

                ${LOADING_STEPS[0].icon}

            </span>

            <span

                id="stageText"

                class="stage-text"

            >

                ${LOADING_STEPS[0].label}

            </span>

        </div>

        <div

            id="stageDots"

            class="stage-dots"

        >

            ${LOADING_STEPS.map(() =>

                `<span class="stage-dot"></span>`

            ).join("")}

        </div>

    </div>

    `;

    animateLoading();

}



// ============================================================
// Loading Animation
// ============================================================

function animateLoading() {

    const fill =

        document.getElementById(
            "progressFill"
        );

    const icon =

        document.getElementById(
            "stageIcon"
        );

    const text =

        document.getElementById(
            "stageText"
        );

    const dots =

        document.querySelectorAll(
            ".stage-dot"
        );

    let step = 0;

    clearInterval(
        loadingTimer
    );

    loadingTimer =

        setInterval(() => {

            if (
                step >= LOADING_STEPS.length
            ) {

                return;

            }

            const progress =

                (

                    (step + 1)

                    /

                    LOADING_STEPS.length

                ) * 100;

            fill.style.width =
                progress + "%";

            icon.textContent =

                LOADING_STEPS[step].icon;

            text.textContent =

                LOADING_STEPS[step].label;

            dots.forEach(

                (dot, index) => {

                    dot.classList.remove(

                        "active",

                        "filled"

                    );

                    if (
                        index < step
                    ) {

                        dot.classList.add(
                            "filled"
                        );

                    }

                    if (
                        index === step
                    ) {

                        dot.classList.add(
                            "active"
                        );

                    }

                }

            );

            step++;

        },

        850

    );

}



// ============================================================
// Stop Loading
// ============================================================

function stopLoadingAnimation() {

    clearInterval(
        loadingTimer
    );

    loadingTimer = null;

}
// ============================================================
// Entrance Animations
// ============================================================

function runEntranceAnimations(
    data,
    verificationResults
) {

    requestAnimationFrame(() => {

        // ---------------------------------
        // Credibility Ring
        // ---------------------------------

        const scoreTarget =

            document.getElementById(
                "scoreTarget"
            );

        if (scoreTarget) {

            animateScoreRing(

                Number(
                    scoreTarget.dataset.score
                )

            );

        }

        // ---------------------------------
        // AI Probability Gauge
        // ---------------------------------

        const gauge =

            document.getElementById(
                "aiGauge"
            );

        if (gauge) {

            animateGauge(

                gauge,

                "aiGaugeValue",

                Number(
                    gauge.dataset.value
                )

            );

        }

        // ---------------------------------
        // Confidence Bars
        // ---------------------------------

        document

            .querySelectorAll(
                ".confidence-fill"
            )

            .forEach((bar, index) => {

                animateConfidenceBar(

                    bar,

                    `confidenceValue-${index}`,

                    Number(
                        bar.dataset.value
                    )

                );

            });

    });

}



// ============================================================
// Credibility Ring Animation
// ============================================================

function animateScoreRing(target) {

    const ring = document.getElementById("scoreRing");
    const number = document.getElementById("scoreNumber");

    if (!ring || !number) return;

    const start = performance.now();
    const duration = 1200;

    // Final destination color
    const finalColor = scoreToColor(target);
    console.log(finalColor);

    function animate(now) {

        const progress = clamp(
            (now - start) / duration,
            0,
            1
        );

        const eased = 1 - Math.pow(1 - progress, 3);

        const value = eased * target;

        number.textContent = Math.round(value);

        ring.style.strokeDashoffset =
            RING_CIRCUMFERENCE -
            (value / 100) * RING_CIRCUMFERENCE;

        // Animate from red → final color
        const animatedColor = mixHexColors(
            "#ef4444",
            finalColor,
            eased
        );

        document.documentElement.style.setProperty(
          "--ring-color",
          animatedColor
      );

        if (progress < 1) {

            requestAnimationFrame(animate);

        } else {

            // Lock the final color
            document.documentElement.style.setProperty(
                "--ring-color",
                finalColor
            );

            number.textContent = target;
        }
    }

    requestAnimationFrame(animate);
}



// ============================================================
// AI Probability Animation
// ============================================================

function animateGauge(

    gauge,

    valueId,

    target

) {

    const valueElement =

        document.getElementById(
            valueId
        );

    const start =
        performance.now();

    const duration = 900;

    function animate(now) {

        const progress =

            clamp(

                (now - start) /
                duration,

                0,

                1

            );

        const eased =

            1 -

            Math.pow(

                1 - progress,

                3

            );

        const value =
            eased * target;

        gauge.style.width =
            value + "%";

        valueElement.textContent =

            value.toFixed(2) +

            "%";

        if (

            progress < 1

        ) {

            requestAnimationFrame(
                animate
            );

        }

        else {

            valueElement.textContent =

                target.toFixed(2) +

                "%";

        }

    }

    requestAnimationFrame(
        animate
    );

}



// ============================================================
// Confidence Bar Animation
// ============================================================

function animateConfidenceBar(

    bar,

    valueId,

    target

) {

    const valueElement =

        document.getElementById(
            valueId
        );

    const start =
        performance.now();

    const duration = 900;

    function animate(now) {

        const progress =

            clamp(

                (now - start) /
                duration,

                0,

                1

            );

        const eased =

            1 -

            Math.pow(

                1 - progress,

                3

            );

        const value =
            eased * target;

        bar.style.width =
            value + "%";

        valueElement.textContent =

            Math.round(value) +

            "%";

        if (

            progress < 1

        ) {

            requestAnimationFrame(
                animate
            );

        }

        else {

            valueElement.textContent =

                Math.round(target) +

                "%";

        }

    }

    requestAnimationFrame(
        animate
    );

}



// ============================================================
// Ring Color Interpolation
// ============================================================

function scoreToColor(score) {

    const style =

        getComputedStyle(
            document.documentElement
        );

    const low =

        style
            .getPropertyValue(
                "--score-low"
            )
            .trim();

    const mid =

        style
            .getPropertyValue(
                "--score-mid"
            )
            .trim();

    const high =

        style
            .getPropertyValue(
                "--score-high"
            )
            .trim();

    if (

        score <= 50

    ) {

        return mixHexColors(

            low,

            mid,

            score / 50

        );

    }

    return mixHexColors(

        mid,

        high,

        (score - 50) / 50

    );

}



// ============================================================
// Color Mixing
// ============================================================

function mixHexColors(

    colorA,

    colorB,

    ratio

) {

    const a =
        hexToRGB(colorA);

    const b =
        hexToRGB(colorB);

    const r = Math.round(

        a.r +

        (b.r - a.r) *

        ratio

    );

    const g = Math.round(

        a.g +

        (b.g - a.g) *

        ratio

    );

    const bl = Math.round(

        a.b +

        (b.b - a.b) *

        ratio

    );

    return `rgb(${r}, ${g}, ${bl})`;

}



// ============================================================
// HEX → RGB
// ============================================================

function hexToRGB(color){

    if(color.startsWith("rgb")){

        const values = color.match(/\d+/g).map(Number);

        return{

            r: values[0],
            g: values[1],
            b: values[2]

        };

    }

    color = color.replace("#","");

    if(color.length===3){

        color = color.split("").map(c=>c+c).join("");

    }

    const number = parseInt(color,16);

    return{

        r:(number>>16)&255,
        g:(number>>8)&255,
        b:number&255

    };

}

// ============================================================
// Evidence Expand / Collapse
// ============================================================

function attachEvidenceHandlers() {

    const buttons =

        document.querySelectorAll(
            ".evidence-btn"
        );

    buttons.forEach(button => {

        button.onclick = () => {

            const container =

                document.getElementById(

                    button.dataset.target

                );

            if (!container)
                return;

            const isOpen =

                container.classList.toggle(
                    "open"
                );

            button.setAttribute(

                "aria-expanded",

                String(isOpen)

            );

            const label =

                button.querySelector("span");

            if (label) {

                label.textContent =

                    isOpen

                        ? "Hide Evidence"

                        : "View Evidence";

            }

        };

    });

}



// ============================================================
// Error Screen
// ============================================================

function showError(message) {

    resultsContainer.innerHTML = `

    <div class="card error-card">

        <div class="error-title">

            ⚠ Analysis Failed

        </div>

        <div class="error-message">

            ${escapeHTML(message)}

        </div>

        <ul class="error-reasons">

            <li>

                Ensure the FastAPI backend is running.

            </li>

            <li>

                Ensure SearXNG is reachable.

            </li>

            <li>

                Check your internet connection.

            </li>

            <li>

                Inspect the browser console for details.

            </li>

        </ul>

    </div>

    `;

}



// ============================================================
// Information Message
// ============================================================

function showMessage(message) {

    resultsContainer.innerHTML = `

    <div class="card message-card">

        ${escapeHTML(message)}

    </div>

    `;

}



// ============================================================
// Empty Results Screen
// ============================================================

function showNoClaims() {

    resultsContainer.innerHTML = `

    <div class="card message-card">

        <h3>

            No Claims Found

        </h3>

        <p>

            The selected text does not contain
            any factual claims that require
            verification.

        </p>

    </div>

    `;

}



// ============================================================
// Backend Offline Screen
// ============================================================

function showBackendOffline() {

    resultsContainer.innerHTML = `

    <div class="card error-card">

        <div class="error-title">

            🔴 Backend Offline

        </div>

        <div class="error-message">

            Could not connect to the local
            verification server.

        </div>

        <ul class="error-reasons">

            <li>

                Start FastAPI

            </li>

            <li>

                Verify port 8000

            </li>

            <li>

                Reload the extension

            </li>

        </ul>

    </div>

    `;

}



// ============================================================
// Refresh Backend Status
// ============================================================

function refreshBackendStatus() {

    checkBackendHealth();

}
// ============================================================
// Clamp Number
// ============================================================

function clamp(

    value,

    min,

    max

) {

    return Math.min(

        Math.max(

            value,

            min

        ),

        max

    );

}



// ============================================================
// Status Badge Mapping
// ============================================================

function getStatusClass(status) {

    switch (status) {

        case "Supported":

            return "supported";

        case "Contradicted":

            return "contradicted";

        case "Insufficient Evidence":

        case "Unknown":

        default:

            return "unknown";

    }

}



// ============================================================
// Risk Badge Mapping
// ============================================================

function getRiskClass(riskLevel) {

    switch (riskLevel) {

        case "Very Low":

            return "risk-verylow";

        case "Low":

            return "risk-low";

        case "Moderate":

            return "risk-moderate";

        case "Elevated":

            return "risk-elevated";

        case "High":

            return "risk-high";

        case "Very High":

            return "risk-veryhigh";

        default:

            return "risk-moderate";

    }

}

function getHeroRiskClass(level){

    switch(level){

        case "Very Low":
        case "Low":
            return "hero-green";

        case "Moderate":
            return "hero-yellow";

        case "Elevated":
            return "hero-orange";

        case "High":
        case "Very High":
            return "hero-red";

        default:
            return "";

    }

}



// ============================================================
// Safe HTML Escaping
// ============================================================

function escapeHTML(text) {

    return String(

        text ?? ""

    ).replace(

        /[&<>"']/g,

        character => ({

            "&": "&amp;",

            "<": "&lt;",

            ">": "&gt;",

            "\"": "&quot;",

            "'": "&#39;"

        })[character]

    );

}



// ============================================================
// Safe Attribute Escaping
// ============================================================

function escapeAttr(text) {

    return escapeHTML(text);

}



// ============================================================
// Safe Percentage Formatter
// ============================================================

function formatPercentage(value) {

    if (

        value === null ||

        value === undefined ||

        isNaN(value)

    ) {

        return "0%";

    }

    return Number(value).toFixed(2) + "%";

}



// ============================================================
// Safe Integer Formatter
// ============================================================

function formatInteger(value) {

    if (

        value === null ||

        value === undefined ||

        isNaN(value)

    ) {

        return "0";

    }

    return Math.round(value).toString();

}
// ============================================================
// Safe Object Getter
// ============================================================

function safeGet(object, key, defaultValue = "") {

    if (

        object === null ||

        object === undefined

    ) {

        return defaultValue;

    }

    const value = object[key];

    return (

        value === undefined ||

        value === null

    )

        ? defaultValue

        : value;

}



// ============================================================
// Safe Array
// ============================================================

function safeArray(value) {

    return Array.isArray(value)

        ? value

        : [];

}



// ============================================================
// Safe Number
// ============================================================

function safeNumber(value) {

    const number = Number(value);

    return Number.isFinite(number)

        ? number

        : 0;

}



// ============================================================
// Delay Utility
// ============================================================

function delay(milliseconds) {

    return new Promise(resolve =>

        setTimeout(

            resolve,

            milliseconds

        )

    );

}



// ============================================================
// Logger
// ============================================================

function log(...args) {

    console.log(

        "[AI Claim Verifier]",

        ...args

    );

}



// ============================================================
// Warn
// ============================================================

function warn(...args) {

    console.warn(

        "[AI Claim Verifier]",

        ...args

    );

}



// ============================================================
// Error Logger
// ============================================================

function error(...args) {

    console.error(

        "[AI Claim Verifier]",

        ...args

    );

}



// ============================================================
// Development Banner
// ============================================================

log("Popup Loaded");




// ============================================================
// End of popup.js
// ============================================================