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

fetch("http://127.0.0.1:8000/analyze", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        title: pageTitle,
        text: pageText
    })
})
.then(response => response.json())
.then(data => {

    overlay.innerHTML = `
    <h3>AI Claim Verifier</h3>

    <p><strong>Title:</strong></p>
    <p>${data.title}</p>

    <p><strong>Words:</strong></p>
    <p>${data.word_count}</p>

    <p><strong>Characters:</strong></p>
    <p>${data.character_count}</p>

    <hr>

    <p>${data.analysis}</p>
    `;
})
.catch(error => {

    console.error(error);

    overlay.innerHTML = `
    <h3>AI Claim Verifier</h3>
    <p>Analysis Failed</p>
    `;
});