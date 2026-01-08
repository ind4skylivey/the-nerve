"""
Save/Load System - JSON-based persistence
"""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime


class SaveManager:
    """Handles game save and load operations"""

    def __init__(self, saves_dir: str = "saves"):
        self.saves_dir = Path(saves_dir)
        self.saves_dir.mkdir(exist_ok=True)
        self.autosave_path = self.saves_dir / "autosave.json"

    def save_game(self, game_state: 'GameState', slot_name: str = "slot_1") -> bool:
        """
        Save game state to file

        Args:
            game_state: Current game state
            slot_name: Save slot name (e.g., "slot_1", "slot_2")

        Returns:
            True if save successful
        """
        try:
            save_path = self.saves_dir / f"{slot_name}.json"

            save_data = {
                "metadata": {
                    "save_time": datetime.now().isoformat(),
                    "version": game_state.save_version,
                    "location": game_state.current_location_id,
                    "playtime": game_state.playtime_seconds,
                },
                "game_state": game_state.to_dict(),
                "player": game_state.player.to_dict() if game_state.player else None,
            }

            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Game saved to {slot_name}")
            return True

        except Exception as e:
            print(f"❌ Save failed: {e}")
            return False

    def load_game(self, slot_name: str = "slot_1") -> Optional['GameState']:
        """
        Load game state from file

        Args:
            slot_name: Save slot to load

        Returns:
            Loaded GameState or None if failed
        """
        try:
            save_path = self.saves_dir / f"{slot_name}.json"

            if not save_path.exists():
                print(f"❌ Save file not found: {slot_name}")
                return None

            with open(save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)

            # Validate version
            if save_data["metadata"]["version"] != "1.0.0":
                print("⚠️  Save file version mismatch - may have issues")

            # Reconstruct game state
            from .game_state import GameState
            game_state = GameState.from_dict(save_data["game_state"])

            # Reconstruct player
            if save_data["player"]:
                from src.entities.player import Player
                game_state.player = Player.from_dict(save_data["player"])

            print(f"✅ Game loaded from {slot_name}")
            return game_state

        except Exception as e:
            print(f"❌ Load failed: {e}")
            return None

    def autosave(self, game_state: 'GameState') -> bool:
        """Quick autosave to dedicated slot"""
        return self.save_game(game_state, "autosave")

    def list_saves(self) -> list[dict]:
        """
        List all available save files with metadata

        Returns:
            List of save info dicts
        """
        saves = []

        for save_file in self.saves_dir.glob("*.json"):
            try:
                with open(save_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                saves.append({
                    "slot_name": save_file.stem,
                    "save_time": data["metadata"]["save_time"],
                    "location": data["metadata"]["location"],
                    "playtime": data["metadata"]["playtime"],
                })
            except Exception:
                continue

        return sorted(saves, key=lambda x: x["save_time"], reverse=True)
