/* ---------- UPLOAD PAGE ---------- */
async function analyze() {
  const fileInput = document.getElementById("resumeFile");
  const error = document.getElementById("error");
  const loading = document.getElementById("loading");
  const spinner = document.getElementById("spinner");
  const btn = document.getElementById("analyzeBtn");
  const file = fileInput?.files?.[0];

  if (error) error.innerText = "";

  if (!file) {
    error.innerText = "Please select a PDF file.";
    return;
  }

  btn.disabled = true;
  btn.innerText = "Analyzing...";
  loading.style.display = "block";
  spinner.style.display = "block";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    localStorage.setItem("ats_result", JSON.stringify(data));
    window.location.href = "result.html";

  } catch (e) {
    error.innerText = "Backend not reachable.";
    btn.disabled = false;
    btn.innerText = "Analyze";
    loading.style.display = "none";
    spinner.style.display = "none";
  }
}

/* ---------- RESULT PAGE ---------- */
document.addEventListener("DOMContentLoaded", () => {
  if (!window.location.pathname.includes("result.html")) return;

  const content = document.getElementById("result-content");
  const data = JSON.parse(localStorage.getItem("ats_result"));

  if (!data) {
    content.innerHTML = "<p>No ATS data found.</p>";
    return;
  }

  let html = "";

  html += `<h2>ATS SCORE : ${data.score}</h2>`;
  html += `<p><strong>STATUS :</strong> ${data.status}</p>`;

  html += `<hr><h3>---------------- CATEGORY SCORES ----------------</h3>`;
  for (const cat in data.category_scores) {
    html += `<p>${cat}: ${data.category_scores[cat]} / ${data.category_max_scores[cat]}</p>`;
  }

  html += `<hr><h3>---------------- ISSUES ----------------</h3>`;
  data.issues.forEach((i, idx) => {
    html += `
      <p>
        <strong>${idx + 1}. [${i.priority} Priority] (${i.category})</strong><br>
        Issue  : ${i.message}<br>
        Reason : ${i.reason}<br>
        Fix    : ${i.fix}
      </p>`;
  });

  html += `<hr><h3>----------- ACTIONABLE RECOMMENDATIONS -----------</h3>`;

  const grouped = {};
  data.issues.forEach(i => {
    grouped[i.priority] = grouped[i.priority] || [];
    grouped[i.priority].push(i);
  });

  for (const level in grouped) {
    html += `<h4>${level} Priority:</h4>`;
    grouped[level].forEach(i => {
      html += `<p>- (${i.category}) ${i.message}<br>Fix: ${i.fix}</p>`;
    });
  }

  html += `<a href="index.html" class="btn secondary">Analyze Another Resume</a>`;
  content.innerHTML = html;

  // AUTO-SCROLL SAFE
  setTimeout(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, 50);
});
