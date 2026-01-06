"""
Act System - Event Deck Organization

Organizes events into acts and manages transitions between narrative phases.
"""

from typing import List, Dict
from events import Event


class ActSystem:
    """Manages the act structure and event deck selection"""

    def __init__(self):
        self.current_act = 1
        self.rounds_per_act = {
            1: 10,   # Act 1 = rounds 1–10
            2: 15,   # Act 2 = rounds 11–25
            3: 10    # Act 3 placeholder
        }

    def get_current_act(self, round_num: int) -> int:
        """Determine which act we're in based on round number"""
        if round_num <= 10:
            return 1
        elif round_num <= 25:
            return 2
        else:
            return 3

    def get_available_deck(self, act: int) -> List[Event]:
        """Get the event deck for a specific act"""
        return ACT_EVENT_POOLS.get(act, [])

    def get_act_banner(self, act: int) -> Dict[str, str]:
        """Get the banner display for an act"""
        return ACT_BANNERS.get(act, {})


# Act banner information
ACT_BANNERS = {
    1: {
        "title": "ACT I: MISLEADING CALM",
        "tagline": "Things seem manageable... for now.",
        "symbol": "🌅"
    },
    2: {
        "title": "ACT II: ESCALATION",
        "tagline": "The world begins to crack.",
        "symbol": "⚡"
    },
    3: {
        "title": "ACT III: COLLAPSE OR TRANSCENDENCE",
        "tagline": "Everything comes to a head.",
        "symbol": "🔥"
    }
}


# Event pools will be populated with event instances
# This will be built when the simulation initializes by parsing act_data.json
ACT_EVENT_POOLS: Dict[int, List[Event]] = {
    1: [],  # Act I events
    2: [],  # Act II events
    3: []   # Act III events (placeholder)
}


def display_act_banner(act: int):
    """Display the banner for a new act"""
    banner = ACT_BANNERS.get(act)
    if not banner:
        return

    print("\n" + "=" * 80)
    print(f"{banner['symbol']} {banner['title']} {banner['symbol']}")
    print("=" * 80)
    print(f"  {banner['tagline']}")
    print("=" * 80)
    print()
