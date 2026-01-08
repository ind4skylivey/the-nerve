"""
Data Loader - Load and cache JSON game content
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional


class DataLoader:
    """
    Loads game content from JSON files with caching

    Example:
        loader = DataLoader(Path("data"))
        location = loader.load_location("cyberpunk", "golden_drake_tavern")
    """

    def __init__(self, data_dir: Path):
        """
        Initialize data loader

        Args:
            data_dir: Root data directory (e.g., Path("data"))
        """
        self.data_dir = data_dir
        self._cache: Dict[str, Any] = {}

    def _load_json(self, file_path: Path) -> dict:
        """
        Load JSON file with caching

        Args:
            file_path: Path to JSON file

        Returns:
            Parsed JSON data

        Raises:
            FileNotFoundError: If file doesn't exist
            json.JSONDecodeError: If JSON is invalid
        """
        cache_key = str(file_path)

        # Check cache first
        if cache_key in self._cache:
            return self._cache[cache_key]

        # Load from disk
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Store in cache
        self._cache[cache_key] = data
        return data

    def load_location(self, genre: str, location_id: str) -> dict:
        """
        Load location data

        Args:
            genre: Genre folder (e.g., "cyberpunk")
            location_id: Location ID (matches filename without .json)

        Returns:
            Location data dict

        Example:
            location = loader.load_location("cyberpunk", "golden_drake_tavern")
            print(location['name'])  # "The Golden Drake"
        """
        file_path = self.data_dir / "genres" / genre / "locations" / f"{location_id}.json"
        return self._load_json(file_path)

    def load_npc(self, genre: str, npc_id: str) -> dict:
        """
        Load NPC data

        Args:
            genre: Genre folder
            npc_id: NPC ID

        Returns:
            NPC data dict
        """
        file_path = self.data_dir / "genres" / genre / "npcs" / f"{npc_id}.json"
        return self._load_json(file_path)

    def load_dialogue_tree(self, genre: str, dialogue_id: str) -> dict:
        """
        Load dialogue tree data

        Args:
            genre: Genre folder
            dialogue_id: Dialogue tree ID

        Returns:
            Dialogue tree data dict
        """
        file_path = self.data_dir / "genres" / genre / "dialogues" / f"{dialogue_id}.json"
        return self._load_json(file_path)

    def load_enemy(self, genre: str, enemy_id: str) -> dict:
        """
        Load enemy data

        Args:
            genre: Genre folder
            enemy_id: Enemy ID

        Returns:
            Enemy data dict
        """
        file_path = self.data_dir / "genres" / genre / "enemies" / f"{enemy_id}.json"
        return self._load_json(file_path)

    def load_item(self, genre: str, item_id: str) -> dict:
        """
        Load item data

        Args:
            genre: Genre folder
            item_id: Item ID

        Returns:
            Item data dict
        """
        file_path = self.data_dir / "genres" / genre / "items" / f"{item_id}.json"
        return self._load_json(file_path)

    def load_factions(self, genre: str) -> dict:
        """
        Load faction data

        Args:
            genre: Genre folder

        Returns:
            Factions data dict
        """
        file_path = self.data_dir / "genres" / genre / "factions.json"
        return self._load_json(file_path)

    def clear_cache(self):
        """Clear all cached data (useful for hot-reloading in dev)"""
        self._cache.clear()

    def get_cache_stats(self) -> dict:
        """
        Get cache statistics

        Returns:
            Dict with cache info
        """
        return {
            "cached_files": len(self._cache),
            "cache_keys": list(self._cache.keys())
        }
