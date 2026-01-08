"""
Utility functions - dice rolling, text parsing, etc.
"""

from .dice import (
    d4, d6, d8, d10, d12, d20, d100,
    roll_dice, advantage, disadvantage, skill_check
)

__all__ = [
    "d4", "d6", "d8", "d10", "d12", "d20", "d100",
    "roll_dice", "advantage", "disadvantage", "skill_check"
]
