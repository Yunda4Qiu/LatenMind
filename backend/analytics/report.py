import csv
from pathlib import Path


_BACKEND_DIR = Path(__file__).resolve().parent.parent
LOG_PATH = _BACKEND_DIR / "behavior_log.csv"


def load_session(game_id: str):
    if not LOG_PATH.is_file():
        return []

    rows = []
    with LOG_PATH.open(newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["game_id"] == game_id:
                rows.append(row)
    return rows


def summarize_session(rows):
    if not rows:
        return {}

    rounds = len(rows)
    avg_reward = sum(float(r["reward"]) for r in rows) / rounds
    avg_stability = sum(float(r["stability"]) for r in rows) / rounds

    final = rows[-1]

    return {
        "rounds_played": rounds,
        "average_reward": round(avg_reward, 2),
        "average_stability": round(avg_stability, 2),
        "final_score": round(float(final["score"]), 2),
        "final_profile": {
            "risk_aversion": round(float(final["risk_aversion"]), 2),
            "exploration": round(float(final["exploration"]), 2),
            "consistency": round(float(final["consistency"]), 2),
        }
    }


def interpret_profile(profile):
    text = []

    if profile["exploration"] > 0.6:
        text.append("You tend to explore aggressively under uncertainty.")
    else:
        text.append("You prefer exploiting familiar patterns.")

    if profile["risk_aversion"] > 0.6:
        text.append("You are sensitive to negative feedback.")
    else:
        text.append("You tolerate instability relatively well.")

    if profile["consistency"] > 0.6:
        text.append("Your behavior was internally consistent.")
    else:
        text.append("Your strategy shifted frequently.")

    return " ".join(text)
