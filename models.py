"""
Core data models for the Narrative Coherence Engine
"""

from typing import Optional
from constants import (
    C_SELF_MIN, C_SELF_MAX, C_DYAD_MIN, C_DYAD_MAX,
    CHARACTER_STATE_THRESHOLDS, RELATIONSHIP_STATE_THRESHOLDS
)


class Character:
    """Represents a character with coherence metrics"""

    def __init__(self, name: str, c_self: float = 7.0, special_state: Optional[str] = None):
        self.name = name
        self._c_self = c_self
        self.special_state = special_state  # e.g., "Craycray", "Grounded", "Obsessed"
        self.history = []  # Track changes over time

        # Memory Scars system
        self.scars = 0  # Count of personal scars from trauma
        self.chaos_sensitivity = 0.0  # Passive chaos contribution per round

        # Transcendence system
        self.transcendence_unlocked = False  # Can reach C=10 only if True

    @property
    def c_self(self) -> float:
        return self._c_self

    @c_self.setter
    def c_self(self, value: float):
        """
        Set C_self with bounds checking

        TRANSCENDENCE REQUIREMENTS (C=10):
        - Cannot reach 10.0 through normal accumulation
        - Caps at 9.0 unless transcendence_unlocked flag is set
        - Requires: breakthrough event, <= 1 scar, mythic bond
        """
        # Cap at 9.0 (transcendence requires special conditions)
        max_value = C_SELF_MAX if getattr(self, 'transcendence_unlocked', False) else 9.0

        # Apply scar-based ceiling reduction (3+ scars lower max)
        if self.scars >= 6:
            max_value = min(max_value, 8.0)  # 6+ scars: max 8.0
        elif self.scars >= 4:
            max_value = min(max_value, 9.0)  # 4+ scars: max 9.0

        self._c_self = max(C_SELF_MIN, min(max_value, value))

    def modify_c_self(self, delta: float, reason: str = "", apply_scar_penalty: bool = True):
        """Modify C_self value and track the change"""
        old_value = self._c_self
        old_state = self.get_state()
        old_scars = self.scars

        # Apply Memory Scar penalty to recovery (EXPONENTIAL)
        effective_delta = delta
        if delta > 0 and apply_scar_penalty and self.scars > 0:
            # Exponential scar penalties:
            # 1 scar: -0.5, 2 scars: -1.0, 3 scars: -2.0, 4+ scars: -3.0
            if self.scars == 1:
                penalty = 0.5
            elif self.scars == 2:
                penalty = 1.0
            elif self.scars == 3:
                penalty = 2.0
            else:  # 4+
                penalty = 3.0

            effective_delta = max(0, delta - penalty)

        self.c_self = self._c_self + effective_delta

        new_state = self.get_state()

        # Check if character should gain a scar (dropped into Crisis range)
        gained_scar = False
        if old_value >= 3 and self._c_self < 3:
            self.add_scar("dropped below crisis threshold")
            gained_scar = True

        change_record = {
            'reason': reason,
            'delta': delta,
            'effective_delta': effective_delta,
            'old_value': old_value,
            'new_value': self._c_self,
            'old_state': old_state,
            'new_state': new_state,
            'scar_penalty': (delta - effective_delta) if delta > 0 and effective_delta != delta else 0,
            'gained_scar': gained_scar
        }
        self.history.append(change_record)

        return change_record

    def add_scar(self, reason: str = ""):
        """Add a memory scar - permanent trauma that affects future recovery"""
        self.scars += 1
        self.chaos_sensitivity += 0.1
        return {"scars": self.scars, "chaos_sensitivity": self.chaos_sensitivity, "reason": reason}

    def get_state(self) -> str:
        """Get the current state based on C_self threshold"""
        if self.special_state:
            return self.special_state

        for threshold, state in CHARACTER_STATE_THRESHOLDS:
            if self._c_self >= threshold:
                return state

        return "Gone"

    def __repr__(self):
        return f"{self.name} (C_self: {self._c_self:.1f}, State: {self.get_state()})"


