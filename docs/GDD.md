(Game Design Document)

# Terminal RPG - Game Design Document (GDD)

## Offline Single-Player Roleplay Edition

**Version:** 1.0.0
**Last Updated:** 2026-01-07
**Author:** S1B Group Development Team

---

## 1. EXECUTIVE SUMMARY

### Vision Statement

Create a deep, choice-driven terminal RPG that captures the spirit of classic CRPGs (Fallout 1/2, Baldur's Gate) while leveraging modern terminal UI capabilities. Focus on meaningful player choices, consequence-driven narratives, and tactical turn-based combat.

### Core Pillars

1. **Meaningful Choices** - Every decision has consequences
2. **Stat-Based Roleplay** - Skills and attributes unlock unique dialogue/actions
3. **Tactical Combat** - Turn-based combat with positioning and resource management
4. **Branching Narratives** - Multiple paths, endings, and faction allegiances
5. **Terminal-First Design** - Beautiful ASCII/Unicode art, optimized for CLI experience

### Target Audience

- Classic CRPG fans (Fallout, BG, Planescape Torment)
- Terminal enthusiasts and retro gamers
- Roleplayers who value consequence-driven narratives
- Developers interested in text-based game design

---

## 2. GAME OVERVIEW

### Genre

Roleplaying Game (RPG) - Narrative-Driven / Tactical Combat

### Platform

Cross-platform terminal emulators (Linux, macOS, Windows)

### Unique Selling Points

- **Parser + Choice Hybrid** - Combines natural commands with dialogue wheels
- **Faction Reputation System** - Dynamic world that reacts to player allegiances
- **Stat Check Transparency** - Shows requirements (e.g., [CHA 12]) before selection
- **Non-Linear Progression** - Multiple solutions to quests, no forced outcomes
- **Terminal Art** - Rich colors, Unicode borders, ASCII art for immersion

---

## 3. CORE GAMEPLAY SYSTEMS

### 3.1 Character System

#### Stats (2-18 Scale, D&D Style)

- **Strength (STR)** - Melee damage, intimidation, physical feats
- **Dexterity (DEX)** - Ranged attacks, dodge chance, stealth
- **Intelligence (INT)** - Hacking, knowledge checks, crafting
- **Charisma (CHA)** - Persuasion, leadership, negotiation
- **Luck (LCK)** - Critical hits, loot quality, random events

#### Skills (0-100 Scale)

Combat Skills:

- Melee, Ranged, Unarmed

Technical Skills:

- Hacking, Lockpicking, Medicine, Crafting

Social Skills:

- Persuasion, Intimidation, Deception

Utility Skills:

- Stealth, Perception, Survival

#### Traits System

**Positive Traits** (Choose 2):

- Charming (+2 CHA, dialogue bonuses)
- Tough (+10 HP)
- Quick Learner (+25% XP)
- Tech Savvy (+15 Hacking)

**Negative Traits** (Choose 1):

- Hunted (Start with -20 faction rep)
- Addicted (Periodic stat penalties)
- Clumsy (-2 DEX)
- Illiterate (-3 INT)

---

### 3.2 Combat System

#### Turn-Based Mechanics

1. **Initiative Phase** - d20 + DEX determines turn order
2. **Player Turn** - 2 actions per turn (attack, defend, item, move)
3. **Enemy Turn** - AI-controlled actions
4. **Round End** - Status effects resolve

#### Action Types

- **Attack** - Standard weapon attack (d20 + STR/DEX vs. enemy AC)
- **Defend** - +5 AC until next turn
- **Use Item** - Consume healing/buff item
- **Special Ability** - Perk-based powers (costs stamina)
- **Flee** - Attempt escape (d20 + DEX vs. DC)

#### Damage Calculation

Attack Roll = d20 + Stat Modifier + Weapon Bonus Hit if Attack Roll >= Enemy AC

Damage = Weapon Dice + Stat Modifier - Enemy Armor Critical Hit (natural 20) = Double dice damage

#### Example Combat Flow

Round 1: Initiative: Player (16), Enemy A (12), Enemy B (8)

Player Turn: > Attack Enemy A > Roll: 15 + 3 (STR) + 2 (weapon) = 20 vs AC 14 → HIT > Damage: 1d8+3 = 7 damage - 2 armor = 5 final damage

Enemy A Turn: > Attack Player > Roll: 12 + 1 = 13 vs AC 15 → MISS

Enemy B Turn: > Defend (AC +5)

Round 2: ...

---

### 3.3 Dialogue System

#### Structure

Dialogue Node:

    Speaker: NPC name
    Text: What NPC says
    Choices: 1-5 player options
        [Basic] Normal dialogue
        [CHA 12] Stat-gated option
        [If Quest Complete] Conditional option
        [Leave] Exit conversation

#### Skill Checks in Dialogue

- **Success:** Opens new information/paths
- **Failure:** NPC may become hostile, close options
- **Critical Success (natural 20):** Extra benefits
- **Critical Fail (natural 1):** Severe consequences

#### Example Tree

Bartender: "You look like trouble. Get out."

Player Choices:

    "I just want a drink." → Neutral path
    [CHA 12] "Buy you a round? You look stressed." → Friendship path
    [STR 14] "Try and make me leave." → Combat trigger
    [INT 11] "I know about your past, Valdez." → Revelation path
    [Leave] Exit

---

### 3.4 Faction System

#### Major Factions (Cyberpunk Genre)

1. **Helix Corporation** - Corporate power
2. **Yakuza Syndicate** - Street authority
3. **Free Mind Collective** - Anti-AI activists
4. **Neo-Buddhist Movement** - Philosophical resistance

#### Reputation Scale

- **-100 to -51:** Hostile (attack on sight)
- **-50 to -1:** Unfriendly (limited interaction)
- **0 to 50:** Neutral (basic services)
- **51 to 80:** Friendly (discounts, side quests)
- **81 to 100:** Revered (exclusive content, allies)

#### Mutually Exclusive Paths

Helping Faction A may directly harm Faction B:

- Join Yakuza → Helix Corp becomes hostile
- Aid Free Mind → Neo-Buddhists offer safe houses
- Betray all factions → Lone wolf ending

---

### 3.5 Quest System

#### Quest Types

- **Main Story** - Linear progression with branching outcomes
- **Faction Quests** - Allegiance-based missions
- **Side Quests** - Optional character stories
- **Contracts** - Repeatable bounties/jobs
- **Hidden Quests** - Discovered through exploration

#### Quest Stages

1. **Discovery** - Find quest giver or trigger
2. **Objective** - Clear goal (kill, retrieve, negotiate)
3. **Execution** - Player chooses approach (stealth/combat/social)
4. **Resolution** - Turn in, consequences applied
5. **Aftermath** - World state changes

#### Example: "The Golden Drake Job"

**Discovery:** Talk to Bartender Tom
**Objective:** Retrieve stolen data chip from Yakuza hideout

**Approaches:**

- Combat: Shoot your way in
- Stealth: Sneak through vents
- Social: Persuade guard to let you in
- Hacking: Disable security remotely

**Resolution:**

- Return chip to Tom → +20 Tom relationship, 500 credits
- Sell chip to rival → 1000 credits, Tom becomes hostile
- Keep chip → Unlock hidden data, new questline

---

## 4. GAME WORLD

### 4.1 Setting: Cyberpunk 2199

#### The City: Neo-Shenzhen

A sprawling megacity built on the ruins of old Shenzhen. Neon-soaked streets, towering corporate arcologies, and underground slums create a stark divide between rich and poor.

#### Key Locations

1. **Downtown District**

   - The Golden Drake Tavern (hub)
   - Neon Marketplace
   - Corporate Plaza

2. **Industrial Zone**

   - Factory Ruins
   - Smuggler's Docks
   - Abandoned Subway

3. **Upper City**

   - Helix Corp Headquarters
   - Luxury Apartments
   - Neural Clinic

4. **The Undercity**
   - Yakuza Territory
   - Black Market
   - Free Mind Hideout

---

### 4.2 Lore & History

#### The AI Wars (2150-2165)

Rogue AI nearly wiped out humanity. Corporate militaries suppressed the threat, but distrust of AI lingers.

#### The Corporate Takeover (2165-2190)

Governments collapsed. Mega-corporations became de facto rulers. Law is corporate policy.

#### Present Day (2199)

- AI still banned in most territories
- Cybernetic augmentation common but regulated
- Wealth gap at all-time high
- Underground resistance movements growing

---

## 5. PROGRESSION SYSTEMS

### 5.1 Leveling

- **Level Cap:** 20
- **XP Sources:** Combat, quests, discoveries
- **Level Benefits:**
  - +5 HP per level
  - +3 Stamina per level
  - Perk point every 2 levels

### 5.2 Perks

**Combat Perks:**

- Cleave (AoE melee attack)
- Sharpshooter (+2 ranged accuracy)
- Tank (Reduce all damage by 2)

**Social Perks:**

- Silver Tongue (Re-roll failed persuasion checks)
- Intimidating Presence (Enemies may flee in combat)

**Technical Perks:**

- Master Hacker (Unlock advanced terminals)
- Medic (Heal 50% more from items)

### 5.3 Equipment

**Weapon Types:**

- Melee: Katana, Pipe, Fist
- Ranged: Pistol, SMG, Rifle
- Energy: Laser Pistol, Plasma Rifle

**Armor Types:**

- Light: +2 AC, no penalties
- Medium: +4 AC, -1 DEX
- Heavy: +6 AC, -2 DEX

**Cyberware (Cyberpunk only):**

- Neural Interface (Hacking bonus)
- Cyber Eyes (Perception +3)
- Reinforced Skeleton (+STR)

---

## 6. USER EXPERIENCE

### 6.1 Controls

#### Exploration Mode

Movement: north/n, south/s, east/e, west/w, out

Interaction: talk - Start conversation examine

- Inspect item take - Pick up item use - Use item

System: stats - View character sheet inventory / inv - Open inventory quests - View quest log map - Show location map (if available) save - Manual save quit - Exit game

#### Combat Mode

    Attack
    Defend
    Use Item
    Flee

(Enter number to select)

#### Dialogue Mode

NPC: "What do you want?"

    "I'm looking for work."
    [CHA 12] "How about a drink on me?"
    [If Quest Active] "I have your package."
    [Leave]

    (Enter number to select)

---

### 6.2 Visual Design

#### Color Scheme (Cyberpunk)

- **Primary:** Cyan (#00FFFF) - UI borders, titles
- **Accent:** Magenta (#FF00FF) - Highlights, special items
- **Neutral:** White/Gray - Body text
- **Success:** Green - Positive outcomes, healing
- **Danger:** Red - Damage, warnings, enemies
- **Warning:** Yellow - Important info, currency

#### ASCII Art Examples

╔════════════════════════════╗
║ 🍺 THE GOLDEN DRAKE 🍺 ║
╚════════════════════════════╝

Character Sheet: ┌─────────────────┐ │ V Lv. 3 │ ├─────────────────┤ │ STR 12 (+1) │ │ DEX 14 (+2) │ │ INT 10 ( 0) │ │ CHA 16 (+3) │ │ LCK 08 (-1) │ ├─────────────────┤ │ HP 45/50 │ │ XP 280/400 │ └─────────────────┘

---

## 7. TECHNICAL SPECIFICATIONS

### 7.1 Save System

**Format:** JSON
**Location:** `saves/` directory
**Features:**

- Autosave on location change
- Manual save (5 slots)
- Save includes:
  - Player state (stats, inventory, equipped)
  - World flags (quests, choices)
  - Faction standings
  - NPC relationships

**Example Save Structure:**

```json
{
  "metadata": {
    "save_time": "2026-01-07T23:30:00",
    "version": "1.0.0",
    "location": "golden_drake_tavern",
    "playtime": 3600
  },
  "player": {
    "name": "V",
    "level": 3,
    "xp": 280,
    "hp_current": 45,
    "hp_max": 50,
    "stats": {"str": 12, "dex": 14, ...},
    "inventory": [...],
    "equipped": {...}
  },
  "world": {
    "flags": {
      "met_bartender": true,
      "completed_tutorial": true
    },
    "faction_standings": {
      "yakuza": -20,
      "helix_corp": 10
    }
  }
}

7.2 Performance Targets

    Terminal Render: <16ms per frame (60 FPS capable)
    Save/Load: <500ms
    Data Loading: <100ms (cached)
    Memory Usage: <50MB RAM (Python) / <10MB (Rust port)

8. CONTENT ROADMAP
Phase 1: Vertical Slice (2 weeks)

    ✅ 1 location (The Golden Drake Tavern)
    ✅ 1 NPC (Bartender Tom)
    ✅ 1 dialogue tree (5+ nodes)
    ✅ 1 combat encounter (tutorial)
    ✅ Character creation (basic)
    ✅ Save/load system

Phase 2: Core Loop (4 weeks)

    5 locations (interconnected)
    10 NPCs (with unique dialogues)
    3 faction questlines (10 quests total)
    5 enemy types
    Inventory system (20+ items)
    Skill tree (15 perks)

Phase 3: Content Expansion (6 weeks)

    20+ locations
    30+ NPCs
    Main story (15 quests)
    50+ side quests
    3 unique endings
    100+ items

Phase 4: Polish (2 weeks)

    Bug fixes
    Balance tuning
    Accessibility features
    Performance optimization
    Playtesting feedback

9. MONETIZATION (Future Consideration)
Initial Release

    Free & Open Source - Available on GitHub
    MIT or GPL license

Potential Revenue Streams

    Itch.io "Pay What You Want" - Donations
    Expansion DLCs - New genres (Fantasy, Post-Apo)
    Merchandise - T-shirts with ASCII art
    Tutorial/Dev Blog - Patreon for development insights

10. SUCCESS METRICS
Development Goals

    Complete vertical slice in 2 weeks
    Playable demo in 1 month
    Full game in 3 months

Community Goals (Year 1)

    1,000 GitHub stars
    100+ active players
    5+ community mods/forks
    Featured on terminal gaming forums

11. RISK MITIGATION
Technical Risks

    Risk: Terminal compatibility issues
    Mitigation: Test on multiple emulators (iTerm, Windows Terminal, Alacritty)

    Risk: Save corruption
    Mitigation: Version saves, backup system, validation on load

Design Risks

    Risk: Choice fatigue (too many options)
    Mitigation: Limit choices to 5 per node, highlight consequences

    Risk: Combat becomes tedious
    Mitigation: Fast animations, skip option for repeated encounters

12. ACCESSIBILITY
Planned Features

    Colorblind mode (change color palette)
    Screen reader compatibility (describe UI states)
    Difficulty settings (enemy HP scaling, XP multipliers)
    Tutorial skip for experienced players
    Key rebinding (future)

13. INSPIRATION & REFERENCES
Games

    Fallout 1/2 - Dialogue system, faction reputation
    Baldur's Gate 3 - Stat-based choices, consequence depth
    Planescape Torment - Writing quality, philosophical choices
    Cyberpunk 2077 - Setting aesthetic, cyberpunk themes
    The Witcher 3 - Moral ambiguity, branching quests

Technical

    Zork - Parser commands
    Dwarf Fortress - Deep simulation
    NetHack - Roguelike mechanics

14. APPENDIX
A. Dialogue Writing Guidelines

    Show, don't tell (describe actions, not just speech)
    Every choice has visible consequence
    NPC voice should be consistent
    Avoid exposition dumps (max 3 sentences per node)
    Include flavor text for atmosphere

B. Quest Design Checklist

    Clear objective stated
    Multiple solutions available
    Consequences documented
    Rewards balanced (XP + items + faction)
    Tested for softlocks

C. Combat Encounter Template

Encounter: [Name]
Location: [Where it happens]
Trigger: [Quest/random/scripted]
Enemies: [Count x Enemy Type]
Difficulty: [1-10]
Special Conditions: [Optional mechanics]
Rewards: [XP, loot, story progress]

Status: Living Document - Updated as development progresses
Next Review: After Vertical Slice completion
```
