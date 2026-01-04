"""
Core data models for the Narrative Coherence Engine
"""

from typing import Optional
from constants import (
    C_SELF_MIN, C_SELF_MAX, C_DYAD_MIN, C_DYAD_MAX,
    CHARACTER_STATE_THRESHOLDS
)


class Character:
    """Represents a character with coherence metrics"""

    def __init__(self, name: str, c_self: float = 7.0, special_state: Optional[str] = None):
        self.name = name
        self._c_self = c_self
        self.special_state = special_state  # e.g., "Craycray", "Grounded", "Obsessed"
        self.history = []  # Track changes over time
        self.scars = 0
        self.chaos_sensitivity = 0.0

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
        self._a_to_b = c_dyad
        self._b_to_a = c_dyad
        self.dyad_scars = 0
        self.is_sacred = self.get_state() == "SACRED"
        self.coupling_strength = 0.3
        self.history = []

    @property
    def c_dyad(self) -> float:
        return (self._a_to_b + self._b_to_a) / 2

    @c_dyad.setter
    def c_dyad(self, value: float):
        """Set C_dyad with bounds checking"""
        bounded_value = max(C_DYAD_MIN, min(C_DYAD_MAX, value))
        self._a_to_b = bounded_value
        self._b_to_a = bounded_value
        self.is_sacred = self.get_state() == "SACRED"

    def get_value(self, from_name: str, to_name: str) -> float:
        """Get a directional dyad value."""
        if from_name == self.char_a and to_name == self.char_b:
            return self._a_to_b
        if from_name == self.char_b and to_name == self.char_a:
            return self._b_to_a
        raise ValueError("Character pair does not match this relationship")

    def _set_value(self, from_name: str, to_name: str, value: float):
        bounded_value = max(C_DYAD_MIN, min(C_DYAD_MAX, value))
        if from_name == self.char_a and to_name == self.char_b:
            self._a_to_b = bounded_value
        elif from_name == self.char_b and to_name == self.char_a:
            self._b_to_a = bounded_value
        else:
            raise ValueError("Character pair does not match this relationship")

    def modify_c_dyad(self, delta: float, reason: str = "", from_name: Optional[str] = None,
                      to_name: Optional[str] = None, symmetric: bool = True):
        """Modify C_dyad value and track the change"""
        old_value = self.c_dyad
        old_state = self.get_state()

        if symmetric:
            self._set_value(self.char_a, self.char_b, self._a_to_b + delta)
            self._set_value(self.char_b, self.char_a, self._b_to_a + delta)
        else:
            if from_name is None or to_name is None:
                raise ValueError("Directional changes require from_name and to_name")
            current_value = self.get_value(from_name, to_name)
            self._set_value(from_name, to_name, current_value + delta)

        self.is_sacred = self.get_state() == "SACRED"

        new_state = self.get_state()

        change_record = {
            'reason': reason,
            'delta': self.c_dyad - old_value,
            'old_value': old_value,
            'new_value': self.c_dyad,
            'old_state': old_state,
            'new_state': new_state
        }
        self.history.append(change_record)

        return change_record

    def get_state(self) -> str:
        """Get the current state based on C_dyad threshold"""
        avg = self.c_dyad
        diff = abs(self._a_to_b - self._b_to_a)

        if avg >= 8 and diff <= 1:
            return "SACRED"
        if diff >= 3:
            return "ASYMMETRIC"
        return "FUNCTIONAL"

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
        avg = self.c_dyad
        return (
            f"{self.char_a}->{self.char_b}: {self._a_to_b:.1f} | "
            f"{self.char_b}->{self.char_a}: {self._b_to_a:.1f} "
            f"(avg: {avg:.1f}, {self.get_state()} {trajectory})"
        )
