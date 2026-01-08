"""
Dice Rolling System - D&D style mechanics
"""

import random
from typing import Tuple


def d4() -> int:
    """Roll a 4-sided die"""
    return random.randint(1, 4)


def d6() -> int:
    """Roll a 6-sided die"""
    return random.randint(1, 6)


def d8() -> int:
    """Roll an 8-sided die"""
    return random.randint(1, 8)


def d10() -> int:
    """Roll a 10-sided die"""
    return random.randint(1, 10)


def d12() -> int:
    """Roll a 12-sided die"""
    return random.randint(1, 12)


def d20() -> int:
    """
    Roll a 20-sided die (D&D standard)

    Returns:
        Random integer 1-20
    """
    return random.randint(1, 20)


def d100() -> int:
    """Roll percentile dice (1-100)"""
    return random.randint(1, 100)


def roll_dice(dice_notation: str) -> int:
    """
    Roll dice from notation string (e.g., '2d6+3', '1d20', '3d8-2')

    Supports:
        - Standard notation: XdY (X dice with Y sides)
        - Modifiers: +N or -N
        - Examples:
            '1d20' -> 1-20
            '2d6+5' -> 7-17
            '3d8-2' -> 1-22

    Args:
        dice_notation: Dice string (e.g., "2d6+3")

    Returns:
        Total roll result

    Raises:
        ValueError: If notation is invalid
    """
    dice_notation = dice_notation.strip().lower()

    # Parse modifier
    modifier = 0
    if '+' in dice_notation:
        dice_part, mod_part = dice_notation.split('+')
        modifier = int(mod_part)
    elif '-' in dice_notation and dice_notation.count('-') == 1:
        parts = dice_notation.split('-')
        dice_part = parts[0]
        if parts[1]:  # Make sure there's a number after the dash
            modifier = -int(parts[1])
    else:
        dice_part = dice_notation

    # Parse dice
    if 'd' not in dice_part:
        raise ValueError(f"Invalid dice notation: {dice_notation}")

    count_str, sides_str = dice_part.split('d')
    count = int(count_str) if count_str else 1
    sides = int(sides_str)

    # Roll
    total = sum(random.randint(1, sides) for _ in range(count))
    return total + modifier


def advantage() -> Tuple[int, int, int]:
    """
    Roll with advantage (2d20, take higher)

    Returns:
        (roll1, roll2, result)
    """
    roll1 = d20()
    roll2 = d20()
    return (roll1, roll2, max(roll1, roll2))


def disadvantage() -> Tuple[int, int, int]:
    """
    Roll with disadvantage (2d20, take lower)

    Returns:
        (roll1, roll2, result)
    """
    roll1 = d20()
    roll2 = d20()
    return (roll1, roll2, min(roll1, roll2))


def skill_check(
    skill_value: int,
    difficulty: int,
    use_advantage: bool = False,
    use_disadvantage: bool = False
) -> Tuple[bool, int, int]:
    """
    Perform a skill check against difficulty

    Args:
        skill_value: Bonus to add to d20 roll
        difficulty: Target DC (Difficulty Class)
        use_advantage: Roll 2d20, take higher
        use_disadvantage: Roll 2d20, take lower

    Returns:
        (success: bool, roll_result: int, total: int)

    Example:
        success, roll, total = skill_check(skill_value=5, difficulty=15)
        if success:
            print(f"Success! Rolled {roll}+5={total} vs DC 15")
    """
    if use_advantage:
        _, _, roll = advantage()
    elif use_disadvantage:
        _, _, roll = disadvantage()
    else:
        roll = d20()

    total = roll + skill_value
    success = total >= difficulty

    return (success, roll, total)


def critical_hit_check(attack_roll: int) -> bool:
    """
    Check if attack roll is a critical hit (natural 20)

    Args:
        attack_roll: The raw d20 result

    Returns:
        True if critical hit
    """
    return attack_roll == 20


def critical_fail_check(attack_roll: int) -> bool:
    """
    Check if attack roll is a critical fail (natural 1)

    Args:
        attack_roll: The raw d20 result

    Returns:
        True if critical fail
    """
    return attack_roll == 1


def damage_roll(dice_notation: str, critical: bool = False) -> int:
    """
    Roll damage, doubling dice on critical hits

    Args:
        dice_notation: Damage dice (e.g., "1d8+3")
        critical: Whether this is a critical hit

    Returns:
        Total damage
    """
    if not critical:
        return roll_dice(dice_notation)

    # On critical, roll damage dice twice (but don't double modifier)
    base_notation = dice_notation.split('+')[0].split('-')[0]

    # Roll base damage twice
    damage = roll_dice(base_notation) + roll_dice(base_notation)

    # Add modifier once
    if '+' in dice_notation:
        modifier = int(dice_notation.split('+')[1])
        damage += modifier
    elif '-' in dice_notation:
        modifier = int(dice_notation.split('-')[1])
        damage -= modifier

    return damage
