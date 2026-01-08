"""
Final Words System - Character's last words based on their strongest bond

When a character dies, they speak final words to the person they're most
connected to. Makes every death personal and tragic.
"""

# ============================================================================
# FINAL WORDS - MAEVE
# ============================================================================

MAEVE_TO_YUUL = '"I tried. I swear I tried to—"'
MAEVE_TO_KIT = '"Keep her safe. Please. Just... keep her—"'
MAEVE_TO_RIELLE = '"You were right. About all of it."'
MAEVE_TO_DANIEL = '"Tell them I wasn\'t—tell them it mattered."'
MAEVE_TO_FARRIS = '"Stay. Don\'t let them forget."'

# Sacred bond versions
MAEVE_TO_YUUL_SACRED = '"I see you. I finally see you. All of you."'
MAEVE_TO_RIELLE_MYTHIC = '"Don\'t let me go. Please. Don\'t—"'

# ============================================================================
# FINAL WORDS - YUUL
# ============================================================================

YUUL_TO_MAEVE = '"The fire. You have to—don\'t let it—"'
YUUL_TO_KIT = '"I\'m sorry. I\'m so sorry I couldn\'t stay."'
YUUL_TO_RIELLE = '"Burn it all. You know how."'
YUUL_TO_DANIEL = '"You never understood. That\'s okay."'

# Special cases
YUUL_DISSOLVING = "She mouths words in reverse. No one hears them."
YUUL_TO_KIT_SACRED = '"Wait for me. In the place between."'

# ============================================================================
# FINAL WORDS - KIT
# ============================================================================

KIT_TO_YUUL = '"I see you. I\'ve always seen you."'
KIT_TO_MAEVE = '"Don\'t blame yourself. Promise me."'
KIT_TO_RIELLE = '"Take care of them. Both of them."'
KIT_TO_DANIEL = '"You did what you thought was right."'
KIT_ALONE = '"At least I tried."'

# Sacred bond version
KIT_TO_YUUL_SACRED = '"I\'ll find you. Even in the after. I promise."'

# ============================================================================
# FINAL WORDS - RIELLE
# ============================================================================

RIELLE_TO_MAEVE = '"I loved you, you know. Just... differently."'
RIELLE_TO_YUUL = '"I\'m sorry I couldn\'t fix it."'
RIELLE_TO_KIT = '"You\'re better than all of us. Don\'t forget that."'
RIELLE_TO_DANIEL = '"Fuck your protocols."'
RIELLE_ALONE = '"Fine. I\'ll burn alone then."'

# ============================================================================
# FINAL WORDS - DANIEL
# ============================================================================

DANIEL_TO_MAEVE = '"I thought I was helping. I really did."'
DANIEL_TO_KIT = '"I\'m sorry. God, I\'m so sorry."'
DANIEL_TO_YUUL = '"I should have listened."'
DANIEL_TO_RIELLE = '"You were right to hate me."'
DANIEL_ALONE = '"Protocol... protocol seventeen, section—"'

# ============================================================================
# FINAL WORDS - FARRIS
# ============================================================================

FARRIS_TO_MAEVE = '"It was always you. Every version. Every timeline."'
FARRIS_DEVOURER_DEATH = '"Worth it. You\'re still here."'
FARRIS_REALITY_FRACTURE = '"I\'m not leaving. I\'m becoming the door."'

# ============================================================================
# FINAL WORDS MAPPING
# ============================================================================

