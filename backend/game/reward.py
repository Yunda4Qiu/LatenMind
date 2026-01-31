def compute_reward(state, action: int) -> float:
    """
    Reward is intentionally noisy and indirect
    """

    # 基础奖励：命中隐藏规则
    if action == state.hidden_rule:
        base = 1.0
    else:
        base = -0.3

    # 稳定度奖励（鼓励低风险玩家）
    stability_bonus = 0.6 * (1 - state.player.risk_aversion)

    # 漂移惩罚
    drift_penalty = - state.drift_rate

    return base + stability_bonus + drift_penalty
