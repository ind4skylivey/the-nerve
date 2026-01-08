# Terminal RPG - Vertical Slice Plan
**2-Week Implementation Roadmap**

**Goal:** Playable demo with ALL core mechanics  
**Timeline:** 14 days  
**Status:** In Progress  

---

## OVERVIEW

### What is a Vertical Slice?
A minimal but **complete** version of the game that includes:
- ✅ Every major system (combat, dialogue, exploration)
- ✅ One full example of each (1 location, 1 NPC, 1 fight)
- ✅ Polish enough to feel like a real game

### Why This Matters
- Proves the concept works
- Identifies technical blockers early
- Creates a foundation to build on
- Generates excitement (shareable demo)

---

## WEEK 1: FOUNDATION + DIALOGUE

### Day 1-2: Core Systems Setup

#### Tasks
- [x] Project structure (folders, files)
- [x] `game_state.py` - State management
- [x] `event_dispatcher.py` - Event bus
- [x] `player.py` - Player entity with stats
- [x] `dice.py` - Dice rolling system
- [x] `save_manager.py` - Basic save/load

#### Deliverables
```python
# Can create a player
player = Player(name="V", stats=PlayerStats(strength=12))

# Can save/load
save_manager.save_game(game_state, "slot_1")
loaded_state = save_manager.load_game("slot_1")

# Can roll dice
result = roll_dice("2d6+3")  # Returns 5-15

Validation

    Player created with valid stats
    Save/load works without corruption
    Dice rolls within expected ranges

Day 3-4: UI Foundation + First Location
Tasks

    renderer.py - Rich console setup
    stat_panel.py - Character sheet component
    location.py - Location class
    loader.py - JSON data loader
    golden_drake_tavern.json - First location data

Deliverables
python

# Load and display location
location = Location.from_dict(loader.load_location("cyberpunk", "golden_drake_tavern"))

# Render UI
console.print(render_stats(player))
console.print(location.description)

Validation

    Location loads from JSON
    Stats panel displays correctly
    Can examine objects in location
    Exits listed properly

Day 5-7: Dialogue System Complete
Tasks

    dialogue.py - Dialogue tree engine
    dialogue_box.py - UI component
    bartender_tom.json - NPC data
    dialogue_bartender_intro.json - Full dialogue tree
    Implement skill checks in dialogue
    Consequence system (relationship changes, flags)

Deliverables
python

# Load dialogue
dialogue_data = loader.load_dialogue_tree("cyberpunk", "dialogue_bartender_intro")
tree = DialogueTree.from_json(dialogue_data)

# Play conversation
while not tree.is_complete:
    print(tree.current_node.text)
    choices = tree.get_available_choices(player)
    # ... player selects choice
    tree.select_choice(choice_index, player)

Test Scenarios

    Basic Conversation - Play through without requirements
    Stat Check Success - [CHA 12] option available if player.charisma >= 12
    Stat Check Failure - [CHA 12] option grayed out if charisma < 12
    Consequence Applied - Relationship with bartender increases after choice
    Branching Paths - Different choices lead to different endings

Validation

    Dialogue tree loads without errors
    Choices filtered by requirements
    Consequences applied correctly
    Can reach multiple endings

CHECKPOINT WEEK 1
Must Have Working:

✅ Player creation
✅ Location loading and display
✅ Dialogue system with skill checks
✅ Save/load
Playable Flow:

1. Start game
2. Create character (name + allocate stats)
3. Spawn in tavern
4. Talk to bartender
5. Make dialogue choices (some gated by stats)
6. See conversation outcome
7. Save game

WEEK 2: COMBAT + INTEGRATION
Day 8-10: Combat System
Tasks

    combat.py - Turn-based combat engine
    combat_log.py - Combat UI component
    enemy.py - Enemy entity class
    street_thug_tutorial.json - Tutorial enemy data
    Integrate combat into dialogue (trigger encounter)
    Victory/defeat handling

Deliverables
python

# Start combat
enemy = Enemy.from_dict(loader.load_enemy("cyberpunk", "street_thug_tutorial"))
combat = CombatEncounter(player, [enemy], is_tutorial=True)
combat.start_combat()

# Combat loop
while not combat.is_over:
    if combat.phase == CombatPhase.PLAYER_TURN:
        action = get_player_action()  # UI prompts
        combat.execute_player_action(action)
    
    render_combat_ui(combat)

# Check result
if combat.player_won:
    player.add_xp(enemy.xp_reward)

Combat Scenarios to Test

    Basic Attack - Player attacks, enemy takes damage
    Defend Action - Player defends, AC increases
    Use Item - Player uses medkit, HP restored
    Enemy AI - Enemy attacks player automatically
    Victory - All enemies dead → XP granted
    Defeat - Player HP reaches 0 → game over
    Flee - Player escapes combat

Validation

    Initiative rolls correctly
    Attack rolls hit/miss based on AC
    Damage calculated with armor reduction
    Turn order respected
    Combat log records all events
    Victory grants XP and loot

Day 11-12: Inventory + Items
Tasks

    inventory.py - Inventory management system
    item.py - Item entity class
    inventory_menu.py - UI component
    Create item data files (medkit, pistol, etc.)
    Integrate items into combat (use item action)

Deliverables
python

# Add item to inventory
medkit = Item.from_dict(loader.load_item("cyberpunk", "medkit_basic"))
player.add_item(medkit)

# Use item in combat
combat.execute_player_action(CombatAction(
    action_type=CombatActionType.USE_ITEM,
    actor_id="player",
    item_id="medkit_basic"
))

Validation

    Items load from JSON
    Can add/remove items
    Inventory UI displays items correctly
    Items usable in combat
    Items removed after use

Day 13-14: Polish + Integration
Tasks

    Main game loop (connects all systems)
    Character creation screen
    Main menu (New Game / Load Game / Quit)
    Autosave on location change
    Tutorial integration (tavern → dialogue → combat → win)
    Bug fixes
    Playtesting

Main Loop Pseudocode
python

def main():
    # Main menu
    choice = show_main_menu()
    
    if choice == "new_game":
        player = character_creation_screen()
        game_state = GameState(player=player)
        game_state.current_location_id = "golden_drake_tavern"
    elif choice == "load_game":
        game_state = save_manager.load_game("slot_1")
    
    # Game loop
    while True:
        location = load_current_location(game_state)
        render_location_view(location, game_state)
        
        command = get_player_input()
        
        if command.startswith("talk"):
            npc_id = parse_npc_name(command)
            start_dialogue(npc_id, game_state)
        elif command.startswith("go"):
            direction = parse_direction(command)
            move_to_location(direction, game_state)
        elif command == "stats":
            show_character_sheet(game_state.player)
        elif command == "quit":
            save_and_quit(game_state)

Validation

    Can complete full flow: create char → explore → talk → fight → win
    Autosave triggers correctly
    No crashes during happy path
    Combat tutorial feels fair
    Dialogue choices make sense

CHECKPOINT WEEK 2
Must Have Working:

✅ Combat system (full turn-based flow)
✅ Inventory and items
✅ Main game loop
✅ Tutorial playthrough
Demo Script (10 minutes):

1. Start game → See main menu
2. New Game → Character creation (allocate stats)
3. Spawn in Golden Drake Tavern
4. Examine ale barrel → Find medkit
5. Talk to Bartender Tom
   - Try [CHA 12] option (success if CHA high enough)
   - Accept combat tutorial
6. Fight Street Thug
   - Attack twice
   - Use medkit when low HP
   - Defeat enemy
7. Return to bartender → Post-combat dialogue
8. Save game
9. Quit and reload → Verify save works

SCOPE LIMITS (What's NOT in Vertical Slice)
Explicitly Excluded:

    ❌ Multiple locations (just tavern)
    ❌ Multiple NPCs (just bartender)
    ❌ Quest system (just dialogue flags)
    ❌ Multiple enemies (just 1 tutorial fight)
    ❌ Advanced combat (no special abilities/perks)
    ❌ Equipment system (just inventory)
    ❌ Faction reputation (just NPC relationships)
    ❌ Level-up screen (auto-level background)

Why This is Okay:

The vertical slice proves:

    ✅ Combat works
    ✅ Dialogue works
    ✅ Data pipeline works
    ✅ Save system works

Everything else is scaling content, not proving systems.
SUCCESS CRITERIA
Technical

    All core systems implemented
    Zero crashes in happy path
    Save/load works reliably
    Performance: <100ms input lag

Gameplay

    Tutorial combat feels fair
    Dialogue choices feel meaningful
    Stat checks intuitive (clear when you pass/fail)
    Win condition achievable

Polish

    UI looks clean (no text overflow)
    Colors consistent (cyberpunk theme)
    Tutorial hints clear
    Error messages helpful

RISK MITIGATION
Risk: Combat Balance Issues

Mitigation: Tutorial enemy has low HP (30), telegraphed attacks
Risk: Dialogue Tree Too Complex

Mitigation: Limit to 5 nodes, 3 branches max
Risk: Save Corruption

Mitigation: Validate JSON on load, backup saves
Risk: Terminal Compatibility

Mitigation: Test on 3 terminals (iTerm, Windows Terminal, Alacritty)
POST-VERTICAL SLICE
Immediate Next Steps:

    Gather playtest feedback
    Fix critical bugs
    Balance combat (if too easy/hard)
    Refactor based on learnings

Phase 2 Prep:

    Design 5 more locations
    Write 10 more NPCs
    Create faction system
    Add quest tracking

DAILY CHECKLIST TEMPLATE
markdown

### Day X - [Focus Area]

**Goal:** [What you're building today]

**Tasks:**
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

**Tests:**
- [ ] Test scenario 1
- [ ] Test scenario 2

**Blockers:**
- [Note any issues]

**Tomorrow:**
- [What's next]

FINAL DELIVERABLE
GitHub Release: v0.1.0-vertical-slice

Includes:

    Full source code
    Data files (1 location, 1 NPC, 1 enemy)
    README with quickstart
    Demo video (terminal recording)

Announcement:

🎮 Terminal RPG - Vertical Slice Released!

Play a 10-minute cyberpunk RPG demo in your terminal.

Features:
✅ Stat-based dialogue choices
✅ Turn-based tactical combat
✅ Beautiful terminal UI
✅ Save/load system

Try it: [GitHub link]
Feedback welcome!

Status: Ready to begin
Next Update: After Week 1 checkpoint 
