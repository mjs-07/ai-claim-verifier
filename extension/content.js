console.log("AI Claim Verifier Loaded");
const pageTitle = document.title;

const pageText = document.body.innerText;

const wordCount = pageText
    .trim()
    .split(/\s+/) // Splits on spaces, tabs and new lines
    .length;

const characterCount = pageText.length;

const overlay = document.createElement("div");

overlay.id = "ai-claim-verifier-overlay";

overlay.innerHTML = `
<h3>AI Claim Verifier</h3>
<p>Checking backend...</p>
`;

document.body.appendChild(overlay);

fetch("http://127.0.0.1:8000/detect_text_ai", {
    method: "POST",

    headers: {
        "Content-Type": "application/json"
    },

    body: JSON.stringify({
        text: pageText
    })
})
.then(response => response.json())
.then(data => {

    overlay.innerHTML = `
    <h3>AI Claim Verifier</h3>

    <p><strong>Title:</strong></p>
    <p>${pageTitle}</p>

    <hr>

    <p><strong>AI Probability:</strong></p>
    <p>${data.ai_probability}%</p>

    <p><strong>Classification:</strong></p>
    <p>${data.classification}</p>
    `;
})
.catch(error => {

    console.error(error);

    overlay.innerHTML = `
    <h3>AI Claim Verifier</h3>
    <p>Detection Failed</p>
    `;
});