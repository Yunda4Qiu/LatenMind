import csv
from datetime import datetime
from pathlib import Path

# Store logs in the backend folder (stable regardless of the process CWD).
_BACKEND_DIR = Path(__file__).resolve().parent.parent
LOG_PATH = _BACKEND_DIR / "behavior_log.csv"

# Back-compat: some code may treat this as a string path.
LOG_FILE = str(LOG_PATH)
FIELDNAMES = [
    "timestamp",
    "game_id",
    "round",
    "action",
    "reward",
    "score",
    "stability",
    "risk_aversion",
    "exploration",
    "consistency",
    "hidden_rule",
    "drift_rate",
]


def log_trial(state, action, reward):
    file_exists = LOG_PATH.is_file()

    with LOG_PATH.open(mode="a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.now().astimezone().isoformat(),
            "game_id": state.game_id,
            "round": state.round,
            "action": action,
            "reward": reward,
            "score": state.score,
            "stability": state.compute_stability(),
            "risk_aversion": state.player.risk_aversion,
            "exploration": state.player.exploration,
            "consistency": state.player.consistency,
            "hidden_rule": state.hidden_rule,
            "drift_rate": state.drift_rate,
        })
