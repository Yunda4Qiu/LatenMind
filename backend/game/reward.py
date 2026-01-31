def compute_reward(state, action: int) -> float:
    if action == state.hidden_rule:
        base = 1.0
    else:
        base = -0.3

    stability_bonus = 0.6 * (1 - state.player.risk_aversion)

    drift_penalty = - state.drift_rate

    return base + stability_bonus + drift_penalty
