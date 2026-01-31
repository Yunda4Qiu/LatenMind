import random

FEEDBACK_POOL = {
    "stable": [
        "The system feels coherent.",
        "Patterns remain aligned.",
        "No anomalies detected."
    ],
    "unstable": [
        "A subtle inconsistency emerged.",
        "The system hesitated.",
        "Alignment weakened."
    ],
    "drift": [
        "Something shifted beneath the surface.",
        "Your assumptions may no longer hold.",
        "The system reconfigured quietly."
    ]
}


def generate_feedback(stability: float, drift_rate: float) -> str:
    if drift_rate > 0.7:
        return random.choice(FEEDBACK_POOL["drift"])
    elif stability > 0.6:
        return random.choice(FEEDBACK_POOL["stable"])
    else:
        return random.choice(FEEDBACK_POOL["unstable"])
