"""
Main Simulation Engine for the Narrative Coherence System
"""

import random
import json
import os
from typing import Dict, List, Optional, Any
from models import Character, Relationship
from events import Event, create_event_deck
from chaos_state import ChaosState, get_chaos_components
from act_system import ActSystem, ACT_EVENT_POOLS, display_act_banner
from act_events import EVENT_FUNCTIONS
from act3_system import Act3System, FarrisEntity, ENDING_NARRATIVES
from momentum_system import FieldState, calculate_stacked_modifier, get_momentum_display
from constants import (
    CHAOS_THRESHOLD, CHAOS_WARNING_THRESHOLD,
    WITCH_TRINE_MEMBERS, WITCH_TRINE_DYADS
)


class NarrativeSimulation:
    """Main simulation engine for running narrative scenarios"""

    def __init__(self, name: str = "Untitled Scenario", interactive_mode: bool = False, use_act_system: bool = False):
        self.name = name
        self.characters: Dict[str, Character] = {}
        self.relationships: List[Relationship] = []
        self.chaos_state = ChaosState()  # Two-dimensional chaos: turbulence + pressure
        self.round_number = 0
        self.event_history = []
        self.log_entries = []

        # Choice system for interactive mode (must be set early for _load_act_data)
        self.interactive_mode = interactive_mode
        self.choices_data = None
        self.archetype_counts = {"witness": 0, "trickster": 0, "devourer": 0}
        self.choice_history = []  # Track which choices were made

        # Act system (new structured event system)
        self.use_act_system = use_act_system
        self.act_system = None
        self.act_data = None
        self.last_displayed_act = 0  # Track which act banner we last displayed

        # Act 3 system (conditional events, endings, Farris)
        self.act3_system = None
        self.farris = None
        self.character_stats = None

        # Momentum system (coherence breeds coherence)
        self.field_state = FieldState()  # Environmental field affects all characters

        if use_act_system:
            self.act_system = ActSystem()
            self.act3_system = Act3System()
            self.farris = FarrisEntity()
            self._load_act_data()
            self._load_character_stats()
            self.event_deck = self.act_system.get_available_deck(1)  # Start with Act 1
        else:
            self.event_deck = create_event_deck()  # Use legacy event deck

        # Event tracking for cooldowns, unique flags, and probability decay
        self.event_last_played: Dict[str, str] = {}  # event_id -> round_number when last played
        self.event_play_count: Dict[str, int] = {}   # event_id -> number of times played
        self.event_played_unique: set = set()        # set of event_ids that are unique and have been played

        # Burn card system
        self.burned_cards: set = set()  # Set of card IDs that have been burned
        self.world_effects: Dict[str, Any] = {}  # Active world effects from burned cards
        self.chaos_baseline: float = 0.0  # Baseline chaos added each round
        self.cor_threshold: float = CHAOS_THRESHOLD  # Custom CoR threshold (can be modified by burns)
        self.recovery_modifier: float = 1.0  # Global recovery modifier (1.0 = normal, 0.7 = -30%)
        self.dyad_healing_modifier: float = 1.0  # Dyad healing cost modifier

        if self.interactive_mode:
            self._load_choices()

    @property
    def chaos(self) -> float:
        """Total chaos (backward compatibility property)"""
        return self.chaos_state.total

    @chaos.setter
    def chaos(self, value: float):
        """Set chaos by splitting evenly between turbulence and pressure"""
        half = value / 2.0
        self.chaos_state.turbulence = half
        self.chaos_state.pressure = half

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

    def _load_act_data(self):
        """Load act data from act_data.json and build event pools"""
        act_data_path = os.path.join(os.path.dirname(__file__), 'act_data.json')
        try:
            with open(act_data_path, 'r') as f:
                self.act_data = json.load(f)

            # Build event pools for each act
            for act_num_str, act_info in self.act_data['acts'].items():
                act_num = int(act_num_str)
                events = []

                for event_data in act_info['events']:
                    event_id = event_data['id']

                    # Get the event function
                    if event_id not in EVENT_FUNCTIONS:
                        print(f"⚠️  Warning: Event function not found for '{event_id}'")
                        continue

                    # Get burn effects if present
                    burn_effects = event_data.get('burn_effects', {})

                    # Create Event object
                    event = Event(
                        id=event_id,  # Use string ID for act events
                        name=event_data['name'],
                        category=event_data['category'],
                        description=event_data['description'],
                        chaos_base=event_data['chaos'],
                        apply_func=EVENT_FUNCTIONS[event_id],
                        unique=event_data.get('unique', False),
                        cooldown=event_data.get('cooldown', 0),
                        probability_decay=event_data.get('probability_decay', 1.0),
                        burns=event_data.get('burns', False),
                        burn_effects=burn_effects,
                        turbulence=event_data.get('turbulence'),
                        pressure=event_data.get('pressure')
                    )

                    # Add Act 3 conditional triggers as attribute
                    if 'triggers' in event_data:
                        event.triggers = event_data['triggers']

                    events.append(event)

                ACT_EVENT_POOLS[act_num] = events

            print(f"✓ Loaded {len(self.act_data['acts'])} acts with events")

            # Load choices from act_data if in interactive mode
            if self.interactive_mode and 'choices' in self.act_data:
                self._load_choices_from_act_data()

        except FileNotFoundError:
            print(f"⚠️  act_data.json not found at {act_data_path}")
            self.use_act_system = False
        except json.JSONDecodeError as e:
            print(f"⚠️  Error parsing act_data.json: {e}")
            self.use_act_system = False

    def _load_choices_from_act_data(self):
        """Load choices from act_data.json for interactive mode"""
        try:
            # Convert act_data choices format to the format expected by display_choice
            choices_list = []
            unique_card_mapping = {}

            for choice_id_str, choice_data in self.act_data['choices'].items():
                choice_id = int(choice_id_str)
                event_id = choice_data['event_id']

                # Map event_id to choice_id
                unique_card_mapping[event_id] = choice_id

                # Build choice entry
                choices_list.append({
                    'id': choice_id,
                    'description': choice_data['description'],
                    'witness': choice_data['choices']['witness']['text'],
                    'trickster': choice_data['choices']['trickster']['text'],
                    'devourer': choice_data['choices']['devourer']['text']
                })

            # Build archetype_effects (standard across all choices)
            archetype_effects = {
                'witness': {'note': 'Truth cuts deep', 'chaos': -1.0, 'target_c_self': +1.0},
                'trickster': {'note': 'Chaos creates space', 'chaos': +1.0, 'target_c_self': -0.5},
                'devourer': {'note': 'Sacrifice bears weight', 'chaos': -0.5, 'bearer_c_self': -1.0}
            }

            self.choices_data = {
                'choices': choices_list,
                'unique_card_mapping': unique_card_mapping,
                'archetype_effects': archetype_effects
            }

            print(f"✓ Loaded {len(choices_list)} choice moments from act_data.json")

        except Exception as e:
            print(f"⚠️  Error loading choices from act_data: {e}")
            self.interactive_mode = False

    def _load_choices(self):
        """Load choices from choices.json (legacy mode)"""
        if self.use_act_system:
            # Choices already loaded from act_data
            return

        choices_path = os.path.join(os.path.dirname(__file__), 'choices.json')
        try:
            with open(choices_path, 'r') as f:
                self.choices_data = json.load(f)
            print(f"✓ Loaded {len(self.choices_data['choices'])} choice moments")
        except FileNotFoundError:
            print(f"⚠️  choices.json not found at {choices_path}")
            self.interactive_mode = False
        except json.JSONDecodeError as e:
            print(f"⚠️  Error parsing choices.json: {e}")
            self.interactive_mode = False

    def _load_character_stats(self):
        """Load character stat blocks for Act 3 breakpoints"""
        stats_path = os.path.join(os.path.dirname(__file__), 'character_stats.json')
        try:
            with open(stats_path, 'r') as f:
                self.character_stats = json.load(f)
            print(f"✓ Loaded character stats for {len(self.character_stats['characters'])} characters")
        except FileNotFoundError:
            print(f"⚠️  character_stats.json not found")
        except json.JSONDecodeError as e:
            print(f"⚠️  Error parsing character_stats.json: {e}")

    def display_choice(self, choice_id: int) -> Optional[str]:
        """
        Display a choice moment and get player input

        Returns: "witness", "trickster", or "devourer"
        """
        if not self.choices_data:
            return None

        # Find the choice
        choice = None
        for c in self.choices_data['choices']:
            if c['id'] == choice_id:
                choice = c
                break

        if not choice:
            print(f"⚠️  Choice {choice_id} not found")
            return None

        # Display choice
        print("\n" + "=" * 80)
        print(f"⚡ CHOICE MOMENT: {choice['description']}")
        print("=" * 80)
        print()
        print("[1] WITNESS")
        print(f'    "{choice["witness"]}"')
        print()
        print("[2] TRICKSTER")
        print(f'    "{choice["trickster"]}"')
        print()
        print("[3] DEVOURER")
        print(f'    "{choice["devourer"]}"')
        print()

        # Get input
        while True:
            try:
                selection = input("Select (1/2/3): ").strip()
                if selection in ["1", "2", "3"]:
                    archetype_map = {"1": "witness", "2": "trickster", "3": "devourer"}
                    return archetype_map[selection]
                else:
                    print("Please enter 1, 2, or 3")
            except (KeyboardInterrupt, EOFError):
                print("\nDefaulting to WITNESS")
                return "witness"

    def apply_archetype_effect(self, archetype: str, event_name: str):
        """
        Apply the mechanical effects of an archetype choice

        Effects:
        - Witness: target +0.5 C_self, chaos +0.1
        - Trickster: target +0.3 C_self, chaos +1.0
        - Devourer: target +1.0 C_self, Maeve -0.5 C_self, chaos -0.5
        """
        if not self.choices_data or archetype not in self.choices_data['archetype_effects']:
            return

        effects = self.choices_data['archetype_effects'][archetype]
        print(f"\n⚡ {archetype.upper()} chosen: {effects['note']}")

        # Apply chaos effect
        chaos_delta = effects.get('chaos', 0)
        if chaos_delta != 0:
            # Archetype chaos splits evenly
            half = chaos_delta / 2.0
            self.chaos_state.add_hybrid(half, half)
            print(f"   Chaos {chaos_delta:+.1f} → {self.chaos:.1f}")

        # Apply target C_self effect (apply to a random character as "target")
        target_delta = effects.get('target_c_self', 0)
        if target_delta != 0 and self.characters:
            target_char = random.choice(list(self.characters.keys()))
            result = self.modify_character_c_self(target_char, target_delta,
                                                  f"{archetype} archetype effect",
                                                  apply_sacred_coupling=False)
            print(f"   {target_char} C_self {target_delta:+.1f} → {result['new_value']:.1f}")

        # Apply bearer effect (Devourer sacrifices Maeve's coherence)
        bearer_delta = effects.get('bearer_c_self', 0)
        if bearer_delta != 0:
            bearer = self.get_character("Maeve")
            if bearer:
                result = self.modify_character_c_self("Maeve", bearer_delta,
                                                      f"{archetype} archetype sacrifice",
                                                      apply_sacred_coupling=False)
                print(f"   Maeve (bearer) C_self {bearer_delta:+.1f} → {result['new_value']:.1f}")

    def apply_burn_effect(self, event: Event):
        """
        Apply permanent burn effects from a burn card

        Burn cards permanently alter the game state after triggering
        """
        if not event.burns or event.id in self.burned_cards:
            return

        burn_effects = event.burn_effects
        world_effect = burn_effects.get('world_effect', 'unknown')

        print(f"\n🔥 BURN CARD TRIGGERED: {event.name}")
        print(f"   💀 {world_effect.replace('_', ' ').title()}")

        # Mark card as burned
        self.burned_cards.add(event.id)
        self.world_effects[world_effect] = burn_effects

        # Apply chaos baseline increase
        chaos_baseline_delta = burn_effects.get('chaos_baseline', 0)
        if chaos_baseline_delta > 0:
            self.chaos_baseline += chaos_baseline_delta
            print(f"   → Baseline chaos increased: +{chaos_baseline_delta:.1f} per round")

        # Remove cards from deck
        remove_cards = burn_effects.get('remove_cards', [])
        if remove_cards:
            for card_id in remove_cards:
                # Find and remove the card
                self.event_deck = [e for e in self.event_deck if e.id != card_id]
                removed_card = next((e for e in create_event_deck() if e.id == card_id), None)
                if removed_card:
                    print(f"   → Card removed from deck: {removed_card.name}")

        # Modify CoR threshold
        cor_threshold = burn_effects.get('cor_threshold')
        if cor_threshold:
            self.cor_threshold = cor_threshold
            print(f"   → CoR threshold lowered: {cor_threshold:.1f}")

        # Apply recovery penalty
        recovery_penalty = burn_effects.get('recovery_penalty', 0)
        if recovery_penalty > 0:
            self.recovery_modifier *= (1.0 - recovery_penalty)
            print(f"   → All recovery effects: {(1.0-recovery_penalty)*100:.0f}% effectiveness")

        # Apply dyad healing cost multiplier
        dyad_cost = burn_effects.get('dyad_healing_cost', 1.0)
        if dyad_cost != 1.0:
            self.dyad_healing_modifier *= dyad_cost
            print(f"   → Dyad healing costs: {dyad_cost}x")

        # Apply chaos multipliers (for specific categories)
        chaos_multiplier = burn_effects.get('chaos_multiplier', {})
        if chaos_multiplier:
            for category, mult in chaos_multiplier.items():
                print(f"   → {category} events: {(mult-1)*100:+.0f}% chaos")

        print(f"   💀 The world remembers {event.name}")

    def modify_character_c_self(self, char_name: str, delta: float, reason: str = "",
                                apply_sacred_coupling: bool = True) -> Dict:
        """Modify a character's C_self value and apply Sacred Dyad Conservation Law"""
        char = self.get_character(char_name)
        if not char:
            return {"error": f"Character {char_name} not found"}

        old_c_self = char.c_self

        # Apply momentum modifiers to positive gains only
        original_delta = delta
        momentum_bonus = ""
        if delta > 0:
            char_mod = char.momentum.get_coherence_modifier()
            field_mod = self.field_state.get_coherence_modifier()
            stacked_mod = calculate_stacked_modifier(char_mod, field_mod)

            if stacked_mod > 1.0:
                delta = delta * stacked_mod
                momentum_bonus = get_momentum_display(char_mod, field_mod)

        change = char.modify_c_self(delta, reason)

        # Update character momentum (track if this was positive or negative)
        char.momentum.update(delta > 0)

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
            "original_delta": original_delta,
            "effective_delta": change.get('effective_delta', delta),
            "new_value": char.c_self,
            "new_state": char.get_state(),
            "reason": reason,
            "sacred_echoes": change.get('sacred_echoes', []),
            "sacred_chaos": change.get('sacred_chaos', 0),
            "scar_penalty": change.get('scar_penalty', 0),
            "gained_scar": change.get('gained_scar', False),
            "momentum_bonus": momentum_bonus
        }

    def modify_dyad(self, char_a: str, char_b: str, delta: float, reason: str = "",
                    direction: Optional[str] = None) -> Dict:
        """
        Modify a dyad's C_dyad value

        Parameters:
            char_a, char_b: The characters in the relationship
            delta: Amount to change
            reason: Description
            direction: "AtoB", "BtoA", or None for symmetric
        """
        dyad = self.get_dyad(char_a, char_b)
        if not dyad:
            return {"error": f"Relationship {char_a}-{char_b} not found"}

        change = dyad.modify_c_dyad(delta, reason, direction)

        return {
            "type": "dyad",
            "dyad": f"{dyad.char_a}-{dyad.char_b}",
            "delta": delta,
            "effective_delta": change.get('effective_delta', delta),
            "direction": change.get('direction'),
            "new_value": dyad.c_dyad,
            "new_AtoB": dyad.AtoB,
            "new_BtoA": dyad.BtoA,
            "new_state": dyad.get_state(),
            "reason": reason,
            "became_sacred": change.get('became_sacred', False),
            "scar_penalty": change.get('scar_penalty', 0),
            "gained_scar": change.get('gained_scar', False),
            "asymmetry": dyad.get_asymmetry()
        }

    def modify_chaos(self, delta: float, reason: str = "", event_id: int = None):
        """
        Modify the chaos counter using textured chaos (turbulence + pressure)

        If event_id is provided, uses the event's chaos typing to split into components
        Otherwise, splits evenly between turbulence and pressure
        """
        old_chaos = self.chaos

        if event_id:
            # Use event-specific chaos typing
            turbulence, pressure = get_chaos_components(event_id, delta)
            self.chaos_state.add_hybrid(turbulence, pressure)
        else:
            # Default: split evenly
            half = delta / 2.0
            self.chaos_state.add_hybrid(half, half)

        return {
            "type": "chaos",
            "delta": delta,
            "old_value": old_chaos,
            "new_value": self.chaos,
            "turbulence": self.chaos_state.turbulence,
            "pressure": self.chaos_state.pressure,
            "field": self.chaos_state.dominant_field,
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

        # Add the chaos (sacred chaos is mostly turbulence - unpredictable)
        if chaos_impact > 0:
            self.chaos_state.add_hybrid(chaos_impact * 0.7, chaos_impact * 0.3)

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

            # Reality buckles (sacred collapse is pure pressure - reality enforcing loss)
            self.chaos_state.add_hybrid(0.0, 4.0)

            print(f"\n💔 SACRED BREAK: {collapsed_char} falls, {partner_name} destabilizes!")
            print(f"   → {partner_name} suffers grief rupture (-2.0 C_self)")
            print(f"   → Reality buckles (+4.0 pressure chaos)")

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

    def select_event_with_probability(self) -> Optional[Event]:
        """
        Select an event using probability weights, respecting cooldowns and unique flags

        Returns:
            Selected Event, or None if no events are available
        """
        available_events = []
        weights = []

        for event in self.event_deck:
            # Skip burned cards
            if event.id in self.burned_cards:
                continue

            # Skip unique events that have already been played
            if event.unique and event.id in self.event_played_unique:
                continue

            # Skip events on cooldown
            if event.id in self.event_last_played:
                rounds_since_played = self.round_number - self.event_last_played[event.id]
                if rounds_since_played < event.cooldown:
                    continue

            # Act 3: Check conditional triggers
            if self.act3_system and hasattr(event, 'triggers'):
                # Convert event to dict for trigger checking
                event_dict = {
                    "triggers": getattr(event, 'triggers', {})
                }
                if not self.act3_system.check_event_triggers(event_dict, self.characters, self.relationships):
                    continue  # Skip event if triggers not met

            # Calculate weight based on probability decay
            play_count = self.event_play_count.get(event.id, 0)
            weight = event.probability_decay ** play_count

            available_events.append(event)
            weights.append(weight)

        # If no events available, return None
        if not available_events:
            return None

        # Weighted random selection
        return random.choices(available_events, weights=weights, k=1)[0]

    def run_round(self, event: Optional[Event] = None):
        """Run a single round with a random (or specified) event"""
        self.round_number += 1

        # Check for act transition (if using act system)
        if self.use_act_system and self.act_system:
            current_act = self.act_system.get_current_act(self.round_number)

            # Display act banner if transitioning to new act
            if current_act != self.last_displayed_act:
                display_act_banner(current_act)
                self.last_displayed_act = current_act

                # Update event deck for new act
                self.event_deck = self.act_system.get_available_deck(current_act)

        # Pick an event if not specified
        if event is None:
            event = self.select_event_with_probability()
            if event is None:
                print(f"\n⚠️ No events available to play (all on cooldown or unique events exhausted)")
                return

        # Track event play
        self.event_last_played[event.id] = self.round_number
        self.event_play_count[event.id] = self.event_play_count.get(event.id, 0) + 1
        if event.unique:
            self.event_played_unique.add(event.id)
        self.event_history.append(event)

        print(f"\n{'='*80}")
        print(f"ROUND {self.round_number}: {event.name}")
        print(f"{'='*80}")
        print(f"Category: {event.category}")
        print(f"Description: {event.description}")
        print()

        # Apply the event
        result = event.apply(self)

        # Apply burn effects if this is a burn card
        if event.burns:
            self.apply_burn_effect(event)

        # Check for choice moment (only on unique cards in interactive mode)
        if self.interactive_mode and event.unique and self.choices_data:
            # Check if this unique card has a choice mapped
            unique_card_mapping = self.choices_data.get('unique_card_mapping', {})
            # Handle both string and numeric event IDs
            event_id_key = event.id if isinstance(event.id, str) else str(event.id)
            choice_id = unique_card_mapping.get(event_id_key)

            if choice_id:
                # Display choice and get selection
                archetype = self.display_choice(choice_id)
                if archetype:
                    # Track the choice
                    self.archetype_counts[archetype] += 1
                    self.choice_history.append({
                        "round": self.round_number,
                        "event": event.name,
                        "choice_id": choice_id,
                        "archetype": archetype
                    })

                    # Update Farris mode (Act 3)
                    if self.farris:
                        self.farris.update_from_choice(archetype)
                        self.farris.coherence = self.farris.get_coherence(self.characters.get("Maeve").c_self)

                    # Apply archetype effects
                    self.apply_archetype_effect(archetype, event.name)

        # Update chaos
        # For act events, use event.chaos_base if the result doesn't include chaos
        chaos_delta = result.get("chaos", event.chaos_base if hasattr(event, 'chaos_base') and event.chaos_base != 0 else 0)

        if chaos_delta != 0 or (hasattr(event, 'turbulence') and event.turbulence is not None):
            old_chaos = self.chaos

            # For act events with explicit turbulence/pressure, use those
            if hasattr(event, 'turbulence') and event.turbulence is not None and hasattr(event, 'pressure') and event.pressure is not None:
                self.chaos_state.add_hybrid(event.turbulence, event.pressure)
                chaos_change = {
                    "type": "chaos",
                    "delta": chaos_delta,
                    "old_value": old_chaos,
                    "new_value": self.chaos,
                    "turbulence": self.chaos_state.turbulence,
                    "pressure": self.chaos_state.pressure,
                    "field": self.chaos_state.dominant_field,
                    "reason": event.name
                }
            else:
                # Legacy events: use modify_chaos
                chaos_change = self.modify_chaos(chaos_delta, event.name, event_id=event.id)

            print(f"Chaos: {chaos_change['old_value']:.1f} → {chaos_change['new_value']:.1f} ({chaos_delta:+.1f})")
            print(f"  Turbulence: {chaos_change['turbulence']:.1f} | Pressure: {chaos_change['pressure']:.1f}")

            # Display field state if significant
            field_type = chaos_change['field']
            if field_type != "BALANCED":
                effects = self.chaos_state.get_field_effects()
                print(f"  {effects['type']} ACTIVE")
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
                original_delta = entry.get("original_delta", delta)
                effective_delta = entry.get("effective_delta", delta)
                new_val = entry["new_value"]
                state = entry["new_state"]
                reason = entry.get("reason", "")
                sacred_echoes = entry.get("sacred_echoes", [])
                sacred_chaos = entry.get("sacred_chaos", 0)
                scar_penalty = entry.get("scar_penalty", 0)
                gained_scar = entry.get("gained_scar", False)
                momentum_bonus = entry.get("momentum_bonus", "")

                symbol = "↑" if delta > 0 else "↓"

                # Show effective delta if different from original
                if abs(effective_delta - delta) > 0.01:
                    print(f"  {symbol} {char}: C_self {delta:+.1f} (effective: {effective_delta:+.1f}) → {new_val:.1f} [{state}]")
                    print(f"     💔 Scar penalty: -{scar_penalty:.1f}")
                # Show momentum bonus if present
                elif momentum_bonus:
                    print(f"  {symbol} {char}: C_self {original_delta:+.1f} → {delta:+.1f} {momentum_bonus} → {new_val:.1f} [{state}]")
                else:
                    print(f"  {symbol} {char}: C_self {delta:+.1f} → {new_val:.1f} [{state}]")

                if reason:
                    print(f"     → {reason}")

                # Display scar gain
                if gained_scar:
                    print(f"     💔 GAINED MEMORY SCAR - recovery now harder")

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
                effective_delta = entry.get("effective_delta", delta)
                new_val = entry["new_value"]
                state = entry["new_state"]
                reason = entry.get("reason", "")
                became_sacred = entry.get("became_sacred", False)
                scar_penalty = entry.get("scar_penalty", 0)
                gained_scar = entry.get("gained_scar", False)

                symbol = "↑" if delta > 0 else "↓"

                # Show effective delta if different from original
                if abs(effective_delta - delta) > 0.01:
                    print(f"  {symbol} {dyad}: C_dyad {delta:+.1f} (effective: {effective_delta:+.1f}) → {new_val:.1f} [{state}]")
                    print(f"     💔 Dyad scar penalty: -{scar_penalty:.1f}")
                else:
                    print(f"  {symbol} {dyad}: C_dyad {delta:+.1f} → {new_val:.1f} [{state}]")

                if reason:
                    print(f"     → {reason}")

                # Display scar gain
                if gained_scar:
                    print(f"     💔 GAINED DYAD SCAR - reconciliation now harder")

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

        # Apply passive chaos from Memory Scars (scars add pressure - weight of trauma)
        scar_chaos = sum(char.chaos_sensitivity for char in self.characters.values())
        if scar_chaos > 0:
            self.chaos_state.add_hybrid(0.0, scar_chaos)
            print(f"\n💔 Memory Scars add {scar_chaos:.1f} passive pressure (Total: {self.chaos:.1f})")

        # Update Field State based on round outcomes
        positive_count = 0
        negative_count = 0
        for entry in result.get("log", []):
            if entry.get("type") == "character":
                delta = entry.get("delta", 0)
                if delta > 0:
                    positive_count += 1
                elif delta < 0:
                    negative_count += 1

        self.field_state.update_from_round(positive_count, negative_count)

        # Display field state if it's significant
        if self.field_state.state != "neutral":
            field_desc = self.field_state.get_state_description()
            print(f"\n🌊 Field State: {field_desc}")

        # Apply special character effects (Farris mirroring, etc.)
        self._apply_special_character_effects()

    def _apply_special_character_effects(self):
        """Apply special character-specific effects at end of round"""
        # Farris mirrors Maeve's coherence
        farris = self.get_character("Farris")
        maeve = self.get_character("Maeve")

        if farris and maeve:
            old_farris_c = farris.c_self

            if maeve.c_self >= 7:
                # Farris mirrors Maeve when she's stable/high
                farris._c_self = maeve.c_self
                if abs(old_farris_c - farris.c_self) > 0.1:
                    print(f"\n🐺 Farris mirrors Maeve: {old_farris_c:.1f} → {farris.c_self:.1f}")

            elif maeve.c_self <= 4:
                # Farris becomes volatile when Maeve is low
                if not hasattr(farris, 'instability'):
                    farris.instability = 0
                farris.instability += 1

                if farris.instability > 0:
                    print(f"\n🐺 Farris destabilizes as Maeve falls (instability: {farris.instability})")

        # Daniel pressure check
        daniel = self.get_character("Daniel")
        if daniel and maeve:
            maeve_daniel_dyad = self.get_dyad("Maeve", "Daniel")
            if maeve_daniel_dyad and maeve_daniel_dyad.c_dyad < 3:
                if hasattr(self, 'act3_system'):
                    if not self.act3_system.special_flags.get("h11_unstable", False):
                        self.act3_system.special_flags["h11_unstable"] = True
                        print(f"\n⚠️  H11 becomes unstable (Maeve-Daniel dyad fractured)")

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
            scar_info = f" 💔 {char.scars} scars" if char.scars > 0 else ""
            print(f"  {state_symbol} {char}{scar_info}")

        print("\nFINAL RELATIONSHIP STATES:")
        for rel in sorted(self.relationships, key=lambda r: (r.char_a, r.char_b)):
            state_symbol = self._get_dyad_state_symbol(rel.get_state())
            trajectory = rel.get_trajectory()
            sacred_mark = " ⚡ SACRED" if rel.is_sacred else ""
            scar_mark = f" 💔 {rel.dyad_scars} scars" if rel.dyad_scars > 0 else ""
            print(f"  {state_symbol} {rel.char_a}-{rel.char_b}: {rel.c_dyad:.1f} [{rel.get_state()}] {trajectory}{sacred_mark}{scar_mark}")

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

        # Display archetype summary if in interactive mode
        if self.interactive_mode and self.choice_history:
            print(f"\n{'='*80}")
            print("ARCHETYPE SUMMARY")
            print(f"{'='*80}")

            total_choices = sum(self.archetype_counts.values())
            if total_choices > 0:
                for archetype, count in sorted(self.archetype_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / total_choices) * 100
                    print(f"  {archetype.upper()}: {count} choices ({percentage:.1f}%)")

                # Determine dominant archetype
                dominant = max(self.archetype_counts.items(), key=lambda x: x[1])
                print(f"\n  Dominant Archetype: {dominant[0].upper()}")

                if dominant[0] == "witness":
                    print("  Your story favored clarity and truth-telling.")
                elif dominant[0] == "trickster":
                    print("  Your story favored chaos and disruption as medicine.")
                elif dominant[0] == "devourer":
                    print("  Your story favored sacrifice and burden-bearing.")

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

        # Act 3: Calculate and display ending
        if self.act3_system and self.farris:
            print(f"\n{'='*80}")
            print("CALCULATING ENDING...")
            print(f"{'='*80}")

            # Calculate ending
            final_ending, all_weights = self.act3_system.calculate_ending(self, self.farris)

            # Display Farris final state
            print(f"\n🗣️ FARRIS (Voice Archetype Mirror)")
            print(f"  Mode: {self.farris.mode.upper()}")
            print(f"  Coherence: {self.farris.coherence:.1f} (mirroring Maeve)")

            # Display ending weights
            print(f"\n📊 ENDING WEIGHTS:")
            for ending_name, weight in sorted(all_weights.items(), key=lambda x: x[1], reverse=True):
                bar = "█" * int(weight / 5) if weight > 0 else ""
                print(f"  {ending_name.replace('_', ' ').title():25s}: {weight:3.0f} {bar}")

            # Display the final ending
            ending_data = ENDING_NARRATIVES.get(final_ending, {})
            print(f"\n{'='*80}")
            print(f"{'='*80}")
            print(f"{ending_data.get('title', 'UNKNOWN ENDING')}")
            print(f"{'='*80}")
            print(f"{'='*80}")
            print(ending_data.get('description', 'No description available.'))

            # Display ending metadata
            if 'survivors' in ending_data:
                print(f"\n✓ SURVIVORS: {', '.join(ending_data['survivors'])}")
            if 'dead' in ending_data:
                print(f"\n💀 CASUALTIES: {', '.join(ending_data['dead'])}")
            if 'transformed' in ending_data:
                print(f"\n🌀 TRANSFORMED: {', '.join(ending_data['transformed'])}")
            if 'status' in ending_data:
                print(f"\n⚠️  STATUS: {ending_data['status']}")

            print(f"\n{'='*80}")

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
