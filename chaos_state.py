"""
Textured Chaos System - Field Bias

Splits chaos into two components:
- Turbulence: Randomness, stress, entropy
- Pressure: Directional force, control/collapse
"""

class ChaosState:
    """Represents the two-dimensional chaos state"""

    def __init__(self, turbulence: float = 0.0, pressure: float = 0.0):
        self.turbulence = turbulence
        self.pressure = pressure

    @property
    def total(self) -> float:
        """Total chaos = turbulence + pressure"""
        return self.turbulence + self.pressure

    @property
    def dominant_field(self) -> str:
        """Determine which field type is dominant"""
        if self.turbulence == 0 and self.pressure == 0:
            return "BALANCED"

        ratio = self.pressure / max(self.turbulence, 0.1)

        if ratio > 1.5:
            return "PRESSURE_DOMINANT"  # Control/erasure
        elif ratio < 0.66:
            return "TURBULENCE_DOMINANT"  # Chaos/dissolution
        else:
            return "BALANCED"  # Both forces

    def add_turbulence(self, amount: float):
        """Add turbulence to the system"""
        self.turbulence += amount

    def add_pressure(self, amount: float):
        """Add pressure to the system"""
        self.pressure += amount

    def add_hybrid(self, turbulence: float, pressure: float):
        """Add both turbulence and pressure"""
        self.turbulence += turbulence
        self.pressure += pressure

    def get_field_effects(self) -> dict:
        """Get the active field effects based on dominant type"""
        field_type = self.dominant_field

        if field_type == "TURBULENCE_DOMINANT":
            return {
                "type": "🌀 TURBULENT FIELD",
                "variance_modifier": 1.2,  # ±20% variance on outcomes
                "wild_card_boost": 1.3,  # Wild card probability +30%
                "sacred_fluctuation": True,  # Sacred bonds fluctuate
                "cor_type": "DISSOLUTION",
                "description": "Chaotic but survivable, nothing stable"
            }
        elif field_type == "PRESSURE_DOMINANT":
            return {
                "type": "⚡ PRESSURE FIELD",
                "choice_limit": -1,  # One fewer option at key moments
                "external_boost": 1.5,  # External control events +50%
                "recovery_penalty": 0.7,  # Recovery -30% effectiveness
                "cor_type": "CONTROL",
                "description": "Rigid, suffocating, surveillance"
            }
        else:  # BALANCED
            return {
                "type": "⚖️ CONTESTED FIELD",
                "reality_torn": True,  # Reality torn between order and chaos
                "both_manifestations": True,  # Both CoR types possible
                "player_determines": True,  # Player choices determine which wins
                "cor_type": "HYBRID",
                "description": "Most dangerous state - reality undecided"
            }

    def __repr__(self):
        return f"ChaosState(turbulence={self.turbulence:.1f}, pressure={self.pressure:.1f}, total={self.total:.1f})"


# Event chaos categorization
EVENT_CHAOS_TYPES = {
    # High Turbulence
    7: {"turbulence": 2.0, "pressure": 0.0},  # Kit Overextends
    11: {"turbulence": 3.0, "pressure": 0.0},  # Mission Goes Wrong
    19: {"turbulence": 2.0, "pressure": 0.0},  # Rielle's Impulse
    6: {"turbulence": 2.0, "pressure": 0.0},  # Someone Notices

    # High Pressure
    12: {"turbulence": 0.0, "pressure": 4.0},  # DCE Investigation
    2: {"turbulence": 0.0, "pressure": 2.0},  # Prophetic Isolation
    8: {"turbulence": 0.0, "pressure": 4.0},  # Trine Ritual (fail = pressure)
    17: {"turbulence": 0.0, "pressure": 4.0},  # Redchurch Warning

    # Hybrid
    4: {"turbulence": 2.0, "pressure": 3.0},  # Mirror Incident
    1: {"turbulence": 1.0, "pressure": 1.0},  # Yuul Vision Horror
    3: {"turbulence": 1.0, "pressure": 1.0},  # Yuul Speaks Reversals
    13: {"turbulence": 1.5, "pressure": 1.5},  # Thing They've Been Avoiding

    # Low chaos / balanced
    5: {"turbulence": 0.0, "pressure": -0.5},  # Kit Grounds Yuul (stabilizing)
    14: {"turbulence": -1.0, "pressure": -1.0},  # Bonfire Night (reduces both)
    16: {"turbulence": 0.0, "pressure": -0.5},  # Maeve Reaches Out
    20: {"turbulence": -0.5, "pressure": -0.5},  # Grace Moment

    # Neutral/story-specific
    9: {"turbulence": 0.5, "pressure": 0.5},  # Rielle Questions Maeve
    10: {"turbulence": 1.5, "pressure": 1.5},  # Yuul's Last Prophecy
    15: {"turbulence": 0.5, "pressure": 0.5},  # Kit Confesses
    18: {"turbulence": 1.0, "pressure": 1.0},  # Kit Makes Promise
}


def get_chaos_components(event_id: int, chaos_amount: float) -> tuple:
    """
    Get the turbulence and pressure components for an event

    Returns: (turbulence, pressure)
    """
    if event_id in EVENT_CHAOS_TYPES:
        components = EVENT_CHAOS_TYPES[event_id]
        return (components["turbulence"], components["pressure"])
    else:
        # Default: split evenly
        half = chaos_amount / 2.0
        return (half, half)
