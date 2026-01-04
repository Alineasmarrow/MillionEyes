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

    def __init__(self, char_a: str, char_b: str, c_dyad: float = 5.0):
        # Store names in alphabetical order for consistent lookups
        self.char_a, self.char_b = sorted([char_a, char_b])
        self._c_dyad = c_dyad
        self.history = []

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

        self.c_dyad = self._c_dyad + delta

        new_state = self.get_state()

        change_record = {
            'reason': reason,
            'delta': delta,
            'old_value': old_value,
            'new_value': self._c_dyad,
            'old_state': old_state,
            'new_state': new_state
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

    def __repr__(self):
        trajectory = self.get_trajectory()
        return f"{self.char_a}-{self.char_b} (C_dyad: {self._c_dyad:.1f}, {self.get_state()} {trajectory})"
