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
            // STEP 5 - RENDER UI
            // ==========================

            let claimsHtml = "";

            if (claims.length === 0) {

                claimsHtml =
                    "<p>No factual claims detected.</p>";

            } else {

                claimsHtml = "<ul>";

                verificationResults.forEach(
                    result => {

                        claimsHtml += `
                            <li>
                                ${result.claim}
                                <br>
                                <strong>
                                    ${result.status}
                                </strong>
                                (${result.confidence}%)
                            </li>
                        `;
                    }
                );

                claimsHtml += "</ul>";
            }

            document.getElementById(
                "results"
            ).innerHTML = `

                <hr>

                <p>
                    <strong>AI Probability:</strong>
                    ${aiData.ai_probability}%
                </p>

                <p>
                    <strong>Classification:</strong>
                    ${aiData.classification}
                </p>

                <hr>

                <p>
                    <strong>Claims Found:</strong>
                    ${claims.length}
                </p>

                ${claimsHtml}

                <hr>

                <p>
                    <strong>Credibility Score:</strong>
                    ${credibilityScore}/100
                </p>
            `;

        } catch (error) {

            console.error(error);

            document.getElementById(
                "results"
            ).innerHTML =
                "<p>Analysis Failed</p>";
        }
    });