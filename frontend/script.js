async function evaluateCV() {
  const jd = document.getElementById("jd").value;
  const cv = document.getElementById("cv").files[0];
  const output = document.getElementById("output");

  if (!jd || !cv) {
    alert("Provide JD and CV");
    return;
  }

  output.innerHTML = "⏳ Evaluating...";

  const formData = new FormData();
  formData.append("jd_text", jd);
  formData.append("cv", cv);

  try {
    const res = await fetch("http://127.0.0.1:8000/evaluate", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    output.innerHTML = `
      <h3>Total Score: ${data.total}/100</h3>
      <pre>${JSON.stringify(data.scores, null, 2)}</pre>
      <ul>${data.feedback.map(f => `<li>${f}</li>`).join("")}</ul>
    `;
  } catch (e) {
    output.innerHTML = "❌ Backend not reachable";
  }
}
