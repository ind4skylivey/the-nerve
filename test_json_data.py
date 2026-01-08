#!/usr/bin/env python3
"""
Test script to validate all JSON data files
"""

from pathlib import Path
from src.data.loader import DataLoader

def main():
    """Test loading all JSON files"""
    print("=" * 60)
    print("📦 JSON DATA VALIDATION TEST")
    print("=" * 60)
    print()

    loader = DataLoader(Path("data"))

    # Test location
    try:
        print("📍 Testing location loading...")
        location = loader.load_location("cyberpunk", "golden_drake_tavern")
        print(f"   ✅ Loaded location: {location['name']}")
        print(f"      - Type: {location['type']}")
        print(f"      - Exits: {len(location['exits'])}")
        print(f"      - NPCs: {len(location['npcs'])}")
        print(f"      - Objects: {len(location['objects'])}")
        print()
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print()

    # Test NPC
    try:
        print("👤 Testing NPC loading...")
        npc = loader.load_npc("cyberpunk", "bartender_tom")
        print(f"   ✅ Loaded NPC: {npc['name']}")
        print(f"      - Title: {npc['title']}")
        print(f"      - Level: {npc['stats']['level']}")
        print(f"      - Is Merchant: {npc['merchant_data']['is_merchant']}")
        print()
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print()

    # Test dialogue
    try:
        print("💬 Testing dialogue tree loading...")
        dialogue = loader.load_dialogue_tree("cyberpunk", "dialogue_bartender_intro")
        print(f"   ✅ Loaded dialogue: {dialogue['title']}")
        print(f"      - Speaker: {dialogue['speaker_npc_id']}")
        print(f"      - Nodes: {len(dialogue.get('nodes', []))}")
        if len(dialogue.get('nodes', [])) == 0:
            print(f"      ⚠️  WARNING: Dialogue tree has no nodes (placeholder)")
        print()
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print()

    # Test enemy
    try:
        print("⚔️  Testing enemy loading...")
        enemy = loader.load_enemy("cyberpunk", "street_thug_tutorial")
        print(f"   ✅ Loaded enemy: {enemy['name']}")
        print(f"      - Type: {enemy['type']}")
        print(f"      - Level: {enemy['stats']['level']}")
        print(f"      - HP: {enemy['stats']['hp_max']}")
        print(f"      - Is Tutorial: {enemy['tutorial_notes']['is_tutorial_enemy']}")
        print()
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print()

    # Test items
    try:
        print("🎒 Testing item loading...")

        # Medkit
        medkit = loader.load_item("cyberpunk", "medkit_basic")
        print(f"   ✅ Loaded item: {medkit['name']}")
        print(f"      - Type: {medkit['type']}")
        print(f"      - Effect: {medkit['effect']['effect_description']}")

        # Credits
        credits = loader.load_item("cyberpunk", "credits_50")
        print(f"   ✅ Loaded item: {credits['name']}")
        print(f"      - Value: {credits['stats']['value']}¢")

        # Whiskey
        whiskey = loader.load_item("cyberpunk", "synth_whiskey")
        print(f"   ✅ Loaded item: {whiskey['name']}")
        print(f"      - Effect: {whiskey['effect']['effect_description']}")
        print()
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print()

    # Test factions (optional)
    try:
        print("🏛️  Testing factions loading...")
        factions = loader.load_factions("cyberpunk")
        print(f"   ✅ Loaded factions: {len(factions.get('factions', []))} factions")
        print()
    except FileNotFoundError:
        print(f"   ⚠️  Factions file not found (not created yet)")
        print()
    except Exception as e:
        print(f"   ❌ FAILED: {e}")
        print()

    # Cache stats
    print("📊 Cache Statistics:")
    stats = loader.get_cache_stats()
    print(f"   - Cached files: {stats['cached_files']}")
    print()

    print("=" * 60)
    print("✅ VALIDATION COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    main()
