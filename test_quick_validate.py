from pathlib import Path
from src.data.loader import DataLoader

loader = DataLoader(Path("data"))

# Test location
location = loader.load_location("cyberpunk", "golden_drake_tavern")
print(f"✅ Loaded location: {location['name']}")

# Test NPC
npc = loader.load_npc("cyberpunk", "bartender_tom")
print(f"✅ Loaded NPC: {npc['name']}")

# Test dialogue
dialogue = loader.load_dialogue_tree("cyberpunk", "dialogue_bartender_intro")
print(f"✅ Loaded dialogue: {dialogue['title']}")

# Test enemy
enemy = loader.load_enemy("cyberpunk", "street_thug_tutorial")
print(f"✅ Loaded enemy: {enemy['name']}")

# Test items
medkit = loader.load_item("cyberpunk", "medkit_basic")
print(f"✅ Loaded item: {medkit['name']}")

print("\n🎉 All JSON files validated successfully!")
