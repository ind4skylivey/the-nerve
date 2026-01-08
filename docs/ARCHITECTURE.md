# Terminal RPG - Architecture Guide

**Technical Design & Code Structure - Complete Reference**

**Version:** 1.0.0
**Last Updated:** 2026-01-07
**Author:** S1B Group Development Team

---

## 📋 TABLE OF CONTENTS

1. [Architectural Overview](#1-architectural-overview)
2. [Design Principles](#2-design-principles)
3. [Project Structure](#3-project-structure)
4. [Module Responsibilities](#4-module-responsibilities)
5. [Core Architecture Patterns](#5-core-architecture-patterns)
6. [Key System Designs](#6-key-system-designs)
7. [Data Flow Examples](#7-data-flow-examples)
8. [Data Schemas](#8-data-schemas)
9. [Game Loop Design](#9-game-loop-design)
10. [Testing Strategy](#10-testing-strategy)
11. [Performance Optimization](#11-performance-optimization)
12. [Scalability & Extensibility](#12-scalability--extensibility)
13. [Development Workflow](#13-development-workflow)
14. [Debugging Tools](#14-debugging-tools)
15. [Dependencies & Tech Stack](#15-dependencies--tech-stack)
16. [Code Style Guide](#16-code-style-guide)
17. [Future Roadmap](#17-future-roadmap)
18. [Glossary](#18-glossary)

---

## 1. ARCHITECTURAL OVERVIEW

### Design Philosophy

┌─────────────────────────────────────────┐ │ PRINCIPLES │ ├─────────────────────────────────────────┤ │ ✅ Separation of Concerns │ │ ✅ Event-Driven Communication │ │ ✅ Data-Driven Content │ │ ✅ Modular & Testable │ │ ✅ Genre-Agnostic Core │ └─────────────────────────────────────────┘

### Tech Stack

| Layer            | Technology        | Purpose                                |
| ---------------- | ----------------- | -------------------------------------- |
| **Language**     | Python 3.11+      | Modern syntax, type hints, dataclasses |
| **UI Framework** | Rich 13.7+        | Terminal rendering, colors, layouts    |
| **Data Format**  | JSON              | Human-readable, Git-friendly           |
| **Testing**      | pytest            | Unit & integration tests               |
| **Linting**      | ruff, black, mypy | Code quality, type safety              |
| **Save Format**  | JSON (compressed) | Portable, debuggable saves             |

---

## 2. DESIGN PRINCIPLES

### 2.1 Separation of Concerns

┌──────────────────┐ │ UI Layer │ ← Rendering only, no logic │ (src/ui/) │ └────────┬─────────┘ │ Events (user input) ▼ ┌──────────────────┐ │ Game State │ ← Single source of truth │ (src/core/) │ └────────┬─────────┘ │ Commands ▼ ┌──────────────────┐ │ Game Systems │ ← Combat, Dialogue, Quests │ (src/systems/) │ └────────┬─────────┘ │ Modifies ▼ ┌──────────────────┐ │ Entities │ ← Player, NPCs, Items │ (src/entities/) │ └──────────────────┘

**Benefits:**

- UI can swap (terminal → web) without touching game logic
- Systems testable in isolation
- Clear data flow

---

### 2.2 Event-Driven Architecture

```python
# Example: Combat system publishes damage event
from src.core.event_dispatcher import game_events, Event, EventType

# System A: Combat publishes
def deal_damage(target, amount):
    target.hp -= amount
    game_events.publish(Event(
        EventType.DAMAGE_DEALT,
        {"target": target.name, "amount": amount}
    ))

# System B: UI subscribes
def on_damage_dealt(event: Event):
    print(f"💥 {event.data['target']} took {event.data['amount']} damage!")

game_events.subscribe(EventType.DAMAGE_DEALT, on_damage_dealt)

Why Event Bus:

    ✅ Loose coupling between systems
    ✅ Easy to add new listeners
    ✅ Clean system boundaries
    ✅ Debugging via event history

2.3 Data-Driven Design
python

# ❌ BAD: Hardcoded content
tavern = Location(
    name="The Golden Drake",
    description="A dimly lit tavern...",
    exits={"north": "marketplace"}
)

# ✅ GOOD: Data-driven
tavern_data = loader.load_location("cyberpunk", "golden_drake_tavern")
tavern = Location.from_dict(tavern_data)

Benefits:

    Content creators don't need to code
    Hot-reloadable during development
    Git-friendly JSON diffs
    Easy to A/B test content

3. PROJECT STRUCTURE

terminal-rpg/
│
├── src/                           # Source code
│   ├── core/                      # Engine - genre-agnostic
│   │   ├── game_state.py          # Central state manager
│   │   ├── event_dispatcher.py    # Event bus
│   │   ├── save_manager.py        # Save/load JSON
│   │   └── random_engine.py       # Seeded RNG (future)
│   │
│   ├── entities/                  # Game objects
│   │   ├── player.py              # Player character
│   │   ├── enemy.py               # Combat enemies
│   │   ├── npc.py                 # Non-combat NPCs (future)
│   │   ├── item.py                # Items/equipment (future)
│   │   └── faction.py             # Faction data (future)
│   │
│   ├── systems/                   # Game mechanics
│   │   ├── dialogue.py            # Conversation trees
│   │   ├── combat.py              # Turn-based combat
│   │   ├── inventory.py           # Item management (future)
│   │   ├── skills.py              # Skill checks (future)
│   │   ├── progression.py         # XP/leveling (future)
│   │   └── quest.py               # Quest tracking (future)
│   │
│   ├── world/                     # World management
│   │   ├── location.py            # Location class
│   │   ├── world_manager.py       # Transitions (future)
│   │   └── encounter.py           # Random encounters (future)
│   │
│   ├── ui/                        # Terminal rendering
│   │   ├── components/            # Reusable widgets
│   │   │   ├── stat_panel.py
│   │   │   ├── dialogue_box.py
│   │   │   ├── combat_log.py
│   │   │   └── inventory_menu.py
│   │   ├── screens/               # Full-screen views
│   │   │   ├── main_menu.py
│   │   │   ├── character_creation.py
│   │   │   ├── game_view.py
│   │   │   └── pause_menu.py
│   │   └── themes/                # Visual styling
│   │       ├── cyberpunk.py
│   │       ├── fantasy.py
│   │       └── post_apo.py
│   │
│   ├── data/                      # Data loading
│   │   ├── loader.py              # JSON parser + cache
│   │   └── validator.py           # Schema validation (future)
│   │
│   ├── utils/                     # Utilities
│   │   ├── dice.py                # RNG, dice rolls
│   │   ├── text.py                # Text parsing (future)
│   │   └── logger.py              # Debug logging (future)
│   │
│   └── main.py                    # Entry point
│
├── data/                          # Game content (JSON)
│   ├── genres/
│   │   ├── cyberpunk/             # Current implementation
│   │   │   ├── locations/
│   │   │   ├── npcs/
│   │   │   ├── dialogues/
│   │   │   ├── enemies/
│   │   │   ├── items/
│   │   │   └── factions.json
│   │   ├── fantasy/               # Future DLC
│   │   └── post_apo/              # Future DLC
│   │
│   ├── shared/                    # Genre-agnostic data
│   │   ├── base_stats.json
│   │   └── combat_rules.json
│   │
│   └── templates/                 # Reusable templates
│       ├── dialogue_template.json
│       └── quest_template.json
│
├── saves/                         # Player save files
│   ├── autosave.json
│   ├── slot_1.json
│   └── ...
│
├── tests/                         # Unit/integration tests
│   ├── test_core/
│   ├── test_systems/
│   ├── test_entities/
│   └── test_integration/
│
├── docs/                          # Documentation
│   ├── GDD.md
│   ├── ARCHITECTURE.md            # This file
│   └── VERTICAL_SLICE.md
│
├── tools/                         # Dev tools (future)
│   └── dialogue_visualizer.py
│
├── requirements.txt
├── pyproject.toml
├── README.md
├── .gitignore
└── setup.sh

4. MODULE RESPONSIBILITIES
4.1 src/core/ - Game Engine

Purpose: Genre-agnostic core systems
File	Responsibility	Key Classes
game_state.py	Central state management, flags	GameState, GamePhase
event_dispatcher.py	Publish/subscribe event bus	EventDispatcher, Event
save_manager.py	JSON serialization, save slots	SaveManager

Design Rule: ⚠️ Core systems NEVER import from src/systems/ or src/ui/
4.2 src/entities/ - Game Objects

Purpose: Data classes representing game entities
File	Represents	Key Methods
player.py	Player character	skill_check(), take_damage(), add_xp()
enemy.py	Combat enemies	choose_action(), generate_loot()
npc.py	Non-combat NPCs	(future)
item.py	Items/equipment	(future)

Characteristics:

    Dataclasses for clean structure
    Serializable via to_dict() / from_dict()
    No game logic - just data + utility methods

4.3 src/systems/ - Game Mechanics

Purpose: Stateless processors of game logic
File	System	Inputs	Outputs
dialogue.py	Conversation trees	Player, DialogueTree	Choice consequences
combat.py	Turn-based combat	Player, Enemies	Victory/Defeat
inventory.py	Item management	(future)
quest.py	Quest tracking	(future)

Design Pattern:
python

# Systems are stateless - don't store game state
class CombatSystem:
    def __init__(self, game_state: GameState):
        self.state = game_state  # Reference, not ownership

    def start_encounter(self, enemies: List[Enemy]):
        # Process combat using self.state.player
        pass

4.4 src/world/ - World Management

Purpose: Location and spatial systems
File	Purpose
location.py	Location data structure + loader
world_manager.py	Handle transitions between locations
encounter.py	Random/scripted encounter triggers
4.5 src/ui/ - Terminal Rendering

Purpose: Visual presentation (100% separated from logic)

Structure:

ui/
├── components/       ← Reusable widgets
│   ├── stat_panel.py       → render_stats(player)
│   ├── dialogue_box.py     → render_dialogue(tree)
│   ├── combat_log.py       → CombatUI class
│   └── inventory_menu.py   → render_inventory(items)
│
├── screens/          ← Full-screen views
│   ├── main_menu.py        → show_main_menu()
│   ├── character_creation.py
│   └── game_view.py        → GameView class
│
└── themes/           ← Visual styling
    ├── cyberpunk.py        → CYAN, MAGENTA palette
    ├── fantasy.py          → GOLD, EMERALD palette
    └── post_apo.py         → BROWN, GREEN palette

Key Rule: 🚨 UI components NEVER call game logic directly - only via events
4.6 src/data/ - Data Loading

Purpose: Load and cache JSON game content
python

class DataLoader:
    def __init__(self, data_dir: Path):
        self._cache = {}  # path -> data

    def load_location(self, genre: str, location_id: str) -> dict:
        """Load location JSON with caching"""
        pass

    def load_dialogue_tree(self, genre: str, dialogue_id: str) -> dict:
        """Load dialogue tree JSON"""
        pass

Caching Strategy:

    Cache all loaded JSON in memory
    clear_cache() for hot-reloading during dev
    Preload entire genre on game start (optional)

4.7 src/utils/ - Utilities

Purpose: Helper functions with no dependencies
File	Functions
dice.py	d20(), roll_dice(), skill_check(), advantage()
text.py	(future) Text parsing, formatting
logger.py	(future) Debug logging setup
5. CORE ARCHITECTURE PATTERNS
5.1 State Management Pattern

Problem: Multiple systems need access to game state

Solution: Centralized GameState - single source of truth
python

# ❌ BAD: Tight coupling
class CombatSystem:
    def __init__(self, player, world, save_manager):
        self.player = player
        self.world = world
        self.save_manager = save_manager

# ✅ GOOD: Centralized state
class CombatSystem:
    def __init__(self, game_state: GameState):
        self.state = game_state
        # Access everything through state
        player = self.state.player
        flags = self.state.world_flags

Benefits:

    ✅ Single point of access
    ✅ Easy to serialize (entire state in one object)
    ✅ Clear data flow
    ✅ Testable (mock GameState)

5.2 Event-Driven Communication Pattern

Problem: Systems need to react to each other without direct dependencies

Solution: Publish/Subscribe event bus

Event Types:
python

class EventType(Enum):
    # Player
    PLAYER_MOVED = "player_moved"
    PLAYER_DIALOGUE_CHOICE = "player_dialogue_choice"
    PLAYER_LEVEL_UP = "player_level_up"

    # Combat
    COMBAT_STARTED = "combat_started"
    DAMAGE_DEALT = "damage_dealt"
    COMBAT_ENDED = "combat_ended"

    # World
    LOCATION_ENTERED = "location_entered"
    QUEST_UPDATED = "quest_updated"

    # System
    SAVE_TRIGGERED = "save_triggered"
    GAME_OVER = "game_over"

Example Use Case:
python

# Multiple systems react to single event
def on_combat_ended(event: Event):
    if event.data["player_won"]:
        # Quest system
        quest_system.check_kill_objectives(event.data["enemies"])

        # Save system
        save_manager.autosave(game_state)

        # UI
        ui.show_victory_screen(event.data["xp_gained"])

game_events.subscribe(EventType.COMBAT_ENDED, on_combat_ended)

5.3 Data-Driven Content Pattern

JSON File Structure:

data/genres/cyberpunk/
    locations/golden_drake_tavern.json
    npcs/bartender_tom.json
    dialogues/dialogue_bartender_intro.json
    enemies/street_thug_tutorial.json

Runtime Loading:
python

# Load game content
loader = DataLoader(Path("data"))
location_data = loader.load_location("cyberpunk", "golden_drake_tavern")
location = Location.from_dict(location_data)

Hot-Reloading (Dev Mode):
python

# Reload changed content without restarting game
loader.clear_cache()
location = loader.load_location("cyberpunk", "golden_drake_tavern")

6. KEY SYSTEM DESIGNS
6.1 Combat System Architecture

CombatEncounter (orchestrator)
    │
    ├─ Participants (snapshot pattern)
    │   ├─ Player: hp_current, armor, initiative
    │   └─ Enemies: hp_current, armor, initiative
    │
    ├─ Combat Log (history tracking)
    │   └─ [CombatLog entries with timestamps]
    │
    ├─ Phase Management (FSM)
    │   ├─ INITIATIVE → roll d20 + DEX for all
    │   ├─ PLAYER_TURN → await input
    │   ├─ ENEMY_TURN → AI executes action
    │   ├─ ROUND_END → status effects resolve
    │   └─ VICTORY/DEFEAT → end state
    │
    └─ Action Execution
        ├─ Attack → d20 + bonus vs AC → damage roll
        ├─ Defend → AC +5 until next turn
        ├─ Use Item → consume item, apply effect
        └─ Flee → d20 + DEX vs DC (12 + round_number)

Design Decisions:

    Snapshot Pattern:
        Combat participants are copies, not references
        Why: Prevents mid-combat stat changes from external systems
        Trade-off: Must sync back to entities after combat ends

    Finite State Machine:
        Clear phase transitions prevent illegal actions
        Why: Can't attack during enemy turn, can't use items during initiative

    Separate AI Method: _execute_enemy_ai()
        Why: Different enemy types can override behavior
        Future: Load AI scripts from JSON

Combat Flow Example:
python

combat = CombatEncounter(player, [enemy1, enemy2])
combat.start_combat()

while not combat.is_over:
    if combat.phase == CombatPhase.PLAYER_TURN:
        # UI prompts for action
        action = get_player_action_from_ui()
        combat.execute_player_action(action)

    # Render current state
    combat_ui.render_combat_state(combat)

# Check result
if combat.player_won:
    player.add_xp(combat.total_xp_reward)

6.2 Dialogue System Architecture

DialogueTree
    │
    ├─ Nodes (dict: node_id → DialogueNode)
    │   └─ DialogueNode
    │       ├─ speaker_id: "bartender_tom"
    │       ├─ text: "What do you want?"
    │       ├─ choices: [Choice1, Choice2, ...]
    │       └─ auto_next: "next_node" (optional)
    │
    ├─ Current Node Pointer (tracks position)
    │
    ├─ History (visited node_ids)
    │
    └─ Completion Flag (is_complete)

DialogueChoice
    ├─ choice_id: "persuade_option"
    ├─ text: "Convince him to help"
    ├─ next_node_id: "job_offer_node"
    ├─ requirements: [
    │     {"type": "stat_check", "stat": "charisma", "min": 12},
    │     {"type": "quest_flag", "flag": "met_yakuza"}
    │   ]
    └─ consequences: {
          "relationship_change": {"bartender": +10},
          "set_flag": "bartender_trusts_player"
        }

Requirement System (Extensible):
python

requirements = [
    {"type": "stat_check", "stat": "charisma", "min": 12},
    {"type": "skill_check", "skill": "persuasion", "min": 50},
    {"type": "quest_flag", "flag": "completed_intro"},
    {"type": "item_required", "item_id": "yakuza_token"},
    {"type": "faction_rep", "faction": "yakuza", "min": 50}
]

Why This Design:

    ✅ Tree structure = easy branching
    ✅ Requirements list = combinable conditions (AND logic)
    ✅ Consequences dict = standardized actions
    ✅ Modular: Add new requirement types without touching core
    ✅ JSON-serializable

Dialogue Flow Example:
python

tree = DialogueTree.from_json(dialogue_data)

while not tree.is_complete:
    node = tree.current_node
    print(node.text)

    # Filter choices by requirements
    available = tree.get_available_choices(player)

    for i, choice in enumerate(available):
        requirement_hint = ""
        if choice.display_requirement:
            requirement_hint = "[CHA 12]"
        print(f"{i+1}. {requirement_hint} {choice.text}")

    selection = int(input("> ")) - 1
    tree.select_choice(selection, player, game_state)

6.3 Save System Architecture

Save File Format:
json

{
  "metadata": {
    "save_time": "2026-01-07T23:30:00",
    "version": "1.0.0",
    "location": "golden_drake_tavern",
    "playtime": 3600,
    "player_name": "V",
    "player_level": 3
  },
  "game_state": {
    "phase": "exploration",
    "genre": "cyberpunk",
    "current_location_id": "golden_drake_tavern",
    "world_flags": {
      "met_bartender": true,
      "tutorial_complete": true
    },
    "choice_history": ["bartender_persuade", "accept_job"],
    "turn_count": 145
  },
  "player": {
    "name": "V",
    "level": 3,
    "xp": 280,
    "hp_current": 45,
    "hp_max": 50,
    "stats": {"strength": 12, "dexterity": 14, ...},
    "inventory": [...],
    "equipped": {...},
    "faction_standings": {"yakuza": -20, "helix_corp": 10}
  }
}

Version Migration Strategy:
python

def load_game(slot_name):
    data = load_json(f"saves/{slot_name}.json")

    version = data["metadata"]["version"]

    if version == "1.0.0":
        # Current version - no migration
        pass

    elif version == "0.9.0":
        # Migrate from old format
        data = migrate_0_9_to_1_0(data)

    elif version == "0.8.0":
        # Chain migrations
        data = migrate_0_8_to_0_9(data)
        data = migrate_0_9_to_1_0(data)

    else:
        raise ValueError(f"Unsupported save version: {version}")

    return GameState.from_dict(data["game_state"])

Autosave Triggers:

    ✅ Location change
    ✅ Combat victory
    ✅ Major dialogue choice
    ✅ Quest completion
    ✅ Level up

7. DATA FLOW EXAMPLES
Example 1: Player Makes Dialogue Choice

┌─────────────────┐
│ 1. UI renders   │  User sees choices with [CHA 12] tags
│    dialogue     │
└────────┬────────┘
         │ Player selects choice #2
         ▼
┌─────────────────┐
│ 2. UI publishes │  Event(PLAYER_DIALOGUE_CHOICE, {choice_id: "persuade"})
│    event        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 3. Dialogue     │  - Check requirements (CHA >= 12?)
│    system       │  - Apply consequences (+10 faction rep)
│    processes    │  - Update GameState.choice_history
│                 │  - Transition to next node
└────────┬────────┘
         │ Publishes: DIALOGUE_CHOICE_MADE
         ▼
┌─────────────────┐
│ 4. Multiple     │  - Faction system updates reputation
│    systems      │  - Quest system checks objectives
│    react        │  - Save system triggers autosave
│                 │  - UI re-renders with new node
└─────────────────┘

Example 2: Combat Damage Calculation

Player attacks Enemy A:

1. Player Turn Phase
   └─> execute_player_action(CombatAction.ATTACK, target="enemy_0")

2. Attack Roll
   └─> roll = d20() = 15
   └─> hit_bonus = player.stats.get_modifier('strength') = +2
   └─> total = 15 + 2 = 17

3. Check Hit
   └─> enemy_ac = 10 + enemy.stats.dexterity = 14
   └─> 17 >= 14 → HIT!

4. Damage Roll
   └─> weapon_damage = roll_dice("1d8+3") = 7
   └─> armor_reduction = enemy.armor = 2
   └─> final_damage = max(1, 7 - 2) = 5

5. Apply Damage
   └─> enemy.hp_current -= 5

6. Publish Event
   └─> game_events.publish(Event(DAMAGE_DEALT, {
           "attacker": "player",
           "target": "enemy_0",
           "damage": 5
       }))

7. Systems React
   └─> Combat log appends entry
   └─> UI renders HP bar update
   └─> Check if enemy.hp_current <= 0 → trigger death

8. DATA SCHEMAS
8.1 Location Schema (JSON)
json

{
  "location_id": "string (unique identifier)",
  "name": "string (display name)",
  "description": "string (supports markdown)",
  "type": "hub | dungeon | wilderness",

  "ascii_art": [
    "    ╔════════════════╗",
    "    ║  TAVERN SIGN  ║",
    "    ╚════════════════╝"
  ],

  "exits": {
    "north": {
      "target": "target_location_id",
      "description": "A grimy door",
      "locked": false,
      "key_required": "item_id or null",
      "first_time_exit_text": "The bartender calls out..."
    }
  },

  "npcs": [
    {
      "npc_id": "bartender_tom",
      "spawn_position": "behind_bar",
      "spawn_conditions": {
        "always": true,
        "quest_flag": "quest_flag_name",
        "chance": 0.5
      },
      "dialogue_tree": "dialogue_bartender_intro"
    }
  ],

  "objects": [
    {
      "object_id": "ale_barrel",
      "name": "Dented Ale Barrel",
      "examine_text": "Rusty and smells of motor oil.",
      "interactable": true,
      "actions": {
        "search": {
          "first_time_text": "You find a medkit!",
          "first_time_reward": {"items": ["medkit_basic"]},
          "repeat_text": "Nothing else here."
        }
      }
    }
  ],

  "encounters": [
    {
      "encounter_id": "tutorial_combat",
      "trigger": "dialogue_choice_bartender_accept_tutorial",
      "enemy_groups": [{"enemies": ["street_thug"], "count": 1}],
      "intro_text": "A thug steps forward...",
      "on_victory": {"xp": 50, "items": ["credits_50"]}
    }
  ],

  "ambient_text": [
    "The jukebox skips.",
    "Someone laughs bitterly.",
    "Static crackles."
  ],

  "music_theme": "ambient_noir",
  "danger_level": 0,

  "first_visit_flags": {
    "set_flags": ["visited_golden_drake"],
    "dialogue": "dialogue_tavern_first_entrance"
  }
}

8.2 Dialogue Tree Schema (JSON)
json

{
  "dialogue_id": "dialogue_bartender_intro",
  "speaker_npc_id": "bartender_tom",
  "title": "First Conversation with Tom",

  "nodes": [
    {
      "node_id": "start",
      "speaker": "bartender_tom",
      "text": "Tom doesn't look up. 'You got trouble written all over you.'",

      "choices": [
        {
          "choice_id": "polite",
          "text": "Just looking for information. This place safe?",
          "next_node": "node_info_request",
          "requirements": [],
          "consequences": {
            "relationship_change": {"bartender_tom": 5}
          }
        },
        {
          "choice_id": "charisma_charm",
          "text": "'Buy you a drink, friend? You look stressed.'",
          "next_node": "node_charm_success",
          "requirements": [
            {"type": "stat_check", "stat": "charisma", "min": 12}
          ],
          "display_requirement": true,
          "consequences": {
            "relationship_change": {"bartender_tom": 15},
            "player_spend_credits": 20
          }
        },
        {
          "choice_id": "leave",
          "text": "[Leave]",
          "next_node": "END",
          "requirements": []
        }
      ]
    },

    {
      "node_id": "node_info_request",
      "speaker": "bartender_tom",
      "text": "'Safe as anywhere. Keep your head down.'",
      "choices": [...]
    }
  ]
}

8.3 Enemy Schema (JSON)
json

{
  "enemy_id": "street_thug_tutorial",
  "name": "Ricky 'Fast Hands' Chen",
  "type": "humanoid",
  "danger_level": 1,

  "description": "Wiry guy with gang tattoos.",

  "stats": {
    "level": 1,
    "hp_max": 30,
    "hp_current": 30,
    "armor": 2,
    "evasion": 12,
    "strength": 10,
    "dexterity": 14,
    "intelligence": 8
  },

  "combat_behavior": {
    "ai_type": "aggressive_melee",
    "preferred_range": "close",
    "special_tactics": [
      {
        "name": "Cheap Shot",
        "trigger_condition": "hp_below_50_percent",
        "effect": "extra_damage_5"
      }
    ]
  },

  "attacks": [
    {
      "attack_id": "punch",
      "name": "Street Brawl Punch",
      "type": "melee",
      "damage_dice": "1d6+2",
      "hit_bonus": 3,
      "description": "Quick jab at your jaw."
    }
  ],

  "loot_table": {
    "guaranteed": [{"item_id": "credits_50", "quantity": 1}],
    "random": [
      {"item_id": "cheap_stim", "chance": 0.3},
      {"item_id": "switchblade", "chance": 0.15}
    ]
  },

  "xp_reward": 50,

  "dialogue": {
    "on_encounter": "'Nothing personal, choom.'",
    "on_hit_player": ["Ha! Too slow!", "Got you!"],
    "on_hit_by_player": ["Agh! Lucky shot!"],
    "on_death": "'Alright... I'm done. You win.'"
  },

  "tutorial_notes": {
    "is_tutorial_enemy": true,
    "non_lethal": true,
    "hints_during_combat": [
      "TIP: Use [Defend] to reduce damage by 50%"
    ]
  }
}

8.4 NPC Schema (JSON)
json

{
  "npc_id": "bartender_tom",
  "name": "Tom 'Chrome-Arm' Valdez",
  "title": "Bartender",

  "description": "Grizzled veteran with a chrome arm.",

  "portrait_ascii": [
    "    ⚙️👁️",
    "   /|🥃|\\",
    "    | |"
  ],

  "personality": {
    "traits": ["cynical", "protective", "seen_it_all"],
    "voice": "Gravelly, short sentences."
  },

  "stats": {
    "level": 8,
    "strength": 14,
    "charisma": 8
  },

  "faction_affiliations": {
    "veterans_guild": 80,
    "downtown_locals": 60
  },

  "merchant_data": {
    "is_merchant": true,
    "shop_inventory": [
      {"item_id": "synth_whiskey", "price": 20, "stock": -1},
      {"item_id": "medkit_basic", "price": 100, "stock": 3}
    ],
    "discount_conditions": {
      "charisma_check": {"min_charisma": 12, "discount_percent": 20}
    }
  },

  "dialogue_trees": {
    "default": "dialogue_bartender_intro",
    "post_tutorial": "dialogue_bartender_regular"
  },

  "relationship_tracker": {
    "initial_standing": 0,
    "max_standing": 100,
    "current_standing": 0
  }
}

9. GAME LOOP DESIGN
Main Loop Pseudocode
python

def main_game_loop(game_state: GameState):
    """
    Central game loop - handles all phases
    """

    while game_state.phase != GamePhase.MAIN_MENU:

        # 1. Render current state based on phase
        if game_state.phase == GamePhase.EXPLORATION:
            location = load_current_location(game_state)
            game_view.render(game_state, location)

        elif game_state.phase == GamePhase.DIALOGUE:
            dialogue_ui.render(game_state.active_dialogue)

        elif game_state.phase == GamePhase.COMBAT:
            combat_ui.render_combat_state(game_state.active_combat)

        # 2. Get player input
        command = input_handler.get_command()

        # 3. Process command based on phase
        if game_state.phase == GamePhase.EXPLORATION:
            handle_exploration_command(command, game_state)

        elif game_state.phase == GamePhase.DIALOGUE:
            handle_dialogue_command(command, game_state)

        elif game_state.phase == GamePhase.COMBAT:
            handle_combat_command(command, game_state)

        # 4. Update systems
        quest_system.check_objectives(game_state)

        # 5. Check for phase transitions
        if game_state.active_combat and game_state.active_combat.is_over:
            game_state.phase = GamePhase.EXPLORATION
            game_state.active_combat = None

        if game_state.active_dialogue and game_state.active_dialogue.is_complete:
            game_state.phase = GamePhase.EXPLORATION
            game_state.active_dialogue = None

Command Handling Example
python

def handle_exploration_command(command: str, game_state: GameState):
    """Process commands during exploration phase"""

    if command.startswith("talk"):
        npc_id = parse_npc_name(command)
        start_dialogue(npc_id, game_state)

    elif command.startswith("go"):
        direction = parse_direction(command)
        move_to_location(direction, game_state)

    elif command.startswith("examine"):
        object_id = parse_object_name(command)
        examine_object(object_id, game_state)

    elif command == "stats":
        show_character_sheet(game_state.player)

    elif command in ["inventory", "inv"]:
        show_inventory(game_state.player)

    elif command == "save":
        save_manager.save_game(game_state, "manual_save")

    elif command == "quit":
        confirm_and_quit(game_state)

10. TESTING STRATEGY
10.1 Unit Tests
python

# tests/test_dice.py
def test_d20_range():
    """d20 should always return 1-20"""
    for _ in range(100):
        roll = d20()
        assert 1 <= roll <= 20

def test_roll_dice_notation():
    """roll_dice should parse notation correctly"""
    # 2d6+3 should be 5-15
    for _ in range(100):
        roll = roll_dice("2d6+3")
        assert 5 <= roll <= 15

def test_roll_dice_with_negative_modifier():
    """roll_dice should handle negative modifiers"""
    result = roll_dice("1d6-2")
    assert -1 <= result <= 4  # 1-2 = -1, 6-2 = 4

python

# tests/test_player.py
def test_player_skill_check():
    """Skill checks should work with bonuses"""
    player = Player(name="Test")
    player.skills["hacking"] = 5

    # Mock d20 to return 10
    with mock.patch('src.utils.dice.d20', return_value=10):
        success, total = player.skill_check("hacking", difficulty=14)
        assert total == 15  # 10 + 5
        assert success is True

def test_player_take_damage():
    """Taking damage should reduce HP"""
    player = Player(hp_current=50, hp_max=50)
    player.take_damage(20)
    assert player.hp_current == 30

10.2 Integration Tests
python

# tests/test_integration/test_combat_flow.py
def test_full_combat_encounter():
    """Complete combat from start to victory"""

    # Setup
    player = Player(name="Test", hp_current=50)
    enemy_data = load_json("data/genres/cyberpunk/enemies/street_thug_tutorial.json")
    enemy = Enemy.from_dict(enemy_data)

    combat = CombatEncounter(player, [enemy])
    combat.start_combat()

    # Simulate player attacks until victory
    while not combat.is_over:
        if combat.phase == CombatPhase.PLAYER_TURN:
            action = CombatAction(
                action_type=CombatActionType.ATTACK,
                actor_id="player",
                target_id="enemy_0"
            )
            combat.execute_player_action(action)

    # Verify outcome
    assert combat.player_won is True
    assert len(combat.combat_log) > 0
    assert player.xp > 0  # XP granted on victory

10.3 Test Coverage Goals
Module	Target Coverage
src/core/	90%+
src/entities/	85%+
src/systems/	80%+
src/utils/	95%+
src/ui/	50%+ (visual testing)
11. PERFORMANCE OPTIMIZATION
11.1 Caching Strategy
python

class DataLoader:
    def __init__(self):
        self._cache = {}  # path -> data

    def _load_json(self, path: Path) -> dict:
        """Load JSON with caching"""
        cache_key = str(path)

        # Cache hit - instant return
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Cache miss - load from disk
        with open(path, 'r') as f:
            data = json.load(f)

        # Store in cache
        self._cache[cache_key] = data
        return data

When to Clear Cache:

    Development: After modifying JSON files
    Production: Never (cache persists entire session)

11.2 Lazy Loading
python

class WorldManager:
    def __init__(self):
        self._loaded_locations = {}

    def get_location(self, location_id: str) -> Location:
        """Load location on-demand"""
        if location_id not in self._loaded_locations:
            data = loader.load_location(genre, location_id)
            self._loaded_locations[location_id] = Location.from_dict(data)

        return self._loaded_locations[location_id]

Benefits:

    Don't load entire game world at startup
    Load locations as player reaches them
    Lower memory footprint

11.3 Terminal Render Optimization
python

class GameView:
    def render_partial(self, changed_section: str):
        """Only re-render changed UI sections"""

        if changed_section == "stats":
            # Only update sidebar
            self.layout["sidebar"].update(render_stats(self.player))

        elif changed_section == "location":
            # Only update main content
            self.layout["content"].update(render_location(self.location))

        # Don't re-render entire screen
        self.console.print(self.layout)

Rich Library Optimization:

    Rich already handles dirty region tracking
    Use Layout for composite UIs
    Avoid console.clear() when possible

11.4 Performance Targets
Operation	Target Time	Notes
Data load (cached)	<1ms	In-memory lookup
Data load (uncached)	<50ms	Disk read + JSON parse
Save game	<200ms	JSON serialization + write
Load game	<500ms	Read + deserialize + validate
UI render	<16ms	60 FPS target
Combat action	<100ms	Including AI decision
12. SCALABILITY & EXTENSIBILITY
12.1 Genre Modularity

data/
  genres/
    cyberpunk/          # Current implementation
      locations/
      npcs/
      items/
      skills.json
      factions.json

    fantasy/            # Future DLC
      locations/
      npcs/
      items/
      skills.json       # Different skill tree
      magic_schools.json

    post_apo/           # Future DLC
      locations/
      npcs/
      items/
      radiation_rules.json

Same Engine, Different Content:
python

# Load genre-specific content
game_state.genre = "fantasy"
loader = DataLoader(Path("data"))
skills = loader.load_genre_file("fantasy", "skills.json")

UI Themes by Genre:
python

# src/ui/themes/fantasy.py
THEME = {
    "primary": "#D4AF37",  # Gold
    "accent": "#50C878",   # Emerald
    "danger": "#8B0000",   # Dark red
    "text": "#F5F5DC"      # Beige
}

12.2 Modding Support (Future)

~/.terminal-rpg/mods/
  my_custom_quest/
    mod.json          # Metadata (name, author, version)
    locations/
      custom_dungeon.json
    npcs/
      custom_merchant.json
    dialogues/
      custom_quest_dialogue.json

Mod Loader:
python

class ModLoader:
    def load_mods(self):
        """Load and merge mod content"""
        for mod_dir in Path("~/.terminal-rpg/mods").iterdir():
            mod_metadata = load_json(mod_dir / "mod.json")

            # Merge locations
            for location_file in (mod_dir / "locations").glob("*.json"):
                self.register_location(location_file)

12.3 Scripting Layer (Future)

Lua Scripts for Quest Logic:
lua

-- data/quests/find_stolen_chip.lua
function on_quest_start(player, world)
    world.set_flag("chip_quest_active", true)
    player.add_item("quest_datapad")
end

function on_quest_complete(player, world)
    player.add_xp(500)
    player.modify_faction("yakuza", -20)
    world.set_flag("chip_returned", true)
end

13. DEVELOPMENT WORKFLOW
13.1 Adding a New Feature

Step-by-Step Process:

    Design - Update GDD/docs
    Data - Create JSON files (if content-heavy)
    Entities - Add data classes if needed
    Systems - Implement game logic
    Events - Define new event types
    UI - Create/update components
    Test - Write unit tests
    Integration - Connect to main loop
    Playtest - Manual QA

13.2 Example: Adding Netrunning System

1. Design
   └─ Update GDD with netrunning mechanics

2. Data
   └─ Create data/genres/cyberpunk/netrun_programs.json

3. Entities
   └─ No new entities needed (uses existing Player)

4. Systems
   └─ Create src/systems/netrunning.py
      └─ class NetrunSession:
             def start_hack(target):
                 ...

5. Events
   └─ Add to event_dispatcher.py:
      └─ EventType.NETRUN_STARTED
      └─ EventType.NETRUN_SUCCESS
      └─ EventType.NETRUN_DETECTED

6. UI
   └─ Create src/ui/components/netrun_interface.py
      └─ def render_netrun_ui(session):
             ...

7. Test
   └─ Create tests/test_netrunning.py

8. Integration
   └─ Update GamePhase enum with NETRUNNING
   └─ Add to main game loop

9. Playtest
   └─ Test netrun encounter from tavern

13.3 Git Workflow

Branch Strategy:

main                    ← Stable releases only
├─ develop              ← Active development
│  ├─ feature/combat-system
│  ├─ feature/dialogue-trees
│  └─ bugfix/save-corruption

Commit Message Format:

[category] Brief description

- Detailed change 1
- Detailed change 2

Closes #123

Categories:

    [feat] New feature
    [fix] Bug fix
    [refactor] Code cleanup
    [docs] Documentation
    [test] Tests
    [data] Content changes (JSON)

14. DEBUGGING TOOLS
14.1 Event History Viewer
python

# View all events fired this session
history = game_events.get_event_history()

for event in history:
    print(f"{event.type}: {event.data}")

# Filter by type
combats = game_events.get_event_history(EventType.COMBAT_STARTED)

14.2 State Inspector
python

# Dump current game state to JSON
import json
print(json.dumps(game_state.to_dict(), indent=2))

# Check specific flags
print(game_state.world_flags)
print(game_state.choice_history)

14.3 Dialogue Tree Visualizer (Future)
bash

# Generate Graphviz diagram of dialogue tree
python tools/visualize_dialogue.py dialogue_bartender_intro.json > tree.dot
dot -Tpng tree.dot -o tree.png

Output:

[start] → [node_info_request]
        ↘ [node_charm_success]
        ↘ [END]

[node_info_request] → [node_tutorial_offer]
                     ↘ [node_tutorial_declined]

14.4 Combat Simulator
python

# Test combat balance without playing
def simulate_combat(player_stats, enemy_id, iterations=1000):
    wins = 0

    for _ in range(iterations):
        player = Player(stats=player_stats, hp_current=50)
        enemy = Enemy.from_dict(load_enemy(enemy_id))

        combat = CombatEncounter(player, [enemy])
        combat.start_combat()

        # Auto-attack until end
        while not combat.is_over:
            if combat.phase == CombatPhase.PLAYER_TURN:
                combat.execute_player_action(attack_action)

        if combat.player_won:
            wins += 1

    return wins / iterations  # Win rate

# Test balance
win_rate = simulate_combat(PlayerStats(strength=12), "street_thug", 1000)
print(f"Win rate: {win_rate*100}%")  # Should be ~70-80% for tutorial enemy

15. DEPENDENCIES & TECH STACK
15.1 Production Dependencies
toml

[project]
dependencies = [
    "rich>=13.7.0",        # Terminal UI - tables, panels, colors
    "pydantic>=2.5.0",     # Data validation (future use)
    "pyyaml>=6.0",         # YAML support (optional vs JSON)
]

Why Rich?

    ✅ Beautiful terminal output with zero effort
    ✅ Layouts, tables, panels out-of-the-box
    ✅ TrueColor support (16M colors)
    ✅ Cross-platform (Windows/Linux/Mac)

15.2 Development Dependencies
toml

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",       # Test framework
    "pytest-cov>=4.1.0",   # Coverage reporting
    "black>=23.12.0",      # Code formatter
    "ruff>=0.1.0",         # Fast linter
    "mypy>=1.7.0",         # Static type checker
]

15.3 Dependency Management

Installation:
bash

# Production only
pip install -e .

# Development
pip install -e ".[dev]"

Lock File:
bash

# Generate requirements.txt from pyproject.toml
pip freeze > requirements.txt

16. CODE STYLE GUIDE
16.1 Python Conventions
python

# ✅ Class names: PascalCase
class DialogueTree:
    pass

class CombatEncounter:
    pass

# ✅ Functions/variables: snake_case
def execute_player_action(action):
    current_hp = player.hp_current

# ✅ Constants: SCREAMING_SNAKE_CASE
MAX_INVENTORY_SIZE = 50
DEFAULT_PLAYER_HP = 50

# ✅ Private methods: _leading_underscore
def _calculate_damage(self, roll):
    pass

# ✅ Type hints everywhere
def skill_check(skill_value: int, difficulty: int) -> tuple[bool, int]:
    pass

16.2 File Organization
python

# File: src/systems/dialogue.py

"""
Dialogue System - Branching conversation trees

This module handles dialogue tree processing, requirement checking,
and consequence application.
"""

# Standard library imports
from dataclasses import dataclass
from typing import List, Optional, Callable
from enum import Enum

# Third-party imports
from rich.console import Console

# Local imports
from src.core.event_dispatcher import game_events, Event

# Constants
MAX_CHOICES = 5
DEFAULT_TIMEOUT = 30

# Enums
class ChoiceRequirement(Enum):
    NONE = "none"
    STAT_CHECK = "stat_check"

# Dataclasses
@dataclass
class DialogueChoice:
    """Represents a single dialogue choice"""
    text: str
    next_node_id: str

# Main classes
class DialogueTree:
    """Manages branching dialogue flow"""

    def __init__(self, nodes: List[DialogueNode]):
        self.nodes = nodes

    def select_choice(self, index: int):
        """Process player choice selection"""
        pass

# Helper functions (private)
def _validate_node(node: DialogueNode) -> bool:
    """Validate node structure"""
    pass

16.3 Documentation Standards

Docstring Format:
python

def skill_check(skill_value: int, difficulty: int) -> tuple[bool, int]:
    """
    Perform a skill check against DC

    Args:
        skill_value: Bonus to add to d20 roll
        difficulty: Target Difficulty Class (10-30)

    Returns:
        Tuple of (success: bool, total_roll: int)

    Example:
        >>> success, total = skill_check(5, 15)
        >>> if success:
        ...     print(f"Success with {total}!")
    """
    pass

16.4 Git Commit Guidelines

Format:

[category] Brief summary (50 chars max)

Detailed explanation of changes:
- Point 1
- Point 2

Closes #123

Categories:

    [feat] New feature
    [fix] Bug fix
    [refactor] Code restructure
    [docs] Documentation
    [test] Tests
    [data] JSON content changes

Examples:

[feat] Add dialogue requirement system

- Implemented stat checks (CHA, INT, STR)
- Added quest flag requirements
- Created consequence application framework

Closes #45

---

[fix] Combat damage calculation off by one

Fixed armor reduction applying twice in melee attacks.

Closes #78

17. FUTURE ROADMAP
17.1 Planned Refactors
ECS Architecture (Entity-Component-System)

Current: Object-oriented entities Future: Component-based composition
python

# Current
class Player:
    hp: int
    stats: PlayerStats
    inventory: List[Item]

# ECS Future
class Entity:
    components: Dict[str, Component]

player.get_component(HealthComponent).hp
player.get_component(StatsComponent).strength

Benefits:

    Better performance (data locality)
    More flexible entity composition
    Easier to serialize

Async I/O for File Loading
python

# Current: Blocking
data = loader.load_location("cyberpunk", "tavern")

# Future: Async
data = await loader.load_location_async("cyberpunk", "tavern")

Benefits:

    Non-blocking load screens
    Preload next location during travel
    Smoother gameplay

Compiled Asset Pipeline
python

# Development: JSON (human-readable)
data/genres/cyberpunk/locations/tavern.json

# Production: Binary (faster loading)
data/compiled/cyberpunk_locations.pak

Tools:
bash

python tools/compile_assets.py --genre cyberpunk --output data/compiled/

Benefits:

    10x faster load times
    Smaller file size (compressed)
    Harder to mod (but official modding API provided)

17.2 Potential Features
Scripting Layer (Lua)

Use Case: Complex quest logic without hardcoding
lua

-- data/quests/yakuza_infiltration.lua
function on_enter_compound(player, world)
    if player.has_item("disguise_uniform") then
        world.spawn_npc("guard_friendly")
    else
        world.trigger_combat("yakuza_guards")
    end
end

Network Multiplayer (Ambitious)

Mode: Turn-based co-op (2 players)
python

# Host player
session = MultiplayerSession.host(port=7777)

# Client player
session = MultiplayerSession.join(host="192.168.1.10", port=7777)

# Shared game state
session.sync_game_state()

Challenges:

    State synchronization
    Turn timing
    Network latency handling

18. GLOSSARY
Term	Definition
Game State	Central data container holding all game progress
Event Bus	Pub/sub system for cross-system communication
Participant	Combat wrapper around Player/Enemy entities
Dialogue Node	Single point in conversation tree
Requirement	Condition for dialogue choice visibility
Consequence	Action triggered by dialogue choice
Genre	Content theme (cyberpunk/fantasy/post-apo)
Snapshot Pattern	Creating copies instead of references for isolation
FSM	Finite State Machine - clear state transitions
Data-Driven	Content in JSON, not hardcoded in Python
Lazy Loading	Load data on-demand instead of at startup
Hot-Reloading	Reload changed files without restarting game
Serialization	Converting objects to JSON for saving
Deserialization	Reconstructing objects from JSON
AC	Armor Class - target number for attack rolls
DC	Difficulty Class - target number for skill checks
d20	20-sided die roll (1-20)
XP	Experience Points for leveling
RECOMMENDED READING ORDER

For New Developers:

    src/utils/dice.py - Simple, no dependencies
    src/core/event_dispatcher.py - Core pattern
    src/core/game_state.py - Central state
    src/entities/player.py - Data structure example
    src/systems/dialogue.py - System example
    src/systems/combat.py - Complex system
    src/main.py - Entry point + loop

For Content Creators:

    data/genres/cyberpunk/locations/golden_drake_tavern.json
    data/genres/cyberpunk/dialogues/dialogue_bartender_intro.json
    data/genres/cyberpunk/enemies/street_thug_tutorial.json
    docs/GDD.md - Game design reference

ARCHITECTURE GOALS

✅ Modularity - Systems can be swapped/extended
✅ Testability - Pure functions, dependency injection
✅ Scalability - Add content without touching code
✅ Maintainability - Clear responsibilities, no spaghetti
✅ Genre-Agnostic - Same engine, different data
✅ Performance - <100ms for any user action
✅ Developer-Friendly - Easy to onboard new contributors

Document Version: 1.0.0
Last Updated: 2026-01-07
Status: Living Document - Updated as architecture evolves

Questions? Open an issue on GitHub or contact the dev team.
```
