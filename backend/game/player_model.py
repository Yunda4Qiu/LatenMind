class PlayerProfile:
    def __init__(self):
        self.risk_aversion = 0.5      # 高 → 更厌恶损失
        self.exploration = 0.5        # 高 → 更喜欢试新
        self.consistency = 0.5        # 高 → 行为稳定
        self.recent_actions = []

    def update(self, action: int, reward: float):
        self.recent_actions.append(action)
        if len(self.recent_actions) > 5:
            self.recent_actions.pop(0)

        # 更新 risk aversion
        if reward < 0:
            self.risk_aversion = min(1.0, self.risk_aversion + 0.05)
        else:
            self.risk_aversion = max(0.0, self.risk_aversion - 0.03)

        # 更新 exploration（是否重复动作）
        if len(set(self.recent_actions)) > 2:
            self.exploration = min(1.0, self.exploration + 0.04)
        else:
            self.exploration = max(0.0, self.exploration - 0.02)

        # consistency：动作是否稳定
        self.consistency = 1 - len(set(self.recent_actions)) / max(1, len(self.recent_actions))
