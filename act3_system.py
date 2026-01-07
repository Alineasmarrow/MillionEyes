"""
Act 3 System - Conditional Events, Endings, and Special Mechanics

Manages:
- Ending path unlocks
- Special flags and tags
- Conditional event triggers
- Farris entity and modes
- Ending calculation
"""

import json
import os
from typing import Dict, List, Optional, Any


class FarrisEntity:
    """
    Farris - The voice archetype mirror that influences endings

    Mirrors Maeve's coherence with modifications based on player archetype choices
    """

    def __init__(self):
        self.mode = "witness"  # Changes with player choice archetype
        self.coherence = 0.0

    def update_from_choice(self, archetype_chosen: str):
        """Update Farris' mode based on player's archetype choice"""
        self.mode = archetype_chosen

    def get_coherence(self, maeve_c_self: float) -> float:
        """Calculate Farris coherence from Maeve's with modifier"""
        modifier = {
            "witness": +1.0,
            "trickster": 0.0,
            "devourer": -1.0
        }
        return max(0, min(10, maeve_c_self + modifier.get(self.mode, 0)))

    def apply_mode_effects(self, simulation):
        """Apply Farris mode effects to simulation"""
        if self.mode == "witness":
            # Witness mode stabilizes
            simulation.modify_chaos(-0.5, "Farris: Witness Mode stability")

        elif self.mode == "trickster":
            # Trickster mode reroutes chaos
            simulation.special_flags["reroute_available"] = True

        elif self.mode == "devourer":
            # Devourer mode absorbs harm from Maeve
            # This is handled in event processing
            pass


class Act3System:
    """
    Manages Act 3 conditional events, special flags, and ending paths
    """

    def __init__(self):
        # Ending paths that can be unlocked
        self.ending_paths_unlocked = {
            "miracle": False,
            "disappearance": False,
            "redchurch": False,
            "cor_manifestation": False
        }

        # Special flags affecting mechanics
        self.special_flags = {
            "obsession": False,
            "desperate_protector_mode": False,
            "trine_severed": False,
            "dce_path_unlocked": False,
            "true_insight_unlocked": False,
            "seeress_owes_debt": False,
            "redchurch_burned": False
        }

        # Temporary buffs that expire
        self.temp_buffs = []

        # Pressure and tracking modifiers
        self.pressure_baseline = 0.0
        self.dce_pressure = 0
        self.dce_tracking = 0

        # Ending weight modifiers
        self.ending_weights_modifier = {
            "miracle": 0,
            "disappearance": 0,
            "redchurch": 0,
            "cor_manifestation": 0
        }

    def check_event_triggers(self, event: Dict, characters: Dict, dyads: List) -> bool:
        """
        Check if event's trigger conditions are met

        Returns True if event should be available in pool
        """
        triggers = event.get("triggers", {})

        if not triggers:
            return True  # No triggers = always available

        # Check character coherence triggers
        if "yuul_coherence_below" in triggers:
            yuul = characters.get("Yuul")
            if not yuul or yuul.c_self >= triggers["yuul_coherence_below"]:
                return False

        if "maeve_coherence_below" in triggers:
            maeve = characters.get("Maeve")
            if not maeve or maeve.c_self >= triggers["maeve_coherence_below"]:
                return False

        if "kit_coherence_below" in triggers:
            kit = characters.get("Kit")
            if not kit or kit.c_self >= triggers["kit_coherence_below"]:
                return False

        if "maeve_coherence_min" in triggers:
            maeve = characters.get("Maeve")
            if not maeve or maeve.c_self < triggers["maeve_coherence_min"]:
                return False

        # Check dyad triggers
        if "kit_yuul_dyad_min" in triggers:
            # Find Kit-Yuul dyad
            kit_yuul = None
            for dyad in dyads:
                if dyad.matches("Kit", "Yuul"):
                    kit_yuul = dyad
                    break

            if not kit_yuul or kit_yuul.c_dyad < triggers["kit_yuul_dyad_min"]:
                return False

        # Check tag requirements
        if "requires_tag" in triggers:
            required_tag = triggers["requires_tag"]
            if not self.special_flags.get(required_tag, False):
                return False

        return True  # All conditions met

    def apply_special_effects(self, effects: Dict, simulation):
        """Apply special effects from events and choices"""

        # Tag additions
        if "add_tag" in effects:
            tag = effects["add_tag"]
            self.special_flags[tag] = True
            print(f"   🏷️ Tag added: {tag}")

        # Mode activations
        if "enable_desperate_protector_mode" in effects and effects["enable_desperate_protector_mode"]:
            self.special_flags["desperate_protector_mode"] = True
            print(f"   ⚔️ Kit enters Desperate Protector Mode")

        # Ending path unlocks
        if "unlock_miracle_path" in effects and effects["unlock_miracle_path"]:
            self.ending_paths_unlocked["miracle"] = True
            print(f"   ✨ MIRACLE ENDING PATH UNLOCKED")

        if "lock_disappearance_path" in effects and effects["lock_disappearance_path"]:
            self.ending_paths_unlocked["disappearance"] = False
            print(f"   🔒 Disappearance path locked")

        # Pressure modifications
        if "pressure_baseline_increase" in effects:
            increase = effects["pressure_baseline_increase"]
            self.pressure_baseline += increase
            print(f"   📈 Pressure baseline +{increase}")

        # DCE tracking
        if "dce_pressure" in effects:
            self.dce_pressure += effects["dce_pressure"]
        if "dce_tracking" in effects:
            self.dce_tracking += effects["dce_tracking"]

        # Ending weight modifiers
        if "miracle_weight" in effects:
            self.ending_weights_modifier["miracle"] += effects["miracle_weight"]
        if "fate_weight_disappearance" in effects:
            self.ending_weights_modifier["disappearance"] += effects["fate_weight_disappearance"]
        if "increase_redchurch_and_cor_weight" in effects:
            self.ending_weights_modifier["redchurch"] += 2
            self.ending_weights_modifier["cor_manifestation"] += 2

    def calculate_ending(self, simulation, farris: FarrisEntity) -> tuple:
        """
        Calculate which ending based on game state

        Returns: (ending_name, all_weights_dict)
        """
        characters = simulation.characters
        chaos_total = simulation.chaos
        pressure_ratio = simulation.chaos_state.pressure / max(simulation.chaos_state.turbulence, 0.1)

        # Get character final states
        yuul = characters.get("Yuul")
        kit = characters.get("Kit")
        maeve = characters.get("Maeve")
        rielle = characters.get("Rielle")

        yuul_final = yuul.c_self if yuul else 0
        kit_final = kit.c_self if kit else 0
        maeve_final = maeve.c_self if maeve else 0
        rielle_final = rielle.c_self if rielle else 0

        # Initialize ending weights
        endings = {
            "miracle": 0,
            "disappearance": 0,
            "redchurch": 0,
            "cor_manifestation": 0
        }

        # Apply base modifiers
        for ending, modifier in self.ending_weights_modifier.items():
            endings[ending] += modifier

        # MIRACLE ENDING
        if self.ending_paths_unlocked["miracle"]:
            endings["miracle"] += 30

        if maeve_final >= 7 and self.special_flags.get("obsession"):
            endings["miracle"] += 20  # True Insight achieved

        all_alive = all(c.c_self >= 6 for c in characters.values())
        if all_alive:
            endings["miracle"] += 15  # Everyone survived intact

        if farris.mode == "witness":
            endings["miracle"] += 10

        # DISAPPEARANCE ENDING
        if self.ending_paths_unlocked.get("disappearance", True):  # Default available
            if yuul_final == 0:
                endings["disappearance"] += 25  # Yuul dissolved

            if yuul_final <= 1:
                endings["disappearance"] += 15

        kit_yuul_dyad = simulation.get_dyad("Kit", "Yuul")
        if kit_yuul_dyad and kit_final >= 7 and kit_yuul_dyad.c_dyad >= 9:
            endings["disappearance"] += 20  # Sacred bond held

        if farris.mode == "trickster":
            endings["disappearance"] += 10

        # REDCHURCH TRAGEDY (Canon)
        if yuul_final <= 2 and kit_final <= 5:
            endings["redchurch"] += 30

        if self.special_flags.get("trine_severed"):
            endings["redchurch"] += 20

        if maeve_final <= 4:
            endings["redchurch"] += 15  # Obsession consumed her

        if farris.mode == "devourer":
            endings["redchurch"] += 10

        # COR MANIFESTATION
        if chaos_total >= 25:
            endings["cor_manifestation"] += 30

        if pressure_ratio > 2.0:
            endings["cor_manifestation"] += 20  # Pressure-dominant

        if any(getattr(c, 'marked_by_list', False) for c in characters.values()):
            endings["cor_manifestation"] += 15

        # Select ending with highest weight
        final_ending = max(endings, key=endings.get)

        return final_ending, endings


