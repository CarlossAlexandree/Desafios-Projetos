/**
 * app.js — Orquestra o formulário, a chamada à API do backend e a
 * renderização dos resultados (resumo, grafo, ameaças por categoria STRIDE
 * e sugestões).
 */

// Ajuste este valor para a URL do backend em produção (ex: Render, Railway).
const API_BASE_URL = window.STRIDE_API_BASE_URL || "http://localhost:8000";

const STRIDE_ORDER = [
  "Spoofing",
  "Tampering",
  "Repudiation",
  "Information Disclosure",
  "Denial of Service",
  "Elevation of Privilege",
];

const form = document.getElementById("analysis-form");
const submitBtn = document.getElementById("submit-btn");
const printBtn = document.getElementById("print-btn");
const formError = document.getElementById("form-error");
const emptyState = document.getElementById("empty-state");
const resultsEl = document.getElementById("results");
const stampProvider = document.getElementById("stamp-provider");
const stampStatus = document.getElementById("stamp-status");

// --- Preview de imagem (dropzone) ---
const imagemInput = document.getElementById("imagem");
const dropzone = document.getElementById("dropzone");
const dropzoneHint = document.getElementById("dropzone-hint");
const preview = document.getElementById("preview");

imagemInput.addEventListener("change", () => {
  const file = imagemInput.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = (e) => {
    preview.src = e.target.result;
    preview.hidden = false;
    dropzoneHint.hidden = true;
  };
  reader.readAsDataURL(file);
});

["dragover", "dragleave", "drop"].forEach((eventName) => {
  dropzone.addEventListener(eventName, (e) => {
    e.preventDefault();
    dropzone.classList.toggle("is-dragover", eventName === "dragover");
    if (eventName === "drop" && e.dataTransfer.files[0]) {
      imagemInput.files = e.dataTransfer.files;
      imagemInput.dispatchEvent(new Event("change"));
    }
  });
});

// --- Envio do formulário ---
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  hideError();
  setLoading(true);

  try {
    const formData = new FormData(form);

    const response = await fetch(`${API_BASE_URL}/api/v1/analisar-arquitetura`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || `Erro ${response.status} ao analisar a arquitetura.`);
    }

    renderResults(data);
    stampStatus.textContent = "Concluída";
    stampProvider.textContent = data.provider_used || "—";
    printBtn.disabled = false;
  } catch (err) {
    console.error(err);
    showError(
      err.message ||
        "Não foi possível conectar à API. Verifique se o backend está rodando."
    );
    stampStatus.textContent = "Falhou";
  } finally {
    setLoading(false);
  }
});

printBtn.addEventListener("click", () => window.print());

function setLoading(isLoading) {
  submitBtn.disabled = isLoading;
  submitBtn.querySelector(".btn__spinner").hidden = !isLoading;
  submitBtn.querySelector(".btn__label").textContent = isLoading
    ? "Analisando..."
    : "Analisar arquitetura";
  if (isLoading) stampStatus.textContent = "Processando...";
}

function showError(message) {
  formError.textContent = message;
  formError.hidden = false;
}

function hideError() {
  formError.hidden = true;
}

function severityClass(severity) {
  const normalized = (severity || "").toLowerCase();
  if (normalized.includes("crít")) return "critica";
  if (normalized.includes("alt")) return "alta";
  if (normalized.includes("méd") || normalized.includes("med")) return "media";
  return "baixa";
}

function renderResults(data) {
  emptyState.hidden = true;
  resultsEl.hidden = false;

  document.getElementById("summary-text").textContent =
    data.summary || "Nenhum resumo foi retornado.";

  // Agrupa ameaças por categoria STRIDE, preservando a ordem canônica
  const grouped = new Map(STRIDE_ORDER.map((key) => [key, []]));
  (data.threat_model || []).forEach((threat) => {
    if (!grouped.has(threat.threat_type)) grouped.set(threat.threat_type, []);
    grouped.get(threat.threat_type).push(threat);
  });

  const grid = document.getElementById("threats-grid");
  grid.innerHTML = "";

  grouped.forEach((threats, category) => {
    if (threats.length === 0) return;

    const color = window.STRIDEGraph.STRIDE_COLORS[category] || "#8B9AAB";
    const card = document.createElement("div");
    card.className = "threat-category";
    card.innerHTML = `
      <div class="threat-category__header" style="background:${color}">
        ${category} (${threats.length})
      </div>
      <div class="threat-category__body">
        ${threats
          .map(
            (t) => `
          <div class="threat-item">
            <p class="threat-item__scenario">${escapeHtml(t.scenario)}</p>
            <div class="threat-item__meta">
              <span>Impacto: ${escapeHtml(t.potential_impact || "—")}</span>
              ${
                t.affected_component
                  ? `<span>Componente: ${escapeHtml(t.affected_component)}</span>`
                  : ""
              }
              <span class="severity-badge severity-badge--${severityClass(t.severity)}">
                ${escapeHtml(t.severity || "N/D")}
              </span>
            </div>
          </div>`
          )
          .join("")}
      </div>
    `;
    grid.appendChild(card);
  });

  const suggestionsList = document.getElementById("suggestions-list");
  suggestionsList.innerHTML = (data.improvement_suggestions || [])
    .map((s) => `<li>${escapeHtml(s)}</li>`)
    .join("");

  window.STRIDEGraph.renderGraph(data.threat_model || []);
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
