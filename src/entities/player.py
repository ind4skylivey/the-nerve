"""
Player Entity - Character stats, inventory, skills
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any


@dataclass
class PlayerStats:
    """
    Player base stats (D&D style, 2-18 scale)

    Attributes:
        strength: Melee damage, intimidation (2-18)
        dexterity: Ranged attacks, dodge, initiative (2-18)
        intelligence: Hacking, knowledge checks (2-18)
        charisma: Persuasion, leadership (2-18)
        luck: Critical hits, loot quality (2-18)
    """
    strength: int = 10
    dexterity: int = 10
    intelligence: int = 10
    charisma: int = 10
    luck: int = 10

    def get_modifier(self, stat_name: str) -> int:
        """
        Get D&D-style modifier for a stat

        Args:
            stat_name: Name of stat (e.g., 'strength')

        Returns:
            Modifier value (-4 to +4)

        Example:
            >>> stats = PlayerStats(strength=16)
            >>> stats.get_modifier('strength')
            3
        """
        stat_value = getattr(self, stat_name, 10)
        return (stat_value - 10) // 2

    def to_dict(self) -> dict:
        """Serialize to dictionary"""
        return {
            "strength": self.strength,
            "dexterity": self.dexterity,
            "intelligence": self.intelligence,
            "charisma": self.charisma,
            "luck": self.luck
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'PlayerStats':
        """Deserialize from dictionary"""
        return cls(
            strength=data.get("strength", 10),
            dexterity=data.get("dexterity", 10),
            intelligence=data.get("intelligence", 10),
            charisma=data.get("charisma", 10),
            luck=data.get("luck", 10)
        )


@dataclass
class Player:
    """
    Player character entity

    Attributes:
        name: Character name
        level: Current level (1-20)
        xp: Experience points
        hp_current: Current hit points
        hp_max: Maximum hit points
        stamina_current: Current stamina
        stamina_max: Maximum stamina
        stats: PlayerStats object
        skills: Skill levels (0-100)
        inventory: List of item IDs
        equipped: Equipped items by slot
        credits: Current money
        perks: List of perk IDs
        traits: List of trait IDs
        faction_standings: Faction reputation (-100 to 100)
        npc_relationships: NPC relationship values
    """

    # Basic info
    name: str = "Unknown"
    level: int = 1
    xp: int = 0

    # Vitals
    hp_current: int = 50
    hp_max: int = 50
    stamina_current: int = 100
    stamina_max: int = 100

    # Stats
    stats: PlayerStats = field(default_factory=PlayerStats)

    # Skills (0-100 scale)
    skills: Dict[str, int] = field(default_factory=lambda: {
        "melee": 0,
        "ranged": 0,
        "hacking": 0,
        "persuasion": 0,
        "intimidation": 0,
        "stealth": 0,
        "perception": 0,
        "medicine": 0
    })

    # Inventory
    inventory: List[str] = field(default_factory=list)
    equipped: Dict[str, str] = field(default_factory=dict)
    credits: int = 100

    # Progression
    perks: List[str] = field(default_factory=list)
    traits: List[str] = field(default_factory=list)

    # Relationships
    faction_standings: Dict[str, int] = field(default_factory=dict)
    npc_relationships: Dict[str, int] = field(default_factory=dict)

    def skill_check(self, skill: str, difficulty: int) -> tuple[bool, int]:
        """
        Perform a skill check

        Args:
            skill: Skill name (e.g., 'hacking')
            difficulty: DC target (10-30)

        Returns:
            (success: bool, total: int)

        Example:
            >>> player = Player(skills={"hacking": 50})
            >>> success, total = player.skill_check("hacking", 15)
        """
        from src.utils.dice import d20

        skill_value = self.skills.get(skill, 0)
        skill_bonus = skill_value // 10  # Every 10 skill = +1 bonus

        roll = d20()
        total = roll + skill_bonus

        success = total >= difficulty
        return (success, total)

    def stat_check(self, stat: str, difficulty: int) -> tuple[bool, int]:
        """
        Perform a stat check (D&D style)

        Args:
            stat: Stat name (e.g., 'charisma')
            difficulty: DC target

        Returns:
            (success: bool, total: int)
        """
        from src.utils.dice import d20

        modifier = self.stats.get_modifier(stat)
        roll = d20()
        total = roll + modifier

        success = total >= difficulty
        return (success, total)

    def take_damage(self, amount: int) -> int:
        """
        Take damage and update HP

        Args:
            amount: Damage amount

        Returns:
            Actual damage taken (can't go below 0 HP)
        """
        old_hp = self.hp_current
        self.hp_current = max(0, self.hp_current - amount)
        actual_damage = old_hp - self.hp_current

        return actual_damage

    def heal(self, amount: int) -> int:
        """
        Heal HP

        Args:
            amount: Healing amount

        Returns:
            Actual HP healed (can't exceed hp_max)
        """
        old_hp = self.hp_current
        self.hp_current = min(self.hp_max, self.hp_current + amount)
        actual_healing = self.hp_current - old_hp

        return actual_healing

    def add_xp(self, amount: int):
        """
        Add experience points and check for level up

        Args:
            amount: XP to add
        """
        self.xp += amount

        # Check for level up (simple formula: level * 100 XP)
        xp_needed = self.level * 100
        if self.xp >= xp_needed:
            self.level_up()

    def level_up(self):
        """
        Level up the player

        Increases:
            - Level by 1
            - HP max by 5
            - Stamina max by 3
        """
        self.level += 1
        self.hp_max += 5
        self.hp_current = self.hp_max  # Full heal on level up
        self.stamina_max += 3
        self.stamina_current = self.stamina_max

        print(f"🎉 LEVEL UP! You are now level {self.level}!")

    def add_item(self, item_id: str):
        """Add item to inventory"""
        self.inventory.append(item_id)

    def remove_item(self, item_id: str) -> bool:
        """
        Remove item from inventory

        Returns:
            True if item was removed, False if not found
        """
        if item_id in self.inventory:
            self.inventory.remove(item_id)
            return True
        return False

    def has_item(self, item_id: str) -> bool:
        """Check if player has an item"""
        return item_id in self.inventory

    def modify_faction_standing(self, faction: str, amount: int):
        """
        Modify faction reputation

        Args:
            faction: Faction ID
            amount: Change amount (positive or negative)
        """
        current = self.faction_standings.get(faction, 0)
        new_value = max(-100, min(100, current + amount))
        self.faction_standings[faction] = new_value

    def modify_npc_relationship(self, npc_id: str, amount: int):
        """
        Modify NPC relationship

        Args:
            npc_id: NPC ID
            amount: Change amount
        """
        current = self.npc_relationships.get(npc_id, 0)
        new_value = max(-100, min(100, current + amount))
        self.npc_relationships[npc_id] = new_value

    def is_alive(self) -> bool:
        """Check if player is alive"""
        return self.hp_current > 0

    def to_dict(self) -> dict:
        """Serialize player to dictionary (for saving)"""
        return {
            "name": self.name,
            "level": self.level,
            "xp": self.xp,
            "hp_current": self.hp_current,
            "hp_max": self.hp_max,
            "stamina_current": self.stamina_current,
            "stamina_max": self.stamina_max,
            "stats": self.stats.to_dict(),
            "skills": self.skills,
            "inventory": self.inventory,
            "equipped": self.equipped,
            "credits": self.credits,
            "perks": self.perks,
            "traits": self.traits,
            "faction_standings": self.faction_standings,
            "npc_relationships": self.npc_relationships
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Player':
        """Deserialize player from dictionary"""
        stats = PlayerStats.from_dict(data.get("stats", {}))

        return cls(
            name=data.get("name", "Unknown"),
            level=data.get("level", 1),
            xp=data.get("xp", 0),
            hp_current=data.get("hp_current", 50),
            hp_max=data.get("hp_max", 50),
            stamina_current=data.get("stamina_current", 100),
            stamina_max=data.get("stamina_max", 100),
            stats=stats,
            skills=data.get("skills", {}),
            inventory=data.get("inventory", []),
            equipped=data.get("equipped", {}),
            credits=data.get("credits", 100),
            perks=data.get("perks", []),
            traits=data.get("traits", []),
            faction_standings=data.get("faction_standings", {}),
            npc_relationships=data.get("npc_relationships", {})
        )
