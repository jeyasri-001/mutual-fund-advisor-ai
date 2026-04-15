def calculate_risk_score(scores, weights):
    total_weight = sum(weights)
    weighted_sum = sum(s * w for s, w in zip(scores, weights))
    return weighted_sum / total_weight


def get_risk_category(score):
    if score <= 20:
        return "conservative"
    elif score <= 40:
        return "moderately conservative"
    elif score <= 60:
        return "moderate"
    elif score <= 80:
        return "moderately aggressive"
    else:
        return "aggressive"