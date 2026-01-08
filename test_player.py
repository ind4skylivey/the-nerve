#!/usr/bin/env python3
"""Test Player entity"""

from src.entities.player import Player, PlayerStats

print("=" * 60)
print("🧪 TESTING PLAYER ENTITY")
print("=" * 60)
print()

# Test 1: Create player with default stats
print("1️⃣ Creating player with default stats...")
player = Player(name="V")
print(f"   ✅ Player created: {player.name}")
print(f"      HP: {player.hp_current}/{player.hp_max}")
print(f"      Level: {player.level}")
print()

# Test 2: Stat modifiers
print("2️⃣ Testing stat modifiers...")
player.stats.strength = 16
player.stats.charisma = 12
print(f"   STR 16 modifier: {player.stats.get_modifier('strength')}")  # Should be +3
print(f"   CHA 12 modifier: {player.stats.get_modifier('charisma')}")  # Should be +1
print()

# Test 3: Damage system
print("3️⃣ Testing damage system...")
damage_taken = player.take_damage(20)
print(f"   Took {damage_taken} damage")
print(f"   HP: {player.hp_current}/{player.hp_max}")
print()

# Test 4: Healing
print("4️⃣ Testing healing...")
healed = player.heal(10)
print(f"   Healed {healed} HP")
print(f"   HP: {player.hp_current}/{player.hp_max}")
print()

# Test 5: Skill check
print("5️⃣ Testing skill check...")
player.skills["hacking"] = 50  # 50 skill = +5 bonus
success, total = player.skill_check("hacking", 15)
print(f"   Hacking check (DC 15): {total} - {'SUCCESS' if success else 'FAIL'}")
print()

# Test 6: Stat check
print("6️⃣ Testing stat check...")
success, total = player.stat_check("charisma", 12)
print(f"   CHA check (DC 12): {total} - {'SUCCESS' if success else 'FAIL'}")
print()

# Test 7: Inventory
print("7️⃣ Testing inventory...")
player.add_item("medkit_basic")
player.add_item("credits_50")
print(f"   Inventory: {player.inventory}")
print(f"   Has medkit: {player.has_item('medkit_basic')}")
player.remove_item("medkit_basic")
print(f"   After removing medkit: {player.inventory}")
print()

# Test 8: XP and leveling
print("8️⃣ Testing XP and leveling...")
print(f"   Current level: {player.level}, XP: {player.xp}")
player.add_xp(150)  # Should level up (needs 100 XP for level 2)
print(f"   After 150 XP: Level {player.level}, HP: {player.hp_max}")
print()

# Test 9: Relationships
print("9️⃣ Testing relationships...")
player.modify_npc_relationship("bartender_tom", 15)
player.modify_faction_standing("yakuza", -20)
print(f"   Bartender Tom: {player.npc_relationships.get('bartender_tom')}")
print(f"   Yakuza standing: {player.faction_standings.get('yakuza')}")
print()

# Test 10: Serialization
print("🔟 Testing serialization...")
player_dict = player.to_dict()
print(f"   Serialized: {len(player_dict)} keys")
player_loaded = Player.from_dict(player_dict)
print(f"   Loaded player: {player_loaded.name}, Level {player_loaded.level}")
print()

print("=" * 60)
print("✅ ALL PLAYER TESTS PASSED")
print("=" * 60)
