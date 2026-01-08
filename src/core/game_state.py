"""
Game State Management - Central source of truth
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum


class GamePhase(Enum):
    """Current phase of the game"""
    MAIN_MENU = "main_menu"
    CHARACTER_CREATION = "character_creation"
    EXPLORATION = "exploration"
    DIALOGUE = "dialogue"
    COMBAT = "combat"
    INVENTORY = "inventory"
    PAUSED = "paused"


@dataclass
class GameState:
    """
    Central game state - single source of truth
    All game systems read from and write to this state
    """

    # Meta
    phase: GamePhase = GamePhase.MAIN_MENU
    genre: str = "cyberpunk"  # cyberpunk/fantasy/post_apo

    # Player
    player: Optional[Any] = None  # Player entity

    # World
    current_location_id: str = ""
    world_flags: Dict[str, Any] = field(default_factory=dict)

    # Active systems
    active_dialogue: Optional[Any] = None  # DialogueTree instance
    active_combat: Optional[Any] = None  # CombatEncounter instance

    # History tracking
    choice_history: list[str] = field(default_factory=list)
    visited_locations: set[str] = field(default_factory=set)
    turn_count: int = 0

    # Save metadata
    save_version: str = "1.0.0"
    seed: int = 0  # For reproducible RNG
    playtime_seconds: int = 0

    def set_flag(self, flag_name: str, value: Any = True):
        """Set a world flag"""
        self.world_flags[flag_name] = value

    def get_flag(self, flag_name: str, default: Any = False) -> Any:
        """Get a world flag value"""
        return self.world_flags.get(flag_name, default)

    def has_flag(self, flag_name: str) -> bool:
        """Check if flag exists and is truthy"""
        return bool(self.world_flags.get(flag_name, False))

    def record_choice(self, choice_id: str):
        """Record a player choice for consequence tracking"""
        self.choice_history.append(choice_id)

    def has_made_choice(self, choice_id: str) -> bool:
        """Check if player made a specific choice"""
        return choice_id in self.choice_history

    def to_dict(self) -> dict:
        """Serialize to dictionary for saving"""
        return {
            "phase": self.phase.value,
            "genre": self.genre,
            "current_location_id": self.current_location_id,
            "world_flags": self.world_flags,
            "choice_history": self.choice_history,
            "visited_locations": list(self.visited_locations),
            "turn_count": self.turn_count,
            "save_version": self.save_version,
            "seed": self.seed,
            "playtime_seconds": self.playtime_seconds,
            # Player serialized separately
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'GameState':
        """Deserialize from dictionary"""
        state = cls(
            phase=GamePhase(data["phase"]),
            genre=data["genre"],
            current_location_id=data["current_location_id"],
            world_flags=data["world_flags"],
            choice_history=data["choice_history"],
            turn_count=data["turn_count"],
            save_version=data["save_version"],
            seed=data["seed"],
            playtime_seconds=data["playtime_seconds"],
        )
        state.visited_locations = set(data["visited_locations"])
        return state
