"""
Epilogue Composer for Narrative Coherence Engine

Composes dynamic epilogues in Maeve's voice (or DCE for TPK) based on run_state.
Each ending has a template spine with character blocks slotted in.
"""

import json
import random
from typing import Dict, Any, List, Optional


# New transition phrases for cluster-based system
NEW_TRANSITIONS = {
    "before_dead": [
        "This is where the story tightens.",
        "I have to slow down for this part.",
        "Everything in me goes still when I speak their names.",
        "The air changes here.",
        "I never get this part right, but I'll try.",
        "This is the part that still bruises."
    ],
    "before_survivors": [
        "The story tilts here.",
        "Not everyone was taken.",
        "There were still voices left to answer.",
        "The map changes when I talk about the ones who stayed.",
        "This is the part that breathes a little easier."
    ],
    "before_disappeared": [
        "Some names don't fit into death.",
        "This next part feels... unfinished.",
        "There are shapes the field doesn't classify.",
        "I don't know what verb belongs to them.",
        "They didn't die. They shifted."
    ],
    "optional_survivor_start": [
        "",
        "Their names land differently.",
        "I still don't know how to talk about this without shaking.",
        "Somehow, all of them made it through.",
        "The world sounds different when I say these names."
    ],
    "archetype_bleed": {
        "witness": [
            "Something quiet in me leans forward here.",
            "A voice older than memory murmurs: pay attention.",
            "The Witness brushes a hand against the thread."
        ],
        "trickster": [
            "The line wavers -- something amused cuts through.",
            "I can hear laughter in the margins.",
            "The Trickster tugs the thread sideways for a breath."
        ],
        "devourer": [
            "The dark geometry presses closer.",
            "A hunger in the field stirs at this part.",
            "The Devourer tastes the shape of this memory."
        ]
    }
}


