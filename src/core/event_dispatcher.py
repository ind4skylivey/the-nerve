"""
Event System - Decoupled communication between game systems
"""

from typing import Callable, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class EventType(Enum):
    """All possible game events"""

    # Player actions
    PLAYER_MOVED = "player_moved"
    PLAYER_DIALOGUE_CHOICE = "player_dialogue_choice"
    PLAYER_COMBAT_ACTION = "player_combat_action"
    PLAYER_ITEM_USED = "player_item_used"
    PLAYER_LEVEL_UP = "player_level_up"

    # World events
    LOCATION_ENTERED = "location_entered"
    LOCATION_EXITED = "location_exited"
    NPC_SPAWNED = "npc_spawned"
    QUEST_UPDATED = "quest_updated"
    FLAG_SET = "flag_set"

    # Combat events
    COMBAT_STARTED = "combat_started"
    COMBAT_ENDED = "combat_ended"
    DAMAGE_DEALT = "damage_dealt"
    ENTITY_DIED = "entity_died"

    # Dialogue events
    DIALOGUE_STARTED = "dialogue_started"
    DIALOGUE_ENDED = "dialogue_ended"
    DIALOGUE_CHOICE_MADE = "dialogue_choice_made"

    # System events
    SAVE_TRIGGERED = "save_triggered"
    LOAD_TRIGGERED = "load_triggered"
    GAME_OVER = "game_over"


@dataclass
class Event:
    """Event data container"""
    type: EventType
    data: dict


class EventDispatcher:
    """
    Central event bus - allows systems to communicate without tight coupling

    Example usage:
        # System A publishes event
        game_events.publish(Event(EventType.COMBAT_STARTED, {"enemy_count": 3}))

        # System B subscribes to event
        def on_combat_start(event: Event):
            print(f"Combat started with {event.data['enemy_count']} enemies!")

        game_events.subscribe(EventType.COMBAT_STARTED, on_combat_start)
    """

    def __init__(self):
        self._listeners: Dict[EventType, List[Callable]] = {}
        self._event_history: List[Event] = []  # For debugging

    def subscribe(self, event_type: EventType, callback: Callable):
        """
        Register a listener for an event type

        Args:
            event_type: Type of event to listen for
            callback: Function to call when event fires (receives Event object)
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)

    def unsubscribe(self, event_type: EventType, callback: Callable):
        """Remove a listener"""
        if event_type in self._listeners:
            try:
                self._listeners[event_type].remove(callback)
            except ValueError:
                pass  # Callback wasn't subscribed

    def publish(self, event: Event):
        """
        Fire an event - notify all listeners

        Args:
            event: Event object to publish
        """
        # Record in history
        self._event_history.append(event)

        # Notify listeners
        if event.type in self._listeners:
            for callback in self._listeners[event.type]:
                try:
                    callback(event)
                except Exception as e:
                    print(f"⚠️  Error in event listener for {event.type}: {e}")

    def clear_listeners(self, event_type: Optional[EventType] = None):
        """Clear all listeners (or for specific type)"""
        if event_type:
            self._listeners[event_type] = []
        else:
            self._listeners.clear()

    def get_event_history(self, event_type: Optional[EventType] = None) -> List[Event]:
        """Get event history (for debugging)"""
        if event_type:
            return [e for e in self._event_history if e.type == event_type]
        return self._event_history.copy()


# Global singleton instance
game_events = EventDispatcher()
