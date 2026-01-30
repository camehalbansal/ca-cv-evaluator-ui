async function evaluateCV() {
  const jd = document.getElementById("jd").value;
  const cv = document.getElementById("cv").files[0];
  const output = document.getElementById("output");

  if (!jd || !cv) {
    alert("Provide JD and CV");
    return;
  }

  output.innerHTML = "⏳ Evaluating CV...";

  // DEMO MODE (Vercel-safe)
  setTimeout(() => {
    output.innerHTML = `
      <h3>Total Score: 68 / 100</h3>
      <ul>
        <li>GST: Moderate exposure, add scale</li>
        <li>Direct Tax: Needs more concrete examples</li>
        <li>Audit: Mention types of audits handled</li>
        <li>Ind AS: Missing, but JD requires it</li>
      </ul>
      <p><b>Recommendation:</b> Needs Improvement</p>
      <p class="note">
        (Full evaluation engine runs on Python backend)
      </p>
    `;
  }, 1200);
}
