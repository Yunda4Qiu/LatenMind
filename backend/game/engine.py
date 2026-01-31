import uuid
import random

# Prefer package-qualified imports (avoids collisions with third-party packages
# named like "game"/"db"). Fall back to local imports for the workflow:
# `cd backend && uvicorn app:app --reload`.
try:
    from backend.game.player_model import PlayerProfile
    from backend.game.reward import compute_reward
    from backend.game.feedback import generate_feedback
    from backend.db.logger import log_trial
except ImportError:  # pragma: no cover
    from game.player_model import PlayerProfile
    from game.reward import compute_reward
    from game.feedback import generate_feedback
    from db.logger import log_trial   # 👈 新增


class GameState:
    def __init__(self):
        self.game_id = str(uuid.uuid4())
        self.round = 0
        self.score = 0.0

        self.hidden_rule = random.randint(0, 2)
        self.drift_rate = random.uniform(0.1, 0.3)

        self.player = PlayerProfile()

    def compute_stability(self) -> float:
        return max(0.0, 1.0 - (self.player.risk_aversion + self.drift_rate) / 2)

    def public_view(self):
        stability = self.compute_stability()
        message = generate_feedback(stability, self.drift_rate)

        return {
            "game_id": self.game_id,
            "round": self.round,
            "symbols": [random.randint(0, 9) for _ in range(3)],
            "score": round(self.score, 2),
            "stability_index": round(stability, 2),
            "message": message
        }


def init_game():
    state = GameState()
    return state.game_id, state


def play_round(state: GameState, action: int) -> GameState:
    reward = compute_reward(state, action)

    # 👇 先更新玩家
    state.player.update(action, reward)

    # 👇 再更新系统
    state.score += reward
    state.round += 1

    # 👇 行为日志（关键）
    log_trial(state, action, reward)

    # 👇 自适应漂移
    if state.player.exploration > 0.6 and random.random() < state.drift_rate:
        state.hidden_rule = random.randint(0, 2)
        state.drift_rate = min(1.0, state.drift_rate + 0.1)
    else:
        state.drift_rate = max(0.05, state.drift_rate - 0.02)

    return state
