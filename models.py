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

    @property
    def c_self(self) -> float:
        return self._c_self

    @c_self.setter
    def c_self(self, value: float):
        """Set C_self with bounds checking"""
        self._c_self = max(C_SELF_MIN, min(C_SELF_MAX, value))

    def modify_c_self(self, delta: float, reason: str = ""):
        """Modify C_self value and track the change"""
        old_value = self._c_self
        old_state = self.get_state()

        self.c_self = self._c_self + delta

        new_state = self.get_state()

        change_record = {
            'reason': reason,
            'delta': delta,
            'old_value': old_value,
            'new_value': self._c_self,
            'old_state': old_state,
            'new_state': new_state
        }
        self.history.append(change_record)

        return change_record

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
        self._c_dyad = c_dyad
        self.history = []

        # Sacred Dyad Conservation Law
        self.is_sacred = False
        self.coupling_strength = coupling_strength  # how much one's change affects the other
        self._check_sacred_status()  # Check if starting as sacred

    @property
    def c_dyad(self) -> float:
        return self._c_dyad

    @c_dyad.setter
    def c_dyad(self, value: float):
        """Set C_dyad with bounds checking"""
        self._c_dyad = max(C_DYAD_MIN, min(C_DYAD_MAX, value))

    def modify_c_dyad(self, delta: float, reason: str = ""):
        """Modify C_dyad value and track the change"""
        old_value = self._c_dyad
        old_state = self.get_state()
        was_sacred = self.is_sacred

        self.c_dyad = self._c_dyad + delta

        new_state = self.get_state()

        # Check if this change made the bond sacred
        became_sacred = self._check_sacred_status()

        change_record = {
            'reason': reason,
            'delta': delta,
            'old_value': old_value,
            'new_value': self._c_dyad,
            'old_state': old_state,
            'new_state': new_state,
            'became_sacred': became_sacred
        }
        self.history.append(change_record)

        return change_record

    def get_state(self) -> str:
        """Get the current state based on C_dyad threshold"""
        for threshold, state in RELATIONSHIP_STATE_THRESHOLDS:
            if self._c_dyad >= threshold:
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

    def _check_sacred_status(self) -> bool:
        """Check if this dyad should become sacred (C_dyad >= 9.0)"""
        if self._c_dyad >= 9.0 and not self.is_sacred:
            self.is_sacred = True
            return True  # Sacred dyad just formed
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
        return f"{self.char_a}-{self.char_b} (C_dyad: {self._c_dyad:.1f}, {self.get_state()} {trajectory}{sacred_mark})"
