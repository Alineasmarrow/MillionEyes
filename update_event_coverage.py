"""
Add Farris and Daniel to Event Effects

This script identifies and modifies events to include Farris and Daniel where appropriate:
- Group/household/crew events should affect Farris
- DCE/institutional/pressure events should affect Daniel
"""

# Events that should include Farris (household/crew events)
FARRIS_EVENTS = [
    "bonfire_night",  # Group bonding
    "grace_moment",  # Moment of connection
    "thing_avoided_soft",  # Group tension
    "mission_wrong_low",  # Mission failure
    "mission_wrong_higher",  # Worse mission
    "trine_ritual_stable",  # Household ritual
    "trine_ritual_heavy",  # Strained ritual
    "trine_mistrust",  # Group fracture
    "maeve_memory_glitch",  # Household concern
    "kit_overextends",  # Someone overextends (Farris would notice)
    "case_shifts",  # Investigation affects everyone
    "yuul_forgets_date",  # Household moment
    "map_wont_stay_still",  # Paranormal event at home
    "quiet_town_watches",  # External pressure on group
    # Act 2
    "rielle_impulse_harder",  # Rielle's recklessness affects everyone
    "kit_panic_attack",  # Kit's crisis affects household
    "maeve_voice_slips",  # Maeve's instability
    "prophetic_collapse",  # Yuul's breakdown
    "something_breaks",  # Household object breaks
    "kettle_moment",  # Household domestic scene
    "trine_shatters",  # Major household fracture
    # Act 3
    "first_warning_returns",  # Group moment
    "photo_album_memory",  # Household memory
    "coherence_whiplash",  # Affects everyone present
    "house_that_hears",  # House/Sanctuary event
]

# Events that should include Daniel (DCE/institutional/pressure)
DANIEL_EVENTS = [
    "internal_suspicion",  # H11/institutional
    "soft_surveillance",  # DCE watching
    "soft_betrayal_h11",  # H11 institutional pressure
    "misaligned_questions",  # External questioning
    "quiet_town_watches",  # Surveillance pressure
    # Act 2
    "dce_warning",  # DCE directly involved
    "jurisdiction_fight",  # Institutional conflict (Daniel would be involved)
    "restraint_order",  # DCE legal action
    "someone_recognizes",  # Public exposure
    "dce_surveillance_intensifies",  # DCE directly tracking
    # Act 3
    "dce_restraint_order",  # DCE endgame
]

# Character name mapping
CHARACTER_NAMES = {
    "Yuul": "Yuul",
    "Maeve": "Maeve",
    "Kit": "Kit",
    "Rielle": "Rielle",
    "Farris": "Farris",
    "Daniel": "Daniel",
}


def generate_additions():
    """Generate code additions for events"""

    print("="*80)
    print("FARRIS ADDITIONS FOR GROUP EVENTS")
    print("="*80)
    print()
    print("Add these lines to group/household events:")
    print()
    print("# After existing character changes:")
    print("farris = sim.get_character('Farris')")
    print("if farris and not farris.is_dead:")
    print("    farris_change = sim.modify_character_c_self('Farris', [SAME_DELTA], [SAME_REASON])")
    print("    log.append(farris_change)")
    print()

    print("="*80)
    print("DANIEL ADDITIONS FOR DCE/INSTITUTIONAL EVENTS")
    print("="*80)
    print()
    print("Add these lines to DCE/pressure events:")
    print()
    print("# After existing character changes:")
    print("daniel = sim.get_character('Daniel')")
    print("if daniel and not daniel.is_dead:")
    print("    daniel_change = sim.modify_character_c_self('Daniel', [PRESSURE_DELTA], [REASON])")
    print("    log.append(daniel_change)")
    print()

    print("="*80)
    print("SPECIFIC EVENT RECOMMENDATIONS")
    print("="*80)
    print()

    # Provide specific recommendations
    recommendations = [
        ("bonfire_night", "Farris", "+1.0", "warmth and belonging"),
        ("grace_moment", "Farris", "+0.5", "shared moment of connection"),
        ("mission_wrong_low", "Farris", "-0.3", "coordination failure"),
        ("mission_wrong_higher", "Farris", "-0.8", "mission disaster"),
        ("soft_surveillance", "Daniel", "-0.5", "institutional pressure"),
        ("internal_suspicion", "Daniel", "-0.8", "H11 suspects something"),
        ("dce_warning", "Daniel", "-1.0", "caught between loyalties"),
    ]

    for event_id, char, delta, reason in recommendations:
        print(f"{event_id}:")
        print(f"  {char}: {delta} - '{reason}'")
        print()

    print("="*80)
    print("KEY PATTERNS")
    print("="*80)
    print()
    print("1. Farris should take ~same damage as crew in group events")
    print("2. Daniel should take pressure damage in DCE/institutional events")
    print("3. Always check if character exists and isn't dead")
    print("4. Match the emotional tone of the event")
    print()


if __name__ == "__main__":
    generate_additions()
