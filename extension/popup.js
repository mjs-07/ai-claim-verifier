document
    .getElementById("analyzeBtn")
    .addEventListener("click", async () => {

        const [tab] = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        const results = await chrome.scripting.executeScript({
            target: {
                tabId: tab.id
            },
            func: () => window.getSelection().toString()
        });

        const selectedText = results[0].result;

        if (!selectedText) {

            document.getElementById("results").innerHTML =
                "<p>Please select some text first.</p>";

            return;
        }

        document.getElementById("results").innerHTML =
            "<p>Analyzing...</p>";

        try {

            // ==========================
            // STEP 1 - AI DETECTION
            // ==========================

            const aiResponse = await fetch(
                "http://127.0.0.1:8000/detect_text_ai",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        text: selectedText
                    })
                }
            );

            const aiData = await aiResponse.json();

            // ==========================
            // STEP 2 - CLAIM EXTRACTION
            // ==========================

            const claimResponse = await fetch(
                "http://127.0.0.1:8000/extract_claims",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        text: selectedText
                    })
                }
            );

            const claimData = await claimResponse.json();

            const claims = claimData.claims;

            // ==========================
            // STEP 3 - VERIFICATION
            // ==========================

            let verificationResults = [];

            for (const claim of claims) {

                const verifyResponse = await fetch(
                    "http://127.0.0.1:8000/verify_claim",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            claim: claim
                        })
                    }
                );

                const verifyData =
                    await verifyResponse.json();

                verificationResults.push(
                    verifyData
                );
            }

            // ==========================
            // STEP 4 - CREDIBILITY SCORE
            // ==========================

            let averageVerification = 0;

            if (verificationResults.length > 0) {

                const totalConfidence =
                    verificationResults.reduce(
                        (sum, item) =>
                            sum + item.confidence,
                        0
                    );

                averageVerification =
                    totalConfidence /
                    verificationResults.length;
            }

            const humanScore =
                100 - aiData.ai_probability;

            const credibilityScore =
                Math.round(
                    (0.7 * averageVerification) +
                    (0.3 * humanScore)
                );

            // ==========================
            // STEP 5 - RISK BADGE
            // ==========================

            let riskLevel = "Medium Risk";
            let riskClass = "medium-risk";

            if (
                aiData.ai_probability < 30 &&
                credibilityScore > 70
            ) {
                riskLevel = "Low Risk";
                riskClass = "low-risk";
            }
            else if (
                aiData.ai_probability > 70 &&
                credibilityScore < 50
            ) {
                riskLevel = "High Risk";
                riskClass = "high-risk";
            }

            // ==========================
            // STEP 6 - RENDER UI
            // ==========================

            let claimsHtml = "";

            if (claims.length === 0) {

                claimsHtml =
                    "<p>No factual claims detected.</p>";

            } else {

                verificationResults.forEach(
                    (result, index) => {

                        let evidenceHtml = "";

                        if (
                            result.evidence &&
                            result.evidence.length > 0
                        ) {

                            evidenceHtml +=
                                "<div class='evidence-list'>";

                            result.evidence.forEach(
                                evidence => {

                                    evidenceHtml += `
                                    <a
                                        href="${evidence.url}"
                                        target="_blank"
                                        class="evidence-link"
                                    >
                                        🔗 ${evidence.title}
                                    </a>
                                    <br>
                                    `;
                                }
                            );

                            evidenceHtml += "</div>";
                        }
                        else {

                        evidenceHtml = `
                        <p class="no-evidence">
                            No supporting evidence found.
                        </p>
                        `;
                        }

                        const evidenceId = "evidence-" + index;

                        const buttonLabel =
                            result.evidence &&
                            result.evidence.length > 0
                                ? "View Evidence"
                                : "No Evidence Available";

                        claimsHtml += `
                        <div class="claim">

                            <p>
                                <strong>Claim:</strong>
                            </p>

                            <p>${result.claim}</p>

                            <p>
                                <strong>Status:</strong>
                                ${result.status}
                            </p>

                            <p>
                                <strong>Confidence:</strong>
                                ${result.confidence}%
                            </p>

                            <button
                                class="evidence-btn"
                                data-target="${evidenceId}"
                                data-default-label="${buttonLabel}"
                            >
                                ${buttonLabel}
                            </button>

                            <div
                                id="${evidenceId}"
                                class="evidence-container"
                                style="display:none;"
                            >

                                ${evidenceHtml}

                            </div>

                        </div>
                        `;
                    }
                );
            }

            document.getElementById(
                "results"
            ).innerHTML = `

            <div class="card">

                <div class="score">
                    ${credibilityScore}/100
                </div>

                <p style="text-align:center;">
                    Trust Score
                </p>

                <p
                    class="${riskClass}"
                    style="text-align:center;"
                >
                    ${riskLevel}
                </p>

            </div>

            <div class="card">

                <p>
                    <strong>AI Probability:</strong>
                    ${aiData.ai_probability}%
                </p>

                <p>
                    <strong>Classification:</strong>
                    ${aiData.classification}
                </p>

            </div>

            <div class="card">

                <p>
                    <strong>Claims Found:</strong>
                    ${claims.length}
                </p>

                ${claimsHtml}

            </div>
            `;

            document.addEventListener("click", (event) => {

                if (
                    !event.target.classList.contains(
                        "evidence-btn"
                    )
                ) {
                    return;
                }

                const button = event.target;

                console.log("Button clicked");

                console.log(button.dataset.target);

                const target =
                    document.getElementById(
                        button.dataset.target
                    );

                console.log("Target:");
                console.log(target);

                if (!target) {
                    console.log("TARGET NOT FOUND");
                    return;
                }

                console.log(
                    "Current display:",
                    target.style.display
                );

                if (
                    target.style.display === "none" ||
                    target.style.display === ""
                ) {

                    target.style.display = "block";

                    button.innerText =
                        "Hide Evidence";

                    console.log(
                        "Changed to BLOCK"
                    );

                } else {

                    target.style.display = "none";

                    button.innerText =
                        button.dataset.defaultLabel;

                    console.log(
                        "Changed to NONE"
                    );
                }
            });

        } catch (error) {

            console.error(error);

            document.getElementById(
                "results"
            ).innerHTML =
                "<p>Analysis Failed</p>";
        }
    });

