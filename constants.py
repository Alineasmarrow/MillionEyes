"""
Constants and thresholds for the Narrative Coherence Engine
"""

# System constants
CHAOS_THRESHOLD = 20.0  # CoR manifestation point
CHAOS_WARNING_THRESHOLD = 16.0  # 80% of max, warnings trigger

C_SELF_MIN = 0.0  # Floor (dissolution/death)
C_SELF_MAX = 10.0  # Ceiling (transcendence)

C_DYAD_MIN = 0.0  # Floor (severance)
C_DYAD_MAX = 10.0  # Ceiling (mythic bond)

WITCH_TRINE_IDEAL = 8.0  # Average C needed for Trine to function
WITCH_TRINE_FAILURE = 6.0  # Below this = Trine unstable

SACRED_BOND_THRESHOLD = 9.0  # When dyad becomes sacred
RUPTURE_THRESHOLD = 3.0  # When dyad enters danger zone
SEVERANCE_VALUE = 0.0  # Complete bond destruction

# Character state thresholds (ordered from highest to lowest)
CHARACTER_STATE_THRESHOLDS = [
    (9.0, "Transcendent"),
    (7.0, "Stable"),
    (5.0, "Functional"),
    (4.0, "Strained"),
    (3.0, "Crisis"),
    (1.0, "Dissolving"),
    (0.0, "Gone"),
]

# Relationship state thresholds (ordered from highest to lowest)
RELATIONSHIP_STATE_THRESHOLDS = [
    (10.0, "MYTHIC"),
    (9.0, "SACRED"),
    (7.0, "Strong"),
    (5.0, "Functional"),
    (3.0, "STRAINED"),
    (1.0, "RUPTURE ZONE"),
    (0.0, "SEVERED"),
]

# Witch Trine configuration
WITCH_TRINE_MEMBERS = ["Maeve", "Yuul", "Rielle"]
WITCH_TRINE_DYADS = [
    ("Maeve", "Yuul"),
    ("Maeve", "Rielle"),
    ("Yuul", "Rielle")
]
