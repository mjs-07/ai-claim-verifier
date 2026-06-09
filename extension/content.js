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

fetch("http://127.0.0.1:8000/health")
  .then(response => response.json())
  .then(data => {
    overlay.innerHTML = `
    <h3>AI Claim Verifier</h3>

    <p><strong>Title:</strong></p>
    <p>${pageTitle}</p>

    <p><strong>Words:</strong></p>
    <p>${wordCount}</p>

    <p><strong>Characters:</strong></p>
    <p>${characterCount}</p>

    <hr>

    <p><strong>Backend:</strong></p>
    <p>${data.status}</p>
    `;
})
  .catch(error => {
      overlay.innerHTML = `
      <h3>AI Claim Verifier</h3>
      <p>Backend Offline</p>
      `;
  });