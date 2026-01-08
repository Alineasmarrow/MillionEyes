"""
Momentum System - Coherence breeds coherence, despair breeds despair

Two-layered system:
1. Individual Momentum - character-level resilience/spiral tracking
2. Field State - environmental pressure that affects everyone

Thematic: "Small wins compound. When things are going well,
people have capacity to heal faster."
"""


class MomentumTracker:
    """
    Tracks positive/negative streaks for individual characters

    Positive streaks reward resilience and growth
    Negative streaks create downward spiral effects
    """

    def __init__(self):
        self.positive_streak = 0
        self.negative_streak = 0

    def update(self, event_was_positive: bool):
        """
        Update streak based on event outcome

        Args:
            event_was_positive: True if character gained coherence, False if lost
        """
        if event_was_positive:
            self.positive_streak += 1
            self.negative_streak = 0
        else:
            self.negative_streak += 1
            self.positive_streak = 0

    def get_coherence_modifier(self) -> float:
        """
        Returns multiplier for C_self gains

        Positive streaks amplify healing
        Returns 1.0 (no effect) for neutral/negative streaks
        """
        if self.positive_streak >= 3:
            return 1.5  # 50% bonus - "momentum carries them"
        elif self.positive_streak == 2:
            return 1.25  # 25% bonus - "building strength"
        else:
            return 1.0  # Normal

    def get_chaos_modifier(self) -> float:
        """
        Returns modifier for chaos accumulation during negative streaks

        Negative streaks amplify chaos (spiral effect)
        Returns 1.0 (no effect) for neutral/positive streaks
        """
        if self.negative_streak >= 3:
            return 1.3  # 30% more chaos - "free fall"
        elif self.negative_streak == 2:
            return 1.15  # 15% more chaos - "losing grip"
        else:
            return 1.0  # Normal

    def reset(self):
        """Reset all streaks (used for major events/act transitions)"""
        self.positive_streak = 0
        self.negative_streak = 0

    def get_state_description(self) -> str:
        """Get human-readable state description"""
        if self.positive_streak >= 3:
            return f"Building momentum (+{self.positive_streak})"
        elif self.positive_streak == 2:
            return f"Gaining strength (+{self.positive_streak})"
        elif self.negative_streak >= 3:
            return f"Spiraling down (-{self.negative_streak})"
        elif self.negative_streak == 2:
            return f"Struggling (-{self.negative_streak})"
        else:
            return "Neutral"


class FieldState:
    """
    Environmental field state that affects all characters

    Tracks overall narrative momentum - are things generally
    improving or deteriorating?
    """

    STATES = ["descending", "neutral", "ascending"]

    def __init__(self):
        self.state = "neutral"  # Current field state
        self.duration = 0  # How many rounds in current state
        self.positive_count = 0  # Positive events this round
        self.negative_count = 0  # Negative events this round

    def update_from_round(self, positive_count: int, negative_count: int):
        """
        Update field state based on round outcomes

        Args:
            positive_count: Number of positive character changes this round
            negative_count: Number of negative character changes this round
        """
        self.positive_count = positive_count
        self.negative_count = negative_count

        # Determine new state
        net_change = positive_count - negative_count

        if net_change >= 2:
            new_state = "ascending"
        elif net_change <= -2:
            new_state = "descending"
        else:
            new_state = "neutral"

        # Update duration
        if new_state == self.state:
            self.duration += 1
        else:
            self.state = new_state
            self.duration = 1

    def get_coherence_modifier(self) -> float:
        """
        Returns multiplier for all coherence gains

        Ascending field amplifies healing
        """
        if self.state == "ascending" and self.duration >= 3:
            return 1.2  # 20% bonus - sustained hope
        elif self.state == "ascending" and self.duration >= 2:
            return 1.15  # 15% bonus - building hope
        else:
            return 1.0  # No field bonus

    def get_chaos_modifier(self) -> float:
        """
        Returns modifier for chaos accumulation

        Descending field amplifies chaos
        """
        if self.state == "descending" and self.duration >= 3:
            return 1.25  # 25% more chaos - sustained crisis
        elif self.state == "descending" and self.duration >= 2:
            return 1.15  # 15% more chaos - building crisis
        else:
            return 1.0  # No field penalty

    def reset(self):
        """Reset field state (used for act transitions)"""
        self.state = "neutral"
        self.duration = 0
        self.positive_count = 0
        self.negative_count = 0

    def get_state_description(self) -> str:
        """Get human-readable state description"""
        if self.state == "ascending":
            return f"Ascending ({self.duration} rounds) - Hope builds"
        elif self.state == "descending":
            return f"Descending ({self.duration} rounds) - Crisis deepens"
        else:
            return "Neutral - Equilibrium"


def calculate_stacked_modifier(character_modifier: float, field_modifier: float) -> float:
    """
    Calculate final modifier by stacking character and field effects multiplicatively

    Example:
        Character momentum: 1.25x
        Field state: 1.15x
        Stacked: 1.25 × 1.15 = 1.44x

    Args:
        character_modifier: From character's MomentumTracker
        field_modifier: From FieldState

    Returns:
        Stacked multiplier
    """
    return character_modifier * field_modifier


def get_momentum_display(character_mod: float, field_mod: float) -> str:
    """
    Generate display string for momentum bonuses

    Args:
        character_mod: Character momentum modifier
        field_mod: Field state modifier

    Returns:
        Display string like "+44% (momentum +25%, field +15%)"
    """
    if character_mod == 1.0 and field_mod == 1.0:
        return ""

    stacked = calculate_stacked_modifier(character_mod, field_mod)
    total_bonus = (stacked - 1.0) * 100

    parts = []
    if character_mod > 1.0:
        char_bonus = (character_mod - 1.0) * 100
        parts.append(f"momentum +{char_bonus:.0f}%")
    if field_mod > 1.0:
        field_bonus = (field_mod - 1.0) * 100
        parts.append(f"field +{field_bonus:.0f}%")

    detail = ", ".join(parts)
    return f"+{total_bonus:.0f}% ({detail})"
