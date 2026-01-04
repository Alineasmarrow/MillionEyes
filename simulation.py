"""
Main Simulation Engine for the Narrative Coherence System
"""

import random
from typing import Dict, List, Optional
from models import Character, Relationship
from events import Event, create_event_deck
from constants import (
    CHAOS_THRESHOLD, CHAOS_WARNING_THRESHOLD,
    WITCH_TRINE_MEMBERS, WITCH_TRINE_DYADS
)


class NarrativeSimulation:
    """Main simulation engine for running narrative scenarios"""

    def __init__(self, name: str = "Untitled Scenario"):
        self.name = name
        self.characters: Dict[str, Character] = {}
        self.relationships: List[Relationship] = []
        self.chaos = 0.0
        self.event_deck = create_event_deck()
        self.round_number = 0
        self.event_history = []
        self.log_entries = []

    def add_character(self, name: str, c_self: float = 7.0, special_state: Optional[str] = None):
        """Add a character to the simulation"""
        self.characters[name] = Character(name, c_self, special_state)

    def add_relationship(self, char_a: str, char_b: str, c_dyad: float = 5.0):
        """Add a relationship between two characters"""
        # Check if relationship already exists
        for rel in self.relationships:
            if rel.matches(char_a, char_b):
                print(f"Relationship {char_a}-{char_b} already exists")
                return

        self.relationships.append(Relationship(char_a, char_b, c_dyad))

    def get_character(self, name: str) -> Optional[Character]:
        """Get a character by name"""
        return self.characters.get(name)

    def get_dyad(self, char_a: str, char_b: str) -> Optional[Relationship]:
        """Get a relationship between two characters"""
        for rel in self.relationships:
            if rel.matches(char_a, char_b):
                return rel
        return None

    def get_character_dyads(self, char_name: str) -> List[Relationship]:
        """Get all relationships involving a character"""
        return [rel for rel in self.relationships
                if rel.char_a == char_name or rel.char_b == char_name]

    def modify_character_c_self(self, char_name: str, delta: float, reason: str = "",
                                apply_sacred_coupling: bool = True) -> Dict:
        """Modify a character's C_self value and apply Sacred Dyad Conservation Law"""
        char = self.get_character(char_name)
        if not char:
            return {"error": f"Character {char_name} not found"}

        old_c_self = char.c_self
        change = char.modify_c_self(delta, reason)

        # Check for catastrophic collapse BEFORE applying coupling
        if old_c_self > 0 and char.c_self <= 0 and apply_sacred_coupling:
            self._handle_sacred_collapse(char_name)

        # Apply Sacred Dyad Conservation Law
        if apply_sacred_coupling:
            sacred_echoes = self._apply_sacred_conservation(char_name, delta, reason)
            if sacred_echoes:
                change['sacred_echoes'] = sacred_echoes

        # Chaos amplification for sacred dyad changes
        if apply_sacred_coupling and delta != 0:
            sacred_chaos = self._calculate_sacred_chaos_impact(char_name, delta)
            if sacred_chaos > 0:
                change['sacred_chaos'] = sacred_chaos

        return {
            "type": "character",
            "character": char_name,
            "delta": delta,
            "new_value": char.c_self,
            "new_state": char.get_state(),
            "reason": reason,
            "sacred_echoes": change.get('sacred_echoes', []),
            "sacred_chaos": change.get('sacred_chaos', 0)
        }

    def modify_dyad(self, char_a: str, char_b: str, delta: float, reason: str = "") -> Dict:
        """Modify a dyad's C_dyad value"""
        dyad = self.get_dyad(char_a, char_b)
        if not dyad:
            return {"error": f"Relationship {char_a}-{char_b} not found"}

        change = dyad.modify_c_dyad(delta, reason)

        # Check if the dyad just became sacred
        became_sacred = change.get('became_sacred', False)

        return {
            "type": "dyad",
            "dyad": f"{dyad.char_a}-{dyad.char_b}",
            "delta": delta,
            "new_value": dyad.c_dyad,
            "new_state": dyad.get_state(),
            "reason": reason,
            "became_sacred": became_sacred
        }

    def modify_chaos(self, delta: float, reason: str = ""):
        """Modify the chaos counter"""
        old_chaos = self.chaos
        self.chaos = max(0, self.chaos + delta)

        return {
            "type": "chaos",
            "delta": delta,
            "old_value": old_chaos,
            "new_value": self.chaos,
            "reason": reason
        }

    def _apply_sacred_conservation(self, char_name: str, delta: float, reason: str) -> List[Dict]:
        """
        Apply Sacred Dyad Conservation Law: when a character changes,
        their sacred partner(s) echo the change
        """
        echoes = []

        # Find all sacred dyads involving this character
        sacred_dyads = [rel for rel in self.relationships
                       if rel.is_sacred and (rel.char_a == char_name or rel.char_b == char_name)]

        for dyad in sacred_dyads:
            # Get the partner
            partner_name = dyad.get_sacred_partner(char_name)
            if not partner_name:
                continue

            partner = self.get_character(partner_name)
            if not partner:
                continue

            # Apply the coupling
            echo_delta = delta * dyad.coupling_strength
            echo_reason = f"sacred echo from {char_name}"

            # Modify partner WITHOUT triggering another round of coupling (prevent infinite loop)
            partner.modify_c_self(echo_delta, echo_reason)

            echoes.append({
                "partner": partner_name,
                "delta": echo_delta,
                "new_value": partner.c_self,
                "dyad": f"{dyad.char_a}-{dyad.char_b}"
            })

        return echoes

    def _calculate_sacred_chaos_impact(self, char_name: str, delta: float) -> float:
        """
        Sacred bonds shake reality when they waver.
        Returns additional chaos from sacred dyad changes.
        """
        sacred_dyads = [rel for rel in self.relationships
                       if rel.is_sacred and (rel.char_a == char_name or rel.char_b == char_name)]

        if not sacred_dyads:
            return 0.0

        # Each sacred dyad amplifies chaos
        chaos_impact = len(sacred_dyads) * abs(delta) * 0.5

        # Add the chaos
        if chaos_impact > 0:
            self.chaos += chaos_impact

        return chaos_impact

    def _handle_sacred_collapse(self, collapsed_char: str):
        """
        Catastrophic case: when a sacred partner hits collapse (C_self <= 0),
        their partner(s) suffer grief rupture
        """
        sacred_dyads = [rel for rel in self.relationships
                       if rel.is_sacred and (rel.char_a == collapsed_char or rel.char_b == collapsed_char)]

        for dyad in sacred_dyads:
            partner_name = dyad.get_sacred_partner(collapsed_char)
            if not partner_name:
                continue

            partner = self.get_character(partner_name)
            if not partner:
                continue

            # Grief rupture
            partner.modify_c_self(-2.0, f"💔 Sacred Break: {collapsed_char} falls")

            # Reality buckles
            self.chaos += 4.0

            print(f"\n💔 SACRED BREAK: {collapsed_char} falls, {partner_name} destabilizes!")
            print(f"   → {partner_name} suffers grief rupture (-2.0 C_self)")
            print(f"   → Reality buckles (+4.0 chaos)")

    def calculate_witch_trine_health(self) -> float:
        """Calculate the health of the Witch Trine"""
        trine_dyads = []
        for char_a, char_b in WITCH_TRINE_DYADS:
            dyad = self.get_dyad(char_a, char_b)
            if dyad:
                trine_dyads.append(dyad.c_dyad)

        if not trine_dyads:
            return 0.0

        return sum(trine_dyads) / len(trine_dyads)

    def run_round(self, event: Optional[Event] = None):
        """Run a single round with a random (or specified) event"""
        self.round_number += 1

        # Pick an event if not specified
        if event is None:
            event = random.choice(self.event_deck)

        print(f"\n{'='*80}")
        print(f"ROUND {self.round_number}: {event.name}")
        print(f"{'='*80}")
        print(f"Category: {event.category}")
        print(f"Description: {event.description}")
        print()

        # Apply the event
        result = event.apply(self)

        # Update chaos
        chaos_delta = result.get("chaos", 0)
        if chaos_delta != 0:
            chaos_change = self.modify_chaos(chaos_delta, event.name)
            print(f"Chaos: {chaos_change['old_value']:.1f} → {chaos_change['new_value']:.1f} ({chaos_delta:+.1f})")
            print()

        # Print the log
        for entry in result.get("log", []):
            if "error" in entry:
                print(f"❌ ERROR: {entry['error']}")
            elif "warning" in entry:
                print(f"⚠️  {entry['warning']}")
            elif "note" in entry:
                print(f"   {entry['note']}")
            elif entry.get("type") == "character":
                char = entry["character"]
                delta = entry["delta"]
                new_val = entry["new_value"]
                state = entry["new_state"]
                reason = entry.get("reason", "")
                sacred_echoes = entry.get("sacred_echoes", [])
                sacred_chaos = entry.get("sacred_chaos", 0)

                symbol = "↑" if delta > 0 else "↓"
                print(f"  {symbol} {char}: C_self {delta:+.1f} → {new_val:.1f} [{state}]")
                if reason:
                    print(f"     → {reason}")

                # Display sacred echoes
                if sacred_echoes:
                    for echo in sacred_echoes:
                        echo_symbol = "↑" if echo['delta'] > 0 else "↓"
                        print(f"     ⚡ Sacred echo: {echo['partner']} {echo_symbol} {echo['delta']:+.1f} → {echo['new_value']:.1f}")

                # Display sacred chaos impact
                if sacred_chaos > 0:
                    print(f"     ⚡ Sacred bond shakes reality: +{sacred_chaos:.1f} chaos")

            elif entry.get("type") == "dyad":
                dyad = entry["dyad"]
                delta = entry["delta"]
                new_val = entry["new_value"]
                state = entry["new_state"]
                reason = entry.get("reason", "")
                became_sacred = entry.get("became_sacred", False)

                symbol = "↑" if delta > 0 else "↓"
                print(f"  {symbol} {dyad}: C_dyad {delta:+.1f} → {new_val:.1f} [{state}]")
                if reason:
                    print(f"     → {reason}")

                # Display sacred formation
                if became_sacred:
                    print(f"     ✨ SACRED DYAD FORMED: {dyad} ⚡")

        # Check for warnings
        if self.chaos >= CHAOS_WARNING_THRESHOLD:
            print(f"\n⚠️⚠️⚠️  CHAOS WARNING: {self.chaos:.1f}/{CHAOS_THRESHOLD} - CoR approaching!")

        if self.chaos >= CHAOS_THRESHOLD:
            print(f"\n🔥🔥🔥 CHAOS THRESHOLD REACHED: CoR MANIFESTS 🔥🔥🔥")

        # Store in history
        self.event_history.append({
            "round": self.round_number,
            "event": event,
            "result": result
        })

    def run_scenario(self, num_rounds: int = 10, events: Optional[List[Event]] = None):
        """Run a complete scenario with multiple rounds"""
        print(f"\n🎭 STARTING SCENARIO: {self.name}")
        print(f"Running {num_rounds} rounds...")

        self.print_initial_state()

        for i in range(num_rounds):
            if events and i < len(events):
                self.run_round(events[i])
            else:
                self.run_round()

        self.print_final_state()

    def print_initial_state(self):
        """Print the initial state of all characters and relationships"""
        print(f"\n{'='*80}")
        print("INITIAL STATE")
        print(f"{'='*80}")

        print("\nCHARACTERS:")
        for char_name, char in sorted(self.characters.items()):
            print(f"  {char}")

        print("\nRELATIONSHIPS:")
        for rel in sorted(self.relationships, key=lambda r: (r.char_a, r.char_b)):
            print(f"  {rel}")

        # Check Witch Trine if applicable
        if all(name in self.characters for name in WITCH_TRINE_MEMBERS):
            trine_health = self.calculate_witch_trine_health()
            print(f"\nWITCH TRINE HEALTH: {trine_health:.1f}")

        print(f"\nInitial Chaos: {self.chaos:.1f}")

    def print_final_state(self):
        """Print the final state after all rounds"""
        print(f"\n{'='*80}")
        print("FINAL STATE")
        print(f"{'='*80}")

        print(f"\nTotal Rounds: {self.round_number}")
        print(f"Final Chaos: {self.chaos:.1f}/{CHAOS_THRESHOLD}")

        if self.chaos >= CHAOS_THRESHOLD:
            print("⚠️  CoR HAS MANIFESTED")
        elif self.chaos >= CHAOS_WARNING_THRESHOLD:
            print("⚠️  APPROACHING CoR MANIFESTATION")

        print("\nFINAL CHARACTER STATES:")
        for char_name, char in sorted(self.characters.items()):
            state_symbol = self._get_state_symbol(char.get_state())
            print(f"  {state_symbol} {char}")

        print("\nFINAL RELATIONSHIP STATES:")
        for rel in sorted(self.relationships, key=lambda r: (r.char_a, r.char_b)):
            state_symbol = self._get_dyad_state_symbol(rel.get_state())
            trajectory = rel.get_trajectory()
            sacred_mark = " ⚡ SACRED" if rel.is_sacred else ""
            print(f"  {state_symbol} {rel.char_a}-{rel.char_b}: {rel.c_dyad:.1f} [{rel.get_state()}] {trajectory}{sacred_mark}")

        # Display Sacred Dyads prominently
        sacred_dyads = [rel for rel in self.relationships if rel.is_sacred]
        if sacred_dyads:
            print("\n⚡ SACRED DYADS (Conservation Law Active):")
            for dyad in sacred_dyads:
                print(f"  ⚡ {dyad.char_a} ↔ {dyad.char_b}")
                print(f"     Coupling Strength: {dyad.coupling_strength:.1%}")
                print(f"     C_dyad: {dyad.c_dyad:.1f}")

        # Check Witch Trine if applicable
        if all(name in self.characters for name in WITCH_TRINE_MEMBERS):
            trine_health = self.calculate_witch_trine_health()
            print(f"\nWITCH TRINE HEALTH: {trine_health:.1f}")

            if trine_health >= 8:
                print("  ✓ Trine is STRONG")
            elif trine_health >= 6:
                print("  ~ Trine is FUNCTIONAL")
            else:
                print("  ✗ Trine is FAILING")

        # Print critical warnings
        print("\nCRITICAL WARNINGS:")
        warnings = []

        for char_name, char in self.characters.items():
            if char.c_self <= 3:
                warnings.append(f"  ⚠️  {char_name} in CRISIS state (C_self: {char.c_self:.1f})")
            if char.c_self < 1:
                warnings.append(f"  🔥 {char_name} DISSOLVING (C_self: {char.c_self:.1f})")

        for rel in self.relationships:
            if rel.c_dyad <= 3:
                warnings.append(f"  ⚠️  {rel.char_a}-{rel.char_b} STRAINED (C_dyad: {rel.c_dyad:.1f})")
            if rel.c_dyad <= 1:
                warnings.append(f"  🔥 {rel.char_a}-{rel.char_b} in RUPTURE ZONE (C_dyad: {rel.c_dyad:.1f})")

        if warnings:
            for warning in warnings:
                print(warning)
        else:
            print("  ✓ No critical warnings")

    def _get_state_symbol(self, state: str) -> str:
        """Get a symbol for a character state"""
        state_symbols = {
            "Transcendent": "✨",
            "Stable": "✓",
            "Functional": "~",
            "Strained": "⚠",
            "Crisis": "⚠⚠",
            "Dissolving": "🔥",
            "Gone": "💀"
        }
        return state_symbols.get(state, "•")

    def _get_dyad_state_symbol(self, state: str) -> str:
        """Get a symbol for a relationship state"""
        state_symbols = {
            "MYTHIC": "✨✨",
            "SACRED": "✨",
            "Strong": "✓",
            "Functional": "~",
            "STRAINED": "⚠",
            "RUPTURE ZONE": "🔥",
            "SEVERED": "💀"
        }
        return state_symbols.get(state, "•")

    def save_log(self, filename: str):
        """Save the simulation log to a file"""
        with open(filename, 'w') as f:
            f.write(f"SIMULATION LOG: {self.name}\n")
            f.write(f"{'='*80}\n\n")

            for entry in self.event_history:
                round_num = entry["round"]
                event = entry["event"]
                result = entry["result"]

                f.write(f"ROUND {round_num}: {event.name}\n")
                f.write(f"Chaos: {result.get('chaos', 0):+.1f}\n")

                for log_entry in result.get("log", []):
                    if "note" in log_entry:
                        f.write(f"  {log_entry['note']}\n")
                    elif log_entry.get("type") == "character":
                        char = log_entry["character"]
                        delta = log_entry["delta"]
                        new_val = log_entry["new_value"]
                        f.write(f"  {char}: {delta:+.1f} → {new_val:.1f}\n")
                    elif log_entry.get("type") == "dyad":
                        dyad = log_entry["dyad"]
                        delta = log_entry["delta"]
                        new_val = log_entry["new_value"]
                        f.write(f"  {dyad}: {delta:+.1f} → {new_val:.1f}\n")

                f.write("\n")

        print(f"\n✓ Log saved to {filename}")
