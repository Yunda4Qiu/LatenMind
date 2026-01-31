let gameId = null;

// Default to the common dev backend port. You can override via:
//   index.html?api=http://127.0.0.1:8001
const params = new URLSearchParams(window.location.search);
const API_URL = params.get("api") || "http://127.0.0.1:8001";

const STORAGE_KEY = "latentmind.session";

function setConnectionPill(ok) {
  const pill = document.getElementById("connectionPill");
  if (!pill) return;
  pill.textContent = ok ? "API: connected" : "API: unreachable";
  pill.className = ok ? "pill pill-ok" : "pill pill-bad";
}

function setReportLinks() {
  const reportUrl = `report.html?game_id=${encodeURIComponent(gameId)}&api=${encodeURIComponent(API_URL)}`;

  const link = document.getElementById("reportLink");
  if (link) link.href = reportUrl;

  const linkTop = document.getElementById("reportLinkTop");
  if (linkTop) {
    linkTop.href = reportUrl;
    linkTop.style.display = gameId ? "inline-flex" : "none";
  }
}

function persistSession(lastState) {
  try {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        gameId,
        apiUrl: API_URL,
        lastState,
        savedAt: Date.now(),
      })
    );
  } catch {
    // ignore storage errors
  }
}

function restoreSession() {
  const gameIdFromQuery = params.get("game_id");
  if (gameIdFromQuery) {
    return { gameId: gameIdFromQuery };
  }

  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return null;
    const data = JSON.parse(raw);
    if (!data?.gameId) return null;
    if (data.apiUrl && data.apiUrl !== API_URL) return null;
    return data;
  } catch {
    return null;
  }
}

function showSessionUI() {
  document.getElementById("status").style.display = "block";
  document.getElementById("gameIdLine").style.display = "block";
  document.getElementById("gameId").innerText = gameId;
  setReportLinks();
}

function resetGame() {
  gameId = null;
  try {
    localStorage.removeItem(STORAGE_KEY);
  } catch {
    // ignore
  }

  document.getElementById("status").style.display = "none";
  document.getElementById("gameIdLine").style.display = "none";
  document.getElementById("reportLinkTop").style.display = "none";
  document.getElementById("after20Row").style.display = "none";
}

function initPage() {
  const apiLabel = document.getElementById("apiUrlLabel");
  if (apiLabel) apiLabel.textContent = API_URL;

  fetch(`${API_URL}/`, { method: "GET" })
    .then(res => setConnectionPill(res.ok))
    .catch(() => setConnectionPill(false));

  const restored = restoreSession();
  if (restored?.gameId) {
    gameId = restored.gameId;
    showSessionUI();
    if (restored.lastState) {
      updateUI(restored.lastState);
    } else {
      document.getElementById("message").innerText = "Session restored. Choose an action to continue.";
    }
  }
}

function startGame() {
  fetch(`${API_URL}/start`, {
    method: "POST"
  })
    .then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then(data => {
      gameId = data.game_id;
      showSessionUI();
      updateUI(data);
      persistSession(data);
    })
    .catch(err => {
      console.error("startGame failed:", err);
      alert(`Start failed. Is backend running at ${API_URL}?`);
    });
}

function sendAction(action) {
  if (!gameId) return;

  fetch(`${API_URL}/action`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      game_id: gameId,
      action: action
    })
  })
    .then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then(data => updateUI(data))
    .catch(err => {
      console.error("sendAction failed:", err);
      alert("Action failed. If you restarted the backend, the in-memory session may be gone. Click 'New experiment' to start over.");
    });
}

function updateUI(data) {
  document.getElementById("round").innerText = data.round;
  document.getElementById("score").innerText = data.score;
  document.getElementById("stability").innerText = data.stability_index;
  document.getElementById("message").innerText = data.message;

  persistSession(data);
  setReportLinks();

  if (data.round >= 20) {
    const after20Row = document.getElementById("after20Row");
    if (after20Row) after20Row.style.display = "flex";
  }

}

// Initialize UI state on load
initPage();
