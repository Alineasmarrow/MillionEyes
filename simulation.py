"""
Main Simulation Engine for the Narrative Coherence System
"""

import json
import random
from typing import Any, Dict, List, Optional
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
        self.choice_prompts = self._load_choice_prompts()
        self.deck_weights = {event.id: 1.0 for event in self.event_deck}
        self.deck_mutated = False
        self.archetype_counts = {"Witness": 0, "Trickster": 0, "Devourer": 0}
        self.pressure_bias = 0
        self.log = []
        self._pending_choice_log = []
        self._pending_choice_summary = []
        self.witness_choice_count = 0
        self.trickster_choice_count = 0
        self.devourer_choice_count = 0
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

    def modify_character_c_self(
        self,
        char_name: str,
        delta: float,
        reason: str = "",
        apply_sacred: bool = True,
        apply_chaos: bool = True
    ) -> List[Dict]:
        """Modify a character's C_self value"""
        char = self.get_character(char_name)
        if not char:
            return [{"error": f"Character {char_name} not found"}]

        effective_delta = delta
        if delta > 0:
            effective_delta = delta * max(0.2, (1 - 0.1 * char.scars))

        char.modify_c_self(effective_delta, reason)
        if char.c_self < 3:
            char.scars += 1
            char.chaos_sensitivity += 0.1
        log_entries = [{
            "type": "character",
            "character": char_name,
            "delta": effective_delta,
            "new_value": char.c_self,
            "new_state": char.get_state(),
            "reason": reason
        }]

        if apply_sacred:
            log_entries.extend(self._apply_sacred_effects(char_name, effective_delta, apply_chaos))

        return log_entries

    def modify_dyad(
        self,
        char_a: str,
        char_b: str,
        delta: float,
        reason: str = "",
        target: Optional[str] = None
    ) -> List[Dict]:
        """Modify a dyad's C_dyad value"""
        dyad = self.get_dyad(char_a, char_b)
        if not dyad:
            return [{"error": f"Relationship {char_a}-{char_b} not found"}]

        if abs(delta) >= 2:
            dyad.dyad_scars += 1

        effective_delta = delta
        if delta > 0:
            effective_delta = delta * max(0.3, (1 - 0.15 * dyad.dyad_scars))

        was_sacred = dyad.is_sacred
        if target == "A_to_B":
            dyad.modify_c_dyad(
                effective_delta,
                reason,
                from_name=char_a,
                to_name=char_b,
                symmetric=False
            )
        elif target == "B_to_A":
            dyad.modify_c_dyad(
                effective_delta,
                reason,
                from_name=char_b,
                to_name=char_a,
                symmetric=False
            )
        else:
            dyad.modify_c_dyad(effective_delta, reason, symmetric=True)

        log_entries = [{
            "type": "dyad",
            "dyad": f"{dyad.char_a}-{dyad.char_b}",
            "delta": effective_delta,
            "new_value": dyad.c_dyad,
            "new_state": dyad.get_state(),
            "reason": reason
        }]

        if dyad.is_sacred and not was_sacred:
            log_entries.append({"note": f"✨ Sacred Dyad Formed: {dyad.char_a} ↔ {dyad.char_b}"})

        return log_entries

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

    def _apply_sacred_effects(self, char_name: str, delta: float, apply_chaos: bool) -> List[Dict]:
        log_entries = []
        if delta == 0:
            return log_entries

        for dyad in self.get_character_dyads(char_name):
            if not dyad.is_sacred:
                continue

            other_char_name = dyad.char_b if dyad.char_a == char_name else dyad.char_a
            coupling_delta = delta * dyad.coupling_strength

            if coupling_delta != 0:
                log_entries.extend(
                    self.modify_character_c_self(
                        other_char_name,
                        coupling_delta,
                        f"sacred resonance with {char_name}",
                        apply_sacred=False,
                        apply_chaos=False
                    )
                )

            if apply_chaos:
                log_entries.append(
                    self.modify_chaos(
                        abs(delta) * 0.5,
                        f"Sacred resonance: {dyad.char_a}-{dyad.char_b}"
                    )
                )

            if delta < 0 and dyad.is_sacred:
                drop = abs(delta)
                if char_name == dyad.char_a:
                    log_entries.extend(
                        self.modify_dyad(
                            dyad.char_b,
                            dyad.char_a,
                            -drop * 0.5,
                            f"sacred bleed from {char_name}",
                            target="A_to_B"
                        )
                    )
                elif char_name == dyad.char_b:
                    log_entries.extend(
                        self.modify_dyad(
                            dyad.char_a,
                            dyad.char_b,
                            -drop * 0.5,
                            f"sacred bleed from {char_name}",
                            target="A_to_B"
                        )
                    )

            char = self.get_character(char_name)
            if char and char.c_self <= 0:
                log_entries.extend(
                    self.modify_character_c_self(
                        other_char_name,
                        -2.0,
                        f"sacred break: {char_name} falls",
                        apply_sacred=False,
                        apply_chaos=False
                    )
                )
                if apply_chaos:
                    log_entries.append(
                        self.modify_chaos(
                            4.0,
                            f"Sacred break: {dyad.char_a}-{dyad.char_b}"
                        )
                    )
                log_entries.append(
                    {"note": f"💔 Sacred Break: {char_name} falls, {other_char_name} destabilizes."}
                )

        return log_entries

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

    def _load_choice_prompts(self) -> Dict[int, Dict[str, Any]]:
        with open("choices.json", "r") as file_handle:
            choice_list = json.load(file_handle)
        return {entry["id"]: entry for entry in choice_list}

    def _select_event(self) -> Event:
        weights = [self.deck_weights.get(event.id, 1.0) for event in self.event_deck]
        return random.choices(self.event_deck, weights=weights, k=1)[0]

    def choose_event(self) -> Event:
        return self._select_event()

    def run_round(self, event: Optional[Event] = None):
        """Run a single round with a random (or specified) event"""
        self.round_number += 1
        self._pending_choice_log = []
        self._pending_choice_summary = []

        # Pick an event if not specified
        if event is None:
            event = self.choose_event()

        # --- CHOICE PROCESSING BLOCK ---
        if event.id in self.choice_prompts:
            choice = self.prompt_for_choice(event)
            self.apply_choice(event, choice)
            self.log.append({"event": event.name, "choice": choice})
        # --- END CHOICE PROCESSING BLOCK ---

        print(f"\n{'='*80}")
        print(f"ROUND {self.round_number}: {event.name}")
        print(f"{'='*80}")
        print(f"Category: {event.category}")
        print(f"Description: {event.description}")
        print()

        # Apply the event
        result = event.apply(self)
        if event.category in ("prophecy", "betrayal"):
            self._apply_thematic_scars(result.get("log", []))

        # Update chaos
        chaos_delta = result.get("chaos", 0)
        if chaos_delta != 0:
            chaos_change = self.modify_chaos(chaos_delta, event.name)
            print(f"Chaos: {chaos_change['old_value']:.1f} → {chaos_change['new_value']:.1f} ({chaos_delta:+.1f})")
            print()

        self._apply_asymmetric_rupture_chaos(result)

        sensitivity_total = sum(char.chaos_sensitivity for char in self.characters.values())
        if sensitivity_total:
            result.setdefault("log", []).append(
                self.modify_chaos(sensitivity_total, "Memory scars resonance")
            )

        # Print the log
        if self._pending_choice_log:
            result.setdefault("log", []).extend(self._pending_choice_log)
        for line in self._pending_choice_summary:
            print(line)
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

                symbol = "↑" if delta > 0 else "↓"
                print(f"  {symbol} {char}: C_self {delta:+.1f} → {new_val:.1f} [{state}]")
                if reason:
                    print(f"     → {reason}")
            elif entry.get("type") == "dyad":
                dyad = entry["dyad"]
                delta = entry["delta"]
                new_val = entry["new_value"]
                state = entry["new_state"]
                reason = entry.get("reason", "")

                symbol = "↑" if delta > 0 else "↓"
                print(f"  {symbol} {dyad}: C_dyad {delta:+.1f} → {new_val:.1f} [{state}]")
                if reason:
                    print(f"     → {reason}")
            elif entry.get("type") == "chaos":
                delta = entry["delta"]
                old_val = entry["old_value"]
                new_val = entry["new_value"]
                reason = entry.get("reason", "")
                symbol = "↑" if delta > 0 else "↓"
                print(f"  {symbol} Chaos: {old_val:.1f} → {new_val:.1f} ({delta:+.1f})")
                if reason:
                    print(f"     → {reason}")

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
            print(f"  {state_symbol} {rel.char_a}-{rel.char_b}: {rel.c_dyad:.1f} [{rel.get_state()}] {trajectory}")

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
            "SACRED": "✨",
            "ASYMMETRIC": "⚡",
            "FUNCTIONAL": "~"
        }
        return state_symbols.get(state, "•")

    def _apply_thematic_scars(self, log_entries: List[Dict]):
        affected_characters = {
            entry.get("character")
            for entry in log_entries
            if entry.get("type") == "character"
        }
        for char_name in affected_characters:
            if not char_name:
                continue
            char = self.get_character(char_name)
            if not char:
                continue
            char.scars += 1
            char.chaos_sensitivity += 0.1

    def _apply_asymmetric_rupture_chaos(self, result: Dict):
        if not result.get("is_rupture"):
            return

        rupture_dyads = result.get("rupture_dyads", [])
        if not rupture_dyads:
            return

        for char_a, char_b in rupture_dyads:
            dyad = self.get_dyad(char_a, char_b)
            if dyad and dyad.get_state() == "ASYMMETRIC":
                extra_chaos = result.get("chaos", 0)
                if extra_chaos:
                    result.setdefault("log", []).append(
                        self.modify_chaos(extra_chaos, "Asymmetric rupture amplification")
                    )
                return

    def _prompt_choice(self, event: Event) -> str:
        choice_entry = self.choice_prompts.get(event.id)
        print("\nCHOICE REQUIRED")
        if choice_entry:
            print(f"Trigger: {choice_entry['trigger']}")
            for key, text in choice_entry["choices"].items():
                print(f"  {key}: {text}")
        print("Choose an archetype: witness, trickster, devourer")
        while True:
            selection = input("Your choice: ").strip().lower()
            if selection in {"witness", "trickster", "devourer"}:
                return selection
            print("Invalid choice. Please enter witness, trickster, or devourer.")

    def prompt_for_choice(self, event: Event) -> str:
        return self._prompt_choice(event)

    def apply_choice(self, event: Event, archetype: str):
        choice_entries, choice_summary = self._resolve_choice(event, archetype)
        self._pending_choice_log.extend(choice_entries)
        self._pending_choice_summary.extend(choice_summary)

        placeholder_entries = self._apply_choice_placeholders(archetype)
        if placeholder_entries:
            self._pending_choice_log.extend(placeholder_entries)

    def _apply_archetype_logic(
        self,
        archetype: str,
        chaos_mod: float,
        c_self_mods: Dict[str, float],
        dyad_mods: Dict[str, float],
        flags: Dict[str, Any]
    ) -> (float, Dict[str, float], Dict[str, float], Dict[str, Any], bool):
        force_mutation = False

        if archetype == "Witness":
            if chaos_mod > 0:
                chaos_mod = 0
            for dyad_key, mod in list(dyad_mods.items()):
                if mod == -1:
                    dyad_mods[dyad_key] = 0.5
            for char_name, mod in list(c_self_mods.items()):
                if mod < 0:
                    char = self.get_character(char_name)
                    if char and char.c_self < 4:
                        c_self_mods[char_name] = mod * 0.5
        elif archetype == "Trickster":
            if random.random() < 0.5:
                chaos_mod += random.choice([-1, 1])
            for char_name, mod in list(c_self_mods.items()):
                if mod != 0:
                    c_self_mods[char_name] = -mod
            for dyad_key, mod in list(dyad_mods.items()):
                if mod != 0:
                    dyad_mods[dyad_key] = -mod
            force_mutation = random.random() < 0.5
        elif archetype == "Devourer":
            total_positive = sum(mod for mod in c_self_mods.values() if mod > 0)
            for char_name, mod in list(c_self_mods.items()):
                if mod > 0:
                    c_self_mods[char_name] = -mod
            if total_positive and c_self_mods:
                lowest_char = min(
                    c_self_mods.keys(),
                    key=lambda name: self.get_character(name).c_self if self.get_character(name) else 0
                )
                c_self_mods[lowest_char] = c_self_mods.get(lowest_char, 0) + total_positive
            for dyad_key, mod in list(dyad_mods.items()):
                if mod > 0:
                    dyad_mods[dyad_key] = -mod
            self.pressure_bias += 1

        return chaos_mod, c_self_mods, dyad_mods, flags, force_mutation

    def _resolve_choice(self, event: Event, archetype: str) -> (List[Dict], List[str]):
        choice_data = event.choices.get(archetype.title(), {})

        chaos_mod = float(choice_data.get("chaos_mod", 0) or 0)
        c_self_mods = dict(choice_data.get("c_self_mods", {}) or {})
        dyad_mods = dict(choice_data.get("dyad_mods", {}) or {})
        flags = dict(choice_data.get("flags", {}) or {})

        chaos_mod, c_self_mods, dyad_mods, flags, force_mutation = self._apply_archetype_logic(
            archetype,
            chaos_mod,
            c_self_mods,
            dyad_mods,
            flags
        )

        log_entries: List[Dict] = []
        if chaos_mod:
            log_entries.append(self.modify_chaos(chaos_mod, f"{archetype} choice"))
        for char_name, mod in c_self_mods.items():
            log_entries.extend(self.modify_character_c_self(char_name, mod, f"{archetype} choice"))
        for dyad_key, mod in dyad_mods.items():
            if "-" not in dyad_key:
                continue
            char_a, char_b = dyad_key.split("-", 1)
            log_entries.extend(self.modify_dyad(char_a, char_b, mod, f"{archetype} choice"))

        choice_key = archetype.title()
        self.archetype_counts[choice_key] += 1
        mutated = self._maybe_mutate_deck(choice_key, force_mutation)

        counts = self.archetype_counts
        choice_summary = [
            f"\nYOU CHOSE: {choice_key}",
            "Choice Effects Applied:",
            f" - Chaos: {chaos_mod:+.1f}",
            f" - c_self adjustments: {c_self_mods or {}}",
            f" - dyad adjustments: {dyad_mods or {}}",
            f" - Flags: {flags or {}}",
            f"Archetype Affinity: W/T/D = {counts['Witness']}/{counts['Trickster']}/{counts['Devourer']}",
            f"Deck Mutated: {'Yes' if mutated else 'No'}"
        ]

        for line in choice_summary:
            log_entries.append({"note": line})

        return log_entries, choice_summary

    def _apply_choice_placeholders(self, archetype: str) -> List[Dict]:
        log_entries = []
        log_entries.append(self.modify_chaos(0.1, f"{archetype} placeholder effect"))

        for char_name in self.characters:
            log_entries.extend(
                self.modify_character_c_self(
                    char_name,
                    0.1,
                    f"{archetype} placeholder uplift"
                )
            )

        for event in self.event_deck:
            self.deck_weights[event.id] = self.deck_weights.get(event.id, 1.0) * 1.01

        choice_key = archetype.title()
        if choice_key == "Witness":
            self.witness_choice_count += 1
        elif choice_key == "Trickster":
            self.trickster_choice_count += 1
        elif choice_key == "Devourer":
            self.devourer_choice_count += 1

        return log_entries

    def _maybe_mutate_deck(self, archetype: str, force: bool = False) -> bool:
        if force or self.archetype_counts[archetype] >= 3:
            self._mutate_deck(archetype)
            self.archetype_counts[archetype] = 0
            return True
        return False

    def _mutate_deck(self, archetype: str):
        for event in self.event_deck:
            weight = self.deck_weights.get(event.id, 1.0)
            if archetype == "Witness":
                if event.category == "salvation" or event.chaos_base < 0:
                    weight *= 1.5
                if "repair" in event.description.lower():
                    weight *= 1.2
            elif archetype == "Trickster":
                weight *= random.uniform(0.5, 1.5)
                if event.unique or event.chaos_base >= 3:
                    weight *= 1.2
            elif archetype == "Devourer":
                keywords = ("prophecy", "rupture", "isolation", "sacrifice", "mirror")
                if (
                    event.category in ("prophecy", "yuul_vulnerability", "external_pressure")
                    or any(word in event.name.lower() for word in keywords)
                    or any(word in event.description.lower() for word in keywords)
                ):
                    weight *= 1.5 * (1 + 0.1 * self.pressure_bias)
                if event.category == "salvation" or event.chaos_base < 0:
                    weight *= 0.5
            self.deck_weights[event.id] = weight

        self.deck_mutated = True

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
                    elif log_entry.get("type") == "chaos":
                        delta = log_entry["delta"]
                        old_val = log_entry["old_value"]
                        new_val = log_entry["new_value"]
                        f.write(f"  Chaos: {old_val:.1f} → {new_val:.1f} ({delta:+.1f})\n")

                f.write("\n")

        print(f"\n✓ Log saved to {filename}")
