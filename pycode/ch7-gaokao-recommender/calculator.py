from config import *

def adjust_rank_for_2025(user_rank):
    """将2025年位次调整为等效2024年位次"""
    return int(user_rank * RANK_ADJUSTMENT_RATIO)
def calculate_recommendation_intervals(adjusted_rank):
    """
    计算三个推荐区间的位次边界
    Returns: dict with 'challenge', 'stable', 'safe' keys
    """
    return {
        'challenge': (int(adjusted_rank * CHALLENGE_LOWER), int(adjusted_rank * CHALLENGE_UPPER)),
        'stable': (int(adjusted_rank * STABLE_LOWER), int(adjusted_rank * STABLE_UPPER)),
        'safe': (int(adjusted_rank * SAFE_LOWER), int(adjusted_rank * SAFE_UPPER))
    }