# Ending narratives
ENDING_NARRATIVES = {
    "miracle": {
        "title": "THE MIRACLE",
        "description": """
Maeve saw it. The real pattern. The List feeds on extremes-
dissolution AND ascension. She understood: don't let anyone
reach 0 or 10. Hold the middle. Survive through balance.

She pulled Yuul back from the edge. Kit stayed whole.
The Trine held. Barely. Scarred. But intact.

They walked away from Redchurch. All of them.

The world doesn't remember this timeline. But they do.
        """,
        "survivors": ["Maeve", "Kit", "Yuul", "Rielle"]
    },

    "disappearance": {
        "title": "THE DISAPPEARANCE",
        "description": """
Yuul stood at the mirror. The Seeress danced. They synchronized.

But this time, Kit was there. Watching. Understanding.

"I see you," he said. Not "come back." Just: "I see you."

Yuul smiled. Then stepped through.

Not dead. Not dissolved. **Gone.** To a place Kit couldn't follow.

He carries her memory. The Seeress took her body.
Her name remains in his chest like a second heartbeat.
        """,
        "survivors": ["Maeve", "Kit", "Rielle"],
        "transformed": ["Yuul"]
    },

    "redchurch": {
        "title": "THE REDCHURCH INCIDENT",
        "description": """
They burned. Kit died reaching. Yuul became the wound.
Maeve survived to carry the guilt.

Rielle found them too late.

The world marked it down as a resonance accident.
Nine casualties. Cause: unknown.

But those who remain know the truth:
Love without understanding. Courage without wisdom.
Good intentions paving the road to Redchurch.

Kit's last words: "Stay with me."
Yuul couldn't. The Seeress wouldn't allow it.
        """,
        "dead": ["Kit", "Yuul", "6 H11 agents"],
        "survivors": ["Maeve", "Rielle"]
    },

    "cor_manifestation": {
        "title": "THE CHILDREN RETURN",
        "description": """
The chaos exceeded threshold. The pressure broke the field.

The Children of Resonance didn't just manifest.
They **rewrote** recent events.

"That stabilization in Round 12? It was a lie. Roll it back."

They offered perfect coherence. C=1.0 for everyone.
No more pain. No more fear. Just... sameness.

Some accepted. Some refused.

Those who refused are still running.
Those who accepted are still smiling.

Neither group remembers what they used to be.
        """,
        "status": "SYSTEM CORRUPTED"
    }
}