# Standard final words (character, partner) -> words
FINAL_WORDS = {
    # Maeve
    ("Maeve", "Yuul"): MAEVE_TO_YUUL,
    ("Maeve", "Kit"): MAEVE_TO_KIT,
    ("Maeve", "Rielle"): MAEVE_TO_RIELLE,
    ("Maeve", "Daniel"): MAEVE_TO_DANIEL,
    ("Maeve", "Farris"): MAEVE_TO_FARRIS,

    # Yuul
    ("Yuul", "Maeve"): YUUL_TO_MAEVE,
    ("Yuul", "Kit"): YUUL_TO_KIT,
    ("Yuul", "Rielle"): YUUL_TO_RIELLE,
    ("Yuul", "Daniel"): YUUL_TO_DANIEL,

    # Kit
    ("Kit", "Yuul"): KIT_TO_YUUL,
    ("Kit", "Maeve"): KIT_TO_MAEVE,
    ("Kit", "Rielle"): KIT_TO_RIELLE,
    ("Kit", "Daniel"): KIT_TO_DANIEL,

    # Rielle
    ("Rielle", "Maeve"): RIELLE_TO_MAEVE,
    ("Rielle", "Yuul"): RIELLE_TO_YUUL,
    ("Rielle", "Kit"): RIELLE_TO_KIT,
    ("Rielle", "Daniel"): RIELLE_TO_DANIEL,

    # Daniel
    ("Daniel", "Maeve"): DANIEL_TO_MAEVE,
    ("Daniel", "Kit"): DANIEL_TO_KIT,
    ("Daniel", "Yuul"): DANIEL_TO_YUUL,
    ("Daniel", "Rielle"): DANIEL_TO_RIELLE,

    # Farris
    ("Farris", "Maeve"): FARRIS_TO_MAEVE,
}

# Sacred bond final words (C ≥ 9.0)
SACRED_FINAL_WORDS = {
    ("Kit", "Yuul"): KIT_TO_YUUL_SACRED,
    ("Yuul", "Kit"): YUUL_TO_KIT_SACRED,
    ("Maeve", "Yuul"): MAEVE_TO_YUUL_SACRED,
    ("Maeve", "Rielle"): MAEVE_TO_RIELLE_MYTHIC,
}

# Dying alone final words
ALONE_FINAL_WORDS = {
    "Kit": KIT_ALONE,
    "Rielle": RIELLE_ALONE,
    "Daniel": DANIEL_ALONE,
    "Yuul": YUUL_DISSOLVING,
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_highest_dyad_partner(character_name: str, dyads: list) -> tuple:
    """
    Find the character's strongest remaining bond

    Args:
        character_name: Name of dying character
        dyads: List of Relationship objects

    Returns:
        (partner_name, dyad_value) or (None, 0) if no bonds exist
    """
    highest_partner = None
    highest_value = 0.0

    for dyad in dyads:
        if dyad.char_a == character_name or dyad.char_b == character_name:
            if dyad.c_dyad > highest_value:
                highest_value = dyad.c_dyad
                # Get the other character in the dyad
                highest_partner = dyad.char_b if dyad.char_a == character_name else dyad.char_a

    return (highest_partner, highest_value)


def get_final_words(character_name: str, partner_name: str, dyad_value: float) -> str:
    """
    Get appropriate final words based on relationship

    Args:
        character_name: Name of dying character
        partner_name: Name of their strongest bond (or None)
        dyad_value: Strength of that bond

    Returns:
        Final words string
    """
    # Check if dying alone
    if partner_name is None:
        return ALONE_FINAL_WORDS.get(character_name, f"{character_name} falls silent.")

    # Check for sacred bond (C ≥ 9.0)
    if dyad_value >= 9.0:
        sacred_key = (character_name, partner_name)
        if sacred_key in SACRED_FINAL_WORDS:
            return SACRED_FINAL_WORDS[sacred_key]

    # Standard final words
    key = (character_name, partner_name)
    return FINAL_WORDS.get(key, f'"{partner_name}... I—"')


def display_final_words(character_name: str, partner_name: str, dyad_value: float):
    """
    Display the full final words sequence

    Args:
        character_name: Name of dying character
        partner_name: Name of their strongest bond (or None)
        dyad_value: Strength of that bond
    """
    final_words = get_final_words(character_name, partner_name, dyad_value)

    print(f"\n{'='*60}")
    print(f"💀 {character_name} falls.")
    print(f"{'='*60}\n")

    if partner_name:
        print(f"{character_name} looks to {partner_name}.")
        print(f"{final_words}")
    else:
        print(final_words)

    print(f"\n{character_name} is gone.\n")