class EpilogueComposer:
    """Composes narrative epilogues based on game ending state"""

    def __init__(self):
        """Load all epilogue data files"""
        with open('ending_templates.json', 'r') as f:
            self.ending_templates = json.load(f)

        with open('character_epilogues.json', 'r') as f:
            self.character_epilogues = json.load(f)

        with open('transition_phrases.json', 'r') as f:
            self.transition_phrases = json.load(f)

        with open('archetype_glitches.json', 'r') as f:
            self.archetype_glitches = json.load(f)

    def determine_ending_key(self, run_state: Dict[str, Any]) -> str:
        """
        Determine which ending template to use based on run_state

        Priority order:
        1. TPK (total party kill)
        2. CoR manifestation
        3. DCE win
        4. Canon Redchurch (Kit + Yuul dead)
        5. Disappearance (Kit or Yuul dissolved)
        6. Miracle (everyone survived)
        """
        end_state = run_state['end_state']
        flags = run_state['flags']

        # TPK - everyone died
        if end_state.get('total_party_kill', False):
            return 'tpk_redchurch'

        # CoR manifestation - Children of Resonance won
        if flags.get('cor_manifestation', False):
            return 'cor_manifestation'

        # DCE win - high pressure and team compromised
        if flags.get('dce_pressure_high', False) and flags.get('h11_team_compromised', False):
            return 'dce_win'

        # Canon Redchurch - Kit and Yuul both dead
        if end_state.get('kit_dead', False) and end_state.get('yuul_dead', False):
            return 'redchurch_canon'

        # Disappearance - Kit or Yuul dissolved
        if end_state.get('kit_dissolved', False) or end_state.get('yuul_dissolved', False):
            return 'disappearance'

        # Miracle - everyone survived
        if end_state.get('everyone_survived', False):
            return 'miracle_run'

        # Fallback to canon redchurch
        return 'redchurch_canon'

    def get_character_block(self, char_name: str, run_state: Dict[str, Any]) -> str:
        """
        Get the appropriate character epilogue block

        Priority:
        1. Check for special flag variants (sacred_with_yuul, rielle_recursion, farris_death_echo)
        2. Use base fate block (survived/died/dissolved)
        3. Append global list_hunger variant if flag is set
        """
        characters = run_state['characters']
        flags = run_state['flags']

        if char_name not in characters:
            return ""

        char_state = characters[char_name]
        char_epilogues = self.character_epilogues.get(char_name, {})

        # Determine base fate
        if char_state.get('dissolved', False):
            fate = 'dissolved'
        elif char_state.get('dead', False):
            fate = 'died'
        else:
            fate = 'survived'

        # Check for character-specific flag overrides
        block = ""

        # Yuul - sacred bond override
        if char_name == 'yuul' and flags.get('sacred_with_yuul', False):
            flag_key = f'sacred_with_yuul_{fate}'
            if flag_key in char_epilogues:
                block = char_epilogues[flag_key]

        # Rielle - recursion override
        elif char_name == 'rielle' and flags.get('rielle_recursion', False):
            flag_key = f'rielle_recursion_{fate}'
            if flag_key in char_epilogues:
                block = char_epilogues[flag_key]

        # No special override, use base block
        if not block:
            block = char_epilogues.get(fate, "")

        # Farris death echo (appends to died block)
        if char_name == 'farris' and fate == 'died' and flags.get('farris_death_echo', False):
            echo = char_epilogues.get('farris_death_echo', "")
            if echo:
                block += " " + echo

        # Global List hunger variants (append to any death/dissolution)
        if flags.get('maeve_learned_list_hunger', False):
            global_blocks = self.character_epilogues.get('global_list_hunger', {})
            if fate == 'died':
                list_line = global_blocks.get('maeve_learned_list_hunger_death', "")
                if list_line:
                    block += " " + list_line
            elif fate == 'dissolved':
                list_line = global_blocks.get('maeve_learned_list_hunger_dissolution', "")
                if list_line:
                    block += " " + list_line

        return block

    def choose_transition_phrase(self, run_state: Dict[str, Any], ending_key: str, used_transitions: set) -> str:
        """
        Choose a transition phrase between character blocks

        Based on ending tone + small chance of archetype bleed
        Tracks used transitions to avoid repetition
        """
        # Choose base pool
        if ending_key == 'miracle_run':
            pool = self.transition_phrases['soft']
        elif ending_key in ['redchurch_canon', 'cor_manifestation']:
            pool = self.transition_phrases['fractured']
        else:
            pool = self.transition_phrases['neutral']

        # Archetype bleed chance
        bleed_chance = self._archetype_transition_chance(run_state, ending_key)

        if random.random() < bleed_chance:
            archetype = self._choose_archetype(run_state, ending_key)
            if archetype:
                bleed_pool = self.transition_phrases['archetype_bleed'].get(archetype, [])
                if bleed_pool:
                    # Filter out used transitions
                    available = [t for t in bleed_pool if t not in used_transitions]
                    if available:
                        chosen = random.choice(available)
                        used_transitions.add(chosen)
                        return chosen

        # Filter out used transitions from base pool
        available = [t for t in pool if t not in used_transitions]

        # If all transitions used, reset and use full pool
        if not available:
            available = pool

        chosen = random.choice(available)
        used_transitions.add(chosen)
        return chosen

    def _archetype_transition_chance(self, run_state: Dict[str, Any], ending_key: str) -> float:
        """Calculate chance of archetype bleed in transitions"""
        base = 0.05

        if ending_key in ['redchurch_canon', 'cor_manifestation']:
            base = 0.15

        if run_state['flags'].get('maeve_learned_list_hunger', False):
            base += 0.10

        return min(base, 0.35)

    def _should_glitch(self, run_state: Dict[str, Any], ending_key: str) -> bool:
        """Determine if an archetype glitch line should appear"""
        base_chance = 0.0

        if ending_key == 'miracle_run':
            base_chance = 0.02
        elif ending_key == 'disappearance':
            base_chance = 0.08
        elif ending_key == 'redchurch_canon':
            base_chance = 0.16
        elif ending_key == 'cor_manifestation':
            base_chance = 0.32
        elif ending_key == 'dce_win':
            base_chance = 0.10
        elif ending_key == 'tpk_redchurch':
            base_chance = 0.0  # No glitches in DCE narration

        # Flag modifiers
        if run_state['flags'].get('maeve_learned_list_hunger', False):
            base_chance += 0.10

        if run_state['flags'].get('rielle_recursion', False):
            base_chance += 0.07

        return random.random() < base_chance

    def _choose_archetype(self, run_state: Dict[str, Any], ending_key: str) -> Optional[str]:
        """
        Choose which archetype glitches through

        Weighted by ending type and flags
        """
        weights = {'witness': 1, 'trickster': 1, 'devourer': 1}

        # Ending-specific shifts
        if ending_key == 'redchurch_canon':
            weights['devourer'] += 2
            weights['witness'] += 1
        elif ending_key == 'cor_manifestation':
            weights['devourer'] += 3
            weights['trickster'] += 1
        elif ending_key == 'miracle_run':
            weights['witness'] += 3
            weights['devourer'] = max(0, weights['devourer'] - 2)

        # Flag modifiers
        if run_state['flags'].get('sacred_with_yuul', False):
            weights['witness'] += 2

        if run_state['flags'].get('rielle_recursion', False):
            weights['trickster'] += 2

        if run_state['flags'].get('maeve_learned_list_hunger', False):
            weights['devourer'] += 3

        # Weighted random choice
        total = sum(weights.values())
        if total <= 0:
            return None

        roll = random.random() * total
        cumulative = 0

        for archetype, weight in weights.items():
            cumulative += weight
            if roll < cumulative:
                return archetype

        return 'witness'  # Fallback

    def _choose_glitch_intensity(self, run_state: Dict[str, Any]) -> str:
        """Choose glitch line intensity based on Maeve's coherence"""
        maeve_c = run_state['metrics'].get('maeve_coherence', 5.0)

        if maeve_c > 6:
            return 'soft'
        elif maeve_c > 3:
            # For trickster, return 'chaotic'; for others, return available keys
            return 'sharp'  # or 'chaotic' for trickster
        else:
            return 'hunger'  # or 'prophetic' for devourer

    def compose_epilogue(self, run_state: Dict[str, Any]) -> str:
        """
        Compose the full epilogue text

        Main entry point - returns complete epilogue string
        """
        # Step 1: Determine ending
        ending_key = self.determine_ending_key(run_state)
        template = self.ending_templates[ending_key]

        # Step 2: If DCE narrator, compose clinical version
        if template.get('narrator') == 'dce':
            return self._compose_dce_epilogue(template)

        # Step 3: Compose Maeve narration
        return self._compose_maeve_epilogue(run_state, ending_key, template)

    def _compose_dce_epilogue(self, template: Dict[str, str]) -> str:
        """Compose DCE post-mortem epilogue (TPK)"""
        parts = [
            template['dce_open'],
            template['dce_mid'],
            template['dce_after'],
            template['dce_close']
        ]
        return '\n\n'.join(parts)

    def _glitch_tier(self, run_state: Dict[str, Any]) -> str:
        """Choose glitch intensity tier based on Maeve's coherence"""
        c = run_state['metrics'].get('maeve_coherence', 5.0)
        if c > 6:
            return "soft"
        elif c > 3:
            return "sharp"
        else:
            return "hunger"

    def _compose_maeve_epilogue(self, run_state: Dict[str, Any], ending_key: str, template: Dict[str, str]) -> str:
        """Compose Maeve-narrated epilogue with character blocks using cluster logic"""
        output = []

        # Open
        output.append(template['maeve_open'])
        output.append('')

        # Before characters
        output.append(template['maeve_before_characters'])
        output.append('')

        # -------------------------------
        # CLUSTERING BY FATE
        # -------------------------------
        dead_cluster = []
        disappeared_cluster = []
        survivor_cluster = []

        character_order = ['yuul', 'kit', 'rielle', 'daniel', 'farris', 'maeve']

        for name in character_order:
            if name not in run_state['characters']:
                continue
            c = run_state['characters'][name]

            if c.get('dead', False):
                dead_cluster.append(name)
            elif c.get('dissolved', False):
                disappeared_cluster.append(name)
            else:
                survivor_cluster.append(name)

        # -------------------------------
        # DEAD CLUSTER
        # -------------------------------
        if dead_cluster:
            # ONE transition line before all deaths
            output.append(random.choice(NEW_TRANSITIONS["before_dead"]))
            output.append('')

            for name in dead_cluster:
                block = self.get_character_block(name, run_state)
                if block:
                    output.append(block)
                    output.append('')

        # -------------------------------
        # DISAPPEARED CLUSTER
        # (only used in disappearance endings)
        # -------------------------------
        if disappeared_cluster:
            output.append(random.choice(NEW_TRANSITIONS["before_disappeared"]))
            output.append('')

            for name in disappeared_cluster:
                block = self.get_character_block(name, run_state)
                if block:
                    output.append(block)
                    output.append('')

        # -------------------------------
        # SURVIVOR CLUSTER
        # -------------------------------
        if survivor_cluster:
            # If we already had dead/dissolved -> pivot tone
            if dead_cluster or disappeared_cluster:
                output.append(random.choice(NEW_TRANSITIONS["before_survivors"]))
                output.append('')
            else:
                # If it's a clean miracle/survival run
                start = random.choice(NEW_TRANSITIONS["optional_survivor_start"])
                if start:
                    output.append(start)
                    output.append('')

            for name in survivor_cluster:
                block = self.get_character_block(name, run_state)
                if block:
                    output.append(block)
                    output.append('')

        # -------------------------------
        # AFTER CHARACTERS
        # -------------------------------
        output.append(template['maeve_after_characters'])
        output.append('')

        # ARCHETYPE GLITCH (after reflection)
        if self._should_glitch(run_state, ending_key):
            archetype = self._choose_archetype(run_state, ending_key)
            if archetype:
                tier = self._glitch_tier(run_state)
                # Use archetype bleed transition from NEW_TRANSITIONS
                bleed_line = random.choice(NEW_TRANSITIONS["archetype_bleed"][archetype])
                output.append(bleed_line)
                output.append('')

        # Close
        output.append(template['maeve_close'])

        return '\n\n'.join(output)


# Convenience function
def compose_epilogue(run_state: Dict[str, Any]) -> str:
    """
    Compose epilogue from run_state

    Usage:
        epilogue_text = compose_epilogue(run_state)
        print(epilogue_text)
    """
    composer = EpilogueComposer()
    return composer.compose_epilogue(run_state)
