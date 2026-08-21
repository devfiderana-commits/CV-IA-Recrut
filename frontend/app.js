const API_ROOT = window.location.origin;

const statusMap = {
  true: { label: "Connecté", style: "success" },
  false: { label: "Déconnecté", style: "danger" },
};

const elements = {
  healthStatus: document.getElementById("healthStatus"),
  dbStatus: document.getElementById("dbStatus"),
  testStatus: document.getElementById("testStatus"),
  apiHealthText: document.getElementById("apiHealthText"),
  mongoText: document.getElementById("mongoText"),
  dbTestText: document.getElementById("dbTestText"),
  refreshBtn: document.getElementById("refreshBtn"),
  dbTestBtn: document.getElementById("dbTestBtn"),
};

async function fetchJson(path) {
  const res = await fetch(`${API_ROOT}${path}`);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`${res.status} ${res.statusText}: ${text}`);
  }
  return res.json();
}

function setElementText(element, value) {
  if (element) element.textContent = value;
}

function getStatusBadge(isOk) {
  const status = statusMap[String(isOk)];
  return `${status.label}`;
}

async function refreshStatus() {
  try {
    const health = await fetchJson("/api/health");
    setElementText(elements.healthStatus, "OK");
    setElementText(elements.apiHealthText, `Projet: ${health.project}`);
  } catch (error) {
    setElementText(elements.healthStatus, "Échec");
    setElementText(elements.apiHealthText, error.message);
  }

  try {
    const dbStatus = await fetchJson("/api/db-status");
    const connected = dbStatus.db_connected === true;
    setElementText(elements.dbStatus, connected ? "OK" : "Déconnecté");
    setElementText(elements.mongoText, connected ? "MongoDB actif" : "MongoDB non connecté");
  } catch (error) {
    setElementText(elements.dbStatus, "Échec");
    setElementText(elements.mongoText, error.message);
  }
}

async function runDbTest() {
  setElementText(elements.testStatus, "En cours...");
  setElementText(elements.dbTestText, "En cours...");

  try {
    const result = await fetchJson("/api/test-db");
    if (result.result === "ok") {
      setElementText(elements.testStatus, "Réussi");
      setElementText(elements.dbTestText, `ID temporaire: ${result.document_id}`);
    } else {
      setElementText(elements.testStatus, "Échec");
      setElementText(elements.dbTestText, `Resultat: ${result.result}`);
    }
  } catch (error) {
    setElementText(elements.testStatus, "Échec");
    setElementText(elements.dbTestText, error.message);
  }
}

function bindEvents() {
  if (elements.refreshBtn) elements.refreshBtn.addEventListener("click", refreshStatus);
  if (elements.dbTestBtn) elements.dbTestBtn.addEventListener("click", runDbTest);
}

async function initDashboard() {
  bindEvents();
  await refreshStatus();
}

initDashboard();