class Relationship:
    """Represents a dyadic relationship between two characters"""

    def __init__(self, char_a: str, char_b: str, c_dyad: float = 5.0, coupling_strength: float = 0.3):
        # Store names in alphabetical order for consistent lookups
        self.char_a, self.char_b = sorted([char_a, char_b])

        # Asymmetric Dyads: directional relationship values
        self._AtoB = c_dyad  # How much A values/trusts B
        self._BtoA = c_dyad  # How much B values/trusts A
        self.history = []

        # Sacred Dyad Conservation Law
        self.is_sacred = False
        self.coupling_strength = coupling_strength  # how much one's change affects the other
        self._check_sacred_status()  # Check if starting as sacred

        # Memory Scars system
        self.dyad_scars = 0  # Persistent damage to the relationship

    @property
    def c_dyad(self) -> float:
        """Average of AtoB and BtoA"""
        return (self._AtoB + self._BtoA) / 2.0

    @property
    def AtoB(self) -> float:
        """How much char_a values/trusts char_b"""
        return self._AtoB

    @AtoB.setter
    def AtoB(self, value: float):
        """Set AtoB with bounds checking"""
        self._AtoB = max(C_DYAD_MIN, min(C_DYAD_MAX, value))

    @property
    def BtoA(self) -> float:
        """How much char_b values/trusts char_a"""
        return self._BtoA

    @BtoA.setter
    def BtoA(self, value: float):
        """Set BtoA with bounds checking"""
        self._BtoA = max(C_DYAD_MIN, min(C_DYAD_MAX, value))

    def get_asymmetry(self) -> float:
        """Get the difference between AtoB and BtoA"""
        return abs(self._AtoB - self._BtoA)

    def modify_c_dyad(self, delta: float, reason: str = "", direction: Optional[str] = None,
                      apply_scar_penalty: bool = True):
        """
        Modify C_dyad value and track the change

        Parameters:
            delta: Amount to change
            reason: Description of why
            direction: "AtoB", "BtoA", or None for symmetric
            apply_scar_penalty: Whether to apply scar penalty
        """
        old_AtoB = self._AtoB
        old_BtoA = self._BtoA
        old_avg = self.c_dyad
        old_state = self.get_state()
        was_sacred = self.is_sacred

        # Apply Dyad Scar penalty to reconciliation (EXPONENTIAL)
        effective_delta = delta
        if delta > 0 and apply_scar_penalty and self.dyad_scars > 0:
            # Exponential dyad scar penalties (slightly less harsh than character scars)
            # 1 scar: -0.4, 2 scars: -0.8, 3 scars: -1.5, 4+ scars: -2.5
            if self.dyad_scars == 1:
                penalty = 0.4
            elif self.dyad_scars == 2:
                penalty = 0.8
            elif self.dyad_scars == 3:
                penalty = 1.5
            else:  # 4+
                penalty = 2.5

            effective_delta = max(0, delta - penalty)

        # Apply directionally or symmetrically
        if direction == "AtoB":
            self.AtoB = self._AtoB + effective_delta
        elif direction == "BtoA":
            self.BtoA = self._BtoA + effective_delta
        else:
            # Symmetric - apply to both
            self.AtoB = self._AtoB + effective_delta
            self.BtoA = self._BtoA + effective_delta

        new_state = self.get_state()

        # Check if this change made the bond sacred
        became_sacred = self._check_sacred_status()

        # Check if relationship should gain a scar (major rupture: delta <= -2)
        gained_scar = False
        if effective_delta <= -2.0:
            self.add_dyad_scar("major rupture event")
            gained_scar = True

        change_record = {
            'reason': reason,
            'delta': delta,
            'effective_delta': effective_delta,
            'direction': direction,
            'old_AtoB': old_AtoB,
            'old_BtoA': old_BtoA,
            'new_AtoB': self._AtoB,
            'new_BtoA': self._BtoA,
            'old_value': old_avg,
            'new_value': self.c_dyad,
            'old_state': old_state,
            'new_state': new_state,
            'became_sacred': became_sacred,
            'scar_penalty': (delta - effective_delta) if delta > 0 and effective_delta != delta else 0,
            'gained_scar': gained_scar
        }
        self.history.append(change_record)

        return change_record

    def add_dyad_scar(self, reason: str = ""):
        """Add a dyad scar - persistent damage that makes reconciliation harder"""
        self.dyad_scars += 1
        return {"dyad_scars": self.dyad_scars, "reason": reason}

    def get_state(self) -> str:
        """Get the current state based on C_dyad threshold and asymmetry"""
        avg = self.c_dyad
        diff = self.get_asymmetry()

        # Check for asymmetric state first
        if diff >= 3.0:
            return "ASYMMETRIC"

        # Then check standard thresholds
        for threshold, state in RELATIONSHIP_STATE_THRESHOLDS:
            if avg >= threshold:
                # Special case: SACRED requires low asymmetry
                if state == "SACRED" and diff > 1.0:
                    return "Strong"  # Too asymmetric to be SACRED
                return state

        return "SEVERED"

    def get_trajectory(self) -> str:
        """Get trajectory indicator based on recent history"""
        if len(self.history) < 2:
            return "→"

        recent_changes = sum(h['delta'] for h in self.history[-3:])

        if recent_changes > 0.5:
            return "↑"
        elif recent_changes < -0.5:
            return "↓"
        else:
            return "→"

    def matches(self, char_a: str, char_b: str) -> bool:
        """Check if this relationship matches the given character pair"""
        sorted_pair = sorted([char_a, char_b])
        return self.char_a == sorted_pair[0] and self.char_b == sorted_pair[1]

    def get_direction(self, from_char: str, to_char: str) -> Optional[str]:
        """
        Get the direction string for a change from from_char to to_char
        Returns "AtoB", "BtoA", or None if invalid
        """
        if from_char == self.char_a and to_char == self.char_b:
            return "AtoB"
        elif from_char == self.char_b and to_char == self.char_a:
            return "BtoA"
        return None

    def get_value_from_to(self, from_char: str) -> float:
        """Get how much from_char values the other person"""
        if from_char == self.char_a:
            return self._AtoB
        elif from_char == self.char_b:
            return self._BtoA
        return 0.0

    def _check_sacred_status(self) -> bool:
        """Check if this dyad should become sacred (avg >= 9.0 and diff <= 1.0)"""
        avg = self.c_dyad
        diff = self.get_asymmetry()

        # Sacred requires high average AND low asymmetry
        if avg >= 9.0 and diff <= 1.0:
            if not self.is_sacred:
                self.is_sacred = True
                return True  # Sacred dyad just formed
        else:
            # Lost sacred status (dropped below threshold or too asymmetric)
            if self.is_sacred:
                self.is_sacred = False

        return False

    def get_sacred_partner(self, char_name: str) -> str:
        """Get the other character in this sacred dyad"""
        if char_name == self.char_a:
            return self.char_b
        elif char_name == self.char_b:
            return self.char_a
        return None

    def __repr__(self):
        trajectory = self.get_trajectory()
        sacred_mark = "⚡" if self.is_sacred else ""
        asymm = self.get_asymmetry()

        # Show directional values if asymmetric
        if asymm >= 1.0:
            return f"{self.char_a}-{self.char_b} ({self.char_a}→{self.char_b}: {self._AtoB:.1f}, {self.char_b}→{self.char_a}: {self._BtoA:.1f}, {self.get_state()} {trajectory}{sacred_mark})"
        else:
            return f"{self.char_a}-{self.char_b} (C_dyad: {self.c_dyad:.1f}, {self.get_state()} {trajectory}{sacred_mark})"
